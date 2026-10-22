#!/usr/bin/env bash
set -euo pipefail

# MediaHub OS unified bootstrap/qualification.
# Safe-by-default: no credentials, no paid cloud, no destructive git operations.
REPO="${MEDIAHUB_REPO:-/home/mediahub/mediahub-os}"
BIN="${MEDIAHUB_BIN_PREFIX:-$HOME/.local/bin}"
LOOPS="${MEDIAHUB_QUALIFY_LOOPS:-5}"

log(){ printf '[mediahub] %s\n' "$*"; }
fail(){ log "ERROR: $*"; exit 1; }

cd "$REPO"
[[ -d runtime/mediahub_runtime ]] || fail "MediaHub runtime missing"

log "1/9 component presence"
test -x "$BIN/naabu" || fail "Naabu missing"
test -x "$BIN/caddy" || fail "Caddy missing"
test -x "$BIN/authelia" || fail "Authelia missing"
test -f runtime/mediahub_runtime/astra_service.py || fail "Astra missing"
command -v claude >/dev/null || fail "Claude Code missing"
command -v exp >/dev/null || fail "Experiential CLI missing"

log "2/9 version verification"
"$BIN/naabu" -version >/dev/null
"$BIN/caddy" version >/dev/null
"$BIN/authelia" --version >/dev/null
claude mcp list >/dev/null
exp --help >/dev/null

log "3/9 local Ollama"
pgrep -x ollama >/dev/null || fail "Ollama process missing"
curl -fsS --max-time 3 http://127.0.0.1:11434/api/tags >/tmp/mediahub-ollama-tags.json
python3 - /tmp/mediahub-ollama-tags.json <<'PY'
import json,sys
d=json.load(open(sys.argv[1]))
names={m.get("name") for m in d.get("models",[])}
assert "qwen2.5-coder:3b" in names or "qwen2.5-coder-3b" in names
PY
rm -f /tmp/mediahub-ollama-tags.json

log "4/9 contracts/connectors/host"
python3 tools/validate_connectors.py
python3 tools/validate_host_registration.py
python3 tools/validate_contracts.py

log "5/9 Python runtime"
python3 -m compileall -q runtime tools
PYTHONPATH=runtime pytest -q

log "6/9 repository hygiene"
git diff --check

log "7/9 Claude/Ruflo boundary"
claude mcp list 2>&1 | grep -F 'ruflo: npx ruflo@3.42.5 mcp start - ✔ Connected' >/dev/null || fail "Ruflo MCP not connected"

log "8/9 security posture"
[[ ! -e .env ]] || fail ".env must not exist in repository root"
grep -R --exclude-dir=.git -nE 'sk-[A-Za-z0-9_-]{20,}|TINYFISH_API_KEY[[:space:]]*=' . 2>/dev/null && fail "possible credential in repository" || true
grep -F 'PAID_CLOUD_ENABLED=NO' deploy/install-mediahub-security-stack.sh >/dev/null

log "9/9 stability loop: $LOOPS iterations"
for i in $(seq 1 "$LOOPS"); do
  PYTHONPATH=runtime pytest -q >/tmp/mediahub-test.log
  grep -Eq '[0-9]+ passed' /tmp/mediahub-test.log || { cat /tmp/mediahub-test.log; fail "iteration $i failed"; }
  python3 tools/validate_connectors.py >/dev/null
  python3 tools/validate_host_registration.py >/dev/null
  python3 tools/validate_contracts.py >/dev/null
  log "loop $i/$LOOPS PASS"
done
rm -f /tmp/mediahub-test.log

log "QUALIFICATION=PASS"
log "AUTONOMOUS_LOCAL_CORE=PASS"
log "SECURITY_EDGE_BINARIES=PASS"
log "CREDENTIALS_CREATED=NO"
log "PAID_CLOUD_ENABLED=NO"
log "PRODUCTION_AUTHORIZATION=NOT_VERIFIED"
log "SENTINELX_ENROLLMENT=NOT_VERIFIED"
log "EXPERIENTIAL_LIVE_GATEWAY=NOT_VERIFIED"
