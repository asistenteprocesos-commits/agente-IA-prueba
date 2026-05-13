from uuid import UUID

from sqlalchemy.orm import Session

from app.models.process_case import ProcessCaseModel
from app.schemas.process_deliverables import (
    FinalDeliverableCreate,
    FinalDeliverableResponse,
    ImplementationStepResponse,
)
from app.schemas.process_repository import ArtifactType, ProcessArtifactCreate
from app.services.process_analysis_service import ProcessAnalysisService
from app.services.process_redesign_service import ProcessRedesignService
from app.services.process_repository_service import ProcessRepositoryService
from app.services.process_simulation_service import ProcessSimulationService


class ProcessDeliverablesService:
    def __init__(self, db: Session) -> None:
        self.db = db

    def build_final_deliverable(
        self,
        case_id: UUID,
        payload: FinalDeliverableCreate | None = None,
    ) -> FinalDeliverableResponse | None:
        process_case = self.db.get(ProcessCaseModel, str(case_id))
        if process_case is None:
            return None

        analysis = ProcessAnalysisService(self.db).analyze_case(case_id)
        redesign = ProcessRedesignService(self.db).build_to_be_options(case_id)
        simulation = ProcessSimulationService(self.db).simulate_case(case_id)
        if analysis is None or redesign is None or simulation is None:
            return None

        recommended = redesign.comparison.recommended_option_title_es
        executive = (
            f"El caso {process_case.name} cuenta con analisis as-is, alternativas to-be y simulacion inicial. "
            f"La opcion recomendada es '{recommended}', con una reduccion estimada de "
            f"{simulation.comparison.cycle_time_reduction_percent}% del tiempo de ciclo frente al as-is."
        )
        technical = (
            f"El analisis obtuvo score {analysis.analysis_score}%. "
            f"Se identificaron {len(analysis.findings)} hallazgos, {len(analysis.metrics)} metrica(s), "
            f"{len(redesign.alternatives)} alternativa(s) to-be y {len(simulation.scenarios)} escenario(s). "
            "Los resultados son preliminares y requieren validacion humana antes de publicacion."
        )
        deliverable = FinalDeliverableResponse(
            case_id=UUID(process_case.id),
            executive_summary_es=executive,
            technical_summary_es=technical,
            implementation_plan=[
                ImplementationStepResponse(
                    order=1,
                    title_es="Validar as-is y hallazgos",
                    owner_es=process_case.owner or "Dueno del proceso",
                    timeframe_es="Semana 1",
                    deliverable_es="As-is aprobado y matriz de hallazgos validada",
                ),
                ImplementationStepResponse(
                    order=2,
                    title_es="Aprobar alternativa to-be",
                    owner_es="Comite de proceso",
                    timeframe_es="Semana 2",
                    deliverable_es="Opcion to-be seleccionada con riesgos aceptados",
                ),
                ImplementationStepResponse(
                    order=3,
                    title_es="Ejecutar piloto controlado",
                    owner_es="Equipo operativo y TI",
                    timeframe_es="Semanas 3-6",
                    deliverable_es="Piloto con metricas antes/despues",
                ),
                ImplementationStepResponse(
                    order=4,
                    title_es="Escalar y gobernar",
                    owner_es="Gobierno de procesos",
                    timeframe_es="Semanas 7-12",
                    deliverable_es="Proceso publicado, controles activos y seguimiento SLA",
                ),
            ],
            decision_points_es=[
                "Aprobar alcance final del as-is.",
                "Aprobar alternativa to-be recomendada.",
                "Aprobar riesgos residuales y controles compensatorios.",
                "Autorizar piloto o implementacion.",
            ],
            residual_risks_es=[
                risk.risk_es for risk in analysis.risks_controls if risk.status in {"unknown", "control_gap", "needs_validation"}
            ][:5]
            or ["No se identificaron riesgos residuales criticos en el analisis inicial."],
        )

        if payload and payload.persist:
            artifact = ProcessRepositoryService(self.db).create_artifact(
                case_id,
                ProcessArtifactCreate(
                    artifact_type=ArtifactType.final_report,
                    title=payload.title,
                    description="Informe final generado por el Agente Redactor.",
                    content=self._markdown(deliverable),
                    version="0.1.0",
                    change_summary="Informe final ejecutivo/tecnico inicial generado por agente.",
                    author=payload.author,
                ),
            )
            if artifact:
                deliverable.artifact_id = artifact.id
                deliverable.artifact_version_id = artifact.versions[0].id if artifact.versions else None

        return deliverable

    @staticmethod
    def _markdown(deliverable: FinalDeliverableResponse) -> str:
        plan = "\n".join(
            f"{step.order}. **{step.title_es}** ({step.timeframe_es}) - Responsable: {step.owner_es}. Entregable: {step.deliverable_es}."
            for step in deliverable.implementation_plan
        )
        decisions = "\n".join(f"- {item}" for item in deliverable.decision_points_es)
        risks = "\n".join(f"- {item}" for item in deliverable.residual_risks_es)
        return (
            "# Informe final generado por agente\n\n"
            "## Resumen ejecutivo\n"
            f"{deliverable.executive_summary_es}\n\n"
            "## Resumen tecnico\n"
            f"{deliverable.technical_summary_es}\n\n"
            "## Plan de implementacion\n"
            f"{plan}\n\n"
            "## Puntos de decision\n"
            f"{decisions}\n\n"
            "## Riesgos residuales\n"
            f"{risks}\n"
        )
