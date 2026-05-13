from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.orchestration import (
    CheckpointDecisionCreate,
    OrchestrationContextCreate,
    OrchestrationStateResponse,
)
from app.services.orchestration_service import OrchestrationService, OrchestrationTransitionError

router = APIRouter()


@router.get("/{case_id}/orchestration", response_model=OrchestrationStateResponse)
def get_orchestration_state(
    case_id: UUID,
    db: Session = Depends(get_db),
) -> OrchestrationStateResponse:
    state = OrchestrationService(db).get_or_create_state(case_id)
    if state is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Process case not found")
    return state


@router.post("/{case_id}/orchestration/start", response_model=OrchestrationStateResponse)
def start_orchestration(
    case_id: UUID,
    db: Session = Depends(get_db),
) -> OrchestrationStateResponse:
    try:
        state = OrchestrationService(db).start(case_id)
    except OrchestrationTransitionError as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(error)) from error
    if state is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Process case not found")
    return state


@router.post("/{case_id}/orchestration/advance", response_model=OrchestrationStateResponse)
def advance_orchestration(
    case_id: UUID,
    db: Session = Depends(get_db),
) -> OrchestrationStateResponse:
    try:
        state = OrchestrationService(db).advance(case_id)
    except OrchestrationTransitionError as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(error)) from error
    if state is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Process case not found")
    return state


@router.post("/{case_id}/orchestration/checkpoint", response_model=OrchestrationStateResponse)
def decide_orchestration_checkpoint(
    case_id: UUID,
    payload: CheckpointDecisionCreate,
    db: Session = Depends(get_db),
) -> OrchestrationStateResponse:
    try:
        state = OrchestrationService(db).decide_checkpoint(case_id, payload)
    except OrchestrationTransitionError as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(error)) from error
    if state is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Process case not found")
    return state


@router.post("/{case_id}/orchestration/rollback", response_model=OrchestrationStateResponse)
def rollback_orchestration(
    case_id: UUID,
    db: Session = Depends(get_db),
) -> OrchestrationStateResponse:
    try:
        state = OrchestrationService(db).rollback(case_id)
    except OrchestrationTransitionError as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(error)) from error
    if state is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Process case not found")
    return state


@router.post("/{case_id}/orchestration/context", response_model=OrchestrationStateResponse)
def add_orchestration_context(
    case_id: UUID,
    payload: OrchestrationContextCreate,
    db: Session = Depends(get_db),
) -> OrchestrationStateResponse:
    state = OrchestrationService(db).add_context(case_id, payload)
    if state is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Process case not found")
    return state
