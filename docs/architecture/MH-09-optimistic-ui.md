# MH-09 — Optimistic UI

**Status:** PROPOSED / REQUIRES VERIFICATION

Optimistic presentation follows `Intent → Pending → Authorization → Command → Commit → Confirmed`.

Pending or accepted is never equivalent to committed. UI must distinguish pending, accepted, committed, failed, rejected, cancelled and unknown. Destructive operations must not be duplicated automatically. Retries require explicit classification and must not change authorization or policy semantics.
