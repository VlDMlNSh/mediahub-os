import pytest

from ops.mediahub_credential_broker import CredentialBroker
from ops.mediahub_model_registry import ModelRecord, ModelRegistry
from ops.mediahub_native_agent_launcher import (
    NativeAgentDenied,
    build_command,
    resolve_launch,
)


def test_codex_command_uses_native_cli_without_secret():
    command = build_command("codex", "qualified-codex-model", "do the task")
    assert command[1:3] == ("exec", "--json")
    assert "--model" in command
    assert "openrouter" not in " ".join(command).lower()
    assert "secret" not in " ".join(command).lower()


def test_claude_command_uses_native_cli_without_secret():
    command = build_command("claude", "qualified-claude-model", "do the task")
    assert command[1:3] == ("-p", "--output-format")
    assert "--model" in command
    assert "openrouter" not in " ".join(command).lower()


def test_unknown_agent_and_missing_model_fail_closed():
    with pytest.raises(NativeAgentDenied):
        build_command("unknown", "model", "task")
    with pytest.raises(NativeAgentDenied):
        build_command("codex", "", "task")


def test_launch_requires_qualified_model_and_broker(tmp_path):
    credential_dir = tmp_path / "credentials"
    credential_dir.mkdir()
    credential = credential_dir / "mediahub-openai"
    credential.write_text("synthetic-secret", encoding="utf-8")
    credential.chmod(0o600)
    broker = CredentialBroker(credential_dir, frozenset({"openai"}))
    broker.authorize()
    registry = ModelRegistry((ModelRecord("openai", "qualified-codex-model"),))
    spec, ref, endpoint = resolve_launch(
        "codex", broker, "https://api.openai.com/v1", "qualified-codex-model", registry
    )
    assert spec.provider == "openai"
    assert ref.path == credential
    assert endpoint == "https://api.openai.com/v1"


def test_non_https_endpoint_is_denied(tmp_path):
    broker = CredentialBroker(tmp_path, frozenset({"openai"}))
    registry = ModelRegistry((ModelRecord("openai", "m"),))
    with pytest.raises(NativeAgentDenied):
        resolve_launch("codex", broker, "http://127.0.0.1:1", "m", registry)


def test_missing_model_is_denied_by_registry(tmp_path):
    credential_dir = tmp_path / "credentials"
    credential_dir.mkdir()
    credential = credential_dir / "mediahub-openai"
    credential.write_text("synthetic-secret", encoding="utf-8")
    credential.chmod(0o600)
    broker = CredentialBroker(credential_dir, frozenset({"openai"}))
    broker.authorize()
    registry = ModelRegistry((ModelRecord("openai", "qualified"),))
    with pytest.raises(PermissionError):
        resolve_launch("codex", broker, "https://api.openai.com/v1", "unqualified", registry)
