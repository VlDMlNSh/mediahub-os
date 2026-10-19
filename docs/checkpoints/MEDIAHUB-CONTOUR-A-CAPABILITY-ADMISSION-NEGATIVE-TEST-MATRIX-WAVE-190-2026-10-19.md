# MediaHub OS Contour A — capability admission negative-test matrix (Wave 190)

- Date: 2026-10-19
- Scope: test-design pass only; no code/schema mutation and no test execution.
- Canonical map: [MEDIAHUB-CHAT-TREE-MAP.md](../architecture/MEDIAHUB-CHAT-TREE-MAP.md)
- Prior analysis: [Wave 189 issuer/lifecycle crosswalk](MEDIAHUB-CONTOUR-A-MESH-CAPABILITY-ISSUER-LIFECYCLE-CROSSWALK-WAVE-189-2026-10-19.md)
- Governance issue: [#301](https://github.com/VlDMlNSh/mediahub-os/issues/301)

## Frozen source refs

- `main` HEAD: `c06015e0b1526e0aaa6a522306052b077455aba5`.
- `architecture/ASTRA-GOLD-GOVERNANCE-CONTRACT.yaml`: blob `1d3ac25e7817f365807ad85d0d7c9007bd48bebf`.
- `architecture/mesh/capability.schema.json`: blob `d9360b62520aabd2fa8d74a2b74bf3fc328c9c7c`.
- `ops/mesh/validators.py`: blob `416a7ecaf4add9d0b81f0467cf426d9c7deb3ec7`.
- `ops/mesh/admission.py`: blob `46e92d3c4f9b9865356443403e9ebd34587996cd`.
- `tests/test_mesh_admission_boundary.py`: blob `1e047a5ffd3448ab83e9a2517b2cd73d3606bd28`.
- `tests/test_astra_gold_governance_contract.py`: blob `2b3a530106330ff88a16d296df0272154ecc2052`.
- `docs/architecture/MH-12-capability-security.md`: blob `8723cdb100b7ca5526616464f9fcdef60f4c61b7`.

## Clarification from deeper source review

The generic mesh capability validator checks required fields, schema version, executable identity digest format, and authority enum. Admission adds node status/identity, execution authority, qualification-state and auxiliary-capability restrictions. The repository also has a separately authenticated heartbeat path with HMAC/time/sequence checks; this report does **not** claim that all replay protection is absent system-wide. The gap here is that those heartbeat checks do not, in the inspected code, authenticate a capability envelope or bind it to the exact requested operation/resource.

The canonical governance contract requires credential rotation/expiry/revocation/audit and states missing qualification evidence blocks. Its invariant registry binds governance invariants to tests, but the inspected mesh admission boundary tests do not cover the capability issuer/lifecycle matrix below. This is a source/test inventory; no runtime tests were run.

## Proposed negative-test matrix (design only)

| ID | Adversarial input / condition | Required outcome | Enforcement layer |
|---|---|---|---|
| CAP-ISS-01 | Missing signature or signature metadata | Reject, stable reason code | Envelope verifier |
| CAP-ISS-02 | Unknown/untrusted issuer key ID | Reject | Trust-store lookup |
| CAP-ISS-03 | Signature does not verify over canonical bytes | Reject | Signature verifier |
| CAP-BND-01 | Principal differs from authenticated caller | Reject | Admission policy |
| CAP-BND-02 | Operation differs from exact requested command | Reject | Command binding |
| CAP-BND-03 | Resource/node differs from requested target | Reject | Resource binding |
| CAP-SCP-01 | Requested scope exceeds issued scope | Reject; attenuation only | Scope evaluator |
| CAP-TIM-01 | Issued-at is unreasonably in the future | Reject | Trusted clock policy |
| CAP-TIM-02 | Expired capability | Reject | Lifetime validator |
| CAP-REV-01 | Capability or issuer key is revoked | Reject | Revocation evaluator |
| CAP-REV-02 | Revocation state is stale/unavailable where policy requires freshness | Fail closed | Revocation evaluator |
| CAP-RPL-01 | Same one-time nonce/command ID replayed | Reject duplicate | Durable replay guard |
| CAP-QLF-01 | Self-asserted qualification string without required fresh evidence | Reject | Qualification policy |
| CAP-AUX-01 | Auxiliary capability requests execution or credential creation | Reject | Existing auxiliary policy |
| CAP-ALG-01 | Unsupported or downgraded signature algorithm | Reject | Algorithm policy |
| CAP-ENC-01 | Equivalent semantic envelope has non-canonical encoding / ambiguous fields | Reject before verification | Canonical parser |
| CAP-KEY-01 | Expired or rotated-out signing key used outside overlap policy | Reject | Key lifecycle policy |
| CAP-ERR-01 | Trust/revocation/replay backend unavailable | Fail closed, auditable reason | Admission orchestrator |

## Required positive and property tests

- Valid signed envelope from a trusted current issuer, correctly bound to principal/operation/resource, unexpired, non-revoked and not replayed is admitted only if independent qualification evidence and the existing node/auxiliary policy also pass.
- Attenuation may narrow scope but must never broaden operation, resource, duration, or constraints.
- Changing any signed field after signing invalidates verification.
- A capability accepted for one operation/resource is not reusable for a different one.
- Replay protection must be atomic under concurrent duplicate submissions.
- Failures must not log secret values or raw authorization tokens.

## Design constraints and governance

This is a proposed test matrix, not an approved protocol. Before implementation, decide via the applicable governance process: signature algorithm and canonical serialization, trust-root provisioning/rotation, issuer-to-principal mapping, clock skew, revocation consistency, nonce persistence/retention, failure reason taxonomy, schema migration/versioning, and backward-compatibility policy. Do not invent or silently choose cryptographic/key lifecycle semantics in implementation. Preserve historical IDs and Baseline 2.0.

## Current state / next action

Issue #301 remains open; PR #374/#375/#376 remain Draft/unmerged. SentinelX has zero connected hosts; Mac mini is offline; two development hosts are user-disabled; Codex Tasks has no registered environments. Gemini workflow authority and exact MCP OCI digest/provenance blockers remain unresolved.

Next: submit this matrix with the proposed signed envelope contract for independent architecture/governance review. After approval, implement tests first, then enforcement, and run exact-head CI. No code/schema/workflow changes, test execution, secret access, Gemini dispatch, merge, deployment, or qualification occurred in Wave 190.

Contour A remains **NOT QUALIFIED / NOT DEPLOYED / NOT INDEPENDENTLY ACCEPTED**.
