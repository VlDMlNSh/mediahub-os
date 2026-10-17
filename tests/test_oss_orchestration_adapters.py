"""Contract tests for optional OSS orchestration adapters."""
import asyncio

import pytest

from mediahub_runtime.oss_adapters.orchestration import (
    OrchestrationAdapterError,
    build_task_validation_graph,
    connect_temporal,
    temporal_endpoint_from_env,
    trace_operation,
)


def test_temporal_is_not_configured_implicitly(monkeypatch):
    monkeypatch.delenv("ASTRA_TEMPORAL_ENDPOINT", raising=False)
    assert temporal_endpoint_from_env() is None
    with pytest.raises(OrchestrationAdapterError, match="temporal_endpoint_not_configured"):
        asyncio.run(connect_temporal())


def test_temporal_endpoint_rejects_whitespace(monkeypatch):
    with pytest.raises(OrchestrationAdapterError, match="temporal_endpoint_invalid"):
        asyncio.run(connect_temporal("bad endpoint"))


def test_trace_operation_filters_sensitive_attributes():
    with trace_operation("astra.test", {"task_id": "T-1", "api_key": "DO_NOT_RECORD", "secret_name": "hidden"}) as span:
        assert span is not None


def test_langgraph_validation_graph_accepts_valid_envelope():
    pytest.importorskip("langgraph.graph")
    graph = build_task_validation_graph()
    result = graph.invoke({
        "task_id": "TASK-1",
        "operation": "qualify",
        "payload": {"bounded": True},
        "correlation_id": "corr-1",
    })
    assert result["accepted"] is True
    assert result["reason"] == "contract_valid"
    assert result["task_id"] == "TASK-1"


def test_langgraph_validation_graph_rejects_invalid_envelope():
    pytest.importorskip("langgraph.graph")
    result = build_task_validation_graph().invoke({"task_id": "", "payload": []})
    assert result["accepted"] is False
    assert result["reason"] == "invalid_task_envelope"


@pytest.mark.parametrize("bad_correlation", [17, [], {"id": "x"}])
def test_langgraph_rejects_non_string_correlation_without_crashing(bad_correlation):
    pytest.importorskip("langgraph.graph")
    result = build_task_validation_graph().invoke({
        "task_id": "TASK-2", "operation": "qualify", "payload": {},
        "correlation_id": bad_correlation,
    })
    assert result["accepted"] is False
    assert result["reason"] == "invalid_task_envelope"


def test_langgraph_rejects_oversized_nested_payload():
    pytest.importorskip("langgraph.graph")
    result = build_task_validation_graph().invoke({
        "task_id": "TASK-3", "operation": "qualify",
        "payload": {"items": ["x"] * 129}, "correlation_id": "corr-3",
    })
    assert result["accepted"] is False


def test_langgraph_rejects_custom_payload_objects():
    pytest.importorskip("langgraph.graph")
    result = build_task_validation_graph().invoke({
        "task_id": "TASK-4", "operation": "qualify",
        "payload": {"unexpected": object()}, "correlation_id": "corr-4",
    })
    assert result["accepted"] is False
