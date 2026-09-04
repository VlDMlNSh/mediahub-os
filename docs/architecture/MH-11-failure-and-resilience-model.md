# MH-11 — Failure and Resilience Model

Status: PROPOSED

Observability failures are contained. Logger, metrics, trace, audit, storage, collector, clock, network and cloud failures must not make State Authority or core runtime fail solely because observation failed.

Telemetry overload uses bounded queues, prioritization, sampling/aggregation and deterministic drop semantics. Critical runtime resources are protected first.
