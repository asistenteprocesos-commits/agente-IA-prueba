from fastapi.testclient import TestClient

from app.db.session import reset_db
from app.main import create_app


def _create_case(client: TestClient) -> str:
    response = client.post(
        "/api/process-cases",
        json={
            "name": "Gestion de reclamos",
            "area": "Servicio",
            "objective": "Cerrar caso",
            "owner": "Lider BPM",
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


def test_final_report_preview_builds_sections() -> None:
    reset_db()
    client = TestClient(create_app())
    case_id = _create_case(client)
    _add_element(client, case_id, "metric", "20 dias de ciclo")
    _add_element(client, case_id, "pain_point", "Demora por aprobacion manual")

    response = client.get(f"/api/process-cases/{case_id}/deliverables/final-report")

    assert response.status_code == 200
    deliverable = response.json()
    assert "Gestion de reclamos" in deliverable["executive_summary_es"]
    assert len(deliverable["implementation_plan"]) == 4
    assert deliverable["decision_points_es"]


def test_final_report_can_be_persisted() -> None:
    reset_db()
    client = TestClient(create_app())
    case_id = _create_case(client)
    _add_element(client, case_id, "metric", "10 horas de espera")
    _add_element(client, case_id, "pain_point", "Cola manual")

    response = client.post(
        f"/api/process-cases/{case_id}/deliverables/final-report",
        json={
            "title": "Informe final inicial",
            "author": "Agente Redactor",
            "persist": True,
        },
    )

    assert response.status_code == 200
    deliverable = response.json()
    assert deliverable["artifact_id"] is not None
    artifacts_response = client.get(f"/api/process-cases/{case_id}/repository/artifacts")
    assert artifacts_response.status_code == 200
    assert artifacts_response.json()[0]["artifact_type"] == "final_report"


def test_final_report_unknown_case_returns_404() -> None:
    reset_db()
    client = TestClient(create_app())

    response = client.get("/api/process-cases/00000000-0000-0000-0000-000000000000/deliverables/final-report")

    assert response.status_code == 404
