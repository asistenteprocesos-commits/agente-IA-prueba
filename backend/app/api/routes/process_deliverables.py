from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.process_deliverables import FinalDeliverableCreate, FinalDeliverableResponse
from app.services.process_deliverables_service import ProcessDeliverablesService

router = APIRouter()


@router.get("/{case_id}/deliverables/final-report", response_model=FinalDeliverableResponse)
def preview_final_report(
    case_id: UUID,
    db: Session = Depends(get_db),
) -> FinalDeliverableResponse:
    deliverable = ProcessDeliverablesService(db).build_final_deliverable(case_id)
    if deliverable is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Process case not found")
    return deliverable


@router.post("/{case_id}/deliverables/final-report", response_model=FinalDeliverableResponse)
def create_final_report(
    case_id: UUID,
    payload: FinalDeliverableCreate,
    db: Session = Depends(get_db),
) -> FinalDeliverableResponse:
    deliverable = ProcessDeliverablesService(db).build_final_deliverable(case_id, payload)
    if deliverable is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Process case not found")
    return deliverable
