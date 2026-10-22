# MediaHub OS — Distributed Compute Architecture Decisions, Wave 378

- Date: 2026-10-22
- Status: **OWNER-DIRECTED ARCHITECTURE DECISIONS RECORDED / DESIGN ONLY / NOT IMPLEMENTED / NOT QUALIFIED / NOT ACCEPTED**
- Scope: distributed compute, model placement, queue separation, resource scheduling, recovery and hybrid observability.
- Contour: architecture across Contour A engineering execution and local MediaHub compute; this record does not authorize crossing existing contour or data-policy boundaries.
- Canonical navigation: [MEDIAHUB-CHAT-TREE-MAP.md](../architecture/MEDIAHUB-CHAT-TREE-MAP.md)
- Map addendum: [Wave 378](../architecture/MEDIAHUB-CHAT-TREE-MAP-ADDENDUM-WAVE-378-2026-10-22.md)
- Related tracker: [Issue #301 — Contour A cloud-agent development fabric](https://github.com/VlDMlNSh/mediahub-os/issues/301)
- Related pending architecture context: [PR #485 — Wave 362 distributed compute/context state](https://github.com/VlDMlNSh/mediahub-os/pull/485)

## 1. Purpose and decision status

This report records decisions made in the owner-directed architecture discussion. It is not evidence of implementation, runtime behavior, qualification, deployment or acceptance. Functional Baseline 2.0 on `main` remains the accepted immutable functional reference. No baseline, governance contract, issuer/capability gate or Product State Authority boundary is changed by this report.

Decision status in this report:
- **DECIDED**: explicitly selected by the owner in this discussion.
- **PROPOSED DEFAULT**: architecture recommendation, not yet independently accepted as a normative contract.
- **OPEN**: needs specification or verification before implementation.
- **NOT IMPLEMENTED**: no runtime code or infrastructure was changed by this record.

## 2. Owner-selected architecture decisions

### 2.1 Model catalog and artifact placement — DECIDED

- GitHub stores the model catalog, version manifests, policy metadata and references to approved artifacts.
- Permitted model weights are replicated locally onto suitable servers.
- Do not store large model weights in ordinary Git history. Git LFS or package/artifact storage may be used only after artifact size, license, quota and cost are checked.
- Model records distinguish catalog presence, local disk presence, integrity verification, loaded state, active use and task-specific qualification.
- Adaptive replication is preferred: popular models may be replicated to suitable nodes; heavy or infrequently used models should be placed where resources and policy permit.

### 2.2 Cloud inference and engineering execution — DECIDED WITH EXISTING GATES

- Approved model APIs may be called from GitHub Actions for bounded engineering tasks.
- GitHub Actions is an ephemeral execution/control surface, not an unlimited persistent GPU fleet. Paid runners or paid provider routes require explicit authorization and verified budget.
- Provider availability, free quota, region, fixed egress IP and inference capability must not be assumed.
- Gemini execution remains exclusively behind the approved repository controller and its mandatory governance/security gates. This architecture record does not authorize dispatch or waive a blocked gate.
- No paid fallback, proxy/VPN, region spoofing or alternate transport that bypasses approved routing.

### 2.3 Queue topology — DECIDED

- GitHub is the primary durable queue/control/evidence path for engineering tasks.
- Local media tasks use a separate local queue so media processing can continue when GitHub is unavailable.
- The queues share task identity, envelope semantics, policy checks, cancellation semantics, provenance and evidence conventions, but they do not blindly mirror full queue state.
- Jarvis routes incoming requests; ASTRA GOLD A0 decomposes complex engineering work and owns task-level coordination; the GitHub Supervisor/controller provides approved execution, lease, status and evidence functions.
- Agents remain untrusted executors/advisors. MediaHub Product State Authority remains the sole canonical product-state mutation authority.

### 2.4 Networking — DECIDED

- Default: outbound protected connections with no public inbound listener.
- A private network is allowed for specifically authorized node-to-node operations, such as transfers of large media artifacts between owner-controlled nodes.
- Private-network reachability is not authorization. Node identity, issuer/capability, least privilege, task scope, destination policy, lease/fencing, revocation and audit apply to both public egress and private-network paths.
- Transfer records should capture task ID, source/destination node identities, artifact digest, policy decision and outcome.
- If GitHub is unavailable, a local queue may execute only work that was already fully authorized and remains within a valid lease, data policy, resource quota and budget. Results stay local as awaiting confirmation until the approved control path returns.

### 2.5 Resource scheduling — DECIDED AT POLICY LEVEL

- Select an adaptive balance between performance and memory economy, protecting interactive work.
- Priority classes: P0 interactive Jarvis queries; P1 normal user tasks; P2 background engineering jobs; P3 batch/maintenance.
- Suggested resource modes: `NORMAL`, `CONSTRAINED`, `PROTECTIVE`, with hysteresis to avoid oscillation.
- Under pressure, defer or throttle background jobs before degrading interactive work; protect active models where practical and avoid starvation.
- Priority never bypasses safety, authorization, data policy, hard resource ceilings, budget or quota limits.
- Numeric thresholds remain OPEN until actual hardware and workload baselines are measured.

### 2.6 Adaptive recovery — DECIDED

Before retry, resume or migrate a task, Recovery Manager must check:
1. **Lease and fencing:** authority remains valid; stale executors cannot continue acting under expired authority.
2. **Result state:** determine whether execution actually completed and whether an output already exists and validates. Lost acknowledgement is not proof of failed execution.
3. **Idempotency:** retry only when repeated effects are known to be safe, deduplicated or explicitly reconciled.
4. **Executor compatibility:** validate model/version, hardware/resource fit, data class, approved route, artifact availability and required reproducibility.

If result state, authority or side effects are ambiguous, fail closed into quarantine/manual resolution rather than launching a blind duplicate. Retries must be bounded and obey budget/quota. No paid fallback is implicit.

### 2.7 Hybrid observability — DECIDED

- Detailed operational telemetry remains local to the executing nodes/control plane where feasible.
- Engineering evidence, source-bound manifests, qualified reports and relevant status records are indexed in GitHub.
- A shared set of task, attempt, node, model-version and artifact identifiers correlates the streams without copying unnecessary private media data.
- Keep three logical streams distinct:
  - operational telemetry (latency, queue age, CPU/GPU, RAM/VRAM, model load state, failures, retries, quota and disk cache);
  - audit trail (issuer/capability decision, policy version, lease, state transitions, executor choice and recovery decision);
  - evidence store (artifact digests, source SHA, model versions, validation outcomes and review records).
- Retention differs by stream and must be policy-defined. Do not put secrets, raw credentials or unnecessary user media into logs, GitHub artifacts or prompts.

## 3. Shared task and model lifecycle conventions

### Engineering task envelope

The envelope should carry a stable task ID, immutable target SHA where applicable, task type, allowed paths, permitted model/provider routes, data classification, resource/budget/quota ceilings, deadline, bounded retry policy, deliverables, acceptance criteria, cancellation state and required review policy.

### Local media task lifecycle — PROPOSED DEFAULT

`SUBMITTED → VALIDATED → QUEUED → RESERVED → RUNNING → OUTPUT_VALIDATION → COMPLETED`

Additional explicit states should cover `BLOCKED`, `WAITING_RESOURCES`, `WAITING_APPROVAL`, `CANCELLED`, `FAILED` and `QUARANTINED`. A terminal status must not be inferred from a worker process disappearing.

### Model lifecycle — PROPOSED DEFAULT

`DISCOVERED → DOWNLOADED → INTEGRITY_CHECKED → QUALIFIED → STAGED → ACTIVE`

Catalog registration does not grant permission to execute. Qualification is tied to model version/hash, runtime, hardware profile, task class, data policy and test evidence; revoked or incompatible versions must be prevented from new scheduling.

## 4. Privacy, security and authority invariants

- Project technical specifications may be versioned in GitHub; actual user media is a separate data class and must not be uploaded to GitHub or external model APIs without an explicit approved data policy.
- Provider/model routing must check data classification and the allowed destination before dispatch.
- The model agent cannot grant itself capabilities, approve its own result, authorize product-state mutation or promote its own changes.
- No secrets in prompts, logs, artifacts, task envelopes or repository files.
- No automatic merge to `main`, production deployment or canonical product-state mutation from an untrusted agent result.
- Evidence status labels remain distinct: `PLANNED`, `DISPATCHED`, `RUNNING`, `SUCCEEDED`, `VERIFIED`, `QUALIFIED`, `ACCEPTED`, `NOT RUN`, `BLOCKED`, `FAILED`, `NOT VERIFIED`.

## 5. Remaining architecture work — bounded

The next architecture work is limited to three consolidated passes, not an open-ended sequence of preference questions:

1. **Privacy and observability contract:** data classes, telemetry redaction, retention, evidence publication and correlation identifiers.
2. **Reliability and operations contract:** node loss, backups/recovery, model updates/rollback, disconnected operation and failover without duplicate side effects.
3. **Consolidation and acceptance matrix:** resolve cross-document conflicts, label owner decisions vs proposed defaults, and define measurable qualification tests.

Hardware-specific resource thresholds and provider-specific quotas remain OPEN until measured; they must not be invented to make the architecture appear complete.

## 6. Evidence and current status

- This is a documentation-only architecture record.
- No runtime code, installer, queue, scheduler, model registry, worker, network, server or provider configuration was changed.
- No model inference, media processing, benchmark, CI run, Gemini dispatch or local executor task was started by this record.
- Implementation: **NOT IMPLEMENTED**.
- Runtime verification: **NOT RUN**.
- Qualification: **NOT QUALIFIED**.
- Acceptance: **NOT ACCEPTED**.
- Canonical map remains on the separate documentation branch. This proposal must not be described as canonical until the documentation PR is reviewed, its required checks are verified and it is merged.
