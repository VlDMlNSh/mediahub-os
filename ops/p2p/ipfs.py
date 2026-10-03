from __future__ import annotations
from pathlib import Path
import shutil
from ops.mesh.artifacts import VerificationResult, verify_artifact

class TransportUnavailable(RuntimeError):
    pass

def ipfs_available() -> bool:
    return shutil.which("ipfs") is not None

def resolve_cid(cid: str) -> str:
    if not ipfs_available():
        raise TransportUnavailable("ipfs binary unavailable")
    if not cid or any(ch.isspace() for ch in cid):
        raise ValueError("invalid cid")
    return cid

def fetch_cid(cid: str, destination: Path) -> Path:
    resolve_cid(cid)
    raise NotImplementedError("live IPFS fetch requires an explicit transport policy")

def verify_cid_artifact(path: Path, expected_sha256: str) -> VerificationResult:
    return verify_artifact(path, expected_sha256)
