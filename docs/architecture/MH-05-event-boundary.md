# MH-5 — Event Boundary

**Status:** PROPOSED — GOVERNANCE REVIEW REQUIRED

An Event is a bounded representation of a fact that has already occurred. It is not a command and cannot mutate canonical state merely by being observed or delivered.

## Event classes

- **Domain Event:** fact about governed domain/runtime behavior.
- **Audit Event:** security/governance record of an authorization or critical action.
- **Telemetry:** bounded operational measurement.
- **Diagnostic Record:** sanitized troubleshooting information.
- **Notification:** consumer-facing signal derived from an event/fact.
- **Command:** request for an operation; never an event.
- **Proposal:** inert suggested action; never an event by default.

Events should carry correlation/causation identifiers only where they provide real traceability value. They must be bounded and must not expose secrets or unrestricted internal object identity.

Observers are read/observation consumers. Receiving an event does not grant command or mutation authority.
