"""P0-08 manifest contract tests."""

import pytest

from mediahub_runtime.plugin_manifest import PluginManifest, PluginManifestError


def valid_manifest():
    return {
        "schema_version": "1",
        "plugin_id": "example.plugin",
        "display_name": "Example",
        "plugin_version": "1.0.0",
        "api_version": "1",
        "declared_capabilities": ["media.read"],
        "resource_limits": {"message_bytes": 1024},
        "metadata": {"vendor": "example"},
    }


def test_valid_manifest_is_immutable_and_declarative():
    manifest = PluginManifest.from_mapping(valid_manifest())
    assert manifest.plugin_id == "example.plugin"
    assert manifest.declared_capabilities == frozenset({"media.read"})
    with pytest.raises(TypeError):
        manifest.metadata["vendor"] = "other"


@pytest.mark.parametrize("field", ["unknown", "extra"])
def test_unknown_fields_are_rejected(field):
    raw = valid_manifest()
    raw[field] = "x"
    with pytest.raises(PluginManifestError):
        PluginManifest.from_mapping(raw)


def test_duplicate_capability_is_rejected():
    raw = valid_manifest()
    raw["declared_capabilities"] = ["media.read", "media.read"]
    with pytest.raises(PluginManifestError):
        PluginManifest.from_mapping(raw)


def test_wildcard_capability_is_rejected():
    raw = valid_manifest()
    raw["declared_capabilities"] = ["media.*"]
    with pytest.raises(PluginManifestError):
        PluginManifest.from_mapping(raw)


@pytest.mark.parametrize("capability", ["media.network", "media.shell", "media.credentials"])
def test_forbidden_capability_terms_are_rejected(capability):
    raw = valid_manifest()
    raw["declared_capabilities"] = [capability]
    with pytest.raises(PluginManifestError):
        PluginManifest.from_mapping(raw)


def test_oversized_plugin_id_is_rejected():
    raw = valid_manifest()
    raw["plugin_id"] = "x" * 129
    with pytest.raises(PluginManifestError):
        PluginManifest.from_mapping(raw)


def test_resource_limit_is_non_negative_integer():
    raw = valid_manifest()
    raw["resource_limits"] = {"message_bytes": -1}
    with pytest.raises(PluginManifestError):
        PluginManifest.from_mapping(raw)
