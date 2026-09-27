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
