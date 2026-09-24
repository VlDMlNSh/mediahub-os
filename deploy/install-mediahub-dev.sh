#!/usr/bin/env bash
set -euo pipefail
REPO="${MEDIAHUB_REPO:-/home/mediahub/mediahub-os}"
export MEDIAHUB_REPO="$REPO"
cd "$REPO"
printf '%s\n' '=== MediaHub DEV INSTALL ==='
printf 'HOST='; hostname
printf 'REPO=%s\n' "$REPO"
printf '%s\n' '--- PREFLIGHT ---'
bash deploy/preflight-mediahub-dev.sh
printf '%s\n' '--- ULTIMATE INSTALL / QUALIFICATION ---'
MEDIAHUB_QUALIFY_LOOPS="${MEDIAHUB_QUALIFY_LOOPS:-5}" bash deploy/install-mediahub-ultimate.sh
printf '%s\n' '=== MEDIAHUB DEV INSTALL COMPLETE ==='
