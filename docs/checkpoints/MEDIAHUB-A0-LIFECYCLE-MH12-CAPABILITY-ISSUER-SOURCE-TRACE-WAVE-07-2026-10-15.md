# MediaHub OS — A0 Lifecycle and MH-12 Capability Issuer Source Trace, Wave 07

- Date: 2026-10-15
- Status: **SOURCE TRACE COMPLETE FOR REVIEWED ARTIFACTS / INTERFACE GAPS OPEN / PROPOSAL ONLY**
- Purpose: close the next safe step from Wave 06 by mapping exact accepted ASTRA workflow rules and MH-12 security semantics to the missing Jarvis↔A0 integration contract.
- No endpoints, wire schemas, capability token formats, issuer identity, retry semantics or authorization defaults are invented here.
- This is not an accepted protocol, implementation, runtime inspection, test, qualification or acceptance.

## 1. Live ref state

- Repository: `VlDMlNSh/mediahub-os`
- `main` HEAD: `608d7463011798ca75e36bfce4b749a9caf4f9a0`
- Documentation branch: `docs/mediahub-chat-tree-map-20261012`
- Live comparison: `DIVERGED`, documentation branch 1182 ahead / 3 behind; merge base `f0f406feb9f9816b009f4e6e756813541e53b9bc`.
- No integration performed.

## 2. Primary-source trace

| Concern | Source / SHA | What the source establishes | What remains unproven |
|---|---|---|---|
| A0 role boundary | `architecture/ASTRA-GOLD-REFERENCE-ARCHITECTURE.md@main`, `7be5fadd3055642e7823c7233f90e978a87e5366`, §1; documentation branch copy `b354acfa4cff595583a7f1778371143e9868f293`, §1 | Main wording says “single MediaHub coordination and state authority”; docs-branch reference scopes A0 to ASTRA GOLD engineering coordination and ASTRA-internal queue/claim/gate state. Owner-approved DEC-DEV-02 Option C and the executor matrix separate engineering workflow state from canonical product state. | Main’s normative wording still needs controlled reconciliation. No branch integration authorized. |
| Queue/claim/lease | `docs/operations/ASTRA-EXECUTOR-CAPABILITY-MATRIX.md`, docs branch SHA `9ad83781a8da53d1a8f540ede54eba95281f01c0); `architecture/ASTRA-GOLD-GOVERNANCE-CONTRACT.yaml@main`, `1d3ac25e7817f365807ad85d0d7c9007bd48bebf` | ASTRA workflow owns dependency-aware dispatch, claims, lease/heartbeat/recovery, bounded admission, target-SHA binding and evidence/gate transitions. Governance YAML sets lease TTL 600 seconds and maximum three concurrent autonomous claims. | Exact public A0 ingress/API, persisted data model, fencing token/generation and external caller contract are not established by these sources. Numeric limits are contract values, not proof of live runtime behavior. |
| Retry/replay/recovery | ASTRA reference architecture `@main`, SHA `7be5fadd3055642e7823c7233f90e978a87e5366`, §§ recovery/idempotency; governance YAML SHA above | Source-level invariants include replay idempotency, stale-claim recovery, bounded retries and deterministic recovery or BLOCKED. Missing/contradictory evidence blocks promotion. | Exact idempotency-key scope, retention window, deduplication record, replay response, cancellation race semantics and fencing behavior are not fully defined as a Jarvis-facing wire contract. No global exactly-once guarantee is supported. |
| Security capability semantics | `docs/architecture/MH-12-security-architecture.md@main`, SHA `cf4ebfd5bf471ca676f075c51d3a24906504e490`, §§2, 8, audit | Capability is bound to principal, issuer, operation, resource/target, scope, constraints, provenance, lifetime and revocation context. Authorization is explicit, identity/policy-bound, auditable and fail-closed; ambiguity resolves to deny/safe containment. | Concrete issuer service, capability representation/signature, audience, expiry clock rules, revocation propagation, replay defence and A0 adapter verification procedure are not specified by MH-12 itself. |
| Candidate security technologies | MH-12 same SHA, final section | JWT/OAuth/OIDC/RBAC/ABAC/capability-token/mTLS/PKI/Keychain/Vault/TPM/etc. are candidates/unknown until evidence-based selection. | No technology or issuer may be treated as selected merely because named in a candidate list. |
| Jarvis ingress adapter | `docs/checkpoints/MEDIAHUB-JARVIS-CONTROL-PLANE-GITHUB-ADAPTER-CONTRACT-DRAFT-01-2026-10-14.md`, docs branch SHA `e112cc73178eef5f71b8a814296e4902c2e80390`, §§2–4 | Draft says the accepted A0 API, authentication, issuer and queue interface must be sourced; proposed mission fields are explicitly not a deployed wire format. | No accepted endpoint, request/response schema or concrete auth profile is identified. |
| Mission DAG/result envelope | `docs/checkpoints/MEDIAHUB-DISTRIBUTED-TASK-DAG-AND-RESULT-CONTRACT-CROSSWALK-WAVE-01-2026-10-15.md`, docs branch SHA `3669fb53d33d68e00186d40f3b4eaa6f9f5f0666`; `architecture/MH-21-CHAT-MASTER-PROMPT.md@main`, SHA `61d552db4d1a1abefa2cef9f44eebcf634d11111` | Existing ASTRA workflow and MH-21 define useful boundaries: external compute returns untrusted data; MediaHub decides; no distributed State Authority; task DAG/result schema remains a design gap. | No accepted corporation-wide DAG/result protocol or end-to-end exactly-once semantics. |

## 3. Contract gaps that must remain explicit

1. **Ingress identity:** accepted API base/path, transport, protocol version, caller identity and trust boundary are unknown in reviewed sources.
2. **Capability issuer:** issuer principal/service, signing/verification profile, audience, key rotation, expiry, revocation and audit event contract are not accepted at this integration boundary.
3. **Operation authorization:** mapping from Jarvis mission/task operation to A0 capability operations and resource scopes is not yet source-backed.
4. **Claim fencing:** lease TTL alone does not establish fencing against a stale worker. Required monotonic generation/fencing semantics and result-commit preconditions need an accepted source.
5. **Cancellation:** requested/accepted/propagated/terminal cancellation states, races with completion, and treatment of already-produced artifacts need a contract.
6. **Replay/idempotency:** key scope, payload binding, retention, duplicate response, and behavior after lease expiry/recovery need a contract. Do not promise global exactly-once execution.
7. **Result publication:** required target SHA, producer provenance, schema/policy revisions, artifact references, validation state and independent verification are described as design requirements, not one accepted wire schema.
8. **Fail-closed behavior:** missing/invalid/expired/revoked capability, unknown route, stale lease, conflicting result or unavailable authority must not fall back to a permissive route or grant canonical product-state authority.

## 4. Safe disposition / proposal

- Reuse ASTRA’s existing internal workflow semantics; do not create a parallel Jarvis queue or let Jarvis write A0 internals.
- Treat Jarvis as a mission submitter and result/status consumer through a future explicitly accepted A0 interface.
- Treat capability tokens and executor results as untrusted until the A0/security boundary validates identity, scope, expiry/revocation, target binding and policy.
- Keep MediaHub Product State Authority as the only canonical product-state mutation authority.
- Keep corporation DAG/result envelope, API endpoint, auth scheme and issuer as **OPEN / NOT ACCEPTED** until primary accepted contracts or an explicit owner decision establish them.
- Next governance artifact should be a change proposal with fields: decision required, options, trust/security consequences, compatibility impact, migration/rollout, evidence required, rollback and owner acceptance. This report does not select the options.

## 5. Effect on Wave 05 classes

- **C-01:** source boundary is now exact; docs branch scoped, main reference architecture still uses broader wording. Partial only; main-side fix remains blocked by branch/change-control constraints.
- **C-03:** branch divergence rechecked; no integration.
- **C-05:** contract boundary confirmed; runtime conformance remains unverified.
- **C-06:** semantic requirements confirmed; concrete issuer lifecycle remains an open governance/interface gap.
- **C-07:** existing DAG crosswalk is sufficient for requirements inventory, not an accepted schema.
- **C-09:** main generated qualification truth is G0–G11 BLOCKED and overall NOT_PROVEN/BLOCKED; readiness label is not a qualification result.
- **C-12:** roadmap has a dated supersession block; historical continuation entries remain historical. Map/checkpoint current pointers need continuous freshness updates.

## 6. Verification boundary

This pass used GitHub source reads and branch comparison only. It did not invoke tests, qualification, models/providers, credentials, runtime/host inspection, installations, infrastructure changes, deployment or branch integration. Source-level assertions are not runtime evidence.

## 7. Live source-anchor refresh — /next 2026-10-15

This dated addendum supersedes only the stale branch-count snapshot in §1; it preserves the original observation as historical evidence. A fresh GitHub compare reports `main` HEAD `608d7463011798ca75e36bfce4b749a9caf4f9a0`, documentation branch `DIVERGED`, ahead 1212 / behind 3, merge base `f0f406feb9f9816b009f4e6e756813541e53b9bc`. No branch integration was performed.

### Re-read current source anchors

| Source | Live ref | Blob SHA | Bounded observation |
|---|---|---|---|
| `runtime/mediahub_runtime/authorization.py` | `main` | `4d8df5d3c1c26f7f133a8093cd270635b085f4d5` | `AuthorizationContext` contains `principal` and `capability`; policy matching uses principal/capability/operation. This is grant matching, not evidence of issuer provenance or lifecycle. |
| `runtime/mediahub_runtime/consumer_boundary.py` | `main` | `98bf2da9cea85da2c82145b4baef417c20b9ae73` | Boundary accepts typed `AuthorizationContext`; inspected request seam does not itself evidence issuer, audience, expiry or revocation verification. |
| `runtime/mediahub_runtime/in_memory_state.py` | `main` | `0fbc71369d19e09944ba67a60ccb9df802f30a4b` | Authority checks context type and uses configured authorization policy; the inspected seam does not establish how context was issued. |
| `runtime/mediahub_runtime/lifecycle_service.py` | `main` | `0b9d3d888e988615f1ad8cd50b1bef22f2be011b` | Lifecycle request carries the typed context and declares `runtime.lifecycle.transition`; capability string equality is not proof of authenticated principal or trusted issuance. |
| `docs/architecture/MH-12-security-architecture.md` | `main` | `cf4ebfd5bf471ca676f075c51d3a24906504e490` | Security architecture distinguishes principal, credential, session, capability and authorization, and specifies a layered trust path. It does not, by itself, instantiate the concrete issuer/API lifecycle. |
| `docs/operations/ASTRA-EXECUTOR-CAPABILITY-MATRIX.md` | documentation branch | `9ad83781a8da53d1a8f540ede54eba95281f01c0` | Reusable ASTRA-internal workflow capability matrix; not an accepted Jarvis-facing ingress API. |

**Bounded disposition:** source anchors were refreshed, but no accepted Jarvis→A0 ingress contract, concrete capability issuer/delegation lifecycle, or complete expiry/revocation/replay/fencing/cancellation semantics was established by these reads. P0-07 remains proposal-only / NOT ACCEPTED; P0-05/P0-04 edges must not be inferred from a shared context type. This is source inspection only, not a vulnerability determination, runtime verification, test or qualification. No tests, installations, provider/model calls, credentials, host/runtime inspection, infrastructure changes, deployment, merge, rebase or cherry-pick occurred.


## 8. Cross-ref boundary revalidation — /next 2026-10-15

**Scope:** read-only comparison of the current `main` authorization/consumer seam with the `implementation/p0-05-consumer-boundary` and `integration/p0-07-runtime-reconciled` refs, plus MH-12 and the existing P0-07 proposal. This is a bounded source comparison, not an acceptance or runtime claim.

| Source | Ref | Live blob SHA | Direct observation |
|---|---|---|---|
| `runtime/mediahub_runtime/authorization.py` | `main` and `implementation/p0-05-consumer-boundary` | `4d8df5d3c1c26f7f133a8093cd270635b085f4d5` on both | Same `AuthorizationContext(principal, capability)` and explicit grant matching by (principal, capability, operation). No issuer, audience, expiry, revocation, or request/resource/revision binding is represented in this type. |
| `runtime/mediahub_runtime/consumer_boundary.py` | `implementation/p0-05-consumer-boundary` and `integration/p0-07-runtime-reconciled` | `23b95f1b37cb35e311b61e3babcca4bd1aea9596` on both | The refs contain the same P0-05 boundary implementation. The presence of the module on the P0-07 integration ref does not itself prove a P0-07 caller→P0-05 invocation edge or trusted context issuance. |
| `runtime/mediahub_runtime/consumer_boundary.py` | `main` | `98bf2da9cea85da2c82145b4baef417c20b9ae73` | Main contains a nearby boundary revision; typed caller-supplied context is forwarded to the authority seam. The inspected boundary does not establish issuer lifecycle verification. |
| `docs/architecture/MH-12-security-architecture.md` | `main` | `cf4ebfd5bf471ca676f075c51d3a24906504e490` | Defines a layered identity→authentication→trust→capability→authorization→policy→consumer-boundary→State Authority path and sole canonical mutation authority; status remains governance-review-required and does not instantiate a concrete issuer. |
| Existing P0-07 D2 proposal | documentation ref | `c0ae0d3fe340c3e50382b7d4aa8da7b6b5f56d9f` | Explicitly proposes governance of a trusted-context lifecycle and marks D1/D2/D3/D6 open; it is not an accepted contract. |

**Result:** no direct, accepted producer→consumer edge was established across P0-07 → P0-05 → P0-04 by these source reads. P0-05 implementation lineage and a P0-05 governance acceptance record do not resolve the separate discrepancy that the referenced consumer contract text retains a DRAFT header. Preserve D6 as OPEN; do not alter the protected contract header or infer normative acceptance. P0-07 remains proposal-only; mutation/publication remains BLOCKED — GOVERNANCE/API GAP. P0-04 remains the sole canonical transaction/state mutation authority.

**Next evidence needed:** an accepted source naming the context issuer/attester and verifier, a source-backed P0-07 caller/adapter edge into the P0-05 boundary, and the exact governed P0-05 contract-status disposition. If no such source is available, route these items to owner/governance and continue only independent work. No tests, installs, credentials, provider/model calls, host/runtime inspection, qualification, infrastructure change, deployment, merge, rebase or cherry-pick occurred.

## Source-edge refresh — P0-05 contract-status and P0-04 mutation boundary (2026-10-15)

**Scope:** read-only source comparison; this addendum updates evidence only and does not accept a proposal, amend a normative contract, or authorize implementation.

| Source | Live ref / blob SHA | Directly established | Not established |
|---|---|---|---|
| `runtime/mediahub_runtime/authorization.py` | `main` / `4d8df5d3c1c26f7f133a8093cd270635b085f4d5` | `AuthorizationContext` contains only `principal` and `capability`; policy grants are exact tuples of principal, capability and operation; absent grant denies. | Issuer/attester, audience, expiry, revocation, request/resource/payload/revision binding, signed representation or external verifier. |
| `runtime/mediahub_runtime/consumer_boundary.py` | `main` / `98bf2da9cea85da2c82145b4baef417c20b9ae73` | P0-05 facade mediates begin/commit/abort/snapshot/restore through the injected authority; request context is typed; transaction handles are opaque at this facade. | A P0-07 caller/adapter edge, trusted context issuance, persistence or distributed fencing. The implementation file alone does not prove end-to-end caller wiring. |
| `docs/checkpoints/p0-05-consumer-contract-v1.1-candidate-for-governance-review-2026-10-12.md` | documentation ref / `79e2b4865c47b5394ade266cd3cd7cfbe3097717` | Explicitly NON-NORMATIVE / NOT ACCEPTED / NOT FROZEN. Records the discrepancy between DRAFT-labelled contract text and a separate implementation acceptance record; D6 requires owner/governance disposition. | Whether acceptance covered the exact contract text. Do not edit the DRAFT header or treat this candidate as normative. |
| `docs/checkpoints/p0-05-contract-revision-proposal-p0-07-existing-context-2026-10-12.md` | documentation ref / `fce7019b3430a95d12f723a769d39e1cd29067af` | Existing-context approach remains a proposal; no source-bound caller path was established in its bounded audit. | Accepted hand-off/API, P0-04-authorized context delivery or approval of proposal clauses. |
| P0-04 state authority implementation | `main` / `runtime/mediahub_runtime/in_memory_state.py`, blob `0fbc71369d19e09944ba67a60ccb9df802f30a4b` (previously live-read; refresh required before any future reliance) | Existing source lineage assigns canonical transaction/state mutation to the P0-04 authority; P0-05 is the facade in the current inspected path. | This pass did not re-fetch the full P0-04 source body; do not infer further transaction guarantees from the recorded SHA alone. |

### Edge disposition

- **P0-07 → P0-05:** `NOT ESTABLISHED` — no accepted caller/adapter contract or live source edge identified.
- **P0-05 → P0-04:** `IMPLEMENTATION SEAM OBSERVED` — the facade invokes the injected authority; this is source-level code evidence, not an accepted cross-domain integration contract or runtime verification.
- **Trusted context / capability issuer:** `OPEN` — principal/capability typing and grant matching do not prove issuance, attestation, audience, freshness or revocation.
- **P0-05 governance status:** `OPEN / OWNER-GOVERNANCE REQUIRED` — DRAFT header vs implementation acceptance-record discrepancy remains unresolved.
- **P0-04 authority:** remains the sole canonical mutation authority; no alternate authority is proposed.

**Bounded result:** source anchors sharpen the distinction between an observed in-process P0-05→P0-04 code seam and the absent accepted P0-07→P0-05 trust/ingress contract. No direct edge is promoted to accepted normative status. GitHub code search returned no useful hits for P0-04/P0-05 terms; because the connector search is known to be non-diagnostic here, zero results are not evidence of absence. Exact candidate files were fetched directly.

No tests, installs, credentials, provider/model calls, host/runtime inspection, qualification, infrastructure changes, deployment, merge, rebase or cherry-pick were performed.


## Source-contract comparison — ASTRA executor capability matrix ref drift (2026-10-15)

**Scope:** read-only comparison of the same canonical-path artifact across `main` and the documentation branch, alongside the current MH-12 security architecture/invariants. This addendum records the exact wording delta; it does not modify either normative/source contract.

| Source | Ref / blob SHA | Direct observation |
|---|---|---|
| ASTRA executor capability matrix | `main` / `da26185254d9954fcee204f81ecca129bf052e7c` | Status says `CANONICAL EXECUTOR-WORKFLOW POLICY`; table row 19 says `Global coordination/state` and `autonomous queue + claim/evidence state`. This wording is broader/ambiguous against the owner-approved separation of corporation missions, ASTRA-internal workflow state and canonical product state. |
| Same matrix | `docs/mediahub-chat-tree-map-20261012` / `9ad83781a8da53d1a8f540ede54eba95281f01c0` | Same status and core workflow policy, but row 19 narrows the capability to `ASTRA workflow/control state`, explicitly excluding MediaHub Product State Authority; lines 109–110 clarify that “state” means ASTRA engineering workflow/control state, not canonical product state. |
| MH-12 security architecture | `main` / `cf4ebfd5bf471ca676f075c51d3a24906504e490` | States the layered identity/authentication/trust/capability/authorization/policy/consumer-boundary/state-authority path, that capability cannot self-grant, and that authorization never bypasses Consumer Boundary or State Authority. Status is architecture complete / governance review required. |
| MH-12 security invariants | `main` / `0609be9c3420070434014dad4529e4ccd46b0996` | Labels invariants `PROPOSED → READY FOR GOVERNANCE REVIEW`; SI-01 says State Authority is sole canonical mutation authority, SI-02 distinguishes authentication from authorization, SI-04 prohibits bypassing State Authority, and SI-18/SI-19 require fail-closed handling of malformed/ambiguous security input. |

### Disposition

- **Confirmed documentation-ref drift:** the documentation branch contains a scope clarification absent from the `main` blob. It is consistent with owner-approved DEC-DEV-02 Option C (Jarvis corporation mission coordination; ASTRA A0 owns ASTRA-internal queue/claim/lease/retry/cancellation/evidence-gate state; Product State Authority alone mutates canonical product state).
- **Not a runtime finding:** neither source wording nor the comparison proves deployed enforcement, accepted A0 ingress, a trusted-context issuer, fencing, cancellation/replay behavior, or end-to-end caller wiring.
- **No automatic promotion:** the matrix's canonical-policy label and the MH-12 documents' governance-review status must be kept distinct. Do not overwrite `main`, merge branches, or treat documentation-branch wording as merged/accepted on `main` without the authorized integration/governance path.
- **Related blockers remain open:** P0-07 → P0-05 accepted caller/adapter edge NOT ESTABLISHED; trusted-context issuer/attester/verifier lifecycle OPEN; P0-05 D6 contract-status discrepancy OPEN / OWNER-GOVERNANCE REQUIRED; P0-04 remains sole canonical mutation authority.
- **Next:** retain the source-anchored delta in this trace and the corporation reconciliation. Continue the schema inventory only from existing files and stable IDs; do not draft a new normative wire schema until ingress/identity ownership and ref conflict are resolved. No tests, installs, credentials, provider/model calls, host/runtime inspection, qualification, infrastructure change, deployment or branch integration occurred.
