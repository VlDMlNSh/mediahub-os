#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LOOPS="${MEDIAHUB_QUALIFY_LOOPS:-3}"
EVIDENCE_DIR="${MEDIAHUB_EVIDENCE_DIR:-$ROOT/.mediahub/evidence/autonomous-dev}"

log(){ printf '[mediahub-autonomous] %s\n' "$*"; }
fail(){ log "FAIL: $*"; exit 1; }

cd "$ROOT"
mkdir -p "$EVIDENCE_DIR"

log "1/8 repository identity"
git rev-parse --show-toplevel | grep -Fx "$ROOT" >/dev/null
git diff --check

log "2/8 tracked-state and secret boundary"
if git diff --name-only | grep -E '(^|/)(\.env|.*\.pem|.*\.key|credentials|secrets?)($|[./])' >/dev/null; then
  fail "sensitive path appears in working-tree diff"
fi
if git diff --cached --name-only | grep -E '(^|/)(\.env|.*\.pem|.*\.key|credentials|secrets?)($|[./])' >/dev/null; then
  fail "sensitive path appears in index"
fi

log "3/8 contract and connector gates"
python3 tools/validate_contracts.py
python3 tools/validate_connectors.py
python3 tools/validate_host_registration.py

log "4/8 runtime regression"
PYTHONPATH=runtime python3 -m pytest -q

log "5/8 autonomous local execution"
PYTHONPATH=runtime python3 - <<'PY'
from mediahub_runtime import MediaHubHarness
r = MediaHubHarness().run(["python3", "-c", "print('MEDIAHUB_AUTONOMOUS_EXECUTION_READY')"])
assert r.status == "completed"
assert "MEDIAHUB_AUTONOMOUS_EXECUTION_READY" in r.stdout
print("AUTONOMOUS_EXECUTION=PASS")
PY

log "6/8 qualification stability"
for i in $(seq 1 "$LOOPS"); do
  log "qualification loop $i/$LOOPS"
  bash deploy/qualify-mediahub-reference-stack.sh >/tmp/mediahub-autonomous-qualify.log
  grep -q 'QUALIFICATION=PASS' /tmp/mediahub-autonomous-qualify.log
done

log "7/8 immutable evidence"
{
  printf 'timestamp_utc=%s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  printf 'repository=%s\n' "$(git remote get-url origin 2>/dev/null || printf unknown)"
  printf 'branch=%s\n' "$(git branch --show-current)"
  printf 'commit=%s\n' "$(git rev-parse HEAD)"
  printf 'qualification=PASS\n'
  printf 'autonomous_local_execution=PASS\n'
  printf 'credentials_created=NO\n'
  printf 'paid_cloud_enabled=NO\n'
  printf 'production_authorization=NOT_VERIFIED\n'
  printf 'sentinelx_enrollment=NOT_VERIFIED\n'
} > "$EVIDENCE_DIR/last-pass.env"
sha256sum "$EVIDENCE_DIR/last-pass.env" > "$EVIDENCE_DIR/last-pass.env.sha256"

log "8/8 mutation boundary"
printf '%s\n' 'AUTONOMOUS_DEV_GATE=PASS'
printf '%s\n' 'AUTO_COMMIT=DISABLED'
printf '%s\n' 'AUTO_PUSH=DISABLED'
printf '%s\n' 'CREDENTIAL_CREATION=DISABLED'
printf '%s\n' 'PAID_CLOUD=DISABLED'
printf '%s\n' 'PRODUCTION_DEPLOY=NOT_AUTHORIZED'
