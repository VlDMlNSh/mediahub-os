# P0-04 Security Review Exit Criteria v1.0

## Status

Prepared. This document defines the security exit gate for the future in-memory implementation; it does not authorize implementation.

## Mandatory PASS domains

Security review cannot exit successfully unless evidence covers all applicable domains:

1. **Authority:** only State Authority can publish canonical state.
2. **Authorization:** every mutation/recovery operation is operation-specific and default-deny.
3. **Isolation:** uncommitted candidate state cannot affect canonical readers.
4. **Atomicity:** commit publishes a complete valid revision or nothing.
5. **Versioning:** revision sequencing is authority-owned; stale writers are rejected.
6. **Generation:** incompatible binary/schema/state generations are rejected.
7. **Integrity:** integrity failure independently rejects state even when generation compatibility passes.
8. **Recovery:** restore is authorized, validated, isolated, and published as a new revision; checkpoint identity remains immutable.
9. **Input safety:** malformed, hostile, oversized, or structurally invalid data is rejected safely.
10. **Execution boundary:** no subprocess, arbitrary command, dynamic-code execution, or equivalent primitive.
11. **Network boundary:** no network transport or implicit telemetry capability.
12. **Filesystem boundary:** no arbitrary filesystem mutation capability.
13. **Deserialization:** no unsafe deserialization primitive.
14. **AI boundary:** AI/external proposals cannot directly mutate canonical state.
15. **Privacy:** diagnostics, errors, tests, and evidence do not disclose unnecessary sensitive or personal data.
16. **Failure preservation:** rejected operations preserve the last known valid canonical state.
17. **Resource safety:** defined bounds prevent trivial resource-exhaustion paths within the in-memory scope.

## Blocking findings

Any unresolved HIGH/CRITICAL security finding blocks exit. A MEDIUM finding requires explicit mitigation or documented accepted residual risk by the appropriate authority.

## Evidence requirements

The review package must reference exact implementation SHA, execution environment, commands, exit codes, test results, security scans, adversarial tests, and privacy inspection. Claims based solely on design intent do not satisfy execution evidence requirements.

## Scope boundary

This exit gate covers only deterministic in-memory State Authority behavior. It does not approve SQLite/ZFS/filesystem persistence, cloud or hardware persistence, network/mTLS, bootloader/systemd appliance, installer/recovery media, update/rollback engine, or production deployment.

## Historical boundary

No historical MH-02…MH-16 responsibility is inferred.
