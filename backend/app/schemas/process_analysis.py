from enum import StrEnum
from uuid import UUID

from pydantic import BaseModel, Field


class FindingSeverity(StrEnum):
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"


class FindingType(StrEnum):
    bottleneck = "bottleneck"
    waste = "waste"
    risk = "risk"
    control_gap = "control_gap"
    automation = "automation"
    data_gap = "data_gap"
    quality = "quality"


class AnalysisFindingResponse(BaseModel):
    finding_type: FindingType
    severity: FindingSeverity
    title_es: str
    detail_es: str
    evidence_es: str | None
    recommendation_es: str
    confidence_level: str


class AnalysisMetricResponse(BaseModel):
    name_es: str
    value: float | None
    unit: str | None
    source_es: str
    interpretation_es: str


class RiskControlResponse(BaseModel):
    risk_es: str
    control_es: str | None
    status: str
    recommendation_es: str


class ImprovementCandidateResponse(BaseModel):
    title_es: str
    impact_es: str
    effort_es: str
    risk_es: str
    evidence_es: str | None


class ProcessAnalysisResponse(BaseModel):
    case_id: UUID
    analysis_score: int
    findings: list[AnalysisFindingResponse]
    metrics: list[AnalysisMetricResponse]
    risks_controls: list[RiskControlResponse]
    improvement_candidates: list[ImprovementCandidateResponse]
    next_actions_es: list[str]


class ProcessAnalysisReportCreate(BaseModel):
    title: str = Field(default="Analisis as-is generado por agente", min_length=3, max_length=180)
    author: str | None = Field(default="Agente Analista", max_length=120)
    persist: bool = True
