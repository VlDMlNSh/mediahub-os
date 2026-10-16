# MediaHub OS — Contour A WB-14U: Health/readiness and A0 lifecycle-status ownership closure

- Date: 2026-10-16
- Ref: docs/mediahub-chat-tree-map-20261012
- Status: **SOURCE-ONLY RECONCILIATION / PARTIAL CLOSURE / OWNER DECISION STILL REQUIRED / NOT IMPLEMENTED / NOT TESTED / NOT QUALIFIED**
- Scope: resolve what can be resolved from accepted health/readiness semantics and establish which lifecycle/status questions remain unowned or non-normative before the Jarvis → ASTRA A0 ingress schema can be finalized.
- Change boundary: documentation only. No normative contract, schema, runtime source, configuration or infrastructure was changed.

## 1. Result

This pass separates three issues that prior WB-14T wording had conflated:

1. **MH-06 semantic authority is already accepted.** `docs/architecture/MH-06-ADR-001-health-readiness-semantic-contract.md` is explicitly marked ACCEPTED / GOVERNANCE ACCEPTED. Its scoped semantic contract is not waiting for general acceptance. It does not authorize implementation.
2. **The generic domain health schema and MH-06 use different vocabularies.** The domain schema is a separate, currently existing schema with its own ID and fields. It lists HEALTHY, DEGRADED, WARNING, FAILED, UNKNOWN. The accepted MH-06 health semantics list UNKNOWN, HEALTHY, DEGRADED, FAILED, QUARANTINED. The accepted MH-06 readiness semantics are UNKNOWN, NOT_READY, READY, DEGRADED, QUARANTINED. The source set does not establish an approved mapping or that these different schemas have the same scope. This is a real cross-contract reconciliation gap, not grounds to edit either enum silently.
3. **No accepted corporation-wide A0 lifecycle state machine was found.** Owner direction establishes that A0 owns ASTRA-internal queue/claim/lease/heartbeat/retry/cancellation/recovery and evidence/gate transitions. ASTRA governance gives lifecycle numeric bounds and gate IDs; it does not provide a complete A0 ingress-facing state enum and transition table. The corporation task/result schema set has illustrative mission_status and attempt_status lists explicitly marked logical/non-normative, with transitions and owner semantics unresolved.

**Conclusion:** WB-14U closes the false claim that MH-06 itself remains merely proposed. It does not close the domain-health mapping or A0 lifecycle enum/transition contract. D-ING-05 remains OPEN, narrowed to an owner decision on the relationship between the existing domain health schema and accepted MH-06 semantics, plus the contract-specific A0 probe/readiness mapping. The final ingress schema remains blocked.

## 2. Live repository state

- `main` HEAD: `ab36db009d034db8dca723691e23b331322287e7`.
- Documentation branch HEAD/tree at review: `0e818a81acbc34d5485b3115c7a621354666d07a`.
- Recursive tree: 973 entries; `truncated=false`.
- Compare `main...docs/mediahub-chat-tree-map-20261012`: diverged, docs branch ahead 1499 / behind 4; merge base `f0f406feb9f9816b009f4e6e756813541e53b9bc`.
- No branch integration or main ref movement was attempted.

The latest checkpoint says WB-14T → WB-14U. Current tree and refs were refreshed rather than relying on the checkpoint's older branch HEAD. WB-14S, WB-14T, the master roadmap and map were re-read for this pass.

## 3. Source-pinned health/readiness reconciliation

| Source | Current docs-branch blob SHA | Exact finding | Status |
|---|---|---|---|
| `docs/architecture/MH-06-ADR-001-health-readiness-semantic-contract.md` | `7dda05379bd70007dc18acd62ed14fc83f0c9226` | Header explicitly says ACCEPTED / GOVERNANCE ACCEPTED; scope MH-06 Core Runtime Services; implementation authorization NO. | Accepted semantic contract; no implementation permission. |
| `docs/architecture/MH-06-health-readiness.md` | `895f0bb2dec39c989d2dca345afeefde4cb70626` | Repeats the accepted semantic vocabularies and says P0-06 lifecycle READY is not MH-06 readiness READY. | Consistent summary of accepted MH-06 semantics. |
| `schemas/domain/health.schema.json` | `8b85c4c1dd271ca53efb0e4b50fd8654e0f2d58e` | `$id=mediahub://schemas/domain/health.schema.json`; requires status, timestamp, source, details; status enum HEALTHY, DEGRADED, WARNING, FAILED, UNKNOWN. | Existing domain schema; vocabulary differs from MH-06. No approved mapping was found in the inspected sources. |
| `schemas/domain/lifecycle.schema.json` | `f573802fc08d4af90fa5d1c15adcc4334839c05a` | Describes canonical lifecycle of a MediaHub Device, with DISCOVERED, IDENTIFIED, ONBOARDING, ACTIVE, OFFLINE, DEGRADED, RETIRED. | Device lifecycle, not A0 task/mission lifecycle and not MH-06 readiness. |
| `docs/architecture/MH-06-lifecycle-model.md` | `04dd558a1a19d16340792d6761f47ac0d5408d73` | Status REQUIRES VERIFICATION against frozen P0-06 implementation/evidence; lifecycle values PROVISIONING, INITIALIZING, SELF_TEST, READY, DEGRADED, SAFE_MODE, RECOVERY. Explicitly excludes STOPPING, STOPPED, FAILED and QUARANTINED from P0-06 lifecycle absent governance evidence. | Different lifecycle domain; verification remains open. |
| `runtime/mediahub_runtime/astra_lifecycle.py` | `703dd1df043a29d187c7ed34c3b519a9f36ed93e` | Implements Astra memory provenance/supersession metadata; it is not an A0 queue/claim/task lifecycle state machine. | Must not be cited as evidence of A0 workflow lifecycle implementation. |
| `architecture/ASTRA-GOLD-GOVERNANCE-CONTRACT.yaml` | `1d3ac25e7817f365807ad85d0d7c9007bd48bebf` | Canonical governance source for ASTRA gates and numeric lifecycle bounds (heartbeat, lease, timeout, retry, concurrency) and gate failure states. Does not define a complete ingress-facing mission/task status machine. | Governs scoped bounds/gates; insufficient to finalize ingress status enums. |
| `docs/operations/ASTRA-EXECUTOR-CAPABILITY-MATRIX.md` | `9ad83781a8da53d1a8f540ede54eba95281f01c0` | Defines A0 authority over ASTRA internal queue/claim/lease/evidence/gate transitions and dependency-aware scheduling; explicitly excludes Product State Authority. | Confirms owner boundary, not a complete wire state machine. |
| Corporation mission/task/result schema-set draft | `e6c65c9949f45d247a2a57d1806da33737060619` | `mission_status` candidate list is DRAFT, SUBMITTED, ACCEPTED, REJECTED, PLANNED, RUNNING, SUCCEEDED, PARTIAL, FAILED, CANCELLED, BLOCKED; `attempt_status` candidate list is RUNNING, RESULT_PENDING_VALIDATION, VERIFIED, UNVERIFIED, FAILED, CANCELLED, BLOCKED, PARTIAL. Both are logical/non-normative and transitions/owner authority are unresolved. | Draft vocabulary only; do not promote into A0 API. |
| WB-14S schema ownership/operation map | `6b5159fdbe0c99d34e754047dd7c0a8afde8c61c` | Already distinguishes admission disposition, A0 lifecycle, attempt outcome, verifier, qualification, health, readiness, trust and authorization. Its health mapping is marked unresolved. | Preserve the domain separation. |
| WB-14T owner/governance decision packet | `4a70802f2eafe264f37a5c47ddf0dc82586db212` | Correctly lists the domain-schema vs MH-06 vocabulary discrepancy but incorrectly states “MH-06 itself remains proposed pending full reconciliation/governance acceptance,” despite the accepted ADR and summary. | Narrow documentary correction required; MH-06 semantic acceptance is not pending. |

## 4. Resolved and unresolved distinctions

### 4.1 Resolved by accepted source

These semantic distinctions are not open for the new ingress design to collapse:

- **Probe outcome**: did the expected authenticated responder answer the fresh, correlated challenge under the expected contract revision?
- **Entity/service health**: observation of a health condition under the relevant health contract.
- **Operation readiness**: whether prerequisites for a specific operation are satisfied under MH-06.
- **Trust**: whether the principal/context is trusted under the security contract.
- **Authorization**: whether that principal is allowed to perform the requested operation/resource action.
- **A0 lifecycle**: ASTRA-owned engineering workflow state.
- **Attempt outcome**: one execution attempt's result.
- **Verifier disposition**: independent review of output/evidence.
- **Qualification/gate state**: governed qualification state, not task success.
- **Product state**: exclusively owned by MediaHub Product State Authority.

Health or readiness cannot grant trust, capability, authorization or mutation authority. A fresh successful probe is not proof that the service is ready for every operation.

### 4.2 Domain health enum discrepancy — owner decision required

The current generic domain schema includes `WARNING` and omits `QUARANTINED`; the accepted MH-06 scoped semantic contract includes `QUARANTINED` and omits `WARNING`. Both include HEALTHY, DEGRADED, FAILED and UNKNOWN.

Do not choose one of the following without the relevant domain/MH-06 owner:
- A. Keep the schemas intentionally separate by scope and specify an explicit, loss-aware mapping/reference contract for consumers that need both.
- B. Revise the generic domain schema through a controlled schema-owner decision if it is intended to be the shared canonical entity-health schema.
- C. Define a new scoped contract/reference for Core Runtime Services health while preserving the generic domain schema for its existing consumers.

Recommendation: **A as the immediate ingress design boundary**—do not merge the enums; carry a scoped health contract/reference and only add an explicit mapping after the owners decide whether the two schemas have overlapping scope. This is not an accepted domain architecture decision. A future schema-owner review may choose B or C.

### 4.3 A0 lifecycle/status state machine — still open

Accepted source establishes the A0 authority boundary but not the final corporation-facing transition contract. In particular, do not assume that:
- mission_status and attempt_status are the same state machine;
- admission ACCEPTED means execution RUNNING;
- cancellation requested/acknowledged means execution stopped;
- executor-reported VERIFIED is independently verified;
- task SUCCEEDED means ASTRA qualification PASS or product acceptance;
- a health/readiness status is an A0 lifecycle state.

A0 lifecycle owner/governance must define, at minimum:
1. Separate admission disposition from lifecycle state.
2. State transition table and authority for each transition.
3. Revision/sequence semantics for status responses.
4. Claim/lease/fencing and stale/late result rules.
5. Cancellation request, acknowledgement, effective cancellation and completion-race outcomes.
6. Retry/recovery transitions and terminality.
7. Relation between attempt outcome and task/mission aggregation.
8. Independent verifier and qualification-gate boundaries.
9. Unknown/invalid transition behavior and stable error reasons.

No complete state transition contract or accepted enum was found in this pass. Do not write final JSON Schemas yet.

## 5. Corrective statement for WB-14T

WB-14T §7 should no longer state that MH-06 itself remains proposed pending full reconciliation/governance acceptance. The evidence supports the following replacement statement:

> The MH-06 Health/Readiness semantic contract is ACCEPTED / GOVERNANCE ACCEPTED for MH-06 Core Runtime Services, with implementation authorization explicitly not granted. A separate existing domain health schema uses a different status vocabulary. The approved mapping or intentional separation between those scopes remains unresolved and requires the relevant schema/domain owners. The proposed A0 health wire contract must keep probe outcome, scoped health, operation readiness, trust and authorization separate.

This wording corrects the documentary status without changing the accepted ADR, the generic domain schema, or any runtime contract.

## 6. Proposed follow-up decision record

Keep D-ING-05 OPEN, but split its acceptance criteria into two independently reviewable sub-decisions:

- **D-ING-05a — Domain health schema ↔ MH-06 scope/mapping:** decide whether scopes are separate, mapped, or the generic schema should be revised. Owner: domain schema owner + MH-06 governance. No enum edit in this pass.
- **D-ING-05b — A0 HealthChallenge/HealthResponse contract:** define probe outcome, challenge/request/digest correlation, authenticated responder context, capture/response time, contract revision and optional scoped health/readiness references. Owner: A0 ingress contract owner plus security/health governance. Numeric freshness remains under D-ING-04 and is not selected here.

Add a separate **D-ING-06 — A0 lifecycle state machine and transition ownership** with owner response OPEN. This does not replace D-ING-03 admission/idempotency; it formalizes the state-transition contract needed after admission.

Recommended status domains remain separate and versioned only after governance:
- `probe_outcome`
- `entity_health` (schema/scope TBD)
- `operation_readiness` (accepted MH-06 semantics where applicable)
- `admission_disposition`
- `a0_lifecycle_state`
- `attempt_outcome`
- `verifier_disposition`
- `qualification_gate_state`
- `trust_state`
- `authorization_decision`

These names are a field-separation proposal, not registered schema fields or enums.

## 7. Verification boundary and next step

Completed:
- Refreshed live refs, recursive tree and branch comparison.
- Read MH-06 accepted ADR/summary, generic domain health and device lifecycle schemas, P0-06 lifecycle summary, ASTRA governance contract, executor capability matrix, corporation schema draft, WB-14S and WB-14T.
- Distinguished source-backed semantic acceptance from implementation authorization and from unresolved cross-schema mapping.
- Identified the precise erroneous pending-acceptance sentence in WB-14T and prepared a replacement.
- No code/schema/runtime files were edited; no tests or validators were executed.

Not performed:
- No test, validator, qualification, workflow, provider/model, credential, host/runtime, installation, infrastructure, deployment, migration, merge, rebase or cherry-pick action.
- No enum was selected or normalized by assumption.
- No runtime readiness, implementation, qualification or acceptance is claimed.

Next bounded step: **WB-14V — correct WB-14T’s MH-06 status sentence and record the split decision packet D-ING-05a / D-ING-05b plus D-ING-06, then update map/checkpoint/roadmap.** Keep all owner responses OPEN until explicitly accepted. Do not create final JSON Schemas until the scoped health mapping and A0 lifecycle transition contract have accountable owners and accepted decisions.

- Project map: [MEDIAHUB-CHAT-TREE-MAP.md](../architecture/MEDIAHUB-CHAT-TREE-MAP.md).
