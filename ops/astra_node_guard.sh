#!/usr/bin/env bash
set -u
ROOT="${MEDIAHUB_ROOT:-/home/mediahub/dev/mediahub-os-autonomous}"
STATE="$ROOT/.autonomous/node_bus"
PIDFILE="$STATE/node_agent.pid"
mkdir -p "$STATE"
lock="$STATE/guard.lock"
exec 9>"$lock"
flock -n 9 || exit 0

owned_pid() {
  local pid start expected
  pid="${1:-}"
  [ -n "$pid" ] || return 1
  [ -r "/proc/$pid/stat" ] || return 1
  start="$(awk '{print $22}' "/proc/$pid/stat" 2>/dev/null || true)"
  [ -n "$start" ] || return 1
  expected="$(cat "$PIDFILE.start" 2>/dev/null || true)"
  [ -n "$expected" ] && [ "$start" = "$expected" ] || return 1
  grep -Fqx "python3 $ROOT/ops/astra_node_agent.py" "/proc/$pid/cmdline" 2>/dev/null && return 0
  tr '\0' ' ' < "/proc/$pid/cmdline" 2>/dev/null | grep -Fq "$ROOT/ops/astra_node_agent.py"
}

pid="$(cat "$PIDFILE" 2>/dev/null || true)"
if ! owned_pid "$pid"; then
  nohup /usr/bin/python3 "$ROOT/ops/astra_node_agent.py" >>"$STATE/dev2.log" 2>&1 &
  pid="$!"
  echo "$pid" > "$PIDFILE"
  sleep 1
  if [ -r "/proc/$pid/stat" ]; then
    awk '{print $22}' "/proc/$pid/stat" > "$PIDFILE.start"
  fi
fi
