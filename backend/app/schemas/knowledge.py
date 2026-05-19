from datetime import datetime
from enum import StrEnum
from uuid import UUID

from pydantic import BaseModel


class KnowledgeDocumentStatus(StrEnum):
    uploaded = "uploaded"
    processed = "processed"
    failed = "failed"


class KnowledgeSourceType(StrEnum):
    book = "book"
    article = "article"
    internal_document = "internal_document"
    standard = "standard"
    interview = "interview"
    process_artifact = "process_artifact"
    other = "other"


class KnowledgeInsightType(StrEnum):
    definition = "definition"
    method = "method"
    framework = "framework"
    principle = "principle"
    checklist = "checklist"
    metric = "metric"
    risk_control = "risk_control"
    bpmn_modeling = "bpmn_modeling"
    process_mining = "process_mining"
    digital_transformation = "digital_transformation"
    case_management = "case_management"


class ConfidenceLevel(StrEnum):
    low = "low"
    medium = "medium"
    high = "high"


class KnowledgeDocumentResponse(BaseModel):
    id: UUID
    title: str
    author: str | None
    source_type: KnowledgeSourceType
    subject_area: str | None
    language: str
    case_id: UUID | None
    filename: str
    mime_type: str | None
    doc_category: str
    status: KnowledgeDocumentStatus
    error_message: str | None
    text_char_count: int
    chunk_count: int
    created_at: datetime
    updated_at: datetime


class KnowledgeChunkResponse(BaseModel):
    id: UUID
    document_id: UUID
    chunk_index: int
    content: str
    char_start: int
    char_end: int
    created_at: datetime


class KnowledgeInsightResponse(BaseModel):
    id: UUID
    document_id: UUID
    chunk_id: UUID
    insight_type: KnowledgeInsightType
    topic: str
    title_es: str
    summary_es: str
    source_excerpt: str
    source_language: str
    confidence_level: ConfidenceLevel
    created_by: str
    created_at: datetime


class KnowledgeLearningRunResponse(BaseModel):
    analyzed_documents: int
    created_insights: int
    total_insights: int


class CaseMethodologyPhaseResponse(BaseModel):
    phase: str
    objective_es: str
    actions_es: list[str]
    outputs_es: list[str]
    quality_checks_es: list[str]
    related_topics: list[str]
    source_insight_count: int


class CaseMethodologyResponse(BaseModel):
    title: str
    language: str
    source_insight_count: int
    phases: list[CaseMethodologyPhaseResponse]


class AgentTrainingArtifactResponse(BaseModel):
    name: str
    kind: str
    path: str
    exists: bool
    size_bytes: int | None = None


class AgentTrainingProfileResponse(BaseModel):
    profile_name: str
    training_mode: str
    language: str
    books_processed: int
    pages_processed: int
    extracted_characters: int
    insights: int
    methodology_phases: int
    dataset_examples: int
    graph_is_visual: bool
    obsidian_vault_path: str
    obsidian_canvas_path: str
    artifacts: list[AgentTrainingArtifactResponse]
    limitations: list[str]
    next_step: str
