"""Filesystem-only lifecycle boundary for Cloud Development workloads.

This module deliberately does not claim to provide kernel/network isolation.
Those controls remain infrastructure responsibilities outside the adapter.
"""
from __future__ import annotations

import secrets
import shutil
from dataclasses import dataclass
from pathlib import Path

MARKER = ".mediahub-cloud-sandbox"


class SandboxDenied(PermissionError):
    """Raised when a sandbox lifecycle operation is unsafe."""


@dataclass(frozen=True)
class CloudDevelopmentSandbox:
    root: Path
    worktree: Path
    marker: Path

    @classmethod
    def create(cls, parent: Path) -> CloudDevelopmentSandbox:
        parent = Path(parent)
        if parent.exists() and parent.is_symlink():
            raise SandboxDenied("sandbox parent must not be a symlink")
        parent.mkdir(parents=True, exist_ok=True)
        if not parent.is_dir():
            raise SandboxDenied("sandbox parent must be a directory")
        for _ in range(8):
            token = secrets.token_hex(16)
            root = parent / f"mh-cloud-{token}"
            try:
                root.mkdir(mode=0o700)
                break
            except FileExistsError:
                continue
        else:
            raise SandboxDenied("could not allocate unique sandbox")
        worktree = root / "worktree"
        worktree.mkdir(mode=0o700)
        marker = root / MARKER
        marker.write_text(token, encoding="ascii")
        return cls(root=root, worktree=worktree, marker=marker)

    def validate(self) -> None:
        if self.root.is_symlink() or self.worktree.is_symlink() or self.marker.is_symlink():
            raise SandboxDenied("sandbox paths must not be symlinks")
        root = self.root.resolve()
        worktree = self.worktree.resolve()
        marker = self.marker.resolve()
        if root == Path("/") or marker.parent != root:
            raise SandboxDenied("invalid sandbox ownership boundary")
        if worktree != root and root not in worktree.parents:
            raise SandboxDenied("worktree escapes sandbox root")
        if not root.is_dir() or not worktree.is_dir() or marker.parent != root:
            raise SandboxDenied("sandbox is incomplete")
        token = marker.read_text(encoding="ascii")
        if len(token) != 32 or any(c not in "0123456789abcdef" for c in token):
            raise SandboxDenied("sandbox ownership marker is invalid")

    def teardown(self) -> None:
        self.validate()
        shutil.rmtree(self.root)
        if self.root.exists():
            raise SandboxDenied("sandbox teardown did not complete")
