#!/usr/bin/env bash
set -euo pipefail
ROOT="/home/mediahub/dev/mediahub-os-autonomous"
export MEDIAHUB_ROOT="$ROOT"
exec "$ROOT/ops/autonomous_os_loop.sh"
