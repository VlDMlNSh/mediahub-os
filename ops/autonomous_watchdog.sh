#!/usr/bin/env bash
set -u
ROOT="/home/mediahub/dev/mediahub-os-autonomous"
PIDFILE="$ROOT/.autonomous/loop.pid"
CONTROLLER_PIDFILE="$ROOT/.autonomous/controller.pid"
STATE="$ROOT/.autonomous"
WATCHLOCK="$STATE/watchdog.lock"
HEARTBEAT="$STATE/heartbeat.log"
HEARTBEAT_MAX=45
STOPFILE="$ROOT/.autonomous/STOP"
LOG="$ROOT/.autonomous/watchdog.log"
exec 9>"$WATCHLOCK"
flock -n 9 || exit 73
WATCHDOG_PIDFILE="$STATE/watchdog.pid"
HYBRID_START="$STATE/hybrid_controller_start.log"
echo $$ >"$WATCHDOG_PIDFILE"
trap 'rm -f "$WATCHDOG_PIDFILE"' EXIT INT TERM
while [ ! -e "$STOPFILE" ]; do
	now=$(date +%s)
	stale=1
	if [ -s "$HEARTBEAT" ]; then
		age=$((now - $(stat -c %Y "$HEARTBEAT")))
		[ "$age" -le "$HEARTBEAT_MAX" ] && stale=0
	fi
	pid_record="$(cat "$PIDFILE" 2>/dev/null || true)"
	pid="${pid_record%%:*}"
	recorded_starttime="${pid_record#*:}"
	owned=0
	if [ -n "$pid" ] && [ "$pid" != "$pid_record" ] && kill -0 "$pid" 2>/dev/null; then
		current_starttime="$(awk '{print $22}' "/proc/$pid/stat" 2>/dev/null || true)"
		cmd="$(ps -p "$pid" -o args= 2>/dev/null || true)"
		case "$cmd" in
			*"$ROOT/ops/autonomous_os_loop.sh"*|*"./ops/autonomous_os_loop.sh"*)
				[ -n "$recorded_starttime" ] && [ "$recorded_starttime" = "$current_starttime" ] && owned=1 ;;
		esac
	fi
	if [ "$stale" -eq 1 ] && [ "$owned" -eq 1 ]; then
		echo "$(date -u +%FT%TZ) stale heartbeat; requesting graceful TERM pid=$pid" >>"$LOG"
		kill -TERM "$pid" 2>/dev/null || true
		stopped=0
		for _ in 1 2 3 4 5; do
			if ! kill -0 "$pid" 2>/dev/null; then
				stopped=1
				break
			fi
			sleep 1
		done
		if [ "$stopped" -eq 1 ]; then
			owned=0
			echo "$(date -u +%FT%TZ) controller stopped gracefully pid=$pid" >>"$LOG"
		else
			owned=1
			echo "$(date -u +%FT%TZ) controller did not stop gracefully; replacement blocked pid=$pid" >>"$LOG"
		fi
	fi
	# Independently supervise the hybrid controller. The controller's flock remains the authority
	# against duplicate instances; this watchdog only starts it when its recorded owner is absent.
	controller_owned=0
	controller_record="$(cat "$CONTROLLER_PIDFILE" 2>/dev/null || true)"
	controller_pid="${controller_record%%:*}"
	controller_starttime="${controller_record#*:}"
	if [ -n "$controller_pid" ] && [ "$controller_pid" != "$controller_record" ] && kill -0 "$controller_pid" 2>/dev/null; then
		current_controller_starttime="$(awk '{print $22}' "/proc/$controller_pid/stat" 2>/dev/null || true)"
		controller_cmd="$(ps -p "$controller_pid" -o args= 2>/dev/null || true)"
		case "$controller_cmd" in
			*"$ROOT/ops/hybrid_orchestrator.py"*|*"python3 ops/hybrid_orchestrator.py"*)
				[ -n "$controller_starttime" ] && [ "$controller_starttime" = "$current_controller_starttime" ] && controller_owned=1 ;;
		esac
	fi
	if [ "$controller_owned" -eq 0 ] && [ ! -e "$STOPFILE" ]; then
		echo "$(date -u +%FT%TZ) hybrid controller absent; starting flock-protected controller" >>"$HYBRID_START"
		nohup python3 "$ROOT/ops/hybrid_orchestrator.py" >>"$STATE/hybrid_controller.log" 2>&1 &
		controller_pid=$!
		sleep 1
		controller_starttime="$(awk '{print $22}' "/proc/$controller_pid/stat" 2>/dev/null || true)"
		if [ -n "$controller_starttime" ]; then
			echo "$controller_pid:$controller_starttime" >"$CONTROLLER_PIDFILE"
		else
			echo "" >"$CONTROLLER_PIDFILE"
		fi
	fi
	if [ "$owned" -eq 0 ]; then
		if [ -e "$STOPFILE" ]; then
			echo "$(date -u +%FT%TZ) stop marker observed before replacement; recovery suppressed" >>"$LOG"
			break
		fi
		echo "$(date -u +%FT%TZ) ensuring controller exists" >>"$LOG"
		rm -f "$PIDFILE"
		nohup "$ROOT/ops/autonomous_os_loop.sh" >>"$LOG" 2>&1 &
		sleep 5
	fi
	sleep 20
done
echo "$(date -u +%FT%TZ) stop marker observed; watchdog exiting" >>"$LOG"
