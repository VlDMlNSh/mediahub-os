#!/usr/bin/env bash
set -euo pipefail

# MediaHub OS — single reference-stack installer.
# Safe-by-default. No credentials, paid cloud, destructive git operations,
# production deployment, or external authorization are performed.

REPO="${MEDIAHUB_REPO:-/home/mediahub/mediahub-os}"
cd "$REPO"

log(){ printf '[mediahub-bootstrap] %s\n' "$*"; }
fail(){ log "ERROR: $*"; exit 1; }

[[ -f deploy/install-mediahub-security-stack.sh ]] || fail "security installer missing"
[[ -f deploy/qualify-mediahub-reference-stack.sh ]] || fail "qualification script missing"

log "Installing/refreshing security edge components"
bash deploy/install-mediahub-security-stack.sh

log "Running reference-stack qualification"
MEDIAHUB_QUALIFY_LOOPS="${MEDIAHUB_QUALIFY_LOOPS:-5}"   bash deploy/qualify-mediahub-reference-stack.sh

log "Unified installation and qualification complete"
log "INSTALLATION=PASS"
log "QUALIFICATION=PASS"
log "CREDENTIALS_CREATED=NO"
log "PAID_CLOUD_ENABLED=NO"
