from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path
from typing import Any
import re

HEX64 = re.compile(r"^[0-9a-fA-F]{64}$")

@dataclass(frozen=True)
class VerificationResult:
    verified: bool
    sha256: str
    size: int
    reason: str = ""

def compute_sha256(path: Path) -> str:
    digest = sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()

def verify_artifact(path: Path, expected_sha256: str) -> VerificationResult:
    if not HEX64.fullmatch(expected_sha256):
        return VerificationResult(False, "", path.stat().st_size, "invalid expected sha256")
    actual = compute_sha256(path)
    size = path.stat().st_size
    if actual.lower() != expected_sha256.lower():
        return VerificationResult(False, actual, size, "sha256 mismatch")
    return VerificationResult(True, actual, size)

def validate_artifact_manifest(manifest: dict[str, Any]) -> bool:
    required = {"schema_version","artifact_id","sha256","size","type","origin","transport","replicas","verification_state"}
    return isinstance(manifest, dict) and required.issubset(manifest) and manifest.get("schema_version") == "mediahub.mesh.artifact.v1" and bool(HEX64.fullmatch(str(manifest.get("sha256", ""))))

def admit_verified_artifact(manifest: dict[str, Any], verification: VerificationResult) -> bool:
    return validate_artifact_manifest(manifest) and verification.verified and verification.sha256.lower() == str(manifest["sha256"]).lower() and verification.size == int(manifest["size"])
