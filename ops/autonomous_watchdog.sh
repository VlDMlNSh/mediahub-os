#!/usr/bin/env bash
set -u
ROOT="/home/mediahub/dev/mediahub-os-autonomous"
PIDFILE="$ROOT/.autonomous/loop.pid"
STATE="$ROOT/.autonomous"
WATCHLOCK="$STATE/watchdog.lock"
HEARTBEAT="$STATE/heartbeat.log"
HEARTBEAT_MAX=45
STOPFILE="$ROOT/.autonomous/STOP"
LOG="$ROOT/.autonomous/watchdog.log"
exec 9>"$WATCHLOCK"
flock -n 9 || exit 73
WATCHDOG_PIDFILE="$STATE/watchdog.pid"
echo $$ >"$WATCHDOG_PIDFILE"
trap 'rm -f "$WATCHDOG_PIDFILE"' EXIT INT TERM
while [ ! -e "$STOPFILE" ]; do
	now=$(date +%s)
	stale=1
	if [ -s "$HEARTBEAT" ]; then
		age=$((now - $(stat -c %Y "$HEARTBEAT")))
		[ "$age" -le "$HEARTBEAT_MAX" ] && stale=0
	fi
	pid="$(cat "$PIDFILE" 2>/dev/null || true)"
	owned=0
	if [ -n "$pid" ] && kill -0 "$pid" 2>/dev/null; then
		cmd="$(ps -p "$pid" -o args= 2>/dev/null || true)"
		case "$cmd" in
			*"$ROOT/ops/autonomous_os_loop.sh"*|*"./ops/autonomous_os_loop.sh"*) owned=1 ;;
		esac
	fi
	if [ "$owned" -eq 0 ] || [ "$stale" -eq 1 ]; then
		if [ "$stale" -eq 1 ] && kill -0 "$pid" 2>/dev/null; then
			echo "$(date -u +%FT%TZ) stale heartbeat; terminating controller pid=$pid" >>"$LOG"
			pkill -TERM -P "$pid" 2>/dev/null || true
			kill -TERM "$pid" 2>/dev/null || true
			for _ in 1 2 3 4 5; do
				kill -0 "$pid" 2>/dev/null || break
				sleep 1
			done
			if kill -0 "$pid" 2>/dev/null; then
				pkill -KILL -P "$pid" 2>/dev/null || true
				kill -KILL "$pid" 2>/dev/null || true
			fi
		fi
		echo "$(date -u +%FT%TZ) restarting controller" >>"$LOG"
		rm -f "$PIDFILE"
		nohup "$ROOT/ops/autonomous_os_loop.sh" >>"$LOG" 2>&1 &
		sleep 5
	fi
	sleep 20
done
echo "$(date -u +%FT%TZ) stop marker observed; watchdog exiting" >>"$LOG"
