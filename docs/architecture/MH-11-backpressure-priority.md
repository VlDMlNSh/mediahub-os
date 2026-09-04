# MH-11 — Backpressure and Priority

Status: PROPOSED

Observability must be failure-contained. Use bounded queues, sampling, aggregation, rate limiting, prioritization and explicit drop policy. Priority order: Critical security/integrity/failure; High service/authorization/policy failures; Normal operational metrics; Low debug/verbose/exploratory telemetry. Telemetry overload must not starve critical runtime.
