#!/usr/bin/env python3
"""Read-only GitHub control-plane observer for the hybrid development loop."""
from __future__ import annotations

import json
import os
import time
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

REPO = os.environ.get("MEDIAHUB_GITHUB_REPO", "VlDMlNSh/mediahub-os")
BRANCH = os.environ.get("MEDIAHUB_GITHUB_BRANCH", "engineering/mh21-godmode-openrouter")
INTERVAL = max(15, int(os.environ.get("MEDIAHUB_SITE_POLL_SECONDS", "60")))
STATE = Path(os.environ.get("MEDIAHUB_ROOT", "/home/mediahub/dev/mediahub-os-autonomous")) / ".autonomous"
STATE.mkdir(parents=True, exist_ok=True)
REMOTE = STATE / "github_remote.json"


def fetch() -> dict:
    url = f"https://api.github.com/repos/{REPO}/branches/{BRANCH}"
    request = Request(url, headers={"Accept": "application/vnd.github+json", "User-Agent": "MediaHub-Hybrid-Observer/1"})
    with urlopen(request, timeout=10) as response:  # nosec B310 - fixed HTTPS GitHub endpoint
        payload = json.load(response)
    commit = payload.get("commit", {})
    return {
        "repo": REPO,
        "branch": BRANCH,
        "sha": commit.get("sha"),
        "updated_at": time.time(),
        "source": "github-api-readonly",
    }


def once() -> int:
    try:
        data = fetch()
    except (HTTPError, URLError, TimeoutError, OSError, ValueError) as exc:
        REMOTE.write_text(json.dumps({"state": "UNAVAILABLE", "error": type(exc).__name__, "updated_at": time.time()}, indent=2) + "\n", encoding="utf-8")
        return 2
    REMOTE.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    print(f"GITHUB_REMOTE=AVAILABLE repo={REPO} branch={BRANCH} sha={data['sha']}", flush=True)
    return 0


if __name__ == "__main__":
    if os.environ.get("MEDIAHUB_SITE_ONCE") == "1":
        raise SystemExit(once())
    while True:
        once()
        time.sleep(INTERVAL)
