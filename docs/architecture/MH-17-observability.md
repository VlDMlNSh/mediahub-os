# MH-17 — Observability Boundary

**Status:** PROPOSED / CANDIDATE

Observability consumes integration facts, metrics, traces, health signals, command outcomes, and security events through read-only contracts. It MUST NOT gain device-control authority.

Correlation identifiers MUST permit tracing discovery, enrollment, authorization, command, adapter, device response, normalization, and State Authority commit without exposing unnecessary secrets or sensitive payloads.

Telemetry loss MUST NOT silently become canonical state. Observability failure MUST NOT authorize or block ordinary device control unless an explicit safety/security policy says so.
