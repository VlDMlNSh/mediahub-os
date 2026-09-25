from __future__ import annotations
import json, time
from dataclasses import dataclass
from pathlib import Path
from runtime.mediahub_control_plane.agent_registry import AgentRegistry
from runtime.mediahub_control_plane.model import Agent, AgentStatus

@dataclass(frozen=True)
class ExecutorCapability:
    executor_id: str
    version: str
    capabilities: frozenset[str]
    status: str
    node_id: str
    trust_boundary: str
    transport: str

def capabilities_from_inventory(inventory: dict) -> tuple[ExecutorCapability, ...]:
    out=[]
    for row in inventory.get("executors", []):
        if row.get("qualification") != "QUALIFIED" or row.get("status") != "HEALTHY":
            continue
        out.append(ExecutorCapability(str(row["name"]), str(row.get("version","")), frozenset(row.get("capabilities",())), "QUALIFIED", str(inventory.get("host","unknown")), "LOCAL_TRUSTED", "local-cli"))
    return tuple(out)

def register_qualified(registry: AgentRegistry, inventory: dict) -> tuple[Agent, ...]:
    return tuple(registry.register(Agent(c.executor_id,c.node_id,c.version,AgentStatus.IDLE,tuple(sorted(c.capabilities)))) for c in capabilities_from_inventory(inventory))


MAC_XCODE_SCHEMA_VERSION = 3
MAC_XCODE_AGENT_ID = "df3-mac-xcode"

def register_mac_xcode(registry: AgentRegistry, manifest: dict, node_id: str, agent_id: str = MAC_XCODE_AGENT_ID) -> Agent:
    """Register one qualified macOS/Xcode lane using its existing lane manifest as evidence."""
    if not node_id:
        raise ValueError("node_id is required")
    if manifest.get("schema_version") != MAC_XCODE_SCHEMA_VERSION:
        raise ValueError("unsupported mac-xcode manifest schema")
    if manifest.get("lane") != "mac-xcode" or manifest.get("platform") != "Darwin":
        raise ValueError("invalid mac-xcode lane identity")
    if manifest.get("architecture") != "arm64":
        raise ValueError("unsupported mac-xcode architecture")
    if manifest.get("qualified") is not True or manifest.get("reason") != "QUALIFIED":
        raise ValueError("mac-xcode lane is not qualified")
    capabilities = tuple(sorted(set(str(x) for x in manifest.get("capabilities", ()))))
    if not capabilities:
        raise ValueError("qualified mac-xcode lane must advertise capabilities")
    return registry.register(Agent(agent_id, node_id, str(manifest.get("xcode_version") or ""), AgentStatus.IDLE, capabilities, manifest["architecture"]))

def routing_table(inventory: dict) -> dict[str, tuple[str,...]]:
    table={}
    for c in capabilities_from_inventory(inventory):
        for capability in c.capabilities:
            table.setdefault(capability,[]).append(c.executor_id)
    return {k:tuple(sorted(v)) for k,v in table.items()}

def read_inventory(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))

def build_evidence(inventory: dict) -> dict:
    return {"schema_version":1,"ts":time.time(),"qualified":[{"executor_id":c.executor_id,"version":c.version,"capabilities":sorted(c.capabilities),"node_id":c.node_id,"trust_boundary":c.trust_boundary,"transport":c.transport} for c in capabilities_from_inventory(inventory)]}
