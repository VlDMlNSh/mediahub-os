from __future__ import annotations
from dataclasses import dataclass
from typing import Any
from .validators import validate_capability

@dataclass(frozen=True)
class AdmissionResult:
    admitted: bool
    reason: str = ""

AUXILIARY_CAPABILITIES = {"openflux", "ecc"}

def admit_executor(node: dict[str, Any], capability: dict[str, Any], policy: dict[str, Any]) -> AdmissionResult:
    if node.get("status") != "ACTIVE":
        return AdmissionResult(False, "node is not active")
    if not node.get("node_id") or not node.get("role"):
        return AdmissionResult(False, "node identity or role missing")
    cv = validate_capability(capability)
    if not cv.valid:
        return AdmissionResult(False, cv.reason)
    authority = capability.get("authority")
    if authority not in {"NONE", "EXECUTION"}:
        return AdmissionResult(False, "unsupported capability authority")
    cap_id = capability.get("capability_id")
    if cap_id in AUXILIARY_CAPABILITIES:
        if policy.get("provider_selection") is not False:
            return AdmissionResult(False, "auxiliary capability cannot select provider")
        if policy.get("credential_creation") is not False:
            return AdmissionResult(False, "auxiliary capability requires credential creation disabled")
        if capability.get("creates_credentials"):
            return AdmissionResult(False, "auxiliary capability cannot create credentials")
        if authority != "NONE":
            return AdmissionResult(False, "auxiliary capability authority must remain NONE")
    if policy.get("qualification_required", True) and capability.get("qualification_state") not in {"QUALIFIED", "PASS"}:
        return AdmissionResult(False, "qualification required")
    return AdmissionResult(True)
