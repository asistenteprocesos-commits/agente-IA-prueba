from fastapi.testclient import TestClient

from app.db.session import reset_db
from app.main import app


def test_ingest_text_document_and_list_chunks() -> None:
    reset_db()
    client = TestClient(app)

    content = (
        "BPMN permite modelar procesos de negocio con eventos, actividades y gateways. "
        "La gestion por procesos exige identificar responsables, entradas, salidas y reglas."
    )

    response = client.post(
        "/api/knowledge/documents",
        data={
            "title": "Manual base BPM",
            "author": "Equipo BPM",
            "source_type": "book",
            "subject_area": "BPMN",
            "language": "es",
        },
        files={"file": ("manual-bpm.txt", content.encode("utf-8"), "text/plain")},
    )

    assert response.status_code == 201
    document = response.json()
    assert document["title"] == "Manual base BPM"
    assert document["status"] == "processed"
    assert document["chunk_count"] >= 1
    assert document["text_char_count"] == len(content)

    list_response = client.get("/api/knowledge/documents")
    assert list_response.status_code == 200
    assert list_response.json()[0]["id"] == document["id"]

    chunks_response = client.get(f"/api/knowledge/documents/{document['id']}/chunks")
    assert chunks_response.status_code == 200
    chunks = chunks_response.json()
    assert chunks[0]["chunk_index"] == 1
    assert "BPMN permite modelar procesos" in chunks[0]["content"]


def test_bulk_ingest_books() -> None:
    reset_db()
    client = TestClient(app)

    response = client.post(
        "/api/knowledge/documents/bulk",
        data={
            "author": "Biblioteca BPM",
            "source_type": "book",
            "subject_area": "Gestion de procesos",
            "language": "es",
        },
        files=[
            (
                "files",
                (
                    "libro-bpm.txt",
                    b"La gestion por procesos permite analizar actividades, roles y controles.",
                    "text/plain",
                ),
            ),
            (
                "files",
                (
                    "libro-bpmn.txt",
                    b"BPMN usa eventos, tareas, gateways y flujos de secuencia.",
                    "text/plain",
                ),
            ),
        ],
    )

    assert response.status_code == 201
    documents = response.json()
    assert len(documents) == 2
    assert {document["status"] for document in documents} == {"processed"}
    assert {document["source_type"] for document in documents} == {"book"}

    list_response = client.get("/api/knowledge/documents")
    assert list_response.status_code == 200
    assert len(list_response.json()) == 2


def test_library_analysis_creates_spanish_insights_and_methodology() -> None:
    reset_db()
    client = TestClient(app)

    response = client.post(
        "/api/knowledge/documents/bulk",
        data={
            "author": "English BPM Library",
            "source_type": "book",
            "subject_area": "BPM and BPMN",
            "language": "en",
        },
        files=[
            (
                "files",
                (
                    "technical-bpmn.txt",
                    (
                        "BPMN uses events, tasks, gateways, pools, lanes and sequence flow "
                        "to represent an end-to-end business process."
                    ).encode("utf-8"),
                    "text/plain",
                ),
            ),
            (
                "files",
                (
                    "process-mining.txt",
                    (
                        "Process mining analyzes event log data with case id, activity, "
                        "timestamp, variants, conformance and bottleneck analysis."
                    ).encode("utf-8"),
                    "text/plain",
                ),
            ),
        ],
    )
    assert response.status_code == 201

    analysis_response = client.post("/api/knowledge/learning/analyze")
    assert analysis_response.status_code == 201
    analysis = analysis_response.json()
    assert analysis["analyzed_documents"] == 2
    assert analysis["created_insights"] >= 2
    assert analysis["total_insights"] >= analysis["created_insights"]

    insights_response = client.get("/api/knowledge/insights")
    assert insights_response.status_code == 200
    insights = insights_response.json()
    topics = {insight["topic"] for insight in insights}
    assert "Modelado BPMN" in topics
    assert "Process mining" in topics
    assert all(insight["summary_es"] for insight in insights)
    assert all(insight["source_language"] == "en" for insight in insights)

    methodology_response = client.get("/api/knowledge/case-methodology")
    assert methodology_response.status_code == 200
    methodology = methodology_response.json()
    assert methodology["language"] == "es"
    assert methodology["source_insight_count"] >= 2
    assert len(methodology["phases"]) == 8
    assert methodology["phases"][0]["phase"].startswith("1.")


def test_agent_training_profile_exposes_documentary_distillation_pack() -> None:
    reset_db()
    client = TestClient(app)

    response = client.get("/api/knowledge/agent-training-profile")

    assert response.status_code == 200
    profile = response.json()
    assert profile["profile_name"] == "Agente BPM especialista en procesos"
    assert profile["training_mode"] == "documentary_distillation_not_weight_training"
    assert profile["language"] == "es"
    assert profile["methodology_phases"] == 8
    assert profile["dataset_examples"] >= 0
    assert any(artifact["kind"] == "prompt" for artifact in profile["artifacts"])
    assert "embeddings" in profile["next_step"]
