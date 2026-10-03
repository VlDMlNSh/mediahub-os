from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import shutil
import subprocess
from ops.mesh.artifacts import VerificationResult, verify_artifact

@dataclass(frozen=True)
class TorrentMetadata:
    path: Path
    sha256: str | None = None

def _torrent_creator() -> str:
    tool = shutil.which("transmission-create") or shutil.which("transmission-create-cli")
    if not tool:
        raise RuntimeError("torrent creator unavailable; install transmission-cli on the execution node")
    return tool

def publish_torrent(artifact_path: Path, output_path: Path) -> TorrentMetadata:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run([_torrent_creator(), "-o", str(output_path), str(artifact_path)], check=True, capture_output=True, text=True)
    return TorrentMetadata(output_path)

def inspect_torrent(torrent_path: Path) -> TorrentMetadata:
    if not torrent_path.is_file():
        raise FileNotFoundError(torrent_path)
    return TorrentMetadata(torrent_path)

def verify_download(path: Path, expected_sha256: str) -> VerificationResult:
    return verify_artifact(path, expected_sha256)
