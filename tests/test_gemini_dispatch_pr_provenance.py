"""Adversarial tests for dispatch-owned Gemini branch and PR provenance."""
import unittest
from pathlib import Path
from scripts.validate_gemini_dispatch_pr import (
    expected_branch, validate_dispatch_pr, validate_live_dispatch,
)

DISPATCH = "123e4567-e89b-42d3-a456-426614174000"
REPOSITORY = "VlDMlNSh/mediahub-os"
BRANCH = f"agent-1-contour-a-{DISPATCH}"


def fixtures():
    return (
        [{
            "state": "open", "draft": True, "merged_at": None,
            "created_at": "2026-11-15T18:00:01Z",
            "head": {"ref": BRANCH, "sha": "b" * 40,
                     "repo": {"full_name": REPOSITORY}},
            "base": {"ref": "main", "repo": {"full_name": REPOSITORY}},
        }],
        {"ref": f"refs/heads/{BRANCH}", "object": {"sha": "b" * 40}},
        {
            "created_at": "2026-11-15T18:00:00Z",
            "event": "workflow_dispatch",
            "head_branch": "main",
            "repository": {"full_name": REPOSITORY},
        },
    )


class DispatchPRProvenanceTests(unittest.TestCase):
    def validate(self, prs=None, ref=None, run=None, branch=BRANCH, dispatch=DISPATCH):
        good_prs, good_ref, good_run = fixtures()
        return validate_dispatch_pr(
            "agent-1", dispatch, REPOSITORY, branch,
            good_prs if prs is None else prs,
            good_ref if ref is None else ref,
            good_run if run is None else run,
        )

    def test_role_branch_is_bound_to_uuidv4_dispatch(self):
        self.assertEqual(expected_branch("agent-1", DISPATCH), BRANCH)
        self.assertTrue(expected_branch("agent-2", DISPATCH).startswith("agent-2-contract-verification-"))
        self.assertTrue(expected_branch("agent-3", DISPATCH).startswith("agent-3-security-audit-"))
        with self.assertRaisesRegex(ValueError, "UUIDv4"):
            expected_branch("agent-1", "123e4567-e89b-12d3-a456-426614174000")

    def test_valid_dispatch_pr_passes(self):
        self.assertTrue(self.validate())

    def test_wrong_dispatch_or_reused_branch_fails(self):
        with self.assertRaisesRegex(ValueError, "branch does not match"):
            self.validate(branch="agent-1-contour-a-123e4567-e89b-42d3-a456-426614174001")
        prs, ref, run = fixtures()
        prs[0]["head"]["ref"] = "agent-1-contour-a-old-dispatch"
        with self.assertRaisesRegex(ValueError, "head branch"):
            self.validate(prs=prs)

    def test_wrong_head_repository_fails(self):
        prs, _, _ = fixtures()
        prs[0]["head"]["repo"]["full_name"] = "attacker/fork"
        with self.assertRaisesRegex(ValueError, "head/base repository"):
            self.validate(prs=prs)

    def test_wrong_base_fails(self):
        prs, _, _ = fixtures()
        prs[0]["base"]["ref"] = "develop"
        with self.assertRaisesRegex(ValueError, "base must be main"):
            self.validate(prs=prs)

    def test_branch_ref_name_and_sha_must_match_pr_head(self):
        _, ref, _ = fixtures()
        ref["ref"] = "refs/heads/reused-branch"
        with self.assertRaisesRegex(ValueError, "Git ref"):
            self.validate(ref=ref)
        _, ref, _ = fixtures()
        ref["object"]["sha"] = "c" * 40
        with self.assertRaisesRegex(ValueError, "SHA does not match"):
            self.validate(ref=ref)

    def test_exactly_one_open_draft_pr_is_required(self):
        prs, _, _ = fixtures()
        with self.assertRaisesRegex(ValueError, "exactly one"):
            self.validate(prs=[])
        with self.assertRaisesRegex(ValueError, "exactly one"):
            self.validate(prs=prs + prs)
        prs[0]["draft"] = False
        with self.assertRaisesRegex(ValueError, "open, draft"):
            self.validate(prs=prs)

    def test_preexisting_pr_is_rejected_by_run_timestamp(self):
        prs, _, run = fixtures()
        prs[0]["created_at"] = "2026-11-15T17:59:59Z"
        with self.assertRaisesRegex(ValueError, "predates"):
            self.validate(prs=prs, run=run)

    def test_untrusted_run_context_fails(self):
        _, _, run = fixtures()
        run["head_branch"] = "pull/123/merge"
        with self.assertRaisesRegex(ValueError, "trusted main"):
            self.validate(run=run)

    def test_each_child_workflow_invokes_role_bound_live_validator(self):
        root = Path(__file__).resolve().parents[1]
        workflows = {
            ".github/workflows/gemini-autonomous-engineering.yml": "agent-1",
            ".github/workflows/gemini-agent-2.yml": "agent-2",
            ".github/workflows/gemini-agent-3.yml": "agent-3",
        }
        for path, role in workflows.items():
            content = (root / path).read_text()
            self.assertIn("validate_gemini_dispatch_pr.py", content)
            self.assertIn("--role " + role, content)
            self.assertIn("--dispatch-id", content)
            self.assertIn("--run-id", content)

    def test_live_api_reconciles_exact_endpoints_without_logging_credentials(self):
        prs, ref, run = fixtures()
        seen = []
        def fake_get(path, token):
            seen.append((path, token))
            if "/git/ref/" in path:
                return ref
            if "/pulls?" in path:
                return prs
            if "/actions/runs/" in path:
                return run
            raise AssertionError("unexpected API path")
        self.assertTrue(validate_live_dispatch("agent-1", DISPATCH, REPOSITORY, "12345", "test-token", fake_get))
        self.assertEqual(len(seen), 3)
        self.assertTrue(all(item[1] == "test-token" for item in seen))


if __name__ == "__main__":
    unittest.main()
