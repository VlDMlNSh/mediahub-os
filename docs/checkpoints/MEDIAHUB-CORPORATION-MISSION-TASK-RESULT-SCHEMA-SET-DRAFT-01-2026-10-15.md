# MediaHub OS — Corporation Mission / Task / Result Schema Set Draft 01

- Date: 2026-10-15
- Repository: VlDMlNSh/mediahub-os
- Ref: docs/mediahub-chat-tree-map-20261012
- Status: VERSIONED DESIGN DRAFT / NOT NORMATIVE / NOT ACCEPTED / NOT IMPLEMENTED / NOT QUALIFIED
- Scope: field-level schema proposal for mission, task DAG, executor profile, task result and evidence reference in Contour A.
- Authority: owner-approved DEC-DEV-02 Option C, accepted Baseline 2.0 and source-bound domain contracts remain controlling.
- Change boundary: documentation only. This file does not define a callable API, grant authorization, change any accepted schema, or authorize runtime work.

## 1. Why this is a draft

The Wave 01 inventory and Wave 09 technical baseline establish that existing schemas have narrower scopes and no accepted corporation-wide wire contract has been proven. This document records a coherent candidate field set so dependencies and missing authority can be reviewed without inventing live interfaces.

The following are explicitly unresolved and must not be serialized as accepted production semantics:
- Jarvis → ASTRA A0 ingress operation, protocol, version, caller authentication and response/error contract.
- Capability issuer, delegation/attenuation, audience, expiry, revocation, replay protection and verifier lifecycle.
- A0-persisted fencing primitive and authoritative publication acceptance rule.
- Exact cancellation/completion race behavior and persistence/retention semantics.
- Accepted schema ID/version registry and compatibility/deprecation policy.
- Provider/gateway/upstream identity and route/egress evidence where source evidence is unavailable.

Fail-closed rule: any mission requiring A0-managed queue/claim/lease/gate state remains BLOCKED until the accepted ingress and capability-authority contracts are sourced. This draft is not an authorization path.

## 2. Authority and lifecycle invariants

1. Jarvis owns corporation-level mission coordination, bounded decomposition, permitted route selection, progress tracking and reporting.
2. ASTRA A0 alone writes ASTRA-internal queue, claim, lease, heartbeat, retry/cancellation and ASTRA evidence/gate state within its accepted scope.
3. MediaHub Product State Authority alone mutates canonical MediaHub product state in Contour B.
4. Executor, agent role, client, gateway, upstream provider and model are separate identity dimensions. Unknown identity remains UNKNOWN.
5. Worker output is untrusted until validated against the task contract and independently reviewed where required.
6. VERIFIED is result-validation status; it is not qualification, release, deployment or product acceptance.
7. No global exactly-once side-effect guarantee is claimed. Durable idempotent admission, if accepted, has a bounded key scope and does not make arbitrary executor side effects idempotent.
8. Local-only routing must fail closed; no silent cloud/provider fallback.
9. Secrets, tokens, private keys, raw credentials and session material are prohibited from schema payloads and evidence.
10. A proposal or schema file does not prove implementation, runtime enforcement or qualification.

## 3. Schema set overview

| Draft schema | Purpose | Proposed owner | Must not become |
|---|---|---|---|
| Mission envelope | Corporation-level request, intent, constraints, mission status and correlation | Jarvis for coordination; ingress authority unresolved | ASTRA queue mutation or product-state command |
| Task DAG | Immutable task graph revision, dependencies, requirements and integration gates | Jarvis plans; ASTRA admission/queue state stays A0-owned | A second authoritative queue |
| Executor profile | Declared worker capability, identity and admission constraints | Admission registry/governance; exact owner interface unresolved | Self-asserted permission or model/provider equivalence |
| Task result | One attempt's disposition, outputs, provenance and validation state | Executor emits proposal; verifier/A0 determine scoped dispositions | Self-certified acceptance or direct product mutation |
| Evidence reference | Immutable pointer/digest to evidence bound to source, attempt and reviewer | Evidence service/store interface unresolved; authority remains scoped | Evidence content containing secrets or unverified status promotion |

These are logical envelopes and field recommendations, not finalized JSON Schema files or wire-compatible APIs.

## 4. Common metadata candidate

| Field | Candidate type / constraint | Status / rationale |
|---|---|---|
| schema_id | Non-empty stable schema identifier | Proposed; registry and collision check required before assignment |
| schema_version | Semantic version string | Proposed; compatibility policy not accepted |
| mission_id, task_id, attempt_id | Opaque stable identifiers, distinct namespaces | Recommended; cross-check repository ID registry before adopting a format |
| created_at, updated_at | UTC timestamp | Proposed; clock source and timestamp trust rules unresolved |
| correlation_id | Opaque trace/correlation identifier | Proposed |
| source_revision / target_sha | Git commit SHA where applicable | Source-bound evidence; absent when no source revision applies |
| policy_revision | Immutable policy revision/digest | Required for auditable routing/authorization decisions; source interface unresolved |
| data_classification | Enum from accepted policy vocabulary | Reuse only after source verification; no new values inferred |
| status | Schema-specific enum | Must not be one generic lifecycle enum across all object types |

No issuer identity, capability token shape, A0 endpoint, or authorization-context field is defined here.

## 5. Mission envelope — candidate fields

| Field | Purpose | Gate |
|---|---|---|
| mission_id | Stable mission identity | ID namespace collision check |
| request_summary | Bounded human-readable intent | Input constraints and data classification required |
| acceptance_criteria | Verifiable outcome statements | Must identify expected evidence; no automatic acceptance |
| constraints | Deadline, budget, permitted operations and data/egress constraints | Policy schema and authority source unresolved |
| task_graph_ref | Immutable DAG revision reference | Bind to a specific graph digest |
| requester_principal_ref | Reference to authenticated principal, not credential | Identity provider/issuer contract unresolved |
| admission_ref | Reference to accepted ingress disposition | Do not populate until accepted A0 ingress exists |
| mission_status | Draft lifecycle: DRAFT, SUBMITTED, ACCEPTED, REJECTED, PLANNED, RUNNING, SUCCEEDED, PARTIAL, FAILED, CANCELLED, BLOCKED | Logical model only; transitions/owner require governance |
| result_refs | Task result references | Validate against declared DAG outputs |
| evidence_refs | Evidence references | Immutable digest and provenance required |

Mission submission in this draft does not imply A0 admission or dispatch permission.

## 6. Task DAG — candidate fields

| Field | Purpose | Gate |
|---|---|---|
| dag_id, dag_revision | Immutable graph identity/revision | Registry/collision check |
| mission_id | Parent mission | Referential integrity |
| tasks[] | Task nodes with unique task_id and task contract reference | Existing task schemas/IDs must be reconciled first |
| dependencies[] | Directed edges between task IDs | Missing nodes and cycles must be rejected before dispatch; implementation not claimed |
| input_refs[] / output_contract_ref | Typed, digest-bound data references | Contract and artifact validation required |
| required_capabilities[] | Declared needs, not grants | Must not mint/expand capability |
| allowed_executor_classes[] | Admissible executor classes | Policy decision and permanent executor-binding rules apply |
| parallelism_constraints | Declared concurrency and shared-resource constraints | ASTRA G-5 remains max three active claims within its governed scope |
| integration_gate_refs[] | Verification/integration requirements | No integration authority inferred |

A DAG's declared dependencies do not themselves prove execution order, isolation, fencing or cancellation propagation.

## 7. Executor profile — candidate fields

| Field | Purpose | Gate |
|---|---|---|
| executor_id | Stable service/worker identity | Enrollment and authentication contract unresolved |
| executor_class | Capability class/profile | Governed registry required |
| agent_role | Task-scoped role such as planner, implementer or verifier | Role is not an authority grant |
| supported_operations[] | Explicit bounded operations | Authorization remains separate |
| supported_contract_versions[] | Input/output schema compatibility | Exact schema registry required |
| runtime_identity | Runtime/backend identity where relevant | Evidence required; do not infer from product name |
| resource_profile_ref | Capacity and resource evidence | Freshness and measurement source required |
| isolation_profile_ref | Workspace/process/network restrictions | Exact target OS and enforcement evidence required |
| egress_profile_ref | Allowed destinations/local-only policy | Unknown route fails closed |
| admission_status | Candidate, admitted, blocked, revoked, etc. | Governed registry; status transitions not specified here |

An executor profile is descriptive admission input. It is not a capability token and cannot self-authorize.

## 8. Task result — candidate fields

| Field | Purpose | Gate |
|---|---|---|
| mission_id, task_id, attempt_id | Unambiguous attribution | Distinct IDs; attempt IDs never reused |
| task_contract_ref | Exact task requirements/revision | Immutable contract reference |
| input_digest, target_sha | Bind inputs/source revision | Canonicalization rules unresolved |
| executor_id, route_decision_ref | Who ran and which route was selected | Provider/gateway/upstream identities remain separate |
| started_at, finished_at | Attempt timing | Timestamp trust/freshness rules required |
| attempt_status | RUNNING, RESULT_PENDING_VALIDATION, VERIFIED, UNVERIFIED, FAILED, CANCELLED, BLOCKED, PARTIAL | Logical proposal; authoritative transitions not implemented |
| artifact_refs[] | Output URI/reference plus digest | Storage scheme, access control and retention unresolved |
| checks[] | Check name, source revision, result and evidence reference | No tests are authorized by this draft |
| limitations[] | Missing evidence, scope limits, known deviations | Required to prevent overclaiming |
| cancellation_state | Request/acknowledgement/terminal observation | A0 race and fencing contract unresolved |
| verifier_disposition | Independent validation result and verifier reference | Verifier independence must be evidenced |
| evidence_refs[] | Evidence for artifacts and disposition | Immutable, digest-bound, secret-free |

An executor may emit a result proposal but may not set its own output to independently verified, qualified, released, deployed or accepted.

## 9. Evidence reference — candidate fields

| Field | Purpose | Gate |
|---|---|---|
| evidence_id | Stable evidence identity | ID registry/collision check |
| evidence_kind | Source, review, run, check, artifact, policy decision, verifier report, etc. | Controlled vocabulary required |
| subject_ref | Mission/task/attempt/component subject | Referential integrity |
| source_ref, source_sha | Repository/ref and immutable source revision | Must match the evidence claim's scope |
| artifact_digest | Digest of referenced artifact or evidence payload | Digest algorithm and canonicalization policy required |
| observed_at | Observation time | Freshness policy required |
| producer_principal_ref | Producer identity reference | Identity provenance unresolved |
| reviewer_principal_ref | Independent reviewer identity reference | Required where independent verification applies |
| policy_revision | Relevant policy revision | Policy evidence interface unresolved |
| result | PASS, FAIL, UNKNOWN, BLOCKED, PARTIAL or NOT_RUN | Evidence result is not automatic gate promotion |
| limitations[] | Scope, freshness, missing evidence | Must be retained |
| content_ref | Pointer to content; no inline secret material | Access control and retention unresolved |

Evidence corrections create a new linked record; prior evidence is not silently rewritten.

## 10. Reuse crosswalk — existing artifacts are not overloaded

| Existing source | Proven scope | Do not infer |
|---|---|---|
| schemas/ai/ai-inference-request.schema.json on main | Single inference request | Corporation mission/task lifecycle |
| schemas/mediahub-component-evidence-record.schema.json on documentation branch | Draft component/gate/deployment evidence record | Accepted corporation evidence API or qualification |
| docs/operations/ASTRA-EXECUTOR-CAPABILITY-MATRIX.md on main | ASTRA executor workflow, dependencies, claims and bounded executor policy | Jarvis ingress, capability issuance or global task schema |
| architecture/ASTRA-GOLD-GOVERNANCE-CONTRACT.yaml on main | ASTRA-specific documented timing/concurrency limits | Corporation-wide defaults or runtime enforcement |
| docs/architecture/MH-12-security-architecture.md on main | Identity/authentication/trust/capability/authorization/policy boundary invariants | Concrete issuer, token format or endpoint |
| MEDIAHUB-JARVIS-CONTROL-PLANE-GITHUB-ADAPTER-CONTRACT-DRAFT-01 on documentation branch | Draft mission envelope and least-privilege GitHub adapter | Accepted A0 ingress/API |
| MEDIAHUB-CORPORATION-TASK-RESULT-TECHNICAL-BASELINE-WAVE-09 | Technical recommendation for lifecycle, idempotency, fencing, cancellation and result fields | Normative schema, implementation or authorization |

## 11. Required cross-contract acceptance gates

Before any part of this proposal can become normative, source and governance evidence must establish:

1. Stable schema IDs and collision-free object identifiers.
2. Accepted Jarvis → ASTRA A0 ingress and caller authentication.
3. Capability issuer/delegation/attenuation/lifetime/revocation/replay/audit lifecycle.
4. A0 authoritative admission, claim, fencing and result-publication semantics.
5. Idempotency key scope, payload canonicalization, retention and conflict handling.
6. Cancellation/completion race rules and worker propagation semantics.
7. Accepted executor identity, provider/gateway/model separation and route/egress evidence.
8. Immutable artifact/evidence storage references and access/retention policy.
9. Independent verifier identity, evidence requirements and lifecycle separation.
10. Version compatibility, deprecation and change-control approval.
11. Explicit preservation of Product State Authority as the only canonical Contour B product-state mutator.
12. Explicit Contour A deployment and independent-acceptance gate before Contour B autonomous product development.

## 12. Status and next step

- This draft is a field-level design aid, not an accepted wire schema, API or normative contract.
- All A0-dependent admission/dispatch fields remain unresolved and fail closed.
- No schema ID format has been assigned; no historical identifier has been reused or renumbered.
- No code, runtime, configuration, normative main-branch contract or existing schema was modified.
- No tests, installations, model/provider calls, credentials, host/runtime inspection, qualification, infrastructure change, deployment or branch integration occurred.
- Next bounded step: perform a collision-aware identifier/schema-registry crosswalk against existing repository schema and task/agent/component IDs, then revise this draft only with source-backed results. Keep it blocked from normative promotion until ingress and capability-authority prerequisites are accepted.
