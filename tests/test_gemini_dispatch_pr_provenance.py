"""Adversarial tests for dispatch-owned Gemini branch and PR provenance."""
import unittest
from scripts.validate_gemini_dispatch_pr import expected_branch, validate_dispatch_pr

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
            "base": {"ref": "main"},
        }],
        {"ref": f"refs/heads/{BRANCH}", "object": {"sha": "b" * 40}},
        {"created_at": "2026-11-15T18:00:00Z"},
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
        with self.assertRaisesRegex(ValueError, "repository mismatch"):
            self.validate(prs=prs)

    def test_wrong_base_fails(self):
        prs, _, _ = fixtures()
        prs[0]["base"]["ref"] = "develop"
        with self.assertRaisesRegex(ValueError, "base must be main"):
            self.validate(prs=prs)

    def test_branch_ref_sha_must_match_pr_head_sha(self):
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


if __name__ == "__main__":
    unittest.main()
