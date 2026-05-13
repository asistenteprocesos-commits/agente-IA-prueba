import json
import re
from pathlib import Path
from uuid import UUID, uuid4

from docx import Document as DocxDocument
from fastapi import UploadFile
from pypdf import PdfReader
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.core.config import settings
from app.models.knowledge import KnowledgeChunkModel, KnowledgeDocumentModel, KnowledgeInsightModel
from app.schemas.knowledge import (
    AgentTrainingArtifactResponse,
    AgentTrainingProfileResponse,
    CaseMethodologyPhaseResponse,
    CaseMethodologyResponse,
    ConfidenceLevel,
    KnowledgeChunkResponse,
    KnowledgeDocumentResponse,
    KnowledgeDocumentStatus,
    KnowledgeInsightResponse,
    KnowledgeInsightType,
    KnowledgeLearningRunResponse,
    KnowledgeSourceType,
)

PROJECT_ROOT = Path(__file__).resolve().parents[3]
TEXT_SUFFIXES = {".txt", ".md", ".csv", ".json", ".xml", ".bpmn"}
DEFAULT_CHUNK_SIZE = 1200
DEFAULT_CHUNK_OVERLAP = 160

TOPIC_RULES = [
    {
        "topic": "BPM y gestion por procesos",
        "insight_type": KnowledgeInsightType.method.value,
        "keywords": (
            "business process",
            "process management",
            "process owner",
            "process architecture",
            "workflow",
            "value stream",
            "end-to-end process",
            "sipoc",
            "gestion por procesos",
        ),
    },
    {
        "topic": "Modelado BPMN",
        "insight_type": KnowledgeInsightType.bpmn_modeling.value,
        "keywords": (
            "bpmn",
            "business process model and notation",
            "gateway",
            "event",
            "task",
            "pool",
            "lane",
            "sequence flow",
            "message flow",
        ),
    },
    {
        "topic": "Process mining",
        "insight_type": KnowledgeInsightType.process_mining.value,
        "keywords": (
            "process mining",
            "event log",
            "case id",
            "timestamp",
            "activity column",
            "conformance",
            "variant",
            "bottleneck",
        ),
    },
    {
        "topic": "Transformacion digital",
        "insight_type": KnowledgeInsightType.digital_transformation.value,
        "keywords": (
            "digital transformation",
            "automation",
            "rpa",
            "artificial intelligence",
            "data-driven",
            "integration",
            "platform",
            "change management",
        ),
    },
    {
        "topic": "Riesgos y controles",
        "insight_type": KnowledgeInsightType.risk_control.value,
        "keywords": (
            "risk",
            "control",
            "compliance",
            "audit",
            "segregation of duties",
            "governance",
            "policy",
            "approval",
        ),
    },
    {
        "topic": "Metricas y simulacion",
        "insight_type": KnowledgeInsightType.metric.value,
        "keywords": (
            "kpi",
            "metric",
            "cycle time",
            "lead time",
            "throughput",
            "queue",
            "capacity",
            "simulation",
            "sla",
        ),
    },
    {
        "topic": "Mejora continua",
        "insight_type": KnowledgeInsightType.framework.value,
        "keywords": (
            "lean",
            "six sigma",
            "continuous improvement",
            "waste",
            "kaizen",
            "root cause",
            "value-added",
            "standardization",
        ),
    },
    {
        "topic": "Gestion de casos de proceso",
        "insight_type": KnowledgeInsightType.case_management.value,
        "keywords": (
            "stakeholder",
            "interview",
            "workshop",
            "requirements",
            "current state",
            "future state",
            "as-is",
            "to-be",
        ),
    },
]


class KnowledgeService:
    def __init__(self, db: Session) -> None:
        self.db = db

    async def ingest_document(
        self,
        file: UploadFile,
        title: str | None,
        author: str | None,
        source_type: KnowledgeSourceType,
        subject_area: str | None,
        language: str,
        case_id: UUID | None,
    ) -> KnowledgeDocumentResponse:
        document_id = str(uuid4())
        original_filename = Path(file.filename or "documento.txt").name
        filename = self._safe_filename(original_filename)
        storage_dir = Path(settings.document_storage_dir) / document_id
        storage_dir.mkdir(parents=True, exist_ok=True)
        file_path = storage_dir / filename

        raw_content = await file.read()
        file_path.write_bytes(raw_content)

        document = KnowledgeDocumentModel(
            id=document_id,
            title=self._clean_text(title) or Path(filename).stem,
            author=self._clean_text(author),
            source_type=source_type.value,
            subject_area=self._clean_text(subject_area),
            language=self._clean_text(language) or "es",
            case_id=str(case_id) if case_id else None,
            filename=filename,
            mime_type=file.content_type,
            file_path=str(file_path),
            status=KnowledgeDocumentStatus.uploaded.value,
        )

        try:
            extracted_text = self._extract_text(file_path, raw_content)
            chunks = self._chunk_text(extracted_text)
            document.status = (
                KnowledgeDocumentStatus.processed.value
                if chunks
                else KnowledgeDocumentStatus.failed.value
            )
            document.error_message = None if chunks else "No se encontro texto extraible"
            document.text_char_count = len(extracted_text)
            document.chunk_count = len(chunks)
            document.chunks = [
                KnowledgeChunkModel(
                    id=str(uuid4()),
                    document_id=document.id,
                    chunk_index=index,
                    content=chunk["content"],
                    char_start=chunk["char_start"],
                    char_end=chunk["char_end"],
                )
                for index, chunk in enumerate(chunks, start=1)
            ]
        except Exception as error:
            document.status = KnowledgeDocumentStatus.failed.value
            document.error_message = str(error)
            document.text_char_count = 0
            document.chunk_count = 0

        self.db.add(document)
        self.db.commit()
        self.db.refresh(document)
        return self._document_to_response(document)

    def list_documents(self, case_id: UUID | None = None) -> list[KnowledgeDocumentResponse]:
        statement = (
            select(KnowledgeDocumentModel)
            .options(selectinload(KnowledgeDocumentModel.chunks))
            .order_by(KnowledgeDocumentModel.created_at.desc())
        )
        if case_id is not None:
            statement = statement.where(KnowledgeDocumentModel.case_id == str(case_id))

        documents = self.db.scalars(statement).all()
        return [self._document_to_response(document) for document in documents]

    def list_chunks(self, document_id: UUID) -> list[KnowledgeChunkResponse] | None:
        document = self.db.get(KnowledgeDocumentModel, str(document_id))
        if document is None:
            return None

        statement = (
            select(KnowledgeChunkModel)
            .where(KnowledgeChunkModel.document_id == str(document_id))
            .order_by(KnowledgeChunkModel.chunk_index)
        )
        chunks = self.db.scalars(statement).all()
        return [self._chunk_to_response(chunk) for chunk in chunks]

    def analyze_document(self, document_id: UUID) -> KnowledgeLearningRunResponse | None:
        statement = (
            select(KnowledgeDocumentModel)
            .where(KnowledgeDocumentModel.id == str(document_id))
            .options(selectinload(KnowledgeDocumentModel.chunks))
        )
        document = self.db.scalars(statement).first()
        if document is None:
            return None

        created = self._create_insights_for_documents([document])
        return KnowledgeLearningRunResponse(
            analyzed_documents=1,
            created_insights=created,
            total_insights=self._count_insights(),
        )

    def analyze_library(self) -> KnowledgeLearningRunResponse:
        statement = (
            select(KnowledgeDocumentModel)
            .where(KnowledgeDocumentModel.status == KnowledgeDocumentStatus.processed.value)
            .options(selectinload(KnowledgeDocumentModel.chunks))
            .order_by(KnowledgeDocumentModel.created_at.desc())
        )
        documents = self.db.scalars(statement).all()
        created = self._create_insights_for_documents(documents)
        return KnowledgeLearningRunResponse(
            analyzed_documents=len(documents),
            created_insights=created,
            total_insights=self._count_insights(),
        )

    def list_insights(
        self,
        topic: str | None = None,
        limit: int = 100,
    ) -> list[KnowledgeInsightResponse]:
        statement = select(KnowledgeInsightModel).order_by(KnowledgeInsightModel.created_at.desc())
        if topic:
            statement = statement.where(KnowledgeInsightModel.topic == topic)
        insights = self.db.scalars(statement.limit(limit)).all()
        return [self._insight_to_response(insight) for insight in insights]

    def load_agent_training_profile(self) -> AgentTrainingProfileResponse:
        training_dir = self._project_path(settings.agent_training_dir)
        vault_dir = self._project_path(settings.obsidian_vault_dir)
        canvas_path = vault_dir / "BPM_Knowledge_Graph.canvas"
        manifest = self._load_training_manifest(training_dir)
        books = manifest.get("books", [])
        dataset_path = training_dir / "datasets" / "bpm_instruction_dataset.jsonl"
        insight_count = manifest.get("insights")

        artifacts = [
            self._artifact_response("Prompt maestro", "prompt", training_dir / "prompt-maestro-agente-bpm.md"),
            self._artifact_response("Playbook operativo", "playbook", training_dir / "playbook-operativo-bpm.md"),
            self._artifact_response("Rubrica de calidad", "rubric", training_dir / "rubrica-calidad-bpm.md"),
            self._artifact_response("Glosario operativo", "glossary", training_dir / "glosario-operativo.md"),
            self._artifact_response("Dataset JSONL", "dataset", dataset_path),
            self._artifact_response("Manifest de destilacion", "manifest", training_dir / "knowledge-distillation-manifest.json"),
            self._artifact_response("Vault Obsidian", "obsidian_vault", vault_dir),
            self._artifact_response("Canvas visual Obsidian", "obsidian_canvas", canvas_path),
        ]

        return AgentTrainingProfileResponse(
            profile_name="Agente BPM especialista en procesos",
            training_mode=str(manifest.get("mode", "documentary_distillation_not_weight_training")),
            language="es",
            books_processed=len(books),
            pages_processed=sum(int(book.get("pages", 0)) for book in books if isinstance(book, dict)),
            extracted_characters=sum(
                int(book.get("text_chars", 0)) for book in books if isinstance(book, dict)
            ),
            insights=int(insight_count) if insight_count is not None else self._count_insights(),
            methodology_phases=int(manifest.get("methodology_phases", 8)),
            dataset_examples=self._count_dataset_examples(dataset_path),
            graph_is_visual=canvas_path.exists(),
            obsidian_vault_path=str(vault_dir),
            obsidian_canvas_path=str(canvas_path),
            artifacts=artifacts,
            limitations=[
                str(item)
                for item in manifest.get(
                    "limitations",
                    [
                        "No modifica pesos internos del LLM.",
                        "Requiere recuperacion semantica para responder con evidencia.",
                    ],
                )
            ],
            next_step=(
                "Implementar embeddings locales y busqueda semantica para que el agente "
                "recupere fragmentos de los libros antes de responder."
            ),
        )

    def build_case_methodology(self) -> CaseMethodologyResponse:
        insights = self.db.scalars(select(KnowledgeInsightModel)).all()
        topic_counts: dict[str, int] = {}
        for insight in insights:
            topic_counts[insight.topic] = topic_counts.get(insight.topic, 0) + 1

        phases = [
            self._methodology_phase(
                phase="1. Preparar alcance y conocimiento",
                objective="Definir objetivo, alcance, fuentes tecnicas, restricciones y criterios de exito del caso.",
                actions=[
                    "Cargar libros, normas y documentos internos relacionados.",
                    "Analizar la biblioteca para extraer conceptos tecnicos en espanol.",
                    "Definir proceso, area, dueno, alcance y nivel de profundidad requerido.",
                ],
                outputs=[
                    "Caso de proceso creado",
                    "Biblioteca tecnica procesada",
                    "Criterios de supervision humana",
                ],
                checks=[
                    "Las fuentes clave estan procesadas.",
                    "El alcance tiene inicio, fin y areas involucradas.",
                    "La supervision humana esta definida.",
                ],
                related_topics=["BPM y gestion por procesos", "Gestion de casos de proceso"],
                topic_counts=topic_counts,
            ),
            self._methodology_phase(
                phase="2. Levantar as-is",
                objective="Recolectar informacion del proceso actual con entrevistas, talleres y evidencia documental.",
                actions=[
                    "Registrar stakeholders por rol e influencia.",
                    "Usar guias de entrevista y capturar notas completas.",
                    "Vincular evidencias y documentos a cada hallazgo relevante.",
                ],
                outputs=[
                    "Stakeholders registrados",
                    "Entrevistas documentadas",
                    "Evidencias iniciales trazables",
                ],
                checks=[
                    "Cada actividad critica tiene fuente.",
                    "Las excepciones y decisiones estan documentadas.",
                    "Se identifican roles, sistemas, entradas y salidas.",
                ],
                related_topics=["Gestion de casos de proceso", "BPM y gestion por procesos"],
                topic_counts=topic_counts,
            ),
            self._methodology_phase(
                phase="3. Estructurar elementos as-is",
                objective="Convertir notas y fuentes en elementos normalizados del proceso actual.",
                actions=[
                    "Extraer actividades, eventos, reglas, roles, sistemas y excepciones.",
                    "Clasificar dolores, oportunidades, controles y metricas.",
                    "Revisar cada elemento con responsable humano antes de modelar.",
                ],
                outputs=[
                    "Inventario as-is",
                    "Mapa de reglas y excepciones",
                    "Base para narrativa as-is",
                ],
                checks=[
                    "Los elementos tienen fuente y confianza.",
                    "No hay actividades duplicadas o ambiguas.",
                    "Las reglas de negocio son verificables.",
                ],
                related_topics=["BPM y gestion por procesos", "Riesgos y controles"],
                topic_counts=topic_counts,
            ),
            self._methodology_phase(
                phase="4. Modelar BPMN as-is",
                objective="Transformar el inventario validado en un modelo BPMN entendible y revisable.",
                actions=[
                    "Mapear actividades a tareas BPMN.",
                    "Mapear eventos de inicio, fin y excepciones.",
                    "Convertir decisiones y reglas en gateways.",
                    "Usar lanes para roles o areas cuando aporte claridad.",
                ],
                outputs=[
                    "BPMN XML as-is",
                    "Narrativa as-is versionada",
                    "Comentarios por actividad",
                ],
                checks=[
                    "El flujo tiene inicio y fin claros.",
                    "Los gateways tienen condiciones documentadas.",
                    "El modelo coincide con la evidencia levantada.",
                ],
                related_topics=["Modelado BPMN", "BPM y gestion por procesos"],
                topic_counts=topic_counts,
            ),
            self._methodology_phase(
                phase="5. Analizar datos y performance",
                objective="Complementar el levantamiento con metricas, logs y analisis cuantitativo.",
                actions=[
                    "Identificar KPI, SLA, volumenes, tiempos y colas.",
                    "Cargar event logs cuando existan.",
                    "Comparar variantes reales contra el proceso declarado.",
                ],
                outputs=[
                    "Indicadores del as-is",
                    "Hallazgos de process mining",
                    "Cuellos de botella priorizados",
                ],
                checks=[
                    "Los datos tienen calidad suficiente.",
                    "Cada metrica tiene definicion y fuente.",
                    "Los hallazgos distinguen evidencia de hipotesis.",
                ],
                related_topics=["Process mining", "Metricas y simulacion"],
                topic_counts=topic_counts,
            ),
            self._methodology_phase(
                phase="6. Identificar mejoras y riesgos",
                objective="Detectar oportunidades de simplificacion, automatizacion, control y transformacion digital.",
                actions=[
                    "Clasificar desperdicios, reprocesos y controles manuales.",
                    "Evaluar riesgos, cumplimiento y segregacion de funciones.",
                    "Proponer mejoras con impacto, esfuerzo y evidencia.",
                ],
                outputs=[
                    "Matriz de hallazgos",
                    "Mapa de riesgos y controles",
                    "Backlog de oportunidades",
                ],
                checks=[
                    "Cada recomendacion tiene fuente.",
                    "Se separan mejoras rapidas de cambios estructurales.",
                    "Los riesgos no se eliminan sin control alternativo.",
                ],
                related_topics=["Mejora continua", "Riesgos y controles", "Transformacion digital"],
                topic_counts=topic_counts,
            ),
            self._methodology_phase(
                phase="7. Disenar to-be y simular",
                objective="Construir alternativas futuras, estimar impacto y validarlas con las areas involucradas.",
                actions=[
                    "Disenar escenarios to-be con roles, sistemas y controles.",
                    "Comparar as-is contra to-be.",
                    "Simular capacidad, tiempos, costos y sensibilidad cuando existan datos.",
                ],
                outputs=[
                    "BPMN to-be",
                    "Escenarios de simulacion",
                    "Recomendacion final trazable",
                ],
                checks=[
                    "Los supuestos de simulacion estan documentados.",
                    "El to-be conserva controles necesarios.",
                    "Las areas validan cambios de responsabilidad.",
                ],
                related_topics=["Transformacion digital", "Metricas y simulacion", "Modelado BPMN"],
                topic_counts=topic_counts,
            ),
            self._methodology_phase(
                phase="8. Cerrar y gobernar entregables",
                objective="Versionar, aprobar y presentar resultados profesionales para decision y ejecucion.",
                actions=[
                    "Versionar narrativas, BPMN, evidencias y reportes.",
                    "Solicitar aprobacion humana por hito critico.",
                    "Preparar informe ejecutivo, tecnico y plan de implementacion.",
                ],
                outputs=[
                    "Informe final",
                    "BPMN aprobado",
                    "Plan de implementacion",
                ],
                checks=[
                    "Cada entregable tiene version aprobada.",
                    "La decision final se basa en evidencia.",
                    "El caso queda cerrado con responsables claros.",
                ],
                related_topics=["Gestion de casos de proceso", "Riesgos y controles"],
                topic_counts=topic_counts,
            ),
        ]

        return CaseMethodologyResponse(
            title="Esquema operativo del agente para gestionar casos de proceso",
            language="es",
            source_insight_count=len(insights),
            phases=phases,
        )

    @staticmethod
    def _project_path(path_value: str) -> Path:
        path = Path(path_value)
        if path.is_absolute():
            return path
        return PROJECT_ROOT / path

    @staticmethod
    def _load_training_manifest(training_dir: Path) -> dict:
        manifest_path = training_dir / "knowledge-distillation-manifest.json"
        if not manifest_path.exists():
            return {}
        try:
            data = json.loads(manifest_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return {}
        return data if isinstance(data, dict) else {}

    @staticmethod
    def _count_dataset_examples(dataset_path: Path) -> int:
        if not dataset_path.exists():
            return 0
        with dataset_path.open("r", encoding="utf-8") as dataset_file:
            return sum(1 for line in dataset_file if line.strip())

    @staticmethod
    def _artifact_response(name: str, kind: str, path: Path) -> AgentTrainingArtifactResponse:
        return AgentTrainingArtifactResponse(
            name=name,
            kind=kind,
            path=str(path),
            exists=path.exists(),
            size_bytes=path.stat().st_size if path.exists() and path.is_file() else None,
        )

    def _extract_text(self, file_path: Path, raw_content: bytes) -> str:
        suffix = file_path.suffix.lower()
        if suffix == ".pdf":
            return self._extract_pdf_text(file_path)
        if suffix == ".docx":
            return self._extract_docx_text(file_path)
        if suffix in TEXT_SUFFIXES:
            return self._decode_text(raw_content)

        return self._decode_text(raw_content)

    def _create_insights_for_documents(self, documents: list[KnowledgeDocumentModel]) -> int:
        created = 0
        for document in documents:
            for chunk in document.chunks:
                for candidate in self._extract_insight_candidates(document, chunk):
                    exists = self.db.scalars(
                        select(KnowledgeInsightModel).where(
                            KnowledgeInsightModel.chunk_id == chunk.id,
                            KnowledgeInsightModel.topic == candidate["topic"],
                        )
                    ).first()
                    if exists is not None:
                        continue

                    insight = KnowledgeInsightModel(
                        id=str(uuid4()),
                        document_id=document.id,
                        chunk_id=chunk.id,
                        insight_type=candidate["insight_type"],
                        topic=candidate["topic"],
                        title_es=candidate["title_es"],
                        summary_es=candidate["summary_es"],
                        source_excerpt=candidate["source_excerpt"],
                        source_language=document.language,
                        confidence_level=candidate["confidence_level"],
                        created_by="heuristic_bilingual_analyzer",
                    )
                    self.db.add(insight)
                    created += 1

        if created:
            self.db.commit()
        return created

    def _extract_insight_candidates(
        self,
        document: KnowledgeDocumentModel,
        chunk: KnowledgeChunkModel,
    ) -> list[dict[str, str]]:
        text = chunk.content
        lowered = text.lower()
        candidates: list[dict[str, str]] = []
        for rule in TOPIC_RULES:
            matches = [keyword for keyword in rule["keywords"] if keyword in lowered]
            if not matches:
                continue

            excerpt = self._best_excerpt(text, matches)
            confidence = ConfidenceLevel.high.value if len(matches) >= 2 else ConfidenceLevel.medium.value
            candidates.append(
                {
                    "insight_type": rule["insight_type"],
                    "topic": rule["topic"],
                    "title_es": self._build_insight_title(rule["topic"], document.title),
                    "summary_es": self._build_insight_summary(rule["topic"], matches, excerpt),
                    "source_excerpt": excerpt,
                    "confidence_level": confidence,
                }
            )
        return candidates

    @staticmethod
    def _best_excerpt(text: str, matches: list[str], max_length: int = 520) -> str:
        sentences = [sentence.strip() for sentence in re.split(r"(?<=[.!?])\s+|\n+", text) if sentence.strip()]
        for match in matches:
            for sentence in sentences:
                if match in sentence.lower():
                    return sentence[:max_length]
        return text.strip()[:max_length]

    @staticmethod
    def _build_insight_title(topic: str, document_title: str) -> str:
        return f"{topic} - fuente {document_title[:90]}"

    @staticmethod
    def _build_insight_summary(topic: str, matches: list[str], excerpt: str) -> str:
        signals = ", ".join(sorted(set(matches))[:5])
        return (
            f"La fuente aporta conocimiento tecnico sobre {topic}. "
            f"Senales detectadas: {signals}. "
            f"Debe usarse como referencia trazable al analizar procesos y documentar decisiones."
        )

    def _count_insights(self) -> int:
        return len(self.db.scalars(select(KnowledgeInsightModel.id)).all())

    def _methodology_phase(
        self,
        phase: str,
        objective: str,
        actions: list[str],
        outputs: list[str],
        checks: list[str],
        related_topics: list[str],
        topic_counts: dict[str, int],
    ) -> CaseMethodologyPhaseResponse:
        source_count = sum(topic_counts.get(topic, 0) for topic in related_topics)
        return CaseMethodologyPhaseResponse(
            phase=phase,
            objective_es=objective,
            actions_es=actions,
            outputs_es=outputs,
            quality_checks_es=checks,
            related_topics=related_topics,
            source_insight_count=source_count,
        )

    @staticmethod
    def _extract_pdf_text(file_path: Path) -> str:
        reader = PdfReader(str(file_path))
        return "\n\n".join(page.extract_text() or "" for page in reader.pages).strip()

    @staticmethod
    def _extract_docx_text(file_path: Path) -> str:
        document = DocxDocument(str(file_path))
        paragraphs = [paragraph.text for paragraph in document.paragraphs if paragraph.text.strip()]
        return "\n\n".join(paragraphs).strip()

    @staticmethod
    def _decode_text(raw_content: bytes) -> str:
        for encoding in ("utf-8", "utf-8-sig", "cp1252"):
            try:
                return raw_content.decode(encoding).strip()
            except UnicodeDecodeError:
                continue
        return raw_content.decode("utf-8", errors="replace").strip()

    @staticmethod
    def _chunk_text(
        text: str,
        chunk_size: int = DEFAULT_CHUNK_SIZE,
        overlap: int = DEFAULT_CHUNK_OVERLAP,
    ) -> list[dict[str, int | str]]:
        normalized = re.sub(r"\n{3,}", "\n\n", text.strip())
        if not normalized:
            return []

        chunks: list[dict[str, int | str]] = []
        start = 0
        text_length = len(normalized)

        while start < text_length:
            if start > 0:
                start = KnowledgeService._snap_to_next_boundary(normalized, start)

            end = min(start + chunk_size, text_length)
            if end < text_length:
                window = normalized[start:end]
                split_at = max(window.rfind("\n\n"), window.rfind(". "), window.rfind("\n"))
                if split_at > int(chunk_size * 0.55):
                    end = start + split_at + 1

            content = normalized[start:end].strip()
            if content:
                chunks.append(
                    {
                        "content": content,
                        "char_start": start,
                        "char_end": end,
                    }
                )

            if end >= text_length:
                break
            start = max(0, end - overlap)

        return chunks

    @staticmethod
    def _snap_to_next_boundary(text: str, start: int, max_scan: int = 80) -> int:
        scan_end = min(start + max_scan, len(text))
        candidates = [
            position
            for position in (
                text.find("\n\n", start, scan_end),
                text.find("\n", start, scan_end),
                text.find(" ", start, scan_end),
            )
            if position != -1
        ]
        if not candidates:
            return start
        return min(candidates) + 1

    @staticmethod
    def _safe_filename(filename: str) -> str:
        safe = re.sub(r"[^A-Za-z0-9._-]+", "-", filename).strip(".-")
        return safe or "documento.txt"

    @staticmethod
    def _clean_text(value: str | None) -> str | None:
        if value is None:
            return None
        cleaned = value.strip()
        return cleaned or None

    @staticmethod
    def _document_to_response(document: KnowledgeDocumentModel) -> KnowledgeDocumentResponse:
        return KnowledgeDocumentResponse(
            id=UUID(document.id),
            title=document.title,
            author=document.author,
            source_type=KnowledgeSourceType(document.source_type),
            subject_area=document.subject_area,
            language=document.language,
            case_id=UUID(document.case_id) if document.case_id else None,
            filename=document.filename,
            mime_type=document.mime_type,
            status=KnowledgeDocumentStatus(document.status),
            error_message=document.error_message,
            text_char_count=document.text_char_count,
            chunk_count=document.chunk_count,
            created_at=document.created_at,
            updated_at=document.updated_at,
        )

    @staticmethod
    def _chunk_to_response(chunk: KnowledgeChunkModel) -> KnowledgeChunkResponse:
        return KnowledgeChunkResponse(
            id=UUID(chunk.id),
            document_id=UUID(chunk.document_id),
            chunk_index=chunk.chunk_index,
            content=chunk.content,
            char_start=chunk.char_start,
            char_end=chunk.char_end,
            created_at=chunk.created_at,
        )

    @staticmethod
    def _insight_to_response(insight: KnowledgeInsightModel) -> KnowledgeInsightResponse:
        return KnowledgeInsightResponse(
            id=UUID(insight.id),
            document_id=UUID(insight.document_id),
            chunk_id=UUID(insight.chunk_id),
            insight_type=KnowledgeInsightType(insight.insight_type),
            topic=insight.topic,
            title_es=insight.title_es,
            summary_es=insight.summary_es,
            source_excerpt=insight.source_excerpt,
            source_language=insight.source_language,
            confidence_level=ConfidenceLevel(insight.confidence_level),
            created_by=insight.created_by,
            created_at=insight.created_at,
        )
