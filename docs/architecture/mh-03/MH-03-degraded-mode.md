# MH-03 Degraded Mode

DEGRADED means the runtime remains operational with an explicitly known subset of capabilities unavailable or impaired.

Typical transitions:
`READY → DEGRADED` on optional dependency loss;
`DEGRADED → RECOVERING` when bounded recovery begins;
`RECOVERING → READY` after readiness criteria pass;
`RECOVERING → DEGRADED` after unsuccessful recovery.

Cloud unavailable: continue local deterministic capabilities where safe.
AI unavailable: deterministic core continues.
Optional integration unavailable: isolate affected capability.
State Authority unavailable: no mutation fallback; dependent mutation capabilities unavailable.

Degraded mode never relaxes authorization or trust boundaries.
