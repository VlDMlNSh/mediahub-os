# P0-04 — Residual Risk Register v1.0

Status: controlled remediation; final governance disposition pending.

## Accepted-by-scope residuals

| Risk | Status | Reason / boundary |
|---|---|---|
| Cryptographic checkpoint authenticity | Deferred | P0-04 is in-memory only. No durable checkpoint transport or storage is authorized. Future persistence must introduce cryptographic authenticity before trust is established. |
| Crash consistency / durable atomicity | Deferred | No persistence exists in P0-04. Filesystem/SQLite/ZFS crash semantics are not demonstrated and remain out of scope. |
| Retention and deletion of durable state | Deferred | No durable state lifecycle exists in this phase. Future persistence must define minimization, retention, deletion and recovery semantics. |
| Durable personal-data protection | Deferred | P0-04 does not authorize durable personal-data storage/export. Privacy guarantees are limited to the in-memory boundary and diagnostics behavior demonstrated by tests. |
| Appliance/boot/update/recovery integration | Deferred | systemd, bootloader, installer, recovery media and update engine are explicitly unauthorized. |

## Conditions for future phases

1. Deferred risks must not be converted into implicit guarantees by documentation or integration.
2. Any persistence implementation requires a new controlled architecture phase and security review.
3. Checkpoint material crossing a durable or external trust boundary requires authenticity and integrity validation before use.
4. Personal-data-bearing state requires explicit data classification, minimization, retention, deletion and recovery controls before persistence is authorized.
5. P0-04 acceptance, when eventually granted, applies only to the bounded in-memory implementation and its demonstrated properties.

## Current blocking item

The current remediation branch has hardened the read boundary so `CanonicalState.payload` and checkpoint payloads are recursively immutable at the API boundary. This change requires fresh execution evidence against the resulting exact commit before the SEC-SA traceability matrix can be promoted from controlled mapping to execution-backed evidence.

Governance acceptance remains **NOT GRANTED** until security exit criteria and explicit governance approval are complete.
