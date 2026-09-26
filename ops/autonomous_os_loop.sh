#!/usr/bin/env bash
set -euo pipefail
ROOT="/home/mediahub/dev/mediahub-os-autonomous"
STATE="$ROOT/.autonomous"
LOGDIR="$STATE/logs"
PROVENANCE="$STATE/provenance.log"
LOCKFILE="$STATE/loop.lock"
HEARTBEAT="$STATE/heartbeat.log"
PIDFILE="$STATE/loop.pid"
STOPFILE="$STATE/STOP"
mkdir -p "$LOGDIR"
exec 9>"$LOCKFILE"
flock -n 9 || exit 73
PROC_STARTTIME="$(awk '{print $22}' "/proc/$$/stat" 2>/dev/null || true)"
printf '%s:%s\n' "$$" "$PROC_STARTTIME" >"$PIDFILE"
trap 'rm -f "$PIDFILE"' EXIT
export MEDIAHUB_ROOT="$ROOT"
export PYTHONPATH="$ROOT${PYTHONPATH:+:$PYTHONPATH}"
export MEDIAHUB_LOCAL_MODEL="${MEDIAHUB_LOCAL_MODEL:-/home/mediahub/local-ai/models/qwen2.5-coder-1.5b-instruct-q4_k_m.gguf}"
export MEDIAHUB_LOCAL_MODEL_NAME="${MEDIAHUB_LOCAL_MODEL_NAME:-qwen2.5-coder:3b}"
export MEDIAHUB_AI_URL="${MEDIAHUB_AI_URL:-http://127.0.0.1:11434/v1/chat/completions}"
PYTHON_BIN="$ROOT/.venv-mediahub/bin/python"
[ -x "$PYTHON_BIN" ] || PYTHON_BIN="/usr/bin/python3"
export MEDIAHUB_PYTHON="$PYTHON_BIN"
export MEDIAHUB_LLAMA_CLI="/home/mediahub/local-ai/bin/llama-cli"
if [ ! -e "$STOPFILE" ]; then
	nohup "$PYTHON_BIN" "$ROOT/ops/astra_orchestrator.py" >>"$STATE/astra.log" 2>&1 9>&- &
fi
MAX=900
SLEEP=5
CYCLE=BOOT
LAST_RESULT=STARTING
FAIL_STREAK=0
MAX_FAIL_STREAK=3
(while :; do
	printf "STATE=RUNNING\nPID=%s\nPROC_STARTTIME=%s\nCYCLE=%s\nHEAD=%s\nLAST_RESULT=%s\nMODEL=%s\nTIMESTAMP=%s\n" "$$" "$PROC_STARTTIME" "$(cat "$STATE/current_cycle" 2>/dev/null || echo BOOT)" "$(git -C "$ROOT" rev-parse HEAD 2>/dev/null || echo UNKNOWN)" "$(cat "$STATE/current_result" 2>/dev/null || echo STARTING)" "$MEDIAHUB_LOCAL_MODEL" "$(date -u +%FT%TZ)" >"$HEARTBEAT.tmp"
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
		BASE_HEAD="$(git rev-parse HEAD)"
		BASE_TREE="$(git rev-parse 'HEAD^{tree}')"
		echo "MODE=LOCAL_ONLY"
		echo "BASE_HEAD=$BASE_HEAD"
		echo "BASE_TREE=$BASE_TREE"
		echo "SOURCE_SHA=$BASE_HEAD"
		if ! git merge-base --is-ancestor 471f709f5633feab7aeb62dd3ea52effad6d2bc4 HEAD; then
			echo "P0_BLOCKED: R4 ancestry invariant failed"
			printf "BLOCKED\n" >"$STATE/current_result"
			echo "AUTONOMY_RETAINED: controller remains alive; awaiting operator correction"
			sleep 60
			continue
		fi
		if [ -n "$(git status --porcelain)" ]; then
			echo "P0_BLOCKED: baseline worktree is not clean"
			printf "BLOCKED\n" >"$STATE/current_result"
			echo "AUTONOMY_RETAINED: controller remains alive; awaiting clean worktree"
			sleep 60
			continue
		fi
		set +e
		timeout --signal=TERM --kill-after=20s "${MAX}s" "$PYTHON_BIN" ./ops/local_autonomous_agent.py
		RC=$?
		set -e
		POST_HEAD="$(git rev-parse HEAD)"
		POST_TREE="$(git rev-parse 'HEAD^{tree}')"
		STATUS="$(git status --porcelain)"
		echo "LOCAL_AGENT_RC=$RC"
		echo "POST_HEAD=$POST_HEAD"
		echo "POST_TREE=$POST_TREE"
		echo "POST_STATUS:"
		git status --short --branch
		ROLLBACK=NOT_REQUIRED
		if [ "$RC" -ne 0 ] && [ "$POST_HEAD" = "$BASE_HEAD" ] && [ -n "$STATUS" ]; then
			echo "ROLLBACK=REQUIRED_NON_DESTRUCTIVE"
			if git restore --staged --worktree -- . && [ -z "$(git status --porcelain)" ]; then
				ROLLBACK=APPLIED_HEAD_PRESERVED
			else
				ROLLBACK=BLOCKED_RESTORE_FAILED
				LAST_RESULT=BLOCKED
			fi
		elif [ "$RC" -ne 0 ] && [ "$POST_HEAD" != "$BASE_HEAD" ]; then
			ROLLBACK=BLOCKED_HEAD_CHANGED
			LAST_RESULT=BLOCKED
		fi
		if [ "$RC" -eq 0 ] && [ "$POST_HEAD" != "$BASE_HEAD" ] && [ -z "$STATUS" ] && git merge-base --is-ancestor "$BASE_HEAD" "$POST_HEAD"; then
			LAST_RESULT=PASS
			FAIL_STREAK=0
		elif [ "$RC" -eq 0 ] && [ "$POST_HEAD" = "$BASE_HEAD" ] && [ -z "$STATUS" ]; then
			# Clean no-progress/IDLE is a healthy queue-wait state, not an execution failure.
			LAST_RESULT=NO_PROGRESS
			FAIL_STREAK=0
		elif [ "$RC" -eq 30 ]; then
			# Queue wait is a non-error state; do not trip the repeated-failure circuit.
			LAST_RESULT=NO_PROGRESS
			FAIL_STREAK=0
		elif [ "${LAST_RESULT:-}" != "BLOCKED" ]; then
			LAST_RESULT=FAIL
			FAIL_STREAK=$((FAIL_STREAK + 1))
		fi
		printf "%s\n" "$LAST_RESULT" >"$STATE/current_result"
		printf "%s\tSOURCE_SHA=%s\tBASE_TREE=%s\tRC=%s\tPOST_HEAD=%s\tPOST_TREE=%s\tROLLBACK=%s\tRESULT=%s\n" "$STAMP" "$BASE_HEAD" "$BASE_TREE" "$RC" "$POST_HEAD" "$POST_TREE" "$ROLLBACK" "$LAST_RESULT" >>"$PROVENANCE"
		echo "CYCLE_RESULT=$LAST_RESULT"
	} >>"$LOG" 2>&1 || {
		printf "BLOCKED\n" >"$STATE/current_result"
		echo "AUTONOMY_RETAINED: cycle failed closed; controller remains alive" >>"$LOG"
		sleep 60
		continue
	}
	if [ "$FAIL_STREAK" -ge "$MAX_FAIL_STREAK" ]; then
		echo "AUTONOMY_BLOCKED: repeated execution failures; fail-closed after $FAIL_STREAK cycles" >>"$LOG"
		printf "BLOCKED\n" >"$STATE/current_result"
		# Safety block is represented by state; the 24/7 supervisor remains alive for operator/controller correction.
		FAIL_STREAK=0
		sleep 60
		continue
	fi
	if [ "$RC" -eq 30 ]; then
		# No-progress is a queue wait, not a failure and must not terminate autonomy.
		sleep 60
	else
		sleep "$SLEEP"
	fi
done
