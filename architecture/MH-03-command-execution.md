# MH-03 Command Execution

**Status:** PROPOSED

Canonical flow:

`Command → Validation → Authorization/Policy → Consumer Contract → State Authority → Canonical Mutation → Event → Observers`

Rules:
- Command is a request to change.
- UI, AI, plugin, device and cloud inputs are never direct state mutations.
- Missing/invalid authorization is denied.
- Malformed or ambiguous commands are rejected/fail closed.
- Stale transactions are rejected.
- Command execution never uses a private authoritative state store.
- State Authority remains the sole canonical mutation authority.
