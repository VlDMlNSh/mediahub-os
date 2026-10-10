from __future__ import annotations

from ops.qualification.validate_autonomous_queue_summary import EXECUTOR_POOL, build_summary


def valid_raw(command_id: str = "CMD-1", target_sha: str = "a" * 40) -> dict:
    head_sha = "b" * 40
    branch = "astra/MH25-QUEUE-001-CMD-1"
    result = {
        "task_id": "MH25-QUEUE-001",
        "command_id": command_id,
        "base_sha": target_sha,
        "target_sha": target_sha,
        "node_id": "mh-dev-01",
        "executor": "claude",
        "verifier_identity": "claude",
        "status": "VERIFIED",
        "worker_run_id": 123456,
        "worker_run_status": "completed",
        "worker_conclusion": "success",
        "branch": branch,
        "head_sha": head_sha,
        "remote_head": head_sha,
        "evidence_digest": "sha256:" + "c" * 64,
        "push_verification": {"status": "PASS", "branch": branch, "remote_sha": head_sha},
        "independent_verifier": {"status": "PASS", "returncode": 0},
        "error": "",
        "claim_release_error": "",
    }
    return {
        "status": "PASS",
        "command_id": command_id,
        "base_sha": target_sha,
        "mode": "github_remote_claude_only",
        "workers": 1,
        "executor_pool": dict(EXECUTOR_POOL),
        "max_parallel_claims": 3,
        "selected_tasks": ["MH25-QUEUE-001"],
        "results": [result],
        # These deliberately must not be copied to the output summary.
        "debug_stdout": "do not persist raw worker output",
        "secret_token": "NEVER_COPY_ME",
    }


def test_valid_queue_evidence_becomes_sanitized_pass_summary():
    summary = build_summary(valid_raw(), 0, "CMD-1", "a" * 40)
    assert summary["status"] == "PASS"
    assert summary["schema"] == "mediahub.astra.autonomous-queue-summary.v1"
    assert summary["workers"] == 1
    assert summary["results"][0]["worker_run_id"] == "123456"
    assert "secret_token" not in summary
    assert "debug_stdout" not in summary
    assert "error" not in summary["results"][0]
    assert "claim_release_error" not in summary["results"][0]


def test_nonzero_queue_exit_fails_closed_even_with_pass_shaped_payload():
    summary = build_summary(valid_raw(), 2, "CMD-1", "a" * 40)
    assert summary["status"] == "BLOCKED"
    assert summary["failure_code"] == "queue_or_evidence_validation_failed"


def test_wrong_command_or_target_sha_fails_closed():
    assert build_summary(valid_raw(), 0, "CMD-OTHER", "a" * 40)["status"] == "BLOCKED"
    assert build_summary(valid_raw(), 0, "CMD-1", "d" * 40)["status"] == "BLOCKED"


def test_wrong_worker_conclusion_or_verifier_fails_closed():
    raw = valid_raw()
    raw["results"][0]["worker_conclusion"] = "failure"
    assert build_summary(raw, 0, "CMD-1", "a" * 40)["status"] == "BLOCKED"
    raw = valid_raw()
    raw["results"][0]["independent_verifier"] = {"status": "BLOCKED", "returncode": 2}
    assert build_summary(raw, 0, "CMD-1", "a" * 40)["status"] == "BLOCKED"


def test_wrong_remote_head_or_branch_fails_closed():
    raw = valid_raw()
    raw["results"][0]["remote_head"] = "d" * 40
    assert build_summary(raw, 0, "CMD-1", "a" * 40)["status"] == "BLOCKED"
    raw = valid_raw()
    raw["results"][0]["push_verification"]["branch"] = "another-branch"
    assert build_summary(raw, 0, "CMD-1", "a" * 40)["status"] == "BLOCKED"


def test_missing_or_ambiguous_queue_result_fails_closed():
    assert build_summary({}, 0, "CMD-1", "a" * 40)["status"] == "BLOCKED"
    raw = valid_raw()
    raw["selected_tasks"] = ["OTHER"]
    assert build_summary(raw, 0, "CMD-1", "a" * 40)["status"] == "BLOCKED"
