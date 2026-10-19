# MediaHub OS Contour A — mesh capability issuer/lifecycle crosswalk (Wave 189)

- Date: 2026-10-19
- Scope: read-only contract crosswalk, following the Wave 188 Gemini token-authority review.
- Canonical map: [MEDIAHUB-CHAT-TREE-MAP.md](../architecture/MEDIAHUB-CHAT-TREE-MAP.md)
- Wave 188 finding: [Gemini workflow token-authority review](MEDIAHUB-CONTOUR-A-GEMINI-WORKFLOW-TOKEN-AUTHORITY-REVIEW-WAVE-188-2026-10-19.md)
- Governing issue: [#301](https://github.com/VlDMlNSh/mediahub-os/issues/301)

## Frozen source refs and blobs

- `main` HEAD: `c06015e0b1526e0aaa6a522306052b077455aba5`.
- Canonical governance contract: `architecture/ASTRA-GOLD-GOVERNANCE-CONTRACT.yaml`, blob `1d3ac25e7817f365807ad85d0d7c9007bd48bebf`.
- Mesh capability schema: `architecture/mesh/capability.schema.json`, blob `d9360b62520aabd2fa8d74a2b74bf3fc328c9c7c`.
- Mesh admission implementation: `ops/mesh/admission.py`, blob `46e92d3c4f9b9865356443403e9ebd34587996cd`.
- Admission boundary tests: `tests/test_mesh_admission_boundary.py`, blob `1e047a5ffd3448ab83e9a2517b2cd73d3606bd28`.
- Capability-security contract summary: `docs/architecture/MH-12-capability-security.md`, blob `8723cdb100b7ca5526616464f9fcdef60f4c61b7`.

## Contract crosswalk

The MH-12 capability-security contract names candidate fields: issuer, principal, operation, resource, scope, constraints, provenance, issued_at, expires_at, and revocation_context. It states capabilities must be operation-specific, attenuation may only narrow authority, and controls must address delegation, revocation, replay, forgery, leakage, storage, transport, and confused deputy.

The current mesh JSON schema requires only schema_version, capability_id, provider, version, executable, identity_sha256, authority, and qualification_state (sandbox is optional). It uses `additionalProperties: false`. It does not currently encode the MH-12 issuer/principal/operation/resource/scope/provenance/time/revocation fields.

The admission implementation verifies node ACTIVE status, node_id/role presence, schema validity, EXECUTION authority, auxiliary-capability restrictions, and a qualification-state allowlist. It does not itself validate an issuer signature, binding to an exact requested operation/resource, expiration, revocation state, or replay context. The existing boundary tests cover inactive/missing node identity, CONTROL authority, unqualified state, a qualified execution capability, and auxiliary capability restrictions; the inspected tests do not demonstrate the missing lifecycle/issuer cases.

The canonical ASTRA GOLD governance contract also states that credentials must rotate, expire, revoke, and be audited; auxiliary credential creation is forbidden; cloud executors require admission, fresh execution rounds, isolated credential boundaries, independent A3, and cannot self-promote. Candidate cloud paths are recorded as NOT_PROVEN with no authority.

## Finding

There is a **contract-to-enforcement gap** between the capability-security field/control model and the mesh schema/admission implementation reviewed at the frozen `main` SHA. A schema-valid capability plus `authority: EXECUTION` and an allowed qualification string is not, by itself, proof of trusted issuer identity, operation-specific authorization, freshness, non-revocation, or replay resistance.

This is a source-level crosswalk, not a runtime exploit finding. No tests were run in this pass. The test file demonstrates that the qualified execution case can be admitted, but this pass did not execute that test.

## Proposed bounded next design (not approved or implemented)

1. Define a versioned capability envelope with issuer identity/key identifier, principal, exact operation and resource, constrained scope, issued/expiry timestamps, unique nonce or replay key, revocation reference, provenance, and signature/verification algorithm metadata.
2. Make admission fail closed unless issuer trust, signature, exact command/resource binding, expiry, revocation, and replay checks pass against trusted policy/state. Never infer trust from a hash field or self-asserted qualification string.
3. Keep qualification state evidence separate from issuer authentication; do not let a capability or executor self-qualify or self-promote.
4. Add negative tests for unsigned/unknown issuer, wrong principal, operation/resource mismatch, expired token, revoked key/capability, replayed nonce, stale trust data, and attempted authority widening. Add positive tests only for valid signed, current, correctly bound capabilities.
5. Treat schema evolution and enforcement changes as a separately reviewed contract migration; preserve historical IDs and current baseline semantics.

This proposal requires the repository's applicable governance/change-control process. No contract or authority decision is implied by this report.

## Current blockers and non-actions

- Wave 188's Gemini workflow token-authority gap remains unresolved; no workflow change or dispatch occurred.
- Exact OCI manifest/index digest and provenance for `ghcr.io/github/github-mcp-server:v0.27.0` remain unresolved.
- Issue #301 remains open. PR #374/#375/#376 remain Draft/unmerged.
- SentinelX has zero connected hosts; Mac mini is offline and `mh-dev-01` / `mh-dev-02` are user-disabled. Codex Tasks has no registered environments.
- No secrets read, host command, test execution, Gemini dispatch, merge, deployment, or qualification occurred.

## Next action

Submit the proposed capability envelope and fail-closed admission matrix for independent architecture/governance review. Implement only after approval, with issuer/lifecycle negative tests and fresh exact-head CI. Continue authorized registry digest/provenance work separately.

Contour A remains **NOT QUALIFIED / NOT DEPLOYED / NOT INDEPENDENTLY ACCEPTED**.
