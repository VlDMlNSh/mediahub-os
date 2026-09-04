# MH-06 — Supervision

Status: PROPOSED

Supervisor observes liveness, health, restart policy, failure counts, dependency readiness, quarantine and bounded recovery.

It does not own canonical state, bypass P0-05 authorization, self-grant capabilities, execute arbitrary commands, or act as policy author.

Failure classes: transient, repeated, dependency, configuration, security, resource exhaustion, unknown. Retry/backoff/restart/quarantine/operator intervention must be explicit; infinite retry is prohibited.

Restart must not silently duplicate unsafe operations or mutate canonical state.
