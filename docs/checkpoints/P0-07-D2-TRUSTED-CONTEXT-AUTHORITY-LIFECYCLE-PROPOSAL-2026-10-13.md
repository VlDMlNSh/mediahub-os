# P0-07 D2 — Trusted Authorization Context Authority and Lifecycle Proposal

- Date: 2026-10-13
- Repository: `VlDMlNSh/mediahub-os`
- Documentation ref: `docs/mediahub-chat-tree-map-20261012`
- Status: **ARCHITECTURE PROPOSAL / GOVERNANCE REVIEW REQUIRED / NOT ACCEPTED / NOT FROZEN**
- Decision scope: prepare a governed design for trusted authorization-context issuance and lifecycle; this is not an implementation specification or authorization to implement.
- Related domains: P0-04, P0-05, P0-07, MH-04, MH-06, MH-12, MH-13.
- Owner decision: the product owner selected option B — prepare a separate proposal for review. This selection authorizes proposal preparation only.

## 1. Executive summary

The inspected evidence does not establish an approved trusted issuer or a complete lifecycle for the `AuthorizationContext` used across P0-07 → P0-05 → P0-04. The current P0-04 context is represented as `(principal, capability)`; the inspected P0-05 ConsumerBoundary forwards caller-supplied context. MH-04/MH-12 contain relevant identity, authentication, freshness, and revocation requirements, but their current proposed/review-complete status does not prove an accepted issuer or an implemented end-to-end trust path.

**Recommendation:** govern an explicit trusted-context authority boundary and lifecycle contract before implementation. Keep P0-04 as the sole canonical transaction/mutation authority, P0-05 as the consumer boundary, and P0-07 as a policy/operation decision boundary. No component may elevate its own authority by minting or translating capabilities.

This document intentionally does not select an identity provider, cryptographic format, token technology, service, schema, API signature, storage mechanism, or deployment topology.

## 2. Evidence baseline and bounded finding

The following inspected source records are the current evidence anchors recorded by the documentation branch:

- P0-04 authorization context on `implementation/p0-05-consumer-boundary`: blob `4d8df5d3c1c26f7f133a8093cd270635b085f4d5`.
- P0-05 ConsumerBoundary on `implementation/p0-05-consumer-boundary`: blob `23b95f1b37cb35e311b61e3babcca4bd1aea9596`.
- P0-05 governance acceptance: blob `a0d28b4cfd9bed27e8a80968f6beac6cfdd97242`.
- P0-05 decision packet: blob `1253944ffeefcb59502d9f7deb13d38baed1d6e1`.
- P0-05 consumer contract: blob `bba8dd3e8812767b6dbc8afff1bec5bd36dc828b`; the reviewed contract text remains labelled `DRAFT — GOVERNANCE REVIEW REQUIRED`, while the acceptance record describes the implementation state as accepted/frozen. D6 remains a separate open governance question.
- MH-04 identity model: `architecture/mh-04-security-trust-authorization`, blob `dccded8f572bed42e8f40e4240e91e5621f24a37`.
- MH-04 authentication: same ref, blob `834dd3f4036ba1668e4b8af132393e25c70c85eb`.
- MH-04 credential boundaries: same ref, blob `7b5db076bb5a948def0fc4d72dd58740828660c5`.
- MH-04 review record: same ref, blob `177fe4a3b3006c0cacfaccdcbdc6170e837c3bab`.
- MH-04 acceptance criteria: same ref, blob `a75f5c1849ad67cc380a0ba3552bf7f2c5ec82b6`.

These are source anchors from the preceding bounded revalidation, not a claim that every ref was freshly re-read while drafting this proposal. The finding is bounded: the inspected source set does not evidence the required trusted issuer/lifecycle. It does not prove that no such design exists anywhere else in the repository or outside it.

## 3. Goals and non-goals

### Goals

1. Define the trust boundary responsible for establishing the provenance of a principal and issuing or attesting to an authorization context.
2. Define context validity and lifecycle states, including expiry, revocation, freshness, and re-establishment after restart or identity changes.
3. Bind the context to the intended audience and permitted use, and define how the consuming boundary validates it.
4. Prevent context forgery, caller-controlled privilege escalation, confused-deputy behavior, cross-domain reuse, replay, stale authorization, and mismatched request/resource binding.
5. Establish source-backed governance, threat-to-requirement traceability, negative-path acceptance criteria, and a separate implementation authorization gate.

### Non-goals

- No code changes, runtime changes, test execution, qualification, deployment, migration, credentials, provider/model calls, or infrastructure changes.
- No adoption or freeze of a new P0-05 normative contract.
- No decision on D6, the normative status of the P0-05 contract text.
- No new mutation bridge, direct P0-04 caller, alternate state authority, persistence authority, or capability translation.
- No selection of identity/security technology or API signature.

## 4. Proposed responsibility model (for review)

The following is a conceptual responsibility split, not an accepted architecture decision:

1. **Authentication / identity authority:** establishes the authenticated principal from an approved authentication mechanism and provides source evidence for that assertion. It must not itself commit canonical product state.
2. **Trusted context issuer or attestation authority:** creates or attests to a bounded context only after validating identity, policy inputs, intended audience, and lifecycle state. The accountable authority and its trust roots remain undecided pending governance.
3. **P0-07 operation/policy boundary:** evaluates the requested operation and its capability under the approved policy. An ALLOW result is not a P0-04 transaction grant and cannot mint or broaden a P0-04 capability.
4. **P0-05 consumer boundary:** accepts only context whose trust and use constraints can be validated under the eventually accepted contract; rejects invalid or unverifiable context closed. P0-05 remains the only consumer boundary.
5. **P0-04 State Authority:** remains the sole authority for canonical state transactions and mutation. It independently validates the context and transaction constraints applicable to it; downstream layers cannot bypass its authorization.
6. **Audit/privacy governance:** defines minimal security-relevant evidence and retention/access policy without logging credentials or unnecessary sensitive payloads. MH-13 constraints apply.

Governance must decide whether issuance and validation are separate logical responsibilities or one governed authority with clearly separated operations. This proposal does not require a separate microservice or process.

## 5. Minimum context semantics to govern

Before an implementation contract can be drafted, governance and security review should decide the required semantics for each item below. Names and serialization are deliberately unspecified.

| Concern | Minimum question / requirement | Failure disposition |
|---|---|---|
| Principal provenance | What accepted evidence proves the principal was authenticated, and by which authority? | Deny if provenance cannot be validated. |
| Issuer trust | Which authority is permitted to issue or attest context, and how is that authority's trust established and rotated? | Deny unknown, untrusted, or misconfigured issuer. |
| Capability semantics | Which exact capability is granted, for which operation and scope, and who is authorized to grant it? | No implicit translation, self-grant, or broadening. |
| Audience / consumer | Which boundary or domain may consume the context? Is cross-domain reuse ever allowed? | Deny audience mismatch. |
| Expiry / freshness | What bounds validity, clock assumptions, freshness checks, and refresh/re-authentication? | Deny expired or unverifiably stale context. |
| Revocation | Who is authoritative for revocation, what is the consistency bound, and how is revocation checked at use time? | Fail closed when required revocation state is unavailable or indeterminate. |
| Replay resistance | What makes reuse detectable or invalid, and which operation/transaction scope is protected? | Deny detected or unverifiable replay where replay resistance is required. |
| Request binding | How are principal, operation, capability, resource, payload, audience, and canonical revision bound to the same authorized action? | Deny any mismatch; no partial commit. |
| Transaction lifecycle | How do begin/commit/abort use the same accepted authority and transaction context? | Abort on inconsistent or stale binding. |
| Restart / recovery | How is trust re-established after process restart, restore, key rotation, or identity-state change? | Do not silently trust cached context after its validity cannot be established. |
| Error handling | Which stable sanitized errors are observable without leaking secrets or protected data? | Fail closed and avoid sensitive diagnostic disclosure. |
| Audit / privacy | Which minimal events are recorded, by whom, for how long, and who may read them? | No credentials or unnecessary sensitive payload in logs. |

## 6. Candidate lifecycle for governance review

The following lifecycle is a proposal to be refined, not a normative state machine:

1. **UNAUTHENTICATED** — no trusted principal assertion is available.
2. **AUTHENTICATED** — an approved authentication mechanism has established a principal; this alone does not imply a capability.
3. **CONTEXT_ISSUED** — an authorized issuer has created/attested a bounded context from validated inputs.
4. **VALIDATED_FOR_USE** — the consuming boundary has validated issuer trust, principal, capability, audience, time/freshness, revocation status, and applicable request binding.
5. **CONSUMED / TRANSACTION_BOUND** — context is associated with the specific permitted operation and, where relevant, the P0-04 transaction/revision.
6. **EXPIRED / REVOKED / INVALID / REJECTED** — terminal for the relevant context instance; it must not be silently reused.
7. **REAUTHENTICATION / REISSUANCE REQUIRED** — a fresh authentication or newly issued context is required under the eventual contract.

Governance must determine whether single-use semantics are needed, how replay is detected, and whether a validated context can be reused for a bounded session. The proposal does not assume that a particular token format or distributed revocation mechanism is necessary.

## 7. Threat model and required negative cases

At minimum, the eventual design and acceptance plan must cover:

- caller supplies a fabricated or modified context;
- valid principal paired with a capability the issuer was not authorized to grant;
- untrusted or rotated issuer;
- context expired, revoked, stale, or with unverifiable status;
- audience/domain mismatch;
- replay of a previously consumed operation or transaction context;
- context for one resource, operation, payload, or revision reused for another;
- mismatch between P0-07 policy ALLOW and the P0-04 transaction authorization;
- context or trust state lost/changed across restart or recovery;
- revocation service/authority unavailable or indeterminate;
- audit/error output exposes credential material or protected payload;
- stale cache or concurrent update changes authorization-relevant state between decision and commit.

Expected invariant: any unhandled, ambiguous, mismatched, stale, or unverifiable trust condition denies the operation and prevents canonical mutation. The exact tests and evidence must be tied to a separately authorized implementation revision; this proposal does not execute tests or claim any test result.

## 8. Alternatives for the owner and security/governance reviewers

| Option | Description | Benefits | Costs / risks | Assessment |
|---|---|---|---|---|
| A. Reuse an already approved authority | Identify an existing accepted issuer/verifier and exact source evidence; use it only if it satisfies all required semantics. | Least new architecture; potentially smallest change. | Current inspected sources do not identify one; hidden assumptions remain unsafe without evidence. | Preferred if concrete accepted evidence is produced. |
| B. Govern a new explicit authority/lifecycle contract | Approve responsibility, context semantics, lifecycle, threat controls, and validation boundary before choosing technology. | Makes trust boundary and acceptance criteria explicit; supports independent review. | Requires governance and security review; may introduce a new design surface. | **Recommended current path**, because no accepted issuer/lifecycle is evidenced in the bounded source set. |
| C. Defer and retain the block | Make no new authority design decision; continue independent work only. | Avoids premature architecture. | P0-07 mutation/publication remains blocked; D1/D2/D3 remain unresolved. | Safe fallback if governance declines to proceed. |

Option B is the owner's selected path for proposal preparation only. It is not approval to implement a new authority.

## 9. Required decisions and evidence gates

Before this proposal can become an accepted contract:

1. **Authority ownership:** name the accountable governance owner and define the permitted issuer/attester and verifier responsibilities.
2. **Accepted identity/authentication source:** cite exact accepted artifacts and ref/commit/blob provenance.
3. **Context contract:** approve required semantic fields and validation rules without assuming a technology prematurely.
4. **Lifecycle and revocation:** define expiry, freshness, revocation authority/consistency, replay handling, key/trust rotation, and restart/recovery behavior.
5. **Authorization composition:** specify how P0-07 policy decision and P0-04 transaction authorization remain distinct and both necessary where required.
6. **Request/resource/revision binding:** show how the exact operation, principal, resource, payload, and canonical revision are bound across P0-07 → P0-05 → P0-04.
7. **Privacy/audit:** review minimal event evidence, retention, reader authorization, and sensitive-data handling against MH-13.
8. **P0-05 D6 separation:** resolve the discrepancy between implementation acceptance and DRAFT-labelled normative contract through a separate explicit governance record. Do not infer that this proposal resolves D6.
9. **Independent review:** security and architecture review against the threat cases in §7; record objections and dispositions.
10. **Acceptance/freeze:** explicit owner/governance acceptance against exact document blob and commit, with change control.
11. **Implementation authorization:** separate, explicit permission before any code changes.
12. **Verification and qualification:** independently planned and evidenced after implementation; proposal text alone cannot promote status.

## 10. Status and downstream gates

- D1 existing compliant caller path: **NOT DEMONSTRATED** in the inspected source lineage.
- D2 trusted issuer/context lifecycle: **NOT EVIDENCED** in the inspected source set; proposal prepared for review.
- D3 end-to-end request/context/resource/revision binding: **NOT EVIDENCED / DEPENDENT ON D1/D2**.
- D6 P0-05 normative-text status: **OPEN / GOVERNANCE CONFIRMATION REQUIRED**, independent of this proposal.
- P0-07 mutation/publication: **BLOCKED — GOVERNANCE/API GAP**.
- P0-05 v1.1: **NON-NORMATIVE / NOT ACCEPTED / NOT FROZEN**.
- Qualification: **NO-GO / NOT PROVEN**.

## 11. Change log and review record

- 2026-10-13: initial proposal prepared following the owner's selection of option B. Documentary-only. No implementation, tests, qualification, credentials, provider/model calls, host/runtime inspection, infrastructure changes, deployment, migration, merge, or rebase performed.
- Owner decision on this proposal: **PENDING**.
- Security review: **PENDING**.
- Architecture/governance acceptance and freeze: **PENDING**.
- Implementation authorization: **NOT GRANTED**.


## 12. Review-ready candidate architecture and decision worksheet (2026-10-13)

This section makes the proposal concrete enough for security/architecture review. It remains a candidate, non-normative design; it does not choose a technology or establish acceptance.

### 12.1 Recommended logical pattern for review

**Recommendation for governance review: one explicitly accountable trusted-context authority, with separately specified issuer/attester and verifier responsibilities, and independent transaction authorization at P0-04.** “One authority” means one accountable trust policy and lifecycle owner; it does not require one process, service, key, or deployment. Whether issuer and verifier are implemented separately remains a later decision.

The candidate trust chain is:

1. An approved authentication mechanism establishes a principal and produces verifiable provenance. Authentication alone grants no capability.
2. A governed issuer/attester evaluates whether that principal may receive the exact bounded capability for a defined audience, operation/scope and validity interval. The issuer must not infer permission from caller-provided fields.
3. P0-07 evaluates the requested operation under its policy and produces an operation-scoped decision. This decision is not itself a transaction grant and cannot mint, broaden, or replace the trusted context.
4. P0-05 validates the context's provenance and applicable use constraints at the consumer boundary. Unverifiable inputs are rejected closed.
5. P0-04 independently enforces the transaction and canonical-state constraints it owns. It must not rely solely on a P0-07 ALLOW result or on the fact that P0-05 forwarded a value.
6. Audit records capture the minimum security-relevant decision evidence. MH-13 privacy constraints govern data minimization, access and retention.

No step may bypass P0-05 or grant another component canonical mutation authority. If this chain cannot be proven end-to-end, mutation/publication remains blocked.

### 12.2 Proposed context lifecycle rules

The candidate lifecycle in §6 should be reviewed against these transition rules:

| Transition | Preconditions | Required evidence | Deny/stop condition |
|---|---|---|---|
| Unauthenticated → Authenticated | Approved authentication path succeeds | Principal provenance, authentication result and trust-boundary identity | Missing, ambiguous or untrusted provenance |
| Authenticated → Issued | Issuer is approved and policy permits the exact capability/scope | Issuer identity, principal, capability/scope, audience and validity constraints | Caller self-assertion, issuer not authorized to grant, or policy ambiguity |
| Issued → Validated for use | Consumer validates provenance and all required freshness/lifecycle checks | Validation result tied to the context instance and consumer boundary | Expiry, revocation, audience mismatch, invalid signature/integrity if applicable, unknown status or unavailable mandatory validation |
| Validated → Operation-bound | Context matches the exact operation and its resource/payload/revision constraints | Stable operation/transaction correlation and binding evidence | Any mismatch, reuse outside allowed scope, or stale canonical revision |
| Operation-bound → Committed | P0-04's own transaction preconditions and authorization pass | P0-04 transaction outcome and canonical revision evidence | Policy ALLOW without transaction authorization, concurrent revision conflict, or failed precondition |
| Any non-terminal state → Invalid/Expired/Revoked | Expiry, revocation, identity/credential change, trust-root rotation, or invalidation event | Invalidation cause and applicable timestamp/version | State cannot be determined where a positive check is required |
| Restart/recovery → Revalidated | Trust roots and lifecycle state are re-established from an approved source | Fresh validation evidence; no blind restoration of cached trust | Restored cache cannot prove freshness/revocation/current identity |

These are semantic gates, not a mandated serialized state machine. Governance must explicitly decide whether operation-bound contexts are single-use or reusable within a bounded session; until then, cross-operation reuse must not be presumed safe.

### 12.3 Required contract invariants

The review should either accept or explicitly revise each proposed invariant:

- **I-01 Provenance:** a consumer can verify who issued/attested the context and the authenticated principal to which it applies.
- **I-02 Least privilege:** capability and scope are explicit; no caller-controlled escalation or implicit capability translation.
- **I-03 Audience confinement:** context is valid only for its approved consumer/domain and use.
- **I-04 Time and lifecycle:** expiry/freshness/revocation semantics are explicit and enforceable; unknown mandatory status fails closed.
- **I-05 Operation binding:** principal, capability, audience, operation, resource, payload constraints and relevant canonical revision cannot be silently mixed across requests.
- **I-06 Two distinct decisions:** P0-07 policy permission and P0-04 transaction authorization remain distinct; one does not imply the other.
- **I-07 Single mutation authority:** only P0-04 commits canonical product state; the context authority issues/attests trust evidence but does not mutate state.
- **I-08 Recovery safety:** restart, restore, key rotation and identity change require revalidation when validity cannot otherwise be established.
- **I-09 Minimal audit:** decision provenance and outcomes are auditable without logging credentials or unnecessary sensitive payload.
- **I-10 Fail-closed ambiguity:** malformed, forged, stale, revoked, replayed, mis-scoped, unverifiable or conflicting inputs cannot authorize canonical mutation.

These are proposed review invariants, not accepted/frozen requirements. No new stable requirement IDs are allocated in this draft.

### 12.4 Architecture alternatives to resolve

| Candidate | Description | Advantages | Principal unresolved risk | Recommendation |
|---|---|---|---|---|
| A. Reuse an evidenced existing authority | Identify a currently accepted issuer/verifier and prove it satisfies §§5, 7 and 12.3 | Avoids duplicating authority | No such end-to-end path is evidenced by the bounded sources currently recorded | Reconsider only if exact accepted source evidence is produced |
| B1. One logical authority contract, explicit issuer and verifier responsibilities | Govern one accountable lifecycle and trust policy; implementation may be co-located or separated later | Clear ownership without prematurely requiring a service boundary | Needs owner/security decisions for ownership, revocation and trust roots | **Preferred candidate for review** |
| B2. Separate issuer and verifier authorities | Distinct accountable components with explicit trust relationship and lifecycle protocol | Separation can reduce single-component privilege | More key/trust distribution, rotation, revocation and failure modes to govern | Retain as alternative if threat analysis demonstrates a need |
| C. Defer design | Keep D2 open and P0-07 blocked | Avoids premature decision | No progress toward closing the authority/lifecycle gap | Safe fallback if governance declines B1/B2 |

B1 is a review recommendation only. It does not name the accountable project owner, select a technology, or authorize implementation.

### 12.5 Minimum review packet and exit criteria

A review cannot be marked complete merely because this document exists. Reviewers should return a disposition for each item:

1. Confirm or reject the logical responsibility pattern and identify accountable owner(s).
2. Cite the accepted authentication and identity sources, with exact ref/commit/blob.
3. Define the authority's trust root, authorization to issue, rotation and revocation ownership—or mark the decision explicitly unresolved.
4. Decide required context semantics and operation-binding boundary, including the role of P0-04's canonical revision.
5. Decide the revocation availability/consistency policy and fail-closed behavior.
6. Decide single-use versus bounded reuse and the anti-replay evidence required.
7. Review restart/recovery and trust-root rotation.
8. Complete joint MH-12 security and MH-13 privacy/audit review, including minimal logging, access and retention.
9. Record each objection, disposition, evidence and responsible approver.
10. Keep D6 as a separate P0-05 normative-text decision.
11. Accept/freeze only against an exact reviewed document blob and commit; implementation authorization remains a separate decision.
12. Define revision-bound verification/qualification evidence only after implementation is separately authorized.

### 12.6 Review result and status after this pass

- Deliverable status: **PROPOSAL REFINED FOR REVIEW / NOT ACCEPTED / NOT FROZEN**.
- Candidate recommendation: **B1 — one accountable logical authority contract with explicit issuer/verifier responsibilities**, subject to review and owner/governance decision.
- D1: **NOT DEMONSTRATED**. D2: **NOT EVIDENCED; candidate design prepared**. D3: **NOT EVIDENCED / DEPENDENT ON D1/D2**. D6: **OPEN / GOVERNANCE CONFIRMATION REQUIRED**.
- P0-07 mutation/publication remains **BLOCKED — GOVERNANCE/API GAP**; P0-05 v1.1 remains **NON-NORMATIVE / NOT ACCEPTED / NOT FROZEN**; qualification remains **NO-GO / NOT PROVEN**.
- No new stable IDs; no source contract edited; no implementation, tests, qualification, credentials, provider/model calls, host/runtime inspection, infrastructure change, deployment, migration, merge or rebase performed.
- Next bounded step: submit the refined proposal for independent MH-12/MH-13 and architecture review; record review comments and the explicit owner/governance disposition. Do not infer acceptance from this refinement.


### 12.7 Source-anchored MH-12 / MH-13 desk review (2026-10-13)

**Review type:** bounded internal source-consistency review only. This is not an independent review, domain-owner acceptance, or freeze.

**Live source anchors on `main`:** MH-12 identity `27eef9e23db02d6280b94a8e68bff9f73b0de88d`; authentication `a29c6a3cff0ee175a0c868214ffa2b455010002f`; authorization `c48641861691714017aa5b1f99fe8eee8ea0e76a`; MH-12 control point `dea79d709fea274cc5fd08cca4f0d6aec2ad6d93`; MH-13 privacy/data governance `e732ff9cacbc9c1189bd83306cdff30906326cf0`; MH-13 governance acceptance record `6ecdc89440664563f36263bb8da80d1ad24f19a7`; MH-13 reverse prompt `d590b6541870d3f77fbb1e48159b78d5d2f1f203`.

**Review items requiring explicit disposition before acceptance:**

- **R-01 — Canonical security-flow mapping.** MH-12's flow is Identity → Authentication → Trust → Capability → Authorization → Policy → Command/Proposal → Consumer Boundary → State Authority → Event → Audit/Observability. Map the proposed P0-07 decision and P0-04 transaction decision to this sequence without treating P0-07 ALLOW as either identity-bound authorization or P0-04 authorization.
- **R-02 — Principal/delegation scope.** MH-12 defines human, service, device, plugin, AI/model, workload, recovery, update/signing and audit principal classes. Reviewers must state which are in scope and what delegation is permitted; unspecified classes remain unsupported.
- **R-03 — Lifecycle failure semantics.** MH-12 requires issuance, binding, expiry, refresh, revocation, replay resistance, failed-auth handling, rate limits/quarantine and recovery. Revocation consistency/availability, trust-root rotation ownership and behavior during validation unavailability remain undecided.
- **R-04 — Privacy and audit minimization.** MH-13 §§2.3–2.9 require purpose limitation, minimization, retention/deletion governance, redaction of protected data from unauthorized channels and auditable evidence without unnecessary payload disclosure. Define minimal decision evidence, access and retention; do not log credentials, raw authorization material or unnecessary protected payload by default.
- **R-05 — MH-13 status boundary.** Its governance record accepts an authorized reconstruction, not a frozen architecture or production implementation. Preserve unknown taxonomy, retention and provider semantics; do not treat MH-13 as proof that D2 is accepted.
- **R-06 — Required audit unavailable.** MH-13 requires auditability but the inspected sources do not decide whether an operation must stop if required audit evidence cannot be emitted. Owner/security/privacy reviewers must decide per operation risk; no behavior is selected here.

**Desk-review disposition:** no source-backed reason to relax existing P0 authority boundaries was found in this bounded pass. This is not proof of completeness and is not the requested independent review. The proposal is ready for an independent reviewer to assess R-01…R-06. D1 remains NOT DEMONSTRATED; D2 NOT EVIDENCED / CANDIDATE DESIGN PREPARED; D3 NOT EVIDENCED / DEPENDENT ON D1/D2; D6 OPEN / GOVERNANCE CONFIRMATION REQUIRED. P0-07 mutation/publication remains BLOCKED — GOVERNANCE/API GAP; P0-05 v1.1 remains NON-NORMATIVE / NOT ACCEPTED / NOT FROZEN; qualification remains NO-GO / NOT PROVEN. No stable IDs or technology decisions were added; no implementation was authorized.


## 13. Independent reviewer response worksheet (template only, 2026-10-13)

**Status: BLANK TEMPLATE — NOT A REVIEW, NOT ACCEPTANCE, NOT IMPLEMENTATION AUTHORIZATION.** Use this section to capture a real independent review; do not mark it complete without a qualified reviewer and traceable evidence.

### Reviewer and independence
- Reviewer name/stable identifier and role/domain competence:
- Review date and proposal ref/blob SHA reviewed:
- Relationship to author/owner and conflicts of interest:
- Independence declaration:
- Exact source paths, refs, blob SHAs and sections reviewed:

### Required disposition vocabulary
For each R-item choose `ACCEPT`, `ACCEPT WITH CONDITIONS`, `REJECT`, or `UNRESOLVED`. Each disposition needs source anchors, rationale, severity where applicable, and required follow-up. Reviewer recommendations are not owner/governance decisions.

### R-01 — Canonical security-flow mapping
- Disposition and source-anchored reasoning:
- Map Identity → Authentication → Trust → Capability → Authorization → Policy → Command/Proposal → Consumer Boundary → State Authority → Event → Audit/Observability:
- Confirm P0-07 policy ALLOW is neither identity-bound authorization nor P0-04 transaction authorization:
- Findings / required changes:

### R-02 — Principal and delegation scope
- Disposition and source-anchored reasoning:
- Principal classes explicitly in/out of scope; delegation boundary; unsupported unspecified classes:
- Findings / required changes:

### R-03 — Lifecycle failure semantics
- Disposition and source-anchored reasoning:
- Issuance, binding, expiry, refresh, revocation, replay resistance, failed-auth handling, rate limits/quarantine and recovery:
- Revocation consistency/availability, trust-root rotation ownership, validation-unavailable behavior:
- Findings / required changes:

### R-04 — Privacy and audit controls
- Disposition and source-anchored reasoning:
- Data minimization, access control, retention, audit integrity and privacy review:
- Findings / required changes:

### R-05 — MH-13 governance/status boundary
- Disposition and source-anchored reasoning:
- Confirm reconstruction/proposal status is not mistaken for frozen, accepted or production-ready implementation:
- Findings / required changes:

### R-06 — Required audit unavailable
- Disposition and source-anchored reasoning:
- Operation-risk-specific behavior when required audit evidence cannot be emitted:
- Separate reviewer recommendation from owner/security/privacy decision:
- Findings / required changes:

### Cross-cutting review and recommendation
- P0-04 remains canonical mutation authority: findings:
- Any conflation of P0-07 ALLOW with identity/authentication or P0-04 authorization:
- Any unsupported selection of issuer/API/schema/cryptographic mechanism/deployment topology:
- Missing evidence, contradictions, threats, assumptions and severity:
- Overall recommendation: `READY FOR OWNER/GOVERNANCE REVIEW` / `REVISE AND RE-REVIEW` / `NOT READY` / `UNRESOLVED`:
- Conditions and rationale:

### Gate status and sign-off
- Independent review actually completed: YES / NO:
- R-01…R-06 all have evidence-backed dispositions: YES / NO:
- Owner/governance acceptance separately obtained: YES / NO / NOT IN SCOPE:
- D1 remains `NOT DEMONSTRATED`, D2 `NOT EVIDENCED`, D3/D4 `NOT EVIDENCED`, P0-05 v1.1 `NON-NORMATIVE / NOT ACCEPTED / NOT FROZEN` unless separate, traceable evidence and governed decisions justify a change:
- Reviewer sign-off, durable review record URL/path, follow-up owner, unresolved items:

**Guardrail:** This blank worksheet closes no gate. The existing internal desk review is not an independent review. Completing the worksheet records a review only when a real independent reviewer supplies the evidence and dispositions. It grants no implementation or qualification authorization.


### 13.1 Independent-review handoff — exact source anchors (2026-10-13)

This subsection is a reviewer handoff aid, not a completed review. The reviewer must independently inspect the proposal and cited source content, record actual dispositions in §13, and identify any additional sources required. The proposal reviewed is this exact blob at handoff preparation: `5e0ce7ba9f6ab4aa31f939189d49c6635c2457f1` on `docs/mediahub-chat-tree-map-20261012`; refresh it before review and record the actual blob/commit reviewed.

**Current `main` source anchors re-fetched for this handoff** (`main HEAD 1d45bbccbbbd27309c39cb9e9351bb291cdb47a8`):

| Review relevance | Primary source | Blob SHA | Required use / limit |
|---|---|---|---|
| Identity and principal classes | `docs/architecture/MH-12-identity.md` | `27eef9e23db02d6280b94a8e68bff9f73b0de88d` | Review principal identity/provenance; do not infer issuer authorization from identity alone. |
| Authentication | `docs/architecture/MH-12-authentication.md` | `a29c6a3cff0ee175a0c868214ffa2b455010002f` | Verify approved authentication path and evidence; authentication alone grants no capability. |
| Authorization | `docs/architecture/MH-12-authorization.md` | `c48641861691714017aa5b1f99fe8eee8ea0e76a` | Keep authorization distinct from policy decision and P0-04 transaction authorization. |
| Privacy/data governance | `docs/architecture/MH-13-privacy-data-governance.md` | `e732ff9cacbc9c1189bd83306cdff30906326cf0` | Reconstructed/proposed; apply minimization, purpose, access, retention and audit principles without claiming historical completeness. |
| MH-13 acceptance record | `docs/architecture/MH-13-governance-acceptance-record.md` | `6ecdc89440664563f36263bb8da80d1ad24f19a7` | Acceptance is limited to the authorized reconstruction; not a P0-07 review, freeze or production authorization. |
| MH-13 governance state | `docs/architecture/MH-13-governance-state.md` | `7bd2624c3072ecf0a08a430bb8b8214b3d55d3fa` | Confirms not frozen, historical fidelity partial/requires verification, production implementation not authorized, CI/build qualification not verified. |
| MH-13 architecture pointer | `docs/architecture/MH-13-architecture-reference.md` | `1b71d9ea4d4e0924f2814edee0a982f593d71847` | Navigation/status corroboration only; not a replacement for primary privacy contract. |

**Source-discovery boundary:** the current `main` recursive tree filename check did not find an MH-12 control-point path matching the previously cited shorthand. Do not cite a guessed filename. If the review depends on a separate control-point artifact, locate and fetch its exact path/blob before relying on it; otherwise record the dependency as unresolved. The MH-13 acceptance-record SHA in §12.7 matches the live fetch above.

**R-item review routing:**
- **R-01:** use MH-12 identity/authentication/authorization anchors and any separately verified security-flow source; distinguish authentication, trusted context, P0-07 policy ALLOW, and P0-04 transaction authorization.
- **R-02:** use identity and authorization anchors; explicitly list principal classes/delegation in and out of scope.
- **R-03:** use authentication/authorization plus relevant recovery, capability and security-boundary sources; unresolved revocation consistency, trust-root rotation, validation outage and replay policy must stay unresolved unless evidence/decision exists.
- **R-04:** use MH-13 privacy source; specify purpose, minimization, audit contents, access and retention without sensitive-payload assumptions.
- **R-05:** use all four MH-13 anchors; acceptance of the reconstruction is not historical recovery, freeze, P0-07 acceptance or implementation authorization.
- **R-06:** use MH-13 audit requirements but record operation-specific “audit unavailable” behavior as unresolved unless an authorized decision exists.

**Handoff guardrails:** this table does not constitute reviewer analysis or a disposition. The qualified reviewer must record identity, competence, independence/conflicts, exact proposal and source refs/SHAs, evidence-backed R-01…R-06 dispositions, cross-cutting findings, overall recommendation and unresolved issues in §13. Owner/governance acceptance remains separate. No gate status or implementation authorization changes by adding this handoff.


## 13.2 — Live-main MH-12 source anchors verified (2026-10-13)

This addendum supersedes only the source-discovery boundary in §13.1 that said no exact MH-12 control-point source had been located. A read-only query of the complete recursive tree at current main HEAD `1d45bbccbbbd27309c39cb9e9351bb291cdb47a8` found the following exact MH-12 source paths and blob SHAs:

| Review use | Exact source path on `main` | Blob SHA | What it supports / limitation |
|---|---|---|---|
| R-01, R-02 | `docs/architecture/MH-12-identity.md` | `27eef9e23db02d6280b94a8e68bff9f73b0de88d` | Canonical principal classes; identity lifecycle is distinct from authorization; unverifiable identity is not trusted. Does not define an accepted P0-07 issuer. |
| R-01, R-02, R-03 | `docs/architecture/MH-12-authorization.md` | `c48641861691714017aa5b1f99fe8eee8ea0e76a` | Operation-specific, identity-bound, context-aware, policy-aware, auditable, fail-closed authorization; forbids implicit grants/self-grant and alternate mutation authority. Does not evidence the proposed end-to-end context lifecycle as implemented or accepted. |
| R-01, R-03 | `docs/architecture/MH-12-security-boundaries.md` | `38a4505eef87f696748924baedd40cfa2ad07a41` | Boundary-crossing trust requirements and deny/quarantine/safe-degradation framing; does not settle each operation's audit-outage behavior. |
| R-03, R-04, R-06 | `docs/architecture/MH-12-audit.md` | `ab6e1c652790fd9088ac26b595050774611da2fc` | Security audit fields, integrity, access control, privacy-aware retention, bounded storage and controlled export. Does not select the required operation-specific response when audit is unavailable. |
| Review-status guardrail | `docs/architecture/MH-12-acceptance-criteria.md` | `40f37f1600c4730e622480d57bd492fa67f9ca4b` | MH-12 remains governance-review-required; implementation authorization, production qualification and freeze are not granted. This is a status guardrail, not a P0-07 D2 review. |
| R-03 unresolved assumptions | `docs/architecture/MH-12-unknowns.md` | `97f08824fb858dd4506876729ae37d610140c3e8` | Identity/authentication/capability/PKI/recovery and deployment unknowns remain REQUIRES VERIFICATION; no assumptions may fill them. |

The paths and SHAs above were freshly fetched from `main` during this pass. These source anchors improve reviewer routing only. They do not establish a qualified independent review, close R-01…R-06, approve a trusted issuer, select token/API/cryptographic design, grant implementation authority, or change any P0-07/P0-05/MH-22 gate. The §13 reviewer disposition worksheet remains for an actual independent reviewer.


## 13.3 — Live-main authorization-context call-chain trace (2026-10-14)

**Scope:** bounded static source inspection of the current main tree. This is additional internal source evidence for the proposal, not the qualified independent D2 review required by §13.

| Source | Current main blob SHA | Static observation | Limit |
|---|---|---|---|
| runtime/mediahub_runtime/authorization.py | 4d8df5d3c1c26f7f133a8093cd270635b085f4d5 | AuthorizationContext contains only principal and capability; AuthorizationPolicy matches the exact (principal, capability, operation) tuple and an empty grant set denies. | This seam contains no issuer provenance, audience, expiry, revocation or trusted-context validation. The finding is limited to this module. |
| runtime/mediahub_runtime/consumer_boundary.py | 98bf2da9cea85da2c82145b4baef417c20b9ae73 | ConsumerBoundary.request checks the operation string and that context is an AuthorizationContext; _require_operation checks request type/operation. Context is forwarded to the authority. | No issuer/lifecycle verification is evidenced in the inspected boundary. |
| runtime/mediahub_runtime/in_memory_state.py | 0fbc71369d19e09944ba67a60ccb9df802f30a4b | The authority checks context type then calls its configured AuthorizationPolicy.require for operations. | The inspected authorization seam validates configured grants, not how the context was issued. |
| runtime/mediahub_runtime/lifecycle_service.py | 0b9d3d888e988615f1ad8cd50b1bef22f2be011b | Lifecycle requests check the expected runtime.lifecycle.transition capability and forward the context through ConsumerBoundary. | Capability equality is not proof of principal authenticity or trusted issuance. |
| runtime/mediahub_runtime/coordination_service.py | a4b81f2cfb21980af952aff26fb6e31d33b79bf7 | Coordinates typed lifecycle requests; no context issuer is visible in the inspected call path. | No claim about every possible caller or external integration. |
| runtime/mediahub_runtime/astra_gateway.py | 10985e4ad8f682313d08e7492ecc1856a8bce20f | The gateway accepts an AstraTaskRequest with approval_state, and the inspected path classifies sensitive actions before execution. This request type is separate from AuthorizationContext. | No verified call edge from this gateway path to the P0-05 ConsumerBoundary was found in the inspected files. Do not conflate the two paths or infer that gateway approval proves P0-07 trust. |
| runtime/mediahub_runtime/task_ingress.py | 59e1254aa61cc8f55f53bd1e179631e81c441393 | File ingress converts a task-contract file into AstraTaskRequest; context refs are data fields. | No accepted trusted-context issuer/lifecycle is evidenced by this inspected ingress. |
| runtime/mediahub_runtime/astra_service.py | 6aa2d09fc8737ccc0ba7f05bd13a15a0ebde7129 | Service module is 22 lines and contains no matching issuer/context/authorization symbols in the inspected content. | This is a narrow file-level observation only. |

**Bounded finding:** the inspected current-main path confirms the proposal's existing gap: the typed authorization context and downstream grant check are present, but an accepted trusted issuer and end-to-end issuance/expiry/revocation/restart lifecycle are not evidenced in these inspected call-chain files. The current tree filename inventory also did not expose a dedicated runtime/mediahub_runtime trusted-context issuer module; this does not prove that no relevant implementation exists elsewhere in the repository or outside it.

**Disposition unchanged:** D2 remains NOT EVIDENCED; proposal remains NOT ACCEPTED / NOT FROZEN; D1 is not demonstrated; implementation and mutation/publication remain blocked. This is not a confirmed vulnerability report, does not authorize implementation, and does not replace qualified independent review of R-01…R-06 or owner/governance disposition. No tests were run.
