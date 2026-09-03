"""P0-08 capability declaration/request tests."""

import pytest

from mediahub_runtime.plugin_capabilities import (
    CapabilityDeclaration,
    CapabilityRequest,
    PluginCapabilityError,
    capability_operation,
)
from mediahub_runtime.plugin_manifest import PluginManifest


def manifest():
    return PluginManifest.from_mapping(
        {
            "schema_version": "1",
            "plugin_id": "example.plugin",
            "display_name": "Example",
            "plugin_version": "1.0.0",
            "api_version": "1",
            "declared_capabilities": ["media.read", "media.update"],
            "resource_limits": {},
            "metadata": {},
        }
    )


def test_declaration_does_not_grant_authority():
    declaration = CapabilityDeclaration.from_manifest(manifest())
    assert declaration.plugin_id == "example.plugin"
    assert declaration.capabilities == frozenset({"media.read", "media.update"})


def test_declared_request_matches_exact_identity_and_capability():
    declaration = CapabilityDeclaration.from_manifest(manifest())
    request = CapabilityRequest("example.plugin", "media.read", "read")
    assert request.is_declared_by(declaration)


def test_undeclared_capability_is_not_declared():
    declaration = CapabilityDeclaration.from_manifest(manifest())
    request = CapabilityRequest("example.plugin", "media.delete", "delete")
    assert not request.is_declared_by(declaration)


def test_operation_mismatch_is_rejected():
    with pytest.raises(PluginCapabilityError):
        CapabilityRequest("example.plugin", "media.read", "update")


def test_wildcard_is_rejected():
    with pytest.raises(PluginCapabilityError):
        CapabilityRequest("example.plugin", "media.*", "read")


def test_invalid_declaration_type_is_rejected():
    with pytest.raises(PluginCapabilityError):
        CapabilityDeclaration.from_manifest(object())


def test_capability_operation_is_canonical_suffix():
    assert capability_operation("media.update") == "update"
