from uuid import UUID

from sqlalchemy.orm import Session

from app.models.process_case import ProcessCaseModel
from app.schemas.process_analysis import FindingType
from app.schemas.process_redesign import (
    ProcessRedesignReportCreate,
    ProcessRedesignResponse,
    RedesignOptionType,
    ToBeAlternativeResponse,
    ToBeComparisonResponse,
)
from app.schemas.process_repository import ArtifactType, ProcessArtifactCreate
from app.services.process_analysis_service import ProcessAnalysisService
from app.services.process_repository_service import ProcessRepositoryService


class ProcessRedesignService:
    def __init__(self, db: Session) -> None:
        self.db = db

    def build_to_be_options(self, case_id: UUID) -> ProcessRedesignResponse | None:
        process_case = self.db.get(ProcessCaseModel, str(case_id))
        if process_case is None:
            return None

        analysis = ProcessAnalysisService(self.db).analyze_case(case_id)
        if analysis is None:
            return None

        finding_types = {finding.finding_type for finding in analysis.findings}
        alternatives: list[ToBeAlternativeResponse] = []

        if FindingType.waste in finding_types:
            alternatives.append(
                ToBeAlternativeResponse(
                    option_type=RedesignOptionType.quick_win,
                    title_es="Validacion temprana de solicitud",
                    description_es="Agregar checklist o formulario con campos obligatorios antes de iniciar el flujo formal.",
                    expected_impact_es="Reduce devoluciones y reproceso; impacto medio-alto si el problema es informacion faltante.",
                    effort_es="Bajo: plantilla, formulario o regla simple.",
                    risk_es="Puede aumentar rechazos al inicio si no se comunica bien.",
                    changes_es=[
                        "Estandarizar entrada de datos",
                        "Agregar validacion antes de asignar analista",
                        "Registrar motivo de devolucion",
                    ],
                    required_validation_es=[
                        "Validar campos obligatorios con el dueno del proceso",
                        "Confirmar que no se bloquee una excepcion legitima",
                    ],
                )
            )

        if FindingType.bottleneck in finding_types:
            alternatives.append(
                ToBeAlternativeResponse(
                    option_type=RedesignOptionType.structural,
                    title_es="Gestion por SLA y reglas de prioridad",
                    description_es="Redisenar colas y aprobaciones con prioridad, responsables claros y escalamiento por vencimiento.",
                    expected_impact_es="Alto sobre cycle time si la espera representa la mayor parte del proceso.",
                    effort_es="Medio: requiere metricas, responsables y tablero operativo.",
                    risk_es="Puede trasladar la carga a otro rol si no se balancea capacidad.",
                    changes_es=[
                        "Definir SLA por tipo de caso",
                        "Asignar cola visible por responsable",
                        "Escalar vencimientos automaticamente",
                    ],
                    required_validation_es=[
                        "Medir volumen por tipo de caso",
                        "Confirmar capacidad por rol",
                        "Aprobar reglas de escalamiento",
                    ],
                )
            )

        if FindingType.automation in finding_types:
            alternatives.append(
                ToBeAlternativeResponse(
                    option_type=RedesignOptionType.automation,
                    title_es="Workflow digital con trazabilidad",
                    description_es="Sustituir handoffs por correo/Excel por un flujo digital con estados, responsables y bitacora.",
                    expected_impact_es="Medio-alto en trazabilidad, control y reduccion de seguimiento manual.",
                    effort_es="Medio-alto: requiere herramienta workflow e integracion minima.",
                    risk_es="Riesgo de adopcion y datos maestros incompletos.",
                    changes_es=[
                        "Crear estados del proceso",
                        "Centralizar solicitud y documentos",
                        "Notificar automaticamente pendientes",
                    ],
                    required_validation_es=[
                        "Validar sistemas destino",
                        "Definir roles y permisos",
                        "Revisar privacidad y auditoria",
                    ],
                )
            )

        if any(risk.status in {"control_gap", "unknown", "needs_validation"} for risk in analysis.risks_controls):
            alternatives.append(
                ToBeAlternativeResponse(
                    option_type=RedesignOptionType.control,
                    title_es="Redisenio de controles por excepcion",
                    description_es="Mantener controles criticos, automatizar validaciones simples y enviar a aprobacion solo casos fuera de politica.",
                    expected_impact_es="Reduce aprobaciones innecesarias sin eliminar control interno.",
                    effort_es="Medio: requiere matriz de riesgo, umbrales y aprobacion de control.",
                    risk_es="Si los umbrales estan mal definidos, se puede aceptar riesgo no deseado.",
                    changes_es=[
                        "Clasificar controles criticos y redundantes",
                        "Definir umbrales de aprobacion",
                        "Registrar evidencia automatica de decision",
                    ],
                    required_validation_es=[
                        "Aprobacion de Control Interno o Finanzas",
                        "Prueba con casos historicos",
                    ],
                )
            )

        if not alternatives:
            alternatives.append(
                ToBeAlternativeResponse(
                    option_type=RedesignOptionType.quick_win,
                    title_es="Completar evidencia antes del redisenio",
                    description_es="El as-is no contiene suficientes hallazgos para proponer un to-be confiable.",
                    expected_impact_es="Evita redisenar sobre supuestos debiles.",
                    effort_es="Bajo: completar entrevistas y metricas.",
                    risk_es="Postergar diseno hasta tener evidencia minima.",
                    changes_es=["Solicitar metricas", "Validar excepciones", "Confirmar controles"],
                    required_validation_es=["Dueno del proceso confirma informacion faltante"],
                )
            )

        recommended = self._recommended(alternatives)
        return ProcessRedesignResponse(
            case_id=UUID(process_case.id),
            alternatives=alternatives,
            comparison=ToBeComparisonResponse(
                recommended_option_title_es=recommended.title_es,
                rationale_es=self._rationale(recommended),
                assumptions_es=[
                    "Las metricas detectadas deben validarse con fuentes operativas.",
                    "Ningun control critico se elimina sin aprobacion humana.",
                    "La alternativa final debe revisarse con las areas involucradas.",
                ],
            ),
            next_actions_es=[
                "Validar alternativas con el dueno del proceso.",
                "Seleccionar opcion candidata para modelado to-be.",
                "Preparar parametros para simulacion si existen tiempos y volumenes.",
            ],
        )

    def create_report(
        self,
        case_id: UUID,
        payload: ProcessRedesignReportCreate,
    ) -> ProcessRedesignResponse | None:
        redesign = self.build_to_be_options(case_id)
        if redesign is None:
            return None
        if payload.persist:
            ProcessRepositoryService(self.db).create_artifact(
                case_id,
                ProcessArtifactCreate(
                    artifact_type=ArtifactType.process_narrative_to_be,
                    title=payload.title,
                    description="Propuesta to-be generada por el Agente Redisenador.",
                    content=self._markdown(redesign),
                    version="0.1.0",
                    change_summary="Alternativas to-be iniciales generadas desde analisis as-is.",
                    author=payload.author,
                ),
            )
        return redesign

    @staticmethod
    def _recommended(alternatives: list[ToBeAlternativeResponse]) -> ToBeAlternativeResponse:
        priority = {
            RedesignOptionType.quick_win: 0,
            RedesignOptionType.control: 1,
            RedesignOptionType.structural: 2,
            RedesignOptionType.automation: 3,
        }
        return sorted(alternatives, key=lambda item: priority[item.option_type])[0]

    @staticmethod
    def _rationale(option: ToBeAlternativeResponse) -> str:
        if option.option_type == RedesignOptionType.quick_win:
            return "Se recomienda iniciar con quick wins para reducir reproceso y aumentar calidad de datos con bajo esfuerzo."
        if option.option_type == RedesignOptionType.control:
            return "Se recomienda estabilizar controles antes de automatizar para no aumentar riesgo operativo."
        if option.option_type == RedesignOptionType.structural:
            return "Se recomienda si el problema dominante es espera, cola o capacidad."
        return "Se recomienda cuando ya existen reglas claras y sistemas disponibles para digitalizar."

    @staticmethod
    def _markdown(redesign: ProcessRedesignResponse) -> str:
        alternatives = "\n\n".join(
            "\n".join(
                [
                    f"### {item.title_es}",
                    f"- Tipo: {item.option_type}",
                    f"- Descripcion: {item.description_es}",
                    f"- Impacto: {item.expected_impact_es}",
                    f"- Esfuerzo: {item.effort_es}",
                    f"- Riesgo: {item.risk_es}",
                    "- Cambios:",
                    *[f"  - {change}" for change in item.changes_es],
                ]
            )
            for item in redesign.alternatives
        )
        return (
            "# Propuesta to-be generada por agente\n\n"
            f"Recomendacion: **{redesign.comparison.recommended_option_title_es}**\n\n"
            f"{redesign.comparison.rationale_es}\n\n"
            "## Alternativas\n\n"
            f"{alternatives}\n"
        )
