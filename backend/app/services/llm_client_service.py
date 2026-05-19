"""
LLM Client Service
==================
Cliente unificado que abstrae la llamada real a cada proveedor LLM:
  - Gemini 2.5 Pro / Flash  (google-generativeai)
  - Deepseek V3 API         (API compatible con OpenAI)
  - Groq + Llama 4          (groq SDK)
  - Ollama local            (httpx directo)

No depende de LangChain para mantener el proyecto liviano y auditable.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any

import httpx

from app.core.config import settings
from app.services.llm_router_service import AgentTask, LLMProvider, LLMRouterService

logger = logging.getLogger(__name__)

# Temperatura por defecto si no hay tarea disponible
_DEFAULT_TEMP = 0.3
_REQUEST_TIMEOUT = 120.0


@dataclass
class LLMResponse:
    content: str
    provider: str
    model: str
    tokens_used: int | None = None
    error: str | None = None

    @property
    def success(self) -> bool:
        return self.error is None and bool(self.content)


class LLMClientService:
    """
    Llama al LLM seleccionado por el router y retorna LLMResponse.
    Maneja el fallback automático si el provider falla.
    """

    def __init__(
        self,
        router: LLMRouterService | None = None,
        empresa_modo_privado: bool = False,
    ) -> None:
        self._router = router or LLMRouterService(
            empresa_modo_privado=empresa_modo_privado,
            internet_disponible=True,
            gemini_con_cuota=bool(settings.gemini_api_key),
            deepseek_con_cuota=bool(settings.deepseek_api_key),
            groq_con_cuota=bool(settings.groq_api_key),
            ollama_disponible=self._check_ollama(),
        )

    # ── Punto de entrada principal ─────────────────────────────────────────────

    def completar(
        self,
        system_prompt: str,
        user_message: str,
        historial: list[dict[str, str]] | None = None,
        tarea: AgentTask = AgentTask.chat_simple,
        tokens_requeridos: int = 0,
        forzar_provider: LLMProvider | None = None,
    ) -> LLMResponse:
        """
        Genera una respuesta del LLM elegido con fallback automático.

        Args:
            system_prompt: Instrucciones del sistema (rol del agente).
            user_message:  Mensaje actual del usuario.
            historial:     Lista de {"role": "user"|"assistant", "content": "..."}.
            tarea:         Tipo de tarea para la selección del LLM.
            tokens_requeridos: Estimación de tokens del contexto RAG.
            forzar_provider: Si se especifica, ignora la selección automática.
        """
        historial = historial or []
        provider = forzar_provider or self._router.seleccionar(tarea, tokens_requeridos)
        temperatura = LLMRouterService.temperatura(provider, tarea)

        try:
            return self._llamar(provider, system_prompt, user_message, historial, temperatura)
        except Exception as exc:  # noqa: BLE001
            logger.warning("Provider %s falló: %s. Intentando fallback.", provider, exc)
            return self._fallback(provider, system_prompt, user_message, historial, str(exc))

    # ── Dispatcher por provider ────────────────────────────────────────────────

    def _llamar(
        self,
        provider: LLMProvider,
        system_prompt: str,
        user_message: str,
        historial: list[dict[str, str]],
        temperatura: float,
    ) -> LLMResponse:
        import os
        import json
        
        # MOCK GLOBAL PARA PRUEBAS SIN LLM
        if os.environ.get("MOCK_LLM", "false").lower() == "true":
            logger.info("[MOCK] Interceptando llamada al LLM para devolver datos ficticios.")
            content = "Respuesta generada por el MOCK_LLM. "
            if "BPMN" in system_prompt or "as_is" in str(user_message):
                content = '<?xml version="1.0" encoding="UTF-8"?><bpmn:definitions xmlns:bpmn="http://www.omg.org/spec/BPMN/20100524/MODEL" id="Definitions_Mock"><bpmn:process id="Process_Mock" isExecutable="false"><bpmn:startEvent id="StartEvent_1" /></bpmn:process></bpmn:definitions>'
            elif "Documental" in system_prompt or "{" in system_prompt:
                # Simular JSON de respuesta
                content = json.dumps({
                    "code": "MOCK-001",
                    "title": "Documento Mock",
                    "objective": "Objetivo de prueba sin LLM.",
                    "scope": "Alcance de prueba.",
                    "responsibilities": "MOCK",
                    "content": "# MOCK\nEsto es un texto generado sin descargar LLMs.",
                    "next_action_es": "Avanzar a la fase de diseño."
                })
            else:
                # Tratar de devolver un JSON genérico si se pide, o texto
                if "{" in system_prompt or "JSON" in system_prompt:
                    content = json.dumps({"next_action_es": "Avanzar a la siguiente etapa de diseño."})

            return LLMResponse(content=content, provider="mock_local", model="mock-model", tokens_used=10)

        dispatch = {
            LLMProvider.gemini: self._gemini,
            LLMProvider.gemini_flash: self._gemini_flash,
            LLMProvider.deepseek_api: self._deepseek_api,
            LLMProvider.groq: self._groq,
            LLMProvider.deepseek_local: self._ollama_reasoning,
            LLMProvider.deepseek_coder_local: self._ollama_coder,
            LLMProvider.qwen_local: self._ollama_fast,
        }
        handler = dispatch.get(provider)
        if handler is None:
            raise ValueError(f"Provider desconocido: {provider}")
        return handler(system_prompt, user_message, historial, temperatura)

    def _fallback(
        self,
        failed_provider: LLMProvider,
        system_prompt: str,
        user_message: str,
        historial: list[dict[str, str]],
        original_error: str,
    ) -> LLMResponse:
        """Intenta la cadena de fallback si el provider principal falla."""
        fallback_order = [
            LLMProvider.gemini_flash,
            LLMProvider.deepseek_api,
            LLMProvider.groq,
            LLMProvider.deepseek_local,
        ]
        for candidate in fallback_order:
            if candidate == failed_provider:
                continue
            try:
                logger.info("Intentando fallback con %s", candidate)
                result = self._llamar(candidate, system_prompt, user_message, historial, _DEFAULT_TEMP)
                if result.success:
                    return result
            except Exception as exc:  # noqa: BLE001
                logger.warning("Fallback %s también falló: %s", candidate, exc)

        return LLMResponse(
            content="",
            provider=failed_provider.value,
            model="none",
            error=f"Todos los LLMs fallaron. Error original: {original_error}",
        )

    # ── Implementaciones por proveedor ─────────────────────────────────────────

    def _gemini(
        self,
        system_prompt: str,
        user_message: str,
        historial: list[dict[str, str]],
        temperatura: float,
    ) -> LLMResponse:
        try:
            import google.generativeai as genai  # type: ignore[import]
        except ImportError as exc:
            raise RuntimeError("google-generativeai no instalado. Ejecuta: pip install google-generativeai") from exc

        genai.configure(api_key=settings.gemini_api_key)
        model = genai.GenerativeModel(
            model_name=settings.gemini_model,
            system_instruction=system_prompt,
            generation_config={"temperature": temperatura, "max_output_tokens": 8192},
        )
        chat = model.start_chat(history=self._to_gemini_history(historial))
        response = chat.send_message(user_message)
        text = response.text or ""
        return LLMResponse(content=text, provider="gemini", model=settings.gemini_model)

    def _gemini_flash(
        self,
        system_prompt: str,
        user_message: str,
        historial: list[dict[str, str]],
        temperatura: float,
    ) -> LLMResponse:
        try:
            import google.generativeai as genai  # type: ignore[import]
        except ImportError as exc:
            raise RuntimeError("google-generativeai no instalado") from exc

        genai.configure(api_key=settings.gemini_api_key)
        model = genai.GenerativeModel(
            model_name=settings.gemini_flash_model,
            system_instruction=system_prompt,
            generation_config={"temperature": temperatura, "max_output_tokens": 4096},
        )
        chat = model.start_chat(history=self._to_gemini_history(historial))
        response = chat.send_message(user_message)
        text = response.text or ""
        return LLMResponse(content=text, provider="gemini_flash", model=settings.gemini_flash_model)

    def _deepseek_api(
        self,
        system_prompt: str,
        user_message: str,
        historial: list[dict[str, str]],
        temperatura: float,
    ) -> LLMResponse:
        messages = self._build_openai_messages(system_prompt, historial, user_message)
        with httpx.Client(timeout=_REQUEST_TIMEOUT) as client:
            response = client.post(
                "https://api.deepseek.com/chat/completions",
                headers={
                    "Authorization": f"Bearer {settings.deepseek_api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": settings.deepseek_model,
                    "messages": messages,
                    "temperature": temperatura,
                    "max_tokens": 4096,
                },
            )
            response.raise_for_status()
            data: dict[str, Any] = response.json()
        content: str = data["choices"][0]["message"]["content"]
        usage: dict[str, Any] = data.get("usage", {})
        return LLMResponse(
            content=content,
            provider="deepseek_api",
            model=settings.deepseek_model,
            tokens_used=usage.get("total_tokens"),
        )

    def _groq(
        self,
        system_prompt: str,
        user_message: str,
        historial: list[dict[str, str]],
        temperatura: float,
    ) -> LLMResponse:
        try:
            from groq import Groq  # type: ignore[import]
        except ImportError as exc:
            raise RuntimeError("groq no instalado. Ejecuta: pip install groq") from exc

        client = Groq(api_key=settings.groq_api_key)
        messages = self._build_openai_messages(system_prompt, historial, user_message)
        completion = client.chat.completions.create(
            model=settings.groq_model,
            messages=messages,  # type: ignore[arg-type]
            temperature=temperatura,
            max_tokens=2048,
        )
        content = completion.choices[0].message.content or ""
        return LLMResponse(
            content=content,
            provider="groq",
            model=settings.groq_model,
            tokens_used=completion.usage.total_tokens if completion.usage else None,
        )

    def _ollama_reasoning(
        self,
        system_prompt: str,
        user_message: str,
        historial: list[dict[str, str]],
        temperatura: float,
    ) -> LLMResponse:
        return self._ollama_call(
            model=settings.ollama_reasoning_model,
            system_prompt=system_prompt,
            user_message=user_message,
            historial=historial,
            temperatura=temperatura,
            provider_name="deepseek_local",
        )

    def _ollama_coder(
        self,
        system_prompt: str,
        user_message: str,
        historial: list[dict[str, str]],
        temperatura: float,
    ) -> LLMResponse:
        return self._ollama_call(
            model=settings.ollama_coder_model,
            system_prompt=system_prompt,
            user_message=user_message,
            historial=historial,
            temperatura=temperatura,
            provider_name="deepseek_coder_local",
        )

    def _ollama_fast(
        self,
        system_prompt: str,
        user_message: str,
        historial: list[dict[str, str]],
        temperatura: float,
    ) -> LLMResponse:
        return self._ollama_call(
            model=settings.ollama_fast_model,
            system_prompt=system_prompt,
            user_message=user_message,
            historial=historial,
            temperatura=temperatura,
            provider_name="qwen_local",
        )

    def _ollama_call(
        self,
        model: str,
        system_prompt: str,
        user_message: str,
        historial: list[dict[str, str]],
        temperatura: float,
        provider_name: str,
    ) -> LLMResponse:
        messages = self._build_openai_messages(system_prompt, historial, user_message)
        with httpx.Client(timeout=_REQUEST_TIMEOUT) as client:
            response = client.post(
                f"{settings.ollama_base_url}/api/chat",
                json={
                    "model": model,
                    "messages": messages,
                    "stream": False,
                    "options": {"temperature": temperatura},
                },
            )
            response.raise_for_status()
            data: dict[str, Any] = response.json()
        content: str = data.get("message", {}).get("content", "")
        return LLMResponse(content=content, provider=provider_name, model=model)

    # ── Helpers de formato ─────────────────────────────────────────────────────

    @staticmethod
    def _build_openai_messages(
        system_prompt: str,
        historial: list[dict[str, str]],
        user_message: str,
    ) -> list[dict[str, str]]:
        messages: list[dict[str, str]] = [{"role": "system", "content": system_prompt}]
        for msg in historial:
            if msg.get("role") in {"user", "assistant"} and msg.get("content"):
                messages.append({"role": msg["role"], "content": msg["content"]})
        messages.append({"role": "user", "content": user_message})
        return messages

    @staticmethod
    def _to_gemini_history(historial: list[dict[str, str]]) -> list[dict[str, Any]]:
        """Convierte historial OpenAI-style a formato Gemini."""
        result: list[dict[str, Any]] = []
        for msg in historial:
            role = "model" if msg.get("role") == "assistant" else "user"
            content = msg.get("content", "")
            if content:
                result.append({"role": role, "parts": [content]})
        return result

    @staticmethod
    def _check_ollama() -> bool:
        """Verifica si Ollama está disponible localmente."""
        try:
            response = httpx.get(f"{settings.ollama_base_url}/api/tags", timeout=2.0)
            return response.status_code < 500
        except httpx.HTTPError:
            return False
