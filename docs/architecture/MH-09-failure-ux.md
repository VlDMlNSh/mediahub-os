# MH-09 — Failure UX

**Status:** PROPOSED / REQUIRES VERIFICATION

Critical rule: no UI state may claim completion without authoritative commit evidence.

The presentation must distinguish not-started, rejected, failed, committed, cancelled and unknown outcomes. Unknown results remain unknown until reconciled. Stale/conflict states require safe refresh or explicit user resolution; hidden merge/LWW is forbidden. Recovery must preserve authorization boundaries.
