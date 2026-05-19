from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class ChatSessionCreate(BaseModel):
    title: str | None = Field(None, max_length=220)
    case_id: UUID | None = None


class ChatSessionResponse(BaseModel):
    id: UUID
    case_id: UUID | None
    title: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class ChatMessageCreate(BaseModel):
    content: str = Field(..., min_length=1, max_length=8000)


class ChatMessageResponse(BaseModel):
    id: UUID
    session_id: UUID
    role: str
    content: str
    llm_provider: str | None
    llm_model: str | None
    rag_fragments_used: int | None
    normalized_terms: str | None
    agent_task: str | None
    created_at: datetime

    model_config = {"from_attributes": True}


class RAGSearchRequest(BaseModel):
    query: str = Field(..., min_length=2, max_length=1000)
    top_k: int = Field(5, ge=1, le=20)
    case_id: UUID | None = None
    subject_area: str | None = None


class RAGFragmentResponse(BaseModel):
    chunk_id: str
    document_id: str
    document_title: str
    author: str | None
    content: str
    score: float
    chunk_index: int


class RAGSearchResponse(BaseModel):
    query: str
    fragments: list[RAGFragmentResponse]
    total_found: int


class LLMStatusResponse(BaseModel):
    provider: str
    model: str
    available: bool
    api_key_configured: bool
    notes: str | None = None


class LLMSystemStatusResponse(BaseModel):
    providers: list[LLMStatusResponse]
    active_provider: str
    ollama_available: bool
    internet_available: bool
