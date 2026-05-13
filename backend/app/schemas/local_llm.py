from pydantic import BaseModel


class LocalLLMModelResponse(BaseModel):
    role: str
    model: str
    purpose_es: str
    required: bool
    installed: bool


class LocalLLMProfileResponse(BaseModel):
    provider: str
    runtime: str
    base_url: str
    runtime_installed: bool
    server_available: bool
    reasoning_model: str
    embedding_model: str
    pulled_models: list[str]
    recommended_models: list[LocalLLMModelResponse]
    learning_strategy_es: list[str]
    machine_learning_strategy_es: list[str]
    install_commands: list[str]
    next_actions_es: list[str]
