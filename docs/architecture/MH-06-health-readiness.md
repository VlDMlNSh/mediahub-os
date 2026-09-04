# MH-06 — Health / Readiness

Status: PROPOSED

Liveness means the process/service can perform its basic runtime loop. Readiness means it is safe to accept its defined operations. Neither implies trust or mutation authority.

Health candidates: UNKNOWN, STARTING, READY, DEGRADED, FAILED, STOPPING, STOPPED, QUARANTINED. These are observation/supervision semantics and are not additions to the canonical P0-06 lifecycle without evidence.

Health APIs are bounded, immutable/value-semantic and observation-only. Health state cannot grant capability.
