from fastapi.testclient import TestClient

from app.db.session import reset_db
from app.main import create_app


def _create_case(client: TestClient) -> str:
    response = client.post(
        "/api/process-cases",
        json={
            "name": "Gestion de reclamos",
            "area": "Servicio",
            "objective": "Simular to-be",
        },
    )
    assert response.status_code == 201
    return response.json()["id"]


def _add_element(client: TestClient, case_id: str, element_type: str, name: str) -> None:
    response = client.post(
        f"/api/process-cases/{case_id}/discovery/as-is-elements",
        json={
            "element_type": element_type,
            "name": name,
            "description": name,
            "source_excerpt": name,
            "confidence_level": "high",
        },
    )
    assert response.status_code == 201


def test_simulation_generates_scenarios_and_comparison() -> None:
    reset_db()
    client = TestClient(create_app())
    case_id = _create_case(client)
    _add_element(client, case_id, "metric", "20 dias de ciclo")
    _add_element(client, case_id, "pain_point", "Demora por aprobacion manual")
    _add_element(client, case_id, "activity", "Seguimiento por correo y Excel")

    response = client.get(f"/api/process-cases/{case_id}/simulation/scenarios")

    assert response.status_code == 200
    simulation = response.json()
    assert simulation["comparison"]["baseline_cycle_time_hours"] == 160
    assert simulation["comparison"]["cycle_time_reduction_percent"] > 0
    assert len(simulation["scenarios"]) >= 2
    assert simulation["sensitivity"]


def test_simulation_report_persists_artifact() -> None:
    reset_db()
    client = TestClient(create_app())
    case_id = _create_case(client)
    _add_element(client, case_id, "metric", "10 horas de espera")
    _add_element(client, case_id, "pain_point", "Cola de aprobacion")

    response = client.post(
        f"/api/process-cases/{case_id}/simulation/report",
        json={
            "title": "Simulacion inicial",
            "author": "Agente Simulador",
            "persist": True,
        },
    )

    assert response.status_code == 200
    artifacts_response = client.get(f"/api/process-cases/{case_id}/repository/artifacts")
    assert artifacts_response.status_code == 200
    artifacts = artifacts_response.json()
    assert artifacts[0]["artifact_type"] == "simulation_result"


def test_simulation_unknown_case_returns_404() -> None:
    reset_db()
    client = TestClient(create_app())

    response = client.get("/api/process-cases/00000000-0000-0000-0000-000000000000/simulation/scenarios")

    assert response.status_code == 404
