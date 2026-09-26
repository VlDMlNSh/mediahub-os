import pytest

from ops.ai.ai_adapter import AdapterDenied, AIAdapter, ProviderRequest


def test_default_is_fail_closed():
    with pytest.raises(AdapterDenied):
        AIAdapter().admit(ProviderRequest(task_id="t1"))


@pytest.mark.parametrize("capability", ["production", "secrets", "state-authority", "host-filesystem"])
def test_forbidden_capabilities_are_denied(capability):
    adapter = AIAdapter()
    adapter.authorize()
    with pytest.raises(AdapterDenied):
        adapter.admit(ProviderRequest(task_id="t1", capabilities=frozenset({capability})))


def test_egress_is_explicitly_allowlisted():
    adapter = AIAdapter()
    adapter.authorize(frozenset({"unix://alamo"}))
    adapter.admit(ProviderRequest(task_id="t1", egress=frozenset({"unix://alamo"})))
    with pytest.raises(AdapterDenied):
        adapter.admit(ProviderRequest(task_id="t2", egress=frozenset({"https://example.invalid"})))


def test_timeout_is_bounded():
    adapter = AIAdapter()
    adapter.authorize()
    with pytest.raises(AdapterDenied):
        adapter.admit(ProviderRequest(task_id="t1", timeout_seconds=0))
    with pytest.raises(AdapterDenied):
        adapter.admit(ProviderRequest(task_id="t2", timeout_seconds=901))


def test_revocation_is_terminal():
    adapter = AIAdapter()
    adapter.authorize()
    adapter.revoke()
    with pytest.raises(AdapterDenied):
        adapter.admit(ProviderRequest(task_id="t1"))
    with pytest.raises(AdapterDenied):
        adapter.authorize()


def test_provenance_is_bound_to_task_and_sha():
    adapter = AIAdapter()
    result = adapter.provenance(ProviderRequest(task_id="t1"), "abc123")
    assert result["task_id"] == "t1"
    assert result["source_sha"] == "abc123"
    assert result["adapter"] == "mediahub.provider-neutral.v1"
