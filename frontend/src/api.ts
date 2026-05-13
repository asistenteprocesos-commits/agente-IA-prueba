export type HealthResponse = {
  status: string;
  service: string;
  version: string;
  environment: string;
};

export type ProcessCase = {
  id: string;
  name: string;
  area: string | null;
  objective: string | null;
  scope: string | null;
  owner: string | null;
  status: string;
  created_at: string;
  updated_at: string;
};

export type ProcessCaseCreate = {
  name: string;
  area?: string;
  objective?: string;
  scope?: string;
  owner?: string;
};

export type ProcessRepository = {
  id: string;
  case_id: string;
  name: string;
  artifact_count: number;
  created_at: string;
  updated_at: string;
};

export type ArtifactVersion = {
  id: string;
  artifact_id: string;
  version: string;
  status: string;
  content: string;
  change_summary: string | null;
  author: string | null;
  content_hash: string;
  created_at: string;
};

export type ArtifactDecision = {
  id: string;
  version_id: string;
  action: string;
  previous_status: string;
  new_status: string;
  reviewer: string;
  comment: string | null;
  created_at: string;
};

export type ArtifactComment = {
  id: string;
  version_id: string;
  author: string;
  comment: string;
  created_at: string;
};

export type ArtifactVersionHistory = {
  version: ArtifactVersion;
  decisions: ArtifactDecision[];
  comments: ArtifactComment[];
};

export type ArtifactEvidence = {
  id: string;
  version_id: string;
  evidence_type: string;
  source_title: string;
  excerpt: string;
  activity_ref: string | null;
  source_url: string | null;
  notes: string | null;
  created_at: string;
};

export type VersionDiff = {
  base_version_id: string;
  target_version_id: string;
  base_version: string;
  target_version: string;
  added_lines: number;
  removed_lines: number;
  diff: string[];
};

export type QualityCheck = {
  code: string;
  label: string;
  passed: boolean;
  detail: string;
};

export type ArtifactQuality = {
  version_id: string;
  score: number;
  checks: QualityCheck[];
};

export type ProcessArtifact = {
  id: string;
  repository_id: string;
  artifact_type: string;
  title: string;
  description: string | null;
  current_version_id: string | null;
  created_at: string;
  updated_at: string;
  versions: ArtifactVersion[];
};

export type ProcessArtifactCreate = {
  artifact_type: string;
  title: string;
  description?: string;
  content: string;
  version?: string;
  change_summary?: string;
  author?: string;
};

export type ArtifactDecisionCreate = {
  action: string;
  reviewer: string;
  comment?: string;
};

export type ArtifactCommentCreate = {
  author: string;
  comment: string;
};

export type ArtifactVersionCreate = {
  content: string;
  version: string;
  change_summary?: string;
  author?: string;
};

export type ArtifactEvidenceCreate = {
  evidence_type: string;
  source_title: string;
  excerpt: string;
  activity_ref?: string;
  source_url?: string;
  notes?: string;
};

export type KnowledgeDocument = {
  id: string;
  title: string;
  author: string | null;
  source_type: string;
  subject_area: string | null;
  language: string;
  case_id: string | null;
  filename: string;
  mime_type: string | null;
  status: string;
  error_message: string | null;
  text_char_count: number;
  chunk_count: number;
  created_at: string;
  updated_at: string;
};

export type KnowledgeChunk = {
  id: string;
  document_id: string;
  chunk_index: number;
  content: string;
  char_start: number;
  char_end: number;
  created_at: string;
};

export type ProcessStakeholder = {
  id: string;
  case_id: string;
  name: string;
  role: string;
  area: string | null;
  email: string | null;
  influence_level: string;
  availability: string | null;
  notes: string | null;
  created_at: string;
  updated_at: string;
};

export type ProcessStakeholderCreate = {
  name: string;
  role: string;
  area?: string;
  email?: string;
  influence_level: string;
  availability?: string;
  notes?: string;
};

export type ProcessInterview = {
  id: string;
  case_id: string;
  stakeholder_id: string | null;
  stakeholder_name: string | null;
  title: string;
  interview_type: string;
  status: string;
  scheduled_at: string | null;
  objective: string | null;
  questions: string | null;
  notes: string | null;
  summary: string | null;
  created_at: string;
  updated_at: string;
};

export type ProcessInterviewCreate = {
  stakeholder_id?: string;
  title: string;
  interview_type: string;
  status: string;
  scheduled_at?: string;
  objective?: string;
  questions?: string;
  notes?: string;
  summary?: string;
};

export type InterviewGuideSection = {
  title: string;
  questions: string[];
};

export type InterviewGuide = {
  case_id: string;
  title: string;
  sections: InterviewGuideSection[];
};

export type ProcessAsIsElement = {
  id: string;
  case_id: string;
  interview_id: string | null;
  interview_title: string | null;
  element_type: string;
  name: string;
  description: string | null;
  source_excerpt: string | null;
  confidence_level: string;
  created_by: string;
  created_at: string;
  updated_at: string;
};

export type ProcessAsIsElementCreate = {
  interview_id?: string;
  element_type: string;
  name: string;
  description?: string;
  source_excerpt?: string;
  confidence_level: string;
  created_by?: string;
};

export type KnowledgeInsight = {
  id: string;
  document_id: string;
  chunk_id: string;
  insight_type: string;
  topic: string;
  title_es: string;
  summary_es: string;
  source_excerpt: string;
  source_language: string;
  confidence_level: string;
  created_by: string;
  created_at: string;
};

export type KnowledgeLearningRun = {
  analyzed_documents: number;
  created_insights: number;
  total_insights: number;
};

export type CaseMethodologyPhase = {
  phase: string;
  objective_es: string;
  actions_es: string[];
  outputs_es: string[];
  quality_checks_es: string[];
  related_topics: string[];
  source_insight_count: number;
};

export type CaseMethodology = {
  title: string;
  language: string;
  source_insight_count: number;
  phases: CaseMethodologyPhase[];
};

export type AgentTrainingArtifact = {
  name: string;
  kind: string;
  path: string;
  exists: boolean;
  size_bytes: number | null;
};

export type AgentTrainingProfile = {
  profile_name: string;
  training_mode: string;
  language: string;
  books_processed: number;
  pages_processed: number;
  extracted_characters: number;
  insights: number;
  methodology_phases: number;
  dataset_examples: number;
  graph_is_visual: boolean;
  obsidian_vault_path: string;
  obsidian_canvas_path: string;
  artifacts: AgentTrainingArtifact[];
  limitations: string[];
  next_step: string;
};

export type LocalLLMModel = {
  role: string;
  model: string;
  purpose_es: string;
  required: boolean;
  installed: boolean;
};

export type LocalLLMProfile = {
  provider: string;
  runtime: string;
  base_url: string;
  runtime_installed: boolean;
  server_available: boolean;
  reasoning_model: string;
  embedding_model: string;
  pulled_models: string[];
  recommended_models: LocalLLMModel[];
  learning_strategy_es: string[];
  machine_learning_strategy_es: string[];
  install_commands: string[];
  next_actions_es: string[];
};

const apiBaseUrl = import.meta.env.VITE_API_BASE_URL ?? "http://127.0.0.1:8000";

export async function getHealth(): Promise<HealthResponse> {
  const response = await fetch(`${apiBaseUrl}/api/health`);

  if (!response.ok) {
    throw new Error(`Backend health check failed with ${response.status}`);
  }

  return response.json() as Promise<HealthResponse>;
}

export async function listProcessCases(): Promise<ProcessCase[]> {
  const response = await fetch(`${apiBaseUrl}/api/process-cases`);

  if (!response.ok) {
    throw new Error(`Process cases request failed with ${response.status}`);
  }

  return response.json() as Promise<ProcessCase[]>;
}

export async function createProcessCase(payload: ProcessCaseCreate): Promise<ProcessCase> {
  const response = await fetch(`${apiBaseUrl}/api/process-cases`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    throw new Error(`Process case creation failed with ${response.status}`);
  }

  return response.json() as Promise<ProcessCase>;
}

export async function getProcessRepository(caseId: string): Promise<ProcessRepository> {
  const response = await fetch(`${apiBaseUrl}/api/process-cases/${caseId}/repository`);

  if (!response.ok) {
    throw new Error(`Process repository request failed with ${response.status}`);
  }

  return response.json() as Promise<ProcessRepository>;
}

export async function listProcessArtifacts(caseId: string): Promise<ProcessArtifact[]> {
  const response = await fetch(`${apiBaseUrl}/api/process-cases/${caseId}/repository/artifacts`);

  if (!response.ok) {
    throw new Error(`Process artifacts request failed with ${response.status}`);
  }

  return response.json() as Promise<ProcessArtifact[]>;
}

export async function createProcessArtifact(
  caseId: string,
  payload: ProcessArtifactCreate,
): Promise<ProcessArtifact> {
  const response = await fetch(`${apiBaseUrl}/api/process-cases/${caseId}/repository/artifacts`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    throw new Error(`Process artifact creation failed with ${response.status}`);
  }

  return response.json() as Promise<ProcessArtifact>;
}

export async function createArtifactVersion(
  caseId: string,
  artifactId: string,
  payload: ArtifactVersionCreate,
): Promise<ArtifactVersion> {
  const response = await fetch(
    `${apiBaseUrl}/api/process-cases/${caseId}/repository/artifacts/${artifactId}/versions`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    },
  );

  if (!response.ok) {
    throw new Error(`Artifact version creation failed with ${response.status}`);
  }

  return response.json() as Promise<ArtifactVersion>;
}

export async function decideArtifactVersion(
  caseId: string,
  versionId: string,
  payload: ArtifactDecisionCreate,
): Promise<ArtifactDecision> {
  const response = await fetch(
    `${apiBaseUrl}/api/process-cases/${caseId}/repository/artifact-versions/${versionId}/decisions`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    },
  );

  if (!response.ok) {
    throw new Error(`Artifact version decision failed with ${response.status}`);
  }

  return response.json() as Promise<ArtifactDecision>;
}

export async function commentArtifactVersion(
  caseId: string,
  versionId: string,
  payload: ArtifactCommentCreate,
): Promise<ArtifactComment> {
  const response = await fetch(
    `${apiBaseUrl}/api/process-cases/${caseId}/repository/artifact-versions/${versionId}/comments`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    },
  );

  if (!response.ok) {
    throw new Error(`Artifact version comment failed with ${response.status}`);
  }

  return response.json() as Promise<ArtifactComment>;
}

export async function getArtifactVersionHistory(
  caseId: string,
  versionId: string,
): Promise<ArtifactVersionHistory> {
  const response = await fetch(
    `${apiBaseUrl}/api/process-cases/${caseId}/repository/artifact-versions/${versionId}/history`,
  );

  if (!response.ok) {
    throw new Error(`Artifact version history request failed with ${response.status}`);
  }

  return response.json() as Promise<ArtifactVersionHistory>;
}

export async function compareArtifactVersions(
  caseId: string,
  baseVersionId: string,
  targetVersionId: string,
): Promise<VersionDiff> {
  const response = await fetch(
    `${apiBaseUrl}/api/process-cases/${caseId}/repository/artifact-versions/${baseVersionId}/diff/${targetVersionId}`,
  );

  if (!response.ok) {
    throw new Error(`Artifact version diff request failed with ${response.status}`);
  }

  return response.json() as Promise<VersionDiff>;
}

export async function listArtifactEvidence(
  caseId: string,
  versionId: string,
): Promise<ArtifactEvidence[]> {
  const response = await fetch(
    `${apiBaseUrl}/api/process-cases/${caseId}/repository/artifact-versions/${versionId}/evidence`,
  );

  if (!response.ok) {
    throw new Error(`Artifact evidence request failed with ${response.status}`);
  }

  return response.json() as Promise<ArtifactEvidence[]>;
}

export async function addArtifactEvidence(
  caseId: string,
  versionId: string,
  payload: ArtifactEvidenceCreate,
): Promise<ArtifactEvidence> {
  const response = await fetch(
    `${apiBaseUrl}/api/process-cases/${caseId}/repository/artifact-versions/${versionId}/evidence`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    },
  );

  if (!response.ok) {
    throw new Error(`Artifact evidence creation failed with ${response.status}`);
  }

  return response.json() as Promise<ArtifactEvidence>;
}

export async function getArtifactQuality(caseId: string, versionId: string): Promise<ArtifactQuality> {
  const response = await fetch(
    `${apiBaseUrl}/api/process-cases/${caseId}/repository/artifact-versions/${versionId}/quality`,
  );

  if (!response.ok) {
    throw new Error(`Artifact quality request failed with ${response.status}`);
  }

  return response.json() as Promise<ArtifactQuality>;
}

export async function listKnowledgeDocuments(caseId?: string): Promise<KnowledgeDocument[]> {
  const query = caseId ? `?case_id=${encodeURIComponent(caseId)}` : "";
  const response = await fetch(`${apiBaseUrl}/api/knowledge/documents${query}`);

  if (!response.ok) {
    throw new Error(`Knowledge documents request failed with ${response.status}`);
  }

  return response.json() as Promise<KnowledgeDocument[]>;
}

export async function uploadKnowledgeDocument(payload: FormData): Promise<KnowledgeDocument> {
  const response = await fetch(`${apiBaseUrl}/api/knowledge/documents`, {
    method: "POST",
    body: payload,
  });

  if (!response.ok) {
    throw new Error(`Knowledge document upload failed with ${response.status}`);
  }

  return response.json() as Promise<KnowledgeDocument>;
}

export async function uploadKnowledgeDocumentsBulk(payload: FormData): Promise<KnowledgeDocument[]> {
  const response = await fetch(`${apiBaseUrl}/api/knowledge/documents/bulk`, {
    method: "POST",
    body: payload,
  });

  if (!response.ok) {
    throw new Error(`Knowledge documents bulk upload failed with ${response.status}`);
  }

  return response.json() as Promise<KnowledgeDocument[]>;
}

export async function listKnowledgeChunks(documentId: string): Promise<KnowledgeChunk[]> {
  const response = await fetch(`${apiBaseUrl}/api/knowledge/documents/${documentId}/chunks`);

  if (!response.ok) {
    throw new Error(`Knowledge chunks request failed with ${response.status}`);
  }

  return response.json() as Promise<KnowledgeChunk[]>;
}

export async function analyzeKnowledgeLibrary(): Promise<KnowledgeLearningRun> {
  const response = await fetch(`${apiBaseUrl}/api/knowledge/learning/analyze`, {
    method: "POST",
  });

  if (!response.ok) {
    throw new Error(`Knowledge library analysis failed with ${response.status}`);
  }

  return response.json() as Promise<KnowledgeLearningRun>;
}

export async function listKnowledgeInsights(): Promise<KnowledgeInsight[]> {
  const response = await fetch(`${apiBaseUrl}/api/knowledge/insights`);

  if (!response.ok) {
    throw new Error(`Knowledge insights request failed with ${response.status}`);
  }

  return response.json() as Promise<KnowledgeInsight[]>;
}

export async function getCaseMethodology(): Promise<CaseMethodology> {
  const response = await fetch(`${apiBaseUrl}/api/knowledge/case-methodology`);

  if (!response.ok) {
    throw new Error(`Case methodology request failed with ${response.status}`);
  }

  return response.json() as Promise<CaseMethodology>;
}

export async function getAgentTrainingProfile(): Promise<AgentTrainingProfile> {
  const response = await fetch(`${apiBaseUrl}/api/knowledge/agent-training-profile`);

  if (!response.ok) {
    throw new Error(`Agent training profile request failed with ${response.status}`);
  }

  return response.json() as Promise<AgentTrainingProfile>;
}

export async function getLocalLLMProfile(): Promise<LocalLLMProfile> {
  const response = await fetch(`${apiBaseUrl}/api/local-llm/profile`);

  if (!response.ok) {
    throw new Error(`Local LLM profile request failed with ${response.status}`);
  }

  return response.json() as Promise<LocalLLMProfile>;
}

export async function listProcessStakeholders(caseId: string): Promise<ProcessStakeholder[]> {
  const response = await fetch(`${apiBaseUrl}/api/process-cases/${caseId}/discovery/stakeholders`);

  if (!response.ok) {
    throw new Error(`Process stakeholders request failed with ${response.status}`);
  }

  return response.json() as Promise<ProcessStakeholder[]>;
}

export async function createProcessStakeholder(
  caseId: string,
  payload: ProcessStakeholderCreate,
): Promise<ProcessStakeholder> {
  const response = await fetch(`${apiBaseUrl}/api/process-cases/${caseId}/discovery/stakeholders`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    throw new Error(`Process stakeholder creation failed with ${response.status}`);
  }

  return response.json() as Promise<ProcessStakeholder>;
}

export async function listProcessInterviews(caseId: string): Promise<ProcessInterview[]> {
  const response = await fetch(`${apiBaseUrl}/api/process-cases/${caseId}/discovery/interviews`);

  if (!response.ok) {
    throw new Error(`Process interviews request failed with ${response.status}`);
  }

  return response.json() as Promise<ProcessInterview[]>;
}

export async function createProcessInterview(
  caseId: string,
  payload: ProcessInterviewCreate,
): Promise<ProcessInterview> {
  const response = await fetch(`${apiBaseUrl}/api/process-cases/${caseId}/discovery/interviews`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    throw new Error(`Process interview creation failed with ${response.status}`);
  }

  return response.json() as Promise<ProcessInterview>;
}

export async function getInterviewGuide(caseId: string): Promise<InterviewGuide> {
  const response = await fetch(`${apiBaseUrl}/api/process-cases/${caseId}/discovery/interview-guide`);

  if (!response.ok) {
    throw new Error(`Interview guide request failed with ${response.status}`);
  }

  return response.json() as Promise<InterviewGuide>;
}

export async function listAsIsElements(caseId: string): Promise<ProcessAsIsElement[]> {
  const response = await fetch(`${apiBaseUrl}/api/process-cases/${caseId}/discovery/as-is-elements`);

  if (!response.ok) {
    throw new Error(`As-is elements request failed with ${response.status}`);
  }

  return response.json() as Promise<ProcessAsIsElement[]>;
}

export async function createAsIsElement(
  caseId: string,
  payload: ProcessAsIsElementCreate,
): Promise<ProcessAsIsElement> {
  const response = await fetch(`${apiBaseUrl}/api/process-cases/${caseId}/discovery/as-is-elements`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    throw new Error(`As-is element creation failed with ${response.status}`);
  }

  return response.json() as Promise<ProcessAsIsElement>;
}

export async function extractAsIsElements(
  caseId: string,
  interviewId: string,
): Promise<ProcessAsIsElement[]> {
  const response = await fetch(
    `${apiBaseUrl}/api/process-cases/${caseId}/discovery/interviews/${interviewId}/extract-as-is`,
    {
      method: "POST",
    },
  );

  if (!response.ok) {
    throw new Error(`As-is extraction failed with ${response.status}`);
  }

  return response.json() as Promise<ProcessAsIsElement[]>;
}
