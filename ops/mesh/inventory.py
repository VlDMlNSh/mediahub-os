from __future__ import annotations
import hashlib
from pathlib import Path
from typing import Any

def executable_identity_sha256(executable: str | Path) -> str:
    path = Path(executable)
    if not path.is_file():
        raise ValueError(f"executable is not a file: {path}")
    if not path.stat().st_size:
        raise ValueError(f"executable is empty: {path}")
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()

def capability_from_inventory(component: dict[str, Any], *, provider: str, capability_id: str, authority: str = "NONE", qualification_state: str | None = None) -> dict[str, Any]:
    executable = component.get("executable")
    if not isinstance(executable, str) or not executable:
        raise ValueError("inventory component requires an executable path")
    version = component.get("version")
    if not isinstance(version, str) or not version:
        raise ValueError("inventory component requires a version")
    if not provider or not capability_id:
        raise ValueError("provider and capability_id are required")
    if authority not in {"NONE", "CONTROL", "EXECUTION"}:
        raise ValueError("invalid authority")
    state = qualification_state or str(component.get("qualification_state", "DISCOVERED"))
    if not state:
        raise ValueError("qualification_state is required")
    return {"schema_version":"mediahub.mesh.capability.v1","capability_id":capability_id,"provider":provider,"version":version,"executable":executable,"identity_sha256":executable_identity_sha256(executable),"authority":authority,"qualification_state":state}
