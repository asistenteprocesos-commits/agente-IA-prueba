"""
Chat Service — Agente BPMS Conversacional
==========================================
Integra el system prompt del agente BPMS, RAG, normalización semántica y
el cliente multi-LLM para responder preguntas sobre gestión de procesos.

Flujo por mensaje:
  1. Normalizar vocabulario BPM del usuario
  2. Detectar agente / tarea adecuada
  3. Recuperar contexto RAG relevante
  4. Seleccionar LLM automáticamente
  5. Generar respuesta con citas de fuente
  6. Persistir historial en BD
"""

from __future__ import annotations

import re
from datetime import UTC, datetime
from uuid import UUID, uuid4

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.chat import ChatMessageModel, ChatSessionModel
from app.schemas.chat import (
    ChatMessageCreate,
    ChatMessageResponse,
    ChatSessionCreate,
    ChatSessionResponse,
)
from app.services.llm_client_service import LLMClientService
from app.services.llm_router_service import AgentTask, LLMProvider, LLMRouterService
from app.services.rag_service import RAGService

# ── System prompt maestro del Agente BPMS ─────────────────────────────────────
BPMS_SYSTEM_PROMPT = """Eres el Agente BPMS Experto, un arquitecto de procesos de talla mundial (Nivel Black Belt Lean Six Sigma / BPMN 2.0).
Tu objetivo es ayudar al usuario a levantar, analizar, modelar y optimizar procesos.

Tienes acceso a TRES fuentes de inteligencia. Úsalas sabiamente:
1. METODOLOGÍA (RAG adjunto abajo): Son las directrices teóricas (tus libros cargados). Aplica SIEMPRE estas reglas para la notación y calidad.
2. CONTEXTO CORPORATIVO: Es la información de la empresa actual que el usuario te menciona.
3. CONOCIMIENTO DEL MUNDO (Tu base pre-entrenada): Si la información de la empresa está incompleta (ej. el usuario solo dice "proceso de logística"), DEBES USAR tu conocimiento pre-entrenado para inferir, sugerir y completar el proceso basándote en estándares internacionales de esa industria (ej. proponer un flujo típico de SCOR para logística). ¡No te quedes mudo, propon escenarios basados en tu vasta experiencia!

Reglas:
1. Sé conciso y profesional.
2. Si sugieres un rediseño, justifica con conceptos de Lean o Six Sigma.
3. Si modelas BPMN, sé estricto con el estándar y nunca rompas la sintaxis.

## TU ROL
Eres el orquestador que decide qué capacidad activar según lo que el usuario necesita:
- Consultor BPM: conceptos, marcos de referencia, mejores prácticas
- Levantamiento AS-IS: documentar proceso actual, identificar problemas
- Diseño TO-BE: proponer mejoras fundamentadas
- Modelado BPMN: generar o validar XML BPMN 2.0
- Análisis cuantitativo: métricas, tiempos de ciclo, capacidad, nivel sigma
- Análisis cualitativo: stakeholders, madurez, gestión del cambio
- Simulación: escenarios, sensibilidad, comparar alternativas
- Process Mining: analizar logs de eventos

## NORMALIZACIÓN SEMÁNTICA
Reconoces variaciones de términos:
- bpm / gestión de procesos / gerencia de procesos → BPM
- seis sigma / six sigma / DMAIC → Six Sigma
- lean / manufactura esbelta / TPS / Kaizen → Lean
- teoría de restricciones / Goldratt / cuello de botella → TOC
- as-is / estado actual / proceso actual → AS-IS
- to-be / estado futuro / proceso mejorado → TO-BE
- flujograma / mapa de proceso / diagrama → BPMN
- indicador / métrica / OCI → KPI

## REGLAS ESENCIALES
1. Normaliza el vocabulario antes de actuar
2. Cita siempre la fuente del fragmento RAG cuando lo uses
3. No inventes metodologías que no estén en la base de conocimiento
4. Sé progresivo — guía paso a paso sin saltar etapas
5. Propón mejoras con datos, impacto estimado y justificación técnica
6. Indica claramente si necesitas más información del usuario
7. Máximo 3 preguntas de aclaración antes de proceder
8. Usa SIEMPRE el lenguaje del usuario (español)
9. Para BPMN, genera XML 2.0 válido
10. Para métricas, usa tablas comparativas

## FORMATO DE RESPUESTA
- Usa markdown para estructurar
- Indica el agente/capacidad que está respondiendo
- Para métricas: tablas comparativas
- Para mejoras: bullets con justificación técnica
- Para BPMN: bloque XML con comentarios
"""

# ── Normalización semántica BPM ────────────────────────────────────────────────
SEMANTIC_MAP: dict[str, tuple[str, list[str]]] = {
    "bpm": ("BPM / Gestión por Procesos", [
        "gestión de procesos", "gestión por procesos", "gerencia de procesos",
        "administración de procesos", "business process management", "manejo de procesos",
    ]),
    "six_sigma": ("Six Sigma", [
        "seis sigma", "six sigma", "6 sigma", "6σ", "lean six sigma", "lss",
        "dmaic", "dmadv", "metodología sigma",
    ]),
    "lean": ("Lean Manufacturing", [
        "lean manufacturing", "lean management", "manufactura esbelta", "manufactura delgada",
        "metodología lean", "producción esbelta", "toyota production system", "tps", "kaizen",
    ]),
    "toc": ("Teoría de Restricciones (TOC)", [
        "teoría de restricciones", "teoría de las limitaciones", "goldratt",
        "restricciones", "cuello de botella", "theory of constraints",
    ]),
    "asis": ("AS-IS (Proceso Actual)", [
        "as-is", "as is", "estado actual", "proceso actual", "situación actual",
        "proceso existente", "diagnóstico actual", "proceso presente",
    ]),
    "tobe": ("TO-BE (Proceso Futuro)", [
        "to-be", "to be", "estado futuro", "proceso futuro", "proceso mejorado",
        "proceso optimizado", "situación deseada", "proceso objetivo",
    ]),
    "bpmn": ("BPMN / Notación de Procesos", [
        "notación de procesos", "diagrama de proceso", "flujograma",
        "mapa de proceso", "flujo de proceso", "business process model notation",
    ]),
    "kpi": ("KPI / Indicadores", [
        "indicador", "métrica", "indicador clave", "indicador de rendimiento",
        "medidor", "oci", "indicador de desempeño", "performance indicator",
    ]),
    "process_mining": ("Process Mining", [
        "minería de procesos", "minería de datos de procesos",
        "extracción de procesos", "descubrimiento de procesos",
    ]),
    "simulacion": ("Simulación de Procesos", [
        "simulación", "modelado", "escenarios", "what-if", "análisis de escenarios",
    ]),
}

# ── Detección de tarea por palabras clave ──────────────────────────────────────
TASK_KEYWORDS: list[tuple[AgentTask, list[str]]] = [
    (AgentTask.bpmn_xml, ["xml", "bpmn", "generar diagrama", "modelar", "flujograma", "genera el proceso"]),
    (AgentTask.process_mining, ["event log", "log de eventos", "minería", "variantes", "conformance"]),
    (AgentTask.simulacion, ["simular", "simulación", "escenario", "what-if", "proyección", "pronóstico"]),
    (AgentTask.analisis_cuantitativo, ["calcular", "tiempo de ciclo", "eficiencia", "nivel sigma", "dpmo", "capacidad"]),
    (AgentTask.analisis_cualitativo, ["stakeholder", "resistencia al cambio", "madurez", "cultura"]),
    (AgentTask.metodologia, ["six sigma", "lean", "toc", "kaizen", "dmaic", "metodología"]),
    (AgentTask.as_is, ["as-is", "proceso actual", "levantar", "levantamiento", "documentar proceso"]),
    (AgentTask.to_be, ["to-be", "mejorar", "optimizar", "rediseñar", "propuesta", "proceso futuro"]),
]


class ChatService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self._rag = RAGService(db)
        self._llm = LLMClientService()

    # ── Sesiones ───────────────────────────────────────────────────────────────

    def crear_sesion(self, payload: ChatSessionCreate) -> ChatSessionResponse:
        session = ChatSessionModel(
            id=str(uuid4()),
            case_id=str(payload.case_id) if payload.case_id else None,
            title=payload.title or "Nueva conversación BPMS",
        )
        self.db.add(session)
        self.db.commit()
        self.db.refresh(session)
        return self._session_to_response(session)

    def listar_sesiones(self) -> list[ChatSessionResponse]:
        stmt = select(ChatSessionModel).order_by(ChatSessionModel.created_at.desc())
        sessions = self.db.scalars(stmt).all()
        return [self._session_to_response(s) for s in sessions]

    def obtener_sesion(self, session_id: UUID) -> ChatSessionResponse | None:
        session = self.db.get(ChatSessionModel, str(session_id))
        return self._session_to_response(session) if session else None

    # ── Mensajes ───────────────────────────────────────────────────────────────

    def listar_mensajes(self, session_id: UUID) -> list[ChatMessageResponse] | None:
        session = self.db.get(ChatSessionModel, str(session_id))
        if session is None:
            return None
        stmt = (
            select(ChatMessageModel)
            .where(ChatMessageModel.session_id == str(session_id))
            .order_by(ChatMessageModel.created_at)
        )
        messages = self.db.scalars(stmt).all()
        return [self._msg_to_response(m) for m in messages]

    def enviar_mensaje(
        self,
        session_id: UUID,
        payload: ChatMessageCreate,
    ) -> ChatMessageResponse | None:
        session = self.db.get(ChatSessionModel, str(session_id))
        if session is None:
            return None

        # 1. Guardar mensaje del usuario
        user_msg = ChatMessageModel(
            id=str(uuid4()),
            session_id=str(session_id),
            role="user",
            content=payload.content,
        )
        self.db.add(user_msg)
        self.db.commit()

        # 2. Normalizar y detectar tarea
        normalized_terms = self._normalize_bpm_terms(payload.content)
        tarea = self._detectar_tarea(payload.content)

        # 3. Recuperar contexto RAG
        case_id = UUID(session.case_id) if session.case_id else None
        contexto_rag = self._rag.construir_contexto_rag(
            query=payload.content,
            case_id=case_id,
        )

        # 4. Construir system prompt enriquecido
        system_prompt = self._build_system_prompt(contexto_rag, normalized_terms)

        # 5. Recuperar historial reciente
        historial = self._get_historial(str(session_id), tarea)

        # 6. Llamar al LLM
        llm_response = self._llm.completar(
            system_prompt=system_prompt,
            user_message=payload.content,
            historial=historial,
            tarea=tarea,
        )

        # 7. Guardar respuesta del asistente
        content = llm_response.content if llm_response.success else (
            "Lo siento, no pude procesar tu consulta en este momento. "
            f"Error: {llm_response.error}"
        )
        assistant_msg = ChatMessageModel(
            id=str(uuid4()),
            session_id=str(session_id),
            role="assistant",
            content=content,
            llm_provider=llm_response.provider,
            llm_model=llm_response.model,
            rag_fragments_used=len(self._rag.buscar(payload.content, top_k=1, case_id=case_id)),
            normalized_terms=", ".join(normalized_terms) if normalized_terms else None,
            agent_task=tarea.value,
        )
        self.db.add(assistant_msg)

        # 8. Actualizar timestamp sesión
        session.updated_at = datetime.now(UTC)
        self.db.commit()
        self.db.refresh(assistant_msg)
        return self._msg_to_response(assistant_msg)

    # ── Helpers internos ───────────────────────────────────────────────────────

    def _normalize_bpm_terms(self, text: str) -> list[str]:
        """Detecta y normaliza términos BPM no estándar en el mensaje."""
        text_lower = text.lower()
        found: list[str] = []
        for _canonical, (label, variations) in SEMANTIC_MAP.items():
            for var in variations:
                if var in text_lower:
                    found.append(label)
                    break
        return list(dict.fromkeys(found))  # dedup preservando orden

    def _detectar_tarea(self, text: str) -> AgentTask:
        """Detecta el tipo de tarea BPM en el mensaje del usuario."""
        text_lower = text.lower()
        for tarea, keywords in TASK_KEYWORDS:
            for kw in keywords:
                if kw in text_lower:
                    return tarea
        return AgentTask.consulta_bpm

    def _build_system_prompt(
        self,
        contexto_rag: str,
        normalized_terms: list[str],
    ) -> str:
        prompt = BPMS_SYSTEM_PROMPT
        if normalized_terms:
            prompt += (
                f"\n\n## Términos detectados en esta consulta\n"
                + "\n".join(f"- {t}" for t in normalized_terms)
            )
        if contexto_rag:
            prompt += f"\n\n{contexto_rag}"
        else:
            prompt += (
                "\n\n## Base de conocimiento\n"
                "No se encontraron fragmentos específicos para esta consulta. "
                "Responde con tu conocimiento experto en BPM e indica claramente "
                "que la respuesta es basada en conocimiento general."
            )
        return prompt

    def _get_historial(
        self,
        session_id: str,
        tarea: AgentTask,
    ) -> list[dict[str, str]]:
        """Recupera los últimos N mensajes según el LLM que se va a usar."""
        router = LLMRouterService(
            internet_disponible=True,
            gemini_con_cuota=bool(settings.gemini_api_key),
            deepseek_con_cuota=bool(settings.deepseek_api_key),
            groq_con_cuota=bool(settings.groq_api_key),
        )
        provider = router.seleccionar(tarea)
        max_hist = LLMRouterService.max_historial(provider)

        stmt = (
            select(ChatMessageModel)
            .where(ChatMessageModel.session_id == session_id)
            .order_by(ChatMessageModel.created_at.desc())
            .limit(max_hist)
        )
        messages = list(reversed(self.db.scalars(stmt).all()))
        return [{"role": m.role, "content": m.content} for m in messages]

    # ── Conversores a schema ───────────────────────────────────────────────────

    @staticmethod
    def _session_to_response(session: ChatSessionModel) -> ChatSessionResponse:
        return ChatSessionResponse(
            id=UUID(session.id),
            case_id=UUID(session.case_id) if session.case_id else None,
            title=session.title,
            created_at=session.created_at,
            updated_at=session.updated_at,
        )

    @staticmethod
    def _msg_to_response(msg: ChatMessageModel) -> ChatMessageResponse:
        return ChatMessageResponse(
            id=UUID(msg.id),
            session_id=UUID(msg.session_id),
            role=msg.role,
            content=msg.content,
            llm_provider=msg.llm_provider,
            llm_model=msg.llm_model,
            rag_fragments_used=msg.rag_fragments_used,
            normalized_terms=msg.normalized_terms,
            agent_task=msg.agent_task,
            created_at=msg.created_at,
        )
