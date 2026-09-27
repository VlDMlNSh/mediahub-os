"""Capability adapter for the Kimi K3-in-C local engine.

The engine binary can be installed without the model checkpoint. Astra never
pretends the provider is available until a configured checkpoint is present.
"""
from __future__ import annotations

import os
import subprocess
from pathlib import Path


class KimiK3InCExecutor:
    provider_id = "kimi-k3-in-c"
    tier = "local"

    def __init__(self, binary: str | None = None, checkpoint: str | None = None, timeout: int = 300):
        self.binary = Path(binary or os.environ.get("MEDIAHUB_KIMI_K3_BINARY", "/home/mediahub/kimi-k3-in-c/bin/k3"))
        self.checkpoint = Path(checkpoint or os.environ.get("MEDIAHUB_KIMI_K3_CHECKPOINT", ""))
        self.timeout = max(30, min(int(timeout), 900))

    def available(self) -> bool:
        return self.binary.is_file() and self.binary.stat().st_mode & 0o111 and self.checkpoint.is_file()

    def __call__(self, prompt: str) -> str:
        if not self.available():
            raise RuntimeError("kimi_k3_checkpoint_unavailable")
        try:
            result = subprocess.run([str(self.binary), "--model", str(self.checkpoint), "--prompt", prompt], text=True, capture_output=True, timeout=self.timeout, check=False)
        except (OSError, subprocess.TimeoutExpired) as exc:
            raise RuntimeError("kimi_k3_execution_failed") from exc
        if result.returncode != 0 or not result.stdout.strip():
            raise RuntimeError("kimi_k3_execution_failed")
        return result.stdout.strip()

    def status(self) -> dict[str, object]:
        return {
            "provider_id": self.provider_id,
            "binary": str(self.binary),
            "binary_present": self.binary.is_file(),
            "checkpoint": str(self.checkpoint) if str(self.checkpoint) else None,
            "checkpoint_present": self.checkpoint.is_file(),
            "available": self.available(),
        }
