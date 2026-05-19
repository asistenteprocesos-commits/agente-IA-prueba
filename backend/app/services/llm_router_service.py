"""
LLM Router Service
==================
Selecciona automáticamente el LLM más adecuado según:
- Tipo de agente y tarea
- Disponibilidad de internet y cuota
- Política de privacidad de la empresa
- Fallback automático en cadena

Prioridad (del system prompt):
  1. Groq Llama 4        → clasificación, normalización, chat simple (gratis, rápido)
  2. Deepseek V3 API     → código, BPMN XML, cálculos (casi gratis)
  3. Gemini 2.5 Pro      → análisis profundo, process mining, simulación (gratis)
  4. Gemini 2.5 Flash    → fallback si Pro está al límite
  5. Deepseek local      → modo offline o privacidad estricta (Ollama)
  6. Deepseek Coder local→ BPMN/código sin internet (Ollama)
  7. Qwen fast local     → tareas livianas offline (Ollama)
"""

from __future__ import annotations

import logging
from enum import Enum

logger = logging.getLogger(__name__)


class LLMProvider(str, Enum):
    gemini = "gemini"
    gemini_flash = "gemini_flash"
    deepseek_api = "deepseek_api"
    groq = "groq"
    deepseek_local = "deepseek_local"
    deepseek_coder_local = "deepseek_coder_local"
    qwen_local = "qwen_local"


class AgentTask(str, Enum):
    # Tareas simples / rápidas
    clasificacion = "clasificacion"
    normalizacion = "normalizacion"
    chat_simple = "chat_simple"

    # Código / estructuras
    bpmn_xml = "bpmn_xml"
    codigo_python = "codigo_python"
    sql = "sql"
    analisis_datos = "analisis_datos"

    # Análisis complejos
    process_mining = "process_mining"
    simulacion = "simulacion"
    consulta_bpm = "consulta_bpm"
    analisis_cualitativo = "analisis_cualitativo"
    metodologia = "metodologia"
    as_is = "as_is"
    to_be = "to_be"
    analisis_cuantitativo = "analisis_cuantitativo"


# Mapa agente → tarea principal
AGENT_TASK_MAP: dict[str, AgentTask] = {
    "orquestador": AgentTask.clasificacion,
    "consultor_bpm": AgentTask.consulta_bpm,
    "metodologias": AgentTask.metodologia,
    "as_is": AgentTask.as_is,
    "to_be": AgentTask.to_be,
    "bpmn": AgentTask.bpmn_xml,
    "simulacion": AgentTask.simulacion,
    "process_mining": AgentTask.process_mining,
    "analisis_cuantitativo": AgentTask.analisis_cuantitativo,
    "analisis_cualitativo": AgentTask.analisis_cualitativo,
    "chat": AgentTask.chat_simple,
}

# Tareas simples → Groq
_GROQ_TASKS = {AgentTask.clasificacion, AgentTask.normalizacion, AgentTask.chat_simple}

# Tareas de código/estructura → Deepseek API
_DEEPSEEK_TASKS = {AgentTask.bpmn_xml, AgentTask.codigo_python, AgentTask.sql, AgentTask.analisis_datos}

# Tareas de análisis profundo → Gemini Pro
_GEMINI_TASKS = {
    AgentTask.process_mining,
    AgentTask.simulacion,
    AgentTask.consulta_bpm,
    AgentTask.analisis_cualitativo,
    AgentTask.metodologia,
    AgentTask.as_is,
    AgentTask.to_be,
    AgentTask.analisis_cuantitativo,
}


class LLMRouterService:
    """
    Selecciona el LLM correcto según la lógica del system prompt BPMS.
    No instancia clientes — eso lo hace LLMClientService.
    """

    def __init__(
        self,
        empresa_modo_privado: bool = False,
        internet_disponible: bool = True,
        gemini_con_cuota: bool = True,
        deepseek_con_cuota: bool = True,
        groq_con_cuota: bool = True,
        ollama_disponible: bool = False,
    ) -> None:
        self.empresa_modo_privado = empresa_modo_privado
        self.internet_disponible = internet_disponible
        self.gemini_con_cuota = gemini_con_cuota
        self.deepseek_con_cuota = deepseek_con_cuota
        self.groq_con_cuota = groq_con_cuota
        self.ollama_disponible = ollama_disponible

    def seleccionar(
        self,
        tarea: AgentTask,
        tokens_requeridos: int = 0,
    ) -> LLMProvider:
        """Retorna el LLMProvider más adecuado para la tarea dada."""

        # 0. Empresa modo privado → solo Ollama local
        if self.empresa_modo_privado:
            if tarea in {AgentTask.bpmn_xml, AgentTask.codigo_python, AgentTask.sql}:
                return LLMProvider.deepseek_coder_local
            return LLMProvider.deepseek_local

        # 1. Sin internet → Ollama local
        if not self.internet_disponible:
            if tarea in {AgentTask.bpmn_xml, AgentTask.codigo_python}:
                return LLMProvider.deepseek_coder_local
            return LLMProvider.deepseek_local

        # 2. Tareas simples/rápidas → Groq (gratis, instantáneo)
        if tarea in _GROQ_TASKS and self.groq_con_cuota:
            return LLMProvider.groq

        # 3. Código / BPMN XML → Deepseek V3 API (temperatura baja, preciso)
        if tarea in _DEEPSEEK_TASKS and self.deepseek_con_cuota:
            return LLMProvider.deepseek_api

        # 4. Análisis profundo / contexto largo → Gemini Pro
        if tarea in _GEMINI_TASKS or tokens_requeridos > 10_000:
            if self.gemini_con_cuota:
                return LLMProvider.gemini
            return LLMProvider.gemini_flash

        # 5. Deepseek como respaldo general
        if self.deepseek_con_cuota:
            return LLMProvider.deepseek_api

        # 6. Groq como respaldo
        if self.groq_con_cuota:
            return LLMProvider.groq

        # 7. Todo agotado → Ollama local
        if self.ollama_disponible:
            return LLMProvider.deepseek_local

        # Fallback final (Gemini Flash aunque no tenga cuota confirmada)
        logger.warning("No hay LLM disponible con cuota confirmada, intentando Gemini Flash")
        return LLMProvider.gemini_flash

    def seleccionar_por_agente(
        self,
        agente: str,
        tokens_requeridos: int = 0,
    ) -> LLMProvider:
        """Atajo: dado un nombre de agente, retorna el LLM correspondiente."""
        tarea = AGENT_TASK_MAP.get(agente, AgentTask.chat_simple)
        return self.seleccionar(tarea, tokens_requeridos)

    # ── Metadatos de cada LLM ──────────────────────────────────────────────────

    @staticmethod
    def max_contexto_rag(provider: LLMProvider) -> int:
        """Número máximo de fragmentos RAG a incluir según el provider."""
        limits = {
            LLMProvider.gemini: 20,
            LLMProvider.gemini_flash: 10,
            LLMProvider.deepseek_api: 3,
            LLMProvider.groq: 2,
            LLMProvider.deepseek_local: 4,
            LLMProvider.deepseek_coder_local: 3,
            LLMProvider.qwen_local: 2,
        }
        return limits.get(provider, 5)

    @staticmethod
    def max_historial(provider: LLMProvider) -> int:
        """Número máximo de mensajes de historial a incluir."""
        limits = {
            LLMProvider.gemini: 50,
            LLMProvider.gemini_flash: 20,
            LLMProvider.deepseek_api: 5,
            LLMProvider.groq: 3,
            LLMProvider.deepseek_local: 10,
            LLMProvider.deepseek_coder_local: 5,
            LLMProvider.qwen_local: 3,
        }
        return limits.get(provider, 10)

    @staticmethod
    def temperatura(provider: LLMProvider, tarea: AgentTask) -> float:
        """Temperatura recomendada según provider y tarea."""
        if tarea in {AgentTask.bpmn_xml, AgentTask.codigo_python, AgentTask.sql}:
            return 0.1
        if provider == LLMProvider.groq:
            return 0.4
        if provider in {LLMProvider.gemini, LLMProvider.gemini_flash}:
            return 0.2
        return 0.3
