from enum import StrEnum
from uuid import UUID

from pydantic import BaseModel, Field


class BpmnIssueSeverity(StrEnum):
    info = "info"
    warning = "warning"
    error = "error"


class BpmnIssueResponse(BaseModel):
    severity: BpmnIssueSeverity
    code: str
    message_es: str
    element_ref: str | None = None


class BpmnDraftResponse(BaseModel):
    case_id: UUID
    source_element_count: int
    task_count: int
    gateway_count: int
    bpmn_xml: str
    issues: list[BpmnIssueResponse]
    is_valid: bool
    artifact_id: UUID | None = None
    artifact_version_id: UUID | None = None


class BpmnGenerateCreate(BaseModel):
    title: str = Field(default="BPMN as-is generado por agente", min_length=3, max_length=180)
    author: str | None = Field(default="Agente Modelador BPMN", max_length=120)
    persist: bool = True


class BpmnValidationCreate(BaseModel):
    bpmn_xml: str = Field(min_length=20)


class BpmnValidationResponse(BaseModel):
    is_valid: bool
    issues: list[BpmnIssueResponse]
