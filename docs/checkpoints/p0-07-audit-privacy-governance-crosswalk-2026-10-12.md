# P0-07 × MH-06/MH-12/MH-13 — Audit, Privacy and Authorization Decision Packet

- Date: 2026-10-12
- Status: **NON-NORMATIVE / FOR OWNER + GOVERNANCE REVIEW / NO IMPLEMENTATION AUTHORIZATION**
- Scope: bounded documentary crosswalk for P0-07 mutation hand-off through P0-05, focused on authorization composition, decision evidence, audit provenance and privacy.
- Baseline rule: Functional Baseline 2.0 remains canonical; Baseline 1.0 remains historical. This packet does not change either baseline or any frozen P0 contract.
- Owner rule: product/architecture decisions remain with the owner unless explicitly delegated through a recorded governance decision.
- Safety rule: P0-07 canonical mutation/publication remains **BLOCKED — GOVERNANCE/API GAP** until the applicable normative interface is accepted and its authorization chain is evidenced.

## 1. Primary-source evidence

| Source | Ref / blob SHA | Source status and relevant content | Limit |
|---|---|---|---|
| MH-06 Observability | `main`; `a4c949d1ba21354d74f91cbb71864da3bbc13d36` | **PROPOSED**. Metrics/logs/traces/health/audit context/correlation IDs are observability surfaces; observability is non-authoritative; diagnostics must be bounded/sanitized; new diagnostic data paths require privacy/security review. | This artifact is proposed, not accepted/frozen. |
| MH-12 Authorization | `main`; `c48641861691714017aa5b1f99fe8eee8ea0e76a` | Authorization must be explicit, operation-specific, identity-bound, context/policy-aware, auditable and fail-closed. It terminates at the approved Consumer Boundary/State Authority contract and must not create an alternate mutation authority. | Authorization implementation details remain subject to separate evidence and governance. |
| MH-12 Contradiction Register | `main`; `4b3c101317330e47236937b17344299df53deee9` | C-01 security authorization vs P0-05 transaction authorization is REQUIRES VERIFICATION; C-02 P0-07 capability vs P0-04 transaction authorization is BLOCKED by the API/authorization bridge gap. | Explicitly blocks treating domain authorization as transaction authorization. |
| MH-13 Privacy/Data Governance | `main`; `e732ff9cacbc9c1189bd83306cdff30906326cf0` | Reconstructed privacy constraints: purpose limitation, minimization, classification before applicable external egress, explicit authorized bounded transfer, protected-data redaction, auditability without unnecessary payload disclosure, retention/deletion coordination with Persistence, derived data and metadata may remain sensitive. | Historical original not recovered; artifact says RECONSTRUCTED / PROPOSED and acceptance not verified. |
| MH-13 Governance State | `main`; `7bd2624c3072ecf0a08a430bb8b8214b3d55d3fa` | Records an independently accepted **reconstruction**, not historical recovery; Frozen NO; production implementation NOT AUTHORIZED; CI/build qualification NOT VERIFIED. | The accepted reconstruction status does not imply a frozen normative privacy contract. Governance state and artifact-header wording conflict and must remain visible. |
| MH-13 Reconstruction Registers | `main`; `8c66fb49bbe011d8ef5dd78287c72efdad77a8fe` | Unknowns include exact taxonomy, classification, consent/data-subject model, residency, retention/deletion/backup semantics, provider contracts, telemetry privacy, provenance and forensic privacy. | Do not invent values or represent unknowns as settled requirements. |
| P0-05 Consumer Contract | documentation branch `docs/mediahub-chat-tree-map-20261012`; `bba8dd3e8812767b6dbc8afff1bec5bd36dc828b` | Exact blob appears in governance-approved P0-05 tree/packet. | Header still says DRAFT; status reconciliation remains a controlled governance/documentation issue. |
| P0-05 v1.1 candidate | documentation branch; `79e2b4865c47b5394ade266cd3cd7cfbe3097717` | Non-normative candidate specifies decision-to-operation/resource/payload binding, independent P0-04 context, fail-closed behavior, freshness/replay handling, and bounded audit provenance. | Not accepted/frozen; requirements below are questions/proposals, not normative clauses. |
| P0-07 operation boundary | inspected integration tree; `1e3578f1503d0de452b92c1a549c77e4ecddf7bb` | P0-07-scoped principal/domain-capability authorization evaluates an operation and returns a decision; it does not itself publish canonical state or call P0-05. | Finding is bounded to the inspected tree. |
| P0-07 authorization module | inspected integration tree; `260dcb2c5ab92cb319a8c20f6568a14e2cc9b5d3` | Domain capabilities are restricted to `configuration.*` and `policy.*`. | These capabilities do not prove P0-04 transaction authorization. |

## 2. Cross-domain invariants that constrain every option

1. **One canonical mutation authority.** MH-06 observability, MH-12 security, MH-13 privacy and P0-07 domain authorization cannot become an alternate state authority.
2. **Authorization decisions are not executable capabilities.** A P0-07 decision is evidence to evaluate, not permission to bypass P0-05/P0-04.
3. **Independent transaction authorization.** P0-07 domain authorization cannot be translated into or self-grant P0-04 transaction authority.
4. **Exact-operation binding.** Any accepted hand-off must prevent a decision for one principal, operation, resource or candidate state from authorizing a different one.
5. **Fail closed.** Missing, denied, stale, malformed, ambiguous or inconsistent evidence cannot proceed to canonical mutation.
6. **Audit is not ordinary telemetry.** Audit provenance must be distinguishable from diagnostic logs; neither logging nor observability grants authorization.
7. **Minimize sensitive evidence.** Do not record raw payloads, credentials, secrets or unnecessary personal data merely to make an operation traceable. Metadata itself can be sensitive.
8. **Retention is not decided here.** Audit retention, deletion, backup copies, access control and legal/jurisdiction rules require explicit governance and coordination with Persistence; exact values remain unknown.
9. **No provider or external transfer assumption.** This packet does not authorize cloud/AI/provider egress.
10. **Evidence-bound statuses.** Architecture proposal, owner decision, implementation, verification, qualification and production authorization remain separate states.

## 3. Decision D1 — Composition of authorization

**Question:** How should the accepted flow combine the P0-07 domain decision with the independently authorized P0-04 transaction context, without allowing either to impersonate the other?

- **Option A — Two independent decisions plus already-authorized P0-04 context.** The caller supplies P0-07's inert decision evidence and a P0-04 context independently issued/authorized through an approved path. P0-05 validates both under its contract.
- **Option B — P0-05-owned orchestration.** P0-05 obtains the necessary domain decision and P0-04 authorization through separately approved interfaces; it does not create or translate authority.
- **Option C — Defer choice pending trust-boundary evidence.** Map current callers, authority ownership and failure semantics before choosing A or B.

**Recommendation:** **C first, then A if evidence shows a trusted caller can deliver an already-authorized P0-04 context without weakening the boundary; otherwise return to the owner with a concrete B proposal.** No choice is made by this packet.

## 4. Decision D2 — Delivery and lifecycle of P0-04 context

**Question:** Which trusted component obtains and delivers the P0-04 transaction context, and how are principal binding, scope, expiry/revocation and lifecycle represented?

- **Option A — Trusted caller supplies context.** Only if the caller is identified, trusted for that role, and the context is independently validated by P0-04/P0-05; caller-supplied bytes alone are not proof.
- **Option B — Separately governed authority component supplies context.** The authority, API, lifecycle and responsibility are explicitly named and accepted.
- **Option C — Keep blocked until ownership/evidence is mapped.**

**Recommendation:** **C until the authority and trust boundary are evidenced; then prefer the smallest existing approved path if it preserves independent P0-04 authorization.** No new identity protocol, token format or cryptographic scheme is selected.

## 5. Decision D3 — Decision evidence, exact binding, freshness and replay

**Question:** What evidence lets P0-05 establish that the P0-07 decision applies to this exact request and remains valid now?

- **Option A — Structured, immutable decision record.** Candidate attributes for governance review: decision identifier/version, principal reference, operation identifier, resource reference, candidate-state/payload digest or equivalent binding, policy/version reference, request correlation identifier, issuance/freshness metadata and decision result. Exact fields and trust source remain to be approved.
- **Option B — Existing approved signed/cryptographically protected envelope.** Only if an accepted threat model and existing system contract require it and specify key custody, rotation, verification and failure behavior.
- **Option C — Defer representation until threat model and caller flow are mapped.**

**Recommendation:** **C → A**: define the trust boundary and replay/staleness threats first, then prefer the minimum structured evidence that enforces exact binding. Do not add cryptography as decoration or treat a signature alone as authorization.

## 6. Decision D4 — Allowed operation mapping and canonical state shape

**Question:** Which exact P0-07 operations may request canonical mutation, and what precise canonical resource/state does each operation replace or update?

- **Option A — Publish the full P0-07 functional list immediately.** Not recommended: current evidence does not establish a complete operation-to-canonical-state mapping.
- **Option B — Preserve the full functional intent but initially allow only individually mapped and evidenced operations.** Unmapped or unsupported operations remain blocked.
- **Option C — Keep all mutation operations blocked until the complete mapping is accepted.**

**Recommendation:** **C → B**: first inventory and map each operation to canonical resource, schema, invariants, authorization and failure semantics; then allow only the minimal accepted set. This is not permission to implement that set.

## 7. Decision D5 — Audit provenance and privacy

**Question:** What is the minimum evidence needed to reconstruct the authorization chain and transaction outcome without turning audit logs into a copy of private state?

- **Option A — Full request/payload capture.** Rejected as default because it risks secrets and unnecessary personal-data retention; any exception would need separate justification and safeguards.
- **Option B — Minimized provenance record.** Candidate categories for review: correlated request/decision/transaction references; pseudonymous or otherwise minimized principal reference; operation/resource identifiers; decision/policy revision; outcome and bounded reason code; time/freshness; integrity/sequence metadata where required. Avoid raw payload and secrets; use a payload digest only if its privacy/leakage implications are assessed.
- **Option C — No audit record until all MH-06/MH-12/MH-13 schemas are finalized.** Safest short-term for avoiding an unapproved data path, but leaves audit contract unresolved.

**Recommendation:** **C → B**: obtain the applicable owner/security/privacy review first, then define a minimized provenance schema, purpose, authorized readers, retention/deletion, integrity requirements and failure behavior. Do not invent retention periods or claim legal compliance. MH-06 observability is PROPOSED; MH-13 is an accepted reconstruction but not frozen, so this recommendation requires governance approval.

## 8. Decision D7 — Contract boundary and versioning

**Question:** Should the new domain-operation hand-off become P0-05 v1.1 or be governed as a separate P0-07/P0-05 integration contract?

- **Option A — Amend P0-05 v1.1.** Only if change-control rules confirm this is within P0-05's responsibility and its normative versioning model.
- **Option B — Create a separately named integration contract with explicit dependencies on P0-05, P0-07 and P0-04.** P0-05 remains the consumer/mutation boundary; the new document specifies the cross-domain hand-off.
- **Option C — Defer versioning decision until the D1–D4 trust/API shape is understood.**

**Recommendation:** **C → B unless existing versioning rules clearly prove A is in-scope.** Do not duplicate the P0-05 contract or create a second mutation authority. No path/version is accepted by this packet.

## 9. D6 status reconciliation — evidence update, not an API decision

The governance-approved tree at commit `97a01977f521ba8304a455b5d7504896235ddea7` / tree `f926cd6c162f104c8c122cd17dae76dc28f32b19` contains the exact P0-05 contract blob `bba8dd3e8812767b6dbc8afff1bec5bd36dc828b` and the approval packet `1253944ffeefcb59502d9f7deb13d38baed1d6e1`, which explicitly approves the boundary and contract for controlled implementation. Therefore the evidence gap about whether this exact contract blob was included in the accepted package is materially closed.

**Remaining conflict:** the contract header still says DRAFT while the governance package records acceptance/freeze. Do not edit the header silently. The controlled disposition should record the accepted blob/commit and explicitly reconcile the header/status. This baseline acceptance does not accept this packet or unblock P0-07.

## 10. Acceptance gates before any implementation

1. Owner selects or explicitly delegates D1–D5 and D7; every choice is recorded with rationale, scope and evidence.
2. MH-12/security review validates independent authorization, identity/context binding, exact operation/resource/payload binding, freshness/replay and fail-closed behavior.
3. MH-06 observability and MH-13 privacy owners/governance review the proposed audit data path, minimization/redaction, access, retention/deletion, integrity and failure behavior.
4. MH-14/Persistence input resolves durable-copy, retention and deletion implications where applicable.
5. D4 operation mapping and canonical state shape are exact and accepted.
6. D7 contract boundary/versioning is explicitly decided; exact normative document/blob is reviewed and accepted/frozen through governance.
7. Requirement → threat → contract clause → acceptance criterion → negative-path verification evidence is traceable. This packet does not authorize executing tests.
8. A separate explicit implementation authorization is recorded.
9. Qualification and production authorization remain separate future gates.

## 11. Current disposition

- P0-05 baseline contract: exact blob is evidenced in the accepted governance package; contradictory DRAFT header remains for controlled reconciliation.
- MH-06 observability: PROPOSED.
- MH-12: authorization semantics are clear; C-01 and C-02 remain unresolved/blocked at the bridge.
- MH-13: accepted reconstruction, not frozen; production implementation not authorized; exact privacy taxonomy, retention and deletion semantics remain unknown.
- P0-07 → P0-05 mutation publication: **BLOCKED — GOVERNANCE/API GAP**.
- This decision packet: **NON-NORMATIVE / NOT ACCEPTED / NOT FROZEN**.
- No implementation, test, runtime execution, qualification, deployment, migration, infrastructure change, branch integration or merge is performed or authorized.

## 12. Source links

- [MH-06 Observability](https://github.com/VlDMlNSh/mediahub-os/blob/main/docs/architecture/MH-06-observability.md)
- [MH-12 Authorization](https://github.com/VlDMlNSh/mediahub-os/blob/main/docs/architecture/MH-12-authorization.md)
- [MH-12 Contradiction Register](https://github.com/VlDMlNSh/mediahub-os/blob/main/docs/architecture/MH-12-contradiction-register.md)
- [MH-13 Privacy / Data Governance](https://github.com/VlDMlNSh/mediahub-os/blob/main/docs/architecture/MH-13-privacy-data-governance.md)
- [MH-13 Governance State](https://github.com/VlDMlNSh/mediahub-os/blob/main/docs/architecture/MH-13-governance-state.md)
- [MH-13 Reconstruction Registers](https://github.com/VlDMlNSh/mediahub-os/blob/main/docs/architecture/MH-13-reconstruction-registers.md)
- [P0-05 Consumer Contract](https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/P0-05-consumer-contract.md)
- [P0-05 v1.1 candidate](https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/checkpoints/p0-05-consumer-contract-v1.1-candidate-for-governance-review-2026-10-12.md)
- [P0-07 adapter contract](https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/P0-07-adapter-contract.md)


## 13. D4 — P0-07 operation-to-canonical-state mapping (source-bound review, 2026-10-13)

**Status: PROVISIONAL MAPPING / NOT ACCEPTED / NOT IMPLEMENTATION AUTHORIZATION.** This section resolves what the inspected source currently says, not what the future contract should accept.

### Source evidence

- P0-07 branch: `architecture/mh-7-configuration-policy`, HEAD `83ccb0d4993761ffcd43146d982ff9781116c7db`; source lineage is branch-specific and is not proven reachable from current `main` (`1d45bbccbbbd27309c39cb9e9351bb291cdb47a8`).
- `runtime/mediahub_runtime/configuration_policy_operations.py`, blob `1e3578f1503d0de452b92c1a549c77e4ecddf7bb`: request contains `resource_type`, `operation`, `resource`, P0-07 `AuthorizationContext`, and optional typed payload. `decide()` validates, authorizes, evaluates policy and returns a decision; it does not call P0-05 or publish.
- `runtime/mediahub_runtime/configuration_policy_authorization.py`, blob `260dcb2c5ab92cb319a8c20f6568a14e2cc9b5d3`: exact capability inventory is 7 operations for each of `configuration` and `policy`: `read`, `validate`, `propose`, `update`, `replace`, `reset`, `delete`.
- `docs/architecture/P0-07-read-validate-boundary.md`, blob `ceb4e40ea3c41e0b4ec1d3e70eccc4616c77001f`: read is observation-only; until an authoritative source is defined, only an explicitly supplied immutable domain object may be inspected, and it is not thereby canonical persisted state.
- `docs/architecture/P0-07-mutation-authority-reconciliation.md`, blob `15b100f7c5351ea6ba0b5d0c8d2deca861d82063`: the only contemplated v1 publication unit is one complete configuration or policy document; cross-document atomicity and capability translation are prohibited.
- `docs/architecture/P0-07-p0-05-mutation-adapter-contract.md`, blob `22b8e1897e124578e66c8d619b3e8eaf41f69a88`: mutation remains blocked pending an approved independent P0-04 authorization hand-off.
- Current-main `runtime/mediahub_runtime/consumer_boundary.py`, blob `98bf2da9cea85da2c82145b4baef417c20b9ae73`: P0-05 `begin` forwards the supplied context to P0-04; commit/abort remain mediated by P0-05 and P0-04. This does not prove a P0-07 caller or a compatible trusted P0-04 context exists.
- P0-03 State Authority contract on `architecture/p0-03-state-authority-contract`, blob `2f35ed1b77c7979c9de50371c8a0f7a82f5d1e75`: canonical state is a complete immutable revision with generation and state-version metadata; transaction publication is atomic and stale transactions fail closed.

### Operation mapping inventory

| P0-07 operation | Domain-level meaning evidenced by source | Candidate canonical-state mapping | D4 disposition |
|---|---|---|---|
| `configuration.read` | Observation-only | No authoritative configuration source/key or canonical revision binding is defined | **UNMAPPED / READ SOURCE OPEN** |
| `configuration.validate` | Deterministic validation | No canonical mutation; validates supplied bounded configuration | **NO STATE WRITE** |
| `configuration.propose` | Inert proposal | Proposal is not canonical state and must not publish | **NO STATE WRITE** |
| `configuration.update` | Authorized domain operation with configuration payload | Candidate unit could be one complete configuration document; identity/resource and update-vs-replace semantics are not bound to a canonical key | **CONDITIONAL / INCOMPLETE** |
| `configuration.replace` | Authorized domain operation with configuration payload | Same candidate full-document unit; semantic distinction from update and target identity remain undefined | **CONDITIONAL / INCOMPLETE** |
| `configuration.reset` | Capability name only; reset target/default source is not established | No accepted canonical default/template or reset payload contract | **UNMAPPED** |
| `configuration.delete` | Capability name only; delete semantics are not established | No accepted deletion/tombstone/absence representation or invariants | **UNMAPPED** |
| `policy.read` | Observation-only | No authoritative policy source/key or canonical revision binding is defined | **UNMAPPED / READ SOURCE OPEN** |
| `policy.validate` | Deterministic validation | No canonical mutation; validates supplied bounded policy | **NO STATE WRITE** |
| `policy.propose` | Inert proposal | Proposal is not canonical state and must not publish | **NO STATE WRITE** |
| `policy.update` | Authorized domain operation with policy payload | Candidate unit could be one complete policy document; identity/resource and update-vs-replace semantics are not bound to a canonical key | **CONDITIONAL / INCOMPLETE** |
| `policy.replace` | Authorized domain operation with policy payload | Same candidate full-document unit; semantic distinction from update and target identity remain undefined | **CONDITIONAL / INCOMPLETE** |
| `policy.reset` | Capability name only; reset target/default source is not established | No accepted canonical default/template or reset payload contract | **UNMAPPED** |
| `policy.delete` | Capability name only; delete semantics are not established | No accepted deletion/tombstone/absence representation or invariants | **UNMAPPED** |

### D4 result and limits

- The source supports **14 named domain operations**, but does not establish an accepted set of canonical mutations. `validate` and `propose` are non-mutating; `read` lacks a canonical source; `update/replace` are only candidate full-document units; `reset/delete` have no defined canonical-state semantics.
- No source-bound mapping establishes `resource` → canonical State Authority key, exact canonical revision/generation binding, P0-07 decision-to-payload binding, or an unchanged independently P0-04-authorized context from a trusted caller.
- The P0-07 branch lineage and current-main P0-05 source are distinct refs. No end-to-end composition root or call edge is evidenced by this review.
- Do not mint stable operation IDs or promote candidate mappings into normative contract clauses. Owner/security/governance disposition remains required; P0-07 mutation/publication remains **BLOCKED — GOVERNANCE/API GAP**; P0-05 v1.1 remains **NON-NORMATIVE / NOT ACCEPTED / NOT FROZEN**.
- No implementation, tests, qualification, branch integration, deployment or status promotion occurred.
