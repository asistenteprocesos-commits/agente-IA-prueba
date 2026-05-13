from datetime import datetime
from enum import StrEnum
from uuid import UUID

from pydantic import BaseModel, Field


class OrchestrationRunStatus(StrEnum):
    not_started = "not_started"
    running = "running"
    waiting_human = "waiting_human"
    completed = "completed"
    error = "error"


class OrchestrationPhaseStatus(StrEnum):
    pending = "pending"
    in_progress = "in_progress"
    blocked_checkpoint = "blocked_checkpoint"
    completed = "completed"
    error = "error"


class CheckpointStatus(StrEnum):
    not_required = "not_required"
    pending = "pending"
    approved = "approved"
    rejected = "rejected"


class CheckpointAction(StrEnum):
    approve = "approve"
    reject = "reject"


class OrchestrationEventType(StrEnum):
    run_created = "run_created"
    run_started = "run_started"
    phase_started = "phase_started"
    checkpoint_requested = "checkpoint_requested"
    checkpoint_decision = "checkpoint_decision"
    phase_completed = "phase_completed"
    handoff_created = "handoff_created"
    rollback = "rollback"
    context_added = "context_added"
    run_completed = "run_completed"


class OrchestrationPhaseResponse(BaseModel):
    id: UUID
    run_id: UUID
    phase_number: int
    phase_key: str
    title: str
    agent_role: str
    objective_es: str
    expected_outputs_es: list[str]
    quality_checks_es: list[str]
    status: OrchestrationPhaseStatus
    requires_human_checkpoint: bool
    checkpoint_status: CheckpointStatus
    checkpoint_reviewer: str | None
    checkpoint_comment: str | None
    started_at: datetime | None
    completed_at: datetime | None
    updated_at: datetime


class OrchestrationEventResponse(BaseModel):
    id: UUID
    run_id: UUID
    phase_number: int | None
    event_type: OrchestrationEventType
    actor: str
    message_es: str
    payload: dict[str, object] | None
    created_at: datetime


class OrchestrationRunResponse(BaseModel):
    id: UUID
    case_id: UUID
    status: OrchestrationRunStatus
    current_phase_number: int
    context_summary: str | None
    last_error: str | None
    created_at: datetime
    updated_at: datetime


class OrchestrationStateResponse(BaseModel):
    run: OrchestrationRunResponse
    phases: list[OrchestrationPhaseResponse]
    events: list[OrchestrationEventResponse]
    next_action_es: str
    blockers_es: list[str]
    autonomy_progress_percent: int


class CheckpointDecisionCreate(BaseModel):
    action: CheckpointAction
    reviewer: str = Field(min_length=2, max_length=120)
    comment: str | None = Field(default=None, max_length=1200)


class OrchestrationContextCreate(BaseModel):
    actor: str = Field(default="Especialista BPM", min_length=2, max_length=120)
    message_es: str = Field(min_length=3, max_length=2000)
    payload: dict[str, object] | None = None
