import re
from uuid import UUID, uuid4

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models.discovery import (
    ProcessAsIsElementModel,
    ProcessInterviewModel,
    ProcessStakeholderModel,
)
from app.models.process_case import ProcessCaseModel
from app.schemas.discovery import (
    AsIsElementType,
    ConfidenceLevel,
    DiscoveryAssessmentResponse,
    DiscoveryCompletenessDimensionResponse,
    DiscoveryContradictionResponse,
    DiscoveryGapResponse,
    DiscoveryQuestionResponse,
    InterviewGuideResponse,
    InterviewGuideSection,
    InterviewStatus,
    ProcessAsIsElementCreate,
    ProcessAsIsElementResponse,
    ProcessInterviewCreate,
    ProcessInterviewResponse,
    ProcessStakeholderCreate,
    ProcessStakeholderResponse,
    StakeholderInfluenceLevel,
    StakeholderRole,
)
from app.schemas.process_case import ProcessCaseStatus


class DiscoveryValidationError(ValueError):
    pass


class ProcessDiscoveryService:
    def __init__(self, db: Session) -> None:
        self.db = db

    def list_stakeholders(self, case_id: UUID) -> list[ProcessStakeholderResponse] | None:
        if self._get_case(case_id) is None:
            return None

        statement = (
            select(ProcessStakeholderModel)
            .where(ProcessStakeholderModel.case_id == str(case_id))
            .order_by(ProcessStakeholderModel.created_at.desc())
        )
        stakeholders = self.db.scalars(statement).all()
        return [self._stakeholder_to_response(stakeholder) for stakeholder in stakeholders]

    def create_stakeholder(
        self,
        case_id: UUID,
        payload: ProcessStakeholderCreate,
    ) -> ProcessStakeholderResponse | None:
        process_case = self._get_case(case_id)
        if process_case is None:
            return None

        stakeholder = ProcessStakeholderModel(
            id=str(uuid4()),
            case_id=process_case.id,
            name=payload.name,
            role=payload.role.value,
            area=payload.area,
            email=payload.email,
            influence_level=payload.influence_level.value,
            availability=payload.availability,
            notes=payload.notes,
        )
        self._mark_case_in_discovery(process_case)
        self.db.add(stakeholder)
        self.db.commit()
        self.db.refresh(stakeholder)
        return self._stakeholder_to_response(stakeholder)

    def list_interviews(self, case_id: UUID) -> list[ProcessInterviewResponse] | None:
        if self._get_case(case_id) is None:
            return None

        statement = (
            select(ProcessInterviewModel)
            .where(ProcessInterviewModel.case_id == str(case_id))
            .options(selectinload(ProcessInterviewModel.stakeholder))
            .order_by(ProcessInterviewModel.created_at.desc())
        )
        interviews = self.db.scalars(statement).all()
        return [self._interview_to_response(interview) for interview in interviews]

    def create_interview(
        self,
        case_id: UUID,
        payload: ProcessInterviewCreate,
    ) -> ProcessInterviewResponse | None:
        process_case = self._get_case(case_id)
        if process_case is None:
            return None

        stakeholder = None
        if payload.stakeholder_id is not None:
            stakeholder = self.db.get(ProcessStakeholderModel, str(payload.stakeholder_id))
            if stakeholder is None or stakeholder.case_id != process_case.id:
                raise DiscoveryValidationError("Stakeholder does not belong to this case")

        interview = ProcessInterviewModel(
            id=str(uuid4()),
            case_id=process_case.id,
            stakeholder_id=stakeholder.id if stakeholder else None,
            title=payload.title,
            interview_type=payload.interview_type.value,
            status=payload.status.value,
            scheduled_at=payload.scheduled_at,
            objective=payload.objective,
            questions=payload.questions,
            notes=payload.notes,
            summary=payload.summary,
        )
        self._mark_case_in_discovery(process_case)
        self.db.add(interview)
        self.db.commit()
        self.db.refresh(interview)
        return self._interview_to_response(interview)

    def generate_interview_guide(self, case_id: UUID) -> InterviewGuideResponse | None:
        process_case = self._get_case(case_id)
        if process_case is None:
            return None

        process_name = process_case.name
        area = process_case.area or "el area responsable"
        return InterviewGuideResponse(
            case_id=UUID(process_case.id),
            title=f"Guia de levantamiento as-is - {process_name}",
            sections=[
                InterviewGuideSection(
                    title="Contexto y alcance",
                    questions=[
                        f"Cual es el objetivo principal del proceso {process_name}?",
                        f"Donde inicia y donde termina el proceso para {area}?",
                        "Que disparadores activan el proceso?",
                    ],
                ),
                InterviewGuideSection(
                    title="Flujo actual",
                    questions=[
                        "Cuales son las actividades principales en orden?",
                        "Que decisiones o aprobaciones cambian el camino del flujo?",
                        "Que excepciones ocurren con mayor frecuencia?",
                    ],
                ),
                InterviewGuideSection(
                    title="Roles, sistemas y datos",
                    questions=[
                        "Que roles participan y que responsabilidad tiene cada uno?",
                        "Que sistemas, archivos o formularios se usan?",
                        "Que entradas y salidas produce cada actividad critica?",
                    ],
                ),
                InterviewGuideSection(
                    title="Medicion y mejora",
                    questions=[
                        "Que tiempos, volumenes, costos o SLA se miden hoy?",
                        "Donde aparecen retrasos, reprocesos o controles manuales?",
                        "Que oportunidades de automatizacion o simplificacion existen?",
                    ],
                ),
            ],
        )

    def assess_discovery(self, case_id: UUID) -> DiscoveryAssessmentResponse | None:
        process_case = self._get_case(case_id)
        if process_case is None:
            return None

        stakeholders = self._stakeholder_models(case_id)
        interviews = self._interview_models(case_id)
        elements = self._as_is_element_models(case_id)

        dimensions = self._build_completeness_dimensions(stakeholders, interviews, elements)
        total_score = sum(dimension.score for dimension in dimensions)
        total_max = sum(dimension.max_score for dimension in dimensions) or 1
        completeness_score = round((total_score / total_max) * 100)
        gaps = self._detect_gaps(stakeholders, interviews, elements)
        contradictions = self._detect_contradictions(interviews, elements)
        generated_questions = self._generate_role_questions(process_case, stakeholders, interviews, elements, gaps)
        next_actions = self._build_next_actions(completeness_score, gaps, contradictions, generated_questions)

        return DiscoveryAssessmentResponse(
            case_id=UUID(process_case.id),
            readiness_level=self._readiness_level(completeness_score, gaps, contradictions),
            completeness_score=completeness_score,
            dimensions=dimensions,
            generated_questions=generated_questions,
            gaps=gaps,
            contradictions=contradictions,
            next_actions_es=next_actions,
        )

    def list_as_is_elements(self, case_id: UUID) -> list[ProcessAsIsElementResponse] | None:
        if self._get_case(case_id) is None:
            return None

        statement = (
            select(ProcessAsIsElementModel)
            .where(ProcessAsIsElementModel.case_id == str(case_id))
            .options(selectinload(ProcessAsIsElementModel.interview))
            .order_by(ProcessAsIsElementModel.created_at.desc())
        )
        elements = self.db.scalars(statement).all()
        return [self._as_is_element_to_response(element) for element in elements]

    def _stakeholder_models(self, case_id: UUID) -> list[ProcessStakeholderModel]:
        statement = (
            select(ProcessStakeholderModel)
            .where(ProcessStakeholderModel.case_id == str(case_id))
            .order_by(ProcessStakeholderModel.created_at.desc())
        )
        return list(self.db.scalars(statement).all())

    def _interview_models(self, case_id: UUID) -> list[ProcessInterviewModel]:
        statement = (
            select(ProcessInterviewModel)
            .where(ProcessInterviewModel.case_id == str(case_id))
            .options(selectinload(ProcessInterviewModel.stakeholder))
            .order_by(ProcessInterviewModel.created_at.desc())
        )
        return list(self.db.scalars(statement).all())

    def _as_is_element_models(self, case_id: UUID) -> list[ProcessAsIsElementModel]:
        statement = (
            select(ProcessAsIsElementModel)
            .where(ProcessAsIsElementModel.case_id == str(case_id))
            .options(selectinload(ProcessAsIsElementModel.interview))
            .order_by(ProcessAsIsElementModel.created_at.desc())
        )
        return list(self.db.scalars(statement).all())

    @classmethod
    def _build_completeness_dimensions(
        cls,
        stakeholders: list[ProcessStakeholderModel],
        interviews: list[ProcessInterviewModel],
        elements: list[ProcessAsIsElementModel],
    ) -> list[DiscoveryCompletenessDimensionResponse]:
        element_types = {element.element_type for element in elements}
        stakeholder_roles = {stakeholder.role for stakeholder in stakeholders}
        text_sources = [interview for interview in interviews if cls._interview_text(interview).strip()]
        high_confidence = [element for element in elements if element.confidence_level == ConfidenceLevel.high.value]

        raw_dimensions = [
            (
                "stakeholders",
                "Stakeholders y responsables",
                min(20, len(stakeholders) * 5 + (8 if StakeholderRole.process_owner.value in stakeholder_roles else 0)),
                20,
                "Debe existir al menos un dueno del proceso y participantes clave.",
            ),
            (
                "interviews",
                "Entrevistas y fuentes",
                min(20, len(text_sources) * 7 + (5 if len(text_sources) >= 2 else 0)),
                20,
                "Debe haber notas, resumen o preguntas respondidas por los actores.",
            ),
            (
                "flow_elements",
                "Flujo, eventos y actividades",
                cls._coverage_score(element_types, [AsIsElementType.event, AsIsElementType.activity], 20),
                20,
                "Debe existir inicio, fin o disparador y actividades principales.",
            ),
            (
                "rules_systems_data",
                "Reglas, sistemas y datos",
                cls._coverage_score(
                    element_types,
                    [AsIsElementType.business_rule, AsIsElementType.system, AsIsElementType.input_output],
                    20,
                ),
                20,
                "Debe cubrir reglas de negocio, sistemas y entradas/salidas.",
            ),
            (
                "exceptions_metrics_controls",
                "Excepciones, metricas y controles",
                cls._coverage_score(
                    element_types,
                    [AsIsElementType.exception, AsIsElementType.metric, AsIsElementType.control],
                    20,
                ),
                20,
                "Debe cubrir excepciones, indicadores y controles para analizar mejora.",
            ),
            (
                "evidence_confidence",
                "Trazabilidad y confianza",
                min(20, len(high_confidence) * 4 + len([element for element in elements if element.source_excerpt]) * 2),
                20,
                "Los elementos criticos deben tener extracto fuente y confianza alta o media.",
            ),
        ]

        dimensions: list[DiscoveryCompletenessDimensionResponse] = []
        for code, label, score, max_score, detail in raw_dimensions:
            status = "ok" if score >= int(max_score * 0.75) else "partial" if score > 0 else "missing"
            dimensions.append(
                DiscoveryCompletenessDimensionResponse(
                    code=code,
                    label_es=label,
                    score=score,
                    max_score=max_score,
                    status=status,
                    detail_es=detail,
                )
            )
        return dimensions

    @staticmethod
    def _coverage_score(element_types: set[str], required: list[AsIsElementType], max_score: int) -> int:
        if not required:
            return 0
        covered = sum(1 for element_type in required if element_type.value in element_types)
        return round((covered / len(required)) * max_score)

    @classmethod
    def _detect_gaps(
        cls,
        stakeholders: list[ProcessStakeholderModel],
        interviews: list[ProcessInterviewModel],
        elements: list[ProcessAsIsElementModel],
    ) -> list[DiscoveryGapResponse]:
        gaps: list[DiscoveryGapResponse] = []
        roles = {stakeholder.role for stakeholder in stakeholders}
        element_types = {element.element_type for element in elements}
        text_sources = [interview for interview in interviews if cls._interview_text(interview).strip()]

        if StakeholderRole.process_owner.value not in roles:
            gaps.append(
                cls._gap(
                    "missing_process_owner",
                    "high",
                    "Falta dueno del proceso",
                    "No hay stakeholder marcado como process_owner.",
                    "Registrar o confirmar el dueno del proceso antes de aprobar el as-is.",
                )
            )
        if not text_sources:
            gaps.append(
                cls._gap(
                    "missing_interview_notes",
                    "high",
                    "Faltan notas de levantamiento",
                    "Las entrevistas no contienen notas, resumen u objetivo suficiente para extraer evidencia.",
                    "Realizar entrevista de descubrimiento y cargar notas textuales.",
                )
            )
        for element_type, title, recommendation in [
            (AsIsElementType.event.value, "Faltan eventos de inicio/fin", "Preguntar como inicia, termina y se dispara el proceso."),
            (AsIsElementType.activity.value, "Faltan actividades principales", "Levantar la secuencia de actividades con responsables."),
            (AsIsElementType.business_rule.value, "Faltan reglas de negocio", "Documentar condiciones, umbrales y criterios de decision."),
            (AsIsElementType.system.value, "Faltan sistemas", "Identificar aplicaciones, archivos, correos o integraciones usadas."),
            (AsIsElementType.exception.value, "Faltan excepciones", "Preguntar por rechazos, devoluciones, errores y retrabajos frecuentes."),
            (AsIsElementType.metric.value, "Faltan metricas", "Solicitar volumen, tiempos, SLA, colas, costo o capacidad."),
            (AsIsElementType.control.value, "Faltan controles", "Identificar aprobaciones, validaciones y controles de riesgo."),
        ]:
            if element_type not in element_types:
                gaps.append(
                    cls._gap(
                        f"missing_{element_type}",
                        "medium",
                        title,
                        f"No hay elementos as-is de tipo {element_type}.",
                        recommendation,
                    )
                )

        return gaps

    @classmethod
    def _detect_contradictions(
        cls,
        interviews: list[ProcessInterviewModel],
        elements: list[ProcessAsIsElementModel],
    ) -> list[DiscoveryContradictionResponse]:
        text_units = [
            cls._interview_text(interview)
            for interview in interviews
            if cls._interview_text(interview).strip()
        ] + [
            " ".join(value for value in [element.name, element.description, element.source_excerpt] if value)
            for element in elements
        ]
        lowered_units = [unit.lower() for unit in text_units]
        contradictions: list[DiscoveryContradictionResponse] = []

        contradiction_rules = [
            (
                "Regla de aprobacion",
                ("siempre", "aprueb"),
                ("solo si", "aprueb"),
                "Hay evidencia de aprobacion siempre y tambien condicionada.",
            ),
            (
                "Responsabilidad del proceso",
                ("responsable",),
                ("no hay responsable",),
                "Hay afirmaciones incompatibles sobre responsabilidad.",
            ),
            (
                "Automatizacion vs manualidad",
                ("automatic",),
                ("manual",),
                "Hay versiones distintas sobre si la actividad es automatica o manual.",
            ),
            (
                "Uso de sistema",
                ("sap",),
                ("excel",),
                "Hay sistemas distintos mencionados para el mismo proceso; validar si son pasos diferentes o fuentes alternativas.",
            ),
        ]

        for topic, left_terms, right_terms, recommendation in contradiction_rules:
            left = [unit for unit, lowered in zip(text_units, lowered_units, strict=False) if all(term in lowered for term in left_terms)]
            right = [unit for unit, lowered in zip(text_units, lowered_units, strict=False) if all(term in lowered for term in right_terms)]
            if left and right:
                contradictions.append(
                    DiscoveryContradictionResponse(
                        topic=topic,
                        severity="medium",
                        evidence_es=[
                            cls._shorten(left[0]),
                            cls._shorten(right[0]),
                        ],
                        recommendation_es=recommendation,
                    )
                )

        return contradictions

    @classmethod
    def _generate_role_questions(
        cls,
        process_case: ProcessCaseModel,
        stakeholders: list[ProcessStakeholderModel],
        interviews: list[ProcessInterviewModel],
        elements: list[ProcessAsIsElementModel],
        gaps: list[DiscoveryGapResponse],
    ) -> list[DiscoveryQuestionResponse]:
        roles = {stakeholder.role for stakeholder in stakeholders}
        element_types = {element.element_type for element in elements}
        gap_codes = {gap.code for gap in gaps}
        process_name = process_case.name
        questions: list[DiscoveryQuestionResponse] = []

        if StakeholderRole.process_owner.value in roles or "missing_process_owner" in gap_codes:
            questions.extend(
                [
                    cls._question(
                        StakeholderRole.process_owner,
                        "high",
                        f"Confirma el inicio, fin y alcance exacto del proceso {process_name}.",
                        "El modelo as-is no puede aprobarse sin frontera clara.",
                        "Definicion de alcance validada por el dueno del proceso.",
                    ),
                    cls._question(
                        StakeholderRole.process_owner,
                        "high",
                        "Que decisiones requieren aprobacion humana obligatoria y cuales podrian automatizarse por regla?",
                        "El to-be no debe eliminar controles criticos sin validacion.",
                        "Politica, matriz de aprobacion o regla escrita.",
                    ),
                ]
            )

        if AsIsElementType.exception.value not in element_types:
            questions.append(
                cls._question(
                    StakeholderRole.subject_matter_expert,
                    "high",
                    "Cuales son las excepciones, rechazos, devoluciones o retrabajos mas frecuentes?",
                    "El happy path no alcanza para modelar BPMN profesional.",
                    "Lista de excepciones con frecuencia aproximada y responsable.",
                )
            )

        if AsIsElementType.metric.value not in element_types:
            questions.append(
                cls._question(
                    StakeholderRole.participant,
                    "medium",
                    "Cuanto tarda cada actividad y donde se acumulan esperas o colas?",
                    "El analisis cuantitativo requiere tiempos, volumenes y SLA.",
                    "Tiempos por actividad, volumen mensual y SLA actual.",
                )
            )

        if AsIsElementType.system.value not in element_types:
            questions.append(
                cls._question(
                    StakeholderRole.system_owner,
                    "medium",
                    "Que sistemas, archivos, correos o integraciones soportan cada paso del proceso?",
                    "El redisenio digital depende de conocer sistemas y datos.",
                    "Mapa de sistemas por actividad e integraciones existentes.",
                )
            )

        if AsIsElementType.control.value not in element_types:
            questions.append(
                cls._question(
                    StakeholderRole.risk_control,
                    "high",
                    "Que controles previenen fraude, error, incumplimiento o riesgo operativo?",
                    "Las mejoras no deben debilitar el control interno.",
                    "Matriz de controles, riesgos cubiertos y evidencia de ejecucion.",
                )
            )

        if len(interviews) < 2:
            questions.append(
                cls._question(
                    StakeholderRole.approver,
                    "medium",
                    "Que criterios usa para aprobar, rechazar o pedir correcciones?",
                    "Se necesita validar si las reglas declaradas coinciden con la practica.",
                    "Criterios de decision, umbrales y ejemplos de casos rechazados.",
                )
            )

        return questions[:10]

    @classmethod
    def _build_next_actions(
        cls,
        completeness_score: int,
        gaps: list[DiscoveryGapResponse],
        contradictions: list[DiscoveryContradictionResponse],
        questions: list[DiscoveryQuestionResponse],
    ) -> list[str]:
        actions: list[str] = []
        if contradictions:
            actions.append("Resolver contradicciones antes de aprobar la narrativa as-is.")
        high_gaps = [gap for gap in gaps if gap.severity == "high"]
        if high_gaps:
            actions.append(f"Cerrar {len(high_gaps)} vacio(s) critico(s) del levantamiento.")
        if questions:
            actions.append("Agendar la siguiente entrevista usando las preguntas priorizadas del agente levantador.")
        if completeness_score < 60:
            actions.append("Mantener el caso en levantamiento; todavia no esta listo para modelado BPMN.")
        elif completeness_score < 80:
            actions.append("Preparar validacion humana del as-is y completar brechas medianas.")
        else:
            actions.append("El as-is esta cerca de estar listo para modelado BPMN con supervision humana.")
        return actions

    @staticmethod
    def _readiness_level(
        completeness_score: int,
        gaps: list[DiscoveryGapResponse],
        contradictions: list[DiscoveryContradictionResponse],
    ) -> str:
        if contradictions or any(gap.severity == "high" for gap in gaps):
            return "blocked"
        if completeness_score >= 80:
            return "ready_for_bpmn"
        if completeness_score >= 60:
            return "needs_validation"
        return "insufficient"

    @staticmethod
    def _gap(
        code: str,
        severity: str,
        title: str,
        detail: str,
        recommendation: str,
    ) -> DiscoveryGapResponse:
        return DiscoveryGapResponse(
            code=code,
            severity=severity,
            title_es=title,
            detail_es=detail,
            recommendation_es=recommendation,
        )

    @staticmethod
    def _question(
        role: StakeholderRole,
        priority: str,
        question: str,
        reason: str,
        expected_evidence: str,
    ) -> DiscoveryQuestionResponse:
        return DiscoveryQuestionResponse(
            role=role,
            priority=priority,
            question_es=question,
            reason_es=reason,
            expected_evidence_es=expected_evidence,
        )

    @staticmethod
    def _interview_text(interview: ProcessInterviewModel) -> str:
        return "\n".join(
            value
            for value in [interview.objective, interview.questions, interview.notes, interview.summary]
            if value
        )

    @staticmethod
    def _shorten(text: str, max_length: int = 260) -> str:
        cleaned = re.sub(r"\s+", " ", text).strip()
        if len(cleaned) <= max_length:
            return cleaned
        return f"{cleaned[: max_length - 3].rstrip()}..."

    def create_as_is_element(
        self,
        case_id: UUID,
        payload: ProcessAsIsElementCreate,
    ) -> ProcessAsIsElementResponse | None:
        process_case = self._get_case(case_id)
        if process_case is None:
            return None

        interview = None
        if payload.interview_id is not None:
            interview = self.db.get(ProcessInterviewModel, str(payload.interview_id))
            if interview is None or interview.case_id != process_case.id:
                raise DiscoveryValidationError("Interview does not belong to this case")

        element = ProcessAsIsElementModel(
            id=str(uuid4()),
            case_id=process_case.id,
            interview_id=interview.id if interview else None,
            element_type=payload.element_type.value,
            name=payload.name,
            description=payload.description,
            source_excerpt=payload.source_excerpt,
            confidence_level=payload.confidence_level.value,
            created_by=payload.created_by,
        )
        self._mark_case_as_is_drafting(process_case)
        self.db.add(element)
        self.db.commit()
        self.db.refresh(element)
        return self._as_is_element_to_response(element)

    def extract_as_is_from_interview(
        self,
        case_id: UUID,
        interview_id: UUID,
    ) -> list[ProcessAsIsElementResponse] | None:
        process_case = self._get_case(case_id)
        if process_case is None:
            return None

        statement = (
            select(ProcessInterviewModel)
            .where(
                ProcessInterviewModel.id == str(interview_id),
                ProcessInterviewModel.case_id == process_case.id,
            )
            .options(selectinload(ProcessInterviewModel.as_is_elements))
        )
        interview = self.db.scalars(statement).first()
        if interview is None:
            raise DiscoveryValidationError("Interview does not belong to this case")

        text = "\n".join(
            value
            for value in [interview.objective, interview.questions, interview.notes, interview.summary]
            if value
        )
        candidates = self._extract_candidates(text)
        existing_excerpts = {
            element.source_excerpt.strip().lower()
            for element in interview.as_is_elements
            if element.source_excerpt
        }

        created_elements: list[ProcessAsIsElementModel] = []
        for candidate in candidates:
            excerpt_key = candidate["source_excerpt"].strip().lower()
            if excerpt_key in existing_excerpts:
                continue

            element = ProcessAsIsElementModel(
                id=str(uuid4()),
                case_id=process_case.id,
                interview_id=interview.id,
                element_type=candidate["element_type"],
                name=candidate["name"],
                description=candidate["description"],
                source_excerpt=candidate["source_excerpt"],
                confidence_level=candidate["confidence_level"],
                created_by="heuristic_extractor",
            )
            self.db.add(element)
            created_elements.append(element)

        if created_elements:
            self._mark_case_as_is_drafting(process_case)
            self.db.commit()
            for element in created_elements:
                self.db.refresh(element)

        return [self._as_is_element_to_response(element) for element in created_elements]

    def _get_case(self, case_id: UUID) -> ProcessCaseModel | None:
        return self.db.get(ProcessCaseModel, str(case_id))

    @staticmethod
    def _mark_case_in_discovery(process_case: ProcessCaseModel) -> None:
        if process_case.status in {
            ProcessCaseStatus.draft.value,
            ProcessCaseStatus.knowledge_loading.value,
        }:
            process_case.status = ProcessCaseStatus.discovery.value

    @staticmethod
    def _mark_case_as_is_drafting(process_case: ProcessCaseModel) -> None:
        if process_case.status in {
            ProcessCaseStatus.draft.value,
            ProcessCaseStatus.knowledge_loading.value,
            ProcessCaseStatus.discovery.value,
        }:
            process_case.status = ProcessCaseStatus.as_is_drafting.value

    @classmethod
    def _extract_candidates(cls, text: str) -> list[dict[str, str]]:
        fragments = [
            fragment.strip(" -\t")
            for fragment in re.split(r"[\n\r;]+|(?<=[.!?])\s+", text)
            if fragment.strip(" -\t")
        ]
        candidates: list[dict[str, str]] = []
        seen: set[tuple[str, str]] = set()

        for fragment in fragments:
            if len(fragment) < 12:
                continue

            element_type, confidence = cls._classify_fragment(fragment)
            name = cls._build_element_name(fragment)
            key = (element_type, name.lower())
            if key in seen:
                continue
            seen.add(key)
            candidates.append(
                {
                    "element_type": element_type,
                    "name": name,
                    "description": fragment,
                    "source_excerpt": fragment,
                    "confidence_level": confidence,
                }
            )

        return candidates[:20]

    @staticmethod
    def _classify_fragment(fragment: str) -> tuple[str, str]:
        text = fragment.lower()
        rules: list[tuple[str, tuple[str, ...]]] = [
            (
                AsIsElementType.exception.value,
                ("excepcion", "rechaza", "rechazo", "devuelve", "falta", "error", "incidencia"),
            ),
            (
                AsIsElementType.pain_point.value,
                ("demora", "retraso", "cuello", "reproceso", "manual", "problema", "pendiente"),
            ),
            (
                AsIsElementType.opportunity.value,
                ("automatizar", "oportunidad", "mejorar", "simplificar", "digitalizar"),
            ),
            (
                AsIsElementType.event.value,
                ("inicia", "inicio", "termina", "fin", "disparador", "recibe solicitud", "llega"),
            ),
            (
                AsIsElementType.system.value,
                ("sistema", "erp", "sap", "excel", "correo", "formulario", "portal", "bpm"),
            ),
            (
                AsIsElementType.business_rule.value,
                ("regla", "debe", "requiere", "si ", "cuando", "solo si", "obligatorio"),
            ),
            (
                AsIsElementType.control.value,
                ("control", "validar", "valida", "aprueba", "aprobacion", "revision", "revisa"),
            ),
            (
                AsIsElementType.metric.value,
                ("sla", "tiempo", "dias", "horas", "volumen", "cantidad", "costo"),
            ),
            (
                AsIsElementType.input_output.value,
                ("entrada", "salida", "documento", "solicitud", "factura", "archivo", "evidencia"),
            ),
            (
                AsIsElementType.role.value,
                ("responsable", "rol", "usuario", "analista", "jefe", "supervisor", "area"),
            ),
        ]

        for element_type, keywords in rules:
            if any(keyword in text for keyword in keywords):
                return element_type, ConfidenceLevel.high.value

        return AsIsElementType.activity.value, ConfidenceLevel.medium.value

    @staticmethod
    def _build_element_name(fragment: str) -> str:
        cleaned = re.sub(r"\s+", " ", fragment).strip(" .")
        if len(cleaned) <= 90:
            return cleaned
        return f"{cleaned[:87].rstrip()}..."

    @staticmethod
    def _stakeholder_to_response(stakeholder: ProcessStakeholderModel) -> ProcessStakeholderResponse:
        return ProcessStakeholderResponse(
            id=UUID(stakeholder.id),
            case_id=UUID(stakeholder.case_id),
            name=stakeholder.name,
            role=StakeholderRole(stakeholder.role),
            area=stakeholder.area,
            email=stakeholder.email,
            influence_level=StakeholderInfluenceLevel(stakeholder.influence_level),
            availability=stakeholder.availability,
            notes=stakeholder.notes,
            created_at=stakeholder.created_at,
            updated_at=stakeholder.updated_at,
        )

    @staticmethod
    def _interview_to_response(interview: ProcessInterviewModel) -> ProcessInterviewResponse:
        return ProcessInterviewResponse(
            id=UUID(interview.id),
            case_id=UUID(interview.case_id),
            stakeholder_id=UUID(interview.stakeholder_id) if interview.stakeholder_id else None,
            stakeholder_name=interview.stakeholder.name if interview.stakeholder else None,
            title=interview.title,
            interview_type=interview.interview_type,
            status=InterviewStatus(interview.status),
            scheduled_at=interview.scheduled_at,
            objective=interview.objective,
            questions=interview.questions,
            notes=interview.notes,
            summary=interview.summary,
            created_at=interview.created_at,
            updated_at=interview.updated_at,
        )

    @staticmethod
    def _as_is_element_to_response(element: ProcessAsIsElementModel) -> ProcessAsIsElementResponse:
        return ProcessAsIsElementResponse(
            id=UUID(element.id),
            case_id=UUID(element.case_id),
            interview_id=UUID(element.interview_id) if element.interview_id else None,
            interview_title=element.interview.title if element.interview else None,
            element_type=AsIsElementType(element.element_type),
            name=element.name,
            description=element.description,
            source_excerpt=element.source_excerpt,
            confidence_level=ConfidenceLevel(element.confidence_level),
            created_by=element.created_by,
            created_at=element.created_at,
            updated_at=element.updated_at,
        )
