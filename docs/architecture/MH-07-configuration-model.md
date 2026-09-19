# MH-07 — Configuration Model

Status: CANDIDATE.

A Configuration is a bounded immutable candidate containing identity, namespace, schema version, device-local scope, metadata, desired value and provenance/revision metadata when publication is authorized.

Desired configuration is distinct from observed runtime state and telemetry. Values are typed/structured, non-executable and bounded by P0-07 limits. Credentials/secrets are rejected; opaque references are inert and never implicitly dereferenced.

A validated candidate is not published state. Publication requires policy, independent authorization and the P0-05/P0-04 path. Physical persistence is outside the authorized v1 boundary.

Current implementation evidence covers immutable values, bounds and device-local scope; complete revision/provenance/publication metadata is not yet implemented.
