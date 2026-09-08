#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
OUT="$ROOT/.autonomous/security"
mkdir -p "$OUT"
cd "$ROOT"
git status --short --branch > "$OUT/git-status.txt"
python3 -m compileall -q runtime tests > "$OUT/compile.log" 2>&1
PYTHONPATH=runtime:. python3 -m pytest -q > "$OUT/pytest.log" 2>&1
PYTHONPATH=runtime:. python3 -m pytest -q tests/security > "$OUT/security-pytest.log" 2>&1
ruff check . > "$OUT/ruff.log" 2>&1
mypy runtime > "$OUT/mypy.log" 2>&1
semgrep --config p/python --error --metrics=off runtime tests > "$OUT/semgrep.log" 2>&1
bandit -r runtime -q > "$OUT/bandit.log" 2>&1
pip-audit > "$OUT/pip-audit.log" 2>&1
git diff --check > "$OUT/diff-check.log" 2>&1
printf 'SCAN_OK\nSHA=%s\nTREE=%s\n' "$(git rev-parse HEAD)" "$(git rev-parse HEAD^{tree})" > "$OUT/result.txt"
