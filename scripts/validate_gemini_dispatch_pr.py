"""Strict post-Gemini validation for dispatch-owned branches and PRs."""
import argparse
from datetime import datetime
import json
import os
import re
import sys
import uuid
from urllib.parse import quote
from urllib.request import Request, urlopen

ROLE_PREFIXES = {
    "agent-1": "agent-1-contour-a",
    "agent-2": "agent-2-contract-verification",
    "agent-3": "agent-3-security-audit",
}
API = "https://api.github.com"


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
    if (ref or {}).get("ref") != f"refs/heads/{expected}":
        raise ValueError("Git ref does not match current dispatch branch")
    ref_object = (ref or {}).get("object") or {}
    ref_sha = ref_object.get("sha")
    if not isinstance(ref_sha, str) or not re.fullmatch(r"[0-9a-f]{40}", ref_sha):
        raise ValueError("branch ref does not contain a full commit SHA")
    if not isinstance(prs, list) or len(prs) != 1:
        raise ValueError("expected exactly one PR for the dispatch branch")
    pr = prs[0]
    head = pr.get("head") or {}
    base = pr.get("base") or {}
    head_repo = head.get("repo") or {}
    base_repo = base.get("repo") or {}
    if head.get("ref") != expected:
        raise ValueError("PR head branch does not match current dispatch")
    if head_repo.get("full_name") != repository or base_repo.get("full_name") != repository:
        raise ValueError("PR head/base repository mismatch")
    if base.get("ref") != "main":
        raise ValueError("PR base must be main")
    if head.get("sha") != ref_sha:
        raise ValueError("PR head SHA does not match dispatch branch ref")
    if pr.get("state") != "open" or pr.get("draft") is not True or pr.get("merged_at") is not None:
        raise ValueError("dispatch PR must be open, draft, and unmerged")
    if (run or {}).get("event") != "workflow_dispatch":
        raise ValueError("controller child must be a workflow_dispatch run")
    if (run or {}).get("head_branch") != "main":
        raise ValueError("child workflow must execute from trusted main")
    if ((run or {}).get("repository") or {}).get("full_name") != repository:
        raise ValueError("workflow run repository mismatch")
    if _timestamp(pr.get("created_at")) < _timestamp((run or {}).get("created_at")):
        raise ValueError("PR predates this workflow dispatch")
    return True


def _github_get(path, token):
    request = Request(
        API + path,
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": "Bearer " + token,
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "MediaHub-Gemini-Dispatch-Provenance-Validator",
        },
    )
    with urlopen(request, timeout=20) as response:
        return json.loads(response.read().decode("utf-8"))


def validate_live_dispatch(role, dispatch_id, repository, run_id, token, api_get=_github_get):
    if not token:
        raise ValueError("GITHUB_TOKEN unavailable; refusing unverified dispatch PR")
    branch = expected_branch(role, dispatch_id)
    owner = repository.split("/", 1)[0]
    encoded_branch = quote(branch, safe="")
    ref = api_get(f"/repos/{repository}/git/ref/heads/{encoded_branch}", token)
    prs = api_get(
        f"/repos/{repository}/pulls?state=all&head={owner}:{branch}&base=main&per_page=100",
        token,
    )
    run = api_get(f"/repos/{repository}/actions/runs/{run_id}", token)
    return validate_dispatch_pr(role, dispatch_id, repository, branch, prs, ref, run)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--role", required=True, choices=tuple(ROLE_PREFIXES))
    parser.add_argument("--dispatch-id", required=True)
    parser.add_argument("--repository", required=True)
    parser.add_argument("--run-id", required=True)
    args = parser.parse_args()
    try:
        validate_live_dispatch(
            args.role, args.dispatch_id, args.repository, args.run_id,
            os.environ.get("GITHUB_TOKEN", ""),
        )
    except Exception as exc:
        # Never print request headers, token material, or raw HTTP response bodies.
        print(f"::error::Dispatch PR provenance validation failed: {type(exc).__name__}: {exc}")
        return 1
    print("Dispatch PR provenance verified: exact UUID branch, trusted-main run, one new draft PR, same repository, main base, and matching branch/PR SHA.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
