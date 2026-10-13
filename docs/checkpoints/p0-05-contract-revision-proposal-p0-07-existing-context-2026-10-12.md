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
