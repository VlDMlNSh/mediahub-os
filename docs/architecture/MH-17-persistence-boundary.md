# MH-17 — Persistence Boundary

**Status:** PROPOSED / CANDIDATE

Persistence stores integration records, identities, bindings, events, telemetry, command history, and approved runtime state according to their owning contracts. Persistence is not State Authority.

Device and adapter code MUST NOT write directly to canonical persistence. Canonical mutation follows State Authority rules; persistence is downstream storage or an approved persistence interface.

Historical records MUST remain distinguishable from current canonical state. Recovery of persisted data does not itself constitute authorization to control a device.
