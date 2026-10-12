# P0-05 Consumer Contract v1.1 — Candidate for Governance Review

- Date: 2026-10-12
- Candidate status: **NON-NORMATIVE / OWNER + SECURITY + GOVERNANCE REVIEW REQUIRED / NOT ACCEPTED / NOT FROZEN**
- Supersedes: nothing. This candidate does not replace or edit the existing P0-05 DRAFT or the accepted implementation.
- Purpose: make the P0-07 → P0-05 mutation authorization gap reviewable after option A was not found as an implemented end-to-end path in the inspected P0-07 tree.
- Owner direction: option A first; conditional option C if A does not work. The source-bound tree audit found no implemented P0-07 caller/adapter in the inspected tree, so C is now the next governance review path.

## 1. Provenance and status discrepancy — must be decided before adoption

Primary artifacts:
- P0-05 contract at the exact tree of implementation commit `303a766257b90c4356dcffc8967a5574e8e22e7a`, tree `82da63f03da20049954fe69257342cbf66b58395`, path `docs/architecture/P0-05-consumer-contract.md`, blob `bba8dd3e8812767b6dbc8afff1bec5bd36dc828b`: its header says `DRAFT — GOVERNANCE REVIEW REQUIRED`.
- P0-05 governance acceptance record, blob `a0d28b4cfd9bed27e8a80968f6beac6cfdd97242`, records `ACCEPTED / FROZEN` for the reviewed implementation at commit `303a766257b90c4356dcffc8967a5574e8e22e7a`.

These facts establish implementation acceptance and a contract-status discrepancy; they do **not** establish that the DRAFT contract text itself was accepted. Governance must explicitly decide whether (a) the acceptance record accepted the contract text as well and the contract header is stale, or (b) only the implementation was accepted and the contract requires formal acceptance. Do not edit the source document/header or infer a disposition before that decision.

## 2. Unchanged invariants

The candidate must preserve:
1. P0-04 is the sole canonical mutation and transaction authority.
2. P0-05 is the sole consumer/integration boundary.
3. P0-07 owns domain configuration/policy validation, policy evaluation, and domain authorization only.
4. P0-07 ALLOW and policy ALLOW do not replace independently required P0-04 authorization.
5. P0-07 must not call P0-04 directly, mint/translate/self-grant capabilities, alter an authorization context, or create another transaction/version authority.
6. Denials, stale generations, malformed requests, validation failures and commit failures fail closed; canonical state is preserved on rejection.
7. No persistence, external execution, network or filesystem capability is implied.
8. No production qualification or implementation authorization is granted by this candidate.

## 3. Candidate normative additions (proposal text only)

The following clauses are proposed for owner/security/governance review. They are not in force unless adopted in an exact, governance-accepted revision.

### 3.1 Domain-operation hand-off

A domain consumer that requests canonical mutation MUST submit its bounded, validated operation through P0-05. P0-07's authorization decision and policy decision MUST be supplied as inert, auditable decision inputs and MUST be bound to the exact domain operation, resource identity, canonical candidate payload, principal and request correlation identity. They MUST NOT be executable capabilities.

### 3.2 Independent State Authority authorization

The mutation request MUST carry or obtain, through a governance-approved mechanism, an independently authorized P0-04 transaction context for the exact P0-04 lifecycle operation. P0-07 MUST NOT construct, modify, translate or self-grant that context. P0-04 remains responsible for deciding whether the context authorizes `begin`, `commit` and/or `abort`.

### 3.3 Binding and fail-closed semantics

P0-05 MUST reject the request if either domain authorization/policy evaluation or P0-04 authorization is missing or denied; if the principal, operation, resource, payload, transaction, generation or revision binding is inconsistent; or if the request is stale, malformed or replayed outside an explicitly approved idempotency contract. A decision for one payload or resource MUST NOT authorize a different payload or resource.

### 3.4 Transaction integrity

The complete canonical candidate MUST be validated within the P0-04 transaction boundary. Publication MUST occur only through P0-05 commit mediated by P0-04. A failed or rejected transaction MUST preserve canonical state. This proposal does not authorize LWW, implicit retry/rebase, patch/merge, a second version authority or persistence.

### 3.5 Audit and privacy

The boundary MUST emit bounded provenance sufficient to correlate the P0-07 decision, P0-05 request and P0-04 transaction outcome without exposing secrets, sensitive payloads, authorization internals or unnecessary personal data. Exact schema, retention, access control and failure behavior require MH-06/MH-12/MH-13 governance review.

### 3.6 Error contract

Consumer-visible failures MUST remain stable, minimal and sanitized. Internal diagnostics MUST NOT become a source of mutation authority or leak credentials, sensitive state, filesystem paths, network details or authorization material.

## 4. Unresolved design choices — owner/governance must decide

This candidate deliberately does not prescribe an API signature. Before normative adoption, decide and record:

- **D1 — Authorization composition:** Is the accepted pattern (a) two independent decisions passed as inert evidence plus an already-authorized P0-04 context, or (b) a P0-05-owned orchestration that obtains each decision through approved interfaces? No capability translation is allowed in either case.
- **D2 — Context delivery:** Is the P0-04 context supplied by a trusted caller or acquired by a separately governed authority component? Identify the authority, lifecycle, principal binding and trust boundary.
- **D3 — P0-07 decision evidence:** What immutable representation binds the decision to operation/resource/payload, and how is freshness/replay handled?
- **D4 — Operation mapping:** Which exact P0-07 domain operations can be submitted to P0-05, and which canonical state shape is replaced? No mapping is assumed here.
- **D5 — Audit/privacy:** Approve provenance fields, redaction, access and retention through MH-06/MH-12/MH-13.
- **D6 — P0-05 status reconciliation:** Resolve whether the current governance acceptance record includes acceptance of the DRAFT contract text, and record the exact accepted blob/commit.
- **D7 — Change control:** Confirm whether this candidate is to become P0-05 v1.1 or whether a separately named domain-operation contract should be governed under P0-05. No decision is preselected.

## 5. Acceptance and implementation gates

No implementation may begin from this candidate until all are satisfied:
1. Product owner resolves D1–D7 or explicitly delegates the decisions to named governance owners.
2. Security review validates dual-authorization composition, principal binding, payload binding, replay/staleness handling and fail-closed behavior.
3. Governance resolves the DRAFT-vs-acceptance-record discrepancy.
4. The exact normative candidate is stored under a versioned path, reviewed, explicitly accepted and frozen with exact blob and commit references.
5. Requirement → threat → contract clause → negative-path test → evidence traceability is updated.
6. A separate explicit implementation authorization is recorded.
7. Any subsequent qualification is separately authorized and tied to the exact implementation SHA. This document does not authorize or claim any tests or qualification.

## 6. Current disposition

- Option A: not available as an implemented end-to-end path in the inspected P0-07 tree; this conclusion is bounded to that tree.
- Option C: next governance review path, proposal only.
- P0-05 implementation acceptance remains historically recorded; exact normative contract acceptance remains unresolved.
- P0-07 mutation publication remains **BLOCKED — GOVERNANCE/API GAP**.
- Production qualification: **NOT GRANTED**.
- No implementation, test, workflow, deployment, persistence, infrastructure change or branch integration is authorized by this document.
