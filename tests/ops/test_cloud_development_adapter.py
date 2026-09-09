
import pytest

from ops.cloud_development_adapter import (
    AdapterDenied,
    CloudDevelopmentAdapter,
    ProviderProtocolError,
    ProviderRequest,
    SandboxSpec,
)


@pytest.fixture
def sandbox(tmp_path):
    root = tmp_path / "sandbox"
    worktree = root / "worktree"
    worktree.mkdir(parents=True)
    return SandboxSpec(root=root, worktree=worktree)


def request(provider="codex", **kwargs):
    values = {"task_id": "t1", "provider": provider, "prompt": "return HEALTHY",
              "source_sha": "471f709f5633feab7aeb62dd3ea52effad6d2bc4"}
    values.update(kwargs)
    return ProviderRequest(**values)


def test_default_is_fail_closed():
    with pytest.raises(AdapterDenied):
        CloudDevelopmentAdapter().admit(request())


def test_provider_neutral_codex_and_claude_are_allowlisted():
    adapter = CloudDevelopmentAdapter()
    adapter.authorize()
    adapter.admit(request("codex"))
    adapter.admit(request("claude"))


def test_provider_bypass_and_authority_escalation_are_denied():
    adapter = CloudDevelopmentAdapter()
    adapter.authorize()
    with pytest.raises(AdapterDenied):
        adapter.admit(request("unknown"))
    for capability in ("production", "secrets", "state-authority", "host-filesystem"):
        with pytest.raises(AdapterDenied):
            adapter.admit(request(capabilities=frozenset({capability})))


def test_egress_and_sensitive_data_are_denied():
    adapter = CloudDevelopmentAdapter()
    adapter.authorize(frozenset({"https://approved.example"}))
    with pytest.raises(AdapterDenied):
        adapter.admit(request(egress=frozenset({"https://unapproved.example"})))
    with pytest.raises(AdapterDenied):
        adapter.admit(request(data_class="secret"))


def test_missing_provenance_and_bad_timeout_are_denied():
    adapter = CloudDevelopmentAdapter()
    adapter.authorize()
    with pytest.raises(AdapterDenied):
        adapter.admit(request(source_sha=""))
    with pytest.raises(AdapterDenied):
        adapter.admit(request(timeout_seconds=901))


def test_unsafe_harness_flags_are_denied(sandbox):
    adapter = CloudDevelopmentAdapter()
    adapter.authorize()
    with pytest.raises(AdapterDenied):
        adapter.execute(request(), sandbox, ("python3", "--yolo"))


def test_execution_is_sandboxed_and_provider_neutral(sandbox):
    adapter = CloudDevelopmentAdapter()
    adapter.authorize()
    result = adapter.execute(request(), sandbox, ("python3", "-c", "print('BRIDGE_OK')"))
    assert result.status == "ok"
    assert result.output.strip() == "BRIDGE_OK"
    assert result.provenance["adapter_id"] == "mediahub.cloud-development-adapter.v1"
    assert result.provenance["provider"] == "codex"


def test_sandbox_escape_is_denied(tmp_path):
    root = tmp_path / "sandbox"
    root.mkdir()
    outside = tmp_path / "outside"
    outside.mkdir()
    adapter = CloudDevelopmentAdapter()
    adapter.authorize()
    spec = SandboxSpec(root=root, worktree=outside)
    with pytest.raises(AdapterDenied):
        adapter.execute(request(), spec, ("python3", "-c", "print('NO')"))


def test_output_limit_is_enforced(sandbox):
    adapter = CloudDevelopmentAdapter()
    adapter.authorize()
    small = SandboxSpec(root=sandbox.root, worktree=sandbox.worktree, max_output_bytes=4)
    with pytest.raises(ProviderProtocolError):
        adapter.execute(request(), small, ("python3", "-c", "print('TOO-LONG')"))


def test_timeout_and_revocation_fail_closed(sandbox):
    adapter = CloudDevelopmentAdapter()
    adapter.authorize()
    with pytest.raises(AdapterDenied):
        adapter.execute(request(timeout_seconds=1), sandbox,
                        ("python3", "-c", "import time; time.sleep(2)"))
    adapter.revoke()
    with pytest.raises(AdapterDenied):
        adapter.execute(request(), sandbox, ("python3", "-c", "print('NO')"))


def test_execute_provider_uses_allowlisted_wrapper_and_sandbox(tmp_path, monkeypatch):
    import ops.cloud_development_adapter as module

    wrapper = tmp_path / "provider-wrapper"
    wrapper.write_text("#!/bin/sh\nprintf '%s\\n' \"$2\"\n", encoding="utf-8")
    wrapper.chmod(0o700)
    monkeypatch.setitem(module.ENTRYPOINTS, "codex", wrapper)
    root = tmp_path / "sandbox"
    worktree = root / "worktree"
    worktree.mkdir(parents=True)
    adapter = CloudDevelopmentAdapter()
    adapter.authorize()
    result = adapter.execute_provider(request(), SandboxSpec(root=root, worktree=worktree))
    assert result.status == "ok"
    assert result.output.strip() == str(worktree)


def test_execute_provider_denies_missing_wrapper(sandbox, monkeypatch):
    import ops.cloud_development_adapter as module

    missing = sandbox.root / "missing-wrapper"
    monkeypatch.setitem(module.ENTRYPOINTS, "claude", missing)
    adapter = CloudDevelopmentAdapter()
    adapter.authorize()
    with pytest.raises(AdapterDenied):
        adapter.execute_provider(request("claude"), sandbox)
