# MediaHub OS Contour A — authority and publisher boundary audit (Wave 206)

- Date: 2026-10-19
- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
- Governance tracker: https://github.com/VlDMlNSh/mediahub-os/issues/301
- Candidate PR: https://github.com/VlDMlNSh/mediahub-os/pull/375
- Disposition: source audit and readiness sync; no worker dispatch or governance promotion.

## Current exact evidence

- PR #375: OPEN / Draft / unmerged; current observed head `6fb078aad7e8e1bb41916168fdd038dfa4e1022b`; PR updated 2026-10-19T17:35:05Z. Compare against `main` at audit time: 11 commits ahead, 0 behind, merge base `c06015e0b1526e0aaa6a522306052b077455aba5`. Re-check refs before any later integration decision.
- Candidate workflow blob at PR head: `c24ad16ab8ed59fd4dbad9538063f63a933eab2c`.
- Current main worker workflow blob: `f650f2416c19dc75b4a0eeec037661c0c6169910`.
- Main mesh validator blob: `416a7ecaf4add9d0b81f0467cf426d9c7deb3ec7`.
- Main mesh admission blob: `46e92d3c4f9b9865356443403e9ebd34587996cd`.
- Capability schema blob: `d9360b62520aabd2fa8d74a2b74bf3fc328c9c7c`.
- Canonical ASTRA governance contract blob: `1d3ac25e7817f365807ad85d0d7c9007bd48bebf`.
- Wave 205 oracle test blob at PR head: `2c5fae2d431ca765bb548f4a2b5d70874961a438`.

## P0 finding: main still carries write authority

The worker workflow on current `main` explicitly declares workflow-level `permissions: contents: write` (line 35) and all three checkout steps set `persist-credentials: true` (lines 56, 97, 138). The PR candidate changes these to `contents: read` and `persist-credentials: false` at the same locations. This is a material, concrete risk reduction in the candidate, but it is not yet integrated. Do not report the main branch as credential-minimized.

PR candidate patch changes only the workflow permission/checkout credential persistence and adds semantic policy regression tests to Astra Verify. It does not itself establish a separately authorized publisher boundary or eliminate every possible publication path in the broader execution system. Keep PR Draft until independent review, branch protection and governance gates are verified.

## P0 finding: mesh capability validation is not an authenticated envelope

At `main`, `ops/mesh/validators.py` defines `validate_capability` over required fields `schema_version, capability_id, provider, version, executable, identity_sha256, authority, qualification_state`; it checks schema version, 64-hex identity digest, authority enum and qualification state. The capability JSON schema is structural and includes no signature, issuer, operation, resource, expiry, revocation or nonce/replay fields. `ops/mesh/admission.py` calls this validator, requires `EXECUTION` authority, and checks qualification/auxiliary policy, but the inspected path does not authenticate a signed capability envelope or bind the grant to an exact operation and resource.

The governance contract defines broader credential lifecycle and human-approval concepts, but presence in a governance document does not prove the mesh admission path enforces them. The Wave 190/191 source inventories are prior evidence and should be reconciled against current main before implementation.

## P1: YAML oracle scope

Wave 205's `UniqueKeyLoader` rejects duplicate YAML mapping keys and has negative fixtures. Exact-head PR CI was green:
- [Astra Verify run 39295373907](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39295373907), job `118206367053`.
- [Astra Cloud Runtime Validation run 39295373833](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39295373833), job `118206368089`.

These runs are evidence for commit `6fb078aad7e8e1bb41916168fdd038dfa4e1022b`, not a substitute for a new CI run if that commit changes. Parser-based tests still do not fully emulate GitHub Actions schema/permission evaluation or server-side authorization.

## Architecture options, ranked

1. **Preferred:** worker creates a quarantined patch/artifact without repository write credentials; trusted publisher independently reconstructs from immutable base SHA, validates issuer/capability, repository/ref, path allowlist and diff, uses a narrow short-lived grant, records provenance and verifies remote SHA.
2. **Conditional:** GitHub App installation token or equivalent short-lived publisher credential, only after governance approves issuer/key lifecycle, audience, repository/ref/path constraints, expiry, revocation, replay prevention and audit semantics.
3. **Not acceptable as default:** model-controlled worker with ambient `contents: write` and persisted checkout credentials.

## Readiness / gates

- Candidate credential minimization: **CI-verified on PR candidate; not yet integrated**.
- Current main worker credential boundary: **NOT MINIMIZED** based on current main workflow blob.
- Mesh signed capability enforcement: **NOT PROVEN / gap remains**.
- Independent review and branch protection: **NOT VERIFIED**; prior branch-protection API returned 403, which is not evidence of protection.
- Issue #301: OPEN.
- Contour A: **NOT QUALIFIED / NOT DEPLOYED / NOT INDEPENDENTLY ACCEPTED**.
- Contour B: **GATED**.

No worker/Gemini/provider dispatch, secret access, host command, merge, deployment, qualification or acceptance occurred.

## Next action

1. Independently review PR #375 and verify branch-protection/ruleset state using an authorized evidence source.
2. Define and govern the issuer/capability envelope contract before implementation: issuer trust roots, audience, exact operation/resource, source/ref binding, issued-at/expiry, revocation, nonce/replay semantics, canonical serialization and key rotation.
3. Implement fail-closed envelope verification and adversarial tests only after the contract is accepted; verify that mesh admission and runtime execution consume the same grant semantics.
4. Design the trusted publisher as a separate authority boundary; test wrong repository/ref/SHA, forbidden paths, symlink/binary/oversized patches, forged metadata, expired/revoked/replayed grants, cancellation/races, audit outage and remote SHA mismatch.
5. Re-fetch PR head and exact-head CI before any integration. Do not merge or promote readiness based on the present evidence alone.
