from __future__ import annotations
from dataclasses import dataclass
from typing import Any
from .validators import validate_capability

@dataclass(frozen=True)
class AdmissionResult:
    admitted: bool
    reason: str = ""

def admit_executor(node: dict[str, Any], capability: dict[str, Any], policy: dict[str, Any]) -> AdmissionResult:
    if node.get("status") != "ACTIVE":
        return AdmissionResult(False, "node is not active")
    if not node.get("node_id") or not node.get("role"):
        return AdmissionResult(False, "node identity or role missing")
    cv = validate_capability(capability)
    if not cv.valid:
        return AdmissionResult(False, cv.reason)
    if capability.get("authority") not in {"NONE","EXECUTION"}:
        return AdmissionResult(False, "unsupported capability authority")
    if policy.get("provider_selection") is False and capability.get("capability_id") in {"openflux","ecc"}:
        return AdmissionResult(False, "auxiliary capability cannot select provider")
    if policy.get("credential_creation") is False and capability.get("capability_id") in {"openflux","ecc"}:
        # This flag prevents an auxiliary provider from becoming a credential authority.
        if capability.get("creates_credentials"):
            return AdmissionResult(False, "auxiliary capability cannot create credentials")
    if policy.get("qualification_required", True) and capability.get("qualification_state") not in {"QUALIFIED","PASS"}:
        return AdmissionResult(False, "qualification required")
    return AdmissionResult(True)
