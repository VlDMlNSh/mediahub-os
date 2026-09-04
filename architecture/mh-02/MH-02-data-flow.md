# MH-02 — Canonical Data Flow

External World → Protocol/Adapter → Normalization → Capability Model → Command/Event → Security/Authorization → Consumer Boundary → State Authority → Runtime State → Event Stream → Observers.

Rules:
- Command = request to change.
- Event = fact that something happened.
- Events, telemetry and observations do not implicitly mutate state.
- AI output is a proposal until authorized.
- UI input is a request, never direct mutation.

Each transition requires explicit validation, trust context, authority semantics, failure handling and observability.
