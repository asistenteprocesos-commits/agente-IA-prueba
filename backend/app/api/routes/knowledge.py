from uuid import UUID

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.knowledge import (
    AgentTrainingProfileResponse,
    CaseMethodologyResponse,
    KnowledgeChunkResponse,
    KnowledgeDocumentResponse,
    KnowledgeInsightResponse,
    KnowledgeLearningRunResponse,
    KnowledgeSourceType,
)
from app.services.knowledge_service import KnowledgeService

router = APIRouter()


@router.get("/documents", response_model=list[KnowledgeDocumentResponse])
def list_knowledge_documents(
    case_id: UUID | None = None,
    db: Session = Depends(get_db),
) -> list[KnowledgeDocumentResponse]:
    return KnowledgeService(db).list_documents(case_id=case_id)


@router.post(
    "/documents",
    response_model=KnowledgeDocumentResponse,
    status_code=status.HTTP_201_CREATED,
)
async def upload_knowledge_document(
    file: UploadFile = File(...),
    title: str | None = Form(default=None),
    author: str | None = Form(default=None),
    source_type: KnowledgeSourceType = Form(default=KnowledgeSourceType.book),
    subject_area: str | None = Form(default=None),
    language: str = Form(default="es"),
    case_id: UUID | None = Form(default=None),
    db: Session = Depends(get_db),
) -> KnowledgeDocumentResponse:
    return await KnowledgeService(db).ingest_document(
        file=file,
        title=title,
        author=author,
        source_type=source_type,
        subject_area=subject_area,
        language=language,
        case_id=case_id,
    )


@router.post(
    "/documents/bulk",
    response_model=list[KnowledgeDocumentResponse],
    status_code=status.HTTP_201_CREATED,
)
async def upload_knowledge_documents_bulk(
    files: list[UploadFile] = File(...),
    author: str | None = Form(default=None),
    source_type: KnowledgeSourceType = Form(default=KnowledgeSourceType.book),
    subject_area: str | None = Form(default=None),
    language: str = Form(default="es"),
    case_id: UUID | None = Form(default=None),
    db: Session = Depends(get_db),
) -> list[KnowledgeDocumentResponse]:
    service = KnowledgeService(db)
    documents: list[KnowledgeDocumentResponse] = []
    for file in files:
        documents.append(
            await service.ingest_document(
                file=file,
                title=None,
                author=author,
                source_type=source_type,
                subject_area=subject_area,
                language=language,
                case_id=case_id,
            )
        )
    return documents


@router.get(
    "/documents/{document_id}/chunks",
    response_model=list[KnowledgeChunkResponse],
)
def list_knowledge_chunks(
    document_id: UUID,
    db: Session = Depends(get_db),
) -> list[KnowledgeChunkResponse]:
    chunks = KnowledgeService(db).list_chunks(document_id)
    if chunks is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Knowledge document not found",
        )

    return chunks


@router.post(
    "/documents/{document_id}/analyze",
    response_model=KnowledgeLearningRunResponse,
    status_code=status.HTTP_201_CREATED,
)
def analyze_knowledge_document(
    document_id: UUID,
    db: Session = Depends(get_db),
) -> KnowledgeLearningRunResponse:
    result = KnowledgeService(db).analyze_document(document_id)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Knowledge document not found",
        )
    return result


@router.post(
    "/learning/analyze",
    response_model=KnowledgeLearningRunResponse,
    status_code=status.HTTP_201_CREATED,
)
def analyze_knowledge_library(db: Session = Depends(get_db)) -> KnowledgeLearningRunResponse:
    return KnowledgeService(db).analyze_library()


@router.get("/insights", response_model=list[KnowledgeInsightResponse])
def list_knowledge_insights(
    topic: str | None = None,
    limit: int = 100,
    db: Session = Depends(get_db),
) -> list[KnowledgeInsightResponse]:
    return KnowledgeService(db).list_insights(topic=topic, limit=limit)


@router.get("/case-methodology", response_model=CaseMethodologyResponse)
def get_case_methodology(db: Session = Depends(get_db)) -> CaseMethodologyResponse:
    return KnowledgeService(db).build_case_methodology()


@router.get("/agent-training-profile", response_model=AgentTrainingProfileResponse)
def get_agent_training_profile(db: Session = Depends(get_db)) -> AgentTrainingProfileResponse:
    return KnowledgeService(db).load_agent_training_profile()
