from fastapi.testclient import TestClient

from app.db.session import reset_db
from app.main import create_app


def _create_case(client: TestClient) -> str:
    response = client.post(
        "/api/process-cases",
        json={
            "name": "Alta de proveedores",
            "area": "Compras",
            "objective": "Generar BPMN as-is",
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
            "confidence_level": "high",
        },
    )
    assert response.status_code == 201


def test_bpmn_preview_generates_valid_basic_xml() -> None:
    reset_db()
    client = TestClient(create_app())
    case_id = _create_case(client)
    _add_element(client, case_id, "activity", "Recibir solicitud")
    _add_element(client, case_id, "business_rule", "Si proveedor no tiene RUC se devuelve")
    _add_element(client, case_id, "activity", "Registrar proveedor en SAP")
    _add_element(client, case_id, "exception", "Falta RUC")

    response = client.get(f"/api/process-cases/{case_id}/bpmn/as-is/preview")

    assert response.status_code == 200
    draft = response.json()
    assert draft["case_id"] == case_id
    assert draft["source_element_count"] == 4
    assert draft["task_count"] == 2
    assert draft["gateway_count"] == 1
    assert draft["is_valid"] is True
    assert "<bpmn:process" in draft["bpmn_xml"]
    assert "Recibir solicitud" in draft["bpmn_xml"]


def test_bpmn_generate_persists_artifact_version() -> None:
    reset_db()
    client = TestClient(create_app())
    case_id = _create_case(client)
    _add_element(client, case_id, "activity", "Validar solicitud")

    response = client.post(
        f"/api/process-cases/{case_id}/bpmn/as-is/generate",
        json={
            "title": "BPMN as-is inicial",
            "author": "Agente Modelador BPMN",
            "persist": True,
        },
    )

    assert response.status_code == 200
    draft = response.json()
    assert draft["artifact_id"] is not None
    assert draft["artifact_version_id"] is not None

    artifacts_response = client.get(f"/api/process-cases/{case_id}/repository/artifacts")
    assert artifacts_response.status_code == 200
    artifacts = artifacts_response.json()
    assert artifacts[0]["artifact_type"] == "bpmn_xml_as_is"
    assert artifacts[0]["versions"][0]["status"] == "draft"


def test_bpmn_validation_reports_parse_error() -> None:
    reset_db()
    client = TestClient(create_app())
    case_id = _create_case(client)

    response = client.post(
        f"/api/process-cases/{case_id}/bpmn/validate",
        json={"bpmn_xml": "<bpmn:definitions><bpmn:process>"},
    )

    assert response.status_code == 200
    validation = response.json()
    assert validation["is_valid"] is False
    assert validation["issues"][0]["code"] == "xml_parse_error"
