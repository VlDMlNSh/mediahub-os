"""P0-08 plugin boundary negative and positive tests."""

import pytest

from mediahub_runtime.plugin_boundary import (
    MAX_PAYLOAD_DEPTH,
    PluginBoundary,
    PluginBoundaryError,
    PluginRequest,
)


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


def test_boundary_accepts_declared_inert_request():
    boundary = PluginBoundary()
    declaration = boundary.declare_capabilities(boundary.validate_manifest(manifest()))
    request = boundary.validate_request(
        declaration,
        PluginRequest("example.plugin", "media.read", "read", {"id": "x"}),
    )
    assert request.payload == {"id": "x"}


def test_boundary_rejects_undeclared_capability():
    boundary = PluginBoundary()
    declaration = boundary.declare_capabilities(boundary.validate_manifest(manifest()))
    with pytest.raises(PluginBoundaryError, match="capability_not_declared"):
        boundary.validate_request(
            declaration,
            PluginRequest("example.plugin", "media.update", "update", {}),
        )


def test_boundary_rejects_forged_plugin_identity():
    boundary = PluginBoundary()
    declaration = boundary.declare_capabilities(boundary.validate_manifest(manifest()))
    with pytest.raises(PluginBoundaryError):
        boundary.validate_request(
            declaration,
            PluginRequest("forged.plugin", "media.read", "read", {}),
        )


def test_boundary_rejects_excessive_depth():
    boundary = PluginBoundary()
    declaration = boundary.declare_capabilities(boundary.validate_manifest(manifest()))
    payload = "x"
    for _ in range(MAX_PAYLOAD_DEPTH + 1):
        payload = [payload]
    with pytest.raises(PluginBoundaryError, match="payload_limit_exceeded"):
        boundary.validate_request(
            declaration,
            PluginRequest("example.plugin", "media.read", "read", payload),
        )


def test_boundary_rejects_non_finite_float():
    boundary = PluginBoundary()
    declaration = boundary.declare_capabilities(boundary.validate_manifest(manifest()))
    with pytest.raises(PluginBoundaryError, match="payload_rejected"):
        boundary.validate_request(
            declaration,
            PluginRequest("example.plugin", "media.read", "read", {"x": float("inf")}),
        )


def test_observation_is_inert_and_bounded():
    observation = PluginBoundary().observation("example.plugin", "read", {"value": 1})
    assert observation.payload == {"value": 1}
