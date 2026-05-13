from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.process_analysis import ProcessAnalysisReportCreate, ProcessAnalysisResponse
from app.services.process_analysis_service import ProcessAnalysisService

router = APIRouter()


@router.get("/{case_id}/analysis", response_model=ProcessAnalysisResponse)
def analyze_process_case(
    case_id: UUID,
    db: Session = Depends(get_db),
) -> ProcessAnalysisResponse:
    analysis = ProcessAnalysisService(db).analyze_case(case_id)
    if analysis is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Process case not found")
    return analysis


@router.post("/{case_id}/analysis/report", response_model=ProcessAnalysisResponse)
def create_process_analysis_report(
    case_id: UUID,
    payload: ProcessAnalysisReportCreate,
    db: Session = Depends(get_db),
) -> ProcessAnalysisResponse:
    analysis = ProcessAnalysisService(db).create_report(case_id, payload)
    if analysis is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Process case not found")
    return analysis
