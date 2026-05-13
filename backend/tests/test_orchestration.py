from fastapi.testclient import TestClient

from app.db.session import reset_db
from app.main import create_app


def _create_case(client: TestClient) -> str:
    response = client.post(
        "/api/process-cases",
        json={
            "name": "Aprobacion de proveedores",
            "area": "Compras",
            "objective": "Orquestar ciclo BPM completo",
            "owner": "Especialista BPM",
        },
    )
    assert response.status_code == 201
    return response.json()["id"]


def test_orchestration_state_is_created_with_eight_phases() -> None:
    reset_db()
    client = TestClient(create_app())
    case_id = _create_case(client)

    response = client.get(f"/api/process-cases/{case_id}/orchestration")

    assert response.status_code == 200
    state = response.json()
    assert state["run"]["status"] == "not_started"
    assert state["run"]["current_phase_number"] == 1
    assert len(state["phases"]) == 8
    assert state["phases"][0]["phase_key"] == "preparar_alcance"
    assert state["phases"][0]["requires_human_checkpoint"] is True
    assert state["autonomy_progress_percent"] == 0
    assert state["events"][0]["event_type"] == "run_created"


def test_orchestration_runs_checkpoint_and_advances_to_next_phase() -> None:
    reset_db()
    client = TestClient(create_app())
    case_id = _create_case(client)

    start_response = client.post(f"/api/process-cases/{case_id}/orchestration/start")
    assert start_response.status_code == 200
    started = start_response.json()
    assert started["run"]["status"] == "running"
    assert started["phases"][0]["status"] == "in_progress"

    checkpoint_response = client.post(f"/api/process-cases/{case_id}/orchestration/advance")
    assert checkpoint_response.status_code == 200
    checkpoint_state = checkpoint_response.json()
    assert checkpoint_state["run"]["status"] == "waiting_human"
    assert checkpoint_state["phases"][0]["status"] == "blocked_checkpoint"
    assert checkpoint_state["blockers_es"]

    approve_response = client.post(
        f"/api/process-cases/{case_id}/orchestration/checkpoint",
        json={
            "action": "approve",
            "reviewer": "Supervisor BPM",
            "comment": "Alcance validado con el responsable.",
        },
    )
    assert approve_response.status_code == 200
    approved = approve_response.json()
    assert approved["run"]["status"] == "running"
    assert approved["phases"][0]["checkpoint_status"] == "approved"

    advance_response = client.post(f"/api/process-cases/{case_id}/orchestration/advance")
    assert advance_response.status_code == 200
    advanced = advance_response.json()
    assert advanced["run"]["current_phase_number"] == 2
    assert advanced["phases"][0]["status"] == "completed"
    assert advanced["phases"][1]["status"] == "in_progress"
    assert advanced["autonomy_progress_percent"] == 12

    case_response = client.get(f"/api/process-cases/{case_id}")
    assert case_response.status_code == 200
    assert case_response.json()["status"] == "discovery"


def test_orchestration_rollback_returns_to_previous_phase() -> None:
    reset_db()
    client = TestClient(create_app())
    case_id = _create_case(client)

    client.post(f"/api/process-cases/{case_id}/orchestration/start")
    client.post(f"/api/process-cases/{case_id}/orchestration/advance")
    client.post(
        f"/api/process-cases/{case_id}/orchestration/checkpoint",
        json={"action": "approve", "reviewer": "Supervisor BPM"},
    )
    client.post(f"/api/process-cases/{case_id}/orchestration/advance")

    rollback_response = client.post(f"/api/process-cases/{case_id}/orchestration/rollback")

    assert rollback_response.status_code == 200
    state = rollback_response.json()
    assert state["run"]["current_phase_number"] == 1
    assert state["run"]["status"] == "running"
    assert state["phases"][0]["status"] == "in_progress"
    assert state["phases"][0]["checkpoint_status"] == "pending"
    assert any(event["event_type"] == "rollback" for event in state["events"])


def test_orchestration_unknown_case_returns_404() -> None:
    reset_db()
    client = TestClient(create_app())

    response = client.get("/api/process-cases/00000000-0000-0000-0000-000000000000/orchestration")

    assert response.status_code == 404
