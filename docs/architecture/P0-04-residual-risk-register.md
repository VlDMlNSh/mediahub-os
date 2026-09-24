# P0-04 — Residual Risk Register v1.0

Status: security remediation conditions closed; final governance disposition pending.

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

## Remediation disposition

The previously identified P0-04 security conditions are now execution-backed on hardened commit `1279024fc7c20a2eb291c1f5bc5dbf807e2350b0`:

- restore self-test gate: PASS;
- fail-closed self-test exception handling: PASS;
- read-boundary immutability: PASS;
- checkpoint payload/identity immutability: PASS;
- targeted P0-04 regression: 16/16 PASS;
- full repository regression: 126/126 PASS;
- prohibited-capability scan: 0 matches;
- working tree: clean and synchronized.

No new persistence or production integration was introduced.

## Remaining governance blockers

Security traceability is now execution-backed, but P0-04 is not yet governance-accepted. Final disposition still requires evidence-integrity verification and explicit governance approval. Deferred persistence/appliance/privacy risks remain outside this phase and unauthorized.
