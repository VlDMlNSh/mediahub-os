from mediahub_runtime.cloud_orchestrator import CloudFirstOrchestrator, ProviderRoute


def test_failover_uses_next_model_after_first_executor_failure():
    route = ProviderRoute(
        "fake",
        "cloud",
        frozenset({"coding"}),
        "FAKE_API_KEY",
        "FAKE_MODEL",
        1,
    )
    calls = []

    def executor(prompt):
        calls.append(prompt)
        if len(calls) == 1:
            raise RuntimeError("rate limited")
        return "ok"

    orchestrator = CloudFirstOrchestrator(
        cloud_routes=(route,),
        local_routes=(),
        credential_env={
            "FAKE_API_KEY": "key-1",
            "FAKE_MODEL": "model-a",
            "FAKE_MODELS": "model-a,model-b",
        },
        executors={"fake": executor},
    )

    decision, output = orchestrator.execute("coding", "test")

    assert output == "ok"
    assert decision.provider_id == "fake"
    assert decision.model == "model-b"
    assert len(calls) == 2


def test_failover_uses_indexed_credential_slot():
    route = ProviderRoute(
        "fake",
        "cloud",
        frozenset({"coding"}),
        "FAKE_API_KEY",
        "FAKE_MODEL",
        1,
    )
    seen = []

    def executor(prompt):
        seen.append(prompt)
        if len(seen) == 1:
            raise RuntimeError("quota exhausted")
        return "ok"

    orchestrator = CloudFirstOrchestrator(
        cloud_routes=(route,),
        local_routes=(),
        credential_env={
            "FAKE_API_KEY_1": "key-1",
            "FAKE_API_KEY_2": "key-2",
            "FAKE_MODEL": "model-a",
        },
        executors={"fake": executor},
    )

    decision, output = orchestrator.execute("coding", "test")

    assert output == "ok"
    assert decision.model == "model-a"
    assert len(seen) == 2


def test_openrouter_route_builds_compatible_executor():
    route = ProviderRoute(
        "openrouter",
        "cloud",
        frozenset({"coding"}),
        "OPENROUTER_API_KEY",
        "MEDIAHUB_OPENROUTER_MODEL",
        1,
    )
    orchestrator = CloudFirstOrchestrator(
        cloud_routes=(route,),
        local_routes=(),
        credential_env={
            "OPENROUTER_API_KEY": "key",
            "MEDIAHUB_OPENROUTER_MODEL": "model",
        },
    )
    decision, executor = orchestrator._candidates("coding", allow_local_extension=False)[0]
    assert decision.provider_id == "openrouter"
    assert decision.model == "model"
    assert executor.__class__.__name__ == "OpenAICompatibleExecutor"


def test_freellmapi_candidate_uses_selected_model_and_local_gateway():
    route = ProviderRoute(
        "freellmapi", "local_gateway", frozenset({"coding"}), None,
        "MEDIAHUB_FREELLMAPI_MODEL", 1,
    )
    orchestrator = CloudFirstOrchestrator(
        cloud_routes=(),
        local_routes=(route,),
        credential_env={
            "MEDIAHUB_FREELLMAPI_URL": "http://127.0.0.1:3001/v1",
            "MEDIAHUB_FREELLMAPI_KEY_FILE": "/tmp/freellmapi.key",
            "MEDIAHUB_FREELLMAPI_MODEL": "model-a",
            "MEDIAHUB_FREELLMAPI_MODELS": "model-a,model-b",
        },
        executors={},
    )
    candidates = orchestrator._candidates("coding", allow_local_extension=True)
    assert len(candidates) == 2
    assert [d.model for d, _ in candidates] == ["model-a", "model-b"]
    assert all(e.__class__.__name__ == "FreeLLMAPIExecutor" for _, e in candidates)


def test_openai_route_uses_native_responses_executor():
    route = ProviderRoute(
        "openai", "cloud", frozenset({"coding"}), "OPENAI_API_KEY",
        "MEDIAHUB_OPENAI_MODEL", 1,
    )
    orchestrator = CloudFirstOrchestrator(
        cloud_routes=(route,), local_routes=(),
        credential_env={"OPENAI_API_KEY": "key", "MEDIAHUB_OPENAI_MODEL": "model"},
    )
    decision, executor = orchestrator._candidates("coding", allow_local_extension=False)[0]
    assert decision.provider_id == "openai"
    assert executor.__class__.__name__ == "OpenAIResponsesExecutor"


def test_gemini_route_uses_native_executor():
    route = ProviderRoute(
        "gemini", "cloud", frozenset({"reasoning"}), "GEMINI_API_KEY",
        "MEDIAHUB_GEMINI_MODEL", 1,
    )
    orchestrator = CloudFirstOrchestrator(
        cloud_routes=(route,), local_routes=(),
        credential_env={"GEMINI_API_KEY": "key", "MEDIAHUB_GEMINI_MODEL": "model"},
    )
    decision, executor = orchestrator._candidates("reasoning", allow_local_extension=False)[0]
    assert decision.provider_id == "gemini"
    assert executor.__class__.__name__ == "GeminiExecutor"


def test_http_error_classification():
    from mediahub_runtime.cloud_orchestrator import _http_error_code
    assert _http_error_code(401) == "provider_auth_failed"
    assert _http_error_code(403) == "provider_auth_failed"
    assert _http_error_code(402) == "provider_billing_blocked"
    assert _http_error_code(429) == "provider_rate_limited"
    assert _http_error_code(500) == "provider_server_error"
