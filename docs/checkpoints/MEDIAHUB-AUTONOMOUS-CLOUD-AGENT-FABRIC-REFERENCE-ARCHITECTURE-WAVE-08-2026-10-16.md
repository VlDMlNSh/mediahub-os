# MediaHub OS — Autonomous Cloud-Agent Development Fabric, Reference Architecture, Wave 08

- Date: 2026-10-16
- ID: MH-CAF-RA-08
- Status: **REFERENCE DESIGN / PROPOSED / NOT ACCEPTED / NOT IMPLEMENTED / RUNTIME-UNVERIFIED**
- Contour: **A — Developer Fabric only**
- Plan of record: [MEDIAHUB-MASTER-DEVELOPMENT-ROADMAP-1.0.md](MEDIAHUB-MASTER-DEVELOPMENT-ROADMAP-1.0.md)
- Navigation authority: [MEDIAHUB-CHAT-TREE-MAP.md](../architecture/MEDIAHUB-CHAT-TREE-MAP.md)
- Functional authority: Functional Baseline 2.0 on `main`; Baseline 1.0 remains historical provenance.
- Companion control artifact: [Unified System Traceability Matrix v0.1](mediahub-unified-system-traceability-matrix-v0.1.md)
- Purpose: define one safe, auditable architecture for admitting cloud agents, registering their capabilities, assigning queued engineering tasks, collecting proposals, verifying evidence and promoting reviewed changes.

## 1. Executive decision

Adopt a **GitHub-centered, ephemeral-worker, pull-request-first developer fabric** as the preferred Contour A target. GitHub is the source-control and durable task/evidence index; a small policy-controlled coordinator owns the engineering queue; each admitted agent receives a bounded task envelope; isolated workers produce branches or patch artifacts; independent checks and human/governance gates control integration. Hosted runners are preferred for bounded jobs where available, avoiding a requirement for an always-on user-owned server. This choice does not imply fixed egress IP, a guaranteed provider processing region, free quota, or runtime availability.

The initial implementation sequence should reuse the repository's existing Gemini read-only audit workflow as a **candidate advisory worker only**, after its context provenance and permissions are qualified. The first production-capable control plane should remain provider-neutral, with an adapter contract rather than a provider-specific orchestration core. Local agents and owned machines can join later through the same admission and evidence contract.

This is a design decision for the next implementation phase. It is not evidence that a queue, agent registry, scheduler, workflow, provider connection or autonomous execution is currently deployed.

## 2. Authority and safety boundaries

1. Contour A engineering state and queue/claim/lease/gate state belong to the accepted ASTRA A0 engineering boundary. Jarvis coordinates missions at the higher level. MediaHub Product State Authority remains the sole authority for canonical product-state mutation.
2. An agent is an untrusted executor/advisor, never an authorization authority. Model output, tool output, retrieved content, task comments and generated patches are untrusted inputs.
3. Default-deny applies to repository writes, network egress, secrets, provider destinations, external tools, artifact publication, workflow dispatch and product-state operations.
4. Each task has an immutable task ID, source repository/ref/commit, allowed paths, expected deliverable, data class, allowed tools/providers, budget/quota envelope, deadline, retry policy, output schema and required reviewers.
5. Every hosted model destination, including each fallback, requires explicit task-level authorization for the same data class and purpose. A quota event never authorizes a new destination.
6. No automatic merge to `main`, no direct product deployment, no secret exposure to agents, no broad write token and no privileged workflow triggered from untrusted generated content.
7. Preserve all gates for security, privacy, R-06 audit policy, A0 issuer/lifecycle, target identity, component admission and independent qualification. Unknown conditions fail closed.

## 3. Reference topology

```text
Owner / governance
        |
        v
GitHub issue or reviewed task manifest
        |
        v
Policy admission + immutable task envelope
        |
        v
ASTRA A0 queue / claim / lease / cancellation / recovery
        |
        +---------------------+----------------------+
        |                     |                      |
        v                     v                      v
Hosted ephemeral       Approved local worker   Read-only advisory
GitHub runner           (future-gated)          model/provider adapter
        |                     |                      |
        +---------------------+----------------------+
                              |
                              v
                 Isolated workspace / patch artifact
                              |
                              v
              Deterministic validation + independent review
                              |
                              v
                  Pull request / evidence manifest
                              |
                              v
             Required checks + human/governance approval
                              |
                              v
                      Authorized integration
```

The diagram describes the target design. Only currently existing repository workflows and artifacts supported by direct GitHub evidence may be marked implemented.

## 4. Component contracts

| Component | Responsibility | Required contract | Initial state |
|---|---|---|---|
| Task Registry | Durable task metadata, dependencies, priority and status | Versioned task schema; immutable source SHA; stable ID collision check | Design |
| Policy Admission | Validate scope, authority, data class, budget, provider allowlist and required gates | Fail-closed decision with reason code and policy revision | Design |
| ASTRA A0 Queue | Claim, lease, heartbeat, cancel, retry, recover and gate task execution | Existing accepted internal lifecycle contract; exact issuer/API remains gated by source reconciliation | Design / interface gate open |
| Agent Registry | Record agent identity, provider, model, runtime, capabilities, supported tools, trust tier and expiry | Evidence-backed registration, versioned capabilities, revocation and health state | Design |
| Worker Adapter | Convert task envelope into provider/runner-specific execution | Provider-neutral interface; strict input/output bounds; no authority inheritance | Design |
| Isolated Workspace | Keep each task's checkout, edits, caches and credentials separated | Ephemeral environment; minimal filesystem/network; clean teardown evidence | Design |
| Quota and Retry Controller | Track provider-specific quota state and bounded retries | Provider/account quota scope; jittered backoff; circuit breaker; no paid fallback | Design |
| Evidence Collector | Bind source, worker, run, outputs and checks | Immutable commit and file digests; timestamps; policy revision; output digest; reviewer | Design |
| PR Promotion Gate | Keep generated work reviewable and isolated from protected branches | PR-only integration; required checks; independent review; explicit merge authority | Design |
| Audit and Privacy Gate | Record operation intent/outcome and enforce retention/data minimization | R-06 governance decision and accepted sink/schema required | Blocked by governance |
| Target Manifest | Define approved runner/worker OS, network, storage, identity and recovery | Exact source/provenance; unknown values remain UNKNOWN | Open |

## 5. Agent admission and authorization lifecycle

`DISCOVERED → CANDIDATE → ELIGIBILITY_REVIEW → REGISTERED_READ_ONLY → TASK_AUTHORIZED → EXECUTION_LEASED → RESULT_QUARANTINED → EVIDENCE_VERIFIED → REVIEWED → PROMOTABLE → REVOKED/EXPIRED`

Transitions are explicit, audited and revision-bound. Provider authorization and task authorization are separate. Registration alone grants no repository write permission, secret access, provider call, workflow dispatch or task claim. Revocation cancels future claims and invalidates leases; in-flight tasks are quarantined pending reconciliation.

Admission record fields:
- `agent_id`, `agent_version`, `provider_id`, `model_id`, `runtime_id`, `capabilities_digest`
- `eligibility_evidence_ref`, `terms_reviewed_at`, `region_and_age_gate_status`, `data_policy_status`
- `allowed_repositories`, `allowed_refs`, `allowed_paths`, `allowed_tools`, `allowed_egress_destinations`
- `credential_mode` (prefer short-lived workload identity; never place raw secrets in the task payload)
- `registration_status`, `expiry`, `revocation_ref`, `reviewer`, `evidence_digest`

For users or accounts whose eligibility is unknown or unmet, the provider remains blocked. Do not attempt to evade age, region, identity, billing or quota controls. Use only providers and features whose terms permit the intended account, purpose and workload.

## 6. Canonical task envelope

Every task must carry:
- stable task ID and collision-check record;
- objective, bounded acceptance criteria and out-of-scope list;
- repository, immutable source commit SHA, allowed branch/ref pattern and allowed paths;
- Baseline 2.0 / domain-contract references and relevant requirement IDs;
- data classification, minimization/redaction rules and egress decision;
- allowed agent IDs/capabilities, provider/model route allowlist and explicit fallback destinations;
- tool allowlist, network policy, filesystem policy, credential mode and permissions;
- concurrency group, lease duration, heartbeat interval, deadline, retry ceiling and cancellation semantics;
- cost/quota ceiling, paid-fallback policy fixed to zero unless separately authorized, and stop conditions;
- expected artifact type, output schema, evidence manifest, required checks and reviewer independence rule;
- final status among `PROPOSED`, `PATCH_READY`, `CHECKS_PENDING`, `REVIEW_REQUIRED`, `ACCEPTED`, `REJECTED`, `CANCELLED`, `EXPIRED`, `QUARANTINED`.

Generated content cannot expand its own task scope or amend the task envelope.

## 7. Queue and scheduler semantics

- Use durable, explicit task states and a transactional claim/lease protocol. Avoid an unbounded in-memory queue as the sole source of truth.
- Each task claim binds agent identity, task ID, source SHA, lease expiry and attempt number.
- Use bounded concurrency by repository, path/domain, provider quota bucket and resource class. Start conservatively; scale only from measured capacity and isolation evidence.
- Apply exponential backoff with jitter for transient errors; honor provider retry guidance; use circuit breakers for repeated quota, authentication or availability failures.
- Distinguish `RATE_LIMIT`, `QUOTA_EXHAUSTED`, `AUTH_FAILED`, `ELIGIBILITY_BLOCKED`, `POLICY_DENIED`, `TRANSIENT_PROVIDER_FAILURE`, `INVALID_OUTPUT`, `WORKER_FAILURE`, `CANCELLED` and `DEADLINE_EXCEEDED`.
- Fail closed on ambiguous authorization, unknown route, missing evidence, output-schema violation, source drift or lease loss.
- Retries must be idempotent or produce a fresh quarantined attempt; a retry must never silently repeat an irreversible action.
- No quota evasion through account/key cycling, identity changes or region changes. Do not switch to a paid route unless a separate approved task policy explicitly permits it.

## 8. Security controls for GitHub-hosted workers

- Set workflow-level permissions to `contents: read` and add individual permissions only to the exact job that requires them.
- Pin third-party actions to verified full-length commit SHAs; use a reviewed allowlist of actions.
- Set `persist-credentials: false` where checkout credentials are unnecessary; keep tokens short-lived and scoped.
- Resolve caller-supplied refs to immutable commit SHAs before execution; record every selected file path and digest. Reject paths outside an explicit allowlist.
- Treat issue comments, PR descriptions, repository content, agent output and model output as untrusted data; never interpolate them into shell code or privileged workflow expressions.
- Separate read-only analysis jobs from write-capable promotion jobs. A write-capable job must consume a reviewed immutable artifact and use an independent promotion decision.
- Keep secrets out of agent context, logs, artifacts and prompt payloads. Never print secret values. Use approved secret names only when explicit authorization and provider eligibility gates are satisfied.
- Avoid `pull_request_target` or equivalent privileged execution over untrusted head code. Use protected environments and explicit reviewers for sensitive operations.
- Publish a provenance manifest containing workflow/run identity, source SHA, action SHAs, agent/provider/model identity, policy revision, artifact digests and check results.
- Retain logs and artifacts according to approved privacy/retention rules. Redact request/response bodies by default.

These are target controls. Existing workflows require source-level qualification before they can be claimed to satisfy the controls.

## 9. Provider and quota routing

The router chooses only among destinations listed in the task envelope. Routing order is policy-driven and may consider capability, eligibility, privacy/data policy, latency, availability and quota. A provider is ineligible when any required fact is unknown.

- Route 0: deterministic local tools and static analysis where the task can be solved without a model.
- Route 1: an admitted read-only advisory worker on an approved hosted runner/provider, with repository context minimized to exact files.
- Route 2: a second provider only when its identity, terms, account eligibility, data policy, quota scope and exact destination were approved before task start.
- Route 3: a human/manual queue or deferred state. Paid fallback remains disabled by default.
- Local-only tasks stop when local capacity is unavailable; they do not silently egress to cloud.
- Record provider/model/endpoint, account quota bucket identifier (opaque, non-secret), data class, policy decision, retry sequence, response status and output digest.
- Provider availability and free-tier limits are volatile. The router must re-evaluate current provider documentation and owner-authorized account evidence before enabling a destination.

## 10. Evidence and promotion gates

Every completed attempt emits an evidence manifest with:
1. task envelope digest and policy revision;
2. repository, immutable source commit SHA and selected file digests;
3. worker/agent/provider/model/runtime identity and version;
4. workflow run ID, job ID, timestamps and attempt/lease identity;
5. allowed tools/egress decisions and sanitized failure classification;
6. output artifact digest, diff summary and path allowlist result;
7. deterministic check results, logs/artifact references and exact revisions;
8. independent review outcome, reviewer identity and conflicts/limitations;
9. promotion decision and resulting commit/PR URL, if applicable.

Promotion ladder:
`DESIGN → IMPLEMENTATION AUTHORIZED → PATCH CREATED → STATIC REVIEW → TEST AUTHORIZED → TESTED → INDEPENDENTLY VERIFIED → QUALIFICATION AUTHORIZED → QUALIFIED → RELEASE AUTHORIZED → RELEASED → DEPLOYMENT AUTHORIZED → DEPLOYED → OBSERVED → ACCEPTED`.

Each transition requires its own evidence and authorization. Passing an earlier gate never implies a later gate.

## 11. Autonomous work queue — documentary seed

These are queued planning items in GitHub documentation only. They are not dispatched to agents, and their presence does not establish a live scheduler.

| Queue ID | Priority | Work package | Prerequisites | Deliverable | State |
|---|---|---|---|---|---|
| CAF-Q-001 | P0 | Reconcile A0 issuer, queue, lease, cancellation, replay and recovery contracts | Exact primary A0 sources; authority review | Accepted interface and lifecycle crosswalk | QUEUED / SOURCE RECONCILIATION |
| CAF-Q-002 | P0 | Complete R-06 audit/privacy schema, sink, outage and retention disposition | Accountable authority, exact governance source | Filled decision record and evidence contract | BLOCKED / GOVERNANCE |
| CAF-Q-003 | P0 | Source-only hardening review of existing Gemini audit workflows | Exact workflow source SHAs and permission map | Job-level threat/control matrix and patch plan | QUEUED / READ-ONLY |
| CAF-Q-004 | P0 | Define task-envelope and agent-registration schemas | CAF-RA-08 plus A0 contract | Versioned schema and collision-checked IDs | QUEUED / DESIGN |
| CAF-Q-005 | P1 | Define immutable evidence manifest and provenance digest | Task schema; evidence-ledger crosswalk | Schema, examples and validation rules | QUEUED / DESIGN |
| CAF-Q-006 | P1 | Resolve provider identities, account eligibility, data policy and quota buckets | Provider terms plus owner-authorized non-secret evidence | Admitted-provider registry | BLOCKED / ELIGIBILITY EVIDENCE |
| CAF-Q-007 | P1 | Define ephemeral runner/workspace isolation and network egress policy | Exact target manifest; security review | Target profile and isolation control matrix | QUEUED / DESIGN |
| CAF-Q-008 | P1 | Define PR promotion policy and independent review gates | Repository governance evidence | Promotion contract and required-check map | QUEUED / GOVERNANCE EVIDENCE |
| CAF-Q-009 | P2 | Define bounded concurrency/capacity and cost envelope | Workload estimates and approved quota evidence | Capacity model and operational SLO proposal | QUEUED / INPUTS UNKNOWN |
| CAF-Q-010 | P2 | Prepare an implementation branch and staged qualification plan | Separate explicit authorization for code/workflow edits and tests | Patch series, rollback map and test plan | BLOCKED / AUTHORIZATION GATE |

## 12. Implementation and qualification sequence

1. Source reconciliation: A0 lifecycle, R-06, target manifest, current Gemini workflows, current matrix and source registry.
2. Contract package: task envelope, agent registry, evidence manifest, provider registry and error taxonomy.
3. Static implementation plan: separate read-only audit worker from any patch-producing worker; define exact paths, permissions and rollback.
4. First authorized implementation slice: one read-only task, one admitted worker, one immutable source SHA, bounded file context, one artifact and no repository write token.
5. Qualification plan: negative tests for path traversal, prompt injection, unauthorized route, stale ref, replay, cancellation, lease expiry, quota exhaustion, invalid output, secret leakage and source drift.
6. Controlled patch-producing slice: isolated branch/worktree, no direct protected-branch write, PR-only output and independent review.
7. Expand providers/workers only after provider-specific eligibility, data policy, quota and egress evidence is accepted.
8. Deployment and Contour B admission remain separately gated by Contour A deployment and independent acceptance.

Steps 4–8 require their relevant explicit authorization. This document authorizes documentation planning only.

## 13. Public source basis reviewed

- GitHub Actions secure use: https://docs.github.com/en/actions/reference/security/secure-use — recommends full-length SHA pinning and security controls for workflow execution.
- GitHub Copilot code review: https://docs.github.com/en/copilot/concepts/agents/code-review — supports review as a distinct step and describes feature/plan availability.
- VS Code agent trust and safety: https://code.visualstudio.com/docs/copilot/agents/agent-tools — workspace trust, sandboxing, approval and review boundaries.
- Gemini API Additional Terms: https://ai.google.dev/gemini-api/terms — age, region and permitted-purpose gates; current terms must be checked before admission.
- GroqCloud data controls: https://console.groq.com/docs/your-data and https://console.groq.com/docs/legal/services-agreement — data handling and service eligibility are provider-specific.
- OpenRouter provider logging: https://openrouter.ai/docs/guides/privacy/provider-logging.mdx and routing: https://openrouter.ai/docs/guides/routing/provider-selection.mdx — provider-specific data policy, logging and fallback configuration.
- These sources describe external product controls and terms. They do not prove MediaHub has enabled or qualified those services.

## 14. Open gates and status

| Gate | State | Closure evidence |
|---|---|---|
| A0 issuer/API/lifecycle | OPEN | Exact accepted primary contract and independent review |
| R-06 audit/privacy | OPEN | Authorized decision record, accepted schema/sink/outage/retention policy |
| Target OS/runner/network/storage | UNKNOWN | Authoritative target manifest and source provenance |
| Provider eligibility/account/quota | UNKNOWN / FAIL-CLOSED | Owner-authorized evidence and current terms |
| Workflow source qualification | OPEN | Exact SHA-bound review and approved remediation |
| Queue implementation | DESIGN ONLY | Authorized code/workflow patch and tests |
| Security/privacy qualification | NOT RUN | Explicit authorization, evidence, independent reviewer |
| Contour A deployment/acceptance | BLOCKED | Deployment record and independent acceptance |
| Contour B product development gate | BLOCKED | Contour A accepted evidence |

## 15. Change control

This design is subordinate to accepted Baseline 2.0, accepted domain contracts, the canonical component manifest and the Master Development Roadmap. Any conflict must be recorded in the existing matrix and resolved through the responsible authority. Preserve historical IDs; collision-check all new stable IDs before promotion. Update the map, roadmap, checkpoint, matrix and source registry together when state changes.

**Result:** one reference architecture and ten documentary queue entries are defined. Runtime enablement, provider connection, code/workflow changes, tests, qualification, deployment and acceptance remain unclaimed.
