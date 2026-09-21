# P0.3 Controller / Watchdog Verification

Status: VERIFIED_LOCAL_SUBSCOPE

## Scope

Deterministic local evidence for controller/watchdog lock, ownership, PID starttime, stop-marker race, supervision and liveness semantics. This does not authorize production deployment or claim full daemon qualification.

## Verification

Command:

```text
python3 -m pytest -q tests/ops/test_autonomous_control_plane.py
```

Acceptance: all existing autonomous-control-plane tests pass; source validation covers the controller and watchdog shell contracts; no production mutation, release or credential action is performed.

## Provenance

The controller writes this artifact only after executing the verification command successfully against the current task base.
