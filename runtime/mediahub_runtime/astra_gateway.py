"""Astra task intake and cloud-first execution gateway."""

from __future__ import annotations

import hashlib
import json
import urllib.error
import urllib.request
from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from .cloud_orchestrator import CloudFirstOrchestrator, CloudOrchestratorError


class AstraGatewayError(RuntimeError):
    """Sanitized gateway rejection."""

    def __init__(self, code: str):
        self.code = code
        super().__init__(code)


EVENT_TYPES = (
    "task.accepted",
    "task.planned",
    "policy.checked",
    "agent.selected",
    "execution.started",
    "execution.progress",
    "artifact.created",
    "validation.completed",
    "approval.required",
    "task.completed",
    "task.failed",
)


@dataclass(frozen=True)
class AstraTaskRequest:
    request_id: str
    session_id: str
    user_command: str
    approval_state: str = "not_required"
    context_refs: tuple[str, ...] = ()
    client_platform: str = "unknown"
    client_version: str = "unknown"


@dataclass(frozen=True)
class AstraEvent:
    event_id: str
    request_id: str
    session_id: str
    execution_id: str
    event_type: str
    timestamp: str
    payload: dict


@dataclass(frozen=True)
class AstraEvidence:
    output_sha256: str
    output_bytes: int
    provider_id: str
    model: str


@dataclass(frozen=True)
class AstraTaskResult:
    request_id: str
    session_id: str
    execution_id: str
    status: str
    provider_id: str | None
    model: str | None
    output: str | None
    evidence: AstraEvidence | None
    events: tuple[AstraEvent, ...]
    error_code: str | None = None


@dataclass(frozen=True)
class AgentDescriptor:
    agent_id: str
    enabled: bool
    tier: str
    capabilities: frozenset[str]


class AgentRegistry:
    """Read-only view of the canonical repository agent registry."""

    def __init__(self, path: str | Path | None = None):
        registry_path = Path(path) if path else Path(__file__).resolve().parents[2] / "profiles" / "agent-registry.json"
        try:
            raw = registry_path.read_text(encoding="utf-8")
        except OSError as exc:
            raise AstraGatewayError("agent_registry_unavailable") from exc
        try:
            data = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise AstraGatewayError("agent_registry_invalid") from exc
        try:
            agents = data["agents"]
        except (KeyError, TypeError) as exc:
            raise AstraGatewayError("agent_registry_invalid") from exc
        if not isinstance(agents, list):
            raise AstraGatewayError("agent_registry_invalid")
        parsed = []
        for item in agents:
            try:
                descriptor = AgentDescriptor(
                    item["id"], bool(item["enabled"]), item["tier"],
                    frozenset(item["capabilities"]),
                )
            except (KeyError, TypeError) as exc:
                raise AstraGatewayError("agent_registry_invalid") from exc
            if not descriptor.agent_id or not descriptor.tier or any(not isinstance(c, str) or not c for c in descriptor.capabilities):
                raise AstraGatewayError("agent_registry_invalid")
            parsed.append(descriptor)
        self._agents = tuple(parsed)

    def select(self, required_capability: str) -> AgentDescriptor:
        if not isinstance(required_capability, str) or not required_capability.strip():
            raise AstraGatewayError("invalid_capability")
        candidates = [
            agent for agent in self._agents
            if agent.enabled and required_capability in agent.capabilities
        ]
        local = [agent for agent in candidates if agent.tier == "local" and agent.agent_id == "ollama"]
        if local:
            return local[0]
        raise AstraGatewayError("no_local_agent_available")


class OllamaExecutor:
    """Bounded local Ollama adapter; credentials are never accepted."""

    provider_id = "ollama"
    model = "qwen2.5-coder:3b"

    def __init__(self, url="http://127.0.0.1:11434/api/generate", timeout=30):
        self._url = url
        self._timeout = timeout

    def __call__(self, prompt: str) -> str:
        body = json.dumps(
            {"model": self.model, "prompt": prompt, "stream": False,
             "options": {"temperature": 0, "num_predict": 1200}},
            separators=(",", ":"),
        ).encode("utf-8")
        request = urllib.request.Request(
            self._url,
            data=body,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=self._timeout) as response:
                raw = response.read(1_048_576)
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            raise AstraGatewayError("local_provider_unavailable") from exc
        try:
            data = json.loads(raw.decode("utf-8"))
            output = data["response"]
        except (UnicodeDecodeError, json.JSONDecodeError, KeyError, TypeError) as exc:
            raise AstraGatewayError("local_provider_invalid_response") from exc
        if not isinstance(output, str):
            raise AstraGatewayError("local_provider_invalid_response")
        return output


class AstraGatewayRuntime:
    """Contract-first Astra runtime with cloud-first routing and local extension fallback."""

    MAX_COMMAND_BYTES = 65_536
    MAX_CONTEXT_REFS = 32
    MAX_OUTPUT_BYTES = 1_048_576
    SENSITIVE_ACTIONS = frozenset(
        {"host_install", "credential_change", "production_deploy", "destructive_action"}
    )

    def __init__(self, executor: Callable[[str], str] | None = None, registry: AgentRegistry | None = None, orchestrator: CloudFirstOrchestrator | None = None):
        self._legacy_executor = executor
        self._registry = registry or AgentRegistry()
        self._orchestrator = orchestrator or CloudFirstOrchestrator(
            executors={"ollama": OllamaExecutor()}
        )

    def run(self, task: AstraTaskRequest) -> AstraTaskResult:
        self._validate_task(task)
        execution_id = f"exec-{task.request_id}"
        events: list[AstraEvent] = []
        self._emit(events, task, execution_id, "task.accepted", {"route": "cloud_first"})
        self._emit(events, task, execution_id, "task.planned", {"strategy": "cloud_first_local_extension"})
        sensitive = self._classify(task.user_command)
        if sensitive and task.approval_state != "approved":
            self._emit(events, task, execution_id, "policy.checked", {"allowed": False})
            self._emit(events, task, execution_id, "approval.required", {"action": sensitive})
            return AstraTaskResult(task.request_id, task.session_id, execution_id, "failed", None, None, None, None, tuple(events), "approval_required")
        self._emit(events, task, execution_id, "policy.checked", {"allowed": True})
        capability = self._capability(task.user_command)
        try:
            if self._legacy_executor is not None:
                agent = self._registry.select(capability)
                provider_id, tier, model = agent.agent_id, agent.tier, OllamaExecutor.model
                output = self._legacy_executor(task.user_command)
                reason = "legacy_injected_executor"
            else:
                decision, output = self._orchestrator.execute(capability, task.user_command)
                provider_id, tier, model, reason = decision.provider_id, decision.tier, decision.model or "unspecified", decision.reason
        except (CloudOrchestratorError, AstraGatewayError) as exc:
            code = getattr(exc, "code", "provider_execution_failed")
            self._emit(events, task, execution_id, "task.failed", {"error_code": code})
            return AstraTaskResult(task.request_id, task.session_id, execution_id, "failed", None, None, None, None, tuple(events), code)
        self._emit(events, task, execution_id, "agent.selected", {"provider_id": provider_id, "tier": tier, "capability": capability, "route_reason": reason, "model": model})
        self._emit(events, task, execution_id, "execution.started", {"provider_id": provider_id})
        try:
            if not isinstance(output, str) or not output:
                raise AstraGatewayError("empty_execution_result")
            encoded = output.encode("utf-8")
            if len(encoded) > self.MAX_OUTPUT_BYTES:
                raise AstraGatewayError("output_limit_exceeded")
            self._emit(events, task, execution_id, "execution.progress", {"status": "completed"})
            evidence = AstraEvidence(hashlib.sha256(encoded).hexdigest(), len(encoded), provider_id, model)
            self._emit(events, task, execution_id, "artifact.created", {"artifact_type": "text_result", "sha256": evidence.output_sha256, "bytes": evidence.output_bytes})
            self._emit(events, task, execution_id, "validation.completed", {"valid": True})
            self._emit(events, task, execution_id, "task.completed", {"acceptance": "output_present"})
            return AstraTaskResult(task.request_id, task.session_id, execution_id, "completed", provider_id, model, output, evidence, tuple(events))
        except AstraGatewayError as exc:
            self._emit(events, task, execution_id, "task.failed", {"error_code": exc.code})
            return AstraTaskResult(task.request_id, task.session_id, execution_id, "failed", provider_id, model, None, None, tuple(events), exc.code)

    @staticmethod
    def _capability(command: str) -> str:
        normalized = command.lower()
        if any(token in normalized for token in ("research", "web", "search")):
            return "research"
        if any(token in normalized for token in ("architecture", "design")):
            return "architecture"
        if any(token in normalized for token in ("review", "audit")):
            return "review"
        if any(token in normalized for token in ("document", "pdf", "image", "multimodal")):
            return "documents"
        return "coding"

    @classmethod
    def _validate_task(cls, task: AstraTaskRequest) -> None:
        if not isinstance(task, AstraTaskRequest):
            raise AstraGatewayError("invalid_task")
        for value in (task.request_id, task.session_id, task.user_command):
            if not isinstance(value, str) or not value.strip():
                raise AstraGatewayError("invalid_task")
        if task.approval_state not in {"not_required", "approved", "pending", "rejected"}:
            raise AstraGatewayError("invalid_approval_state")
        if len(task.user_command.encode("utf-8")) > cls.MAX_COMMAND_BYTES:
            raise AstraGatewayError("command_limit_exceeded")
        if type(task.context_refs) is not tuple or len(task.context_refs) > cls.MAX_CONTEXT_REFS:
            raise AstraGatewayError("invalid_context")
        if any(not isinstance(ref, str) or not ref.strip() for ref in task.context_refs):
            raise AstraGatewayError("invalid_context")

    @classmethod
    def _classify(cls, command: str) -> str | None:
        normalized = command.strip().lower()
        for action in cls.SENSITIVE_ACTIONS:
            if action in normalized:
                return action
        return None

    @staticmethod
    def _emit(events, task, execution_id, event_type, payload):
        if event_type not in EVENT_TYPES:
            raise AstraGatewayError("invalid_event_type")
        safe_payload = {str(k): v for k, v in payload.items()}
        if any("key" in k.lower() or "token" in k.lower() or "secret" in k.lower()
               or "credential" in k.lower() or "password" in k.lower() for k in safe_payload):
            raise AstraGatewayError("event_secret_field")
        event_id = f"{execution_id}-{len(events) + 1}"
        events.append(AstraEvent(event_id, task.request_id, task.session_id, execution_id,
                                 event_type, datetime.now(timezone.utc).isoformat(), safe_payload))
