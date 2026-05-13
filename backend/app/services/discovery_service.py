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
