from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import hashlib
import shutil
import subprocess
from ops.mesh.artifacts import VerificationResult, verify_artifact

@dataclass(frozen=True)
class TorrentMetadata:
    path: Path
    sha256: str | None = None

def _bencode(value: object) -> bytes:
    if isinstance(value, int):
        return f"i{value}e".encode()
    if isinstance(value, bytes):
        return str(len(value)).encode() + b":" + value
    if isinstance(value, str):
        return _bencode(value.encode())
    if isinstance(value, dict):
        items = sorted(value.items(), key=lambda item: str(item[0]).encode())
        return b"d" + b"".join(_bencode(str(k)) + _bencode(v) for k, v in items) + b"e"
    if isinstance(value, list):
        return b"l" + b"".join(_bencode(v) for v in value) + b"e"
    raise TypeError(f"unsupported bencode type: {type(value).__name__}")

def _write_minimal_torrent(artifact_path: Path, output_path: Path) -> None:
    data = artifact_path.read_bytes()
    piece_length = 16384
    pieces = b"".join(hashlib.sha1(data[i:i + piece_length]).digest() for i in range(0, len(data), piece_length))
    info = {"length": len(data), "name": artifact_path.name, "piece length": piece_length, "pieces": pieces}
    output_path.write_bytes(_bencode({"announce": "", "info": info}))

def _torrent_creator() -> str | None:
    return shutil.which("transmission-create") or shutil.which("transmission-create-cli")

def publish_torrent(artifact_path: Path, output_path: Path) -> TorrentMetadata:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    creator = _torrent_creator()
    if creator:
        subprocess.run([creator, "-o", str(output_path), str(artifact_path)], check=True, capture_output=True, text=True)
    else:
        _write_minimal_torrent(artifact_path, output_path)
    return TorrentMetadata(output_path)

def inspect_torrent(torrent_path: Path) -> TorrentMetadata:
    if not torrent_path.is_file():
        raise FileNotFoundError(torrent_path)
    return TorrentMetadata(torrent_path)

def verify_download(path: Path, expected_sha256: str) -> VerificationResult:
    return verify_artifact(path, expected_sha256)
