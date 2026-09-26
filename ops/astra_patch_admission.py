from __future__ import annotations

import json
import subprocess
from dataclasses import dataclass
from pathlib import Path, PurePosixPath


class PatchAdmissionError(ValueError):
    pass


@dataclass(frozen=True)
class PatchFile:
    path: str
    operation: str
    patch: str


@dataclass(frozen=True)
class StructuredPatch:
    files: tuple[PatchFile, ...]

    @classmethod
    def from_json(cls, payload: str) -> "StructuredPatch":
        try:
            data = json.loads(payload)
        except json.JSONDecodeError as exc:
            raise PatchAdmissionError("proposal is not valid JSON") from exc
        if not isinstance(data, dict) or not isinstance(data.get("files"), list) or not data["files"]:
            raise PatchAdmissionError("proposal.files must be a non-empty array")
        files: list[PatchFile] = []
        for item in data["files"]:
            if not isinstance(item, dict):
                raise PatchAdmissionError("each file entry must be an object")
            path, operation, patch = item.get("path"), item.get("operation"), item.get("patch")
            if not isinstance(path, str) or not isinstance(operation, str) or not isinstance(patch, str):
                raise PatchAdmissionError("file entries require string path, operation and patch")
            files.append(PatchFile(path, operation, patch))
        return cls(tuple(files))


@dataclass(frozen=True)
class AdmissionResult:
    changed_files: tuple[str, ...]
    patch_bytes: int


def _matches(path: str, patterns: tuple[str, ...]) -> bool:
    candidate = PurePosixPath(path)
    return any(candidate.match(pattern) or path.startswith(pattern.rstrip("/") + "/") for pattern in patterns)


def _validate_path(path: str, *, allowed_paths: tuple[str, ...], forbidden_paths: tuple[str, ...]) -> None:
    if not path or "\\" in path or Path(path).is_absolute():
        raise PatchAdmissionError(f"invalid patch path: {path!r}")
    normalized = PurePosixPath(path)
    if normalized == PurePosixPath(".") or ".." in normalized.parts:
        raise PatchAdmissionError(f"path escape rejected: {path!r}")
    if _matches(path, forbidden_paths):
        raise PatchAdmissionError(f"forbidden path: {path}")
    if not _matches(path, allowed_paths):
        raise PatchAdmissionError(f"path outside allowed scope: {path}")


def _git(root: Path, *args: str) -> str:
    result = subprocess.run(["/usr/bin/git", "-C", str(root), *args], text=True, capture_output=True, check=False)
    if result.returncode:
        raise PatchAdmissionError(result.stderr.strip() or f"git {' '.join(args)} failed")
    return result.stdout.strip()


def admit_patch(
    proposal: StructuredPatch,
    root: str | Path,
    *,
    allowed_paths: tuple[str, ...],
    forbidden_paths: tuple[str, ...] = (),
    max_patch_bytes: int = 64_000,
    immutable_r4: str = "471f709f5633feab7aeb62dd3ea52effad6d2bc4",
) -> AdmissionResult:
    root = Path(root).resolve()
    if not proposal.files:
        raise PatchAdmissionError("empty patch")
    changed: list[str] = []
    total = 0
    for item in proposal.files:
        _validate_path(item.path, allowed_paths=allowed_paths, forbidden_paths=forbidden_paths)
        if item.operation != "modify":
            raise PatchAdmissionError(f"unsupported operation: {item.operation}")
        if not item.patch.startswith("diff --git "):
            raise PatchAdmissionError(f"file patch for {item.path} is not a unified git diff")
        total += len(item.patch.encode("utf-8"))
        changed.append(item.path)
    if total > max_patch_bytes:
        raise PatchAdmissionError("patch exceeds configured byte limit")
    if len(set(changed)) != len(changed):
        raise PatchAdmissionError("duplicate changed file")

    git_dir = root / ".git"
    if git_dir.exists():
        try:
            _git(root, "merge-base", "--is-ancestor", immutable_r4, "HEAD")
        except PatchAdmissionError as exc:
            raise PatchAdmissionError("immutable R4 ancestry check failed") from exc

    combined = "\n".join(item.patch.rstrip("\n") for item in proposal.files) + "\n"
    check = subprocess.run(
        ["/usr/bin/git", "-C", str(root), "apply", "--check", "--whitespace=error-all", "-"],
        input=combined,
        text=True,
        capture_output=True,
        check=False,
    )
    if check.returncode:
        raise PatchAdmissionError(check.stderr.strip() or "git apply --check rejected patch")
    apply = subprocess.run(
        ["/usr/bin/git", "-C", str(root), "apply", "--whitespace=error-all", "-"],
        input=combined,
        text=True,
        capture_output=True,
        check=False,
    )
    if apply.returncode:
        raise PatchAdmissionError(apply.stderr.strip() or "git apply rejected patch")
    if (root / ".git").exists():
        actual = tuple(line for line in _git(root, "diff", "--name-only").splitlines() if line)
        if set(actual) != set(changed):
            subprocess.run(["/usr/bin/git", "-C", str(root), "restore", "--", *actual], check=False)
            raise PatchAdmissionError(f"changed-file manifest mismatch: expected {changed}, got {actual}")
    return AdmissionResult(tuple(changed), total)
