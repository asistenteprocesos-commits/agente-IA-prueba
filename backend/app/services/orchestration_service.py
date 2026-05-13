import json
from dataclasses import dataclass
from datetime import UTC, datetime
from uuid import UUID, uuid4

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models.orchestration import (
    OrchestrationEventModel,
    OrchestrationPhaseModel,
    OrchestrationRunModel,
)
from app.models.process_case import ProcessCaseModel
from app.schemas.orchestration import (
    CheckpointAction,
    CheckpointDecisionCreate,
    CheckpointStatus,
    OrchestrationContextCreate,
    OrchestrationEventResponse,
    OrchestrationEventType,
    OrchestrationPhaseResponse,
    OrchestrationPhaseStatus,
    OrchestrationRunResponse,
    OrchestrationRunStatus,
    OrchestrationStateResponse,
)
from app.schemas.process_case import ProcessCaseStatus


class OrchestrationTransitionError(ValueError):
    pass


@dataclass(frozen=True)
class PhaseDefinition:
    number: int
    key: str
    title: str
    agent_role: str
    objective_es: str
    expected_outputs_es: tuple[str, ...]
    quality_checks_es: tuple[str, ...]
    requires_human_checkpoint: bool
    case_status: ProcessCaseStatus


PHASES: tuple[PhaseDefinition, ...] = (
    PhaseDefinition(
        number=1,
        key="preparar_alcance",
        title="Preparar alcance y conocimiento",
        agent_role="coordinador",
        objective_es="Definir objetivo, alcance, fuentes, restricciones y criterio de exito del caso.",
        expected_outputs_es=(
            "Caso de proceso con alcance inicial",
            "Fuentes y restricciones identificadas",
            "Criterios de supervision humana",
        ),
        quality_checks_es=(
            "Inicio y fin del proceso estan delimitados",
            "Responsable principal definido",
            "Riesgos de privacidad y alcance registrados",
        ),
        requires_human_checkpoint=True,
        case_status=ProcessCaseStatus.knowledge_loading,
    ),
    PhaseDefinition(
        number=2,
        key="levantar_as_is",
        title="Levantar as-is",
        agent_role="levantador",
        objective_es="Recolectar informacion del proceso actual con entrevistas, talleres y evidencia documental.",
        expected_outputs_es=(
            "Stakeholders registrados",
            "Entrevistas o notas de levantamiento",
            "Evidencias iniciales vinculadas",
        ),
        quality_checks_es=(
            "Se cubren roles, actividades, reglas, sistemas y excepciones",
            "Cada afirmacion critica tiene fuente",
            "Contradicciones quedan marcadas para validacion",
        ),
        requires_human_checkpoint=True,
        case_status=ProcessCaseStatus.discovery,
    ),
    PhaseDefinition(
        number=3,
        key="estructurar_elementos",
        title="Estructurar elementos as-is",
        agent_role="levantador",
        objective_es="Convertir notas y fuentes en elementos normalizados del proceso actual.",
        expected_outputs_es=(
            "Inventario as-is de actividades, eventos, reglas y excepciones",
            "Mapa inicial de dolores, controles y metricas",
        ),
        quality_checks_es=(
            "Elementos duplicados o ambiguos revisados",
            "Confianza y fuente registradas por elemento",
        ),
        requires_human_checkpoint=False,
        case_status=ProcessCaseStatus.as_is_drafting,
    ),
    PhaseDefinition(
        number=4,
        key="modelar_bpmn",
        title="Modelar BPMN as-is",
        agent_role="modelador_bpmn",
        objective_es="Transformar el inventario validado en un modelo BPMN entendible y revisable.",
        expected_outputs_es=(
            "BPMN XML as-is",
            "Narrativa as-is versionada",
            "Comentarios y evidencias por actividad",
        ),
        quality_checks_es=(
            "Eventos de inicio y fin claros",
            "Gateways con condiciones explicitas",
            "Modelo alineado con evidencia del levantamiento",
        ),
        requires_human_checkpoint=True,
        case_status=ProcessCaseStatus.bpmn_drafting,
    ),
    PhaseDefinition(
        number=5,
        key="analizar_datos",
        title="Analizar datos y performance",
        agent_role="analista",
        objective_es="Complementar el as-is con metricas, logs y hallazgos cuantitativos.",
        expected_outputs_es=(
            "Indicadores del as-is",
            "Hallazgos de variantes, tiempos, colas o cuellos",
            "Brechas de datos identificadas",
        ),
        quality_checks_es=(
            "Metricas tienen definicion y fuente",
            "Se separa evidencia de inferencia",
            "Hallazgos cuantitativos tienen confianza declarada",
        ),
        requires_human_checkpoint=True,
        case_status=ProcessCaseStatus.event_log_analysis,
    ),
    PhaseDefinition(
        number=6,
        key="identificar_mejoras",
        title="Identificar mejoras y riesgos",
        agent_role="redisenador",
        objective_es="Detectar oportunidades de simplificacion, automatizacion, control y transformacion digital.",
        expected_outputs_es=(
            "Matriz de hallazgos",
            "Mapa de riesgos y controles",
            "Backlog de oportunidades priorizado",
        ),
        quality_checks_es=(
            "Cada recomendacion tiene fuente, impacto y esfuerzo",
            "No se elimina un control sin control alternativo",
            "Se distinguen quick wins de cambios estructurales",
        ),
        requires_human_checkpoint=True,
        case_status=ProcessCaseStatus.improvement_analysis,
    ),
    PhaseDefinition(
        number=7,
        key="disenar_to_be_simular",
        title="Disenar to-be y simular",
        agent_role="simulador",
        objective_es="Construir alternativas futuras, estimar impacto y validarlas con las areas involucradas.",
        expected_outputs_es=(
            "BPMN to-be",
            "Escenarios de simulacion",
            "Supuestos y sensibilidad",
        ),
        quality_checks_es=(
            "Supuestos documentados y versionados",
            "Cambios de rol y sistema validados",
            "Escenario recomendado justificado con datos",
        ),
        requires_human_checkpoint=True,
        case_status=ProcessCaseStatus.repository_review,
    ),
    PhaseDefinition(
        number=8,
        key="cerrar_presentar",
        title="Cerrar y presentar",
        agent_role="redactor",
        objective_es="Versionar, aprobar y presentar entregables profesionales para decision y ejecucion.",
        expected_outputs_es=(
            "Informe ejecutivo",
            "Informe tecnico",
            "BPMN y plan de implementacion aprobados",
        ),
        quality_checks_es=(
            "Entregables tienen version aprobada",
            "Decision final basada en evidencia",
            "Responsables y proximos pasos claros",
        ),
        requires_human_checkpoint=True,
        case_status=ProcessCaseStatus.human_review,
    ),
)

PHASE_BY_NUMBER = {phase.number: phase for phase in PHASES}
MAX_PHASE = len(PHASES)


class OrchestrationService:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_or_create_state(self, case_id: UUID) -> OrchestrationStateResponse | None:
        process_case = self._get_case(case_id)
        if process_case is None:
            return None

        run = self._get_run(case_id)
        if run is None:
            run = self._create_run(process_case)
            self.db.commit()
            self.db.refresh(run)

        return self._state_response(run)

    def start(self, case_id: UUID) -> OrchestrationStateResponse | None:
        process_case = self._get_case(case_id)
        if process_case is None:
            return None

        run = self._get_run(case_id) or self._create_run(process_case)
        if run.status in {OrchestrationRunStatus.running.value, OrchestrationRunStatus.waiting_human.value}:
            return self._state_response(run)
        if run.status == OrchestrationRunStatus.completed.value:
            raise OrchestrationTransitionError("El orquestador ya esta completado para este caso")

        run.status = OrchestrationRunStatus.running.value
        run.current_phase_number = 1
        self._start_phase(run, 1)
        self._update_case_status(process_case, 1)
        self._add_event(
            run,
            OrchestrationEventType.run_started,
            "orchestrator",
            "Orquestador iniciado. Fase 1 queda en ejecucion.",
            phase_number=1,
        )
        self.db.commit()
        self.db.refresh(run)
        return self._state_response(run)

    def advance(self, case_id: UUID) -> OrchestrationStateResponse | None:
        process_case = self._get_case(case_id)
        if process_case is None:
            return None

        run = self._get_run(case_id)
        if run is None:
            raise OrchestrationTransitionError("Primero debes iniciar el orquestador")
        if run.status == OrchestrationRunStatus.completed.value:
            return self._state_response(run)
        if run.status == OrchestrationRunStatus.waiting_human.value:
            raise OrchestrationTransitionError("Hay un checkpoint humano pendiente")

        current_phase = self._current_phase(run)
        if current_phase is None:
            raise OrchestrationTransitionError("No hay fase actual para avanzar")
        if current_phase.status == OrchestrationPhaseStatus.pending.value:
            self._start_phase(run, current_phase.phase_number)
            self.db.commit()
            self.db.refresh(run)
            return self._state_response(run)

        if (
            self._bool(current_phase.requires_human_checkpoint)
            and current_phase.checkpoint_status == CheckpointStatus.pending.value
        ):
            current_phase.status = OrchestrationPhaseStatus.blocked_checkpoint.value
            run.status = OrchestrationRunStatus.waiting_human.value
            self._add_event(
                run,
                OrchestrationEventType.checkpoint_requested,
                "orchestrator",
                f"Checkpoint humano solicitado para la fase {current_phase.phase_number}: {current_phase.title}.",
                phase_number=current_phase.phase_number,
            )
            self.db.commit()
            self.db.refresh(run)
            return self._state_response(run)

        if current_phase.checkpoint_status == CheckpointStatus.rejected.value:
            raise OrchestrationTransitionError("El checkpoint fue rechazado; ajusta el trabajo o ejecuta rollback")

        self._complete_phase(run, current_phase)
        next_number = current_phase.phase_number + 1
        if next_number > MAX_PHASE:
            run.status = OrchestrationRunStatus.completed.value
            process_case.status = ProcessCaseStatus.closed.value
            self._add_event(
                run,
                OrchestrationEventType.run_completed,
                "orchestrator",
                "El ciclo completo del agente BPM quedo completado para este caso.",
            )
        else:
            run.current_phase_number = next_number
            run.status = OrchestrationRunStatus.running.value
            self._start_phase(run, next_number)
            self._update_case_status(process_case, next_number)
            self._add_event(
                run,
                OrchestrationEventType.handoff_created,
                "orchestrator",
                f"Contexto transferido desde fase {current_phase.phase_number} hacia fase {next_number}.",
                phase_number=next_number,
                payload={"from_phase": current_phase.phase_key, "to_phase": PHASE_BY_NUMBER[next_number].key},
            )

        self.db.commit()
        self.db.refresh(run)
        return self._state_response(run)

    def decide_checkpoint(
        self,
        case_id: UUID,
        payload: CheckpointDecisionCreate,
    ) -> OrchestrationStateResponse | None:
        process_case = self._get_case(case_id)
        if process_case is None:
            return None

        run = self._get_run(case_id)
        if run is None:
            raise OrchestrationTransitionError("No existe orquestador para este caso")

        phase = self._current_phase(run)
        if phase is None or phase.status != OrchestrationPhaseStatus.blocked_checkpoint.value:
            raise OrchestrationTransitionError("No hay checkpoint bloqueado para decidir")

        if payload.action == CheckpointAction.approve:
            phase.checkpoint_status = CheckpointStatus.approved.value
            phase.status = OrchestrationPhaseStatus.in_progress.value
            run.status = OrchestrationRunStatus.running.value
            message = f"Checkpoint aprobado por {payload.reviewer}. La fase puede avanzar."
        else:
            phase.checkpoint_status = CheckpointStatus.rejected.value
            phase.status = OrchestrationPhaseStatus.error.value
            run.status = OrchestrationRunStatus.error.value
            run.last_error = "Checkpoint humano rechazado"
            message = f"Checkpoint rechazado por {payload.reviewer}. Requiere correccion o rollback."

        phase.checkpoint_reviewer = payload.reviewer
        phase.checkpoint_comment = payload.comment
        self._add_event(
            run,
            OrchestrationEventType.checkpoint_decision,
            payload.reviewer,
            message,
            phase_number=phase.phase_number,
            payload={"action": payload.action.value, "comment": payload.comment},
        )
        self.db.commit()
        self.db.refresh(run)
        return self._state_response(run)

    def rollback(self, case_id: UUID) -> OrchestrationStateResponse | None:
        process_case = self._get_case(case_id)
        if process_case is None:
            return None

        run = self._get_run(case_id)
        if run is None:
            raise OrchestrationTransitionError("No existe orquestador para este caso")

        current_phase = self._current_phase(run)
        target_number = max(1, run.current_phase_number - 1)
        target_phase = self._phase(run, target_number)
        if target_phase is None:
            raise OrchestrationTransitionError("No se encontro la fase destino del rollback")

        if current_phase and current_phase.phase_number != target_number:
            current_phase.status = OrchestrationPhaseStatus.pending.value
            current_phase.started_at = None
            current_phase.completed_at = None
            current_phase.checkpoint_status = (
                CheckpointStatus.pending.value
                if self._bool(current_phase.requires_human_checkpoint)
                else CheckpointStatus.not_required.value
            )
            current_phase.checkpoint_reviewer = None
            current_phase.checkpoint_comment = None

        target_phase.status = OrchestrationPhaseStatus.in_progress.value
        target_phase.completed_at = None
        target_phase.started_at = target_phase.started_at or datetime.now(UTC)
        if target_phase.checkpoint_status == CheckpointStatus.approved.value:
            target_phase.checkpoint_status = (
                CheckpointStatus.pending.value
                if self._bool(target_phase.requires_human_checkpoint)
                else CheckpointStatus.not_required.value
            )
        run.current_phase_number = target_number
        run.status = OrchestrationRunStatus.running.value
        run.last_error = None
        self._update_case_status(process_case, target_number)
        self._add_event(
            run,
            OrchestrationEventType.rollback,
            "orchestrator",
            f"Rollback ejecutado hacia la fase {target_number}: {target_phase.title}.",
            phase_number=target_number,
        )
        self.db.commit()
        self.db.refresh(run)
        return self._state_response(run)

    def add_context(
        self,
        case_id: UUID,
        payload: OrchestrationContextCreate,
    ) -> OrchestrationStateResponse | None:
        process_case = self._get_case(case_id)
        if process_case is None:
            return None

        run = self._get_run(case_id) or self._create_run(process_case)
        phase_number = run.current_phase_number if run.status != OrchestrationRunStatus.not_started.value else None
        run.context_summary = self._append_context(run.context_summary, payload.message_es)
        self._add_event(
            run,
            OrchestrationEventType.context_added,
            payload.actor,
            payload.message_es,
            phase_number=phase_number,
            payload=payload.payload,
        )
        self.db.commit()
        self.db.refresh(run)
        return self._state_response(run)

    def _create_run(self, process_case: ProcessCaseModel) -> OrchestrationRunModel:
        run = OrchestrationRunModel(
            id=str(uuid4()),
            case_id=process_case.id,
            status=OrchestrationRunStatus.not_started.value,
            current_phase_number=1,
        )
        run.phases = [
            OrchestrationPhaseModel(
                id=str(uuid4()),
                run_id=run.id,
                phase_number=phase.number,
                phase_key=phase.key,
                title=phase.title,
                agent_role=phase.agent_role,
                objective_es=phase.objective_es,
                expected_outputs_es=json.dumps(list(phase.expected_outputs_es), ensure_ascii=True),
                quality_checks_es=json.dumps(list(phase.quality_checks_es), ensure_ascii=True),
                status=OrchestrationPhaseStatus.pending.value,
                requires_human_checkpoint=str(phase.requires_human_checkpoint).lower(),
                checkpoint_status=(
                    CheckpointStatus.pending.value
                    if phase.requires_human_checkpoint
                    else CheckpointStatus.not_required.value
                ),
            )
            for phase in PHASES
        ]
        self.db.add(run)
        self._add_event(
            run,
            OrchestrationEventType.run_created,
            "orchestrator",
            "Backbone de orquestacion creado con 8 fases y checkpoints humanos.",
        )
        return run

    def _start_phase(self, run: OrchestrationRunModel, phase_number: int) -> None:
        phase = self._phase(run, phase_number)
        if phase is None:
            raise OrchestrationTransitionError("Fase no encontrada")
        phase.status = OrchestrationPhaseStatus.in_progress.value
        phase.started_at = phase.started_at or datetime.now(UTC)
        phase.completed_at = None
        run.current_phase_number = phase_number
        self._add_event(
            run,
            OrchestrationEventType.phase_started,
            "orchestrator",
            f"Fase {phase.phase_number} iniciada: {phase.title}. Agente responsable: {phase.agent_role}.",
            phase_number=phase.phase_number,
            payload={"agent_role": phase.agent_role, "phase_key": phase.phase_key},
        )

    def _complete_phase(self, run: OrchestrationRunModel, phase: OrchestrationPhaseModel) -> None:
        phase.status = OrchestrationPhaseStatus.completed.value
        phase.completed_at = datetime.now(UTC)
        self._add_event(
            run,
            OrchestrationEventType.phase_completed,
            "orchestrator",
            f"Fase {phase.phase_number} completada: {phase.title}.",
            phase_number=phase.phase_number,
        )

    def _update_case_status(self, process_case: ProcessCaseModel, phase_number: int) -> None:
        process_case.status = PHASE_BY_NUMBER[phase_number].case_status.value

    def _state_response(self, run: OrchestrationRunModel) -> OrchestrationStateResponse:
        phases = sorted(run.phases, key=lambda item: item.phase_number)
        events = sorted(run.events, key=lambda item: item.created_at, reverse=True)
        completed = sum(1 for phase in phases if phase.status == OrchestrationPhaseStatus.completed.value)
        blockers = self._blockers(run)
        return OrchestrationStateResponse(
            run=self._run_to_response(run),
            phases=[self._phase_to_response(phase) for phase in phases],
            events=[self._event_to_response(event) for event in events[:25]],
            next_action_es=self._next_action(run, blockers),
            blockers_es=blockers,
            autonomy_progress_percent=round((completed / MAX_PHASE) * 100),
        )

    def _blockers(self, run: OrchestrationRunModel) -> list[str]:
        phase = self._current_phase(run)
        if phase is None:
            return []
        if run.status == OrchestrationRunStatus.waiting_human.value:
            return [f"Checkpoint humano pendiente en fase {phase.phase_number}: {phase.title}"]
        if run.status == OrchestrationRunStatus.error.value:
            return [run.last_error or "El orquestador esta en error"]
        return []

    def _next_action(self, run: OrchestrationRunModel, blockers: list[str]) -> str:
        if run.status == OrchestrationRunStatus.not_started.value:
            return "Iniciar orquestador para activar la fase 1."
        if run.status == OrchestrationRunStatus.completed.value:
            return "Caso completado. Revisar entregables finales y cierre."
        if blockers:
            return "Resolver el bloqueo antes de continuar."

        phase = self._current_phase(run)
        if phase and self._bool(phase.requires_human_checkpoint) and phase.checkpoint_status == CheckpointStatus.pending.value:
            return "Avanzar solicitara checkpoint humano para esta fase."
        return "Avanzar a la siguiente transicion del ciclo autonomo."

    def _get_case(self, case_id: UUID) -> ProcessCaseModel | None:
        return self.db.get(ProcessCaseModel, str(case_id))

    def _get_run(self, case_id: UUID) -> OrchestrationRunModel | None:
        statement = (
            select(OrchestrationRunModel)
            .where(OrchestrationRunModel.case_id == str(case_id))
            .options(
                selectinload(OrchestrationRunModel.phases),
                selectinload(OrchestrationRunModel.events),
            )
        )
        return self.db.scalars(statement).first()

    def _current_phase(self, run: OrchestrationRunModel) -> OrchestrationPhaseModel | None:
        return self._phase(run, run.current_phase_number)

    @staticmethod
    def _phase(run: OrchestrationRunModel, phase_number: int) -> OrchestrationPhaseModel | None:
        return next((phase for phase in run.phases if phase.phase_number == phase_number), None)

    def _add_event(
        self,
        run: OrchestrationRunModel,
        event_type: OrchestrationEventType,
        actor: str,
        message_es: str,
        phase_number: int | None = None,
        payload: dict[str, object] | None = None,
    ) -> None:
        run.events.append(
            OrchestrationEventModel(
                id=str(uuid4()),
                run_id=run.id,
                phase_number=phase_number,
                event_type=event_type.value,
                actor=actor,
                message_es=message_es,
                payload_json=json.dumps(payload, ensure_ascii=True) if payload else None,
            )
        )

    @staticmethod
    def _append_context(existing: str | None, message: str) -> str:
        lines = [line for line in (existing or "").splitlines() if line.strip()]
        lines.append(f"- {message.strip()}")
        return "\n".join(lines[-20:])

    @staticmethod
    def _bool(value: str) -> bool:
        return value.lower() == "true"

    @staticmethod
    def _list_from_json(value: str) -> list[str]:
        data = json.loads(value)
        return [str(item) for item in data] if isinstance(data, list) else []

    @staticmethod
    def _payload_from_json(value: str | None) -> dict[str, object] | None:
        if not value:
            return None
        data = json.loads(value)
        return data if isinstance(data, dict) else None

    @staticmethod
    def _run_to_response(run: OrchestrationRunModel) -> OrchestrationRunResponse:
        return OrchestrationRunResponse(
            id=UUID(run.id),
            case_id=UUID(run.case_id),
            status=OrchestrationRunStatus(run.status),
            current_phase_number=run.current_phase_number,
            context_summary=run.context_summary,
            last_error=run.last_error,
            created_at=run.created_at,
            updated_at=run.updated_at,
        )

    @classmethod
    def _phase_to_response(cls, phase: OrchestrationPhaseModel) -> OrchestrationPhaseResponse:
        return OrchestrationPhaseResponse(
            id=UUID(phase.id),
            run_id=UUID(phase.run_id),
            phase_number=phase.phase_number,
            phase_key=phase.phase_key,
            title=phase.title,
            agent_role=phase.agent_role,
            objective_es=phase.objective_es,
            expected_outputs_es=cls._list_from_json(phase.expected_outputs_es),
            quality_checks_es=cls._list_from_json(phase.quality_checks_es),
            status=OrchestrationPhaseStatus(phase.status),
            requires_human_checkpoint=cls._bool(phase.requires_human_checkpoint),
            checkpoint_status=CheckpointStatus(phase.checkpoint_status),
            checkpoint_reviewer=phase.checkpoint_reviewer,
            checkpoint_comment=phase.checkpoint_comment,
            started_at=phase.started_at,
            completed_at=phase.completed_at,
            updated_at=phase.updated_at,
        )

    @classmethod
    def _event_to_response(cls, event: OrchestrationEventModel) -> OrchestrationEventResponse:
        return OrchestrationEventResponse(
            id=UUID(event.id),
            run_id=UUID(event.run_id),
            phase_number=event.phase_number,
            event_type=OrchestrationEventType(event.event_type),
            actor=event.actor,
            message_es=event.message_es,
            payload=cls._payload_from_json(event.payload_json),
            created_at=event.created_at,
        )
