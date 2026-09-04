# MH-17 — Offline-First Integration

**Status:** PROPOSED / CANDIDATE

Loss of cloud or network connectivity MUST NOT imply loss of local identity, policy, safety, or canonical-state authority. Local operation continues only within previously authorized capabilities and safety policy.

Offline mode MUST distinguish observed, desired, commanded, applied, confirmed, and predicted states. Queued commands require expiration, authorization re-evaluation, and idempotency semantics before dispatch.

Cloud reconnect MUST reconcile evidence rather than blindly replay stale intent. No cloud dependency may become an implicit direct device-control path.
