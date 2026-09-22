"""Astra Edge execution boundary over the existing local AI routing plane.
Astra owns orchestration; this adapter only admits canonical tasks and delegates
LOCAL execution to the existing Ollama endpoint.
"""
from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from dataclasses import dataclass
from enum import StrEnum
from typing import Any

from ops.ai.ai_routing import ProviderState, Route, RoutingDecision, decide_cloud_failure


class AstraEdgeDenied(PermissionError):
    """Raised when an edge task cannot be admitted safely."""


class EdgeStatus(StrEnum):
    SUCCEEDED = "succeeded"
    BLOCKED = "blocked"
    FAILED = "failed"


@dataclass(frozen=True)
class EdgeTask:
    request_id: str
    session_id: str
    command: str
    approval_state: str
    requested_capabilities: tuple[str, ...] = ()


@dataclass(frozen=True)
class EdgeResult:
    request_id: str
    route: Route
    status: EdgeStatus
    output: str = ""
    error_code: str = ""


class AstraEdgeAdapter:
    """Thin adapter; it is not a second State Authority or orchestrator."""

    def __init__(self, ollama_url: str | None = None, model: str | None = None,
                 timeout_seconds: int = 30) -> None:
        self.ollama_url = ollama_url or os.environ.get(
            "ASTRA_OLLAMA_URL", "http://127.0.0.1:11434/api/generate"
        )
        self.model = model or os.environ.get("ASTRA_OLLAMA_MODEL", "qwen2.5-coder:3b")
        self.timeout_seconds = timeout_seconds
    @staticmethod
    def validate(task: EdgeTask) -> None:
        if not isinstance(task, EdgeTask):
            raise AstraEdgeDenied("task type is invalid")
        if not all(isinstance(v, str) and v.strip() == v and v for v in
                   (task.request_id, task.session_id, task.command)):
            raise AstraEdgeDenied("task identity or command is invalid")
        if task.approval_state not in {"not_required", "approved"}:
            raise AstraEdgeDenied("task approval is not satisfied")
        if not isinstance(task.requested_capabilities, tuple):
            raise AstraEdgeDenied("capabilities are invalid")
        if any(not isinstance(v, str) or not v for v in task.requested_capabilities):
            raise AstraEdgeDenied("capabilities are invalid")
        if len(task.command.encode("utf-8")) > 64 * 1024:
            raise AstraEdgeDenied("command exceeds bounded size")

    def route(self, provider_state: ProviderState = ProviderState.AVAILABLE,
              *, local_available: bool = True,
              local_cluster_available: bool = False) -> RoutingDecision:
        if provider_state is ProviderState.AVAILABLE:
            return RoutingDecision(Route.LOCAL, provider_state, False, "local edge available")
        return decide_cloud_failure(
            provider_state,
            local_cluster_available=local_cluster_available,
            local_available=local_available,
        )

    def execute_local(self, task: EdgeTask) -> EdgeResult:
        self.validate(task)
        decision = self.route()
        if decision.route is not Route.LOCAL:
            return EdgeResult(task.request_id, decision.route, EdgeStatus.BLOCKED,
                              error_code="route_not_local")
        payload: dict[str, Any] = {
            "model": self.model,
            "prompt": task.command,
            "stream": False,
            "options": {"temperature": 0},
        }
        request = urllib.request.Request(
            self.ollama_url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=self.timeout_seconds) as response:
                raw = response.read(1_048_577)
            if len(raw) > 1_048_576:
                return EdgeResult(task.request_id, Route.LOCAL, EdgeStatus.FAILED,
                                  error_code="output_too_large")
            body = json.loads(raw.decode("utf-8"))
            output = body.get("response")
            if not isinstance(output, str):
                return EdgeResult(task.request_id, Route.LOCAL, EdgeStatus.FAILED,
                                  error_code="malformed_provider_response")
            return EdgeResult(task.request_id, Route.LOCAL, EdgeStatus.SUCCEEDED, output=output)
        except (urllib.error.URLError, TimeoutError):
            return EdgeResult(task.request_id, Route.LOCAL, EdgeStatus.FAILED,
                              error_code="local_provider_unavailable")
        except (json.JSONDecodeError, UnicodeDecodeError, KeyError, TypeError):
            return EdgeResult(task.request_id, Route.LOCAL, EdgeStatus.FAILED,
                              error_code="malformed_provider_response")
    def execute(self, task: EdgeTask, *, provider_state: ProviderState = ProviderState.AVAILABLE,
                local_available: bool = True,
                local_cluster_available: bool = False) -> EdgeResult:
        self.validate(task)
        decision = self.route(provider_state, local_available=local_available,
                              local_cluster_available=local_cluster_available)
        if decision.route is Route.LOCAL:
            return self.execute_local(task)
        return EdgeResult(task.request_id, decision.route, EdgeStatus.BLOCKED,
                          error_code="cloud_route_requires_cloud_orchestrator")

    def execute_and_reconcile(self, task: EdgeTask, boundary, request,
                               *, expected_generation: int | None = None) -> EdgeResult:
        """Execute locally, then record the terminal result through the canonical boundary."""
        result = self.execute(task)
        if result.status is not EdgeStatus.SUCCEEDED or result.route is not Route.LOCAL:
            return result
        value = {
            "request_id": result.request_id,
            "route": result.route.value,
            "status": result.status.value,
            "output": result.output,
            "error_code": result.error_code,
        }
        boundary.execute(
            request,
            "set",
            ("astra", "tasks", result.request_id),
            value,
            expected_generation=expected_generation,
            command_id=f"reconcile-{result.request_id}",
        )
        return result
