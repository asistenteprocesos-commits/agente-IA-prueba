from enum import StrEnum
from uuid import UUID

from pydantic import BaseModel, Field


class RedesignOptionType(StrEnum):
    quick_win = "quick_win"
    structural = "structural"
    control = "control"
    automation = "automation"


class ToBeAlternativeResponse(BaseModel):
    option_type: RedesignOptionType
    title_es: str
    description_es: str
    expected_impact_es: str
    effort_es: str
    risk_es: str
    changes_es: list[str]
    required_validation_es: list[str]


class ToBeComparisonResponse(BaseModel):
    recommended_option_title_es: str
    rationale_es: str
    assumptions_es: list[str]


class ProcessRedesignResponse(BaseModel):
    case_id: UUID
    alternatives: list[ToBeAlternativeResponse]
    comparison: ToBeComparisonResponse
    next_actions_es: list[str]


class ProcessRedesignReportCreate(BaseModel):
    title: str = Field(default="Propuesta to-be generada por agente", min_length=3, max_length=180)
    author: str | None = Field(default="Agente Redisenador", max_length=120)
    persist: bool = True
