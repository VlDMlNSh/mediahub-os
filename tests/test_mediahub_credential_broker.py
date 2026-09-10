import pytest

from ops.mediahub_credential_broker import CredentialBroker, CredentialDenied


def test_broker_is_fail_closed(tmp_path):
    broker = CredentialBroker(tmp_path, frozenset({"openai"}))
    with pytest.raises(CredentialDenied):
        broker.resolve("openai")


def test_resolve_returns_reference_without_secret(tmp_path):
    path = tmp_path / "mediahub-openai"
    path.write_text("SECRET", encoding="utf-8")
    path.chmod(0o600)
    broker = CredentialBroker(tmp_path, frozenset({"openai"}))
    broker.authorize()
    ref = broker.resolve("openai")
    assert ref.provider == "openai"
    assert ref.path == path
    assert not hasattr(ref, "value")


def test_provider_and_permission_bounds(tmp_path):
    path = tmp_path / "mediahub-openai"
    path.write_text("SECRET", encoding="utf-8")
    path.chmod(0o644)
    broker = CredentialBroker(tmp_path, frozenset({"openai"}))
    broker.authorize()
    with pytest.raises(CredentialDenied):
        broker.resolve("unknown")
    with pytest.raises(CredentialDenied):
        broker.resolve("openai")


def test_empty_and_symlink_credentials_denied(tmp_path):
    empty = tmp_path / "mediahub-openai"
    empty.write_text("", encoding="utf-8")
    empty.chmod(0o600)
    broker = CredentialBroker(tmp_path, frozenset({"openai"}))
    broker.authorize()
    with pytest.raises(CredentialDenied):
        broker.resolve("openai")
    empty.unlink()
    target = tmp_path / "secret"
    target.write_text("SECRET", encoding="utf-8")
    target.chmod(0o600)
    empty.symlink_to(target)
    with pytest.raises(CredentialDenied):
        broker.resolve("openai")


def test_revoke_is_terminal(tmp_path):
    broker = CredentialBroker(tmp_path, frozenset({"openai"}))
    broker.revoke()
    with pytest.raises(CredentialDenied):
        broker.resolve("openai")
