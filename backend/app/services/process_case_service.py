from uuid import UUID, uuid4

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.process_case import ProcessCaseModel
from app.models.process_repository import ProcessRepositoryModel
from app.schemas.process_case import ProcessCaseCreate, ProcessCaseResponse, ProcessCaseStatus


class ProcessCaseService:
    def __init__(self, db: Session) -> None:
        self.db = db

    def list_cases(self) -> list[ProcessCaseResponse]:
        statement = select(ProcessCaseModel).order_by(ProcessCaseModel.created_at.desc())
        cases = self.db.scalars(statement).all()
        return [self._to_response(process_case) for process_case in cases]

    def get_case(self, case_id: UUID) -> ProcessCaseResponse | None:
        process_case = self.db.get(ProcessCaseModel, str(case_id))
        if process_case is None:
            return None
        return self._to_response(process_case)

    def create_case(self, payload: ProcessCaseCreate) -> ProcessCaseResponse:
        process_case = ProcessCaseModel(
            id=str(uuid4()),
            name=payload.name,
            area=payload.area,
            objective=payload.objective,
            scope=payload.scope,
            owner=payload.owner,
            status=ProcessCaseStatus.draft.value,
        )
        repository = ProcessRepositoryModel(
            id=str(uuid4()),
            case_id=process_case.id,
            name=f"Repositorio - {payload.name}",
        )
        process_case.repository = repository

        self.db.add(process_case)
        self.db.commit()
        self.db.refresh(process_case)
        return self._to_response(process_case)

    @staticmethod
    def _to_response(process_case: ProcessCaseModel) -> ProcessCaseResponse:
        return ProcessCaseResponse(
            id=UUID(process_case.id),
            name=process_case.name,
            area=process_case.area,
            objective=process_case.objective,
            scope=process_case.scope,
            owner=process_case.owner,
            status=ProcessCaseStatus(process_case.status),
            created_at=process_case.created_at,
            updated_at=process_case.updated_at,
        )
