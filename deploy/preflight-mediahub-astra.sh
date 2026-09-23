#!/usr/bin/env bash
set -euo pipefail

REPO="/home/mediahub/mediahub-os"

fail() {
  echo "PREFLIGHT=FAIL: $1" >&2
  exit 1
}

[[ -d "$REPO" ]] || fail "repository missing: $REPO"
[[ -x /usr/bin/python3 ]] || fail "python3 missing"
[[ -x /bin/systemctl ]] || fail "systemd missing"

python3 - <<'PY' || exit 1
import json
from urllib.request import urlopen

try:
    with urlopen("http://127.0.0.1:11434/api/tags", timeout=3) as response:
        data = json.load(response)
except Exception as exc:
    print(f"PREFLIGHT=FAIL: ollama unavailable: {type(exc).__name__}")
    raise SystemExit(1)

names = {item.get("name") for item in data.get("models", [])}
if "qwen2.5-coder:3b" not in names:
    print("PREFLIGHT=FAIL: qwen2.5-coder:3b missing")
    raise SystemExit(1)

print("PREFLIGHT=OLLAMA_PASS")
PY

PYTHONPATH="$REPO/runtime" python3 "$REPO/tools/validate_contracts.py"
PYTHONPATH="$REPO/runtime" python3 "$REPO/tools/validate_connectors.py"
PYTHONPATH="$REPO/runtime" python3 -m compileall -q "$REPO/runtime" "$REPO/tools"
bash -n "$REPO/deploy/install-mediahub-astra.sh"

echo "PREFLIGHT=PASS"
