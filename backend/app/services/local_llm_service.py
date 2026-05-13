import shutil

import httpx

from app.core.config import settings
from app.schemas.local_llm import LocalLLMModelResponse, LocalLLMProfileResponse


class LocalLLMService:
    def get_profile(self) -> LocalLLMProfileResponse:
        runtime_path = shutil.which("ollama")
        pulled_models = self._list_ollama_models() if runtime_path else []

        reasoning_installed = self._has_model(
            pulled_models=pulled_models,
            configured_model=settings.ollama_reasoning_model,
        )
        embedding_installed = self._has_model(
            pulled_models=pulled_models,
            configured_model=settings.ollama_embedding_model,
        )

        return LocalLLMProfileResponse(
            provider=settings.local_llm_provider,
            runtime="Ollama",
            base_url=settings.ollama_base_url,
            runtime_installed=runtime_path is not None,
            server_available=bool(pulled_models) or self._ollama_is_available(),
            reasoning_model=settings.ollama_reasoning_model,
            embedding_model=settings.ollama_embedding_model,
            pulled_models=pulled_models,
            recommended_models=[
                LocalLLMModelResponse(
                    role="reasoning",
                    model=settings.ollama_reasoning_model,
                    purpose_es=(
                        "Razonamiento BPM avanzado, analisis de procesos, recomendaciones "
                        "y revision de casos con pensamiento paso a paso."
                    ),
                    required=True,
                    installed=reasoning_installed,
                ),
                LocalLLMModelResponse(
                    role="embedding",
                    model=settings.ollama_embedding_model,
                    purpose_es=(
                        "Machine learning documental: convertir fragmentos de libros en vectores "
                        "para busqueda semantica y RAG."
                    ),
                    required=True,
                    installed=embedding_installed,
                ),
                LocalLLMModelResponse(
                    role="reasoning_upgrade",
                    model=settings.ollama_reasoning_model_upgrade,
                    purpose_es="Mejor razonamiento local si la maquina tiene mas RAM o GPU.",
                    required=False,
                    installed=self._has_model(
                        pulled_models=pulled_models,
                        configured_model=settings.ollama_reasoning_model_upgrade,
                    ),
                ),
                LocalLLMModelResponse(
                    role="embedding_upgrade",
                    model=settings.ollama_embedding_model_upgrade,
                    purpose_es="Mejor calidad de recuperacion semantica si hay recursos suficientes.",
                    required=False,
                    installed=self._has_model(
                        pulled_models=pulled_models,
                        configured_model=settings.ollama_embedding_model_upgrade,
                    ),
                ),
            ],
            learning_strategy_es=[
                "No se hara fine tuning inicial con libros completos.",
                "El agente usara destilacion documental, embeddings, busqueda semantica y prompts trazables.",
                "DeepSeek-R1 razonara sobre fragmentos recuperados desde los libros.",
                "Qwen3 Embedding creara vectores para recuperar conocimiento en ingles y responder en espanol.",
            ],
            machine_learning_strategy_es=[
                "Generar embeddings para cada registro de knowledge_chunks.",
                "Guardar vectores localmente para busqueda por similitud.",
                "Construir contexto RAG antes de cada respuesta del agente.",
                "Registrar fuentes, fragmentos y nivel de confianza para supervision humana.",
            ],
            install_commands=[
                "scripts\\install-ollama.cmd",
                "scripts\\start-ollama.cmd",
                "scripts\\pull-local-llm-models.cmd",
            ],
            next_actions_es=[
                "Iniciar Ollama localmente.",
                f"Descargar {settings.ollama_reasoning_model}.",
                f"Descargar {settings.ollama_embedding_model}.",
                "Implementar indice vectorial sobre knowledge_chunks.",
                "Conectar el agente BPM al razonador local con citas obligatorias.",
            ],
        )

    def _list_ollama_models(self) -> list[str]:
        try:
            response = httpx.get(f"{settings.ollama_base_url}/api/tags", timeout=2.5)
            response.raise_for_status()
            payload = response.json()
        except (httpx.HTTPError, ValueError):
            return []

        models = payload.get("models", [])
        if not isinstance(models, list):
            return []

        names: list[str] = []
        for model in models:
            if isinstance(model, dict) and isinstance(model.get("name"), str):
                names.append(model["name"])
        return sorted(names)

    def _ollama_is_available(self) -> bool:
        try:
            response = httpx.get(f"{settings.ollama_base_url}/api/tags", timeout=2.5)
        except httpx.HTTPError:
            return False
        return response.status_code < 500

    @staticmethod
    def _has_model(
        pulled_models: list[str],
        configured_model: str,
    ) -> bool:
        if ":" in configured_model:
            return configured_model in pulled_models

        pulled_model_names = {model.split(":", maxsplit=1)[0] for model in pulled_models}
        return configured_model in pulled_model_names
