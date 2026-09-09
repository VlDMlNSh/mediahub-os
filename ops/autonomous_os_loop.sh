#!/usr/bin/env bash
set -euo pipefail
ROOT="/home/mediahub/dev/mediahub-os-autonomous"
STATE="$ROOT/.autonomous"
LOGDIR="$STATE/logs"
LOCKFILE="$STATE/loop.lock"
HEARTBEAT="$STATE/heartbeat.log"
PIDFILE="$STATE/loop.pid"
STOPFILE="$STATE/STOP"
mkdir -p "$LOGDIR"
exec 9>"$LOCKFILE"
flock -n 9 || exit 73
echo $$ >"$PIDFILE"
trap 'rm -f "$PIDFILE"' EXIT
export MEDIAHUB_ROOT="$ROOT"
export MEDIAHUB_LOCAL_MODEL="/home/mediahub/local-ai/models/qwen2.5-coder-1.5b-instruct-q4_k_m.gguf"
export MEDIAHUB_LLAMA_CLI="/home/mediahub/local-ai/bin/llama-cli"
MAX=900
SLEEP=5
CYCLE=BOOT
LAST_RESULT=STARTING
(while :; do
	printf "STATE=RUNNING\nCYCLE=%s\nHEAD=%s\nLAST_RESULT=%s\nMODEL=%s\nTIMESTAMP=%s\n" "$(cat "$STATE/current_cycle" 2>/dev/null || echo BOOT)" "$(git -C "$ROOT" rev-parse HEAD 2>/dev/null || echo UNKNOWN)" "$(cat "$STATE/current_result" 2>/dev/null || echo STARTING)" "$MEDIAHUB_LOCAL_MODEL" "$(date -u +%FT%TZ)" >"$HEARTBEAT.tmp"
	mv -f "$HEARTBEAT.tmp" "$HEARTBEAT"
	sleep 5
done) &
HEARTBEAT_PID=$!
trap 'kill "$HEARTBEAT_PID" 2>/dev/null || true; rm -f "$PIDFILE"' EXIT INT TERM
while [ ! -e "$STOPFILE" ]; do
	STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
	CYCLE="$STAMP"
	LAST_RESULT=RUNNING
	LOG="$LOGDIR/local-cycle-$STAMP.log"
	printf "%s\n" "$CYCLE" >"$STATE/current_cycle"
	printf "RUNNING\n" >"$STATE/current_result"
	{
		echo "=== MEDIAHUB LOCAL AUTONOMOUS CYCLE $STAMP ==="
		cd "$ROOT"
		echo "MODE=LOCAL_ONLY"
		echo "HEAD=$(git rev-parse HEAD)"
		echo "TREE=$(git rev-parse 'HEAD^{tree}')"
		git merge-base --is-ancestor 471f709f5633feab7aeb62dd3ea52effad6d2bc4 HEAD
		test "$(git status --porcelain)" = ""
		set +e
		timeout --signal=TERM --kill-after=20s "${MAX}s" ./ops/local_autonomous_agent.py
		RC=$?
		set -e
		echo "LOCAL_AGENT_RC=$RC"
		echo "POST_HEAD=$(git rev-parse HEAD)"
		echo "POST_TREE=$(git rev-parse 'HEAD^{tree}')"
		echo "POST_STATUS:"
		git status --short --branch
		if [ "$RC" -eq 0 ]; then LAST_RESULT=PASS; else LAST_RESULT=FAIL; fi
		printf "%s\n" "$LAST_RESULT" >"$STATE/current_result"
		echo "CYCLE_RESULT=$LAST_RESULT"
	} >>"$LOG" 2>&1 || true
	sleep "$SLEEP"
done
