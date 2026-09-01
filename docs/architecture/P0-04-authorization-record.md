# P0-04 Implementation Authorization v1.0

## Status

**AUTHORIZED**

## Authority decision

P0-03 State Authority Contract v1.0 was explicitly accepted by project authority.

- P0-03 baseline: `9ae82f9e45bcb9c330ab283b13a482fbeea6b546`
- Decision: `ACCEPT`
- UTC timestamp: `2026-09-01T19:44Z`
- Conditions: none beyond the existing P0-04 scope and security/privacy controls

## Authorization

P0-04 implementation is authorized strictly for deterministic in-memory State Authority implementation and its functional, adversarial, security and privacy verification.

## Prohibited capabilities

Persistence of any kind, SQLite, ZFS, filesystem mutation/storage orchestration, subprocesses, arbitrary command execution, network transport, telemetry, mTLS transport, bootloader/systemd appliance integration, installer/recovery media, update/rollback engine, cloud persistence, hardware persistence/security integration, production deployment topology, unsafe deserialization, dynamic code execution, direct AI/external mutation authority, and real private/user data in fixtures or evidence remain prohibited.

## Acceptance boundary

Authorization is not acceptance. P0-04 must independently satisfy its evidence, security/privacy, adversarial and acceptance gates on an exact immutable implementation commit.

## Historical boundary

No MH-02…MH-16 responsibility is inferred by this authorization.
