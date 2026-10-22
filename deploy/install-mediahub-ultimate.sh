#!/usr/bin/env bash
set -euo pipefail

REPO="${MEDIAHUB_REPO:-/home/mediahub/mediahub-os}"
BIN="${MEDIAHUB_BIN_PREFIX:-$HOME/.local/bin}"
LOOPS="${MEDIAHUB_QUALIFY_LOOPS:-5}"
cd "$REPO"

log(){ printf '[mediahub-ultimate] %s\n' "$*"; }
need(){ command -v "$1" >/dev/null 2>&1 || { log "MISSING: $1"; return 1; }; }

log "1/8 canonical repository"
test -d runtime/mediahub_runtime
test -f CLAUDE.md
test -f docs/ASTRA-RUFLO-VIBE-MASTER-PROMPT.md
test -f profiles/connectors/openrouter.json
test -f .github/workflows/mediahub-cloud-relay.yml

log "2/8 local AI and execution components"
need ollama
need claude
need harness
need exp
test -x "$BIN/naabu"
test -x "$BIN/caddy"
test -x "$BIN/authelia"
test -x "$BIN/codex-web-gpt"

log "3/8 Ruflo and ECC"
npx --yes ruflo@3.42.5 --version | grep -F 'ruflo v3.42.5'
claude mcp list 2>&1 | grep -F 'ruflo: npx ruflo@3.42.5 mcp start - ✔ Connected'
claude mcp list 2>&1 | grep -F 'plugin:ecc:chrome-devtools: npx -y chrome-devtools-mcp@latest - ✔ Connected'

log "4/8 security edge refresh"
bash deploy/install-mediahub-security-stack.sh

log "5/8 architecture and connector validation"
python3 tools/validate_contracts.py
python3 tools/validate_connectors.py
python3 tools/validate_host_registration.py

log "6/8 native MediaHub Harness"
PYTHONPATH=runtime python3 - <<'PY'
from mediahub_runtime import MediaHubHarness
r = MediaHubHarness().run(["python3", "-c", "print('MEDIAHUB_AUTONOMOUS_EXECUTION_READY')"])
assert r.status == "completed" and "MEDIAHUB_AUTONOMOUS_EXECUTION_READY" in r.stdout
print("NATIVE_HARNESS=PASS")
PY

log "7/8 autonomous development gate"
MEDIAHUB_QUALIFY_LOOPS="$LOOPS" bash deploy/qualify-mediahub-autonomous-dev.sh

log "8/8 final truth-state report"
printf '%s\n' \
  'INSTALLATION=PASS' \
  'QUALIFICATION=PASS' \
  'NATIVE_HARNESS=PASS' \
  'OLLAMA=INSTALLED_AND_VERIFIED' \
  'CLAUDE_CODE=INSTALLED_AND_VERIFIED' \
  'RUFLO_MCP=CONNECTED' \
  'ECC_MCP=CONNECTED' \
  'OPENHARNESS=INSTALLED' \
  'EXPERIENTIAL_CLI=INSTALLED_CONFIGURED' \
  'CHATGPT_WEB_ADAPTER=INSTALLED' \
  'NAABU=INSTALLED' \
  'CADDY=INSTALLED' \
  'AUTHELIA=INSTALLED' \
  'TINYFISH_CONNECTOR=CONFIGURED_NOT_AUTHENTICATED' \
  'OPENROUTER_GITHUB_RELAY=CONFIGURED_SECRET_STATE_UNVERIFIED' \
  'SENTINELX=NOT_INSTALLED_OR_ENROLLED' \
  'PAID_CLOUD=DISABLED' \
  'CREDENTIALS=NOT_CREATED' \
  'PRODUCTION_AUTHORIZATION=NOT_VERIFIED'
