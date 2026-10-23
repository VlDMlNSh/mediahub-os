#!/usr/bin/env python3
"""Create a deterministic, secret-free manifest for a downloaded Gemini output artifact.

This helper only reads files from an already downloaded GitHub Actions artifact.
It does not execute model output, access provider credentials, or contact any service.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from pathlib import Path
from typing import Any


TARGET_SHA_RE = re.compile(r"^[0-9a-f]{40}$")
RESULTS = {"success", "failure", "cancelled", "skipped"}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def build_manifest(
    artifact_root: Path,
    *,
    repository: str,
    workflow_file: str,
    run_id: str,
    run_attempt: str,
    dispatch_id: str,
    target_sha: str,
    task_job_result: str,
) -> dict[str, Any]:
    if not TARGET_SHA_RE.fullmatch(target_sha):
        raise ValueError("target SHA must be 40 lowercase hexadecimal characters")
    if not repository or "/" not in repository:
        raise ValueError("repository must be owner/name")
    if not workflow_file.startswith(".github/workflows/"):
        raise ValueError("workflow_file must be a repository-relative workflow path")
    if not run_id.isdigit() or not run_attempt.isdigit():
        raise ValueError("run ID and run attempt must be numeric")
    if not re.fullmatch(r"[0-9a-fA-F-]{36}", dispatch_id):
        raise ValueError("dispatch ID must be a UUID-shaped correlation identifier")
    if task_job_result not in RESULTS:
        raise ValueError("task job result is outside the allowed status vocabulary")
    if artifact_root.is_symlink() or not artifact_root.is_dir():
        raise ValueError("artifact root must be an existing non-symlink directory")

    records: list[dict[str, Any]] = []
    total_size = 0
    for path in sorted(artifact_root.rglob("*"), key=lambda p: p.as_posix()):
        if path.is_symlink():
            raise ValueError("artifact contains a symlink; refusing ambiguous provenance")
        if not path.is_file():
            continue
        relative = path.relative_to(artifact_root).as_posix()
        if relative.startswith("/") or ".." in Path(relative).parts:
            raise ValueError("artifact path escapes its root")
        size = path.stat().st_size
        records.append({"path": relative, "size_bytes": size, "sha256": sha256_file(path)})
        total_size += size

    if not records:
        raise ValueError("downloaded Gemini artifact contains no regular files")

    return {
        "schema": "mediahub-gemini-output-provenance/v1",
        "source": {
            "repository": repository,
            "workflow_file": workflow_file,
            "workflow_run_id": run_id,
            "workflow_run_attempt": run_attempt,
            "dispatch_id": dispatch_id,
            "target_sha": target_sha,
        },
        "task_job_result": task_job_result,
        "artifact": {
            "name": "gemini-output",
            "file_count": len(records),
            "total_size_bytes": total_size,
            "files": records,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--artifact-root", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    try:
        manifest = build_manifest(
            args.artifact_root,
            repository=os.environ.get("GITHUB_REPOSITORY", ""),
            workflow_file=os.environ.get("MEDIAHUB_WORKFLOW_FILE", ""),
            run_id=os.environ.get("GITHUB_RUN_ID", ""),
            run_attempt=os.environ.get("GITHUB_RUN_ATTEMPT", ""),
            dispatch_id=os.environ.get("MEDIAHUB_DISPATCH_ID", ""),
            target_sha=os.environ.get("MEDIAHUB_TARGET_SHA", ""),
            task_job_result=os.environ.get("MEDIAHUB_TASK_JOB_RESULT", ""),
        )
        output = args.output
        if output.resolve().is_relative_to(args.artifact_root.resolve()):
            raise ValueError("manifest output must be outside the source artifact directory")
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(
            json.dumps(manifest, sort_keys=True, separators=(",", ":")) + "\n",
            encoding="utf-8",
        )
    except (OSError, ValueError) as exc:
        print(f"PROVENANCE_MANIFEST_FAILED: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 2

    print(
        "PROVENANCE_MANIFEST_CREATED "
        f"files={manifest['artifact']['file_count']} "
        f"bytes={manifest['artifact']['total_size_bytes']} "
        f"target_sha={manifest['source']['target_sha']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
