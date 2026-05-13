from fastapi.testclient import TestClient

from app.main import app


def test_local_llm_profile_is_available_without_running_model() -> None:
    client = TestClient(app)

    response = client.get("/api/local-llm/profile")

    assert response.status_code == 200
    profile = response.json()
    assert profile["provider"] == "ollama"
    assert profile["runtime"] == "Ollama"
    assert profile["reasoning_model"] == "deepseek-r1:1.5b"
    assert profile["embedding_model"] == "qwen3-embedding:0.6b"
    assert any(model["role"] == "reasoning" for model in profile["recommended_models"])
    assert any(model["role"] == "embedding" for model in profile["recommended_models"])
    assert any("knowledge_chunks" in action for action in profile["machine_learning_strategy_es"])
