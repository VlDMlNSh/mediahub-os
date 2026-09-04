# MH-17 — Evidence Register

**Status:** OPEN / AUDIT BASELINE

| ID | Claim | Evidence | Status | Confidence |
|---|---|---|---|---|
| E-001 | Repository has canonical normalized Device schema | `schemas/domain/device.schema.json` | VERIFIED | High |
| E-002 | MediaHub logical identity is represented by `mediahub_id` | device + identity schemas | VERIFIED | High |
| E-003 | Capability schema exists with safety/discovery fields | `schemas/domain/capability.schema.json` | VERIFIED | High |
| E-004 | Device state and desired state are distinct | state/desired-state schemas + reconciliation test | VERIFIED | High |
| E-005 | Trust is distinct from health/availability | trust schema + reconciliation test | VERIFIED | High |
| E-006 | Protocol binding and endpoint abstractions exist | binding/endpoint schemas | VERIFIED | High |
| E-007 | Events are modeled as immutable facts with source/time/correlation | event schema + reconciliation test | VERIFIED | High |
| E-008 | Real protocol adapters exist | repository tree/search | NOT FOUND / UNKNOWN | Medium |
| E-009 | MQTT/HTTP/WebSocket/BLE/etc. integration exists | repository search | NOT FOUND / UNKNOWN | Medium |
| E-010 | Device discovery implementation exists | repository tree/search | NOT FOUND / UNKNOWN | Medium |
| E-011 | Device enrollment implementation exists | repository tree/search | NOT FOUND / UNKNOWN | Medium |
| E-012 | Certificate/mTLS/PKI device security exists | repository tree/search | NOT FOUND / UNKNOWN | Medium |
| E-013 | Device simulator exists | repository tree/search | NOT FOUND / UNKNOWN | Medium |
| E-014 | Production device commands are authorized through adapter boundary | no implementation evidence | UNKNOWN | High |
| E-015 | P0-06 preserves single State Authority and P0-05 boundary | P0-06 architecture | VERIFIED as prior architecture | High |

**Audit timestamp:** 2026-09-04.

Evidence rule: protocol/device-specific claims require protocol version, hardware/firmware context, observed behavior, test method and timestamp before qualification.