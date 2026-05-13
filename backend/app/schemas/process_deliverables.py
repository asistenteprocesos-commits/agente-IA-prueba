from uuid import UUID

from pydantic import BaseModel, Field


class ImplementationStepResponse(BaseModel):
    order: int
    title_es: str
    owner_es: str
    timeframe_es: str
    deliverable_es: str


class FinalDeliverableResponse(BaseModel):
    case_id: UUID
    executive_summary_es: str
    technical_summary_es: str
    implementation_plan: list[ImplementationStepResponse]
    decision_points_es: list[str]
    residual_risks_es: list[str]
    artifact_id: UUID | None = None
    artifact_version_id: UUID | None = None


class FinalDeliverableCreate(BaseModel):
    title: str = Field(default="Informe final generado por agente", min_length=3, max_length=180)
    author: str | None = Field(default="Agente Redactor", max_length=120)
    persist: bool = True
