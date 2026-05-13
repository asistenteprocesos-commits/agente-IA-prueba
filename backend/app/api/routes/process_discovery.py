from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.discovery import (
    DiscoveryAssessmentResponse,
    InterviewGuideResponse,
    ProcessAsIsElementCreate,
    ProcessAsIsElementResponse,
    ProcessInterviewCreate,
    ProcessInterviewResponse,
    ProcessStakeholderCreate,
    ProcessStakeholderResponse,
)
from app.services.discovery_service import DiscoveryValidationError, ProcessDiscoveryService

router = APIRouter()


@router.get("/{case_id}/discovery/stakeholders", response_model=list[ProcessStakeholderResponse])
def list_process_stakeholders(
    case_id: UUID,
    db: Session = Depends(get_db),
) -> list[ProcessStakeholderResponse]:
    stakeholders = ProcessDiscoveryService(db).list_stakeholders(case_id)
    if stakeholders is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Process case not found",
        )
    return stakeholders


@router.post(
    "/{case_id}/discovery/stakeholders",
    response_model=ProcessStakeholderResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_process_stakeholder(
    case_id: UUID,
    payload: ProcessStakeholderCreate,
    db: Session = Depends(get_db),
) -> ProcessStakeholderResponse:
    stakeholder = ProcessDiscoveryService(db).create_stakeholder(case_id, payload)
    if stakeholder is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Process case not found",
        )
    return stakeholder


@router.get("/{case_id}/discovery/interviews", response_model=list[ProcessInterviewResponse])
def list_process_interviews(
    case_id: UUID,
    db: Session = Depends(get_db),
) -> list[ProcessInterviewResponse]:
    interviews = ProcessDiscoveryService(db).list_interviews(case_id)
    if interviews is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Process case not found",
        )
    return interviews


@router.post(
    "/{case_id}/discovery/interviews",
    response_model=ProcessInterviewResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_process_interview(
    case_id: UUID,
    payload: ProcessInterviewCreate,
    db: Session = Depends(get_db),
) -> ProcessInterviewResponse:
    try:
        interview = ProcessDiscoveryService(db).create_interview(case_id, payload)
    except DiscoveryValidationError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        ) from error

    if interview is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Process case not found",
        )
    return interview


@router.get("/{case_id}/discovery/interview-guide", response_model=InterviewGuideResponse)
def get_process_interview_guide(
    case_id: UUID,
    db: Session = Depends(get_db),
) -> InterviewGuideResponse:
    guide = ProcessDiscoveryService(db).generate_interview_guide(case_id)
    if guide is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Process case not found",
        )
    return guide


@router.get("/{case_id}/discovery/assessment", response_model=DiscoveryAssessmentResponse)
def get_process_discovery_assessment(
    case_id: UUID,
    db: Session = Depends(get_db),
) -> DiscoveryAssessmentResponse:
    assessment = ProcessDiscoveryService(db).assess_discovery(case_id)
    if assessment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Process case not found",
        )
    return assessment


@router.get("/{case_id}/discovery/as-is-elements", response_model=list[ProcessAsIsElementResponse])
def list_process_as_is_elements(
    case_id: UUID,
    db: Session = Depends(get_db),
) -> list[ProcessAsIsElementResponse]:
    elements = ProcessDiscoveryService(db).list_as_is_elements(case_id)
    if elements is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Process case not found",
        )
    return elements


@router.post(
    "/{case_id}/discovery/as-is-elements",
    response_model=ProcessAsIsElementResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_process_as_is_element(
    case_id: UUID,
    payload: ProcessAsIsElementCreate,
    db: Session = Depends(get_db),
) -> ProcessAsIsElementResponse:
    try:
        element = ProcessDiscoveryService(db).create_as_is_element(case_id, payload)
    except DiscoveryValidationError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        ) from error

    if element is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Process case not found",
        )
    return element


@router.post(
    "/{case_id}/discovery/interviews/{interview_id}/extract-as-is",
    response_model=list[ProcessAsIsElementResponse],
    status_code=status.HTTP_201_CREATED,
)
def extract_process_as_is_elements(
    case_id: UUID,
    interview_id: UUID,
    db: Session = Depends(get_db),
) -> list[ProcessAsIsElementResponse]:
    try:
        elements = ProcessDiscoveryService(db).extract_as_is_from_interview(case_id, interview_id)
    except DiscoveryValidationError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        ) from error

    if elements is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Process case not found",
        )
    return elements
