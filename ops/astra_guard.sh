#!/usr/bin/env bash
set -u
ROOT="/home/mediahub/dev/mediahub-os-autonomous"
STATE="$ROOT/.autonomous"
PIDFILE="$STATE/astra.pid"
LOCK="$STATE/astra-guard.lock"
LOG="$STATE/astra-guard.log"
HEARTBEAT="$STATE/astra_heartbeat.json"
HEARTBEAT_MAX=45
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
  if [[ "$owned" -eq 1 && -s "$HEARTBEAT" ]]; then
    now="$(date +%s)"
    heartbeat_mtime="$(stat -c %Y "$HEARTBEAT" 2>/dev/null || echo 0)"
    heartbeat_age=$((now - heartbeat_mtime))
    if [[ "$heartbeat_age" -gt "$HEARTBEAT_MAX" ]]; then
      printf '%s Astra heartbeat stale age=%ss; restarting coordinator\n' "$(date -u +%FT%TZ)" "$heartbeat_age" >>"$LOG"
      kill -TERM "$pid" 2>/dev/null || true
      sleep 2
      kill -KILL "$pid" 2>/dev/null || true
      owned=0
    fi
  fi
  if [[ "$owned" -eq 0 ]]; then
    # Recover ownership after a lost/stale pidfile before starting anything.
    # Never spawn a second Astra when an existing repository-owned coordinator
    # is already resident. If ownership is ambiguous, fail closed and retry.
    candidates=()
    while read -r candidate candidate_cmd; do
      [[ "$candidate" =~ ^[0-9]+$ ]] || continue
      [[ "$candidate" -eq "$$" ]] && continue
      case "$candidate_cmd" in
        *"$ROOT/ops/astra_orchestrator.py"*) candidates+=("$candidate") ;;
      esac
    done < <(ps -eo pid=,args= 2>/dev/null || true)
    if [[ "${#candidates[@]}" -eq 1 ]]; then
      pid="${candidates[0]}"
      start="$(awk '{print $22}' "/proc/$pid/stat" 2>/dev/null || true)"
      if [[ -n "$start" ]]; then
        printf '%s:%s\n' "$pid" "$start" >"$PIDFILE"
        owned=1
        printf '%s Astra ownership recovered pid=%s\n' "$(date -u +%FT%TZ)" "$pid" >>"$LOG"
      fi
    elif [[ "${#candidates[@]}" -gt 1 ]]; then
      printf '%s Astra ownership ambiguous candidates=%s; refusing duplicate start\n' "$(date -u +%FT%TZ)" "${candidates[*]}" >>"$LOG"
    fi
  fi
  if [[ "$owned" -eq 0 ]]; then
    printf '%s Astra absent; starting resident coordinator\n' "$(date -u +%FT%TZ)" >>"$LOG"
    nohup /usr/bin/python3 "$ROOT/ops/astra_orchestrator.py" >>"$STATE/astra.log" 2>&1 9>&- &
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
