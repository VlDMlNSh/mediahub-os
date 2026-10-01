from ops.mediahub_local_executor_control import LocalExecutorDenied, build_request, command_for
def test_default_commands_are_bounded(monkeypatch):
    monkeypatch.delenv("MEDIAHUB_CODEX_EXECUTOR",raising=False); monkeypatch.delenv("MEDIAHUB_CLAUDE_EXECUTOR",raising=False)
    assert command_for("codex")=="codex" and command_for("claude")=="claude"
def test_unknown_provider_denied():
    try: command_for("unknown")
    except LocalExecutorDenied: return
    raise AssertionError("unknown provider was accepted")
def test_identity_required():
    try: build_request("","codex","x","sha")
    except LocalExecutorDenied: return
    raise AssertionError("missing task identity was accepted")
