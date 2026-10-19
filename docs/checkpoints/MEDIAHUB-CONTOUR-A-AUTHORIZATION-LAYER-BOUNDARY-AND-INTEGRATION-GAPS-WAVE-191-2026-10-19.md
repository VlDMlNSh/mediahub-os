# MediaHub OS Contour A — authorization-layer boundary and integration gaps (Wave 191)

- Date: 2026-10-19
- Scope: source-level cross-layer inventory; documentation only, no implementation edits or test execution.
- Canonical map: [MEDIAHUB-CHAT-TREE-MAP.md](../architecture/MEDIAHUB-CHAT-TREE-MAP.md)
- Previous matrix: [Wave 190 capability admission negative-test matrix](MEDIAHUB-CONTOUR-A-CAPABILITY-ADMISSION-NEGATIVE-TEST-MATRIX-WAVE-190-2026-10-19.md)
- Governing issue: [#301](https://github.com/VlDMlNSh/mediahub-os/issues/301)

## Frozen source baseline

- `main` HEAD: `c06015e0b1526e0aaa6a522306052b077455aba5`.
- `ops/mesh/validators.py`: blob `416a7ecaf4add9d0b81f0467cf426d9c7deb3ec7`.
- `ops/mesh/admission.py`: blob `46e92d3c4f9b9865356443403e9ebd34587996cd`.
- `ops/mesh/heartbeat_auth.py`: blob `6cb4adfb616389867c1e6f2490c256e76d0f95a5`.
- `tests/test_mesh_admission_boundary.py`: blob `1e047a5ffd3448ab83e9a2517b2cd73d3606bd28`.
- `tests/mesh/test_admission_authority.py`: blob `669e1661ae9e2b94e7a21b7b0a51300fb47fae20`.
- `astra_github_agent.py` command auth tests: `tests/test_astra_command_auth.py`, blob `8df49fc55e660c13ad54aca9b9dc78132c335dd1`.
- `runtime/mediahub_runtime/authorization.py`: blob `4d8df5d3c1c26f7f133a8093cd270635b085f4d5`.
- `architecture/SECURITY-TRUST-AUTHORIZATION-CONTRACT.md`: blob `8d831c2a8fa333977dd86524099568bae2a8db0e`.
- `docs/architecture/MH-12-authorization.md`: blob `c48641861691714017aa5b1f99fe8eee8ea0e76a`.
- `docs/architecture/MH-12-capability-security.md`: blob `8723cdb100b7ca5526616464f9fcdef60f4c61b7`.

## Findings: keep the layers distinct

1. **Mesh capability admission.** The inspected schema/validator checks required structural fields, schema version, digest shape and authority enum. Admission enforces active node identity, EXECUTION authority, qualification-state policy and auxiliary restrictions. The minimal test `tests/mesh/test_admission_authority.py` accepts a qualified EXECUTION capability without issuer/signature/operation/resource fields. This demonstrates the current API contract, not a demonstrated exploit in a deployed system.
2. **Heartbeat authentication.** `heartbeat_auth.py` canonicalizes JSON and checks HMAC-SHA256, expected node identity, timestamp age/future skew and optional sequence monotonicity. This authenticates heartbeat records, not capability envelopes; do not count it as issuer verification for admission.
3. **Astra command authentication.** `tests/test_astra_command_auth.py` checks that a signed command is rejected when its operation is changed and rejects stale commands. This is a separate command channel and is evidence that operation-binding checks exist there. It does not prove mesh admission is coupled to that verifier, nor does the inspected test alone establish durable command-ID replay protection.
4. **Runtime authorization seam.** `runtime/mediahub_runtime/authorization.py` is default-deny unless an exact tuple of principal, capability, and operation is explicitly granted. Its small API does not itself establish signed capability provenance, expiry/revocation, or resource binding.
5. **Architecture contracts.** Security/Trust/Authorization Contract and MH-12 require explicit identity-bound, operation-specific, resource-aware, fail-closed authorization and prohibit bypassing Consumer Boundary / State Authority. These are normative requirements; they do not alone prove all implementation paths enforce them.

## Integration tests needed (proposal)

| ID | Cross-layer test | Required assertion |
|---|---|---|
| AUTH-X-01 | A capability lacking trusted issuer proof enters mesh admission | Denied before executor is made eligible |
| AUTH-X-02 | A valid Astra command is presented with a capability for a different operation | Denied; command authentication cannot override capability binding |
| AUTH-X-03 | A valid command targets a different node/resource than the capability | Denied |
| AUTH-X-04 | Runtime allow-list grants principal/capability/operation but upstream identity proof is missing | Mutation still denied at trust boundary |
| AUTH-X-05 | Qualification is valid but capability is expired/revoked | Denied; qualification is not authorization |
| AUTH-X-06 | Heartbeat HMAC is valid but capability signature is absent/invalid | Heartbeat may validate independently; executor admission must deny |
| AUTH-X-07 | Capability is narrowed downstream then a child attempts scope expansion | Denied |
| AUTH-X-08 | Concurrent duplicate command/capability replay reaches separate admission workers | At most one execution for one-time authority |
| AUTH-X-09 | Revocation or trust service is stale/unavailable | Fail closed under the approved freshness policy |
| AUTH-X-10 | All layers pass but the mutation attempts to bypass Consumer Boundary / State Authority | Denied and audited |

## Governance and implementation boundary

This is an integration-gap proposal, not an authorization protocol approval. The design review must define the signed envelope and its binding to authenticated principal, exact operation, exact resource, bounded scope, expiry, revocation state, unique command/nonce and provenance; then define how existing Astra command HMAC and runtime grants compose without creating a second authority path. The command HMAC key must not be treated as a capability issuer key by assumption.

Do not choose signature algorithm, trust roots, key rotation, revocation consistency, replay storage, or compatibility migration without review. Preserve historical IDs and Baseline 2.0. Tests should be added before enforcement; schema changes and implementation require approved governance decisions and fresh CI.

## Current state and next action

Issue #301 remains open. PR #374/#375/#376 remain Draft/unmerged. SentinelX reports zero connected hosts; the Mac mini is offline and two development hosts are user-disabled; Codex Tasks environments are empty. Gemini workflow token authority and exact MCP OCI digest/provenance remain blockers.

Next: request independent review of this cross-layer matrix together with Wave 190, then implement cross-layer negative tests against an explicitly approved composition contract. No tests ran; no code/schema/workflow changed; no Gemini dispatch, secret access, merge, deployment or qualification occurred.

Contour A remains **NOT QUALIFIED / NOT DEPLOYED / NOT INDEPENDENTLY ACCEPTED**.
