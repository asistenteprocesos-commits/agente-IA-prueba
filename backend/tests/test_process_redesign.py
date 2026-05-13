from fastapi.testclient import TestClient

from app.db.session import reset_db
from app.main import create_app


def _create_case(client: TestClient) -> str:
    response = client.post(
        "/api/process-cases",
        json={
            "name": "Alta de proveedores",
            "area": "Compras",
            "objective": "Redisenar to-be",
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


def test_redesign_generates_to_be_alternatives_from_analysis() -> None:
    reset_db()
    client = TestClient(create_app())
    case_id = _create_case(client)
    _add_element(client, case_id, "pain_point", "Demora de 20 dias por aprobacion manual")
    _add_element(client, case_id, "exception", "Falta documento y se devuelve")
    _add_element(client, case_id, "activity", "Seguimiento por correo y Excel")

    response = client.get(f"/api/process-cases/{case_id}/redesign/to-be-options")

    assert response.status_code == 200
    redesign = response.json()
    option_types = {option["option_type"] for option in redesign["alternatives"]}
    assert "quick_win" in option_types
    assert "structural" in option_types
    assert "automation" in option_types
    assert redesign["comparison"]["recommended_option_title_es"]
    assert redesign["next_actions_es"]


def test_redesign_report_persists_to_be_artifact() -> None:
    reset_db()
    client = TestClient(create_app())
    case_id = _create_case(client)
    _add_element(client, case_id, "pain_point", "Reproceso por datos incompletos")

    response = client.post(
        f"/api/process-cases/{case_id}/redesign/report",
        json={
            "title": "Propuesta to-be inicial",
            "author": "Agente Redisenador",
            "persist": True,
        },
    )

    assert response.status_code == 200
    artifacts_response = client.get(f"/api/process-cases/{case_id}/repository/artifacts")
    assert artifacts_response.status_code == 200
    artifacts = artifacts_response.json()
    assert artifacts[0]["artifact_type"] == "process_narrative_to_be"


def test_redesign_unknown_case_returns_404() -> None:
    reset_db()
    client = TestClient(create_app())

    response = client.get("/api/process-cases/00000000-0000-0000-0000-000000000000/redesign/to-be-options")

    assert response.status_code == 404
