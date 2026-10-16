# MediaHub OS — Hybrid Distributed Agent Fabric Component Reference Architecture, Wave 11
Date: 2026-10-16
Status: PROPOSED REFERENCE ARCHITECTURE / DOCUMENTATION ONLY / NOT IMPLEMENTED / NOT QUALIFIED
Contour: A — Developer Fabric
Authority: subordinate to accepted Functional Baseline 2.0, accepted domain contracts, canonical component manifest, A0 governance, and explicit authorization boundaries.

## 1. Purpose and decision

Design one composable developer-fabric architecture from narrowly selected capabilities of proven open-source components. Avoid adopting any framework as an indivisible platform. Each component contributes a bounded capability behind a MediaHub-owned contract; the contracts, state authority, admission rules, evidence format, and promotion policy remain MediaHub-owned.

The repository's Wave 08 already establishes a GitHub-centered, ephemeral-worker, PR-first reference fabric, task envelopes, admission/revocation, provider/quota controls, evidence manifests, and CAF-Q-001…CAF-Q-010. Wave 09/10 record Gemini workflow source findings and a successful historical read-only run, while fabric-wide qualification remains open. This wave composes those existing decisions rather than replacing them.

## 2. Architectural rules

1. GitHub is the source-control and review plane, not the sole runtime authority for every long-running workflow.
2. ASTRA A0 remains the engineering coordination/queue boundary. It does not become Product State Authority.
3. Product State Authority alone owns canonical product-state mutation. AI, queues, workflow engines, adapters, and telemetry remain advisory/control-plane services.
4. Workers are ephemeral and capability-scoped. A worker receives a signed, immutable task envelope and a short-lived lease; it receives only the repository paths, permissions, network destinations, and outputs needed for that task.
5. Untrusted model output and patches enter quarantine. No agent output directly merges, deploys, changes infrastructure, modifies secrets, or advances a release state.
6. Every state transition emits provenance: task ID, attempt, source commit, worker image/toolchain digest, policy version, provider/model identifier where relevant, inputs/outputs hashes, timestamps, reviewer, and gate result.
7. Retries are idempotent; leases expire; duplicate delivery is expected; cancellation and revocation are first-class.
8. Fail closed on missing identity, stale evidence, policy ambiguity, target ambiguity, quota exhaustion, signature failure, or conflicting authority.
9. Baseline 2.0 remains the accepted functional reference. Historical Baseline 1.0 is provenance only.
10. This document selects design candidates only. It does not approve installation, workflow edits, tests, provider calls, qualification, deployment, or branch integration.

## 3. Capability composition — take strengths, not whole products

| Capability | Preferred component / source | Reuse only | MediaHub-owned boundary / caveat |
|---|---|---|---|
| Source, review, CI orchestration | GitHub repository, Actions, protected branches, reusable workflows | Event triggers, immutable source refs, job DAGs, PR review and artifact retention | Default-branch immutable-SHA fencing, job-level permissions, explicit secret allowlists, full-SHA action pins, actor/capability/replay checks. GitHub Actions is not the durable system-of-record queue. |
| Durable long-running workflow semantics | Temporal (candidate) | Replay-safe workflow orchestration, durable timers, retries, activity boundaries, resumability | Candidate only; deployment/licensing/operational cost and target fit require evaluation. Temporal workflow state is execution state, never product state. |
| Stateful agent graph / human checkpoints | LangGraph (candidate) | Typed graph transitions, resumable agent state, interrupt/review checkpoints | Use as an optional worker-side planner, not a second global scheduler or policy authority. Persist only approved, minimized state. |
| Reproducible build/test task execution | Dagger (candidate) | Containerized, cache-aware, portable task functions and OpenTelemetry traces | Candidate adapter for build/test reproducibility. Do not permit deployment side effects by default; pin modules/images and constrain mounts/network. |
| Event transport | NATS JetStream (candidate; aligns with Baseline 2.0 candidate bindings) | Durable event delivery, consumer groups, replay and back-pressure | Transport ACK is not evidence of task completion or canonical state commit. Keep message schemas versioned; enforce deduplication and retention. |
| API and typed contract validation | Protobuf/gRPC plus Buf/Protovalidate (existing Baseline 2.0 candidates) | Versioned schemas, compatibility checks, input validation | Admission, lease, heartbeat, result, evidence, revoke and CLOSED contracts are MediaHub-owned. |
| Telemetry | OpenTelemetry Collector | Vendor-neutral collection and routing of traces, metrics and logs | Telemetry is observational only; redact secrets and sensitive payloads, separate audit evidence from sampled telemetry. |
| Artifact and provenance | Content-addressed artifacts + signed evidence manifest; OCI-compatible artifact storage candidate | Immutable references, digest verification, SBOM/provenance attachment | Canonical evidence schema and trust roots remain MediaHub-owned. Artifact existence alone never qualifies a result. |
| Policy enforcement | Small deterministic policy evaluator + signed policy bundle (implementation choice pending) | Explicit allow/deny rules and versioned decisions | Avoid delegating authorization to an LLM. A0 policy and accepted governance remain authoritative. |
| Isolation | Ephemeral hosted runners or isolated containers/VMs, selected per trust tier | Disposable execution, resource ceilings, no ambient credentials | Exact isolation technology depends on accepted target manifest. No privileged host mounts or reusable secrets for untrusted PR/model output. |
| Independent verification | Separate verifier identity and job, source-digest-bound evidence | Independent diff review, schema/security checks, evidence completeness | Must differ from authoring worker identity and credentials. No self-approval. |
| Provider adapter | Narrow provider interface with allowlisted provider/model IDs and per-task egress | Provider portability, quotas, retry classification | Provider selection is policy-bound; no implicit fallback to an unapproved provider. Data handling and R-06 remain open gates. |

Primary public references:
- GitHub Actions secure use: https://docs.github.com/en/actions/reference/security/secure-use
- Reusable workflows: https://docs.github.com/en/actions/how-tos/reuse-automations/reuse-workflows
- Temporal: https://github.com/temporalio/temporal
- LangGraph: https://github.com/langchain-ai/langgraph
- Dagger: https://github.com/dagger/dagger
- OpenTelemetry Collector: https://github.com/open-telemetry/opentelemetry-collector
- NATS: https://github.com/nats-io/nats-server
These are capability references, not proof of MediaHub adoption, approval, installation, or qualification.

## 4. Target logical architecture

```text
GitHub issues / approved triggers
            |
            v
A0 admission boundary ---- policy bundle / actor capability / replay guard
            |
            v
Canonical task envelope + lease + idempotency key
            |
            v
Durable orchestration adapter (Temporal candidate; GitHub Actions for bounded jobs)
            |
            +---- event transport (NATS JetStream candidate)
            |
            +---- ephemeral workers by capability and trust tier
            |       +-- read-only research / source audit
            |       +-- planner / decomposition
            |       +-- isolated patch author
            |       +-- independent verifier
            |       +-- evidence packager
            |
            v
Quarantine: diff + artifacts + signed evidence manifest
            |
            v
Independent review + policy gates + required human/owner approvals
            |
            v
PR / approved promotion transition (never implicit)
            |
            v
GitHub history and evidence ledger

OpenTelemetry Collector observes the system; it cannot authorize transitions.
Product State Authority remains outside this developer-fabric control plane.
```

## 5. Canonical task envelope

Required fields:
- schema_version, task_id, parent_task_id, idempotency_key, attempt, created_at, expires_at;
- issuer identity, requester/actor, capability set, policy bundle digest, approval reference;
- repository, exact base ref and immutable base commit SHA, allowed paths, expected output types;
- worker trust tier, isolation profile, resource/time budget, allowed network destinations;
- provider/model allowlist (empty for tasks without model calls), data classification, retention class;
- acceptance criteria, required independent verifier class, required approval gates;
- cancellation/revocation token reference, lease expiry, heartbeat deadline;
- output artifact digests, source/toolchain image digests, evidence manifest reference.

Validation rules: reject unknown critical fields; require bounded expiry; bind every retry to the same task and policy version unless a new task revision is issued; prohibit a worker from expanding its own capabilities; verify issuer and policy signatures before dispatch.

## 6. Lifecycle and state model

PROPOSED → ADMITTED → LEASED → RUNNING → OUTPUT_QUARANTINED → VERIFIED → REVIEW_PENDING → ACCEPTED_FOR_PR → PR_OPEN → MERGED (only by existing authorized GitHub governance) → CLOSED.

Side states: RETRY_WAIT, CANCEL_REQUESTED, REVOKED, EXPIRED, REJECTED, FAILED, EVIDENCE_INCOMPLETE. Transitions are append-only, actor-attributed and guarded by deterministic policy. A worker may report a result; it cannot set VERIFIED or ACCEPTED itself. Merged is read from GitHub's authoritative state and never inferred from a local action response alone.

## 7. Provider routing and graceful degradation

- Default route: read-only/static tasks use deterministic tools and source retrieval first; model invocation is optional and policy-gated.
- Use per-task provider/model allowlists, explicit destination authorization, payload minimization, bounded retries with jitter, circuit breakers, and cost/quota ceilings.
- Retry transient 429/5xx with bounded exponential backoff; do not retry authorization, schema, signature, policy, or data-classification failures as if transient.
- Failover only among providers already approved for the task's data class and destination policy. No automatic provider expansion.
- Cache only content-addressed, policy-safe results; attach source refs and freshness. Never treat model output as authoritative evidence without independent validation.
- Preserve useful work on provider outage: continue source-only analysis, deterministic validation, document reconciliation, queue hygiene, and evidence assembly.

## 8. Security and trust tiers

T0 — read-only public/source analysis: no secrets, no write permissions.
T1 — private repository read: minimal contents permission, approved context paths only.
T2 — patch author: isolated ephemeral environment, write to task branch only, no merge or deployment authority.
T3 — verifier: separate identity, read-only source plus quarantined artifacts, cannot approve its own author's work.
T4 — privileged promotion: existing authorized human/governance identities only; separate approval and auditable transition.

Required controls:
- pin every third-party Action to a verified full commit SHA;
- set explicit least-privilege GITHUB_TOKEN permissions per job;
- replace broad secret inheritance with per-job secret allowlists;
- bind supervisor execution to approved default-branch immutable SHA before secret access;
- validate actor, capability, task audience, expiry, nonce/idempotency and replay protection;
- keep credentials out of checkout artifacts, logs, prompts, caches and worker outputs;
- treat repository content, issues, PR comments, tool output and model responses as untrusted input;
- constrain egress to explicit destinations and record policy decisions;
- quarantine artifacts and scan/verify them only under separately authorized verification gates;
- provide revocation, cancellation, retention/deletion and incident evidence.

## 9. Component decision register

ACCEPT AS EXISTING PLATFORM BOUNDARY (not blanket acceptance of every feature): GitHub source/review, accepted Baseline 2.0 contract direction, A0 boundary, OpenTelemetry as observational design.

PREFERRED CANDIDATES FOR EVALUATION: Temporal for durable orchestration; NATS JetStream for event transport; Dagger for repeatable isolated task execution; LangGraph for optional stateful agent graphs; Protobuf/gRPC + Buf/Protovalidate for typed contract enforcement; OCI-compatible content-addressed artifacts for outputs.

DEFER / DO NOT DUPLICATE: a second global queue/scheduler inside LangGraph; a second product-state authority; a model-based authorization engine; a general-purpose agent framework with unrestricted tool access; direct model-to-merge; provider fallback without per-task policy.

SELECTION STATUS: Proposed candidates only. No component is considered installed, admitted to the canonical component manifest, or qualified by this report. Existing canonical manifest and its YAML scope relationship remain unchanged pending their governing decision.

## 10. Delivery sequence and gates

Wave A — documentary closure:
1. Resolve exact A0 issuer/lifecycle and approval workflow.
2. Resolve R-06 privacy/data-routing authority and provider eligibility.
3. Obtain an owner-accepted clean target manifest and deployment profile.
4. Reconcile canonical component manifest with YAML consumer/scope without silent normalization.
5. Add the proposed component capability map to the existing traceability matrix with source refs, statuses and acceptance evidence.

Wave B — authorized implementation proposal:
6. Produce exact workflow patch plan for immutable-ref fencing, action pins, permissions, secret allowlists, actor/capability/replay protection, target/executor consistency and evidence schema.
7. Define task-envelope, event and evidence schemas with compatibility rules and stable IDs.
8. Prepare a minimal vertical slice: admission → lease → one read-only worker → quarantine → independent verification → PR draft.
9. Define failure injection and acceptance cases before requesting permission to execute tests.

Wave C — separately authorized execution:
10. Implement only after applicable authorization; run tests/scanners only after explicit permission.
11. Independently verify source digest, security controls, evidence completeness and rollback.
12. Qualify the fabric as a whole only after component-level and end-to-end evidence; keep production and deployment gates separate.

## 11. Acceptance criteria

- Every task has an authenticated issuer, immutable source identity, bounded lease and idempotency key.
- Every worker runs with minimum capabilities and explicit egress.
- Every output is quarantined, digest-bound and independently reviewed.
- No model, queue, workflow engine, telemetry service or adapter can mutate canonical product state.
- Revocation and cancellation stop future work and invalidate stale leases.
- Retries do not duplicate accepted side effects.
- Provider failover respects task-specific policy and data classification.
- Every promotion is attributable to a distinct authorized actor and evidence set.
- Canonical manifest, target profile, A0 governance and R-06 have accepted source evidence.
- End-to-end qualification is independently evidenced and distinct from deployment/production acceptance.

## 12. Current blockers and honest status

- A0 issuer/lifecycle and governance disposition: OPEN.
- R-06 data routing/privacy authority: OPEN.
- Exact owner-accepted target manifest: UNKNOWN / BLOCKED.
- Component manifest/YAML consumer scope: OPEN.
- Gemini: one historical read-only workflow run is verified; broad fabric qualification remains OPEN.
- Durable general-purpose queue, registry, scheduler, isolated patch worker and promotion pipeline: design-level work only unless separate evidence says otherwise.
- Runtime, installation, test, qualification and deployment status: unchanged by this documentary wave.

## 13. Next bounded action

Continue source-bound CAF admission evidence by reconciling the existing canonical component manifest and its YAML consumer, with direct source refs and no silent scope decision. Then update the existing traceability matrix and map only when the full map content can be read and safely preserved. Do not repeat completed Gemini Wave 09 or A0 WB-14AA…WB-14AF work absent new evidence.
