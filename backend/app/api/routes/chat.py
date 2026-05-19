from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.chat import (
    ChatMessageCreate,
    ChatMessageResponse,
    ChatSessionCreate,
    ChatSessionResponse,
    LLMStatusResponse,
    LLMSystemStatusResponse,
    RAGFragmentResponse,
    RAGSearchRequest,
    RAGSearchResponse,
)
from app.services.chat_service import ChatService
from app.services.llm_client_service import LLMClientService
from app.services.llm_router_service import AgentTask, LLMRouterService
from app.services.rag_service import RAGService
from app.core.config import settings

router = APIRouter()


# ── Sesiones de chat ──────────────────────────────────────────────────────────

@router.post("/sessions", response_model=ChatSessionResponse, status_code=status.HTTP_201_CREATED)
def crear_sesion(payload: ChatSessionCreate, db: Session = Depends(get_db)):
    """Crea una nueva sesión de chat con el agente BPMS."""
    svc = ChatService(db)
    return svc.crear_sesion(payload)


@router.get("/sessions", response_model=list[ChatSessionResponse])
def listar_sesiones(db: Session = Depends(get_db)):
    """Lista todas las sesiones de chat."""
    svc = ChatService(db)
    return svc.listar_sesiones()


@router.get("/sessions/{session_id}", response_model=ChatSessionResponse)
def obtener_sesion(session_id: UUID, db: Session = Depends(get_db)):
    """Obtiene una sesión de chat por ID."""
    svc = ChatService(db)
    result = svc.obtener_sesion(session_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Sesión no encontrada")
    return result


# ── Mensajes ──────────────────────────────────────────────────────────────────

@router.get("/sessions/{session_id}/messages", response_model=list[ChatMessageResponse])
def listar_mensajes(session_id: UUID, db: Session = Depends(get_db)):
    """Lista todos los mensajes de una sesión."""
    svc = ChatService(db)
    result = svc.listar_mensajes(session_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Sesión no encontrada")
    return result


@router.post(
    "/sessions/{session_id}/messages",
    response_model=ChatMessageResponse,
    status_code=status.HTTP_201_CREATED,
)
def enviar_mensaje(
    session_id: UUID,
    payload: ChatMessageCreate,
    db: Session = Depends(get_db),
):
    """Envía un mensaje al agente BPMS y recibe su respuesta."""
    svc = ChatService(db)
    result = svc.enviar_mensaje(session_id, payload)
    if result is None:
        raise HTTPException(status_code=404, detail="Sesión no encontrada")
    return result


# ── RAG / Búsqueda semántica ──────────────────────────────────────────────────

@router.post("/rag/search", response_model=RAGSearchResponse)
def buscar_rag(payload: RAGSearchRequest, db: Session = Depends(get_db)):
    """Busca fragmentos relevantes en la base de conocimiento (RAG)."""
    rag = RAGService(db)
    fragmentos = rag.buscar(
        query=payload.query,
        top_k=payload.top_k,
        case_id=payload.case_id,
        subject_area=payload.subject_area,
    )
    return RAGSearchResponse(
        query=payload.query,
        fragments=[
            RAGFragmentResponse(
                chunk_id=f.chunk_id,
                document_id=f.document_id,
                document_title=f.document_title,
                author=f.author,
                content=f.content[:600],
                score=f.score,
                chunk_index=f.chunk_index,
            )
            for f in fragmentos
        ],
        total_found=len(fragmentos),
    )


# ── Estado del sistema LLM ────────────────────────────────────────────────────

@router.get("/llm/status", response_model=LLMSystemStatusResponse)
def estado_llm(db: Session = Depends(get_db)):
    """Muestra el estado y disponibilidad de todos los proveedores LLM."""
    import httpx

    # Verificar Ollama
    ollama_ok = False
    try:
        r = httpx.get(f"{settings.ollama_base_url}/api/tags", timeout=2.0)
        ollama_ok = r.status_code < 500
    except Exception:  # noqa: BLE001
        pass

    providers = [
        LLMStatusResponse(
            provider="Gemini 2.5 Pro",
            model=settings.gemini_model,
            available=bool(settings.gemini_api_key),
            api_key_configured=bool(settings.gemini_api_key),
            notes="Gratis en aistudio.google.com — 1M tokens contexto",
        ),
        LLMStatusResponse(
            provider="Gemini 2.5 Flash",
            model=settings.gemini_flash_model,
            available=bool(settings.gemini_api_key),
            api_key_configured=bool(settings.gemini_api_key),
            notes="Fallback de Gemini Pro — respuestas más rápidas",
        ),
        LLMStatusResponse(
            provider="Deepseek V3 API",
            model=settings.deepseek_model,
            available=bool(settings.deepseek_api_key),
            api_key_configured=bool(settings.deepseek_api_key),
            notes="Ideal para BPMN XML y código — casi gratuito",
        ),
        LLMStatusResponse(
            provider="Groq + Llama 4",
            model=settings.groq_model,
            available=bool(settings.groq_api_key),
            api_key_configured=bool(settings.groq_api_key),
            notes="Gratis en console.groq.com — clasificación y chat simple",
        ),
        LLMStatusResponse(
            provider="Ollama Local (DeepSeek-R1)",
            model=settings.ollama_reasoning_model,
            available=ollama_ok,
            api_key_configured=True,
            notes="Sin internet — instalar en la PC de pruebas",
        ),
        LLMStatusResponse(
            provider="Ollama Local (DeepSeek Coder)",
            model=settings.ollama_coder_model,
            available=ollama_ok,
            api_key_configured=True,
            notes="BPMN/código offline — instalar en la PC de pruebas",
        ),
    ]

    router_svc = LLMRouterService(
        internet_disponible=True,
        gemini_con_cuota=bool(settings.gemini_api_key),
        deepseek_con_cuota=bool(settings.deepseek_api_key),
        groq_con_cuota=bool(settings.groq_api_key),
        ollama_disponible=ollama_ok,
    )
    active = router_svc.seleccionar(AgentTask.chat_simple)

    return LLMSystemStatusResponse(
        providers=providers,
        active_provider=active.value,
        ollama_available=ollama_ok,
        internet_available=True,
    )
