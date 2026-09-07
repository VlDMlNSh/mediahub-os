#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(git rev-parse --show-toplevel)"
cd "$REPO_ROOT"

IMMUTABLE="25f7e3e50708d4bcad37fa712a5000dd2a7dea06"

fail() { echo "PREFLIGHT_FAIL: $*" >&2; exit 1; }

[ -z "$(git status --porcelain)" ] || fail "worktree is dirty"

HEAD="$(git rev-parse HEAD)"
BRANCH="$(git rev-parse --abbrev-ref HEAD)"
echo "HEAD=$HEAD"
echo "BRANCH=$BRANCH"

git cat-file -e "$IMMUTABLE^{commit}" || fail "immutable forensic target unavailable"

grep -RInE 'class[[:space:]]+StateAuthority' runtime --exclude-dir='__pycache__' > /tmp/mh-state-authority.txt || true
COUNT="$(wc -l < /tmp/mh-state-authority.txt)"
[ "$COUNT" -eq 1 ] || fail "expected exactly one StateAuthority, found $COUNT"

grep -RInE 'sqlite|shelve|pickle|EventStore|CheckpointStore|Persistence|Recovery|socket|requests|urllib|subprocess|os\.system|write_text|write_bytes|json\.dump|yaml\.dump' runtime --exclude-dir='__pycache__' && fail "forbidden runtime surface detected" || true

PYTHONPATH=runtime:. python3 -m unittest discover -s tests -t . -p 'test_*.py' -q

git diff --check

echo "PREFLIGHT_RESULT=PASS"
