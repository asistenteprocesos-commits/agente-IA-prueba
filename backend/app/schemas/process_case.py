from datetime import datetime
from enum import StrEnum
from uuid import UUID

from pydantic import BaseModel, Field


class ProcessCaseStatus(StrEnum):
    draft = "draft"
    knowledge_loading = "knowledge_loading"
    discovery = "discovery"
    event_log_analysis = "event_log_analysis"
    as_is_drafting = "as_is_drafting"
    bpmn_drafting = "bpmn_drafting"
    repository_review = "repository_review"
    human_review = "human_review"
    approved_as_is = "approved_as_is"
    improvement_analysis = "improvement_analysis"
    closed = "closed"


class ProcessCaseCreate(BaseModel):
    name: str = Field(min_length=3, max_length=160)
    area: str | None = Field(default=None, max_length=120)
    objective: str | None = Field(default=None, max_length=500)
    scope: str | None = Field(default=None, max_length=1200)
    owner: str | None = Field(default=None, max_length=120)


class ProcessCaseResponse(BaseModel):
    id: UUID
    name: str
    area: str | None
    objective: str | None
    scope: str | None
    owner: str | None
    status: ProcessCaseStatus
    created_at: datetime
    updated_at: datetime
