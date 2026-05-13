from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.bpmn import BpmnDraftResponse, BpmnGenerateCreate, BpmnValidationCreate, BpmnValidationResponse
from app.services.bpmn_modeler_service import BpmnModelerService

router = APIRouter()


@router.get("/{case_id}/bpmn/as-is/preview", response_model=BpmnDraftResponse)
def preview_as_is_bpmn(
    case_id: UUID,
    db: Session = Depends(get_db),
) -> BpmnDraftResponse:
    draft = BpmnModelerService(db).preview_as_is_bpmn(case_id)
    if draft is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Process case not found")
    return draft


@router.post("/{case_id}/bpmn/as-is/generate", response_model=BpmnDraftResponse)
def generate_as_is_bpmn(
    case_id: UUID,
    payload: BpmnGenerateCreate,
    db: Session = Depends(get_db),
) -> BpmnDraftResponse:
    draft = BpmnModelerService(db).generate_as_is_bpmn(case_id, payload)
    if draft is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Process case not found")
    return draft


@router.post("/{case_id}/bpmn/validate", response_model=BpmnValidationResponse)
def validate_bpmn(
    case_id: UUID,
    payload: BpmnValidationCreate,
    db: Session = Depends(get_db),
) -> BpmnValidationResponse:
    draft = BpmnModelerService(db).preview_as_is_bpmn(case_id)
    if draft is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Process case not found")
    return BpmnModelerService(db).validate_bpmn(payload.bpmn_xml)
