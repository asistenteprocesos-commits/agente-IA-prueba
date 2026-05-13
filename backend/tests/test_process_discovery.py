from fastapi.testclient import TestClient

from app.db.session import reset_db
from app.main import create_app


def _create_case(client: TestClient) -> str:
    response = client.post(
        "/api/process-cases",
        json={
            "name": "Alta de proveedores",
            "area": "Compras",
            "objective": "Levantar as-is",
        },
    )
    assert response.status_code == 201
    return response.json()["id"]


def test_stakeholders_and_interviews_can_be_registered() -> None:
    reset_db()
    client = TestClient(create_app())
    case_id = _create_case(client)

    stakeholder_response = client.post(
        f"/api/process-cases/{case_id}/discovery/stakeholders",
        json={
            "name": "Maria Perez",
            "role": "process_owner",
            "area": "Compras",
            "email": "maria@example.com",
            "influence_level": "high",
            "availability": "Martes por la manana",
        },
    )

    assert stakeholder_response.status_code == 201
    stakeholder = stakeholder_response.json()
    assert stakeholder["name"] == "Maria Perez"
    assert stakeholder["role"] == "process_owner"

    interview_response = client.post(
        f"/api/process-cases/{case_id}/discovery/interviews",
        json={
            "stakeholder_id": stakeholder["id"],
            "title": "Entrevista inicial con Compras",
            "interview_type": "discovery",
            "objective": "Entender flujo, reglas y excepciones actuales",
            "questions": "Cual es el inicio?\nQuien aprueba?",
            "notes": "El proceso inicia con una solicitud por correo.",
        },
    )

    assert interview_response.status_code == 201
    interview = interview_response.json()
    assert interview["stakeholder_name"] == "Maria Perez"
    assert interview["status"] == "planned"

    stakeholders_response = client.get(f"/api/process-cases/{case_id}/discovery/stakeholders")
    assert stakeholders_response.status_code == 200
    assert len(stakeholders_response.json()) == 1

    interviews_response = client.get(f"/api/process-cases/{case_id}/discovery/interviews")
    assert interviews_response.status_code == 200
    assert len(interviews_response.json()) == 1

    case_response = client.get(f"/api/process-cases/{case_id}")
    assert case_response.status_code == 200
    assert case_response.json()["status"] == "discovery"


def test_interview_guide_is_generated_for_case() -> None:
    reset_db()
    client = TestClient(create_app())
    case_id = _create_case(client)

    response = client.get(f"/api/process-cases/{case_id}/discovery/interview-guide")

    assert response.status_code == 200
    guide = response.json()
    assert guide["title"] == "Guia de levantamiento as-is - Alta de proveedores"
    assert len(guide["sections"]) == 4
    assert "actividades principales" in guide["sections"][1]["questions"][0]


def test_as_is_elements_can_be_extracted_and_created() -> None:
    reset_db()
    client = TestClient(create_app())
    case_id = _create_case(client)

    interview_response = client.post(
        f"/api/process-cases/{case_id}/discovery/interviews",
        json={
            "title": "Sesion de detalle operativo",
            "interview_type": "discovery",
            "notes": (
                "El proceso inicia cuando Compras recibe solicitud por correo.\n"
                "El analista registra datos en SAP.\n"
                "Si falta RUC se devuelve al solicitante.\n"
                "Existe demora por revision manual."
            ),
        },
    )
    assert interview_response.status_code == 201
    interview_id = interview_response.json()["id"]

    extraction_response = client.post(
        f"/api/process-cases/{case_id}/discovery/interviews/{interview_id}/extract-as-is"
    )

    assert extraction_response.status_code == 201
    extracted = extraction_response.json()
    extracted_types = {element["element_type"] for element in extracted}
    assert "event" in extracted_types
    assert "system" in extracted_types
    assert "exception" in extracted_types
    assert "pain_point" in extracted_types
    assert all(element["created_by"] == "heuristic_extractor" for element in extracted)

    manual_response = client.post(
        f"/api/process-cases/{case_id}/discovery/as-is-elements",
        json={
            "interview_id": interview_id,
            "element_type": "business_rule",
            "name": "Proveedor debe tener RUC activo",
            "description": "La validacion tributaria es obligatoria antes del alta.",
            "confidence_level": "medium",
        },
    )

    assert manual_response.status_code == 201
    assert manual_response.json()["element_type"] == "business_rule"

    list_response = client.get(f"/api/process-cases/{case_id}/discovery/as-is-elements")
    assert list_response.status_code == 200
    assert len(list_response.json()) == len(extracted) + 1

    case_response = client.get(f"/api/process-cases/{case_id}")
    assert case_response.status_code == 200
    assert case_response.json()["status"] == "as_is_drafting"


def test_discovery_assessment_generates_questions_gaps_and_contradictions() -> None:
    reset_db()
    client = TestClient(create_app())
    case_id = _create_case(client)

    stakeholder_response = client.post(
        f"/api/process-cases/{case_id}/discovery/stakeholders",
        json={
            "name": "Ana Responsable",
            "role": "process_owner",
            "area": "Compras",
            "influence_level": "high",
        },
    )
    assert stakeholder_response.status_code == 201
    stakeholder_id = stakeholder_response.json()["id"]

    interview_response = client.post(
        f"/api/process-cases/{case_id}/discovery/interviews",
        json={
            "stakeholder_id": stakeholder_id,
            "title": "Contraste de aprobaciones",
            "interview_type": "discovery",
            "notes": (
                "El proceso inicia cuando llega la solicitud por correo. "
                "Finanzas siempre aprueba las solicitudes. "
                "Otro equipo indica que se aprueba solo si supera 5000. "
                "El analista registra datos en SAP y Excel."
            ),
        },
    )
    assert interview_response.status_code == 201
    interview_id = interview_response.json()["id"]

    client.post(f"/api/process-cases/{case_id}/discovery/interviews/{interview_id}/extract-as-is")

    assessment_response = client.get(f"/api/process-cases/{case_id}/discovery/assessment")

    assert assessment_response.status_code == 200
    assessment = assessment_response.json()
    assert assessment["case_id"] == case_id
    assert assessment["completeness_score"] > 0
    assert assessment["readiness_level"] in {"blocked", "needs_validation", "insufficient", "ready_for_bpmn"}
    assert len(assessment["dimensions"]) == 6
    assert assessment["generated_questions"]
    assert any(gap["code"] == "missing_metric" for gap in assessment["gaps"])
    assert any(contradiction["topic"] == "Regla de aprobacion" for contradiction in assessment["contradictions"])
    assert assessment["next_actions_es"]


def test_discovery_unknown_case_returns_404() -> None:
    reset_db()
    client = TestClient(create_app())

    response = client.get(
        "/api/process-cases/00000000-0000-0000-0000-000000000000/discovery/stakeholders"
    )

    assert response.status_code == 404
