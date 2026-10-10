#!/usr/bin/env python3
"""Produce a sanitized, fail-closed summary of autonomous queue execution.

The script is run after the queue has returned. It never stores command output,
credentials, environment values, prompts, or raw worker artifacts in the summary.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

EXECUTOR_POOL = {
    "mh-dev-01": "claude",
    "mh-dev-02": "claude",
    "Voktors-Mac-mini.local": "claude",
}
DIGEST_RE = re.compile(r"sha256:[0-9a-f]{64}\Z")
SHA_RE = re.compile(r"[0-9a-f]{40}\Z")


def build_summary(raw: object, queue_returncode: int, command_id: str, target_sha: str) -> dict:
    """Validate raw queue output and return only whitelisted evidence fields."""
    raw_dict = raw if isinstance(raw, dict) else {}
    source_results = raw_dict.get("results", [])
    source_results = source_results if isinstance(source_results, list) else []
    selected = raw_dict.get("selected_tasks", [])
    selected = selected if isinstance(selected, list) and all(isinstance(x, str) for x in selected) else []
    sanitized_results: list[dict] = []
    all_results_valid = True

    for item in source_results:
        if not isinstance(item, dict):
            all_results_valid = False
            continue
        push = item.get("push_verification")
        push = push if isinstance(push, dict) else {}
        verifier = item.get("independent_verifier")
        verifier = verifier if isinstance(verifier, dict) else {}
        run_id = item.get("worker_run_id", "")
        if type(run_id) is int and run_id > 0:
            run_id = str(run_id)
        elif not isinstance(run_id, str):
            run_id = ""
        row = {
            key: item.get(key) for key in (
                "task_id", "command_id", "base_sha", "target_sha", "node_id", "executor",
                "verifier_identity", "status", "worker_run_status", "worker_conclusion",
                "branch", "head_sha", "remote_head", "change_status", "evidence_digest",
            )
        }
        row["worker_run_id"] = run_id
        row["push_verification"] = {
            key: push.get(key) for key in ("status", "branch", "remote_sha")
        }
        row["independent_verifier"] = {
            "status": verifier.get("status"),
            "returncode": verifier.get("returncode"),
        }
        sanitized_results.append(row)

        head_sha = row.get("head_sha")
        branch = row.get("branch")
        if push.get("status") == "PASS":
            push_binding_valid = (
                isinstance(branch, str) and bool(branch)
                and push.get("branch") == branch
                and isinstance(head_sha, str) and SHA_RE.fullmatch(head_sha) is not None
                and row.get("remote_head") == head_sha
                and push.get("remote_sha") == head_sha
            )
        elif push.get("status") == "NOT_REQUIRED":
            push_binding_valid = (
                item.get("change_status") == "NO_CHANGES_REQUIRED"
                and head_sha == target_sha
                and isinstance(branch, str) and bool(branch)
                and push.get("branch") == branch
            )
        else:
            push_binding_valid = False
        row_valid = (
            isinstance(item.get("task_id"), str) and bool(item.get("task_id"))
            and item.get("status") == "VERIFIED"
            and item.get("command_id") == command_id
            and item.get("base_sha") == target_sha
            and item.get("target_sha") == target_sha
            and item.get("node_id") in EXECUTOR_POOL
            and item.get("executor") == EXECUTOR_POOL.get(item.get("node_id"))
            and item.get("verifier_identity") == item.get("executor")
            and isinstance(run_id, str) and run_id.isdigit()
            and item.get("worker_run_status") == "completed"
            and item.get("worker_conclusion") == "success"
            and isinstance(item.get("evidence_digest"), str)
            and DIGEST_RE.fullmatch(item["evidence_digest"]) is not None
            and verifier.get("status") == "PASS"
            and type(verifier.get("returncode")) is int and verifier.get("returncode") == 0
            and not item.get("error")
            and not item.get("claim_release_error")
            and push_binding_valid
        )
        all_results_valid = all_results_valid and row_valid

    raw_workers = raw_dict.get("workers", 0)
    workers = raw_workers if type(raw_workers) is int else 0
    raw_max_claims = raw_dict.get("max_parallel_claims", 0)
    max_claims = raw_max_claims if type(raw_max_claims) is int else 0
    valid_selected = bool(selected) and len(selected) == len(set(selected))
    binding_valid = (
        isinstance(raw, dict)
        and raw_dict.get("status") == "PASS"
        and raw_dict.get("command_id") == command_id
        and raw_dict.get("base_sha") == target_sha
        and raw_dict.get("mode") == "github_remote_claude_only"
        and raw_dict.get("executor_pool") == EXECUTOR_POOL
        and type(queue_returncode) is int and queue_returncode == 0
        and workers >= 1 and workers <= len(EXECUTOR_POOL)
        and workers == len(sanitized_results)
        and max_claims >= workers and max_claims <= len(EXECUTOR_POOL)
        and valid_selected
        and [row.get("task_id") for row in sanitized_results] == selected
        and all_results_valid
    )
    return {
        "schema": "mediahub.astra.autonomous-queue-summary.v1",
        "status": "PASS" if binding_valid else "BLOCKED",
        "command_id": command_id,
        "base_sha": target_sha,
        "mode": raw_dict.get("mode") if isinstance(raw, dict) else None,
        "workers": workers,
        "executor_pool": EXECUTOR_POOL,
        "max_parallel_claims": max_claims,
        "selected_tasks": selected,
        "results": sanitized_results,
        "queue_returncode": queue_returncode,
        "failure_code": None if binding_valid else "queue_or_evidence_validation_failed",
    }


def _last_json_line(path: Path) -> object:
    try:
        lines = [line for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
        return json.loads(lines[-1]) if lines else {}
    except (OSError, UnicodeError, json.JSONDecodeError, IndexError):
        return {}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--returncode", required=True, type=int)
    parser.add_argument("--command-id", required=True)
    parser.add_argument("--target-sha", required=True)
    args = parser.parse_args(argv)
    summary = build_summary(
        _last_json_line(args.source), args.returncode, args.command_id, args.target_sha
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("ASTRA_QUEUE_CONTROLLER_SUMMARY=" + json.dumps({
        "status": summary["status"],
        "command_id": summary["command_id"],
        "base_sha": summary["base_sha"],
        "workers": summary["workers"],
        "results": [
            {key: item.get(key) for key in ("task_id", "status", "node_id", "worker_conclusion")}
            for item in summary["results"]
        ],
        "failure_code": summary["failure_code"],
    }, sort_keys=True))
    return 0 if summary["status"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
