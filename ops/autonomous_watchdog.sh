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
	if [ ! -s "$PIDFILE" ] || ! kill -0 "$(cat "$PIDFILE" 2>/dev/null)" 2>/dev/null || [ "$stale" -eq 1 ]; then
		echo "$(date -u +%FT%TZ) restarting controller" >>"$LOG"
		rm -f "$PIDFILE"
		nohup "$ROOT/ops/autonomous_os_loop.sh" >>"$LOG" 2>&1 &
		sleep 5
	fi
	sleep 20
done
echo "$(date -u +%FT%TZ) stop marker observed; watchdog exiting" >>"$LOG"
