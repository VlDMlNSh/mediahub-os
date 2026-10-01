"""GitHub-transport execution entrypoint for the Astra local executor fabric.

The command consumes one immutable task JSON and emits one result JSON. The
caller is responsible for publishing the result to GitHub and for independent
A3 verification.
"""
from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from pathlib import Path

from runtime.mediahub_runtime.local_executor import ExecutorRequest, execute


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--task", required=True)
    parser.add_argument("--result", required=True)
    args = parser.parse_args()

    task_path = Path(args.task)
    result_path = Path(args.result)
    task = json.loads(task_path.read_text(encoding="utf-8"))

    request = ExecutorRequest(
        task_id=task["task_id"],
        claim_id=task["claim_id"],
        owner_id=task["owner_id"],
        generation=int(task["generation"]),
        target_sha=task["target_sha"],
        provider=task["provider"],
        workspace=Path(task["workspace"]),
        prompt=task["prompt"],
        timeout_seconds=int(task.get("timeout_seconds", 900)),
    )
    result = execute(request)
    result_path.parent.mkdir(parents=True, exist_ok=True)
    result_path.write_text(json.dumps(asdict(result), sort_keys=True, indent=2) + "\n", encoding="utf-8")
    return 0 if result.result_status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
