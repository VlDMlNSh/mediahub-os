#!/usr/bin/env bash
set -euo pipefail
ROOT="/home/mediahub/dev/mediahub-os-autonomous"
STATE="$ROOT/.autonomous"
LOCKFILE="$STATE/loop.lock"
mkdir -p "$STATE"
exec 9>"$LOCKFILE"
flock -n 9 || exit 73
export MEDIAHUB_ROOT="$ROOT"
exec /usr/bin/python3 "$ROOT/ops/local_autonomous_agent.py"
