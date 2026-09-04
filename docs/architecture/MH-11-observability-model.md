# MH-11 Observability Model

Status: PROPOSED

Observability is composed of semantically distinct channels:

- Logs — operational/debug context.
- Metrics — numerical measurements and health/performance indicators.
- Traces — execution and causal-correlation context, without becoming commands.
- Domain Events — domain facts defined by their domain contracts.
- Diagnostic Events — operational observations.
- Audit Records — security/accountability records.
- Telemetry Samples — measurements emitted for monitoring/analysis.
- Health/Readiness — observations of lifecycle/service conditions.
- Evidence — integrity/provenance-aware material retained for verification or forensics.
- Notifications/Alerts — signals for attention, not authorization.

No channel is automatically canonical state. No channel grants authority.
