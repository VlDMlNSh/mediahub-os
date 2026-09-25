import json

from ops.mediahub_canonical_protocol import CanonicalRequest, FailureClass, Protocol
from ops.mediahub_provider_adapters import AdapterResult, OpenAIChatAdapter, OpenAIResponsesAdapter, OpenRouterAdapter
from ops.mediahub_provider_execution import ProviderExecutionCoordinator
from ops.mediahub_provider_gateway import Provider, ProviderGateway
from ops.mediahub_resilience import RetryPolicy


def request():
    return CanonicalRequest("exec-1", "model-x", Protocol.OPENAI_CHAT, [{"role": "user", "content": "hello"}], 7.0)


def coordinator(send, *, max_attempts=2, sleep_fn=None):
    gateway = ProviderGateway(
        (Provider("openai", "https://openai.example", 10), Provider("openrouter", "https://openrouter.example", 20)),
        threshold=2,
        cooldown_seconds=60,
    )
    return ProviderExecutionCoordinator(
        gateway,
        adapters=(OpenAIChatAdapter(), OpenRouterAdapter()),
        credential_for=lambda provider: f"credential-{provider}",
        send=send,
        retry_policy=RetryPolicy(max_attempts=max_attempts, base_delay_seconds=0.5, max_delay_seconds=2.0),
        sleep_fn=sleep_fn or (lambda _: None),
    )


def test_503_fails_over_with_bounded_retry():
    calls = []
    def send(http, timeout):
        calls.append((http.url, timeout))
        return AdapterResult(503, {}, b"{}") if len(calls) == 1 else AdapterResult(200, {}, b'{"ok":true}')

    out = coordinator(send).execute(request())
    assert out.provider == "openrouter"
    assert [url for url, _ in calls] == [OpenAIChatAdapter.endpoint, OpenRouterAdapter.endpoint]


def test_429_retry_after_is_bounded_and_not_secret_bearing():
    calls = []
    delays = []
    def send(http, timeout):
        calls.append(http)
        return AdapterResult(429, {"retry-after": "99"}, b"{}") if len(calls) == 1 else AdapterResult(200, {}, b'{"ok":true}')

    out = coordinator(send, sleep_fn=delays.append).execute(request())
    assert out.provider == "openrouter"
    assert delays == [2.0]
    assert all("credential" not in http.url for http in calls)


def test_401_quarantines_provider_without_retrying_same_provider():
    calls = []
    def send(http, timeout):
        calls.append(http.url)
        return AdapterResult(401, {}, b"{}") if len(calls) == 1 else AdapterResult(200, {}, b'{"ok":true}')

    out = coordinator(send).execute(request())
    assert out.provider == "openrouter"
    assert calls == [OpenAIChatAdapter.endpoint, OpenRouterAdapter.endpoint]


def test_permanent_failure_fails_closed_without_failover():
    calls = []
    def send(http, timeout):
        calls.append(http.url)
        return AdapterResult(400, {}, b"{}")

    out = coordinator(send).execute(request())
    assert out.failure_class is FailureClass.PERMANENT
    assert calls == [OpenAIChatAdapter.endpoint]


def test_all_candidates_failed_returns_last_failure_and_stays_bounded():
    calls = []
    def send(http, timeout):
        calls.append(http.url)
        return AdapterResult(503, {}, b"{}")

    out = coordinator(send, max_attempts=2).execute(request())
    assert out.failure_class is FailureClass.TRANSIENT
    assert len(calls) == 2


def test_ambiguous_transport_outcome_fails_closed_without_failover():
    calls = []
    def send(http, timeout):
        calls.append(http.url)
        raise TimeoutError("transport timeout")

    out = coordinator(send).execute(request())
    assert out.failure_class is FailureClass.TRANSIENT
    assert out.outcome_ambiguous is True
    assert calls == [OpenAIChatAdapter.endpoint]


def test_ambiguous_transport_can_fail_over_only_with_explicit_replay_safety():
    calls = []
    def send(http, timeout):
        calls.append(http.url)
        if len(calls) == 1:
            raise TimeoutError("transport timeout")
        return AdapterResult(200, {}, b'{"ok":true}')

    replay_safe = CanonicalRequest(
        "exec-1", "model-x", Protocol.OPENAI_CHAT,
        [{"role": "user", "content": "hello"}], 7.0,
        provider_extensions={"allow_ambiguous_replay": True},
    )
    out = coordinator(send).execute(replay_safe)
    assert out.provider == "openrouter"
    assert calls == [OpenAIChatAdapter.endpoint, OpenRouterAdapter.endpoint]


def test_missing_credential_is_policy_blocked_and_does_not_send():
    calls = []
    out = ProviderExecutionCoordinator(
        ProviderGateway((Provider("openai", "https://openai.example", 10), Provider("openrouter", "https://openrouter.example", 20))),
        adapters=(OpenAIChatAdapter(), OpenRouterAdapter()),
        credential_for=lambda _: None,
        send=lambda http, timeout: calls.append(http),
        retry_policy=RetryPolicy(max_attempts=2),
        sleep_fn=lambda _: None,
    ).execute(request())
    assert out.failure_class is FailureClass.POLICY_BLOCKED
    assert calls == []
