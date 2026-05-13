from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.process_case import ProcessCaseCreate, ProcessCaseResponse
from app.services.process_case_service import ProcessCaseService

router = APIRouter()


@router.get("", response_model=list[ProcessCaseResponse])
def list_process_cases(db: Session = Depends(get_db)) -> list[ProcessCaseResponse]:
    return ProcessCaseService(db).list_cases()


@router.post("", response_model=ProcessCaseResponse, status_code=status.HTTP_201_CREATED)
def create_process_case(
    payload: ProcessCaseCreate,
    db: Session = Depends(get_db),
) -> ProcessCaseResponse:
    return ProcessCaseService(db).create_case(payload)


@router.get("/{case_id}", response_model=ProcessCaseResponse)
def get_process_case(case_id: UUID, db: Session = Depends(get_db)) -> ProcessCaseResponse:
    process_case = ProcessCaseService(db).get_case(case_id)

    if process_case is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Process case not found",
        )

    return process_case
