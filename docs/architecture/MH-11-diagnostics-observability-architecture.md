# MH-11 — Diagnostics / Observability Architecture v1.0

Status: PROPOSED

## Authority boundary
Observability is non-authoritative. Canonical mutation remains P0-03 State Authority. Diagnostic read access is authorized and bounded; any state-changing operation follows the normal Authorization → Consumer Boundary → State Authority path.

## Logical planes
1. Observation: logs, metrics, traces, diagnostic events, telemetry, health observations.
2. Accountability: audit and forensic evidence.
3. Diagnostics: authorized queries and snapshots.
4. Correlation: trace/request/operation/event/incident identifiers.
5. Protection: authorization, redaction, privacy, classification, retention and resource controls.
6. Collection: buffering, sampling, aggregation, prioritization and bounded transport.

## Reliability
Observability failure must not become system-wide failure. Telemetry overload must not starve critical runtime. Local-first diagnostics remain available without cloud where possible.

## Semantic separation
Log, metric, trace, event, audit record, notification, telemetry sample, command and evidence are distinct types. Observed state is not automatically canonical state.

## Cross-system boundary
AI may analyze and recommend but does not gain authority. Plugins receive only authorized, bounded diagnostic capabilities. Cloud observability is external and untrusted. Diagnostic storage is not canonical persistence.

## Status
This document defines the MH-11 architectural target. Implementation and technology choices require separate contracts, ADRs, security/privacy review, resource budget, tests and implementation authorization.
