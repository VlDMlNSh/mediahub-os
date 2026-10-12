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
