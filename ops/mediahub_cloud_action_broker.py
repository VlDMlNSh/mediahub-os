"""GitHub Actions broker for cloud AI lanes.

Cloud provider credentials stay inside GitHub Actions secrets. The MediaHub
runtime sends only non-secret task metadata through the GitHub CLI/API.
"""
from __future__ import annotations

import re
import subprocess
from dataclasses import dataclass


SAFE = re.compile(r"^[A-Za-z0-9._:/-]{1,160}$")
WORKFLOW = "mediahub-cloud-development-agent.yml"


@dataclass(frozen=True)
class CloudDispatch:
    provider: str
    task_id: str
    capability: str
    ref: str
    execution_id: str
    generation: int
    operation_key: str


def _safe(value: str, name: str) -> str:
    if not SAFE.fullmatch(value):
        raise ValueError(f"invalid {name}")
    return value


def dispatch(plan: CloudDispatch, *, repository: str = "VlDMlNSh/mediahub-os") -> str:
    provider = _safe(plan.provider, "provider")
    task_id = _safe(plan.task_id, "task_id")
    capability = _safe(plan.capability, "capability")
    ref = _safe(plan.ref, "ref")
    execution_id = _safe(plan.execution_id, "execution_id")
    operation_key = _safe(plan.operation_key, "operation_key")
    if not isinstance(plan.generation, int) or plan.generation < 1:
        raise ValueError("invalid generation")
    repo = _safe(repository, "repository")
    cmd = [
        "gh", "workflow", "run", WORKFLOW,
        "--repo", repo,
        "--ref", ref,
        "-f", f"provider={provider}",
        "-f", f"task_id={task_id}",
        "-f", f"capability={capability}",
        "-f", f"target_ref={ref}",
        "-f", f"execution_id={execution_id}",
        "-f", f"generation={plan.generation}",
        "-f", f"operation_key={operation_key}",
    ]
    result = subprocess.run(cmd, check=False, capture_output=True, text=True, timeout=20)
    if result.returncode != 0:
        raise RuntimeError("GitHub Actions dispatch failed")
    return result.stdout.strip() or "DISPATCHED"
