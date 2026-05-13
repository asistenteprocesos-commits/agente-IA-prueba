from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.process_redesign import ProcessRedesignReportCreate, ProcessRedesignResponse
from app.services.process_redesign_service import ProcessRedesignService

router = APIRouter()


@router.get("/{case_id}/redesign/to-be-options", response_model=ProcessRedesignResponse)
def build_to_be_options(
    case_id: UUID,
    db: Session = Depends(get_db),
) -> ProcessRedesignResponse:
    redesign = ProcessRedesignService(db).build_to_be_options(case_id)
    if redesign is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Process case not found")
    return redesign


@router.post("/{case_id}/redesign/report", response_model=ProcessRedesignResponse)
def create_redesign_report(
    case_id: UUID,
    payload: ProcessRedesignReportCreate,
    db: Session = Depends(get_db),
) -> ProcessRedesignResponse:
    redesign = ProcessRedesignService(db).create_report(case_id, payload)
    if redesign is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Process case not found")
    return redesign
