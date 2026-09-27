from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parents[1]))

import pytest
from ops.astra_capability_registry import register_mac_xcode
from runtime.mediahub_control_plane.agent_registry import AgentRegistry
from runtime.mediahub_control_plane.model import AgentStatus


def manifest(**overrides):
    value = {
        "schema_version": 3,
        "lane": "mac-xcode",
        "platform": "Darwin",
        "architecture": "arm64",
        "qualified": True,
        "reason": "QUALIFIED",
        "xcode_version": "Xcode 16.2",
        "capabilities": ["ios_build", "ios_test", "xcodebuild"],
    }
    value.update(overrides)
    return value


def test_register_mac_xcode_uses_manifest_as_capability_evidence():
    registry = AgentRegistry()
    agent = register_mac_xcode(registry, manifest(), "df3-node")
    assert agent.agent_id == "df3-mac-xcode"
    assert agent.node_id == "df3-node"
    assert agent.status is AgentStatus.IDLE
    assert agent.architecture == "arm64"
    assert agent.version == "Xcode 16.2"
    assert agent.capabilities == ("ios_build", "ios_test", "xcodebuild")


@pytest.mark.parametrize("overrides", [
    {"schema_version": 2},
    {"lane": "linux"},
    {"platform": "Linux"},
    {"architecture": "x86_64"},
    {"qualified": False},
    {"reason": "NO_BOOTED_SIMULATOR"},
    {"capabilities": []},
])
def test_register_mac_xcode_rejects_unqualified_or_invalid_manifest(overrides):
    with pytest.raises(ValueError):
        register_mac_xcode(AgentRegistry(), manifest(**overrides), "df3-node")


def test_register_mac_xcode_requires_explicit_node_identity():
    with pytest.raises(ValueError):
        register_mac_xcode(AgentRegistry(), manifest(), "")
