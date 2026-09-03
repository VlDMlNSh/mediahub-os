import pytest

from mediahub_runtime.authorization import AuthorizationContext, AuthorizationPolicy
from mediahub_runtime.plugin_authorization import PluginAuthorization
from mediahub_runtime.plugin_boundary import PluginBoundary, PluginRequest


def manifest():
    return {
        "schema_version": "1",
        "plugin_id": "example.plugin",
        "display_name": "Example",
        "plugin_version": "1.0.0",
        "api_version": "1",
        "declared_capabilities": ["media.read"],
        "resource_limits": {},
        "metadata": {},
    }


def setup():
    boundary = PluginBoundary()
    declaration = boundary.declare_capabilities(boundary.validate_manifest(manifest()))
    request = boundary.validate_request(
        declaration,
        PluginRequest("example.plugin", "media.read", "read", {}),
    )
    capability_request = __import__(
        "mediahub_runtime.plugin_capabilities", fromlist=["CapabilityRequest"]
    ).CapabilityRequest(request.plugin_id, request.capability, request.operation)
    return declaration, capability_request


def test_authorization_requires_explicit_grant():
    declaration, request = setup()
    auth = PluginAuthorization(AuthorizationPolicy())
    decision = auth.decide(
        declaration, request, AuthorizationContext("example.plugin", "media.read")
    )
    assert not decision.allowed


def test_authorization_accepts_matching_explicit_grant():
    declaration, request = setup()
    policy = AuthorizationPolicy({("example.plugin", "media.read", "read")})
    decision = PluginAuthorization(policy).decide(
        declaration, request, AuthorizationContext("example.plugin", "media.read")
    )
    assert decision.allowed


def test_authorization_rejects_forged_principal():
    declaration, request = setup()
    policy = AuthorizationPolicy({("example.plugin", "media.read", "read")})
    decision = PluginAuthorization(policy).decide(
        declaration, request, AuthorizationContext("forged.plugin", "media.read")
    )
    assert not decision.allowed
    assert decision.reason == "principal identity mismatch"


def test_authorization_rejects_capability_context_mismatch():
    declaration, request = setup()
    policy = AuthorizationPolicy({("example.plugin", "media.read", "read")})
    decision = PluginAuthorization(policy).decide(
        declaration, request, AuthorizationContext("example.plugin", "other.read")
    )
    assert not decision.allowed
    assert decision.reason == "capability context mismatch"


def test_authorization_rejects_undeclared_request():
    boundary = PluginBoundary()
    declaration = boundary.declare_capabilities(boundary.validate_manifest(manifest()))
    from mediahub_runtime.plugin_capabilities import CapabilityRequest

    request = CapabilityRequest("example.plugin", "media.update", "update")
    policy = AuthorizationPolicy({("example.plugin", "media.update", "update")})
    decision = PluginAuthorization(policy).decide(
        declaration, request, AuthorizationContext("example.plugin", "media.update")
    )
    assert not decision.allowed
    assert decision.reason == "capability not declared"


def test_require_fails_closed():
    declaration, request = setup()
    with pytest.raises(PermissionError):
        PluginAuthorization(AuthorizationPolicy()).require(
            declaration,
            request,
            AuthorizationContext("example.plugin", "media.read"),
        )
