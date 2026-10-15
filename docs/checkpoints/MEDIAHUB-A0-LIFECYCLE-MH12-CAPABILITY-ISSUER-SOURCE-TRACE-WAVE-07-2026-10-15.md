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
