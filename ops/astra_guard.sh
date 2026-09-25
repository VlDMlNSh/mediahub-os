#!/usr/bin/env bash
set -u
ROOT="/home/mediahub/dev/mediahub-os-autonomous"
STATE="$ROOT/.autonomous"
PIDFILE="$STATE/astra.pid"
LOCK="$STATE/astra-guard.lock"
LOG="$STATE/astra-guard.log"
exec 9>"$LOCK"
flock -n 9 || exit 73
mkdir -p "$STATE"
while :; do
  record="$(cat "$PIDFILE" 2>/dev/null || true)"
  pid="${record%%:*}"
  recorded_start="${record#*:}"
  owned=0
  if [[ "$pid" =~ ^[0-9]+$ ]] && [[ "$record" == *:* ]] && kill -0 "$pid" 2>/dev/null; then
    current_start="$(awk '{print $22}' "/proc/$pid/stat" 2>/dev/null || true)"
    cmd="$(ps -p "$pid" -o args= 2>/dev/null || true)"
    case "$cmd" in
      *"$ROOT/ops/astra_orchestrator.py"*)
        [[ -n "$recorded_start" && "$recorded_start" == "$current_start" ]] && owned=1 ;;
    esac
  fi
  if [[ "$owned" -eq 0 ]]; then
    printf '%s Astra absent; starting resident coordinator\n' "$(date -u +%FT%TZ)" >>"$LOG"
    nohup /usr/bin/python3 "$ROOT/ops/astra_orchestrator.py" >>"$STATE/astra.log" 2>&1 &
    pid=$!
    sleep 1
    start="$(awk '{print $22}' "/proc/$pid/stat" 2>/dev/null || true)"
    if [[ -n "$start" ]]; then
      printf '%s:%s\n' "$pid" "$start" >"$PIDFILE"
    else
      rm -f "$PIDFILE"
      printf '%s Astra start failed pid=%s\n' "$(date -u +%FT%TZ)" "$pid" >>"$LOG"
    fi
  fi
  sleep 10
done
