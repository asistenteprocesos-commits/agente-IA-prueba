import {
  Activity,
  Bot,
  CheckCircle2,
  ClipboardList,
  Database,
  FileText,
  GitBranch,
  MessageSquare,
  Play,
  Plus,
  RotateCcw,
  Send,
  ShieldCheck,
  StepForward,
  Upload,
  Users,
  Workflow,
  Zap,
} from "lucide-react";
import { type FormEvent, useEffect, useState } from "react";

import {
  addArtifactEvidence,
  addOrchestrationContext,
  analyzeKnowledgeLibrary,
  advanceOrchestration,
  commentArtifactVersion,
  compareArtifactVersions,
  createProcessAnalysisReport,
  createAsIsElement,
  createArtifactVersion,
  createProcessInterview,
  createProcessArtifact,
  createProcessCase,
  createProcessRedesignReport,
  createProcessSimulationReport,
  createProcessStakeholder,
  createFinalDeliverable,
  decideOrchestrationCheckpoint,
  decideArtifactVersion,
  extractAsIsElements,
  generateAsIsBpmn,
  getAgentTrainingProfile,
  getDiscoveryAssessment,
  getCaseOrchestration,
  getInterviewGuide,
  getArtifactVersionHistory,
  getArtifactQuality,
  getHealth,
  getCaseMethodology,
  getFinalDeliverable,
  getProcessAnalysis,
  getProcessRedesign,
  getProcessRepository,
  getProcessSimulation,
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
  previewAsIsBpmn,
  rollbackOrchestration,
  startCaseOrchestration,
  uploadKnowledgeDocumentsBulk,
  // Chat
  createChatSession,
  listChatSessions,
  listChatMessages,
  sendChatMessage,
  getLLMSystemStatus,
  type AgentTrainingProfile,
  type ArtifactEvidence,
  type ArtifactQuality,
  type ArtifactVersionHistory,
  type BpmnDraft,
  type CaseMethodology,
  type ChatSession,
  type ChatMessage,
  type DiscoveryAssessment,
  type FinalDeliverable,
  type HealthResponse,
  type InterviewGuide,
  type KnowledgeChunk,
  type KnowledgeDocument,
  type KnowledgeInsight,
  type KnowledgeLearningRun,
  type LLMSystemStatus,
  type LocalLLMProfile,
  type OrchestrationState,
  type ProcessAsIsElement,
  type ProcessAnalysis,
  type ProcessArtifact,
  type ProcessCase,
  type ProcessInterview,
  type ProcessRepository,
  type ProcessRedesign,
  type ProcessSimulation,
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
  const [orchestration, setOrchestration] = useState<OrchestrationState | null>(null);
  const [learningRun, setLearningRun] = useState<KnowledgeLearningRun | null>(null);
  const [stakeholders, setStakeholders] = useState<ProcessStakeholder[]>([]);
  const [interviews, setInterviews] = useState<ProcessInterview[]>([]);
  const [interviewGuide, setInterviewGuide] = useState<InterviewGuide | null>(null);
  const [discoveryAssessment, setDiscoveryAssessment] = useState<DiscoveryAssessment | null>(null);
  const [asIsElements, setAsIsElements] = useState<ProcessAsIsElement[]>([]);
  const [bpmnDraft, setBpmnDraft] = useState<BpmnDraft | null>(null);
  const [processAnalysis, setProcessAnalysis] = useState<ProcessAnalysis | null>(null);
  const [processRedesign, setProcessRedesign] = useState<ProcessRedesign | null>(null);
  const [processSimulation, setProcessSimulation] = useState<ProcessSimulation | null>(null);
  const [finalDeliverable, setFinalDeliverable] = useState<FinalDeliverable | null>(null);
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
  const [bpmnError, setBpmnError] = useState<string | null>(null);
  const [bpmnMessage, setBpmnMessage] = useState<string | null>(null);
  const [analysisError, setAnalysisError] = useState<string | null>(null);
  const [analysisMessage, setAnalysisMessage] = useState<string | null>(null);
  const [redesignError, setRedesignError] = useState<string | null>(null);
  const [redesignMessage, setRedesignMessage] = useState<string | null>(null);
  const [simulationError, setSimulationError] = useState<string | null>(null);
  const [simulationMessage, setSimulationMessage] = useState<string | null>(null);
  const [deliverableError, setDeliverableError] = useState<string | null>(null);
  const [deliverableMessage, setDeliverableMessage] = useState<string | null>(null);
  const [orchestrationError, setOrchestrationError] = useState<string | null>(null);
  const [orchestrationMessage, setOrchestrationMessage] = useState<string | null>(null);
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
  const [isGeneratingBpmn, setIsGeneratingBpmn] = useState(false);
  const [isAnalyzingProcess, setIsAnalyzingProcess] = useState(false);
  const [isRedesigningProcess, setIsRedesigningProcess] = useState(false);
  const [isSimulatingProcess, setIsSimulatingProcess] = useState(false);
  const [isCreatingDeliverable, setIsCreatingDeliverable] = useState(false);
  const [isOrchestrating, setIsOrchestrating] = useState(false);
  const [isReviewing, setIsReviewing] = useState(false);
  const [isTracing, setIsTracing] = useState(false);

  // ── Chat state ───────────────────────────────────────────────────────────
  const [chatSessions, setChatSessions] = useState<ChatSession[]>([]);
  const [activeChatSessionId, setActiveChatSessionId] = useState<string | null>(null);
  const [chatMessages, setChatMessages] = useState<ChatMessage[]>([]);
  const [chatInput, setChatInput] = useState("");
  const [isSendingChat, setIsSendingChat] = useState(false);
  const [chatError, setChatError] = useState<string | null>(null);
  const [llmStatus, setLlmStatus] = useState<LLMSystemStatus | null>(null);

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
      setOrchestration(null);
      return;
    }

    let active = true;

    getCaseOrchestration(selectedCaseId)
      .then((data) => {
        if (active) {
          setOrchestration(data);
          setOrchestrationError(null);
          setOrchestrationMessage(data.next_action_es);
        }
      })
      .catch((reason: unknown) => {
        if (active) {
          setOrchestrationError(reason instanceof Error ? reason.message : "No se pudo cargar la orquestacion");
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
      setDiscoveryAssessment(null);
      setAsIsElements([]);
      setBpmnDraft(null);
      setProcessAnalysis(null);
      setProcessRedesign(null);
      setProcessSimulation(null);
      setFinalDeliverable(null);
      return;
    }

    let active = true;

    Promise.all([
      listProcessStakeholders(selectedCaseId),
      listProcessInterviews(selectedCaseId),
      getInterviewGuide(selectedCaseId),
      getDiscoveryAssessment(selectedCaseId),
      listAsIsElements(selectedCaseId),
      previewAsIsBpmn(selectedCaseId),
      getProcessAnalysis(selectedCaseId),
      getProcessRedesign(selectedCaseId),
      getProcessSimulation(selectedCaseId),
      getFinalDeliverable(selectedCaseId),
    ])
      .then(([stakeholderData, interviewData, guideData, assessmentData, elementData, bpmnData, analysisData, redesignData, simulationData, deliverableData]) => {
        if (active) {
          setStakeholders(stakeholderData);
          setInterviews(interviewData);
          setInterviewGuide(guideData);
          setDiscoveryAssessment(assessmentData);
          setAsIsElements(elementData);
          setBpmnDraft(bpmnData);
          setProcessAnalysis(analysisData);
          setProcessRedesign(redesignData);
          setProcessSimulation(simulationData);
          setFinalDeliverable(deliverableData);
          setDiscoveryError(null);
          setBpmnError(null);
          setAnalysisError(null);
          setRedesignError(null);
          setSimulationError(null);
          setDeliverableError(null);
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
      const assessment = await getDiscoveryAssessment(selectedCaseId);
      setStakeholders((current) => [created, ...current]);
      setDiscoveryAssessment(assessment);
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
      const assessment = await getDiscoveryAssessment(selectedCaseId);
      setInterviews((current) => [created, ...current]);
      setDiscoveryAssessment(assessment);
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
      const assessment = await getDiscoveryAssessment(selectedCaseId);
      const bpmn = await previewAsIsBpmn(selectedCaseId);
      const analysis = await getProcessAnalysis(selectedCaseId);
      const redesign = await getProcessRedesign(selectedCaseId);
      const simulation = await getProcessSimulation(selectedCaseId);
      const deliverable = await getFinalDeliverable(selectedCaseId);
      setAsIsElements((current) => [created, ...current]);
      setDiscoveryAssessment(assessment);
      setBpmnDraft(bpmn);
      setProcessAnalysis(analysis);
      setProcessRedesign(redesign);
      setProcessSimulation(simulation);
      setFinalDeliverable(deliverable);
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
      const assessment = await getDiscoveryAssessment(selectedCaseId);
      const bpmn = await previewAsIsBpmn(selectedCaseId);
      const analysis = await getProcessAnalysis(selectedCaseId);
      const redesign = await getProcessRedesign(selectedCaseId);
      const simulation = await getProcessSimulation(selectedCaseId);
      const deliverable = await getFinalDeliverable(selectedCaseId);
      setAsIsElements((current) => [...extracted, ...current]);
      setDiscoveryAssessment(assessment);
      setBpmnDraft(bpmn);
      setProcessAnalysis(analysis);
      setProcessRedesign(redesign);
      setProcessSimulation(simulation);
      setFinalDeliverable(deliverable);
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

  async function runOrchestrationCommand(command: () => Promise<OrchestrationState>) {
    if (!selectedCaseId) {
      setOrchestrationError("Selecciona un caso antes de operar el orquestador");
      return;
    }

    setIsOrchestrating(true);
    setOrchestrationError(null);
    setOrchestrationMessage(null);

    try {
      const state = await command();
      const refreshedCases = await listProcessCases();
      setOrchestration(state);
      setCases(refreshedCases);
      setOrchestrationMessage(state.next_action_es);
    } catch (reason) {
      setOrchestrationError(reason instanceof Error ? reason.message : "No se pudo operar la orquestacion");
    } finally {
      setIsOrchestrating(false);
    }
  }

  async function handleStartOrchestration() {
    if (!selectedCaseId) {
      return;
    }

    await runOrchestrationCommand(() => startCaseOrchestration(selectedCaseId));
  }

  async function handleAdvanceOrchestration() {
    if (!selectedCaseId) {
      return;
    }

    await runOrchestrationCommand(() => advanceOrchestration(selectedCaseId));
  }

  async function handleRollbackOrchestration() {
    if (!selectedCaseId) {
      return;
    }

    await runOrchestrationCommand(() => rollbackOrchestration(selectedCaseId));
  }

  async function handleCheckpointDecision(action: "approve" | "reject") {
    if (!selectedCaseId) {
      return;
    }

    const reviewerInput = document.getElementById("checkpoint-reviewer") as HTMLInputElement | null;
    const commentInput = document.getElementById("checkpoint-comment") as HTMLInputElement | null;
    const reviewer = reviewerInput?.value.trim() || "Supervisor BPM";
    const comment = commentInput?.value.trim() || undefined;

    await runOrchestrationCommand(() =>
      decideOrchestrationCheckpoint(selectedCaseId, {
        action,
        reviewer,
        comment,
      }),
    );
  }

  async function handleAddOrchestrationContext(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    if (!selectedCaseId) {
      setOrchestrationError("Selecciona un caso antes de agregar contexto");
      return;
    }

    const form = new FormData(event.currentTarget);
    const message = String(form.get("message_es") ?? "").trim();
    const actor = String(form.get("actor") ?? "Especialista BPM").trim() || "Especialista BPM";

    if (!message) {
      setOrchestrationError("Registra un contexto antes de guardar");
      return;
    }

    await runOrchestrationCommand(() =>
      addOrchestrationContext(selectedCaseId, {
        actor,
        message_es: message,
      }),
    );
    event.currentTarget.reset();
  }

  async function handleGenerateBpmn(persist: boolean) {
    if (!selectedCaseId) {
      setBpmnError("Selecciona un caso antes de generar BPMN");
      return;
    }

    setIsGeneratingBpmn(true);
    setBpmnError(null);
    setBpmnMessage(null);

    try {
      const draft = persist
        ? await generateAsIsBpmn(selectedCaseId, {
            title: "BPMN as-is generado por agente",
            author: "Agente Modelador BPMN",
            persist: true,
          })
        : await previewAsIsBpmn(selectedCaseId);
      const artifactData = await listProcessArtifacts(selectedCaseId);
      setBpmnDraft(draft);
      setArtifacts(artifactData);
      setBpmnMessage(
        persist
          ? "BPMN generado y guardado como artefacto versionado."
          : "Vista previa BPMN actualizada desde el inventario as-is.",
      );
    } catch (reason) {
      setBpmnError(reason instanceof Error ? reason.message : "No se pudo generar BPMN");
    } finally {
      setIsGeneratingBpmn(false);
    }
  }

  async function handleCreateAnalysisReport() {
    if (!selectedCaseId) {
      setAnalysisError("Selecciona un caso antes de generar analisis");
      return;
    }

    setIsAnalyzingProcess(true);
    setAnalysisError(null);
    setAnalysisMessage(null);

    try {
      const analysis = await createProcessAnalysisReport(selectedCaseId);
      const artifactData = await listProcessArtifacts(selectedCaseId);
      setProcessAnalysis(analysis);
      setArtifacts(artifactData);
      setAnalysisMessage("Analisis generado y guardado como reporte versionado.");
    } catch (reason) {
      setAnalysisError(reason instanceof Error ? reason.message : "No se pudo generar el analisis");
    } finally {
      setIsAnalyzingProcess(false);
    }
  }

  async function handleCreateRedesignReport() {
    if (!selectedCaseId) {
      setRedesignError("Selecciona un caso antes de generar to-be");
      return;
    }

    setIsRedesigningProcess(true);
    setRedesignError(null);
    setRedesignMessage(null);

    try {
      const redesign = await createProcessRedesignReport(selectedCaseId);
      const artifactData = await listProcessArtifacts(selectedCaseId);
      setProcessRedesign(redesign);
      setArtifacts(artifactData);
      setRedesignMessage("Propuesta to-be guardada como artefacto versionado.");
    } catch (reason) {
      setRedesignError(reason instanceof Error ? reason.message : "No se pudo generar la propuesta to-be");
    } finally {
      setIsRedesigningProcess(false);
    }
  }

  async function handleCreateSimulationReport() {
    if (!selectedCaseId) {
      setSimulationError("Selecciona un caso antes de simular");
      return;
    }

    setIsSimulatingProcess(true);
    setSimulationError(null);
    setSimulationMessage(null);

    try {
      const simulation = await createProcessSimulationReport(selectedCaseId);
      const artifactData = await listProcessArtifacts(selectedCaseId);
      setProcessSimulation(simulation);
      setArtifacts(artifactData);
      setSimulationMessage("Simulacion guardada como artefacto versionado.");
    } catch (reason) {
      setSimulationError(reason instanceof Error ? reason.message : "No se pudo generar la simulacion");
    } finally {
      setIsSimulatingProcess(false);
    }
  }

  async function handleCreateFinalDeliverable() {
    if (!selectedCaseId) {
      setDeliverableError("Selecciona un caso antes de generar informe final");
      return;
    }

    setIsCreatingDeliverable(true);
    setDeliverableError(null);
    setDeliverableMessage(null);

    try {
      const deliverable = await createFinalDeliverable(selectedCaseId);
      const artifactData = await listProcessArtifacts(selectedCaseId);
      setFinalDeliverable(deliverable);
      setArtifacts(artifactData);
      setDeliverableMessage("Informe final guardado como artefacto versionado.");
    } catch (reason) {
      setDeliverableError(reason instanceof Error ? reason.message : "No se pudo generar el informe final");
    } finally {
      setIsCreatingDeliverable(false);
    }
  }

  // ── Chat Handlers ─────────────────────────────────────────────────────────

  useEffect(() => {
    let active = true;
    listChatSessions().then((data) => {
      if (active) setChatSessions(data);
    }).catch(console.error);

    getLLMSystemStatus().then((data) => {
      if (active) setLlmStatus(data);
    }).catch(console.error);

    return () => { active = false; };
  }, []);

  async function handleNewChatSession() {
    try {
      const session = await createChatSession({ case_id: selectedCaseId || undefined });
      setChatSessions(prev => [session, ...prev]);
      setActiveChatSessionId(session.id);
      setChatMessages([]);
      setChatError(null);
    } catch (err) {
      setChatError("No se pudo crear la sesión de chat.");
    }
  }

  async function handleSelectChatSession(sessionId: string) {
    setActiveChatSessionId(sessionId);
    setChatError(null);
    try {
      const messages = await listChatMessages(sessionId);
      setChatMessages(messages);
    } catch (err) {
      setChatError("No se pudieron cargar los mensajes.");
    }
  }

  async function handleSendChat(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!chatInput.trim() || !activeChatSessionId) return;

    const inputMsg = chatInput;
    setChatInput("");
    setIsSendingChat(true);
    setChatError(null);

    // Optimistic user message
    const tempId = `temp-${Date.now()}`;
    setChatMessages(prev => [...prev, {
      id: tempId,
      session_id: activeChatSessionId,
      role: "user",
      content: inputMsg,
      llm_provider: null,
      llm_model: null,
      rag_fragments_used: null,
      normalized_terms: null,
      agent_task: null,
      created_at: new Date().toISOString()
    }]);

    try {
      await sendChatMessage(activeChatSessionId, { content: inputMsg });
      // Reload messages to get the real user message and assistant reply
      const messages = await listChatMessages(activeChatSessionId);
      setChatMessages(messages);
    } catch (err) {
      setChatError("Error al enviar el mensaje. Inténtalo de nuevo.");
      setChatInput(inputMsg); // Restore input
      // Remove temp message
      setChatMessages(prev => prev.filter(m => m.id !== tempId));
    } finally {
      setIsSendingChat(false);
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
          <a className="nav-item" href="#orquestacion">
            Orquestacion
          </a>
          <a className="nav-item" href="#levantamiento">
            Levantamiento
          </a>
          <a className="nav-item" href="#asis">
            As-is
          </a>
          <a className="nav-item" href="#bpmn">
            BPMN
          </a>
          <a className="nav-item" href="#chat-panel">
            Agente Chat
          </a>
          <a className="nav-item" href="#analisis">
            Analisis
          </a>
          <a className="nav-item" href="#tobe">
            To-be
          </a>
          <a className="nav-item" href="#simulacion">
            Simulacion
          </a>
          <a className="nav-item" href="#entregables">
            Entregables
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

        <section className="orchestration-layout" id="orquestacion">
          <section className="panel orchestration-panel">
            <div className="list-header">
              <div>
                <p className="section-label">FASE 1.B</p>
                <h2>Orquestador autonomo</h2>
              </div>
              <Workflow size={30} aria-hidden="true" />
            </div>

            {orchestration ? (
              <>
                <div className="progress-block">
                  <div>
                    <strong>{orchestration.autonomy_progress_percent}%</strong>
                    <span>{orchestration.run.status}</span>
                  </div>
                  <div className="progress-track" aria-hidden="true">
                    <span style={{ width: `${orchestration.autonomy_progress_percent}%` }} />
                  </div>
                </div>

                <p className="muted">{orchestrationMessage ?? orchestration.next_action_es}</p>

                {orchestration.blockers_es.length > 0 ? (
                  <div className="blocker-stack">
                    {orchestration.blockers_es.map((blocker) => (
                      <p key={blocker}>{blocker}</p>
                    ))}
                  </div>
                ) : null}

                <div className="orchestration-actions">
                  <button
                    className="primary-button"
                    type="button"
                    disabled={isOrchestrating || !selectedCaseId || orchestration.run.status !== "not_started"}
                    onClick={handleStartOrchestration}
                  >
                    <Play size={18} aria-hidden="true" />
                    <span>Iniciar</span>
                  </button>
                  <button
                    className="ghost-button"
                    type="button"
                    disabled={
                      isOrchestrating ||
                      !selectedCaseId ||
                      orchestration.run.status === "completed" ||
                      orchestration.run.status === "waiting_human"
                    }
                    onClick={handleAdvanceOrchestration}
                  >
                    <StepForward size={16} aria-hidden="true" />
                    Avanzar
                  </button>
                  <button
                    className="ghost-button"
                    type="button"
                    disabled={isOrchestrating || !selectedCaseId || orchestration.run.status !== "waiting_human"}
                    onClick={() => handleCheckpointDecision("approve")}
                  >
                    <CheckCircle2 size={16} aria-hidden="true" />
                    Aprobar checkpoint
                  </button>
                  <button
                    className="ghost-button danger"
                    type="button"
                    disabled={isOrchestrating || !selectedCaseId || orchestration.run.status === "not_started"}
                    onClick={handleRollbackOrchestration}
                  >
                    <RotateCcw size={16} aria-hidden="true" />
                    Rollback
                  </button>
                </div>

                <div className="checkpoint-grid">
                  <label>
                    Supervisor
                    <input id="checkpoint-reviewer" defaultValue="Supervisor BPM" />
                  </label>
                  <label>
                    Comentario
                    <input id="checkpoint-comment" placeholder="Decision, condicion o evidencia requerida" />
                  </label>
                </div>

                <form className="case-form context-form" onSubmit={handleAddOrchestrationContext}>
                  <label>
                    Actor
                    <input name="actor" defaultValue="Especialista BPM" />
                  </label>
                  <label>
                    Contexto compartido
                    <textarea
                      name="message_es"
                      rows={3}
                      placeholder="Decision, supuesto, restriccion o hallazgo que debe viajar entre fases"
                    />
                  </label>
                  <button className="ghost-button" type="submit" disabled={isOrchestrating || !selectedCaseId}>
                    Registrar contexto
                  </button>
                </form>

                {orchestrationError ? <p className="form-error">{orchestrationError}</p> : null}
              </>
            ) : (
              <p className="muted">Selecciona un caso para activar el backbone de orquestacion.</p>
            )}
          </section>

          <section className="panel orchestration-panel">
            <div className="list-header">
              <div>
                <p className="section-label">Maquina de estados</p>
                <h2>8 fases del ciclo BPM</h2>
              </div>
              {orchestration ? (
                <span className="status-tag standalone">
                  Fase {orchestration.run.current_phase_number}
                </span>
              ) : null}
            </div>

            {orchestration ? (
              <>
                <div className="phase-list">
                  {orchestration.phases.map((phase) => (
                    <article className={`phase-item ${phase.status}`} key={phase.id}>
                      <div className="phase-number">{phase.phase_number}</div>
                      <div>
                        <div className="phase-title-row">
                          <h3>{phase.title}</h3>
                          <span>{phase.status}</span>
                        </div>
                        <p>{phase.objective_es}</p>
                        <div className="case-meta">
                          <span>{phase.agent_role}</span>
                          <span>{phase.checkpoint_status}</span>
                          {phase.requires_human_checkpoint ? <span>checkpoint</span> : <span>automatico</span>}
                        </div>
                      </div>
                    </article>
                  ))}
                </div>

                <div className="event-list">
                  <h3>Eventos recientes</h3>
                  {orchestration.events.slice(0, 5).map((event) => (
                    <article className="history-item" key={event.id}>
                      <strong>
                        {event.event_type}
                        {event.phase_number ? ` - fase ${event.phase_number}` : ""}
                      </strong>
                      <p>{event.message_es}</p>
                    </article>
                  ))}
                </div>
              </>
            ) : (
              <p className="muted">La secuencia se genera al seleccionar un caso.</p>
            )}
          </section>
        </section>

        <section className="panel discovery-agent-panel" id="levantamiento">
          <div className="list-header">
            <div>
              <p className="section-label">Agente Levantador</p>
              <h2>Completitud y preguntas inteligentes</h2>
            </div>
            {discoveryAssessment ? (
              <span className="status-tag standalone">{discoveryAssessment.readiness_level}</span>
            ) : null}
          </div>

          {discoveryAssessment ? (
            <>
              <div className="assessment-summary">
                <div className="progress-block compact-progress">
                  <div>
                    <strong>{discoveryAssessment.completeness_score}%</strong>
                    <span>as-is</span>
                  </div>
                  <div className="progress-track" aria-hidden="true">
                    <span style={{ width: `${discoveryAssessment.completeness_score}%` }} />
                  </div>
                </div>
                <div className="case-meta">
                  <span>{discoveryAssessment.gaps.length} vacios</span>
                  <span>{discoveryAssessment.contradictions.length} contradicciones</span>
                  <span>{discoveryAssessment.generated_questions.length} preguntas</span>
                </div>
              </div>

              <div className="assessment-grid">
                <div className="history-stack">
                  <h3>Dimensiones</h3>
                  {discoveryAssessment.dimensions.map((dimension) => (
                    <article className="history-item" key={dimension.code}>
                      <strong>
                        {dimension.label_es} - {dimension.score}/{dimension.max_score}
                      </strong>
                      <p>{dimension.detail_es}</p>
                    </article>
                  ))}
                </div>

                <div className="history-stack">
                  <h3>Preguntas sugeridas</h3>
                  {discoveryAssessment.generated_questions.slice(0, 5).map((question) => (
                    <article className="history-item" key={`${question.role}-${question.question_es}`}>
                      <strong>
                        {question.priority} - {question.role}
                      </strong>
                      <p>{question.question_es}</p>
                      <p>{question.expected_evidence_es}</p>
                    </article>
                  ))}
                </div>

                <div className="history-stack">
                  <h3>Vacios principales</h3>
                  {discoveryAssessment.gaps.slice(0, 5).map((gap) => (
                    <article className="history-item" key={gap.code}>
                      <strong>
                        {gap.severity} - {gap.title_es}
                      </strong>
                      <p>{gap.recommendation_es}</p>
                    </article>
                  ))}
                  {discoveryAssessment.gaps.length === 0 ? <p className="muted">No hay vacios detectados.</p> : null}
                </div>

                <div className="history-stack">
                  <h3>Contradicciones</h3>
                  {discoveryAssessment.contradictions.slice(0, 4).map((contradiction) => (
                    <article className="history-item" key={contradiction.topic}>
                      <strong>{contradiction.topic}</strong>
                      <p>{contradiction.recommendation_es}</p>
                    </article>
                  ))}
                  {discoveryAssessment.contradictions.length === 0 ? (
                    <p className="muted">No hay contradicciones detectadas.</p>
                  ) : null}
                </div>
              </div>

              <div className="next-actions">
                {discoveryAssessment.next_actions_es.map((action) => (
                  <p key={action}>{action}</p>
                ))}
              </div>
            </>
          ) : (
            <p className="muted">Selecciona un caso para que el agente levante brechas y preguntas.</p>
          )}
        </section>

        <section className="discovery-layout">
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

        <section className="bpmn-layout" id="bpmn">
          <section className="panel bpmn-panel">
            <div className="list-header">
              <div>
                <p className="section-label">Agente Modelador BPMN</p>
                <h2>BPMN as-is inicial</h2>
              </div>
              {bpmnDraft ? (
                <span className="status-tag standalone">{bpmnDraft.is_valid ? "valido" : "con errores"}</span>
              ) : null}
            </div>

            {bpmnDraft ? (
              <>
                <div className="case-meta">
                  <span>{bpmnDraft.source_element_count} elementos fuente</span>
                  <span>{bpmnDraft.task_count} tareas</span>
                  <span>{bpmnDraft.gateway_count} gateways</span>
                  <span>{bpmnDraft.issues.length} hallazgos</span>
                </div>
                <div className="orchestration-actions">
                  <button
                    className="ghost-button"
                    type="button"
                    disabled={isGeneratingBpmn || !selectedCaseId}
                    onClick={() => handleGenerateBpmn(false)}
                  >
                    Vista previa
                  </button>
                  <button
                    className="primary-button"
                    type="button"
                    disabled={isGeneratingBpmn || !selectedCaseId}
                    onClick={() => handleGenerateBpmn(true)}
                  >
                    <GitBranch size={18} aria-hidden="true" />
                    <span>Guardar BPMN</span>
                  </button>
                </div>
                {bpmnMessage ? <p className="success-note">{bpmnMessage}</p> : null}
                {bpmnError ? <p className="form-error">{bpmnError}</p> : null}
                <pre className="bpmn-xml-preview">{bpmnDraft.bpmn_xml}</pre>
              </>
            ) : (
              <p className="muted">Selecciona un caso para generar el modelo BPMN desde el inventario as-is.</p>
            )}
          </section>

          <section className="panel bpmn-panel">
            <div className="list-header">
              <div>
                <p className="section-label">Validacion BPMN</p>
                <h2>Checklist tecnico</h2>
              </div>
            </div>
            {bpmnDraft ? (
              <div className="history-stack">
                {bpmnDraft.issues.map((issue) => (
                  <article className="history-item" key={`${issue.code}-${issue.element_ref ?? "global"}`}>
                    <strong>
                      {issue.severity} - {issue.code}
                    </strong>
                    <p>{issue.message_es}</p>
                    {issue.element_ref ? <p>Elemento: {issue.element_ref}</p> : null}
                  </article>
                ))}
              </div>
            ) : (
              <p className="muted">La validacion aparecera cuando exista un borrador BPMN.</p>
            )}
          </section>
        </section>

        <section className="analysis-layout" id="analisis">
          <section className="panel analysis-panel">
            <div className="list-header">
              <div>
                <p className="section-label">Agente Analista</p>
                <h2>Hallazgos y mejora</h2>
              </div>
              {processAnalysis ? (
                <span className="status-tag standalone">{processAnalysis.analysis_score}%</span>
              ) : null}
            </div>
            {processAnalysis ? (
              <>
                <div className="case-meta">
                  <span>{processAnalysis.findings.length} hallazgos</span>
                  <span>{processAnalysis.metrics.length} metricas</span>
                  <span>{processAnalysis.risks_controls.length} riesgos</span>
                  <span>{processAnalysis.improvement_candidates.length} mejoras</span>
                </div>
                <button
                  className="primary-button"
                  type="button"
                  disabled={isAnalyzingProcess || !selectedCaseId}
                  onClick={handleCreateAnalysisReport}
                >
                  <FileText size={18} aria-hidden="true" />
                  <span>Guardar analisis</span>
                </button>
                {analysisMessage ? <p className="success-note">{analysisMessage}</p> : null}
                {analysisError ? <p className="form-error">{analysisError}</p> : null}
                <div className="history-stack">
                  {processAnalysis.findings.slice(0, 6).map((finding) => (
                    <article className="history-item" key={`${finding.finding_type}-${finding.title_es}`}>
                      <strong>
                        {finding.severity} - {finding.title_es}
                      </strong>
                      <p>{finding.detail_es}</p>
                      <p>{finding.recommendation_es}</p>
                    </article>
                  ))}
                </div>
              </>
            ) : (
              <p className="muted">Selecciona un caso para analizar hallazgos, riesgos y oportunidades.</p>
            )}
          </section>

          <section className="panel analysis-panel">
            <div className="list-header">
              <div>
                <p className="section-label">Metricas y candidatos</p>
                <h2>Base cuantitativa</h2>
              </div>
            </div>
            {processAnalysis ? (
              <>
                <div className="history-stack">
                  <h3>Metricas detectadas</h3>
                  {processAnalysis.metrics.slice(0, 4).map((metric) => (
                    <article className="history-item" key={`${metric.name_es}-${metric.source_es}`}>
                      <strong>
                        {metric.name_es}: {metric.value ?? "pendiente"} {metric.unit ?? ""}
                      </strong>
                      <p>{metric.interpretation_es}</p>
                    </article>
                  ))}
                </div>
                <div className="history-stack">
                  <h3>Mejoras candidatas</h3>
                  {processAnalysis.improvement_candidates.slice(0, 4).map((item) => (
                    <article className="history-item" key={item.title_es}>
                      <strong>{item.title_es}</strong>
                      <p>{item.impact_es}</p>
                      <p>{item.effort_es}</p>
                    </article>
                  ))}
                </div>
              </>
            ) : (
              <p className="muted">El analisis aparecera cuando exista inventario as-is.</p>
            )}
          </section>
        </section>

        <section className="redesign-layout" id="tobe">
          <section className="panel redesign-panel">
            <div className="list-header">
              <div>
                <p className="section-label">Agente Rediseñador</p>
                <h2>Alternativas to-be</h2>
              </div>
              {processRedesign ? (
                <span className="status-tag standalone">{processRedesign.alternatives.length}</span>
              ) : null}
            </div>
            {processRedesign ? (
              <>
                <p className="muted">
                  Recomendacion: {processRedesign.comparison.recommended_option_title_es}.{" "}
                  {processRedesign.comparison.rationale_es}
                </p>
                <button
                  className="primary-button"
                  type="button"
                  disabled={isRedesigningProcess || !selectedCaseId}
                  onClick={handleCreateRedesignReport}
                >
                  <FileText size={18} aria-hidden="true" />
                  <span>Guardar to-be</span>
                </button>
                {redesignMessage ? <p className="success-note">{redesignMessage}</p> : null}
                {redesignError ? <p className="form-error">{redesignError}</p> : null}
                <div className="history-stack">
                  {processRedesign.alternatives.map((alternative) => (
                    <article className="history-item" key={alternative.title_es}>
                      <strong>
                        {alternative.option_type} - {alternative.title_es}
                      </strong>
                      <p>{alternative.description_es}</p>
                      <p>{alternative.expected_impact_es}</p>
                    </article>
                  ))}
                </div>
              </>
            ) : (
              <p className="muted">El to-be aparecera cuando exista analisis del proceso.</p>
            )}
          </section>

          <section className="panel redesign-panel">
            <div className="list-header">
              <div>
                <p className="section-label">Validacion requerida</p>
                <h2>Cambios y supuestos</h2>
              </div>
            </div>
            {processRedesign ? (
              <div className="history-stack">
                {processRedesign.alternatives.slice(0, 3).map((alternative) => (
                  <article className="history-item" key={`${alternative.title_es}-changes`}>
                    <strong>{alternative.title_es}</strong>
                    <p>Cambios: {alternative.changes_es.join("; ")}</p>
                    <p>Validar: {alternative.required_validation_es.join("; ")}</p>
                  </article>
                ))}
              </div>
            ) : (
              <p className="muted">Las validaciones apareceran con las alternativas to-be.</p>
            )}
          </section>
        </section>

        <section className="simulation-layout" id="simulacion">
          <section className="panel simulation-panel">
            <div className="list-header">
              <div>
                <p className="section-label">Agente Simulador</p>
                <h2>Escenarios iniciales</h2>
              </div>
              {processSimulation ? (
                <span className="status-tag standalone">
                  -{processSimulation.comparison.cycle_time_reduction_percent}%
                </span>
              ) : null}
            </div>
            {processSimulation ? (
              <>
                <p className="muted">
                  Recomendado: {processSimulation.comparison.recommended_scenario_es}.{" "}
                  {processSimulation.comparison.interpretation_es}
                </p>
                <button
                  className="primary-button"
                  type="button"
                  disabled={isSimulatingProcess || !selectedCaseId}
                  onClick={handleCreateSimulationReport}
                >
                  <FileText size={18} aria-hidden="true" />
                  <span>Guardar simulacion</span>
                </button>
                {simulationMessage ? <p className="success-note">{simulationMessage}</p> : null}
                {simulationError ? <p className="form-error">{simulationError}</p> : null}
                <div className="history-stack">
                  {processSimulation.scenarios.map((scenario) => (
                    <article className="history-item" key={scenario.name_es}>
                      <strong>{scenario.name_es}</strong>
                      <p>
                        Ciclo: {scenario.cycle_time_hours}h | Esfuerzo: {scenario.manual_effort_hours}h | Costo indice:{" "}
                        {scenario.cost_index}
                      </p>
                      <p>Riesgo SLA: {scenario.sla_risk}</p>
                    </article>
                  ))}
                </div>
              </>
            ) : (
              <p className="muted">La simulacion aparecera cuando existan alternativas to-be.</p>
            )}
          </section>

          <section className="panel simulation-panel">
            <div className="list-header">
              <div>
                <p className="section-label">Sensibilidad</p>
                <h2>Supuestos clave</h2>
              </div>
            </div>
            {processSimulation ? (
              <div className="history-stack">
                {processSimulation.sensitivity.map((point) => (
                  <article className="history-item" key={point.variable_es}>
                    <strong>{point.variable_es}</strong>
                    <p>{point.base_case_es}</p>
                    <p>{point.high_case_es}</p>
                  </article>
                ))}
              </div>
            ) : (
              <p className="muted">Los supuestos se muestran junto con la simulacion.</p>
            )}
          </section>
        </section>

        <section className="deliverable-layout" id="entregables">
          <section className="panel deliverable-panel">
            <div className="list-header">
              <div>
                <p className="section-label">Agente Redactor</p>
                <h2>Informe final</h2>
              </div>
              {finalDeliverable ? <span className="status-tag standalone">final</span> : null}
            </div>
            {finalDeliverable ? (
              <>
                <p className="muted">{finalDeliverable.executive_summary_es}</p>
                <p className="muted">{finalDeliverable.technical_summary_es}</p>
                <button
                  className="primary-button"
                  type="button"
                  disabled={isCreatingDeliverable || !selectedCaseId}
                  onClick={handleCreateFinalDeliverable}
                >
                  <FileText size={18} aria-hidden="true" />
                  <span>Guardar informe</span>
                </button>
                {deliverableMessage ? <p className="success-note">{deliverableMessage}</p> : null}
                {deliverableError ? <p className="form-error">{deliverableError}</p> : null}
              </>
            ) : (
              <p className="muted">El informe final aparecera cuando exista analisis, to-be y simulacion.</p>
            )}
          </section>

          <section className="panel deliverable-panel">
            <div className="list-header">
              <div>
                <p className="section-label">Plan</p>
                <h2>Implementacion</h2>
              </div>
            </div>
            {finalDeliverable ? (
              <div className="history-stack">
                {finalDeliverable.implementation_plan.map((step) => (
                  <article className="history-item" key={step.order}>
                    <strong>
                      {step.order}. {step.title_es}
                    </strong>
                    <p>
                      {step.timeframe_es} - {step.owner_es}
                    </p>
                    <p>{step.deliverable_es}</p>
                  </article>
                ))}
              </div>
            ) : (
              <p className="muted">El plan se genera junto con el informe final.</p>
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

      {/* ══════════════════════════════════════════════════════════════
          PANEL CHAT — Agente BPMS
      ══════════════════════════════════════════════════════════════ */}
      <section className="section" id="chat-panel" aria-labelledby="chat-heading">
        <header className="section-header">
          <div className="header-badge">
            <MessageSquare size={18} aria-hidden="true" />
            <span>Agente BPMS</span>
          </div>
          <h2 id="chat-heading">Chat con el Agente Experto</h2>
          <p className="section-desc">
            Consulta al agente sobre BPM, AS-IS, TO-BE, BPMN, metodologías y más.
            Las respuestas usan RAG sobre tu base de conocimiento.
          </p>
        </header>

        {/* LLM Status bar */}
        {llmStatus && (
          <div className="llm-status-bar">
            <span className="llm-badge">
              <Zap size={13} />
              Proveedor activo: <strong>{llmStatus.active_provider}</strong>
            </span>
            <span className={`llm-badge ${llmStatus.ollama_available ? "ok" : "warn"}`}>
              Ollama: {llmStatus.ollama_available ? "✓ disponible" : "✗ no disponible (normal en esta PC)"}
            </span>
            {llmStatus.providers.map((p) => (
              <span key={p.provider} className={`llm-chip ${p.available ? "ok" : "off"}`}>
                {p.provider.split(" ")[0]}: {p.available ? "✓" : "✗"}
              </span>
            ))}
          </div>
        )}

        <div className="chat-layout">
          {/* Sidebar: sesiones */}
          <aside className="chat-sidebar">
            <div className="chat-sidebar-header">
              <h3>Conversaciones</h3>
              <button
                id="new-chat-session-btn"
                className="btn-icon"
                onClick={() => handleNewChatSession()}
                title="Nueva conversación"
              >
                <Plus size={16} />
              </button>
            </div>
            {chatSessions.length === 0 && (
              <p className="chat-empty-hint">Sin conversaciones. Crea una nueva.</p>
            )}
            <ul className="chat-session-list">
              {chatSessions.map((s) => (
                <li
                  key={s.id}
                  className={`chat-session-item ${s.id === activeChatSessionId ? "active" : ""}`}
                  onClick={() => handleSelectChatSession(s.id)}
                >
                  <MessageSquare size={14} />
                  <span>{s.title}</span>
                </li>
              ))}
            </ul>
          </aside>

          {/* Main chat area */}
          <div className="chat-main">
            {!activeChatSessionId ? (
              <div className="chat-welcome">
                <Bot size={48} className="chat-welcome-icon" />
                <h3>Agente BPMS listo</h3>
                <p>Crea una nueva conversación o selecciona una existente para comenzar.</p>
                <button id="start-chat-btn" className="btn-primary" onClick={() => handleNewChatSession()}>
                  <Plus size={16} /> Nueva conversación
                </button>
              </div>
            ) : (
              <>
                <div className="chat-messages" id="chat-messages-container">
                  {chatMessages.length === 0 && (
                    <div className="chat-welcome-inline">
                      <Bot size={32} />
                      <p>¿En qué proceso puedo ayudarte hoy?</p>
                    </div>
                  )}
                  {chatMessages.map((msg) => (
                    <div key={msg.id} className={`chat-bubble ${msg.role}`}>
                      <div className="chat-bubble-content">
                        <pre className="chat-text">{msg.content}</pre>
                      </div>
                      {msg.role === "assistant" && (
                        <div className="chat-meta">
                          {msg.llm_provider && (
                            <span className="chat-tag">
                              <Zap size={11} /> {msg.llm_provider}
                            </span>
                          )}
                          {msg.agent_task && (
                            <span className="chat-tag">
                              <Activity size={11} /> {msg.agent_task}
                            </span>
                          )}
                          {msg.rag_fragments_used != null && msg.rag_fragments_used > 0 && (
                            <span className="chat-tag">
                              <Database size={11} /> {msg.rag_fragments_used} fuente(s) RAG
                            </span>
                          )}
                          {msg.normalized_terms && (
                            <span className="chat-tag">
                              <CheckCircle2 size={11} /> {msg.normalized_terms}
                            </span>
                          )}
                        </div>
                      )}
                    </div>
                  ))}
                  {isSendingChat && (
                    <div className="chat-bubble assistant thinking">
                      <div className="chat-bubble-content">
                        <span className="typing-dot" />
                        <span className="typing-dot" />
                        <span className="typing-dot" />
                      </div>
                    </div>
                  )}
                </div>

                {chatError && <p className="error-msg">{chatError}</p>}

                <form className="chat-input-bar" onSubmit={handleSendChat}>
                  <textarea
                    id="chat-input-field"
                    className="chat-textarea"
                    value={chatInput}
                    onChange={(e) => setChatInput(e.target.value)}
                    onKeyDown={(e) => {
                      if (e.key === "Enter" && !e.shiftKey) {
                        e.preventDefault();
                        void handleSendChat(e as unknown as FormEvent<HTMLFormElement>);
                      }
                    }}
                    placeholder="Escribe tu consulta BPM aquí... (Enter para enviar, Shift+Enter nueva línea)"
                    rows={3}
                    disabled={isSendingChat}
                  />
                  <button
                    id="send-chat-btn"
                    type="submit"
                    className="btn-send"
                    disabled={isSendingChat || !chatInput.trim()}
                    title="Enviar mensaje"
                  >
                    <Send size={18} />
                  </button>
                </form>
              </>
            )}
          </div>
        </div>
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

