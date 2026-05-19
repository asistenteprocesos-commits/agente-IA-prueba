from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class DocumentManagementCreate(BaseModel):
    doc_type: str = Field(..., description="policy, procedure, instruction, or format_record")
    code: str = Field(..., max_length=40)
    title: str = Field(..., max_length=200)
    objective: str | None = None
    scope: str | None = None
    responsibilities: str | None = None
    content: str


class DocumentManagementResponse(BaseModel):
    id: UUID
    case_id: UUID
    doc_type: str
    code: str
    title: str
    version: str
    objective: str | None
    scope: str | None
    responsibilities: str | None
    content: str
    status: str
    created_by: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
