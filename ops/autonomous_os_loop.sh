#!/usr/bin/env bash
set -euo pipefail
ROOT="/home/mediahub/dev/mediahub-os-autonomous"
STATE="$ROOT/.autonomous"
LOGDIR="$STATE/logs"
PIDFILE="$STATE/loop.pid"
STOPFILE="$STATE/STOP"
mkdir -p "$LOGDIR"
echo $$ > "$PIDFILE"
trap 'rm -f "$PIDFILE"' EXIT
export MEDIAHUB_ROOT="$ROOT"
export MEDIAHUB_LOCAL_MODEL="/home/mediahub/local-ai/models/qwen2.5-coder-1.5b-instruct-q4_k_m.gguf"
export MEDIAHUB_LLAMA_CLI="/home/mediahub/local-ai/bin/llama-cli"
MAX=900
while [ ! -e "$STOPFILE" ]; do
  STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
  LOG="$LOGDIR/local-cycle-$STAMP.log"
  {
    echo "=== MEDIAHUB LOCAL AUTONOMOUS CYCLE $STAMP ==="
    cd "$ROOT"
    echo "MODE=LOCAL_ONLY"
    echo "HEAD=$(git rev-parse HEAD)"
    echo "TREE=$(git rev-parse HEAD^{tree})"
    git merge-base --is-ancestor 471f709f5633feab7aeb62dd3ea52effad6d2bc4 HEAD
    test "$(git status --porcelain)" = ""
    timeout --signal=TERM --kill-after=20s "${MAX}s" ./ops/local_autonomous_agent.py
    RC=$?
    echo "LOCAL_AGENT_RC=$RC"
    echo "POST_HEAD=$(git rev-parse HEAD)"
    echo "POST_TREE=$(git rev-parse HEAD^{tree})"
    echo "POST_STATUS:"; git status --short --branch
  } >>"$LOG" 2>&1 || true
  sleep 30
done
