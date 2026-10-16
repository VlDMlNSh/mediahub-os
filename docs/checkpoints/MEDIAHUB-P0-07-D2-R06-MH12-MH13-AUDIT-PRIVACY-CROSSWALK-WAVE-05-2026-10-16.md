# P0-07 D2 R-06 — MH-12 Security Audit × MH-13 Privacy Crosswalk, Wave 05

- Date: 2026-10-16
- Ref: `docs/mediahub-chat-tree-map-20261012`
- Status: **SOURCE-ONLY RECONCILIATION / TECHNICAL RECOMMENDATION / PROPOSED / NOT ACCEPTED / NOT FROZEN**
- Scope: check Wave 04's proposed audit-event content and lifecycle against the available MH-12 audit requirement and MH-13 privacy/data-governance reconstruction. This pass is documentary only.

## 1. Result

Wave 04's minimal audit-intent/decision proposal is directionally compatible with the reviewed MH-12 and MH-13 source text, provided the event contract treats audit metadata itself as potentially sensitive and keeps retention, access, clock, durability and deletion semantics governed separately.

The sources establish audit controls as requirements. They do not establish an accepted runtime audit sink, a registered event schema, durable-emission guarantees, an approved clock, retention durations, or operation-specific outage behavior. Those remain open acceptance/governance gates.

**Recommended technical direction:** keep a transport-neutral logical event contract with an explicit allowlist of minimal fields; classify each field before persistence; prohibit payload capture by default; use bounded reason/result codes and opaque references; apply integrity protection, least-privilege read access, governed retention/deletion and controlled export. Keep the event contract independent from the sink implementation so the sink can be admitted and qualified separately.

## 2. Exact source pins reviewed

| Source | Ref / blob SHA | Source-backed boundary |
|---|---|---|
| MH-12 Audit | `main` / `ab6e1c652790fd9088ac26b595050774611da2fc` | Audit is distinct from ordinary logging. Security audit records who/when/requested operation/capability-context/authorization and policy decision/result/security context. Integrity protection, access control, privacy-aware retention, bounded storage and controlled export are required. Audit is not State Authority. |
| MH-13 Privacy / Data Governance | `main` and documentation branch / `e732ff9cacbc9c1189bd83306cdff30906326cf0` | Minimization, purpose limitation, retention/deletion governance, redaction, protected-channel restrictions and privacy-aware auditability. Exact historical taxonomy and retention periods remain unknown. |
| MH-13 Governance State | `main` and documentation branch / `7bd2624c3072ecf0a08a430bb8b8214b3d55d3fa` | The reconstruction is accepted as a reconstruction; historical original remains unrecovered; frozen = NO; production implementation is unauthorized; CI/build qualification is unverified. |
| MH-13 Reconstruction Registers | `main` and documentation branch / `8c66fb49bbe011d8ef5dd78287c72efdad77a8fe` | Independent-verification acceptance gate remains visible; P0 contracts remain unchanged; exact taxonomy, retention/deletion, residency and legal mapping remain unknown. |
| Wave 04 recommendation | `docs/mediahub-chat-tree-map-20261012` / `15f56b238151782e4ffd02b18b094da1f96321a0` | Proposed seven-operation audit matrix and conjunctive authorization model; no normative acceptance or implementation authorization. |
| Wave 01 MH-13 crosswalk | `docs/mediahub-chat-tree-map-20261012` / `1ebe0f06bf4a3105c6520a76fa516200ab0818f7` | R-04 privacy/audit minimization and R-05 status boundary source-confirmed; R-06 remains unresolved by the reviewed sources. |

## 3. Field-level privacy disposition

| Logical field | Recommendation | Privacy/security handling |
|---|---|---|
| Schema version, event ID, correlation ID | Keep | Opaque identifiers only; define uniqueness and collision handling in the schema contract. |
| Event timestamp | Keep as a required logical field; clock source remains open | Bind clock source, skew and monotonic-order assumptions to an accepted contract. Avoid claiming trustworthy time until evidenced. |
| Domain and operation | Keep | Enumerated values only: configuration/policy and the seven source-identified operations. |
| Principal reference | Keep only as an opaque, privacy-reviewed reference | Treat as potentially personal data; exclude credentials, raw claims, tokens and unnecessary identity attributes. |
| Capability and policy decision | Keep in bounded form | Record exact capability identifier and ALLOW/DENY result; omit raw authorization context and internal policy payload. |
| Target reference and revision | Keep only where required to explain scope and outcome | Use opaque target references and bounded revision identifiers; assess metadata sensitivity. |
| Mutation expected generation/version | Keep for mutation intent where the accepted transaction contract defines it | Do not invent a version field or guarantee that a cross-system atomic commit exists. |
| Phase and result | Keep as enumerated values | Use decision/intent/outcome/reconciliation and bounded result classes; represent unresolved post-commit state as `outcome_unknown`. |
| Reason code | Keep from a bounded registry | Avoid arbitrary strings, stack traces, user text or payload-derived explanations. |
| Policy/schema revision | Keep where required for reproducibility | Record identifiers only, without embedding policy/configuration contents. |
| Raw configuration/policy, proposal or validation payload | Exclude by default | No secrets, full documents, submitted values, returned values or replacement/default payloads in audit records. |
| Retention, export and reader identity | Required governance metadata, exact representation pending | Apply least privilege, integrity controls, bounded storage, privacy-aware retention/deletion and controlled export. Exact durations and legal basis remain open. |

This is a logical allowlist recommendation, not a registered schema or proof of an implemented sink.

## 4. Operation and outage reconciliation

The seven P0-07 operations remain `read`, `validate`, `propose`, `update`, `replace`, `reset`, and `delete`.

- For successful reads, validation responses and proposals, required pre-action decision evidence should be durably accepted before protected results are returned.
- For mutations, durable intent evidence should precede publication; the operation should remain blocked when that precondition fails.
- A denial remains a denial when the audit service is unavailable. Return a bounded sanitized response; never grant access as an audit-outage fallback.
- If a mutation commits but its outcome event cannot be written, preserve the prior durable intent as unresolved and reconcile against authoritative state. Do not describe the commit as rolled back.
- Do not claim atomic coupling between the audit sink and P0-04 without a separately accepted transaction/outbox contract.
- These behaviors remain **PROPOSED**, pending the applicable governance/contract gate. The reviewed source text does not authorize implementation or settle the owner-reserved outage policy.

## 5. Status conflicts and unresolved gates

1. MH-13's architecture/reconstruction text says `Acceptance: NOT YET VERIFIED`, while the separate governance-state record says `ACCEPTED RECONSTRUCTION`. Preserve both dimensions: governance accepts the reconstruction artifact as a reconstruction; independent verification, freeze and production implementation remain separate.
2. MH-12 audit requirements and MH-13 privacy principles are source-confirmed; runtime conformance is unproven.
3. Audit sink identity, durability/availability, event schema registration, approved clock, retention/deletion, authorized readers, integrity mechanism and controlled-export interface remain open.
4. R-06 outage disposition remains operation-scoped and subject to formal governance. This pass recommends fail-closed behavior for protected results/publication when required pre-action evidence is unavailable; it does not claim that the recommendation has been accepted.
5. P0-07 → P0-05/P0-04 authorization composition remains **BLOCKED — GOVERNANCE/API GAP**. The audit proposal creates no authority and no alternate mutation route.
6. D1: NOT DEMONSTRATED. D2: NOT EVIDENCED / NOT ACCEPTED / NOT FROZEN. D3: NOT EVIDENCED. D6: OPEN. Qualification: NO-GO / NOT PROVEN.

## 6. Work performed and next step

- Read the source-pinned MH-12 audit requirement, MH-13 privacy reconstruction, MH-13 governance state/registers, Wave 01 crosswalk and Wave 04 recommendation by exact blob SHA.
- No code, normative contract, schema registry, tests, qualification, provider/model call, credentials, runtime/host inspection, infrastructure, deployment, migration or branch integration.
- Next: update the canonical P0-07 D2 decision packet with this field-level privacy disposition only after its owner/governance acceptance path is identified; meanwhile preserve this report as non-normative evidence and continue checking the existing governance records for an explicit acceptance path.

Project map: [MEDIAHUB-CHAT-TREE-MAP.md](../architecture/MEDIAHUB-CHAT-TREE-MAP.md).
