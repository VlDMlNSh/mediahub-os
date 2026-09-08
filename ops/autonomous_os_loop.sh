#!/usr/bin/env bash
set -euo pipefail
ROOT="/home/mediahub/dev/mediahub-os-autonomous"
LOCK="$ROOT/.autonomous/loop.lock"
LOGDIR="$ROOT/.autonomous/logs"
mkdir -p "$LOGDIR"
PIDFILE="$ROOT/.autonomous/loop.pid"
STOPFILE="$ROOT/.autonomous/STOP"
echo $$ > "$PIDFILE"
trap 'rm -f "$PIDFILE"' EXIT
MAX=3300
while [ ! -e "$STOPFILE" ]; do
  STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
  LOG="$LOGDIR/cycle-$STAMP.log"
  {
    echo "=== MEDIAHUB AUTONOMOUS CYCLE $STAMP ==="
    cd "$ROOT"
    git fetch origin ops/mh05-10lane-orchestration-v1
    git status --short --branch
    echo "HEAD=$(git rev-parse HEAD)"
    echo "TREE=$(git rev-parse HEAD^{tree})"
    echo "R4_GUARD=$(git cat-file -t 471f709f5633feab7aeb62dd3ea52effad6d2bc4)"
    timeout --signal=TERM --kill-after=30s "${MAX}s" codex exec -C "$ROOT" --approve-for-me --ephemeral 'You are the autonomous MediaHub OS engineering executor on mh-dev-01. Work only in this local repository and only on downstream commits from the current branch. Use the product passport, recovered master architecture, implementation map, governance documents, and existing tests as the source of truth. Goal: progressively generate the most complete working MediaHub OS/iOS product that is actually authorized by the repository governance state. Inspect before changing anything. Do not modify immutable R4 commit 471f709f5633feab7aeb62dd3ea52effad6d2bc4. Do not amend, rebase, reset, force-push, merge, or rewrite history. Build features in small verifiable increments. After every change run the narrowest relevant tests, then the full available verification and security scans; inspect failures, make the smallest safe downstream fix, and repeat until green or blocked. You may integrate mature GitHub projects only after checking license, maintenance, security posture, compatibility, pinning exact versions/commits, and adding provenance. Maintain authority integrity and fail-closed behavior. Do not unlock MH-06, production, release, or claim qualification/independence. Do not fabricate evidence. If a governance gate blocks an architectural stage, improve all safe preparatory work instead. Prefer existing repository architecture over invention. Produce real build/test artifacts where the product architecture calls for them. Leave the tree coherent and buildable. Commit completed downstream work with descriptive messages. Never claim a push occurred unless verified.'
    RC=$?
    echo "CODEX_RC=$RC"
    timeout --signal=TERM --kill-after=20s 600s ./ops/security_scan_local.sh || echo "SECURITY_SCAN_RC=$?"
    echo "FINAL_SHA=$(git rev-parse HEAD)"
    echo "FINAL_TREE=$(git rev-parse HEAD^{tree})"
    echo "FINAL_STATUS:"; git status --short --branch
  } >>"$LOG" 2>&1 || true
  sleep 30
done
