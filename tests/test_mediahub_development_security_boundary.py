import pytest

from ops.mediahub_credential_broker import CredentialBroker
from ops.mediahub_egress_controller import EgressController, EgressPolicy
from ops.mediahub_policy_engine import DevelopmentPolicy, PolicyEngine, PolicyRequest
from ops.mediahub_development_security_boundary import (
    DevelopmentBoundaryDenied,
    DevelopmentSecurityBoundary,
)


def build_boundary(tmp_path):
    credential = tmp_path / "mediahub-openai"
    credential.write_text("opaque-secret", encoding="utf-8")
    credential.chmod(0o600)
    return DevelopmentSecurityBoundary(
        policy=PolicyEngine(DevelopmentPolicy(
            providers=frozenset({"openai"}),
            protocols=frozenset({"openai.responses"}),
            data_classes=frozenset({"non-sensitive"}),
        )),
        egress=EgressController(EgressPolicy(frozenset({"https://api.openai.com"}))),
        credentials=CredentialBroker(tmp_path, frozenset({"openai"})),
    )


def request(**kwargs):
    values = dict(provider="openai", protocol="openai.responses",
                  data_class="non-sensitive", timeout_seconds=60, prompt_bytes=10)
    values.update(kwargs)
    return PolicyRequest(**values)


def test_composed_boundary_requires_authorization(tmp_path):
    boundary = build_boundary(tmp_path)
    with pytest.raises(DevelopmentBoundaryDenied):
        boundary.admit(request(), frozenset({"https://api.openai.com"}))


def test_composed_boundary_admits_only_policy_valid_task(tmp_path):
    boundary = build_boundary(tmp_path)
    boundary.authorize()
    boundary.admit(request(), frozenset({"https://api.openai.com"}))
    assert boundary.credential_ref("openai").name == "mediahub-openai"


def test_any_boundary_failure_denies(tmp_path):
    boundary = build_boundary(tmp_path)
    boundary.authorize()
    with pytest.raises(DevelopmentBoundaryDenied):
        boundary.admit(request(), frozenset({"https://evil.example"}))
    with pytest.raises(DevelopmentBoundaryDenied):
        boundary.admit(request(capabilities=frozenset({"production"})),
                        frozenset({"https://api.openai.com"}))


def test_revoke_is_global(tmp_path):
    boundary = build_boundary(tmp_path)
    boundary.authorize()
    boundary.revoke()
    with pytest.raises(DevelopmentBoundaryDenied):
        boundary.admit(request(), frozenset({"https://api.openai.com"}))
