"""Strict post-Gemini validation for dispatch-owned branches and PRs."""
import argparse
from datetime import datetime, timezone
import re
import sys
import uuid

ROLE_PREFIXES = {
    "agent-1": "agent-1-contour-a",
    "agent-2": "agent-2-contract-verification",
    "agent-3": "agent-3-security-audit",
}


def expected_branch(role, dispatch_id):
    if role not in ROLE_PREFIXES:
        raise ValueError("unknown agent role")
    parsed = uuid.UUID(dispatch_id)
    if parsed.version != 4 or str(parsed) != dispatch_id:
        raise ValueError("dispatch_id must be canonical UUIDv4")
    return f"{ROLE_PREFIXES[role]}-{dispatch_id}"


def _timestamp(value):
    if not isinstance(value, str):
        raise ValueError("timestamp missing")
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def validate_dispatch_pr(role, dispatch_id, repository, branch_name, prs, ref, run):
    expected = expected_branch(role, dispatch_id)
    if branch_name != expected:
        raise ValueError("branch does not match current dispatch ID")
    if not isinstance(prs, list) or len(prs) != 1:
        raise ValueError("expected exactly one PR for the dispatch branch")
    pr = prs[0]
    head = pr.get("head") or {}
    base = pr.get("base") or {}
    head_repo = head.get("repo") or {}
    ref_object = (ref or {}).get("object") or {}
    if head.get("ref") != expected:
        raise ValueError("PR head branch does not match current dispatch")
    if head_repo.get("full_name") != repository:
        raise ValueError("PR head repository mismatch")
    if base.get("ref") != "main":
        raise ValueError("PR base must be main")
    if head.get("sha") != ref_object.get("sha"):
        raise ValueError("PR head SHA does not match dispatch branch ref")
    if pr.get("state") != "open" or pr.get("draft") is not True or pr.get("merged_at") is not None:
        raise ValueError("dispatch PR must be open, draft, and unmerged")
    if _timestamp(pr.get("created_at")) < _timestamp((run or {}).get("created_at")):
        raise ValueError("PR predates this workflow dispatch")
    return True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--role", required=True, choices=tuple(ROLE_PREFIXES))
    parser.add_argument("--dispatch-id", required=True)
    parser.add_argument("--repository", required=True)
    parser.add_argument("--branch", required=True)
    parser.add_argument("--prs", required=True)
    parser.add_argument("--ref", required=True)
    parser.add_argument("--run", required=True)
    args = parser.parse_args()
    import json
    from pathlib import Path
    try:
        validate_dispatch_pr(
            args.role, args.dispatch_id, args.repository, args.branch,
            json.loads(Path(args.prs).read_text()),
            json.loads(Path(args.ref).read_text()),
            json.loads(Path(args.run).read_text()),
        )
    except (ValueError, KeyError, TypeError) as exc:
        print(f"::error::Dispatch PR provenance validation failed: {exc}")
        return 1
    print("Dispatch branch and PR provenance validated against UUID, repository, base, branch SHA, and run time.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
