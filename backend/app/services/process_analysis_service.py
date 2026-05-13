import re
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.discovery import ProcessAsIsElementModel, ProcessInterviewModel
from app.models.process_case import ProcessCaseModel
from app.schemas.discovery import AsIsElementType
from app.schemas.process_analysis import (
    AnalysisFindingResponse,
    AnalysisMetricResponse,
    FindingSeverity,
    FindingType,
    ImprovementCandidateResponse,
    ProcessAnalysisReportCreate,
    ProcessAnalysisResponse,
    RiskControlResponse,
)
from app.schemas.process_repository import ArtifactType, ProcessArtifactCreate
from app.services.process_repository_service import ProcessRepositoryService


class ProcessAnalysisService:
    def __init__(self, db: Session) -> None:
        self.db = db

    def analyze_case(self, case_id: UUID) -> ProcessAnalysisResponse | None:
        process_case = self.db.get(ProcessCaseModel, str(case_id))
        if process_case is None:
            return None

        elements = self._elements(case_id)
        interviews = self._interviews(case_id)
        findings = self._build_findings(elements, interviews)
        metrics = self._extract_metrics(elements, interviews)
        risks_controls = self._build_risks_controls(elements)
        improvements = self._build_improvements(findings, elements)
        score = self._score(findings, metrics, risks_controls, improvements)

        return ProcessAnalysisResponse(
            case_id=UUID(process_case.id),
            analysis_score=score,
            findings=findings,
            metrics=metrics,
            risks_controls=risks_controls,
            improvement_candidates=improvements,
            next_actions_es=self._next_actions(score, findings, metrics, risks_controls),
        )

    def create_report(
        self,
        case_id: UUID,
        payload: ProcessAnalysisReportCreate,
    ) -> ProcessAnalysisResponse | None:
        analysis = self.analyze_case(case_id)
        if analysis is None:
            return None
        if payload.persist:
            ProcessRepositoryService(self.db).create_artifact(
                case_id,
                ProcessArtifactCreate(
                    artifact_type=ArtifactType.improvement_report,
                    title=payload.title,
                    description="Analisis as-is generado por el Agente Analista.",
                    content=self._analysis_markdown(analysis),
                    version="0.1.0",
                    change_summary="Analisis inicial de hallazgos, metricas, riesgos y mejoras.",
                    author=payload.author,
                ),
            )
        return analysis

    def _elements(self, case_id: UUID) -> list[ProcessAsIsElementModel]:
        statement = (
            select(ProcessAsIsElementModel)
            .where(ProcessAsIsElementModel.case_id == str(case_id))
            .order_by(ProcessAsIsElementModel.created_at.asc())
        )
        return list(self.db.scalars(statement).all())

    def _interviews(self, case_id: UUID) -> list[ProcessInterviewModel]:
        statement = (
            select(ProcessInterviewModel)
            .where(ProcessInterviewModel.case_id == str(case_id))
            .order_by(ProcessInterviewModel.created_at.asc())
        )
        return list(self.db.scalars(statement).all())

    @classmethod
    def _build_findings(
        cls,
        elements: list[ProcessAsIsElementModel],
        interviews: list[ProcessInterviewModel],
    ) -> list[AnalysisFindingResponse]:
        findings: list[AnalysisFindingResponse] = []
        text_units = cls._text_units(elements, interviews)

        for element in elements:
            text = cls._element_text(element)
            lowered = text.lower()
            if element.element_type == AsIsElementType.pain_point.value or cls._has_any(
                lowered,
                ("demora", "retraso", "cola", "cuello", "espera", "pendiente"),
            ):
                findings.append(
                    cls._finding(
                        FindingType.bottleneck,
                        "high" if cls._has_any(lowered, ("critico", "mucho", "10", "15", "20")) else "medium",
                        "Posible cuello de botella",
                        "Se detecta evidencia de espera, demora o acumulacion.",
                        text,
                        "Medir tiempo de espera por actividad y validar capacidad disponible.",
                        element.confidence_level,
                    )
                )
            if cls._has_any(lowered, ("reproceso", "devuelve", "error", "correccion", "falta")):
                findings.append(
                    cls._finding(
                        FindingType.waste,
                        "medium",
                        "Desperdicio por reproceso o informacion faltante",
                        "Hay senales de retrabajo, devoluciones o errores de entrada.",
                        text,
                        "Agregar validaciones tempranas y campos obligatorios antes de avanzar.",
                        element.confidence_level,
                    )
                )
            if cls._has_any(lowered, ("manual", "excel", "correo")):
                findings.append(
                    cls._finding(
                        FindingType.automation,
                        "medium",
                        "Oportunidad de automatizacion",
                        "El proceso usa soporte manual o herramientas no integradas.",
                        text,
                        "Evaluar formulario digital, workflow o integracion entre sistemas.",
                        element.confidence_level,
                    )
                )

        if not any(element.element_type == AsIsElementType.metric.value for element in elements):
            findings.append(
                cls._finding(
                    FindingType.data_gap,
                    "high",
                    "Falta informacion cuantitativa",
                    "No hay elementos de metrica registrados para sustentar impacto.",
                    None,
                    "Solicitar volumen, tiempos, SLA, capacidad y tasa de error antes de simular.",
                    "high",
                )
            )

        if not any(element.element_type == AsIsElementType.control.value for element in elements):
            findings.append(
                cls._finding(
                    FindingType.control_gap,
                    "medium",
                    "Controles no documentados",
                    "No hay controles registrados en el as-is.",
                    None,
                    "Mapear aprobaciones, validaciones, segregacion de funciones y evidencias.",
                    "medium",
                )
            )

        if not findings and text_units:
            findings.append(
                cls._finding(
                    FindingType.quality,
                    "low",
                    "Sin hallazgos criticos iniciales",
                    "La informacion capturada no evidencia problemas operativos fuertes todavia.",
                    text_units[0],
                    "Completar metricas y validar excepciones para confirmar.",
                    "low",
                )
            )
        return cls._dedupe_findings(findings)[:12]

    @classmethod
    def _extract_metrics(
        cls,
        elements: list[ProcessAsIsElementModel],
        interviews: list[ProcessInterviewModel],
    ) -> list[AnalysisMetricResponse]:
        metrics: list[AnalysisMetricResponse] = []
        for text in cls._text_units(elements, interviews):
            lowered = text.lower()
            for number, unit in re.findall(r"(\d+(?:[.,]\d+)?)\s*(dias|dia|horas|hora|h|%|por ciento|casos|solicitudes)", lowered):
                value = float(number.replace(",", "."))
                name = "Metrica operativa detectada"
                interpretation = "Dato cuantitativo util para validar impacto y priorizar mejoras."
                if unit in {"dias", "dia", "horas", "hora", "h"}:
                    name = "Tiempo de ciclo o espera"
                    interpretation = "Tiempo detectado; debe separarse entre trabajo, espera y reproceso."
                elif unit in {"%", "por ciento"}:
                    name = "Porcentaje operativo"
                    interpretation = "Porcentaje detectado; validar denominador y periodo de medicion."
                metrics.append(
                    AnalysisMetricResponse(
                        name_es=name,
                        value=value,
                        unit=unit,
                        source_es=cls._shorten(text),
                        interpretation_es=interpretation,
                    )
                )
        if not metrics:
            metrics.append(
                AnalysisMetricResponse(
                    name_es="Metricas pendientes",
                    value=None,
                    unit=None,
                    source_es="No se detectaron valores numericos en entrevistas o elementos as-is.",
                    interpretation_es="El analisis cuantitativo queda limitado hasta cargar tiempos, volumenes o SLA.",
                )
            )
        return metrics[:10]

    @classmethod
    def _build_risks_controls(cls, elements: list[ProcessAsIsElementModel]) -> list[RiskControlResponse]:
        controls = [element for element in elements if element.element_type == AsIsElementType.control.value]
        exceptions = [element for element in elements if element.element_type == AsIsElementType.exception.value]
        rules = [element for element in elements if element.element_type == AsIsElementType.business_rule.value]
        risks: list[RiskControlResponse] = []

        for exception in exceptions:
            risks.append(
                RiskControlResponse(
                    risk_es=f"Excepcion frecuente: {exception.name}",
                    control_es=controls[0].name if controls else None,
                    status="covered" if controls else "control_gap",
                    recommendation_es=(
                        "Validar si el control actual mitiga esta excepcion."
                        if controls
                        else "Definir control preventivo o validacion temprana para esta excepcion."
                    ),
                )
            )
        for rule in rules[:3]:
            risks.append(
                RiskControlResponse(
                    risk_es=f"Regla de negocio mal aplicada: {rule.name}",
                    control_es=controls[0].name if controls else None,
                    status="needs_validation",
                    recommendation_es="Confirmar dueno, criterio, umbral y evidencia de aplicacion de la regla.",
                )
            )
        if not risks:
            risks.append(
                RiskControlResponse(
                    risk_es="Riesgos no identificados",
                    control_es=None,
                    status="unknown",
                    recommendation_es="Completar levantamiento con responsable de control interno o riesgo.",
                )
            )
        return risks

    @classmethod
    def _build_improvements(
        cls,
        findings: list[AnalysisFindingResponse],
        elements: list[ProcessAsIsElementModel],
    ) -> list[ImprovementCandidateResponse]:
        improvements: list[ImprovementCandidateResponse] = []
        if any(finding.finding_type == FindingType.bottleneck for finding in findings):
            improvements.append(
                ImprovementCandidateResponse(
                    title_es="Reducir esperas y colas",
                    impact_es="Alto si la mayor parte del ciclo es espera.",
                    effort_es="Medio: requiere medicion de capacidad, SLA y reglas de prioridad.",
                    risk_es="Puede mover el cuello de botella a otra area si no se balancea capacidad.",
                    evidence_es=cls._first_evidence(findings, FindingType.bottleneck),
                )
            )
        if any(finding.finding_type == FindingType.waste for finding in findings):
            improvements.append(
                ImprovementCandidateResponse(
                    title_es="Validacion temprana de datos",
                    impact_es="Medio-alto: reduce reproceso y devoluciones.",
                    effort_es="Bajo a medio: checklist, formulario o validacion automatica.",
                    risk_es="Si se endurecen validaciones, puede aumentar rechazo inicial.",
                    evidence_es=cls._first_evidence(findings, FindingType.waste),
                )
            )
        if any(finding.finding_type == FindingType.automation for finding in findings):
            improvements.append(
                ImprovementCandidateResponse(
                    title_es="Digitalizar handoffs manuales",
                    impact_es="Medio: mejora trazabilidad y reduce seguimiento por correo.",
                    effort_es="Medio: workflow, integracion o formulario unico.",
                    risk_es="Requiere gestion de cambio y control de accesos.",
                    evidence_es=cls._first_evidence(findings, FindingType.automation),
                )
            )
        if not improvements and elements:
            improvements.append(
                ImprovementCandidateResponse(
                    title_es="Completar analisis con datos reales",
                    impact_es="Depende de tiempos y volumenes.",
                    effort_es="Bajo: pedir metricas y event log simple.",
                    risk_es="Sin datos, la mejora puede ser solo cualitativa.",
                    evidence_es=None,
                )
            )
        return improvements

    @staticmethod
    def _score(
        findings: list[AnalysisFindingResponse],
        metrics: list[AnalysisMetricResponse],
        risks: list[RiskControlResponse],
        improvements: list[ImprovementCandidateResponse],
    ) -> int:
        score = 20
        score += min(30, len(findings) * 5)
        score += 20 if any(metric.value is not None for metric in metrics) else 5
        score += 15 if any(risk.status != "unknown" for risk in risks) else 5
        score += min(15, len(improvements) * 5)
        return min(score, 100)

    @staticmethod
    def _next_actions(
        score: int,
        findings: list[AnalysisFindingResponse],
        metrics: list[AnalysisMetricResponse],
        risks: list[RiskControlResponse],
    ) -> list[str]:
        actions: list[str] = []
        if not any(metric.value is not None for metric in metrics):
            actions.append("Solicitar tiempos, volumenes, SLA y tasa de reproceso.")
        if any(finding.severity in {FindingSeverity.high, FindingSeverity.critical} for finding in findings):
            actions.append("Validar hallazgos de severidad alta con el dueno del proceso.")
        if any(risk.status in {"unknown", "control_gap"} for risk in risks):
            actions.append("Completar matriz de riesgos y controles antes del to-be.")
        if score >= 70:
            actions.append("Preparar alternativas de mejora priorizadas para el Agente Redisenador.")
        else:
            actions.append("Completar evidencia cuantitativa antes de pasar a simulacion.")
        return actions

    @staticmethod
    def _analysis_markdown(analysis: ProcessAnalysisResponse) -> str:
        findings = "\n".join(
            f"- **{finding.title_es}** ({finding.severity}): {finding.recommendation_es}"
            for finding in analysis.findings
        )
        metrics = "\n".join(
            f"- {metric.name_es}: {metric.value if metric.value is not None else 'pendiente'} {metric.unit or ''}"
            for metric in analysis.metrics
        )
        improvements = "\n".join(
            f"- **{item.title_es}**: Impacto {item.impact_es}; esfuerzo {item.effort_es}."
            for item in analysis.improvement_candidates
        )
        return (
            "# Analisis as-is generado por agente\n\n"
            f"Score de analisis: {analysis.analysis_score}%\n\n"
            "## Hallazgos\n"
            f"{findings or '- Sin hallazgos.'}\n\n"
            "## Metricas\n"
            f"{metrics or '- Sin metricas.'}\n\n"
            "## Mejoras candidatas\n"
            f"{improvements or '- Sin mejoras.'}\n"
        )

    @staticmethod
    def _finding(
        finding_type: FindingType,
        severity: str,
        title: str,
        detail: str,
        evidence: str | None,
        recommendation: str,
        confidence: str,
    ) -> AnalysisFindingResponse:
        return AnalysisFindingResponse(
            finding_type=finding_type,
            severity=FindingSeverity(severity),
            title_es=title,
            detail_es=detail,
            evidence_es=evidence,
            recommendation_es=recommendation,
            confidence_level=confidence,
        )

    @classmethod
    def _dedupe_findings(cls, findings: list[AnalysisFindingResponse]) -> list[AnalysisFindingResponse]:
        seen: set[tuple[str, str]] = set()
        deduped: list[AnalysisFindingResponse] = []
        for finding in findings:
            key = (finding.finding_type.value, finding.title_es)
            if key in seen:
                continue
            seen.add(key)
            deduped.append(finding)
        return deduped

    @staticmethod
    def _has_any(text: str, keywords: tuple[str, ...]) -> bool:
        return any(keyword in text for keyword in keywords)

    @staticmethod
    def _element_text(element: ProcessAsIsElementModel) -> str:
        return " ".join(value for value in [element.name, element.description, element.source_excerpt] if value)

    @classmethod
    def _text_units(
        cls,
        elements: list[ProcessAsIsElementModel],
        interviews: list[ProcessInterviewModel],
    ) -> list[str]:
        units = [cls._element_text(element) for element in elements]
        units.extend(
            " ".join(value for value in [interview.objective, interview.questions, interview.notes, interview.summary] if value)
            for interview in interviews
        )
        return [unit for unit in units if unit.strip()]

    @staticmethod
    def _first_evidence(findings: list[AnalysisFindingResponse], finding_type: FindingType) -> str | None:
        for finding in findings:
            if finding.finding_type == finding_type and finding.evidence_es:
                return finding.evidence_es
        return None

    @staticmethod
    def _shorten(text: str, max_length: int = 260) -> str:
        cleaned = re.sub(r"\s+", " ", text).strip()
        if len(cleaned) <= max_length:
            return cleaned
        return f"{cleaned[: max_length - 3].rstrip()}..."
