from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.process_simulation import ProcessSimulationReportCreate, ProcessSimulationResponse
from app.services.process_simulation_service import ProcessSimulationService

router = APIRouter()


@router.get("/{case_id}/simulation/scenarios", response_model=ProcessSimulationResponse)
def simulate_process_case(
    case_id: UUID,
    db: Session = Depends(get_db),
) -> ProcessSimulationResponse:
    simulation = ProcessSimulationService(db).simulate_case(case_id)
    if simulation is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Process case not found")
    return simulation


@router.post("/{case_id}/simulation/report", response_model=ProcessSimulationResponse)
def create_simulation_report(
    case_id: UUID,
    payload: ProcessSimulationReportCreate,
    db: Session = Depends(get_db),
) -> ProcessSimulationResponse:
    simulation = ProcessSimulationService(db).create_report(case_id, payload)
    if simulation is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Process case not found")
    return simulation
