# P0-04 Threat-to-Test Traceability v1.0

## Status

Prepared. No implementation authorization is implied.

## Purpose

Provide a direct mapping from the P0-04 threat model and abuse cases to observable verification. This prevents security claims from existing only as prose.

| Threat / abuse class | Observable property | Required evidence |
|---|---|---|
| Unauthorized mutation | Unauthorized operation rejected; canonical state unchanged | Negative authorization test |
| Candidate leakage | Candidate invisible before commit | Isolation test |
| Partial publication | Reader sees complete old or complete new revision | Publication/concurrency test |
| Stale overwrite | Stale transaction rejected | Revision/concurrency test |
| Caller-selected revision | Caller-supplied version cannot control authoritative revision | Negative test |
| Generation confusion | Mismatched generation rejected | Generation test |
| Integrity bypass | Integrity failure rejects otherwise compatible state | Independent integrity test |
| Checkpoint substitution | Checkpoint identity cannot be silently replaced | Checkpoint immutability test |
| Restore corruption | Failed restore preserves canonical state | Restore failure test |
| Malformed/untrusted state | Invalid structure/schema/bounds rejected | Input validation test |
| Resource exhaustion | Defined resource limits reject excessive input | Bounds test |
| Unsafe deserialization | No unsafe deserialization primitive | Capability/source inspection |
| AI/external mutation | External proposal cannot publish canonical state | Interface/adversarial test |
| Command execution | No subprocess/arbitrary command primitive | Capability/source inspection |
| Filesystem mutation | No arbitrary filesystem write primitive | Capability/source inspection |
| Network mutation | No network/telemetry primitive | Capability/source inspection |
| Diagnostic disclosure | Sensitive nested values sanitized | Privacy regression + log inspection |
| Transaction resurrection | Terminal transaction cannot become active again | Lifecycle negative test |

## Evidence rule

Each row must be tied to the exact implementation commit and captured execution result before the corresponding security claim can be marked PASS.

## Privacy rule

All test inputs should be synthetic. Evidence must not contain real credentials, private content, raw voice/audio, or unnecessary personal data.

## Scope

This traceability artifact covers only the deterministic in-memory P0-04 implementation. Persistence, production privilege boundaries, network/mTLS, recovery media, update/rollback, cloud, and hardware security remain separate gates.

## Historical boundary

No historical MH-02…MH-16 responsibility is inferred.
