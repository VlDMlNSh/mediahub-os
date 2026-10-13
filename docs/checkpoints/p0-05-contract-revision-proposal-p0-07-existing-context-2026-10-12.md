# P0-05 Contract Revision Proposal — P0-07 Existing-Context Compatibility

- Date: 2026-10-12
- Status: **PROPOSAL / GOVERNANCE REVIEW REQUIRED / NOT ACCEPTED / NOT FROZEN**
- Scope: documentary proposal only; no change to P0-04/P0-05 implementation or accepted artifacts.
- Decision owner: MediaHub product owner; security/governance reviewers required before normative adoption.
- Related domains: P0-04, P0-05, P0-07, MH-12.

## 1. Decision trail

The owner selected the P0-07 existing-context model as the first option, with a conditional fallback to revising the P0-05 contract if that model does not work.

This pass could not establish that the existing-context model is implementable against the current artifacts without adding a new context hand-off surface:
- P0-07's current request object carries one `AuthorizationContext` whose capability must belong to the P0-07 capability inventory.
- The accepted P0-05 `ConsumerBoundary` passes the supplied context to P0-04 for `begin`; commit/abort use the transaction's P0-04 authorization context.
- The current P0-07 operation boundary only validates/authorizes/evaluates and does not publish state.
- No current, source-bound caller path was found demonstrating that a P0-07 caller already carries a separate P0-04-authorized context and passes it to P0-05 unchanged.

This is **insufficient evidence for A**, not proof that no such path exists anywhere. No tests or runtime actions were performed.

## 2. Non-negotiable invariants

1. P0-04 remains the sole canonical mutation/transaction authority.
2. P0-05 remains the sole consumer boundary.
3. P0-07 authorization and policy ALLOW are necessary but do not substitute for P0-04 transaction authorization.
4. No capability translation, injection, self-grant, hidden privilege escalation, direct P0-04 calls, alternate transaction/version authority, persistence, or implicit publication bridge.
5. Any revision must preserve fail-closed behavior and stable sanitized failures.
6. No change to the accepted/frozen P0-05 artifact is made by this proposal.

## 3. Candidate contract question for governance

Can P0-05 expose an explicit, typed domain-operation hand-off for P0-07 that accepts:
- the P0-07 operation/capability decision and bounded canonical payload as inert inputs;
- an independently authorized P0-04 transaction context that is validated by the existing P0-04 authority;
- explicit binding between the authorized P0-07 operation, the target canonical state payload, and the P0-04 transaction;
- fail-closed rejection if either authorization fails or if operation, principal, resource, payload, generation, or transaction binding is inconsistent?

This is a question for controlled contract design, not an approved interface specification. No proposed signature or field layout is normative.

## 4. Required governance/evidence gates before adoption

- Identify the exact accepted P0-05 normative artifact and its commit/blob provenance; resolve the DRAFT-vs-accepted-tree discrepancy.
- Security review of the dual-authorization composition and principal/context binding.
- Explicit operation mapping and proof that no P0-07 capability is translated into P0-04 privilege.
- Define commit/abort context binding, replay/stale transaction handling, bounded payload validation, sanitized errors, and audit/provenance without leaking sensitive data.
- Update contradiction C-01/C-02 dispositions only with explicit decision records and source-bound evidence.
- Revision-bound threat-to-test traceability and negative-path test plan/results on the exact candidate commit; no status promotion from proposal alone.
- Explicit governance acceptance and freeze commit before any implementation change.
- Separate implementation authorization and fresh execution evidence before claiming implementation or qualification.

## 5. Current disposition

- Option A: **NOT DEMONSTRATED / REQUIRES VERIFICATION**. Existing-context reuse remains preferred if a current caller path can be proven without changing frozen contracts.
- Conditional option C: **PROPOSAL PREPARED FOR REVIEW ONLY**. The frozen P0-05 contract and implementation remain unchanged. This document does not accept or freeze a revision and does not authorize implementation.
- P0-07 mutation publication: **BLOCKED — GOVERNANCE/API GAP**.
- Production qualification: **NOT GRANTED**.

## 6. Next safe step

Resolve the accepted P0-05 artifact/path and prove or disprove the existence of a caller-supplied, independently P0-04-authorized context using repository source and commit/tree evidence. If A is proven, do not revise P0-05. If it is disproven, obtain explicit governance disposition on this proposal before any normative contract or implementation change.

## 7. Follow-up tree audit and conditional transition to option C (2026-10-12)

The exact tree for accepted implementation commit `303a766257b90c4356dcffc8967a5574e8e22e7a` was fetched through the Git Trees API:
- commit tree SHA: `82da63f03da20049954fe69257342cbf66b58395`;
- `docs/architecture/P0-05-consumer-contract.md` exists in that exact tree at blob `bba8dd3e8812767b6dbc8afff1bec5bd36dc828b`;
- that exact contract explicitly says **DRAFT — GOVERNANCE REVIEW REQUIRED**;
- the tree contains `runtime/mediahub_runtime/consumer_boundary.py` at blob `23b95f1b37cb35e311b61e3babcca4bd1aea9596`, but no P0-07 runtime module (P0-07 did not yet exist in that accepted P0-05 tree);
- the P0-07 reconciled tree `751659fbfe546a5cabd5d8c3f3110af05c2ef582` contains the P0-07 operation boundary at blob `1e3578f1503d0de452b92c1a549c77e4ecddf7bb` and authorization module at blob `260dcb2c5ab92cb319a8c20f6568a14e2cc9b5d3`; neither calls `ConsumerBoundary` or P0-05, and the tree has no implemented P0-07 mutation adapter. The operation boundary returns a decision only.
- P0-07's adapter contract blob `22b8e1897e124578e66c8d619b3e8eaf41f69a88` explicitly records that no approved existing-context hand-off is present and keeps mutation publication blocked.

The governance acceptance record `docs/architecture/P0-05-governance-acceptance.md`, blob `a0d28b4cfd9bed27e8a80968f6beac6cfdd97242`, records acceptance/freeze of the implementation at commit `303a766257b90c4356dcffc8967a5574e8e22e7a`, while the normative consumer contract present in that exact commit tree remains labelled DRAFT. This is a material source-status discrepancy; it does not justify silently treating the DRAFT contract as accepted normative text.

### Updated disposition

- Option A is **NOT AVAILABLE AS AN IMPLEMENTED END-TO-END PATH IN THE INSPECTED P0-07 TREE**. The source tree proves there is no implemented P0-07 → P0-05 caller/adapter there. This conclusion is bounded to the inspected tree and does not assert no other out-of-tree caller exists.
- Following the owner's conditional direction, option C is now the **NEXT GOVERNANCE REVIEW PATH**. This is authorization to prepare and submit the controlled revision proposal, not acceptance of new normative wording, not a freeze, and not implementation authorization.
- No accepted/frozen contract or code has been changed. Before a normative revision can be adopted, governance must resolve the DRAFT-vs-acceptance-record discrepancy, review the candidate contract, and record explicit acceptance/freeze against an exact blob and commit.
- Mutation publication remains **BLOCKED — GOVERNANCE/API GAP**.


## 8. Owner/governance disposition sheet (2026-10-13; blank pending decision)

**Purpose:** make the existing proposal actionable without duplicating it or implying approval. This section is a response template only. Blank fields mean no decision is recorded.

| ID | Decision requested | Permitted recorded disposition | Required record |
|---|---|---|---|
| D1 | Authorization composition | ACCEPT OPTION; REJECT; REQUEST REVISION; DEFER | Exact choice and rationale; security/governance reviewer |
| D2 | P0-04 context authority and lifecycle | IDENTIFY TRUSTED CALLER; PROPOSE GOVERNED AUTHORITY; REQUEST EVIDENCE; DEFER | Named authority/owner, lifecycle, principal binding, trust boundary and source evidence |
| D3 | Operation/payload decision binding | ACCEPT SPECIFIC BINDING RULE; REQUEST REVISION; DEFER | Exact binding fields/semantics, freshness/replay rule, threat-model basis |
| D4 | Initial P0-07 operation set | ACCEPT EXPLICIT ENUMERATED SET; REQUEST MAPPING; DEFER | Each operation → resource/canonical state shape → authority → invariants |
| D5 | Audit/privacy | ACCEPT AFTER JOINT REVIEW; REQUEST REVISION; DEFER | MH-06/MH-12/MH-13 reviewers and exact approved provenance/access/redaction/retention rules |
| D6 | P0-05 acceptance/header discrepancy | CONTRACT TEXT ACCEPTED; IMPLEMENTATION ONLY ACCEPTED; REQUEST EVIDENCE; DEFER | Governance interpretation tied to exact contract blob, implementation commit/tree, and acceptance-record blob; controlled correction separately authorized if needed |
| D7 | Contract change-control scope | P0-05 v1.1; SEPARATE INTEGRATION CONTRACT; REQUEST CHANGE-CONTROL REVIEW; DEFER | Exact path/version, supersession semantics and change-control authority |

### Cross-cutting owner disposition

- Product-owner decision / dated record: **PENDING**
- Security review / reviewer / evidence ref: **PENDING**
- Governance review / reviewer / evidence ref: **PENDING**
- Exact normative artifact path + blob SHA + commit SHA to accept/freeze: **PENDING**
- Explicit acceptance/freeze record: **PENDING**
- Separate implementation authorization + scope/commit boundary: **PENDING**
- Qualification authorization: **NOT REQUESTED BY THIS SHEET**

Do not treat an unfilled row, an investigation direction (including C→A or C→B), or an informal acknowledgement as an accepted contract decision. Any selected disposition must be recorded by the authorized owner/reviewer and then reconciled into the owner decision register, matrix, map and checkpoint with exact source refs. Until then the proposal remains **NOT ACCEPTED / NOT FROZEN**, and P0-07 mutation publication remains **BLOCKED — GOVERNANCE/API GAP**.


## 9. D6 decision analysis — exact scope of P0-05 governance acceptance (2026-10-13)

**Status:** owner/governance decision support only. This section records no decision and changes no protected contract, acceptance record, implementation or status.

### Evidence compared

1. Exact accepted implementation commit: `303a766257b90c4356dcffc8967a5574e8e22e7a`; exact tree: `82da63f03da20049954fe69257342cbf66b58395`.
2. Normative contract in that tree: `docs/architecture/P0-05-consumer-contract.md`, blob `bba8dd3e8812767b6dbc8afff1bec5bd36dc828b`, header `DRAFT — GOVERNANCE REVIEW REQUIRED`.
3. Governance acceptance record: `docs/architecture/P0-05-governance-acceptance.md`, blob `a0d28b4cfd9bed27e8a80968f6beac6cfdd97242`, says `ACCEPTED / FROZEN` and explicitly scopes the accepted state to the reviewed implementation commit. Its decision target names the Integration Boundary & Consumer Contract and controlled implementation, but its disposition does not separately identify the contract blob as an accepted/frozen normative artifact.
4. Governance decision packet: `docs/architecture/P0-05-governance-decision-packet.md`, blob `1253944ffeefcb59502d9f7deb13d38baed1d6e1`, records authorization to implement within the defined scope; it distinguishes implementation authorization, implementation acceptance, security exit and production qualification.
5. The current v1.1 candidate remains non-normative and explicitly instructs that the discrepancy must be decided before adoption. No later accepted D6 disposition was found in the inspected documentation-branch tree.

### Options, consequences and recommendation

| Option | Required finding | Consequence | Risk |
|---|---|---|---|
| **A — contract text was accepted; header is stale** | Authorized governance confirms the exact contract blob `bba8dd3e...` was part of the normative acceptance, not merely present in the implementation package. | A separately authorized, controlled status/header correction may be prepared against an exact reviewed revision; acceptance record remains immutable. | Incorrect if the acceptance was implementation-only; could silently promote draft wording. |
| **B — implementation only was accepted** | Authorized governance confirms acceptance applies to commit `303a766...` and does not separately accept the contract text. | Keep the existing implementation acceptance intact; route the normative text through controlled review, explicit acceptance/freeze and exact blob/commit recording before any v1.1 adoption. | Requires an additional governance cycle; avoids conflating implementation evidence with normative-text acceptance. |
| **C — defer pending more evidence** | Governance cannot determine A or B from the present record. | Preserve the discrepancy and all current blocked statuses; request a dated clarification or source record. | Keeps the bridge blocked until resolved. |

**Recommendation:** choose **C for the current evidence state**. The available records establish implementation acceptance and show the contract's DRAFT header, but do not unambiguously state whether the exact contract text was separately accepted as normative/frozen. If the owner requires a provisional working assumption while gathering evidence, use B as the conservative non-promotional assumption—not as a governance decision. Do not edit the header, acceptance record or candidate status without the authorized disposition.

### Required decision record

- Product-owner disposition (A/B/C) and date: **PENDING**
- Governance reviewer and exact supporting evidence: **PENDING**
- Exact normative artifact path + blob SHA + commit SHA, if A or later controlled acceptance: **PENDING**
- Authorized correction/review scope, if any: **PENDING**
- Separate implementation authorization and qualification remain distinct gates.

Until a valid decision is recorded, D6 remains **OPEN / GOVERNANCE AMBIGUITY**; P0-07 mutation/publication remains **BLOCKED — GOVERNANCE/API GAP**; P0-05 v1.1 remains **NON-NORMATIVE / NOT ACCEPTED / NOT FROZEN**; project qualification remains **NO-GO / NOT PROVEN**.


## 10. D1/D2 source-bound context audit and minimum design questions (2026-10-13)

**Status:** design/governance support only; this addendum is not an accepted contract, interface, security design or implementation authorization. The audit is limited to live `main` HEAD `1d45bbccbbbd27309c39cb9e9351bb291cdb47a8` and the documented P0-07 integration tree. No tests or runtime actions were performed.

### 10.1 Exact source findings

| Source | Live `main` blob | Evidence and limit |
|---|---|---|
| `runtime/mediahub_runtime/authorization.py` | `4d8df5d3c1c26f7f133a8093cd270635b085f4d5` | P0-04 `AuthorizationContext` contains `principal` and `capability`; `AuthorizationPolicy` grants only an explicit tuple of principal/capability/operation and otherwise denies. It validates context type, but this module alone does not establish who authenticated or issued the context. |
| `runtime/mediahub_runtime/consumer_boundary.py` | `98bf2da9cea85da2c82145b4baef417c20b9ae73` | P0-05 receives an `AuthorizationContext` and forwards it to injected State Authority for transaction begin; commit/abort use the transaction. This is the consumer/transaction seam, not an issuer or identity lifecycle. |
| `runtime/mediahub_runtime/astra_developer_context.py` | `d1806e5e91e16cb27d34d9331b9a25e25d606a46` | Parses a bounded mobile-facing context envelope; module explicitly says transport-neutral and contains no authentication or secrets. It is not a trusted P0-04 context source. |
| `runtime/mediahub_runtime/astra_context.py` | `9a30c0a3299e6b3a47bc03f55f4d26d2d9f14ad9` | Assembles bounded durable prompt context and marks memory as untrusted/advisory; explicitly not an authority. It cannot be reused as authorization context. |
| MH-06 Execution Context | `35647b282352f56d57f1bd476bff1503571c5650` | Requires explicit identity/service identity/capability/authorization/correlation/deadline/cancellation/resource/security metadata; context is descriptive/control metadata, not canonical state, and must be non-forgeable as required and re-established after restart. It does not name a concrete issuer or accepted provisioning implementation. |
| MH-12 Identity | `27eef9e23db02d6280b94a8e68bff9f73b0de88d` | Defines principal classes and lifecycle requirements (enrollment, activation, suspension/revocation, rotation/expiration, recovery); this is an architectural requirement, not proof of a deployed lifecycle service. |
| MH-12 Authentication | `a29c6a3cff0ee175a0c868214ffa2b455010002f` | Requires issuance, binding, expiry, refresh, revocation, replay resistance, failure handling and recovery; exact technology is explicitly non-canonical pending evidence/ADR. Invalid/expired/unverifiable/replayed context must fail closed. |
| MH-12 Authorization | `c48641861691714017aa5b1f99fe8eee8ea0e76a` | Requires explicit operation-specific, identity/context/policy-bound, auditable, fail-closed authorization terminating at the approved Consumer Boundary/State Authority. |
| Security/Trust/Authorization Contract | `8d831c2a8fa333977dd86524099568bae2a8db0e` | Describes target trust chain from boot/runtime trust context through authenticated principal, capability/policy evaluation and State Authority; target chain does not prove the concrete P0-07 caller wiring exists. |

### 10.2 Evidence-bounded conclusion

- **D1 — existing compliant composition:** NOT DEMONSTRATED in the inspected current `main` source tree. P0-04 authorization and P0-05 transaction forwarding exist; a caller path that authenticates a principal, binds the request to an independently authorized P0-04 context, and passes that context unchanged from P0-07 to P0-05 is not evidenced. This is bounded to inspected source; it is not a universal claim about out-of-tree components.
- **D2 — trusted P0-04 context source/lifecycle:** NOT EVIDENCED. The runtime modules found either validate an untrusted transport envelope, assemble advisory prompt context, or consume a caller-supplied context. MH-06/MH-12 specify lifecycle properties but do not identify an accepted concrete issuer/provisioner or revocation/freshness authority.
- Therefore the current repository does **not** justify reusing `DeveloperContextRequest`, ASTRA prompt memory, caller-supplied `principal/capability` fields, network/mesh membership, or P0-07 ALLOW as a trusted P0-04 context.
- D1's “reuse existing context” branch remains preferred only if further source-bound evidence appears. Based on this bounded audit, the conditional governed-design path is ready for owner/security review; it is not permission to implement.

### 10.3 Minimum design questions — no technology or API selected

A governed design review must answer, with explicit source and authority evidence:

1. **Issuer/authority:** which already-approved logical authority may authenticate/issue or establish P0-04 context? Who owns its lifecycle and key/credential trust root? If none exists, who may propose one for separate approval?
2. **Principal binding:** how is the authenticated principal bound to the exact P0-07 caller, request, operation, resource and P0-04 context without trusting caller-asserted identity?
3. **Capability separation:** how are P0-07 domain decision and P0-04 transaction authorization independently obtained and validated, with no capability translation or self-grant?
4. **Freshness/revocation/replay:** which accepted authority is source of truth for expiry, revocation, rotation, epoch/generation and replay resistance; what happens on stale or unavailable status? Default is fail-closed.
5. **Trust boundary/provenance:** where is untrusted transport input converted into authenticated context; what evidence binds that conversion to a specific source, revision and security boundary?
6. **Transaction/payload binding:** how is the domain decision bound to the exact canonical resource and bounded payload, and to the same P0-04 authority/state revision, without exposing raw transaction authority?
7. **Audit/privacy:** what minimal correlation/provenance is retained, who may read it, and how are credentials/secrets and sensitive payloads excluded or redacted?
8. **Failure semantics:** define deterministic fail-closed behavior for missing, invalid, expired, revoked, replayed, mismatched, or unverifiable context and for unavailable trust/revocation authority.

**Out of scope until separate governance and implementation authorization:** selecting cryptographic technology, token format, issuer/provisioner service, schema, API signature, persistence, adapter implementation, tests, qualification or deployment.

### 10.4 Current gate

D1 = existing composition NOT DEMONSTRATED; D2 = trusted issuer/lifecycle NOT EVIDENCED. P0-07 mutation/publication remains **BLOCKED — GOVERNANCE/API GAP**. P0-05 v1.1 remains **NON-NORMATIVE / NOT ACCEPTED / NOT FROZEN**. This audit changes no protected contract, owner decision, implementation or acceptance status.
