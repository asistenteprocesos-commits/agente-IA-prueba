import {
  Activity,
  ClipboardList,
  Database,
  FileText,
  GitBranch,
  Plus,
  ShieldCheck,
  Upload,
  Users,
} from "lucide-react";
import { type FormEvent, useEffect, useState } from "react";

import {
  addArtifactEvidence,
  analyzeKnowledgeLibrary,
  commentArtifactVersion,
  compareArtifactVersions,
  createAsIsElement,
  createArtifactVersion,
  createProcessInterview,
  createProcessArtifact,
  createProcessCase,
  createProcessStakeholder,
  decideArtifactVersion,
  extractAsIsElements,
  getAgentTrainingProfile,
  getInterviewGuide,
  getArtifactVersionHistory,
  getArtifactQuality,
  getHealth,
  getCaseMethodology,
  getProcessRepository,
  getLocalLLMProfile,
  listArtifactEvidence,
  listKnowledgeChunks,
  listKnowledgeDocuments,
  listKnowledgeInsights,
  listAsIsElements,
  listProcessInterviews,
  listProcessArtifacts,
  listProcessCases,
  listProcessStakeholders,
  uploadKnowledgeDocumentsBulk,
  type AgentTrainingProfile,
  type ArtifactEvidence,
  type ArtifactQuality,
  type ArtifactVersionHistory,
  type CaseMethodology,
  type HealthResponse,
  type InterviewGuide,
  type KnowledgeChunk,
  type KnowledgeDocument,
  type KnowledgeInsight,
  type KnowledgeLearningRun,
  type LocalLLMProfile,
  type ProcessAsIsElement,
  type ProcessArtifact,
  type ProcessCase,
  type ProcessInterview,
  type ProcessRepository,
  type ProcessStakeholder,
  type VersionDiff,
} from "./api";

const foundationItems = [
  {
    icon: FileText,
    title: "Repositorio documental",
    text: "Narrativas, BPMN y evidencias versionadas por caso.",
  },
  {
    icon: GitBranch,
    title: "Control de versiones",
    text: "Borradores, revisiones, aprobaciones y versiones publicadas.",
  },
  {
    icon: Database,
    title: "Base de conocimiento",
    text: "Documentos BPM, procesos y transformacion digital con citas.",
  },
  {
    icon: ShieldCheck,
    title: "Supervision humana",
    text: "Toda salida critica queda pendiente de aprobacion.",
  },
];

export function App() {
  const [health, setHealth] = useState<HealthResponse | null>(null);
  const [cases, setCases] = useState<ProcessCase[]>([]);
  const [selectedCaseId, setSelectedCaseId] = useState<string | null>(null);
  const [repository, setRepository] = useState<ProcessRepository | null>(null);
  const [artifacts, setArtifacts] = useState<ProcessArtifact[]>([]);
  const [knowledgeDocuments, setKnowledgeDocuments] = useState<KnowledgeDocument[]>([]);
  const [knowledgeChunks, setKnowledgeChunks] = useState<KnowledgeChunk[]>([]);
  const [knowledgeInsights, setKnowledgeInsights] = useState<KnowledgeInsight[]>([]);
  const [caseMethodology, setCaseMethodology] = useState<CaseMethodology | null>(null);
  const [agentTrainingProfile, setAgentTrainingProfile] = useState<AgentTrainingProfile | null>(null);
  const [localLLMProfile, setLocalLLMProfile] = useState<LocalLLMProfile | null>(null);
  const [learningRun, setLearningRun] = useState<KnowledgeLearningRun | null>(null);
  const [stakeholders, setStakeholders] = useState<ProcessStakeholder[]>([]);
  const [interviews, setInterviews] = useState<ProcessInterview[]>([]);
  const [interviewGuide, setInterviewGuide] = useState<InterviewGuide | null>(null);
  const [asIsElements, setAsIsElements] = useState<ProcessAsIsElement[]>([]);
  const [selectedArtifactId, setSelectedArtifactId] = useState<string | null>(null);
  const [selectedVersionId, setSelectedVersionId] = useState<string | null>(null);
  const [selectedKnowledgeDocumentId, setSelectedKnowledgeDocumentId] = useState<string | null>(null);
  const [versionHistory, setVersionHistory] = useState<ArtifactVersionHistory | null>(null);
  const [evidence, setEvidence] = useState<ArtifactEvidence[]>([]);
  const [quality, setQuality] = useState<ArtifactQuality | null>(null);
  const [diff, setDiff] = useState<VersionDiff | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [caseError, setCaseError] = useState<string | null>(null);
  const [artifactError, setArtifactError] = useState<string | null>(null);
  const [knowledgeError, setKnowledgeError] = useState<string | null>(null);
  const [knowledgeUploadMessage, setKnowledgeUploadMessage] = useState<string | null>(null);
  const [discoveryError, setDiscoveryError] = useState<string | null>(null);
  const [reviewError, setReviewError] = useState<string | null>(null);
  const [traceError, setTraceError] = useState<string | null>(null);
  const [isCreating, setIsCreating] = useState(false);
  const [isCreatingArtifact, setIsCreatingArtifact] = useState(false);
  const [isUploadingKnowledge, setIsUploadingKnowledge] = useState(false);
  const [isAnalyzingKnowledge, setIsAnalyzingKnowledge] = useState(false);
  const [isCreatingStakeholder, setIsCreatingStakeholder] = useState(false);
  const [isCreatingInterview, setIsCreatingInterview] = useState(false);
  const [isCreatingAsIsElement, setIsCreatingAsIsElement] = useState(false);
  const [extractingInterviewId, setExtractingInterviewId] = useState<string | null>(null);
  const [isReviewing, setIsReviewing] = useState(false);
  const [isTracing, setIsTracing] = useState(false);

  useEffect(() => {
    let active = true;

    getHealth()
      .then((data) => {
        if (active) {
          setHealth(data);
          setError(null);
        }
      })
      .catch((reason: unknown) => {
        if (active) {
          setError(reason instanceof Error ? reason.message : "No se pudo contactar el backend");
        }
      });

    return () => {
      active = false;
    };
  }, []);

  useEffect(() => {
    let active = true;

    listProcessCases()
      .then((data) => {
        if (active) {
          setCases(data);
          setSelectedCaseId((current) => current ?? data[0]?.id ?? null);
          setCaseError(null);
        }
      })
      .catch((reason: unknown) => {
        if (active) {
          setCaseError(reason instanceof Error ? reason.message : "No se pudieron cargar los casos");
        }
      });

    return () => {
      active = false;
    };
  }, []);

  useEffect(() => {
    let active = true;

    Promise.all([
      listKnowledgeDocuments(),
      listKnowledgeInsights(),
      getCaseMethodology(),
      getAgentTrainingProfile(),
      getLocalLLMProfile(),
    ])
      .then(([documents, insights, methodology, trainingProfile, llmProfile]) => {
        if (active) {
          setKnowledgeDocuments(documents);
          setKnowledgeInsights(insights);
          setCaseMethodology(methodology);
          setAgentTrainingProfile(trainingProfile);
          setLocalLLMProfile(llmProfile);
          setSelectedKnowledgeDocumentId((current) => current ?? documents[0]?.id ?? null);
          setKnowledgeError(null);
        }
      })
      .catch((reason: unknown) => {
        if (active) {
          setKnowledgeError(reason instanceof Error ? reason.message : "No se pudieron cargar los documentos");
        }
      });

    return () => {
      active = false;
    };
  }, []);

  useEffect(() => {
    if (!selectedCaseId) {
      setRepository(null);
      setArtifacts([]);
      return;
    }

    let active = true;

    Promise.all([getProcessRepository(selectedCaseId), listProcessArtifacts(selectedCaseId)])
      .then(([repositoryData, artifactData]) => {
        if (active) {
          setRepository(repositoryData);
          setArtifacts(artifactData);
          setSelectedArtifactId(artifactData[0]?.id ?? null);
          setSelectedVersionId(artifactData[0]?.versions[0]?.id ?? null);
          setArtifactError(null);
        }
      })
      .catch((reason: unknown) => {
        if (active) {
          setArtifactError(reason instanceof Error ? reason.message : "No se pudo cargar el repositorio");
        }
      });

    return () => {
      active = false;
    };
  }, [selectedCaseId]);

  useEffect(() => {
    if (!selectedCaseId) {
      setStakeholders([]);
      setInterviews([]);
      setInterviewGuide(null);
      setAsIsElements([]);
      return;
    }

    let active = true;

    Promise.all([
      listProcessStakeholders(selectedCaseId),
      listProcessInterviews(selectedCaseId),
      getInterviewGuide(selectedCaseId),
      listAsIsElements(selectedCaseId),
    ])
      .then(([stakeholderData, interviewData, guideData, elementData]) => {
        if (active) {
          setStakeholders(stakeholderData);
          setInterviews(interviewData);
          setInterviewGuide(guideData);
          setAsIsElements(elementData);
          setDiscoveryError(null);
        }
      })
      .catch((reason: unknown) => {
        if (active) {
          setDiscoveryError(reason instanceof Error ? reason.message : "No se pudo cargar el levantamiento");
        }
      });

    return () => {
      active = false;
    };
  }, [selectedCaseId]);

  useEffect(() => {
    if (!selectedKnowledgeDocumentId) {
      setKnowledgeChunks([]);
      return;
    }

    let active = true;

    listKnowledgeChunks(selectedKnowledgeDocumentId)
      .then((data) => {
        if (active) {
          setKnowledgeChunks(data);
          setKnowledgeError(null);
        }
      })
      .catch((reason: unknown) => {
        if (active) {
          setKnowledgeError(reason instanceof Error ? reason.message : "No se pudieron cargar los fragmentos");
        }
      });

    return () => {
      active = false;
    };
  }, [selectedKnowledgeDocumentId]);

  useEffect(() => {
    if (!selectedCaseId || !selectedVersionId) {
      setVersionHistory(null);
      setEvidence([]);
      setQuality(null);
      return;
    }

    let active = true;

    Promise.all([
      getArtifactVersionHistory(selectedCaseId, selectedVersionId),
      listArtifactEvidence(selectedCaseId, selectedVersionId),
      getArtifactQuality(selectedCaseId, selectedVersionId),
    ])
      .then(([history, evidenceData, qualityData]) => {
        if (active) {
          setVersionHistory(history);
          setEvidence(evidenceData);
          setQuality(qualityData);
          setReviewError(null);
          setTraceError(null);
        }
      })
      .catch((reason: unknown) => {
        if (active) {
          setReviewError(reason instanceof Error ? reason.message : "No se pudo cargar la trazabilidad");
        }
      });

    return () => {
      active = false;
    };
  }, [selectedCaseId, selectedVersionId]);

  async function handleCreateCase(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setIsCreating(true);
    setCaseError(null);

    const form = new FormData(event.currentTarget);
    const payload = {
      name: String(form.get("name") ?? "").trim(),
      area: String(form.get("area") ?? "").trim() || undefined,
      objective: String(form.get("objective") ?? "").trim() || undefined,
      scope: String(form.get("scope") ?? "").trim() || undefined,
      owner: String(form.get("owner") ?? "").trim() || undefined,
    };

    try {
      const created = await createProcessCase(payload);
      setCases((current) => [created, ...current]);
      setSelectedCaseId(created.id);
      event.currentTarget.reset();
    } catch (reason) {
      setCaseError(reason instanceof Error ? reason.message : "No se pudo crear el caso");
    } finally {
      setIsCreating(false);
    }
  }

  async function handleUploadKnowledgeDocument(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setIsUploadingKnowledge(true);
    setKnowledgeError(null);
    setKnowledgeUploadMessage(null);

    const form = new FormData(event.currentTarget);
    const fileEntries = form.getAll("files").filter((entry): entry is File => entry instanceof File && entry.size > 0);

    if (fileEntries.length === 0) {
      setKnowledgeError("Selecciona uno o varios archivos antes de cargar la fuente");
      setIsUploadingKnowledge(false);
      return;
    }

    const payload = new FormData();
    for (const fileEntry of fileEntries) {
      payload.append("files", fileEntry);
    }
    payload.append("language", String(form.get("language") ?? "es").trim() || "es");
    payload.append("source_type", String(form.get("source_type") ?? "book"));

    for (const field of ["author", "subject_area"]) {
      const value = String(form.get(field) ?? "").trim();
      if (value) {
        payload.append(field, value);
      }
    }

    if (selectedCaseId) {
      payload.append("case_id", selectedCaseId);
    }

    try {
      const created = await uploadKnowledgeDocumentsBulk(payload);
      setKnowledgeDocuments((current) => [...created, ...current]);
      setSelectedKnowledgeDocumentId(created[0]?.id ?? null);
      setKnowledgeUploadMessage(`${created.length} fuente(s) cargada(s) para la biblioteca del agente`);
      event.currentTarget.reset();
    } catch (reason) {
      setKnowledgeError(reason instanceof Error ? reason.message : "No se pudieron cargar los documentos");
    } finally {
      setIsUploadingKnowledge(false);
    }
  }

  async function handleAnalyzeKnowledgeLibrary() {
    setIsAnalyzingKnowledge(true);
    setKnowledgeError(null);
    setKnowledgeUploadMessage(null);

    try {
      const run = await analyzeKnowledgeLibrary();
      const [insights, methodology] = await Promise.all([listKnowledgeInsights(), getCaseMethodology()]);
      setLearningRun(run);
      setKnowledgeInsights(insights);
      setCaseMethodology(methodology);
      setKnowledgeUploadMessage(
        `Analisis completado: ${run.created_insights} aprendizaje(s) nuevo(s), ${run.total_insights} en total`,
      );
    } catch (reason) {
      setKnowledgeError(reason instanceof Error ? reason.message : "No se pudo analizar la biblioteca");
    } finally {
      setIsAnalyzingKnowledge(false);
    }
  }

  async function handleCreateStakeholder(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    if (!selectedCaseId) {
      setDiscoveryError("Selecciona un caso antes de registrar participantes");
      return;
    }

    setIsCreatingStakeholder(true);
    setDiscoveryError(null);

    const form = new FormData(event.currentTarget);
    const payload = {
      name: String(form.get("name") ?? "").trim(),
      role: String(form.get("role") ?? "participant"),
      area: String(form.get("area") ?? "").trim() || undefined,
      email: String(form.get("email") ?? "").trim() || undefined,
      influence_level: String(form.get("influence_level") ?? "medium"),
      availability: String(form.get("availability") ?? "").trim() || undefined,
      notes: String(form.get("notes") ?? "").trim() || undefined,
    };

    try {
      const created = await createProcessStakeholder(selectedCaseId, payload);
      setStakeholders((current) => [created, ...current]);
      setCases((current) =>
        current.map((processCase) =>
          processCase.id === selectedCaseId ? { ...processCase, status: "discovery" } : processCase,
        ),
      );
      event.currentTarget.reset();
    } catch (reason) {
      setDiscoveryError(reason instanceof Error ? reason.message : "No se pudo registrar el participante");
    } finally {
      setIsCreatingStakeholder(false);
    }
  }

  async function handleCreateInterview(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    if (!selectedCaseId) {
      setDiscoveryError("Selecciona un caso antes de registrar entrevistas");
      return;
    }

    setIsCreatingInterview(true);
    setDiscoveryError(null);

    const form = new FormData(event.currentTarget);
    const stakeholderId = String(form.get("stakeholder_id") ?? "").trim();
    const scheduledAt = String(form.get("scheduled_at") ?? "").trim();
    const payload = {
      stakeholder_id: stakeholderId || undefined,
      title: String(form.get("title") ?? "").trim(),
      interview_type: String(form.get("interview_type") ?? "discovery"),
      status: String(form.get("status") ?? "planned"),
      scheduled_at: scheduledAt || undefined,
      objective: String(form.get("objective") ?? "").trim() || undefined,
      questions: String(form.get("questions") ?? "").trim() || undefined,
      notes: String(form.get("notes") ?? "").trim() || undefined,
      summary: String(form.get("summary") ?? "").trim() || undefined,
    };

    try {
      const created = await createProcessInterview(selectedCaseId, payload);
      setInterviews((current) => [created, ...current]);
      setCases((current) =>
        current.map((processCase) =>
          processCase.id === selectedCaseId ? { ...processCase, status: "discovery" } : processCase,
        ),
      );
      event.currentTarget.reset();
    } catch (reason) {
      setDiscoveryError(reason instanceof Error ? reason.message : "No se pudo registrar la entrevista");
    } finally {
      setIsCreatingInterview(false);
    }
  }

  async function handleCreateAsIsElement(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    if (!selectedCaseId) {
      setDiscoveryError("Selecciona un caso antes de registrar elementos as-is");
      return;
    }

    setIsCreatingAsIsElement(true);
    setDiscoveryError(null);

    const form = new FormData(event.currentTarget);
    const interviewId = String(form.get("interview_id") ?? "").trim();
    const payload = {
      interview_id: interviewId || undefined,
      element_type: String(form.get("element_type") ?? "activity"),
      name: String(form.get("name") ?? "").trim(),
      description: String(form.get("description") ?? "").trim() || undefined,
      source_excerpt: String(form.get("source_excerpt") ?? "").trim() || undefined,
      confidence_level: String(form.get("confidence_level") ?? "medium"),
      created_by: "human",
    };

    try {
      const created = await createAsIsElement(selectedCaseId, payload);
      setAsIsElements((current) => [created, ...current]);
      setCases((current) =>
        current.map((processCase) =>
          processCase.id === selectedCaseId ? { ...processCase, status: "as_is_drafting" } : processCase,
        ),
      );
      event.currentTarget.reset();
    } catch (reason) {
      setDiscoveryError(reason instanceof Error ? reason.message : "No se pudo registrar el elemento as-is");
    } finally {
      setIsCreatingAsIsElement(false);
    }
  }

  async function handleExtractAsIsElements(interviewId: string) {
    if (!selectedCaseId) {
      return;
    }

    setExtractingInterviewId(interviewId);
    setDiscoveryError(null);

    try {
      const extracted = await extractAsIsElements(selectedCaseId, interviewId);
      setAsIsElements((current) => [...extracted, ...current]);
      setCases((current) =>
        current.map((processCase) =>
          processCase.id === selectedCaseId ? { ...processCase, status: "as_is_drafting" } : processCase,
        ),
      );
    } catch (reason) {
      setDiscoveryError(reason instanceof Error ? reason.message : "No se pudo extraer elementos as-is");
    } finally {
      setExtractingInterviewId(null);
    }
  }

  async function handleCreateArtifact(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    if (!selectedCaseId) {
      setArtifactError("Selecciona un caso antes de crear artefactos");
      return;
    }

    setIsCreatingArtifact(true);
    setArtifactError(null);

    const form = new FormData(event.currentTarget);
    const payload = {
      artifact_type: String(form.get("artifact_type") ?? "process_narrative_as_is"),
      title: String(form.get("title") ?? "").trim(),
      description: String(form.get("description") ?? "").trim() || undefined,
      content: String(form.get("content") ?? "").trim(),
      change_summary: String(form.get("change_summary") ?? "").trim() || undefined,
      author: String(form.get("author") ?? "").trim() || undefined,
    };

    try {
      const created = await createProcessArtifact(selectedCaseId, payload);
      setArtifacts((current) => [created, ...current]);
      setSelectedArtifactId(created.id);
      setSelectedVersionId(created.versions[0]?.id ?? null);
      setRepository((current) =>
        current ? { ...current, artifact_count: current.artifact_count + 1 } : current,
      );
      event.currentTarget.reset();
    } catch (reason) {
      setArtifactError(reason instanceof Error ? reason.message : "No se pudo crear el artefacto");
    } finally {
      setIsCreatingArtifact(false);
    }
  }

  async function handleCreateVersion(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    if (!selectedCaseId || !selectedArtifactId) {
      setTraceError("Selecciona un artefacto antes de crear una nueva version");
      return;
    }

    setIsTracing(true);
    setTraceError(null);

    const form = new FormData(event.currentTarget);
    const payload = {
      version: String(form.get("version") ?? "").trim(),
      content: String(form.get("content") ?? "").trim(),
      change_summary: String(form.get("change_summary") ?? "").trim() || undefined,
      author: String(form.get("author") ?? "").trim() || undefined,
    };

    try {
      const created = await createArtifactVersion(selectedCaseId, selectedArtifactId, payload);
      setArtifacts((current) =>
        current.map((artifact) =>
          artifact.id === selectedArtifactId
            ? { ...artifact, versions: [created, ...artifact.versions], current_version_id: created.id }
            : artifact,
        ),
      );
      setSelectedVersionId(created.id);
      setDiff(null);
      event.currentTarget.reset();
    } catch (reason) {
      setTraceError(reason instanceof Error ? reason.message : "No se pudo crear la version");
    } finally {
      setIsTracing(false);
    }
  }

  async function handleDecision(action: string) {
    if (!selectedCaseId || !selectedVersionId) {
      return;
    }

    setIsReviewing(true);
    setReviewError(null);

    const commentInput = document.querySelector<HTMLInputElement>("#review-comment");
    const comment = commentInput?.value.trim() || undefined;

    try {
      const decision = await decideArtifactVersion(selectedCaseId, selectedVersionId, {
        action,
        reviewer: "Supervisor humano",
        comment,
      });
      setArtifacts((current) => updateVersionStatus(current, selectedVersionId, decision.new_status));
      const history = await getArtifactVersionHistory(selectedCaseId, selectedVersionId);
      setVersionHistory(history);
      if (commentInput) {
        commentInput.value = "";
      }
    } catch (reason) {
      setReviewError(reason instanceof Error ? reason.message : "No se pudo registrar la decision");
    } finally {
      setIsReviewing(false);
    }
  }

  async function handleAddComment(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    if (!selectedCaseId || !selectedVersionId) {
      return;
    }

    setIsReviewing(true);
    setReviewError(null);

    const form = new FormData(event.currentTarget);
    const payload = {
      author: String(form.get("author") ?? "").trim() || "Supervisor humano",
      comment: String(form.get("comment") ?? "").trim(),
    };

    try {
      await commentArtifactVersion(selectedCaseId, selectedVersionId, payload);
      const history = await getArtifactVersionHistory(selectedCaseId, selectedVersionId);
      setVersionHistory(history);
      event.currentTarget.reset();
    } catch (reason) {
      setReviewError(reason instanceof Error ? reason.message : "No se pudo registrar el comentario");
    } finally {
      setIsReviewing(false);
    }
  }

  async function handleAddEvidence(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    if (!selectedCaseId || !selectedVersionId) {
      return;
    }

    setIsTracing(true);
    setTraceError(null);

    const form = new FormData(event.currentTarget);
    const payload = {
      evidence_type: String(form.get("evidence_type") ?? "interview"),
      source_title: String(form.get("source_title") ?? "").trim(),
      excerpt: String(form.get("excerpt") ?? "").trim(),
      activity_ref: String(form.get("activity_ref") ?? "").trim() || undefined,
      source_url: String(form.get("source_url") ?? "").trim() || undefined,
      notes: String(form.get("notes") ?? "").trim() || undefined,
    };

    try {
      const created = await addArtifactEvidence(selectedCaseId, selectedVersionId, payload);
      setEvidence((current) => [created, ...current]);
      const qualityData = await getArtifactQuality(selectedCaseId, selectedVersionId);
      setQuality(qualityData);
      event.currentTarget.reset();
    } catch (reason) {
      setTraceError(reason instanceof Error ? reason.message : "No se pudo registrar la evidencia");
    } finally {
      setIsTracing(false);
    }
  }

  async function handleCompareWithPrevious() {
    if (!selectedCaseId || !selectedArtifactId || !selectedVersionId) {
      return;
    }

    const selectedArtifact = artifacts.find((artifact) => artifact.id === selectedArtifactId);
    const selectedIndex = selectedArtifact?.versions.findIndex((version) => version.id === selectedVersionId) ?? -1;
    const previousVersion = selectedArtifact?.versions[selectedIndex + 1];

    if (!previousVersion) {
      setTraceError("Se necesitan al menos dos versiones del mismo artefacto para comparar");
      return;
    }

    setIsTracing(true);
    setTraceError(null);

    try {
      const diffData = await compareArtifactVersions(selectedCaseId, previousVersion.id, selectedVersionId);
      setDiff(diffData);
    } catch (reason) {
      setTraceError(reason instanceof Error ? reason.message : "No se pudo comparar versiones");
    } finally {
      setIsTracing(false);
    }
  }

  const selectedCase = cases.find((processCase) => processCase.id === selectedCaseId) ?? null;
  const selectedArtifact = artifacts.find((artifact) => artifact.id === selectedArtifactId) ?? null;
  const selectedKnowledgeDocument =
    knowledgeDocuments.find((document) => document.id === selectedKnowledgeDocumentId) ?? null;
  const selectedVersionStatus = versionHistory?.version.status ?? null;

  return (
    <main className="app-shell">
      <aside className="sidebar" aria-label="Navegacion principal">
        <div className="brand-mark">AI</div>
        <nav>
          <a className="nav-item active" href="#vision">
            Vision
          </a>
          <a className="nav-item" href="#conocimiento">
            Conocimiento
          </a>
          <a className="nav-item" href="#casos">
            Casos
          </a>
          <a className="nav-item" href="#levantamiento">
            Levantamiento
          </a>
          <a className="nav-item" href="#asis">
            As-is
          </a>
          <a className="nav-item" href="#repositorio">
            Repositorio
          </a>
          <a className="nav-item" href="#estado">
            Estado
          </a>
        </nav>
      </aside>

      <section className="workspace">
        <header className="topbar">
          <div>
            <p className="eyebrow">Agente IA Prueba</p>
            <h1>Alimentacion del agente</h1>
          </div>
          <div className={`status-pill ${health ? "online" : "offline"}`} id="estado">
            <Activity size={18} aria-hidden="true" />
            <span>{health ? "Backend conectado" : "Esperando backend"}</span>
          </div>
        </header>

        <section className="overview-grid" id="vision">
          <article className="panel main-panel">
            <p className="section-label">Biblioteca BPM</p>
            <h2>Conocimiento para analizar procesos</h2>
            <p>
              Carga libros, guias y normas para que el agente pueda recuperar evidencia
              especializada cuando analice procesos, BPMN y transformacion digital.
            </p>
          </article>

          <article className="panel health-panel">
            <p className="section-label">Health check</p>
            {health ? (
              <dl>
                <div>
                  <dt>Servicio</dt>
                  <dd>{health.service}</dd>
                </div>
                <div>
                  <dt>Version</dt>
                  <dd>{health.version}</dd>
                </div>
                <div>
                  <dt>Ambiente</dt>
                  <dd>{health.environment}</dd>
                </div>
              </dl>
            ) : (
              <p className="muted">{error ?? "Conectando con la API local..."}</p>
            )}
          </article>
        </section>

        <section className="knowledge-layout" id="conocimiento">
          <form className="panel case-form" onSubmit={handleUploadKnowledgeDocument}>
            <p className="section-label">Nueva fuente</p>
            <label>
              Archivos
              <input name="files" required multiple type="file" accept=".txt,.md,.csv,.json,.xml,.bpmn,.pdf,.docx" />
            </label>
            <label>
              Autor
              <input name="author" placeholder="Autor, editorial o entidad comun" />
            </label>
            <label>
              Tipo
              <select name="source_type" defaultValue="book">
                <option value="book">Libro</option>
                <option value="article">Articulo</option>
                <option value="internal_document">Documento interno</option>
                <option value="standard">Norma</option>
                <option value="interview">Entrevista</option>
                <option value="process_artifact">Artefacto de proceso</option>
                <option value="other">Otro</option>
              </select>
            </label>
            <label>
              Tema
              <input name="subject_area" placeholder="BPMN, process mining, transformacion digital" />
            </label>
            <label>
              Idioma
              <input name="language" defaultValue="es" />
            </label>
            <button className="primary-button" type="submit" disabled={isUploadingKnowledge}>
              <Upload size={18} aria-hidden="true" />
              <span>{isUploadingKnowledge ? "Cargando..." : "Cargar fuentes"}</span>
            </button>
            {selectedCase ? (
              <p className="muted">Se asociara al caso activo: {selectedCase.name}</p>
            ) : (
              <p className="muted">La fuente quedara como conocimiento general.</p>
            )}
            {knowledgeUploadMessage ? <p className="success-note">{knowledgeUploadMessage}</p> : null}
            {knowledgeError ? <p className="form-error">{knowledgeError}</p> : null}
          </form>

          <section className="panel knowledge-panel">
            <div className="list-header">
              <div>
                <p className="section-label">Base de conocimiento</p>
                <h2>Fuentes cargadas</h2>
              </div>
              <strong>{knowledgeDocuments.length}</strong>
            </div>
            <button
              className="primary-button"
              type="button"
              disabled={isAnalyzingKnowledge || knowledgeDocuments.length === 0}
              onClick={handleAnalyzeKnowledgeLibrary}
            >
              <Database size={18} aria-hidden="true" />
              <span>{isAnalyzingKnowledge ? "Analizando..." : "Analizar biblioteca"}</span>
            </button>
            {learningRun ? (
              <p className="muted">
                {learningRun.analyzed_documents} documento(s), {learningRun.total_insights} aprendizaje(s).
              </p>
            ) : null}

            {agentTrainingProfile ? (
              <div className="learning-preview">
                <div className="list-header compact">
                  <div>
                    <p className="section-label">Memoria del agente</p>
                    <h2>{agentTrainingProfile.profile_name}</h2>
                  </div>
                  <span className="status-tag standalone">
                    {agentTrainingProfile.graph_is_visual ? "Obsidian visual" : "Sin canvas"}
                  </span>
                </div>
                <div className="case-meta">
                  <span>{agentTrainingProfile.books_processed} libros</span>
                  <span>{agentTrainingProfile.pages_processed} paginas</span>
                  <span>{agentTrainingProfile.insights} aprendizajes</span>
                  <span>{agentTrainingProfile.dataset_examples} ejemplos</span>
                </div>
                <p className="muted">{agentTrainingProfile.next_step}</p>
              </div>
            ) : null}

            {localLLMProfile ? (
              <div className="learning-preview">
                <div className="list-header compact">
                  <div>
                    <p className="section-label">LLM local gratuito</p>
                    <h2>{localLLMProfile.runtime}</h2>
                  </div>
                  <span className="status-tag standalone">
                    {localLLMProfile.server_available ? "Activo" : "Pendiente"}
                  </span>
                </div>
                <div className="case-meta">
                  <span>{localLLMProfile.reasoning_model}</span>
                  <span>{localLLMProfile.embedding_model}</span>
                  <span>{localLLMProfile.pulled_models.length} modelos locales</span>
                </div>
                <p className="muted">
                  Razonamiento local con DeepSeek-R1 y machine learning documental con Qwen3 Embedding.
                </p>
                <div className="history-stack">
                  {localLLMProfile.next_actions_es.slice(0, 3).map((action) => (
                    <article className="history-item" key={action}>
                      <strong>{action}</strong>
                    </article>
                  ))}
                </div>
              </div>
            ) : null}

            {knowledgeDocuments.length > 0 ? (
              <div className="knowledge-items">
                {knowledgeDocuments.map((document) => (
                  <article className="knowledge-item" key={document.id}>
                    <div>
                      <h3>{document.title}</h3>
                      <p>{document.filename}</p>
                    </div>
                    <div className="case-meta">
                      <span>{document.source_type}</span>
                      <span>{document.subject_area ?? "Sin tema"}</span>
                      <span>{document.chunk_count} fragmentos</span>
                      <span className="status-tag">{document.status}</span>
                    </div>
                    {document.error_message ? <p className="form-error">{document.error_message}</p> : null}
                    <button
                      className="ghost-button"
                      type="button"
                      onClick={() => setSelectedKnowledgeDocumentId(document.id)}
                    >
                      Ver fragmentos
                    </button>
                  </article>
                ))}
              </div>
            ) : (
              <p className="muted">Todavia no hay documentos cargados para alimentar al agente.</p>
            )}

            <div className="chunk-preview">
              <div className="list-header compact">
                <div>
                  <p className="section-label">Fragmentos</p>
                  <h2>{selectedKnowledgeDocument?.title ?? "Sin fuente seleccionada"}</h2>
                </div>
                {selectedKnowledgeDocument ? (
                  <span className="status-tag standalone">{selectedKnowledgeDocument.language}</span>
                ) : null}
              </div>
              {knowledgeChunks.length > 0 ? (
                <div className="chunk-list">
                  {knowledgeChunks.slice(0, 4).map((chunk) => (
                    <article className="chunk-item" key={chunk.id}>
                      <strong>Fragmento {chunk.chunk_index}</strong>
                      <p>{chunk.content}</p>
                    </article>
                  ))}
                </div>
              ) : (
                <p className="muted">Selecciona una fuente procesada para ver su texto fragmentado.</p>
              )}
            </div>

            <div className="learning-preview">
              <div className="list-header compact">
                <div>
                  <p className="section-label">Aprendizaje</p>
                  <h2>Esquema para gestionar casos</h2>
                </div>
                <span className="status-tag standalone">{caseMethodology?.source_insight_count ?? 0} fuentes</span>
              </div>
              {caseMethodology ? (
                <div className="methodology-list">
                  {caseMethodology.phases.slice(0, 4).map((phase) => (
                    <article className="history-item" key={phase.phase}>
                      <strong>{phase.phase}</strong>
                      <p>{phase.objective_es}</p>
                      <p>Temas: {phase.related_topics.join(", ")}</p>
                    </article>
                  ))}
                </div>
              ) : (
                <p className="muted">Analiza la biblioteca para construir el esquema operativo del agente.</p>
              )}
            </div>

            <div className="learning-preview">
              <div className="list-header compact">
                <div>
                  <p className="section-label">Conceptos</p>
                  <h2>Aprendizajes extraidos</h2>
                </div>
                <span className="status-tag standalone">{knowledgeInsights.length}</span>
              </div>
              {knowledgeInsights.length > 0 ? (
                <div className="insight-list">
                  {knowledgeInsights.slice(0, 6).map((insight) => (
                    <article className="insight-item" key={insight.id}>
                      <div>
                        <span className="element-type">{insight.topic}</span>
                        <h3>{insight.title_es}</h3>
                      </div>
                      <p>{insight.summary_es}</p>
                      <div className="case-meta">
                        <span>{insight.insight_type}</span>
                        <span>{insight.source_language}</span>
                        <span>{insight.confidence_level}</span>
                      </div>
                    </article>
                  ))}
                </div>
              ) : (
                <p className="muted">Todavia no hay aprendizajes estructurados desde los libros.</p>
              )}
            </div>
          </section>
        </section>

        <section className="case-layout" id="casos">
          <form className="panel case-form" onSubmit={handleCreateCase}>
            <p className="section-label">Nuevo caso</p>
            <label>
              Nombre
              <input name="name" required minLength={3} placeholder="Aprobacion de proveedores" />
            </label>
            <label>
              Area
              <input name="area" placeholder="Compras" />
            </label>
            <label>
              Responsable
              <input name="owner" placeholder="Especialista BPM" />
            </label>
            <label>
              Objetivo
              <textarea name="objective" rows={3} placeholder="Levantar y validar el as-is" />
            </label>
            <label>
              Alcance
              <textarea name="scope" rows={4} placeholder="Desde la solicitud hasta el cierre" />
            </label>
            <button className="primary-button" type="submit" disabled={isCreating}>
              <Plus size={18} aria-hidden="true" />
              <span>{isCreating ? "Creando..." : "Crear caso"}</span>
            </button>
            {caseError ? <p className="form-error">{caseError}</p> : null}
          </form>

          <section className="panel case-list" aria-label="Casos de proceso">
            <div className="list-header">
              <div>
                <p className="section-label">Tablero</p>
                <h2>Casos activos</h2>
              </div>
              <strong>{cases.length}</strong>
            </div>
            {cases.length > 0 ? (
              <div className="case-items">
                {cases.map((processCase) => (
                  <article className="case-item" key={processCase.id}>
                    <div>
                      <h3>{processCase.name}</h3>
                      <p>{processCase.objective ?? "Sin objetivo registrado"}</p>
                    </div>
                    <div className="case-meta">
                      <span>{processCase.area ?? "Sin area"}</span>
                      <span>{processCase.owner ?? "Sin responsable"}</span>
                      <span className="status-tag">{processCase.status}</span>
                    </div>
                    <button
                      className="ghost-button"
                      type="button"
                      onClick={() => setSelectedCaseId(processCase.id)}
                    >
                      Ver repositorio
                    </button>
                  </article>
                ))}
              </div>
            ) : (
              <p className="muted">Todavia no hay casos registrados.</p>
            )}
          </section>
        </section>

        <section className="discovery-layout" id="levantamiento">
          <section className="panel discovery-panel">
            <div className="list-header">
              <div>
                <p className="section-label">Levantamiento as-is</p>
                <h2>Participantes</h2>
              </div>
              <Users size={28} aria-hidden="true" />
            </div>
            <form className="case-form" onSubmit={handleCreateStakeholder}>
              <label>
                Nombre
                <input name="name" required minLength={2} placeholder="Responsable del proceso" />
              </label>
              <label>
                Rol
                <select name="role" defaultValue="participant">
                  <option value="process_owner">Dueno del proceso</option>
                  <option value="subject_matter_expert">Experto operativo</option>
                  <option value="approver">Aprobador</option>
                  <option value="participant">Participante</option>
                  <option value="system_owner">Responsable de sistema</option>
                  <option value="risk_control">Riesgo o control</option>
                  <option value="external">Externo</option>
                </select>
              </label>
              <label>
                Area
                <input name="area" placeholder="Compras, Legal, Tesoreria" />
              </label>
              <label>
                Email
                <input name="email" type="email" placeholder="persona@empresa.com" />
              </label>
              <label>
                Influencia
                <select name="influence_level" defaultValue="medium">
                  <option value="low">Baja</option>
                  <option value="medium">Media</option>
                  <option value="high">Alta</option>
                </select>
              </label>
              <label>
                Disponibilidad
                <input name="availability" placeholder="Martes 10h00, taller semanal" />
              </label>
              <label>
                Notas
                <textarea name="notes" rows={3} placeholder="Conocimiento, riesgos o restricciones" />
              </label>
              <button className="primary-button" type="submit" disabled={isCreatingStakeholder || !selectedCaseId}>
                <Plus size={18} aria-hidden="true" />
                <span>{isCreatingStakeholder ? "Registrando..." : "Agregar participante"}</span>
              </button>
            </form>

            <div className="history-stack">
              {stakeholders.length > 0 ? (
                stakeholders.map((stakeholder) => (
                  <article className="history-item" key={stakeholder.id}>
                    <strong>{stakeholder.name}</strong>
                    <p>
                      {stakeholder.role} - {stakeholder.area ?? "Sin area"} - {stakeholder.influence_level}
                    </p>
                    {stakeholder.availability ? <p>{stakeholder.availability}</p> : null}
                  </article>
                ))
              ) : (
                <p className="muted">Selecciona un caso y registra los involucrados del proceso.</p>
              )}
            </div>
          </section>

          <section className="panel discovery-panel">
            <div className="list-header">
              <div>
                <p className="section-label">Entrevistas</p>
                <h2>Guia y sesiones</h2>
              </div>
              <ClipboardList size={28} aria-hidden="true" />
            </div>
            <form className="case-form" onSubmit={handleCreateInterview}>
              <label>
                Participante
                <select name="stakeholder_id" defaultValue="">
                  <option value="">Sin participante asignado</option>
                  {stakeholders.map((stakeholder) => (
                    <option value={stakeholder.id} key={stakeholder.id}>
                      {stakeholder.name}
                    </option>
                  ))}
                </select>
              </label>
              <label>
                Titulo
                <input name="title" required minLength={3} placeholder="Entrevista inicial de levantamiento" />
              </label>
              <label>
                Tipo
                <select name="interview_type" defaultValue="discovery">
                  <option value="discovery">Descubrimiento</option>
                  <option value="validation">Validacion</option>
                  <option value="workshop">Taller</option>
                  <option value="observation">Observacion</option>
                  <option value="follow_up">Seguimiento</option>
                </select>
              </label>
              <label>
                Estado
                <select name="status" defaultValue="planned">
                  <option value="planned">Planificada</option>
                  <option value="scheduled">Agendada</option>
                  <option value="completed">Completada</option>
                  <option value="cancelled">Cancelada</option>
                </select>
              </label>
              <label>
                Fecha
                <input name="scheduled_at" type="datetime-local" />
              </label>
              <label>
                Objetivo
                <textarea name="objective" rows={2} placeholder="Que informacion se debe levantar" />
              </label>
              <label>
                Preguntas
                <textarea name="questions" rows={4} placeholder="Preguntas clave para esta sesion" />
              </label>
              <label>
                Notas
                <textarea name="notes" rows={4} placeholder="Hallazgos, actividades, reglas, excepciones" />
              </label>
              <button className="primary-button" type="submit" disabled={isCreatingInterview || !selectedCaseId}>
                <Plus size={18} aria-hidden="true" />
                <span>{isCreatingInterview ? "Guardando..." : "Registrar entrevista"}</span>
              </button>
              {discoveryError ? <p className="form-error">{discoveryError}</p> : null}
            </form>

            {interviewGuide ? (
              <div className="guide-grid">
                {interviewGuide.sections.map((section) => (
                  <article className="history-item" key={section.title}>
                    <strong>{section.title}</strong>
                    {section.questions.map((question) => (
                      <p key={question}>{question}</p>
                    ))}
                  </article>
                ))}
              </div>
            ) : (
              <p className="muted">La guia se genera cuando seleccionas un caso.</p>
            )}

            <div className="history-stack">
              <h3>Sesiones registradas</h3>
              {interviews.length > 0 ? (
                interviews.map((interview) => (
                  <article className="history-item" key={interview.id}>
                    <strong>{interview.title}</strong>
                    <p>
                      {interview.interview_type} - {interview.status} -{" "}
                      {interview.stakeholder_name ?? "Sin participante"}
                    </p>
                    {interview.notes ? <p>{interview.notes}</p> : null}
                    <button
                      className="ghost-button"
                      type="button"
                      disabled={extractingInterviewId === interview.id}
                      onClick={() => handleExtractAsIsElements(interview.id)}
                    >
                      {extractingInterviewId === interview.id ? "Extrayendo..." : "Extraer as-is"}
                    </button>
                  </article>
                ))
              ) : (
                <p className="muted">Todavia no hay entrevistas registradas para el caso.</p>
              )}
            </div>
          </section>
        </section>

        <section className="asis-layout" id="asis">
          <form className="panel case-form" onSubmit={handleCreateAsIsElement}>
            <p className="section-label">Elemento as-is</p>
            <label>
              Entrevista
              <select name="interview_id" defaultValue="">
                <option value="">Sin entrevista vinculada</option>
                {interviews.map((interview) => (
                  <option value={interview.id} key={interview.id}>
                    {interview.title}
                  </option>
                ))}
              </select>
            </label>
            <label>
              Tipo
              <select name="element_type" defaultValue="activity">
                <option value="activity">Actividad</option>
                <option value="role">Rol</option>
                <option value="event">Evento</option>
                <option value="business_rule">Regla de negocio</option>
                <option value="system">Sistema</option>
                <option value="input_output">Entrada o salida</option>
                <option value="exception">Excepcion</option>
                <option value="pain_point">Dolor</option>
                <option value="opportunity">Oportunidad</option>
                <option value="metric">Metrica</option>
                <option value="control">Control</option>
              </select>
            </label>
            <label>
              Nombre
              <input name="name" required minLength={2} placeholder="Registrar solicitud de proveedor" />
            </label>
            <label>
              Confianza
              <select name="confidence_level" defaultValue="medium">
                <option value="low">Baja</option>
                <option value="medium">Media</option>
                <option value="high">Alta</option>
              </select>
            </label>
            <label>
              Descripcion
              <textarea name="description" rows={3} placeholder="Detalle normalizado del elemento" />
            </label>
            <label>
              Extracto fuente
              <textarea name="source_excerpt" rows={3} placeholder="Frase o nota que respalda este elemento" />
            </label>
            <button className="primary-button" type="submit" disabled={isCreatingAsIsElement || !selectedCaseId}>
              <Plus size={18} aria-hidden="true" />
              <span>{isCreatingAsIsElement ? "Guardando..." : "Agregar elemento"}</span>
            </button>
          </form>

          <section className="panel asis-panel">
            <div className="list-header">
              <div>
                <p className="section-label">Inventario as-is</p>
                <h2>Elementos extraidos</h2>
              </div>
              <strong>{asIsElements.length}</strong>
            </div>
            {asIsElements.length > 0 ? (
              <div className="asis-grid">
                {asIsElements.map((element) => (
                  <article className="asis-item" key={element.id}>
                    <div>
                      <span className="element-type">{element.element_type}</span>
                      <h3>{element.name}</h3>
                    </div>
                    <p>{element.description ?? element.source_excerpt ?? "Sin descripcion"}</p>
                    <div className="case-meta">
                      <span>{element.confidence_level}</span>
                      <span>{element.created_by}</span>
                      <span>{element.interview_title ?? "Sin entrevista"}</span>
                    </div>
                  </article>
                ))}
              </div>
            ) : (
              <p className="muted">
                Registra elementos manualmente o usa el boton de extraccion en una entrevista con notas.
              </p>
            )}
          </section>
        </section>

        <section className="repository-layout" id="repositorio">
          <section className="panel repository-panel">
            <div className="list-header">
              <div>
                <p className="section-label">Repositorio</p>
                <h2>{selectedCase ? selectedCase.name : "Sin caso seleccionado"}</h2>
              </div>
              <strong>{repository?.artifact_count ?? 0}</strong>
            </div>
            {repository ? (
              <p className="muted">
                {repository.name}. Artefactos versionados asociados al caso seleccionado.
              </p>
            ) : (
              <p className="muted">Crea o selecciona un caso para ver su repositorio.</p>
            )}

            <div className="artifact-items">
              {artifacts.map((artifact) => (
                <article className="artifact-item" key={artifact.id}>
                  <div>
                    <h3>{artifact.title}</h3>
                    <p>{artifact.description ?? "Sin descripcion"}</p>
                  </div>
                  <div className="case-meta">
                    <span>{artifact.artifact_type}</span>
                    <span>{artifact.versions[0]?.version ?? "sin version"}</span>
                    <span className="status-tag">{artifact.versions[0]?.status ?? "draft"}</span>
                  </div>
                  <div className="version-buttons">
                    {artifact.versions.map((version) => (
                      <button
                        className="ghost-button"
                        type="button"
                        key={version.id}
                        onClick={() => {
                          setSelectedArtifactId(artifact.id);
                          setSelectedVersionId(version.id);
                          setDiff(null);
                        }}
                      >
                        {version.version} - {version.status}
                      </button>
                    ))}
                  </div>
                </article>
              ))}
              {repository && artifacts.length === 0 ? (
                <p className="muted">Este caso todavia no tiene artefactos.</p>
              ) : null}
            </div>
          </section>

          <form className="panel case-form" onSubmit={handleCreateArtifact}>
            <p className="section-label">Nuevo artefacto</p>
            <label>
              Tipo
              <select name="artifact_type" defaultValue="process_narrative_as_is">
                <option value="process_narrative_as_is">Narrativa as-is</option>
                <option value="bpmn_xml_as_is">BPMN XML as-is</option>
                <option value="interview_notes">Notas de entrevista</option>
                <option value="event_log">Event log</option>
                <option value="mining_report">Reporte process mining</option>
              </select>
            </label>
            <label>
              Titulo
              <input name="title" required minLength={3} placeholder="Narrativa as-is inicial" />
            </label>
            <label>
              Autor
              <input name="author" placeholder="Especialista BPM" />
            </label>
            <label>
              Descripcion
              <textarea name="description" rows={2} placeholder="Primer borrador validable" />
            </label>
            <label>
              Contenido
              <textarea
                name="content"
                required
                rows={5}
                placeholder="Describe el flujo, reglas, roles o contenido BPMN..."
              />
            </label>
            <label>
              Resumen de cambio
              <textarea name="change_summary" rows={2} placeholder="Version inicial del artefacto" />
            </label>
            <button className="primary-button" type="submit" disabled={isCreatingArtifact || !selectedCaseId}>
              <Plus size={18} aria-hidden="true" />
              <span>{isCreatingArtifact ? "Guardando..." : "Crear version"}</span>
            </button>
            {artifactError ? <p className="form-error">{artifactError}</p> : null}
          </form>
        </section>

        <section className="trace-layout">
          <form className="panel case-form" onSubmit={handleCreateVersion}>
            <p className="section-label">Nueva version</p>
            <label>
              Artefacto
              <input value={selectedArtifact?.title ?? "Sin artefacto seleccionado"} readOnly />
            </label>
            <label>
              Version
              <input name="version" required placeholder="0.2.0" />
            </label>
            <label>
              Autor
              <input name="author" placeholder="Especialista BPM" />
            </label>
            <label>
              Contenido
              <textarea name="content" required rows={5} placeholder="Nueva version del contenido" />
            </label>
            <label>
              Resumen de cambio
              <textarea name="change_summary" rows={2} placeholder="Que cambio frente a la version anterior" />
            </label>
            <button className="primary-button" type="submit" disabled={isTracing || !selectedArtifactId}>
              <Plus size={18} aria-hidden="true" />
              <span>Crear nueva version</span>
            </button>
            {traceError ? <p className="form-error">{traceError}</p> : null}
          </form>

          <section className="panel history-panel">
            <div className="list-header">
              <div>
                <p className="section-label">Comparacion</p>
                <h2>{diff ? `${diff.base_version} vs ${diff.target_version}` : "Versiones de texto"}</h2>
              </div>
              {diff ? <span className="status-tag standalone">+{diff.added_lines} / -{diff.removed_lines}</span> : null}
            </div>
            <button
              className="ghost-button"
              type="button"
              disabled={isTracing || !selectedVersionId}
              onClick={handleCompareWithPrevious}
            >
              Comparar con version anterior
            </button>
            {diff ? (
              <pre className="diff-block">{diff.diff.join("\n")}</pre>
            ) : (
              <p className="muted">Crea al menos dos versiones de un mismo artefacto para comparar cambios.</p>
            )}
          </section>
        </section>

        <section className="history-layout">
          <section className="panel history-panel">
            <div className="list-header">
              <div>
                <p className="section-label">Historial</p>
                <h2>{versionHistory ? `Version ${versionHistory.version.version}` : "Sin version seleccionada"}</h2>
              </div>
              {selectedVersionStatus ? <span className="status-tag standalone">{selectedVersionStatus}</span> : null}
            </div>

            {versionHistory ? (
              <>
                <p className="muted">
                  Hash: {versionHistory.version.content_hash.slice(0, 16)}. Contenido inmutable registrado.
                </p>
                <div className="decision-actions">
                  {selectedVersionStatus === "draft" || selectedVersionStatus === "changes_requested" ? (
                    <button
                      className="ghost-button"
                      type="button"
                      disabled={isReviewing}
                      onClick={() => handleDecision("submit_for_review")}
                    >
                      Enviar a revision
                    </button>
                  ) : null}
                  {selectedVersionStatus === "in_review" ? (
                    <>
                      <button
                        className="ghost-button"
                        type="button"
                        disabled={isReviewing}
                        onClick={() => handleDecision("approve")}
                      >
                        Aprobar
                      </button>
                      <button
                        className="ghost-button"
                        type="button"
                        disabled={isReviewing}
                        onClick={() => handleDecision("request_changes")}
                      >
                        Pedir cambios
                      </button>
                      <button
                        className="ghost-button danger"
                        type="button"
                        disabled={isReviewing}
                        onClick={() => handleDecision("reject")}
                      >
                        Rechazar
                      </button>
                    </>
                  ) : null}
                  {selectedVersionStatus === "approved" ? (
                    <button
                      className="ghost-button"
                      type="button"
                      disabled={isReviewing}
                      onClick={() => handleDecision("publish")}
                    >
                      Publicar
                    </button>
                  ) : null}
                  {selectedVersionStatus !== "archived" ? (
                    <button
                      className="ghost-button"
                      type="button"
                      disabled={isReviewing}
                      onClick={() => handleDecision("archive")}
                    >
                      Archivar
                    </button>
                  ) : null}
                </div>
                <label>
                  Comentario de decision
                  <input id="review-comment" placeholder="Motivo de la decision" />
                </label>

                <div className="history-stack">
                  <h3>Decisiones</h3>
                  {versionHistory.decisions.length > 0 ? (
                    versionHistory.decisions.map((decision) => (
                      <article className="history-item" key={decision.id}>
                        <strong>{decision.action}</strong>
                        <p>
                          {decision.previous_status} {"->"} {decision.new_status} por {decision.reviewer}
                        </p>
                        {decision.comment ? <p>{decision.comment}</p> : null}
                      </article>
                    ))
                  ) : (
                    <p className="muted">Sin decisiones registradas.</p>
                  )}
                </div>
              </>
            ) : (
              <p className="muted">Selecciona una version para ver su historial.</p>
            )}
          </section>

          <form className="panel case-form" onSubmit={handleAddComment}>
            <p className="section-label">Comentario</p>
            <label>
              Autor
              <input name="author" placeholder="Supervisor humano" />
            </label>
            <label>
              Comentario
              <textarea name="comment" required rows={4} placeholder="Observacion sobre la version seleccionada" />
            </label>
            <button className="primary-button" type="submit" disabled={isReviewing || !selectedVersionId}>
              <Plus size={18} aria-hidden="true" />
              <span>Agregar comentario</span>
            </button>
            {reviewError ? <p className="form-error">{reviewError}</p> : null}
            {versionHistory?.comments.length ? (
              <div className="history-stack">
                <h3>Comentarios</h3>
                {versionHistory.comments.map((comment) => (
                  <article className="history-item" key={comment.id}>
                    <strong>{comment.author}</strong>
                    <p>{comment.comment}</p>
                  </article>
                ))}
              </div>
            ) : null}
          </form>
        </section>

        <section className="trace-layout">
          <form className="panel case-form" onSubmit={handleAddEvidence}>
            <p className="section-label">Evidencia</p>
            <label>
              Tipo
              <select name="evidence_type" defaultValue="interview">
                <option value="interview">Entrevista</option>
                <option value="document">Documento</option>
                <option value="event_log">Event log</option>
                <option value="process_mining">Process mining</option>
                <option value="bpmn_activity">Actividad BPMN</option>
                <option value="other">Otro</option>
              </select>
            </label>
            <label>
              Fuente
              <input name="source_title" required placeholder="Entrevista con Compras" />
            </label>
            <label>
              Actividad relacionada
              <input name="activity_ref" placeholder="Validar documentos" />
            </label>
            <label>
              Extracto
              <textarea name="excerpt" required rows={4} placeholder="Fragmento que respalda esta version" />
            </label>
            <label>
              Notas
              <textarea name="notes" rows={2} placeholder="Observaciones de trazabilidad" />
            </label>
            <button className="primary-button" type="submit" disabled={isTracing || !selectedVersionId}>
              <Plus size={18} aria-hidden="true" />
              <span>Vincular evidencia</span>
            </button>
          </form>

          <section className="panel history-panel">
            <div className="list-header">
              <div>
                <p className="section-label">Calidad</p>
                <h2>{quality ? `${quality.score}%` : "Sin evaluacion"}</h2>
              </div>
              {quality ? <span className="status-tag standalone">{quality.checks.filter((check) => check.passed).length}/4</span> : null}
            </div>
            {quality ? (
              <div className="history-stack">
                {quality.checks.map((check) => (
                  <article className="history-item" key={check.code}>
                    <strong>{check.passed ? "OK" : "Pendiente"} - {check.label}</strong>
                    <p>{check.detail}</p>
                  </article>
                ))}
              </div>
            ) : (
              <p className="muted">Selecciona una version para calcular su calidad documental.</p>
            )}

            <div className="history-stack">
              <h3>Evidencias vinculadas</h3>
              {evidence.length > 0 ? (
                evidence.map((item) => (
                  <article className="history-item" key={item.id}>
                    <strong>{item.source_title}</strong>
                    <p>{item.excerpt}</p>
                    {item.activity_ref ? <p>Actividad: {item.activity_ref}</p> : null}
                  </article>
                ))
              ) : (
                <p className="muted">No hay evidencias vinculadas a esta version.</p>
              )}
            </div>
          </section>
        </section>

        <section className="module-grid">
          {foundationItems.map((item) => {
            const Icon = item.icon;

            return (
              <article className="module-card" key={item.title}>
                <div className="icon-box">
                  <Icon size={22} aria-hidden="true" />
                </div>
                <h3>{item.title}</h3>
                <p>{item.text}</p>
              </article>
            );
          })}
        </section>
      </section>
    </main>
  );
}

function updateVersionStatus(
  artifacts: ProcessArtifact[],
  versionId: string,
  status: string,
): ProcessArtifact[] {
  return artifacts.map((artifact) => ({
    ...artifact,
    versions: artifact.versions.map((version) =>
      version.id === versionId ? { ...version, status } : version,
    ),
  }));
}
