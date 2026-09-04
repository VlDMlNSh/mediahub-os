# MH-06 — Observability

Status: PROPOSED

Observability surfaces: metrics, logs, traces, health, audit context and correlation identifiers.

Observability is non-authoritative. Monitoring may observe and report but cannot silently obtain mutation capability. Diagnostic data remains bounded and sanitized; secrets, credentials, private paths, stack traces and sensitive state are not exposed externally.

New diagnostic data paths require privacy/security review.
