from fastapi.testclient import TestClient

from app.db.session import reset_db
from app.main import create_app


def _create_case(client: TestClient) -> str:
    response = client.post(
        "/api/process-cases",
        json={
            "name": "Gestion de reclamos",
            "area": "Servicio",
            "objective": "Analizar mejoras",
        },
    )
    assert response.status_code == 201
    return response.json()["id"]


def _add_element(client: TestClient, case_id: str, element_type: str, name: str, description: str | None = None) -> None:
    response = client.post(
        f"/api/process-cases/{case_id}/discovery/as-is-elements",
        json={
            "element_type": element_type,
            "name": name,
            "description": description or name,
            "source_excerpt": description or name,
            "confidence_level": "high",
        },
    )
    assert response.status_code == 201


def test_process_analysis_detects_findings_metrics_risks_and_improvements() -> None:
    reset_db()
    client = TestClient(create_app())
    case_id = _create_case(client)
    _add_element(client, case_id, "activity", "Registrar reclamo por correo manual")
    _add_element(client, case_id, "pain_point", "Demora de 20 dias por cola de aprobacion")
    _add_element(client, case_id, "exception", "Falta documento y se devuelve al cliente")
    _add_element(client, case_id, "metric", "20 dias de ciclo y 35% reproceso")
    _add_element(client, case_id, "control", "Revision manual por supervisor")

    response = client.get(f"/api/process-cases/{case_id}/analysis")

    assert response.status_code == 200
    analysis = response.json()
    assert analysis["analysis_score"] >= 70
    finding_types = {finding["finding_type"] for finding in analysis["findings"]}
    assert "bottleneck" in finding_types
    assert "waste" in finding_types
    assert "automation" in finding_types
    assert any(metric["value"] == 20 for metric in analysis["metrics"])
    assert analysis["risks_controls"][0]["status"] in {"covered", "needs_validation"}
    assert analysis["improvement_candidates"]
    assert analysis["next_actions_es"]


def test_process_analysis_report_persists_improvement_artifact() -> None:
    reset_db()
    client = TestClient(create_app())
    case_id = _create_case(client)
    _add_element(client, case_id, "pain_point", "Espera de 10 horas por aprobacion manual")

    response = client.post(
        f"/api/process-cases/{case_id}/analysis/report",
        json={
            "title": "Analisis inicial de reclamos",
            "author": "Agente Analista",
            "persist": True,
        },
    )

    assert response.status_code == 200
    artifacts_response = client.get(f"/api/process-cases/{case_id}/repository/artifacts")
    assert artifacts_response.status_code == 200
    artifacts = artifacts_response.json()
    assert artifacts[0]["artifact_type"] == "improvement_report"
    assert "Analisis inicial" in artifacts[0]["title"]


def test_process_analysis_unknown_case_returns_404() -> None:
    reset_db()
    client = TestClient(create_app())

    response = client.get("/api/process-cases/00000000-0000-0000-0000-000000000000/analysis")

    assert response.status_code == 404
