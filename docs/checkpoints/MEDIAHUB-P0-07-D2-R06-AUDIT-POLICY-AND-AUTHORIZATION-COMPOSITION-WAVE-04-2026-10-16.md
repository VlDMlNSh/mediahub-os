# P0-07 R-06 — Recommended Audit Policy and Mutation Authorization Composition, Wave 04

- Date: 2026-10-16
- Status: **TECHNICAL RECOMMENDATION / PROPOSED / NOT ACCEPTED / NOT FROZEN**
- Scope: source-backed target design for the seven P0-07 v1 domain operations, audit-unavailable behavior, and the P0-07 → P0-05 → P0-04 authorization boundary.
- This report selects a recommended engineering direction under the delegated technical-decision rule. It does not grant governance acceptance, amend a normative contract, or authorize implementation beyond the exact existing scope.

## 1. Result and recommendation

**Recommended target:** operation-scoped, minimal security audit evidence for every P0-07 operation, with fail-closed behavior when required pre-action evidence cannot be durably accepted; mutations remain subject to a separate, conjunctive authorization composition at the P0-05 boundary. Do not translate P0-07 capabilities into P0-04 transaction capabilities and do not let P0-07 invoke P0-04 directly.

The recommendation has two parts:

1. **R-06 audit policy:** require a minimal durable audit-intent/decision record for every operation attempt, including denials. For `read`, `validate`, and `propose`, do not return protected data or a proposal/result until the required audit record has been accepted. For `update`, `replace`, `reset`, and `delete`, require durable intent evidence before entering publication/commit. If that precondition fails, reject the operation without publication. After a mutation commits, record its outcome; if outcome recording fails, preserve the already-durable intent as an unresolved outcome and trigger reconciliation/alerting rather than pretending the mutation did not happen or attempting an unsafe rollback.
2. **Authorization composition:** use a governed composition adapter at the P0-05 consumer boundary. Mutation requires all three independent conditions: P0-07 domain capability authorization ALLOW, P0-07 policy evaluation ALLOW, and P0-04/P0-05 transaction authorization ALLOW. The adapter must preserve the original independently authorized P0-04 context and must not mint, translate, broaden, or self-grant transaction authority.

These are recommended target semantics, not accepted changes. A compatible durable audit sink, event schema, privacy/retention policy, trusted-context issuer/lifecycle, and the exact adapter interface are not evidenced as accepted in the reviewed sources. Therefore implementation remains blocked until the existing governance/API gates are satisfied.

## 2. Live source pins and interpretation

| Source | Ref | Blob SHA | What it establishes / does not establish |
|---|---|---|---|
| [P0-07 Governance Decision v1.0](https://github.com/VlDMlNSh/mediahub-os/blob/codex/p0-07-configuration-policy-architecture/docs/architecture/P0-07-governance-decision.md) | `codex/p0-07-configuration-policy-architecture` | `9ff8ad6115a9c0a5182a84a1f4d3d8c85995a96e` | ACCEPTED — IMPLEMENTATION AUTHORIZED for exact P0-07 v1 scope; P0-04 remains sole canonical mutation authority; P0-05 remains mandatory boundary; production qualification not granted. It does not define a complete audit-sink/outage policy. |
| [P0-07 Authorization Reconciliation v1.0](https://github.com/VlDMlNSh/mediahub-os/blob/implementation/p0-07-configuration-policy-runtime/docs/architecture/P0-07-authorization-reconciliation.md) | `implementation/p0-07-configuration-policy-runtime` | `04381ce6e223b8632ec15d17e475b56fe1ab8772` | Describes conjunctive authorization and the P0-07 → P0-05 → P0-04 path, while explicitly stating no P0-04/P0-05 change is authorized by that reconciliation. |
| [P0-07 → P0-05 Mutation Adapter Contract v1.0](https://github.com/VlDMlNSh/mediahub-os/blob/implementation/p0-07-configuration-policy-runtime/docs/architecture/P0-07-p0-05-mutation-adapter-contract.md) | `implementation/p0-07-configuration-policy-runtime` | `22b8e1897e124578e66c8d619b3e8eaf41f69a88` | Explicitly BLOCKED — GOVERNANCE/API GAP. No accepted mapping from P0-07 capability grants to P0-04 transaction authority. Lists existing-context, governed bridge, and revised P0-05 contract as alternatives. |
| [P0-05 Consumer Contract v1.0](https://github.com/VlDMlNSh/mediahub-os/blob/implementation/p0-07-configuration-policy-runtime/docs/architecture/P0-05-consumer-contract.md) | `implementation/p0-07-configuration-policy-runtime` | `bba8dd3e8812767b6dbc8afff1bec5bd36dc828b` | Header remains DRAFT — GOVERNANCE REVIEW REQUIRED; commit is the publication boundary and authorization/freshness are revalidated. Do not silently promote its status. |
| [P0-07 × MH-06/MH-12/MH-13 Audit, Privacy and Authorization Decision Packet](https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/checkpoints/p0-07-audit-privacy-governance-crosswalk-2026-10-12.md) | `docs/mediahub-chat-tree-map-20261012` | `ce371d0dba1d5591eaca3a9f1c4e3ce351557a97` | Explicitly non-normative; warns not to infer a durable audit path, sink, retention, or fail-open/fail-closed choice from a schema or in-memory diagnostic object. |
| [P0-07 D2 Trusted Authorization Context Authority and Lifecycle Proposal](https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/checkpoints/P0-07-D2-TRUSTED-CONTEXT-AUTHORITY-LIFECYCLE-PROPOSAL-2026-10-13.md) | `docs/mediahub-chat-tree-map-20261012` | `c0ae0d3fe340c3e50382b7d4aa8da7b6b5f56d9f` | Proposal only; accepted issuer and complete context lifecycle are not evidenced. Do not treat caller-supplied context as trusted merely because it is present. |

The bounded current documentation branch at the start of this pass was `2859c7813764c1592112285a3be36018a535fa28`; `main` was `b45324009ac3aa65322a702c28069b12190bc4b8`. GitHub compare reports the branches **DIVERGED**, docs branch ahead by 1623 and behind by 10, merge base `f0f406feb9f9816b009f4e6e756813541e53b9bc`. No integration was attempted.

## 3. Recommended operation-scoped R-06 matrix

All seven operations must generate a minimal authorization decision event. For successful operations, the required pre-action evidence must be durably accepted before protected results are released or a mutation can publish. Denials remain denials even if the audit sink is unavailable; return only bounded sanitized errors and do not leak sensitive details. If the audit requirement for a request cannot be satisfied, do not perform the protected operation.

| P0-07 operation | Required evidence before protected result/publication | Audit-unavailable behavior | Post-action evidence |
|---|---|---|---|
| `read` | Record operation, authorization/policy decision, target reference and revision before returning protected configuration/policy data. | Deny/withhold result; bounded sanitized error. | Record outcome where available; never log returned configuration/policy values. |
| `validate` | Record decision and bounded target/schema/revision references before returning validation output. | Do not return validation details; reject fail-closed. | Record result class/reason codes, not submitted data or validation payload. |
| `propose` | Record authorization and proposal-intent metadata before returning the inert proposal. | Do not return proposal; reject fail-closed. | Record proposal outcome/reference only; proposal remains non-publishing. |
| `update` | Durable intent record accepted before transaction publication, bound to target and expected generation/version. | Do not publish; abort/reject safely. | Record committed/rejected/unknown outcome; reconcile an unresolved outcome from the durable intent. |
| `replace` | Same as update; record complete-unit replacement intent without recording replacement content. | Do not publish; abort/reject safely. | Record committed/rejected/unknown outcome; never include replacement payload. |
| `reset` | Record approved-default/reset intent and target revision before publication. | Do not publish; abort/reject safely. | Record committed/rejected/unknown outcome and the approved default reference/version, not the default payload. |
| `delete` | Record authorized deletion intent and target reference before publication. | Do not publish; abort/reject safely. | Record committed/rejected/unknown outcome; avoid copying deleted content into the audit record. |

**Commit ordering:** durable intent evidence must precede publication. A post-commit outcome-write failure cannot be represented as rollback: retain the durable intent as `outcome_unknown`, emit an operational alert through an already-approved channel, and reconcile against authoritative state. Do not claim atomic coupling between audit storage and P0-04 unless a separately accepted transaction/outbox contract proves it.

## 4. Minimal audit event and privacy constraints

Recommended logical fields (not a registered schema):

- schema/version and unique event/correlation identifiers;
- timestamp from the approved clock source;
- operation and domain (`configuration` or `policy`);
- privacy-reviewed opaque principal reference (no credentials or raw identity claims);
- exact capability identifier and policy/authorization decision;
- target reference and applicable schema/configuration/policy revision;
- expected generation/state version for mutation intent, where defined by the accepted contract;
- phase (`decision`, `intent`, `outcome`, `reconciliation`), bounded result class and stable reason code;
- policy/schema version needed to reproduce the decision.

Never record secrets, tokens, authorization-context contents, raw configuration/policy values, proposal payloads, arbitrary user text, or full validation payloads. Keep P0-07 free of a new durable personal-data store; send evidence only through a separately governed audit interface. The audit sink's existence, durability guarantees, access controls, retention/deletion, clock guarantees, and privacy classification remain unverified/open. Do not invent them as implementation facts.

## 5. Recommended authorization composition

Keep the authorities distinct:

- **P0-07:** validate the requested domain operation; enforce the exact operation-specific capability and policy.
- **P0-05:** remain the sole consumer/integration boundary; accept the operation decision and independently authorized transaction context only through an explicitly governed contract.
- **P0-04:** remain the sole canonical mutation authority; retain final transaction authorization, freshness/generation checks, and atomic publication.

Required conjunction:

`P0-07 capability ALLOW AND P0-07 policy ALLOW AND P0-04/P0-05 transaction authorization ALLOW`

Any missing, denied, stale, mis-scoped, or unverifiable component denies mutation. The composition adapter must not translate `configuration.update` or any other P0-07 domain capability into `begin`, `commit`, or other P0-04 authority; it must not mint a trusted context; and it must not call P0-04 mutation APIs directly from P0-07.

**Why this direction:** the existing-context-only option depends on a trusted issuer and a valid context lifecycle that the inspected evidence does not establish. Revising P0-05/P0-04 contracts broadens the normative change surface. A small governed composition adapter preserves the accepted authority hierarchy and allows independent revalidation at the existing consumer boundary, while keeping both authorization domains conjunctive. This is a recommendation only; the current adapter contract still blocks mutation.

## 6. Gates and implementation entry conditions

Before implementation can be considered unblocked, the project must establish and accept:

1. an audit sink/interface with durable acknowledgement semantics and operational ownership;
2. the minimal event schema, privacy classification, access, retention/deletion, and reconciliation procedure;
3. operation-specific audit requirements and outage semantics in a controlled governance artifact;
4. trusted principal/context issuer, audience, freshness, expiry/revocation and transaction-binding lifecycle;
5. a P0-05-facing composition interface that independently checks P0-07 authorization/policy and P0-04 transaction authority without capability translation;
6. explicit disposition of the P0-05 draft/header discrepancy and P0-07 architecture header discrepancy through document control, not silent edits;
7. contract-level negative-path evidence before qualification claims.

No code or normative contract was changed. No tests, qualification, provider/model calls, credentials, runtime/host inspection, infrastructure, deployment, migration, merge, rebase, or cherry-pick were performed.

## 7. Current disposition

- Recommended technical direction: **SELECTED AS PROPOSAL**.
- R-06 governance status: **OPEN — recommendation prepared; audit policy not accepted/frozen**.
- P0-07-to-P0-05/P0-04 mutation publication: **BLOCKED — GOVERNANCE/API GAP**.
- Trusted context lifecycle: **PROPOSED / NOT ACCEPTED / NOT FROZEN**.
- D1: NOT DEMONSTRATED.
- D2: NOT EVIDENCED / NOT ACCEPTED / NOT FROZEN.
- D3: NOT EVIDENCED.
- D6: OPEN.
- Qualification: **NO-GO / NOT PROVEN**.

## 8. Next bounded step

Continue source-only reconciliation against the canonical MH-12 security and MH-13 privacy contracts to verify that the proposed minimal event fields, access, retention, and failure behavior do not conflict with accepted requirements. If no accepted durable audit interface exists, record the missing dependency explicitly; do not implement a sink or modify normative contracts without the required authorization.

Project map: [MEDIAHUB-CHAT-TREE-MAP.md](../architecture/MEDIAHUB-CHAT-TREE-MAP.md).
