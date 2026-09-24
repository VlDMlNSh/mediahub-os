from mediahub_runtime import CloudFirstOrchestrator, CloudOrchestratorError


def test_cloud_first_selects_configured_cloud_provider():
    o = CloudFirstOrchestrator(credential_env={"OPENAI_API_KEY": "test", "MEDIAHUB_OPENAI_MODEL": "cloud-model"})
    d = o.decide("reasoning")
    assert d.provider_id == "openai"
    assert d.tier == "cloud"
    assert d.model == "cloud-model"


def test_local_is_extension_when_cloud_credentials_are_absent():
    o = CloudFirstOrchestrator(credential_env={})
    d = o.decide("coding")
    assert d.provider_id == "ollama"
    assert d.tier == "local"
    assert d.reason == "cloud_unavailable_local_extension"


def test_orchestrator_executes_only_through_registered_adapter():
    o = CloudFirstOrchestrator(credential_env={"OPENAI_API_KEY": "test"}, executors={"openai": lambda p: "OK"})
    d, output = o.execute("reasoning", "hello")
    assert d.provider_id == "openai"
    assert output == "OK"


def test_unconfigured_cloud_without_local_extension_fails_closed():
    o = CloudFirstOrchestrator(credential_env={})
    try:
        o.decide("research", allow_local_extension=False)
    except CloudOrchestratorError as exc:
        assert exc.code == "no_provider_available"
    else:
        raise AssertionError("expected fail-closed routing")


def test_openrouter_is_cloud_first_when_github_runtime_secret_is_present():
    o = CloudFirstOrchestrator(credential_env={"OPENROUTER_API_KEY": "runtime-only", "MEDIAHUB_OPENROUTER_MODEL": "openai/gpt-5.2"})
    d = o.decide("coding")
    assert d.provider_id == "openrouter"
    assert d.tier == "cloud"
    assert d.model == "openai/gpt-5.2"
