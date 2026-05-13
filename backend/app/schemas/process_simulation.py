from uuid import UUID

from pydantic import BaseModel, Field


class SimulationScenarioResponse(BaseModel):
    name_es: str
    cycle_time_hours: float
    manual_effort_hours: float
    cost_index: float
    sla_risk: str
    assumptions_es: list[str]


class SimulationComparisonResponse(BaseModel):
    baseline_cycle_time_hours: float
    best_cycle_time_hours: float
    cycle_time_reduction_percent: int
    recommended_scenario_es: str
    interpretation_es: str


class SensitivityPointResponse(BaseModel):
    variable_es: str
    low_case_es: str
    base_case_es: str
    high_case_es: str


class ProcessSimulationResponse(BaseModel):
    case_id: UUID
    scenarios: list[SimulationScenarioResponse]
    comparison: SimulationComparisonResponse
    sensitivity: list[SensitivityPointResponse]
    next_actions_es: list[str]


class ProcessSimulationReportCreate(BaseModel):
    title: str = Field(default="Simulacion inicial generada por agente", min_length=3, max_length=180)
    author: str | None = Field(default="Agente Simulador", max_length=120)
    persist: bool = True
