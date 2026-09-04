# MH-17 — Event Model

**Status:** CANDIDATE

Device-originated facts are classified as state, telemetry, availability, fault, security, capability or lifecycle events. An event is not a command and not authorization.

Every normalized event requires source, subject/device reference, timestamp, schema version, correlation/causation where available, bounded payload, severity/priority and provenance. Duplicate, delayed, out-of-order and malformed events are explicitly handled.

The repository already has a canonical immutable domain-event schema requiring id, type, version, timestamp, source, subject, payload, severity, priority, correlation_id and causation_id. fileciteturn9file0L2-L5

Device events enter through the integration boundary and cannot directly mutate persistence or bypass State Authority.