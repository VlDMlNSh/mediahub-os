# MediaHub OS — P0-07 → P0-05 and A0 Ingress Requirement / Decision / Evidence Ledger, Wave 46

- Date: 2026-10-17
- Working ref: docs/mediahub-chat-tree-map-20261012
- Status: **SOURCE-BOUND CONTROL LEDGER / PROPOSED / NOT NORMATIVE / NOT IMPLEMENTED / NOT QUALIFIED**
- Scope: Jarvis → ASTRA A0 engineering ingress (Route A) and P0-07 → P0-05 → P0-04 product-state mutation (Route B), with trusted-context lifecycle shared across both routes.
- Evidence boundary: current documentation-ref reads and GitHub metadata only. No tests, qualification, provider/model calls, credential access, host/runtime inspection, installation, infrastructure change, deployment or branch integration.

## 1. Source state and control rules

Existing source artifacts already include a proposed A0 ingress contract (WB-14AA), an A0 source-contract census (WB-14Z), a repository-wide unified traceability matrix, a Contour A requirement/component/control/evidence matrix, and the P0-05 existing-context compatibility proposal. This ledger links those artifacts and isolates closure criteria; it does not replace them.

Live comparison before this pass:
- main: 6c2e8dbdee81c798b64e65546e7ded07093f100a
- documentation-ref HEAD: 470a73cecada95e115778b33da8a70d67edaeb47
- status: **DIVERGED**, ahead 2016 / behind 14
- merge base: f0f406feb9f9816b009f4e6e756813541e53b9bc

No branch integration is part of this pass. Baseline 2.0 remains the canonical functional baseline; Baseline 1.0 remains historical provenance. Contour B product work remains gated on Contour A deployment and independent acceptance.

## 2. Status vocabulary

- **OWNER-APPROVED** — explicit owner decision recorded; this does not prove implementation.
- **SOURCE-OBSERVED** — a source artifact establishes the stated local behavior or wording at its pinned ref/SHA.
- **PROPOSED** — candidate language exists; governance acceptance and freeze are outstanding.
- **OPEN** — required contract, ownership, or evidence is absent from the inspected sources.
- **BLOCKED** — downstream implementation/promotion must wait for an upstream contract or decision.
- **NOT QUALIFIED** — independent qualification evidence is absent from this documentary pass.

A source link or commit/blob SHA establishes provenance, rather than runtime truth or acceptance. Evidence must be bound to the exact revision under review.

## 3. Requirement / decision / evidence ledger

| ID | Route / domain | Requirement or decision | Canonical source anchor | Evidence owner / accountable boundary | Closure evidence / acceptance artifact | Current status |
|---|---|---|---|---|---|---|
| AUTH-01 | Cross-route | Jarvis coordinates corporation missions; ASTRA A0 owns ASTRA-internal engineering lifecycle; Product State Authority alone mutates canonical product state. | Owner decision record, blob 70376a2709e055972ceddc4a280d26992977213c; Wave 45 report, blob 7031d82910b6e5ce8b910aef2463e4405cd05d4f. | Architecture/documentation owner; Product State Authority for mutation boundary. | Controlled reconciliation of broader ASTRA source wording; accepted authority crosswalk and exact source revision. | OWNER-APPROVED split; source reconciliation OPEN |
| A0-01 | Route A | An accepted Jarvis→A0 mission producer/consumer contract must exist before a service adapter is canonical. | WB-14Z census, blob 95f3af63705f4ad7cd24405df9c7c396886cb3a3; WB-14AA candidate, blob 030273bfe9fd6d44e78b611c011af95d08c88a45. | Jarvis mission coordinator and ASTRA A0 ingress authority. | Governance-accepted, versioned contract with caller/receiver identity, admission and result semantics. | PROPOSED / OPEN |
| A0-02 | Route A | Submit, status, result, cancellation, health challenge and uncertain-submit reconciliation require stable semantics. | WB-14AA candidate, blob 030273bfe9fd6d44e78b611c011af95d08c88a45. | ASTRA A0 owns admitted-work lifecycle; Jarvis consumes status/results through an interface. | Accepted operation/state model; idempotent admission and cancellation-race criteria; stable error taxonomy. | PROPOSED / OPEN |
| A0-03 | Route A | Immutable mission intent must bind request identity/digest, target revision, caller, receiver, policy/contract revision and evidence. | WB-14AA candidate; WB-14Z source census. | Jarvis produces request identity; A0 verifies and records admission. | Versioned envelope schema, canonical digest rules, target-SHA binding and durable correlation/evidence record. | PROPOSED / OPEN |
| SEC-01 | Cross-route | Caller identity, issuer/attester provenance, audience, operation/resource/scope, lifetime, freshness, revocation and replay controls require an explicit trust lifecycle. | WB-04 blob dac5e9eab9ec69ab7d15ac8eea45d7a1c8922387; WB-05 blob 1b562c6546b1216f2ee89095cd6a78427a967dc5; WB-06 blob 9bd850e869dbd19db9bde2ce08768aaf502c95a2. | Issuer/attester and verifier governance owners remain to be assigned. | Explicit issuer/attester decision; verifier boundary; trust-anchor/key rotation/revocation procedure; negative-case criteria. | OPEN / BLOCKED |
| SEC-02 | Cross-route | No caller self-grant, capability expansion, implicit translation or authority bypass; authorization failure is fail-closed. | Contour A requirement/control/evidence matrix, blob aa9183c66f13e0931cfc1883960d7c8e09da8c76; P0-05 proposal, blob fce7019b3430a95d12f723a769d39e1cd29067af. | Each receiving authority independently verifies permissions in its own trust domain. | Accepted policy composition and negative-path evidence tied to exact contract/code revision. | REQUIRED INVARIANT / QUALIFICATION OPEN |
| B-01 | Route B | P0-07 domain-operation ALLOW is distinct from P0-04 transaction authorization; P0-05 remains the consumer boundary. | P0-05 proposal, blob fce7019b3430a95d12f723a769d39e1cd29067af; Wave 45 report. | P0-07 domain policy; P0-05 consumer boundary; P0-04/Product State Authority transaction authority. | Source-proven caller context hand-off or governance-approved revision with operation/resource/payload/principal/transaction binding. | BLOCKED / GOVERNANCE REVIEW REQUIRED |
| B-02 | Route B | P0-05 normative artifact and acceptance status must be unambiguous before contract revision or mutation-bridge implementation. | P0-05 proposal §§4–7, blob fce7019b3430a95d12f723a769d39e1cd29067af. | Product owner and security/governance reviewers. | Exact accepted artifact/ref/blob; recorded D6 disposition; explicit acceptance/freeze record if revision is selected. | OPEN / OWNER-GOVERNANCE ROUTE |
| SEC-03 | Cross-route | In-process AuthorizationContext(principal, capability) and tuple-grant checks alone do not establish trusted cross-domain issuance. | WB-06 blob 9bd850e869dbd19db9bde2ce08768aaf502c95a2; WB-07 blob 89fab594f9a9ae9a729d63ecb14dad2543edc9af. | Issuer/attester, transport verifier and receiving authority, after governance assignment. | End-to-end source/contract trace from issuer to verifier to consumer; authenticated transport and context binding; negative cases. | LOCAL SEAMS SOURCE-OBSERVED / END-TO-END OPEN |
| LIFE-01 | Route A | ASTRA A0 remains sole writer for internal queue/claim/lease/heartbeat/retry/cancel/recovery and ASTRA evidence/gate transitions. | WB-14Z blob 95f3af63705f4ad7cd24405df9c7c396886cb3a3; WB-14AA blob 030273bfe9fd6d44e78b611c011af95d08c88a45. | ASTRA A0 internal workflow authority. | Accepted ingress and internal lifecycle contract; fencing/stale-worker/retry/recovery/cancellation semantics; independent evidence. | OWNER-APPROVED BOUNDARY / EXTERNAL CONTRACT OPEN |
| LIFE-02 | Cross-route | Admission, execution, verification, qualification, release, deployment and acceptance are distinct states. | WB-14AA invariant R-04; unified traceability matrix, blob a496f221f2dd5a8816f725f41504c64ad7a70476. | Authorized actor for each transition and independent evidence owner. | Versioned lifecycle/state model; immutable evidence per transition; acceptance gate map. | REQUIRED / MATRIX OPEN |
| AUD-01 | Cross-route | Audit correlates request, principal, target/revision, policy/contract revision, disposition and result while protecting sensitive data. | WB-14AA invariant R-06; unified traceability matrix Wave 01. | Producing authority owns event correctness; security/privacy governance owns policy. | Accepted audit schema, privacy/retention rules, correlation/redaction criteria and review evidence. | PROPOSED / R-06 ALIGNMENT OPEN |
| GOV-01 | Cross-route | Each requirement maps to a decision, source SHA, accountable owner, evidence artifact and acceptance gate. | Unified contract/traceability matrix, blob a496f221f2dd5a8816f725f41504c64ad7a70476; Contour A requirement/control matrix, blob aa9183c66f13e0931cfc1883960d7c8e09da8c76. | Architecture control owner; named evidence owners per requirement remain to be confirmed. | Ledger reviewed against primary sources and linked to accepted contracts/decisions. | CONTROL ARTIFACT PROPOSED |
| QUAL-01 | All | Documentary artifacts alone cannot establish implementation, deployment, qualification or Contour B promotion. | Master Roadmap 1.0; Wave 44 report; Wave 45 checkpoint. | Independent qualification authority and project governance. | Authorized target manifest, revision-bound test/verification evidence, independent disposition and acceptance record. | NO-GO / NOT PROVEN |

## 4. Route separation

### Route A — Jarvis → ASTRA A0 engineering ingress

This route submits bounded engineering missions to A0's own workflow authority. It grants no Product State Authority and must not write A0 internal state outside A0's accepted ingress. WB-14AA is the best current transport-neutral contract candidate, but remains proposed and unfrozen.

### Route B — P0-07 → P0-05 → P0-04 product-state mutation

This route remains a separate product authorization and transaction contract. P0-07 policy ALLOW is insufficient on its own. P0-04 remains canonical transaction authority; P0-05 remains the consumer boundary. Any revision requires existing-context evidence or a recorded governance disposition, with no implicit privilege translation.

Shared identity and audit concepts may be cross-referenced, while issuer decisions, capabilities, payload semantics and state ownership remain typed and domain-bound.

## 5. Minimum closure gates

1. **Contract lineage:** identify accepted/frozen artifacts and exact ref/blob SHA; keep proposals distinct from normative sources.
2. **A0 ingress:** review WB-14AA against current primary A0 internal policy and record each clause as accepted, changed or unresolved.
3. **Trust lifecycle:** route issuer/attester, verifier and trust-anchor decisions through existing governance. No product or token profile is selected by implication.
4. **Route B:** resolve P0-05 artifact/D6 status and source-prove the existing-context hand-off or obtain explicit governance disposition for a revision.
5. **Security semantics:** specify principal/resource/operation/payload/request binding, expiry/freshness, replay/idempotency, revocation, fencing, cancellation and fail-closed behavior.
6. **Evidence and privacy:** define audit correlation, provenance, redaction/retention, error taxonomy and immutable evidence binding.
7. **Acceptance:** attach negative-case criteria and independent review/qualification gates to exact candidate revisions; keep deployment and Contour B gates closed until authorized.

## 6. Next bounded work

Use this ledger as the control index. The next source pass should review WB-14AA clause-by-clause against current ASTRA primary sources and the accepted owner decision, then issue a delta table containing only clause-level dispositions and source evidence. Avoid creating a second competing ingress specification. Keep Route B and D6 on their separate governance path.

## References

- [Canonical project map](../architecture/MEDIAHUB-CHAT-TREE-MAP.md)
- [Wave 45 trusted-context reconciliation](MEDIAHUB-P0-07-P0-05-TRUSTED-CONTEXT-AND-LIFECYCLE-RECONCILIATION-WAVE-45-2026-10-17.md)
- [WB-14AA A0 ingress contract candidate](MEDIAHUB-CONTOUR-A-WB-14AA-ASTRA-A0-INGRESS-CONTRACT-CANDIDATE-2026-10-16.md)
- [WB-14Z A0 ingress source-contract census](MEDIAHUB-CONTOUR-A-WB-14Z-A0-INGRESS-SOURCE-CONTRACT-CENSUS-2026-10-16.md)
- [Unified contract and traceability matrix, Wave 01](MEDIAHUB-UNIFIED-CONTRACT-AND-TRACEABILITY-MATRIX-WAVE-01-2026-10-16.md)
- [Contour A requirement/component/interface/control/evidence matrix](MEDIAHUB-CONTOUR-A-REQUIREMENT-COMPONENT-INTERFACE-CONTROL-EVIDENCE-MATRIX-WAVE-01-2026-10-15.md)
- [P0-05 existing-context compatibility proposal](p0-05-contract-revision-proposal-p0-07-existing-context-2026-10-12.md)
- [Owner decision record / DEC-DEV-02](MEDIAHUB-CHAT-TO-GITHUB-OWNER-DECISIONS-AND-CORPORATION-DIRECTION-WAVE-01-2026-10-15.md)
