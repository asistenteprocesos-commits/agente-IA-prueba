from fastapi.testclient import TestClient

from app.db.session import reset_db
from app.main import create_app


def test_repository_is_created_with_process_case() -> None:
    reset_db()
    client = TestClient(create_app())

    created_case = client.post(
        "/api/process-cases",
        json={"name": "Gestion de reclamos", "area": "Atencion"},
    ).json()

    response = client.get(f"/api/process-cases/{created_case['id']}/repository")

    assert response.status_code == 200
    repository = response.json()
    assert repository["case_id"] == created_case["id"]
    assert repository["artifact_count"] == 0


def test_repository_accepts_first_artifact_version() -> None:
    reset_db()
    client = TestClient(create_app())

    created_case = client.post(
        "/api/process-cases",
        json={"name": "Alta de proveedores"},
    ).json()

    response = client.post(
        f"/api/process-cases/{created_case['id']}/repository/artifacts",
        json={
            "artifact_type": "process_narrative_as_is",
            "title": "Narrativa as-is inicial",
            "description": "Primer borrador validable",
            "content": "El area solicita el alta, Compras valida documentos y Legal aprueba.",
            "change_summary": "Version inicial creada desde entrevista.",
            "author": "Especialista BPM",
        },
    )

    assert response.status_code == 201
    artifact = response.json()
    assert artifact["title"] == "Narrativa as-is inicial"
    assert artifact["versions"][0]["version"] == "0.1.0"
    assert artifact["versions"][0]["status"] == "draft"

    list_response = client.get(f"/api/process-cases/{created_case['id']}/repository/artifacts")

    assert list_response.status_code == 200
    assert len(list_response.json()) == 1


def test_artifact_version_can_be_reviewed_and_commented() -> None:
    reset_db()
    client = TestClient(create_app())

    created_case = client.post(
        "/api/process-cases",
        json={"name": "Cierre contable"},
    ).json()
    artifact = client.post(
        f"/api/process-cases/{created_case['id']}/repository/artifacts",
        json={
            "artifact_type": "process_narrative_as_is",
            "title": "Narrativa inicial",
            "content": "Contabilidad consolida, revisa y cierra.",
        },
    ).json()
    version_id = artifact["versions"][0]["id"]

    submit_response = client.post(
        f"/api/process-cases/{created_case['id']}/repository/artifact-versions/{version_id}/decisions",
        json={
            "action": "submit_for_review",
            "reviewer": "Especialista BPM",
            "comment": "Listo para revision del area.",
        },
    )
    approve_response = client.post(
        f"/api/process-cases/{created_case['id']}/repository/artifact-versions/{version_id}/decisions",
        json={
            "action": "approve",
            "reviewer": "Lider de area",
            "comment": "Aprobado para linea base as-is.",
        },
    )
    comment_response = client.post(
        f"/api/process-cases/{created_case['id']}/repository/artifact-versions/{version_id}/comments",
        json={
            "author": "Auditor de proceso",
            "comment": "Mantener evidencia de aprobacion en el repositorio.",
        },
    )

    assert submit_response.status_code == 201
    assert approve_response.status_code == 201
    assert approve_response.json()["new_status"] == "approved"
    assert comment_response.status_code == 201

    history_response = client.get(
        f"/api/process-cases/{created_case['id']}/repository/artifact-versions/{version_id}/history"
    )

    assert history_response.status_code == 200
    history = history_response.json()
    assert history["version"]["status"] == "approved"
    assert len(history["decisions"]) == 2
    assert len(history["comments"]) == 1


def test_invalid_version_transition_returns_409() -> None:
    reset_db()
    client = TestClient(create_app())

    created_case = client.post(
        "/api/process-cases",
        json={"name": "Atencion de tickets"},
    ).json()
    artifact = client.post(
        f"/api/process-cases/{created_case['id']}/repository/artifacts",
        json={
            "artifact_type": "process_narrative_as_is",
            "title": "Narrativa inicial",
            "content": "Soporte recibe, clasifica y resuelve tickets.",
        },
    ).json()
    version_id = artifact["versions"][0]["id"]

    response = client.post(
        f"/api/process-cases/{created_case['id']}/repository/artifact-versions/{version_id}/decisions",
        json={
            "action": "approve",
            "reviewer": "Lider de soporte",
            "comment": "Intento de aprobacion directa.",
        },
    )

    assert response.status_code == 409


def test_new_version_can_be_created_without_mutating_approved_version() -> None:
    reset_db()
    client = TestClient(create_app())

    created_case = client.post(
        "/api/process-cases",
        json={"name": "Pago a proveedores"},
    ).json()
    artifact = client.post(
        f"/api/process-cases/{created_case['id']}/repository/artifacts",
        json={
            "artifact_type": "process_narrative_as_is",
            "title": "Narrativa inicial",
            "content": "Tesoreria revisa y paga.",
        },
    ).json()
    artifact_id = artifact["id"]
    version_id = artifact["versions"][0]["id"]

    client.post(
        f"/api/process-cases/{created_case['id']}/repository/artifact-versions/{version_id}/decisions",
        json={"action": "submit_for_review", "reviewer": "Especialista BPM"},
    )
    client.post(
        f"/api/process-cases/{created_case['id']}/repository/artifact-versions/{version_id}/decisions",
        json={"action": "approve", "reviewer": "Lider financiero"},
    )

    new_version_response = client.post(
        f"/api/process-cases/{created_case['id']}/repository/artifacts/{artifact_id}/versions",
        json={
            "version": "0.2.0",
            "content": "Tesoreria revisa, programa lote y paga.",
            "change_summary": "Se agrega programacion por lote.",
            "author": "Especialista BPM",
        },
    )

    assert new_version_response.status_code == 201
    assert new_version_response.json()["version"] == "0.2.0"
    assert new_version_response.json()["status"] == "draft"

    artifacts = client.get(f"/api/process-cases/{created_case['id']}/repository/artifacts").json()

    assert len(artifacts[0]["versions"]) == 2
    assert artifacts[0]["versions"][0]["version"] == "0.2.0"
    assert artifacts[0]["versions"][1]["status"] == "approved"


def test_artifact_versions_can_be_compared() -> None:
    reset_db()
    client = TestClient(create_app())

    created_case = client.post(
        "/api/process-cases",
        json={"name": "Revision de facturas"},
    ).json()
    artifact = client.post(
        f"/api/process-cases/{created_case['id']}/repository/artifacts",
        json={
            "artifact_type": "process_narrative_as_is",
            "title": "Narrativa inicial",
            "content": "Compras recibe la factura.\nFinanzas revisa.",
        },
    ).json()
    artifact_id = artifact["id"]
    base_version_id = artifact["versions"][0]["id"]
    target_version = client.post(
        f"/api/process-cases/{created_case['id']}/repository/artifacts/{artifact_id}/versions",
        json={
            "version": "0.2.0",
            "content": "Compras recibe la factura.\nFinanzas valida impuestos.\nTesoreria programa pago.",
            "change_summary": "Se agregan impuestos y programacion de pago.",
        },
    ).json()

    response = client.get(
        f"/api/process-cases/{created_case['id']}/repository/artifact-versions/"
        f"{base_version_id}/diff/{target_version['id']}"
    )

    assert response.status_code == 200
    diff = response.json()
    assert diff["added_lines"] == 2
    assert diff["removed_lines"] == 1
    assert any("Tesoreria programa pago" in line for line in diff["diff"])


def test_artifact_version_accepts_evidence_and_quality_score() -> None:
    reset_db()
    client = TestClient(create_app())

    created_case = client.post(
        "/api/process-cases",
        json={"name": "Alta de clientes"},
    ).json()
    artifact = client.post(
        f"/api/process-cases/{created_case['id']}/repository/artifacts",
        json={
            "artifact_type": "process_narrative_as_is",
            "title": "Narrativa as-is",
            "content": (
                "El area comercial registra la solicitud desde el formulario inicial, "
                "luego Riesgos revisa la informacion y aprueba el alta del cliente."
            ),
        },
    ).json()
    version_id = artifact["versions"][0]["id"]

    evidence_response = client.post(
        f"/api/process-cases/{created_case['id']}/repository/artifact-versions/{version_id}/evidence",
        json={
            "evidence_type": "interview",
            "source_title": "Entrevista con Comercial",
            "excerpt": "Comercial registra la solicitud y Riesgos revisa la informacion.",
            "activity_ref": "Registrar solicitud",
            "notes": "Validado en levantamiento inicial.",
        },
    )
    list_response = client.get(
        f"/api/process-cases/{created_case['id']}/repository/artifact-versions/{version_id}/evidence"
    )
    quality_response = client.get(
        f"/api/process-cases/{created_case['id']}/repository/artifact-versions/{version_id}/quality"
    )

    assert evidence_response.status_code == 201
    assert list_response.status_code == 200
    assert len(list_response.json()) == 1
    assert quality_response.status_code == 200
    assert quality_response.json()["score"] == 100
