from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.process_repository import (
    ArtifactCommentCreate,
    ArtifactCommentResponse,
    ArtifactDecisionCreate,
    ArtifactDecisionResponse,
    ArtifactEvidenceCreate,
    ArtifactEvidenceResponse,
    ArtifactQualityResponse,
    ArtifactVersionCreate,
    ArtifactVersionHistoryResponse,
    ArtifactVersionResponse,
    ProcessArtifactCreate,
    ProcessArtifactResponse,
    ProcessRepositoryResponse,
    VersionDiffResponse,
)
from app.services.process_repository_service import ProcessRepositoryService, VersionTransitionError

router = APIRouter()


@router.get("/{case_id}/repository", response_model=ProcessRepositoryResponse)
def get_process_repository(
    case_id: UUID,
    db: Session = Depends(get_db),
) -> ProcessRepositoryResponse:
    repository = ProcessRepositoryService(db).get_by_case_id(case_id)

    if repository is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Process repository not found",
        )

    return repository


@router.get("/{case_id}/repository/artifacts", response_model=list[ProcessArtifactResponse])
def list_process_artifacts(
    case_id: UUID,
    db: Session = Depends(get_db),
) -> list[ProcessArtifactResponse]:
    artifacts = ProcessRepositoryService(db).list_artifacts(case_id)

    if artifacts is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Process repository not found",
        )

    return artifacts


@router.post(
    "/{case_id}/repository/artifacts",
    response_model=ProcessArtifactResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_process_artifact(
    case_id: UUID,
    payload: ProcessArtifactCreate,
    db: Session = Depends(get_db),
) -> ProcessArtifactResponse:
    artifact = ProcessRepositoryService(db).create_artifact(case_id, payload)

    if artifact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Process repository not found",
        )

    return artifact


@router.post(
    "/{case_id}/repository/artifacts/{artifact_id}/versions",
    response_model=ArtifactVersionResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_artifact_version(
    case_id: UUID,
    artifact_id: UUID,
    payload: ArtifactVersionCreate,
    db: Session = Depends(get_db),
) -> ArtifactVersionResponse:
    try:
        version = ProcessRepositoryService(db).create_artifact_version(artifact_id, payload)
    except VersionTransitionError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(error),
        ) from error

    if version is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Process artifact not found",
        )

    return version


@router.post(
    "/{case_id}/repository/artifact-versions/{version_id}/decisions",
    response_model=ArtifactDecisionResponse,
    status_code=status.HTTP_201_CREATED,
)
def decide_artifact_version(
    case_id: UUID,
    version_id: UUID,
    payload: ArtifactDecisionCreate,
    db: Session = Depends(get_db),
) -> ArtifactDecisionResponse:
    try:
        decision = ProcessRepositoryService(db).decide_version(version_id, payload)
    except VersionTransitionError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(error),
        ) from error

    if decision is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Artifact version not found",
        )

    return decision


@router.post(
    "/{case_id}/repository/artifact-versions/{version_id}/comments",
    response_model=ArtifactCommentResponse,
    status_code=status.HTTP_201_CREATED,
)
def comment_artifact_version(
    case_id: UUID,
    version_id: UUID,
    payload: ArtifactCommentCreate,
    db: Session = Depends(get_db),
) -> ArtifactCommentResponse:
    comment = ProcessRepositoryService(db).add_comment(version_id, payload)

    if comment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Artifact version not found",
        )

    return comment


@router.get(
    "/{case_id}/repository/artifact-versions/{version_id}/history",
    response_model=ArtifactVersionHistoryResponse,
)
def get_artifact_version_history(
    case_id: UUID,
    version_id: UUID,
    db: Session = Depends(get_db),
) -> ArtifactVersionHistoryResponse:
    history = ProcessRepositoryService(db).get_version_history(version_id)

    if history is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Artifact version not found",
        )

    return history


@router.get(
    "/{case_id}/repository/artifact-versions/{base_version_id}/diff/{target_version_id}",
    response_model=VersionDiffResponse,
)
def compare_artifact_versions(
    case_id: UUID,
    base_version_id: UUID,
    target_version_id: UUID,
    db: Session = Depends(get_db),
) -> VersionDiffResponse:
    diff = ProcessRepositoryService(db).compare_versions(base_version_id, target_version_id)

    if diff is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Artifact version not found",
        )

    return diff


@router.post(
    "/{case_id}/repository/artifact-versions/{version_id}/evidence",
    response_model=ArtifactEvidenceResponse,
    status_code=status.HTTP_201_CREATED,
)
def add_artifact_evidence(
    case_id: UUID,
    version_id: UUID,
    payload: ArtifactEvidenceCreate,
    db: Session = Depends(get_db),
) -> ArtifactEvidenceResponse:
    evidence = ProcessRepositoryService(db).add_evidence(version_id, payload)

    if evidence is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Artifact version not found",
        )

    return evidence


@router.get(
    "/{case_id}/repository/artifact-versions/{version_id}/evidence",
    response_model=list[ArtifactEvidenceResponse],
)
def list_artifact_evidence(
    case_id: UUID,
    version_id: UUID,
    db: Session = Depends(get_db),
) -> list[ArtifactEvidenceResponse]:
    evidence = ProcessRepositoryService(db).list_evidence(version_id)

    if evidence is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Artifact version not found",
        )

    return evidence


@router.get(
    "/{case_id}/repository/artifact-versions/{version_id}/quality",
    response_model=ArtifactQualityResponse,
)
def evaluate_artifact_quality(
    case_id: UUID,
    version_id: UUID,
    db: Session = Depends(get_db),
) -> ArtifactQualityResponse:
    quality = ProcessRepositoryService(db).evaluate_quality(version_id)

    if quality is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Artifact version not found",
        )

    return quality
