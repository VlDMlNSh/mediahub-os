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
