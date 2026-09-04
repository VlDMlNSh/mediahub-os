# MH-03 Degraded Mode

**Status:** PROPOSED

Degraded operation is explicit, deterministic and bounded.

Allowed principles:
- cloud unavailable → continue local operation where capability permits;
- AI unavailable → deterministic core continues;
- optional integration unavailable → isolate affected capability;
- optional service failure → remain operational if critical invariants hold;
- critical State Authority failure → no mutation fallback; affected mutation capabilities unavailable.

Degraded mode must not silently weaken authorization, trust boundaries, or authority rules.

Recovery may return DEGRADED → RECOVERING → READY only after health and dependency checks pass.
