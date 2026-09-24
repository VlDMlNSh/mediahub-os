import hashlib

import pytest
from mediahub_runtime import (
    AgentRegistry,
    AstraGatewayError,
    AstraGatewayRuntime,
    AstraTaskRequest,
    AutonomousTaskPolicy,
)


def task(command="Return READY"):
    return AstraTaskRequest("req-1", "session-1", command)


def test_local_path_emits_typed_events_and_evidence():
    gateway = AstraGatewayRuntime(executor=lambda _: "READY")
    result = gateway.run(task())

    assert result.status == "completed"
    assert result.provider_id == "ollama"
    assert result.model == "qwen2.5-coder:3b"
    assert result.output == "READY"
    assert result.evidence.output_sha256 == hashlib.sha256(b"READY").hexdigest()
    assert [event.event_type for event in result.events] == [
        "task.accepted",
        "task.planned",
        "policy.checked",
        "agent.selected",
        "execution.started",
        "execution.progress",
        "artifact.created",
        "validation.completed",
        "task.completed",
    ]


def test_bounded_gateway_path_uses_existing_runtime_and_records_lifecycle_evidence():
    gateway = AstraGatewayRuntime(executor=lambda _: "READY")
    result = gateway.run_bounded(task())

    assert result.status == "PASS"
    assert result.attempts == 1
    assert result.repairs == 0
    assert result.result.output == "READY"
    assert result.evidence[0].phase == "plan"
    assert result.evidence[-1].phase == "verify"
    assert all(len(item.detail_sha256) == 64 for item in result.evidence)


def test_bounded_gateway_path_preserves_approval_boundary():
    called = False

    def executor(_):
        nonlocal called
        called = True
        return "should-not-run"

    gateway = AstraGatewayRuntime(executor=executor)
    result = gateway.run_bounded(
        task("production_deploy now"),
        policy=AutonomousTaskPolicy(max_attempts=2, max_repairs=1),
    )

    assert result.status == "REPAIR_EXHAUSTED"
    assert result.result is None
    assert called is False
    assert result.attempts == 1
    assert result.repairs == 0


def test_sensitive_action_stops_at_approval_boundary():
    called = False

    def executor(_):
        nonlocal called
        called = True
        return "should-not-run"

    result = AstraGatewayRuntime(executor=executor).run(task("production_deploy now"))

    assert result.status == "failed"
    assert result.error_code == "approval_required"
    assert called is False
    assert result.events[-1].event_type == "approval.required"


def test_approved_sensitive_action_can_use_local_executor():
    approved = AstraTaskRequest(
        "req-2", "session-1", "production_deploy", approval_state="approved"
    )
    result = AstraGatewayRuntime(executor=lambda _: "approved-result").run(approved)

    assert result.status == "completed"
    assert result.output == "approved-result"


def test_invalid_task_and_context_fail_closed():
    with pytest.raises(AstraGatewayError) as exc:
        AstraGatewayRuntime().run(object())
    assert exc.value.code == "invalid_task"

    with pytest.raises(AstraGatewayError) as exc:
        AstraGatewayRuntime().run(
            AstraTaskRequest("req", "session", "cmd", context_refs=["bad"])
        )
    assert exc.value.code == "invalid_context"


def test_command_and_output_bounds_are_enforced():
    with pytest.raises(AstraGatewayError) as exc:
        AstraGatewayRuntime().run(task("x" * 65_537))
    assert exc.value.code == "command_limit_exceeded"

    result = AstraGatewayRuntime(executor=lambda _: "x" * 1_048_577).run(task())
    assert result.status == "failed"
    assert result.error_code == "output_limit_exceeded"


def test_failed_provider_result_is_sanitized_and_audited():
    def failing(_):
        raise AstraGatewayError("local_provider_unavailable")

    result = AstraGatewayRuntime(executor=failing).run(task())

    assert result.status == "failed"
    assert result.error_code == "local_provider_unavailable"
    assert result.events[-1].event_type == "task.failed"
    assert result.events[-1].payload == {"error_code": "local_provider_unavailable"}


def test_event_payload_rejects_secret_named_fields():
    gateway = AstraGatewayRuntime(executor=lambda _: "READY")
    task_request = task()
    events = []
    with pytest.raises(AstraGatewayError) as exc:
        gateway._emit(events, task_request, "exec-1", "task.accepted", {"api_key": "x"})
    assert exc.value.code == "event_secret_field"


def test_registry_selects_enabled_local_agent_and_rejects_missing_local_capability():
    registry = AgentRegistry()
    selected = registry.select("coding")
    assert selected.agent_id == "ollama"
    assert selected.tier == "local"
    with pytest.raises(AstraGatewayError) as exc:
        registry.select("research")
    assert exc.value.code == "no_local_agent_available"


def test_gateway_fails_closed_when_registry_is_invalid(tmp_path):
    path = tmp_path / "registry.json"
    path.write_text("{}", encoding="utf-8")
    with pytest.raises(AstraGatewayError) as exc:
        AgentRegistry(path)
    assert exc.value.code == "agent_registry_invalid"

from mediahub_runtime.connectors import TinyFishConnector, TinyFishConnectorError


def test_tinyfish_connector_requires_user_owned_key():
    connector = TinyFishConnector(api_key="")
    assert connector.configured is False
    with pytest.raises(TinyFishConnectorError) as exc:
        connector.start(url="https://example.com", goal="check status")
    assert exc.value.code == "tinyfish_not_configured"


def test_tinyfish_connector_rejects_non_https_webhook():
    connector = TinyFishConnector(api_key="test-only")
    with pytest.raises(TinyFishConnectorError) as exc:
        connector.start(url="https://example.com", goal="check status", webhook_url="http://localhost")
    assert exc.value.code == "invalid_webhook_url"


@pytest.mark.parametrize("webhook_url", [
    "https://127.0.0.1/hook",
    "https://192.168.1.1/hook",
    "https://user:pass@example.com/hook",
    "https://service.local/hook",
])
def test_tinyfish_connector_rejects_non_public_webhook(webhook_url):
    connector = TinyFishConnector(api_key="test-only")
    with pytest.raises(TinyFishConnectorError) as exc:
        connector.start(url="https://example.com", goal="check status", webhook_url=webhook_url)
    assert exc.value.code == "invalid_webhook_url"
