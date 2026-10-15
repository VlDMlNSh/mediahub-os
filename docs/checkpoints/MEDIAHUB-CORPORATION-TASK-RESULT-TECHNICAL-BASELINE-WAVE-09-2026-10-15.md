# MediaHub OS — Corporation Task/Result Contract: Recommended Technical Baseline — Wave 09

- Date: 2026-10-15
- Repository: `VlDMlNSh/mediahub-os`
- Ref: `docs/mediahub-chat-tree-map-20261012`
- Status: **TECHNICAL RECOMMENDATION / DESIGN INPUT / NOT AN ACCEPTED NORMATIVE CONTRACT**
- Scope: close implementation-design ambiguity where existing owner decisions and source contracts provide enough constraints; explicitly fail closed where an authoritative issuer/API or governance source is absent.
- Change boundary: documentation-only. No code, normative primary contract, schema, configuration, runtime or infrastructure changed.

## 1. Decision rule and authority

The owner instruction asks that technical questions be closed without repeated owner interruptions. This brief therefore records recommended defaults for technical design. It does not override the repository's governance rules: a proposal does not become an accepted normative contract, and missing authorization is not filled by assumption.

Owner-approved DEC-DEV-02 Option C remains the authority boundary:
- Jarvis coordinates corporation-level missions and dispatches only through permitted routes.
- ASTRA A0 is the single writer for ASTRA-internal queue, claim, lease, heartbeat, retry/cancellation and ASTRA evidence/gate state.
- MediaHub Product State Authority remains the sole canonical product-state mutation authority.
- External executors/controllers are bounded worker boundaries, never alternate MediaHub or ASTRA state authorities.

## 2. Recommended contract choices

| Area | Recommended technical default | Why | Gate/status |
|---|---|---|---|
| Mission/task identifiers | Opaque stable IDs; mission ID, task ID and attempt ID are distinct. Never reuse IDs after terminal disposition. | Prevents collisions between mission, DAG node and retry attempt. | Design recommendation |
| Schema versioning | Explicit schema identifier plus semantic version; reject unknown major versions and unknown authority-bearing fields. | Prevents silent interpretation drift. | Design recommendation |
| Payload binding | Bind idempotency to authenticated principal, operation, target/resource, schema revision and canonical payload digest. | Prevents a key being replayed for a different request. | Design recommendation |
| Admission/idempotency | Durable admission record; same key + same digest returns the original admission disposition; same key + different digest is a conflict. Scope is bounded by issuer/principal and retention policy. | Predictable duplicate submission without claiming exactly-once side effects. | Design recommendation; persistence contract still required |
| DAG | Immutable DAG revision; edges explicitly identify dependencies; reject cycles and missing dependency IDs before dispatch. | Makes readiness and integration deterministic. | Design recommendation |
| Parallelism | Dispatch only dependency-ready tasks when data policy, executor admission, resource budgets and isolation all allow it. ASTRA parallelism must not exceed its governing limit (currently documented max 3 claims). | Preserves existing ASTRA bounds and avoids unsafe concurrency. | Source-aligned recommendation |
| Executor identity | Separate actor, agent role, executor service, client, gateway, upstream provider and model identities. Unknown identity stays UNKNOWN; never infer equivalence from a product label. | Prevents route/provenance conflation. | Source-aligned recommendation |
| Result envelope | Required mission/task/attempt IDs; schema/policy revisions; target/input digest; executor and route provenance; status; artifact URI+digest; checks; limitations; cancellation/partial-output state; timestamps; verifier disposition. Never include secret values. | Makes results attributable and independently verifiable. | Design recommendation |
| Result trust | All remote/worker results are untrusted input until validated against task contract and acceptance criteria. Worker cannot promote its own result to verified/accepted. | Preserves independent verification. | Source-aligned invariant |
| Fencing | Require monotonically increasing claim generation or equivalent storage-enforced fencing primitive; every state-changing completion/publication must be checked by A0 against the current claim. Lease expiry alone is not sufficient proof of fencing. | Rejects stale workers after reassignment. | Recommended semantics; primitive must be established by accepted A0 storage contract |
| Cancellation | Separate request from acknowledged/terminal state. A0 owns authoritative state for A0-managed work. Cancellation does not erase completed evidence; late result publication is accepted only if current claim/fence and terminal-state policy allow it. | Makes cancel/complete races explicit and avoids split-brain lifecycle. | Recommended state semantics |
| Retries | Retry creates a new attempt ID under the same task ID; bounded retry ceiling and backoff; only retry failures classified retryable by policy. Never imply side effects are idempotent unless the executor contract says so. | Separates logical work from attempts. | Reuse ASTRA policy within ASTRA; corporation-wide defaults require versioned policy |
| Recovery | Reconcile from authoritative persisted state and immutable evidence; never reconstruct authority from worker memory or stale heartbeat alone. | Prevents orphan worker state becoming authoritative. | Design recommendation |
| Aggregation | Aggregate only declared DAG outputs; validate schema/digests and dependency revision; detect conflicting outputs; preserve BLOCKED/PARTIAL/UNVERIFIED/FAILED distinctly. | Prevents silent cherry-picking of inconsistent outputs. | Design recommendation |
| Route selection | Record chosen route, reason/policy revision, locality, data class, egress decision, provider/gateway/model identity where known and fallback decision. LOCAL_ONLY must fail closed; no silent cloud fallback. | Auditable local-first routing. | Source-aligned invariant |
| Evidence | Bind evidence to source/target SHA, schema/policy revisions, run/attempt, artifact digest, reviewer identity and freshness. Draft evidence schema is only a substrate, not qualification by itself. | Prevents stale or unbound evidence promoting status. | Source-aligned invariant |
| User-contributed workers | Opt-in, untrusted by default, least-privilege, isolated workspace, minimal payload, scoped short-lived capability, no central secrets. | Limits external trust and blast radius. | Owner target direction; admission remains gated |

## 3. Recommended lifecycle model

The following is a logical model, not a claim that these states already exist in an API:

1. Mission: `DRAFT → SUBMITTED → ACCEPTED | REJECTED`.
2. Accepted mission: `PLANNED → RUNNING → SUCCEEDED | PARTIAL | FAILED | CANCELLED | BLOCKED`.
3. Task: `BLOCKED_BY_DEPENDENCY → READY → ADMITTED → CLAIMED → RUNNING → RESULT_PENDING_VALIDATION → VERIFIED | UNVERIFIED | FAILED`.
4. Cancellation is an orthogonal request/acknowledgement path: `CANCEL_REQUESTED → CANCEL_ACKNOWLEDGED → CANCELLED`; it may race with completion, but A0 resolves authoritative terminal state for A0-managed tasks using current claim/fence and recorded evidence.
5. Retries are separate attempts; a terminal attempt does not overwrite the audit history of earlier attempts.
6. `VERIFIED` is a result-validation disposition, not product-state mutation or production acceptance. Qualification, release, deployment and product acceptance remain separate gates.

No global exactly-once execution guarantee is made. Recommended guarantee is durable, bounded idempotent admission for a defined key scope; executor side effects require separate per-operation semantics.

## 4. Explicit fail-closed decisions for unresolved interfaces

These questions can be operationally closed safely without inventing missing authority:

- **No source-backed accepted Jarvis→A0 API:** do not submit or mutate A0 internals. Keep engineering missions requiring A0 lifecycle controls BLOCKED pending an accepted ingress interface.
- **No source-backed capability issuer/delegation lifecycle:** deny ingress. Do not let Jarvis self-issue authority, and do not mint a token format or issuer identity by assumption.
- **No accepted fencing/storage primitive:** do not claim stale-worker protection is implemented; do not admit concurrent/reassigned publication as safe.
- **No approved corporation-wide schema revision:** treat this document as a proposal only; do not serialize it as normative production traffic.
- **No authoritative route/provider identity:** preserve UNKNOWN/PENDING; do not relabel FreeLLMAPI, FCC, OmniRoute, UnoRouter, Alamo, Ollama, model or upstream provider by inference.
- **No authorized implementation/testing/qualification scope:** remain documentation-only; do not install, execute, call providers, inspect hosts or promote evidence status.

These are fail-closed defaults, not additional owner decisions and not evidence of runtime enforcement.

## 5. Existing contracts to reuse — without overloading them

- `schemas/ai/ai-inference-request.schema.json@main`, blob `e59c72b4a2a62b2372da57c6699ab12ebe25122f`: single inference operation only.
- `schemas/mediahub-component-evidence-record.schema.json@docs/mediahub-chat-tree-map-20261012`, blob `2e62a9d0174e2c72e23ac88edc3094d13b4e336a`: draft component/gate evidence only.
- `docs/operations/ASTRA-EXECUTOR-CAPABILITY-MATRIX.md@main`, blob `da26185254d9954fcee204f81ecca129bf052e7c`: ASTRA internal queue/claim/lease/recovery/target-SHA/verification scope.
- `architecture/ASTRA-GOLD-GOVERNANCE-CONTRACT.yaml@main`, blob `1d3ac25e7817f365807ad85d0d7c9007bd48bebf`: documented bounds include heartbeat TTL 120s, lease TTL 600s, executor timeout 900s, result publication timeout 120s, retry backoff 30s and max 3 parallel autonomous claims. These are declared contract values, not runtime evidence.
- `docs/architecture/MH-12-security-architecture.md@main`, blob `cf4ebfd5bf471ca676f075c51d3a24906504e490`: identity/authentication/trust/capability/authorization/policy/boundary separation and fail-closed ambiguity.
- `docs/checkpoints/MEDIAHUB-JARVIS-CONTROL-PLANE-GITHUB-ADAPTER-CONTRACT-DRAFT-01-2026-10-14.md@docs/mediahub-chat-tree-map-20261012`, blob `e112cc73178eef5f71b8a814296e4902c2e80390`: mission-envelope and least-privilege adapter draft, not accepted ingress.

## 6. Acceptance criteria before promotion to normative contract

A future contract revision may be marked normative only after all of the following are source-bound and approved through existing governance/change control:

1. Exact accepted A0 ingress operation, version, caller identity and error/response semantics.
2. Capability issuer, delegation, lifetime, revocation, replay defense and audit lifecycle.
3. A0-persisted claim/fencing primitive and publication acceptance rule.
4. Cancellation/completion race table and terminal-state ownership.
5. Idempotency scope, payload canonicalization, retention and conflict behavior.
6. Agent/executor profile, DAG, task and result schema with stable IDs and no collision with existing IDs.
7. Route identity/egress decision evidence and LOCAL_ONLY fail-closed semantics.
8. Independent verification and artifact provenance requirements.
9. Schema compatibility/deprecation policy and change-control approval.
10. Explicit separation from Product State Authority and Contour A→Contour B gate.

## 7. Provenance and non-claims

- This is a technical recommendation for the next draft, not an accepted normative contract, schema, API, implementation or qualification.
- DEC-DEV-02 Option C remains owner-approved; no new product/architecture authority decision is made here.
- The documentation branch remains diverged from `main`; this document is not canonical on `main`.
- No tests, installations, provider/model calls, credentials, host/runtime inspection, qualification, infrastructure changes, deployment, merge, rebase or cherry-pick occurred.
- No runtime PASS/VERIFIED/QUALIFIED/PRODUCTION ACCEPTED claim is made.

## 8. Next bounded step

Create a separately versioned draft schema set for `mission`, `task DAG`, `executor profile`, `task result` and `evidence reference` only after validating existing IDs/schema conventions and explicitly marking all issuer/API-dependent fields as unresolved. Keep all submissions blocked until accepted ingress and capability authority are sourced.
