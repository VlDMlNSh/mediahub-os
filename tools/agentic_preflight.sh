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

grep -RInE 'class[[:space:]]+StateAuthority' runtime --include='*.py' --exclude-dir='__pycache__' > /tmp/mh-state-authority.txt || true
COUNT="$(wc -l < /tmp/mh-state-authority.txt)"
[ "$COUNT" -eq 1 ] || fail "expected exactly one StateAuthority, found $COUNT"

python3 - <<'PY'
import ast
from pathlib import Path

forbidden_imports = {
    "sqlite", "sqlite3", "shelve", "pickle", "socket", "requests", "urllib",
    "subprocess", "yaml", "eventstore", "checkpointstore", "persistence", "recovery",
}
forbidden_calls = {
    "system", "write_text", "write_bytes", "dump",
}
forbidden_classes = {"EventStore", "CheckpointStore", "Persistence", "Recovery"}

violations = []
for path in Path("runtime").rglob("*.py"):
    if "__pycache__" in path.parts:
        continue
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except SyntaxError as exc:
        violations.append(f"{path}: syntax error: {exc}")
        continue
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                root = alias.name.split(".", 1)[0]
                if root in forbidden_imports:
                    violations.append(f"{path}:{node.lineno}: forbidden import {alias.name}")
        elif isinstance(node, ast.ImportFrom):
            root = (node.module or "").split(".", 1)[0]
            if root in forbidden_imports:
                violations.append(f"{path}:{node.lineno}: forbidden import from {node.module}")
        elif isinstance(node, ast.ClassDef) and node.name in forbidden_classes:
            violations.append(f"{path}:{node.lineno}: forbidden class {node.name}")
        elif isinstance(node, ast.Call):
            name = None
            if isinstance(node.func, ast.Name):
                name = node.func.id
            elif isinstance(node.func, ast.Attribute):
                name = node.func.attr
            if name in forbidden_calls:
                violations.append(f"{path}:{node.lineno}: forbidden call {name}")

if violations:
    print("\n".join(violations))
    raise SystemExit(1)
PY

PYTHONPATH=runtime:. python3 -m unittest discover -s tests -t . -p 'test_*.py' -q

git diff --check

echo "PREFLIGHT_RESULT=PASS"
