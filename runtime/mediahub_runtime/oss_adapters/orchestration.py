"""Fail-closed, opt-in adapters for LangGraph, Temporal, and OpenTelemetry.

These adapters do not own queue state, authorize work, or mutate MediaHub State
Authority. Callers must pass an already-authorized, bounded task contract. No
network connection or external workflow is started at import time.
"""
from __future__ import annotations

import os
from contextlib import contextmanager
from typing import Any, Iterator, TypedDict


class OrchestrationAdapterError(RuntimeError):
    """Raised when an optional dependency or explicit runtime setting is absent."""


class TaskEnvelope(TypedDict, total=False):
    task_id: str
    operation: str
    payload: dict[str, Any]
    correlation_id: str


class GraphResult(TypedDict):
    task_id: str
    accepted: bool
    reason: str
    correlation_id: str


def _is_bounded_json_value(value: Any, *, depth: int = 0) -> bool:
    """Accept only bounded JSON-like payloads; reject custom objects and cycles."""
    if depth > 8:
        return False
    if value is None or isinstance(value, (bool, int, float)):
        return True
    if isinstance(value, str):
        return len(value) <= 4096
    if isinstance(value, list):
        return len(value) <= 128 and all(
            _is_bounded_json_value(item, depth=depth + 1) for item in value
        )
    if isinstance(value, dict):
        return len(value) <= 128 and all(
            isinstance(key, str)
            and len(key) <= 128
            and _is_bounded_json_value(item, depth=depth + 1)
            for key, item in value.items()
        )
    return False


def build_task_validation_graph():
    """Build a deterministic LangGraph validation graph, without executing work.

    This graph only validates the outer envelope. It is not a queue consumer and
    cannot execute arbitrary code, dispatch providers, or commit state.
    """
    try:
        from langgraph.graph import END, START, StateGraph
    except ImportError as exc:  # pragma: no cover - depends on deployment extras
        raise OrchestrationAdapterError("langgraph_dependency_unavailable") from exc

    def validate(state: dict[str, Any]) -> dict[str, Any]:
        task_id = state.get("task_id")
        operation = state.get("operation")
        payload = state.get("payload")
        correlation_id = state.get("correlation_id", "")
        accepted = (
            isinstance(task_id, str)
            and 1 <= len(task_id) <= 256
            and task_id == task_id.strip()
            and isinstance(operation, str)
            and 1 <= len(operation) <= 128
            and operation == operation.strip()
            and isinstance(payload, dict)
            and _is_bounded_json_value(payload)
            and isinstance(correlation_id, str)
            and len(correlation_id) <= 256
        )
        return {
            "task_id": task_id if isinstance(task_id, str) else "",
            "accepted": accepted,
            "reason": "contract_valid" if accepted else "invalid_task_envelope",
            "correlation_id": correlation_id if isinstance(correlation_id, str) else "",
        }

    graph = StateGraph(dict)
    graph.add_node("validate_contract", validate)
    graph.add_edge(START, "validate_contract")
    graph.add_edge("validate_contract", END)
    return graph.compile()


def temporal_endpoint_from_env() -> str | None:
    """Return an explicitly configured Temporal endpoint; never infer one."""
    value = os.environ.get("ASTRA_TEMPORAL_ENDPOINT", "").strip()
    return value or None


async def connect_temporal(endpoint: str | None = None):
    """Connect only when explicitly called with a configured endpoint.

    This function does not start workers or create namespaces/workflows. Callers
    remain responsible for TLS/auth configuration and bounded lifecycle.
    """
    address = endpoint or temporal_endpoint_from_env()
    if not address:
        raise OrchestrationAdapterError("temporal_endpoint_not_configured")
    if len(address) > 512 or any(c.isspace() for c in address):
        raise OrchestrationAdapterError("temporal_endpoint_invalid")
    try:
        from temporalio.client import Client
    except ImportError as exc:  # pragma: no cover - depends on deployment extras
        raise OrchestrationAdapterError("temporal_dependency_unavailable") from exc
    try:
        return await Client.connect(address)
    except Exception as exc:
        # Do not include endpoint, credentials, or upstream exception text.
        raise OrchestrationAdapterError("temporal_connection_failed") from exc


@contextmanager
def trace_operation(name: str, attributes: dict[str, str] | None = None) -> Iterator[Any]:
    """Yield an OpenTelemetry span or a no-op span when optional telemetry is absent."""
    if not isinstance(name, str) or not name or len(name) > 128:
        raise OrchestrationAdapterError("trace_name_invalid")
    safe_attributes: dict[str, str] = {}
    for key, value in (attributes or {}).items():
        if (
            isinstance(key, str) and isinstance(value, str)
            and 1 <= len(key) <= 64 and len(value) <= 256
            and not any(secret in key.lower() for secret in ("token", "secret", "password", "api_key", "credential"))
        ):
            safe_attributes[key] = value

    try:
        from opentelemetry import trace
        tracer = trace.get_tracer("mediahub.astra.oss-adapters")
    except ImportError:  # telemetry is optional; task execution must remain available
        class NoOpSpan:
            def set_attribute(self, *_args, **_kwargs):
                return None
            def __enter__(self):
                return self
            def __exit__(self, *_args):
                return False
        with NoOpSpan() as span:
            for key, value in safe_attributes.items():
                span.set_attribute(key, value)
            yield span
        return

    with tracer.start_as_current_span(name) as span:
        for key, value in safe_attributes.items():
            span.set_attribute(key, value)
        yield span
