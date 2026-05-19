from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Agente BPMS - Experto en Procesos"
    app_version: str = "1.2.0"
    app_env: str = "local"
    api_prefix: str = "/api"
    frontend_origins: list[str] = Field(
        default_factory=lambda: [
            "http://localhost:5173",
            "http://127.0.0.1:5173",
            "http://localhost:5174",
            "http://127.0.0.1:5174",
            "http://localhost:5175",
            "http://127.0.0.1:5175",
            "http://localhost:5176",
            "http://127.0.0.1:5176",
            "http://localhost:5177",
            "http://127.0.0.1:5177",
            "http://localhost:5178",
            "http://127.0.0.1:5178",
        ]
    )

    # ── Base de datos ──────────────────────────────────────────────────────────
    database_url: str = "sqlite:///./storage/app.db"
    document_storage_dir: str = "storage/documents"
    agent_training_dir: str = "docs/agent-training"
    obsidian_vault_dir: str = "storage/obsidian-bpm-vault"
    vector_store_dir: str = "storage/vector_store"

    # ── Ollama (LLM Local) ────────────────────────────────────────────────────
    local_llm_provider: str = "ollama"
    ollama_base_url: str = "http://127.0.0.1:11434"
    ollama_reasoning_model: str = "deepseek-r1:32b"
    ollama_reasoning_model_upgrade: str = "deepseek-r1:32b"
    ollama_coder_model: str = "deepseek-coder-v2"
    ollama_fast_model: str = "qwen2.5-coder:7b"
    ollama_embedding_model: str = "qwen3-embedding:0.6b"
    ollama_embedding_model_upgrade: str = "qwen3-embedding:4b"

    # ── Gemini (Google AI Studio — gratuito) ──────────────────────────────────
    gemini_api_key: str = ""
    gemini_model: str = "gemini-2.5-pro-latest"
    gemini_flash_model: str = "gemini-2.5-flash-latest"

    # ── Deepseek API (casi gratuito) ──────────────────────────────────────────
    deepseek_api_key: str = ""
    deepseek_model: str = "deepseek-chat"

    # ── Groq (gratuito, rápido) ───────────────────────────────────────────────
    groq_api_key: str = ""
    groq_model: str = "meta-llama/llama-4-scout"

    # ── RAG / Embeddings ──────────────────────────────────────────────────────
    rag_top_k: int = 5
    rag_chunk_size: int = 1200
    rag_chunk_overlap: int = 160

    # ── Chat ──────────────────────────────────────────────────────────────────
    chat_max_history: int = 20
    chat_max_rag_fragments: int = 5

    model_config = SettingsConfigDict(
        env_file="backend/.env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
