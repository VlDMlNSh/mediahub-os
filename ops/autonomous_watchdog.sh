#!/usr/bin/env bash
set -u
ROOT="/home/mediahub/dev/mediahub-os-autonomous"
PIDFILE="$ROOT/.autonomous/loop.pid"
STOPFILE="$ROOT/.autonomous/STOP"
LOG="$ROOT/.autonomous/watchdog.log"
while [ ! -e "$STOPFILE" ]; do
  if [ ! -s "$PIDFILE" ] || ! kill -0 "$(cat "$PIDFILE" 2>/dev/null)" 2>/dev/null; then
    echo "$(date -u +%FT%TZ) restarting controller" >> "$LOG"
    rm -f "$PIDFILE"
    nohup "$ROOT/ops/autonomous_os_loop.sh" >> "$LOG" 2>&1 &
    sleep 5
  fi
  sleep 20
done
echo "$(date -u +%FT%TZ) stop marker observed; watchdog exiting" >> "$LOG"
