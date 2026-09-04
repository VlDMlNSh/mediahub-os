# MH-09 — Command / Interaction Model

**Status:** PROPOSED

```text
User Intent → UI Validation → Consumer Request → Capability → Authorization/Policy → Command → Consumer Boundary → State Authority
```

Button presses, visible controls and local validation do not authorize execution. Commands are explicit, operation-specific, bounded and auditable. The UI must surface result states: pending, accepted, committed, failed, rejected, cancelled and unknown.

Retry is explicit and bounded. Authorization failures, validation failures, conflicts and stale-version failures are not silently retried. Destructive operations require operation-specific semantics preventing accidental duplication.

Optimistic UI, if used, is presentation-only until authoritative commit confirmation.
