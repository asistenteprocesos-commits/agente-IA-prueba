from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Agente IA Prueba"
    app_version: str = "0.1.0"
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
    database_url: str = "sqlite:///./storage/app.db"
    document_storage_dir: str = "storage/documents"
    agent_training_dir: str = "docs/agent-training"
    obsidian_vault_dir: str = "storage/obsidian-bpm-vault"
    local_llm_provider: str = "ollama"
    ollama_base_url: str = "http://127.0.0.1:11434"
    ollama_reasoning_model: str = "deepseek-r1:1.5b"
    ollama_reasoning_model_upgrade: str = "deepseek-r1:7b"
    ollama_embedding_model: str = "qwen3-embedding:0.6b"
    ollama_embedding_model_upgrade: str = "qwen3-embedding:4b"

    model_config = SettingsConfigDict(
        env_file="backend/.env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
