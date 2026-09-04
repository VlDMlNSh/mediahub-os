# MH-11 Decision Log

## D-11-001 — Observability is non-authoritative
Status: PROPOSED
Decision: MH-11 never becomes State, Policy, Authorization, Runtime or Recovery Authority.

## D-11-002 — Semantic channel separation
Status: PROPOSED
Decision: logs, metrics, traces, events, audit, telemetry, notifications and evidence remain distinct contracts.

## D-11-003 — Diagnostic mutation uses normal path
Status: PROPOSED
Decision: any state-changing diagnostic action must use Authorization → Consumer Boundary → State Authority.

## D-11-004 — Local-first
Status: PROPOSED
Decision: loss of cloud observability must not block local core operation.

## D-11-005 — Technology neutrality
Status: PROPOSED
Decision: Prometheus/Grafana/OpenTelemetry/Loki/Redis/etc. remain candidate technologies until evidence + ADR + security/resource/compatibility review.
