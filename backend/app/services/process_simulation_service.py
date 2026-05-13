from uuid import UUID

from sqlalchemy.orm import Session

from app.models.process_case import ProcessCaseModel
from app.schemas.process_redesign import RedesignOptionType
from app.schemas.process_repository import ArtifactType, ProcessArtifactCreate
from app.schemas.process_simulation import (
    ProcessSimulationReportCreate,
    ProcessSimulationResponse,
    SensitivityPointResponse,
    SimulationComparisonResponse,
    SimulationScenarioResponse,
)
from app.services.process_analysis_service import ProcessAnalysisService
from app.services.process_redesign_service import ProcessRedesignService
from app.services.process_repository_service import ProcessRepositoryService


class ProcessSimulationService:
    def __init__(self, db: Session) -> None:
        self.db = db

    def simulate_case(self, case_id: UUID) -> ProcessSimulationResponse | None:
        process_case = self.db.get(ProcessCaseModel, str(case_id))
        if process_case is None:
            return None

        analysis = ProcessAnalysisService(self.db).analyze_case(case_id)
        redesign = ProcessRedesignService(self.db).build_to_be_options(case_id)
        if analysis is None or redesign is None:
            return None

        baseline_hours = self._baseline_hours(analysis.metrics)
        baseline_effort = max(1.0, baseline_hours * 0.35)
        scenarios = [
            SimulationScenarioResponse(
                name_es="As-is base",
                cycle_time_hours=round(baseline_hours, 2),
                manual_effort_hours=round(baseline_effort, 2),
                cost_index=100.0,
                sla_risk=self._sla_risk(baseline_hours),
                assumptions_es=[
                    "Se usa la metrica de tiempo detectada o un valor proxy si falta informacion.",
                    "El esfuerzo manual se estima como 35% del tiempo de ciclo si no hay dato directo.",
                ],
            )
        ]

        for alternative in redesign.alternatives:
            reduction = self._reduction_factor(alternative.option_type)
            effort_reduction = min(0.65, reduction + 0.1)
            cycle_time = baseline_hours * (1 - reduction)
            manual_effort = baseline_effort * (1 - effort_reduction)
            scenarios.append(
                SimulationScenarioResponse(
                    name_es=alternative.title_es,
                    cycle_time_hours=round(cycle_time, 2),
                    manual_effort_hours=round(max(0.5, manual_effort), 2),
                    cost_index=round(100 * (1 - reduction * 0.75), 2),
                    sla_risk=self._sla_risk(cycle_time),
                    assumptions_es=[
                        f"Reduccion estimada por alternativa {alternative.option_type}: {round(reduction * 100)}%.",
                        "Estimacion inicial; requiere calibracion con datos reales o event log.",
                    ],
                )
            )

        best = min(scenarios[1:] or scenarios, key=lambda scenario: scenario.cycle_time_hours)
        reduction_percent = round(((baseline_hours - best.cycle_time_hours) / baseline_hours) * 100) if baseline_hours else 0
        return ProcessSimulationResponse(
            case_id=UUID(process_case.id),
            scenarios=scenarios,
            comparison=SimulationComparisonResponse(
                baseline_cycle_time_hours=round(baseline_hours, 2),
                best_cycle_time_hours=best.cycle_time_hours,
                cycle_time_reduction_percent=max(0, reduction_percent),
                recommended_scenario_es=best.name_es,
                interpretation_es="Resultado preliminar para orientar decision; no reemplaza simulacion discreta calibrada.",
            ),
            sensitivity=[
                SensitivityPointResponse(
                    variable_es="Volumen de casos",
                    low_case_es="Si baja 20%, la mejora puede verse menos urgente.",
                    base_case_es="Usar volumen promedio actual.",
                    high_case_es="Si sube 20%, priorizar capacidad y automatizacion.",
                ),
                SensitivityPointResponse(
                    variable_es="Tiempo de aprobacion",
                    low_case_es="Si aprobacion ya es rapida, quick wins pueden bastar.",
                    base_case_es="Usar tiempo actual detectado.",
                    high_case_es="Si aprobacion domina el ciclo, usar SLA y escalamiento.",
                ),
                SensitivityPointResponse(
                    variable_es="Tasa de reproceso",
                    low_case_es="Si es baja, enfocar trazabilidad.",
                    base_case_es="Usar tasa historica validada.",
                    high_case_es="Si es alta, priorizar validacion temprana.",
                ),
            ],
            next_actions_es=[
                "Validar supuestos con el dueno del proceso.",
                "Cargar event log o tiempos por actividad para calibrar simulacion.",
                "Comparar escenario recomendado con riesgo y esfuerzo antes de aprobar to-be.",
            ],
        )

    def create_report(
        self,
        case_id: UUID,
        payload: ProcessSimulationReportCreate,
    ) -> ProcessSimulationResponse | None:
        simulation = self.simulate_case(case_id)
        if simulation is None:
            return None
        if payload.persist:
            ProcessRepositoryService(self.db).create_artifact(
                case_id,
                ProcessArtifactCreate(
                    artifact_type=ArtifactType.simulation_result,
                    title=payload.title,
                    description="Simulacion inicial generada por el Agente Simulador.",
                    content=self._markdown(simulation),
                    version="0.1.0",
                    change_summary="Escenarios iniciales as-is vs to-be con sensibilidad basica.",
                    author=payload.author,
                ),
            )
        return simulation

    @staticmethod
    def _baseline_hours(metrics) -> float:
        for metric in metrics:
            if metric.value is None or metric.unit is None:
                continue
            unit = metric.unit.lower()
            if unit in {"dias", "dia"}:
                return max(1.0, metric.value * 8)
            if unit in {"horas", "hora", "h"}:
                return max(1.0, metric.value)
        return 80.0

    @staticmethod
    def _reduction_factor(option_type: RedesignOptionType) -> float:
        return {
            RedesignOptionType.quick_win: 0.2,
            RedesignOptionType.control: 0.15,
            RedesignOptionType.structural: 0.4,
            RedesignOptionType.automation: 0.5,
        }[option_type]

    @staticmethod
    def _sla_risk(cycle_time_hours: float) -> str:
        if cycle_time_hours <= 16:
            return "low"
        if cycle_time_hours <= 80:
            return "medium"
        return "high"

    @staticmethod
    def _markdown(simulation: ProcessSimulationResponse) -> str:
        scenarios = "\n".join(
            f"- **{scenario.name_es}**: {scenario.cycle_time_hours}h ciclo, {scenario.manual_effort_hours}h esfuerzo, riesgo SLA {scenario.sla_risk}."
            for scenario in simulation.scenarios
        )
        return (
            "# Simulacion inicial generada por agente\n\n"
            f"Escenario recomendado: **{simulation.comparison.recommended_scenario_es}**\n\n"
            f"Reduccion estimada: {simulation.comparison.cycle_time_reduction_percent}%\n\n"
            "## Escenarios\n"
            f"{scenarios}\n"
        )
