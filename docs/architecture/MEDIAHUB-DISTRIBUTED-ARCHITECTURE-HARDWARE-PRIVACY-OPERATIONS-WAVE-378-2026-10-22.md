# MediaHub OS — Consolidated Distributed Architecture, Hardware, Privacy and Operations

- Date: 2026-10-22
- Wave: 378 (architecture consolidation)
- Status: **OWNER-SELECTED DESIGN DECISIONS RECORDED / PROPOSAL / NOT IMPLEMENTED / NOT QUALIFIED / NOT ACCEPTED**
- Canonical navigation: [MEDIAHUB-CHAT-TREE-MAP.md](MEDIAHUB-CHAT-TREE-MAP.md)
- Decision record: [Distributed Compute Architecture Decisions — Wave 378](../checkpoints/MEDIAHUB-DISTRIBUTED-COMPUTE-ARCHITECTURE-DECISIONS-WAVE-378-2026-10-22.md)
- Continuation checkpoint: [current continuation checkpoint](../checkpoints/mediahub-next-continuation-checkpoint-2026-10-12-current.md)
- Master roadmap: [MEDIAHUB-MASTER-DEVELOPMENT-ROADMAP-1.0.md](../checkpoints/MEDIAHUB-MASTER-DEVELOPMENT-ROADMAP-1.0.md)
- Functional reference: [Functional Baseline 2.0](../checkpoints/mediahub-functional-baseline-2.0.md) on `main`
- Control-plane tracker: [Issue #301](https://github.com/VlDMlNSh/mediahub-os/issues/301)

## 1. Purpose and authority

This document consolidates the owner-selected architecture decisions from the 2026-10-22 discussion, including physical hardware, model placement, task queues, networking, resource scheduling, privacy, backup/recovery, updates and observability.

It is a design record, not proof of implementation. Functional Baseline 2.0 remains the accepted, immutable functional reference. Baseline 1.0 remains historical provenance. This document does not change either baseline, issuer/capability contracts, governance gates, historical identifiers, or the authority boundaries of Jarvis, ASTRA GOLD A0 and MediaHub Product State Authority.

Statuses are deliberately distinct: **DECIDED BY OWNER**, **PROPOSED DEFAULT**, **OPEN**, **NOT RUN**, **NOT VERIFIED**, **NOT QUALIFIED**, and **NOT ACCEPTED**. A design statement must not be reported as an implemented or production-ready capability.

## 2. Authority and control topology

- **Owner / governance** defines policy and grants permissions.
- **Jarvis** receives requests and routes straightforward media tasks to suitable local capabilities. It may originate a complex engineering mission but is not a replacement for ASTRA GOLD A0.
- **ASTRA GOLD A0** decomposes complex engineering missions, coordinates bounded subtasks and verifies their results under its accepted authority contract.
- **GitHub Supervisor / approved controller** provides the engineering execution control plane: approved dispatch, task status, leases/cancellation/recovery where implemented, and durable evidence. It does not replace A0 as mission decomposition authority.
- **Model agents and worker processes** are untrusted executors/advisors. Their outputs do not authorize themselves, grant capabilities, merge code or mutate canonical product state.
- **MediaHub Product State Authority** remains the sole authority for canonical product-state mutation.
- **Local media control plane** owns the separate local media queue and local operational telemetry within admitted node capabilities.

No flat global resource pool is implied. The local user/media domain and cloud developer domain remain separate trust and data domains. Contour B must not be deployed merely because Contour A has progressed.

## 3. Physical hardware and intended placement

The following is the current planning inventory from the discussion and historical project context. Unknown values are intentionally not inferred; all current availability and capability claims require fresh inventory before execution.

| Node / resource | Known facts | Intended role (planning) | Limits / status |
|---|---|---|---|
| Mac mini 2018 | 6 CPU cores; RAM capacity is not yet verified | Home coordination and Jarvis-related services; light local orchestration | Do not assume it can host a large model until RAM, storage, thermals and runtime are measured |
| Mac mini 2011 | 4 CPU cores, 16 GB RAM, clean Linux installation | Background builds, tests, maintenance and light jobs | Treat as CPU/RAM-limited; no claim of GPU inference qualification |
| `Voktors-Mini.Dlink` (third server) | Historical inventory identifies macOS ARM64; prior records observed Ollama client but a later bounded probe did not find a reachable Ollama server | Separate local executor lane, subject to explicit host/capability/route verification | Current runtime, models, Claude CLI, browser tooling and qualification are NOT VERIFIED; never use this node to transport or launch Gemini |
| Future media server | Owner budget approximately 100,000 RUB; not purchased/qualified in this record | Dedicated media processing and, if qualified, local model inference | Candidate configuration only: Ryzen 5 5600, NVIDIA RTX 3060 12 GB VRAM, 32 GB RAM upgradeable to 64 GB, 1 TB NVMe, compatible PSU/cooling/case/motherboard |

### Hardware sizing rules

1. The future server specification is a **candidate**, not a final bill of materials or performance guarantee. Validate current prices, GPU dimensions/power, PSU quality and headroom, cooling, motherboard/BIOS compatibility, memory configuration, NVMe capacity, case airflow and the intended OS/runtime before purchase.
2. RTX 3060 12 GB VRAM can be a practical entry point for selected local inference and GPU-accelerated media workloads, but does not imply every model, context size, video pipeline or concurrent workload will fit. RAM and VRAM are separate resource pools.
3. 32 GB system RAM is the proposed starting point; 64 GB is a possible upgrade after workload measurements. The 1 TB NVMe is a starting allocation, not unlimited model/media storage.
4. The installer must expose a visible, bounded disk quota for model assets, cache and temporary operation data. It must not repartition disks automatically or consume arbitrary free space.
5. Quantization and selective/streamed loading or offload are different techniques. Combine them only when the chosen model format and runtime explicitly support the combination.
6. Before assigning work, collect CPU architecture/core count, RAM, GPU/VRAM, disk free space, runtime/model versions, thermals/power constraints, node identity, network route and current health. Missing inventory means the node is not eligible for a task that depends on it.
7. Numeric scheduler thresholds are OPEN until representative workloads are benchmarked. Do not invent latency, throughput or capacity targets.

## 4. Model registry and artifact placement

GitHub stores the model catalog, version manifests, policy metadata and references to approved artifacts. Large model weights should not be placed in ordinary Git history. Git LFS or package/artifact storage is an option only after size, licensing, quotas, retention and cost are validated.

Model records should include stable model ID, exact version/revision, artifact digest, license, source, format/quantization, supported runtimes, hardware/resource profile, data-policy constraints, known limitations, qualification evidence and allowed task classes.

Track these as separate states:
- catalog entry exists;
- artifact is available on an approved source;
- artifact exists on a particular node;
- integrity is verified;
- model is loaded;
- model is active for a task;
- exact model/runtime/hardware/task combination is qualified.

Replicate popular models to appropriate nodes when capacity and policy permit. Keep heavy or rarely used models on suitable storage/compute nodes rather than duplicating them everywhere. Model presence never grants execution permission. Revoked, incompatible or unqualified versions must not receive new tasks.

## 5. Execution and queue topology

- GitHub issues/manifests, approved GitHub Actions and their artifacts form the primary durable coordination/evidence path for engineering work.
- Media jobs use a distinct local queue so local processing can continue during GitHub outages.
- Both queue types share task identity conventions, data classification, authorization semantics, bounded resource budgets, cancellation semantics, provenance and result-verification principles. They must not blindly mirror all queue state or user media.
- GitHub Actions is an ephemeral bounded execution surface, not a permanent dispatcher or unlimited GPU service. Hosted GPU capacity, provider availability, free quota, fixed egress IP and provider region must not be assumed.
- Gemini runs exclusively through the approved `.github/workflows/gemini-batch-dispatch-controller.yml` and its governance/security gates. This document does not authorize a run or waive a blocker.
- Never route Gemini through the third server, SentinelX, local CLI or an alternate transport. Do not launch Claude Code on the third server without fresh host identity/capability/allowlist checks and a qualified approved route without paid fallback.
- No direct provider calls outside approved routing, no automatic merge to `main`, no direct production deployment, and no broad write token passed to model workers.

A task envelope should bind a stable task ID, immutable source SHA when applicable, allowed paths, task/data class, permitted tools and provider/model routes, issuer/capability, policy revision, quota/budget limits, deadline, bounded retry rules, expected outputs, acceptance criteria and required independent review.

## 6. Networking and disconnected operation

Default networking is outbound protected connections with no public inbound listener. A private network may be used for specifically authorized owner-controlled node-to-node transfers, including large media artifacts, only when identity, issuer/capability, destination policy, lease/fencing, least privilege, revocation and audit are enforced. Private-network reachability is not authorization.

Transfer evidence should record task ID, source and destination node identities, artifact digest, policy decision, byte/result metadata where safe, and outcome without copying the media payload into GitHub.

When GitHub is unavailable, a local queue may continue only tasks that were already fully authorized and remain within a valid lease, data-egress policy, resource quota and budget. New privileged work and new cloud dispatches stop. Outputs remain locally staged as awaiting reconciliation until the approved control path returns. Conflicting states are reconciled before acceptance.

## 7. Resource scheduling and protection

Owner-selected policy: adapt performance against memory economy while protecting interactive tasks.

| Priority | Work class | Scheduling intent |
|---|---|---|
| P0 | Interactive Jarvis requests | Protect responsiveness; reserve suitable resources |
| P1 | Normal user tasks | Run within admitted capability and user-facing limits |
| P2 | Background engineering, builds and tests | Throttle/defer under pressure |
| P3 | Batch, indexing, maintenance and model housekeeping | Lowest priority; pause when necessary |

Proposed resource modes are `NORMAL`, `CONSTRAINED` and `PROTECTIVE`, with hysteresis to avoid rapid oscillation. Under pressure, defer background jobs before degrading interactive work, avoid starvation, and unload/reload models only when safe and supported.

Measure queue age, end-to-end latency, throughput, CPU, RAM, GPU utilization, VRAM, disk pressure, model load/unload time, cache hit rate, failures, retries, provider quota and cost. Establish numerical thresholds only from actual hardware and workload baselines.

Priority never bypasses authorization, privacy, safety, quota, cost or hard resource limits.

## 8. Strict local-first privacy policy — OWNER DECISION

User-selected rule: **user media and detailed local logs remain on owner-controlled nodes; only explicitly authorized data and necessary engineering evidence may leave that boundary.**

Conservative data classes:
- **D0 — public technical data:** public specifications and approved public source content, excluding secrets and private data.
- **D1 — internal technical data:** internal configuration and sanitized technical context; external transfer only through an approved route and scope.
- **D2 — user media/private content:** photos, video, audio, personal documents, private metadata and derived content. Local by default; cloud processing denied unless a specific task-level authorization explicitly permits the required data and destination.
- **D3 — secrets and authority material:** API keys, tokens, private keys and credentials. Never place them in prompts, artifacts, repository content or agent-visible task payloads; use only dedicated protected runtime injection when authorized.

For every boundary-crossing operation, validate purpose, exact source and recipient, minimum data fields/files, classification, issuer/capability, policy version, lease/expiry, destination, quota/cost, retention/deletion terms and audit evidence. If classification or authorization is missing/ambiguous, fail closed. A hash can itself leak information in some contexts and is not a universal privacy guarantee.

No user media, raw private logs or credentials are to be added to GitHub by this documentation change. Detailed operational telemetry stays local; only minimized, sanitized, necessary engineering evidence is published.

## 9. Backup and restore — OWNER DECISION

Owner-selected strategy: encrypted backups on owner-controlled nodes, keys stored separately from backup media, integrity checks and periodic restore tests.

- Separate backup sets by data class and recovery purpose: system configuration, model manifests/artifacts, user media, queue/task metadata and audit logs.
- Keep encryption keys and recovery material outside the backup location; restrict access and document the recovery authority path. Key loss must be treated as a real recovery risk, not assumed away.
- Verify checksums and archive readability; periodically perform isolated restore tests and record date, source copy, tool/procedure version, integrity result, recovered scope and losses.
- Restore into quarantine first. Verify configuration, artifact digests, node identity, current policy and authority before returning the node to service.
- Do not blindly resume a restored queue. Revalidate lease/fencing, expiry, prior output, idempotency and side effects. Ambiguous jobs remain quarantined until reconciled.
- Offsite/cloud backup is not implicitly authorized by the word “backup”; it requires a separate data-egress policy decision.

## 10. Staged updates and rollback — OWNER DECISION

Owner-selected strategy: staged updates with automatic compatibility and provenance checks, mandatory gates, controlled activation and rollback.

1. Resolve a version and verify source, signature/provenance where available, immutable digest, license and supply-chain policy.
2. Check compatibility with OS, architecture, hardware, model format/runtime, data schemas, contracts and dependent services.
3. Stage the update without replacing the known-good active version; run deterministic tests and the required security/contract checks.
4. Activate only after mandatory gates pass and the authorized promotion decision is present. A successful download or signature alone is not sufficient.
5. Monitor health and compare behavior to the qualified baseline; stop promotion on regression.
6. Roll back to a known-good version when the rollback path is compatible and data migrations are reversible. Irreversible migrations require a separate tested recovery plan.
7. Record old/new version and digests, source, policy revision, checks, approver/gate, activation time, observed result and rollback evidence.

Updates may be downloaded and prepared automatically, but must not auto-promote an unverified version or change canonical product state without the proper authority.

## 11. Adaptive recovery and idempotency

Before retry, resume or migrate a task, the Recovery Manager checks:
1. lease validity and fencing, preventing stale workers from acting;
2. whether execution already completed and whether a valid output exists;
3. whether the operation is idempotent, deduplicated or explicitly reconciled;
4. whether the replacement executor supports the same model/runtime, hardware, data class, route, artifact and reproducibility requirements.

A lost acknowledgement is not proof of failed execution. If state or side effects are ambiguous, quarantine rather than blindly duplicate. Retries are bounded, use the approved budget/quota and never imply paid fallback.

Each attempt records task ID, attempt ID, reason, source/target executor, lease state, prior result state, idempotency evidence, compatibility decision, policy revision and final status.

## 12. Hybrid observability and evidence

- Detailed operational telemetry remains local: CPU/GPU, RAM/VRAM, queue depth/age, model loading, latency, errors, retry behavior, cache, disk and provider quota/cost.
- GitHub contains source-bound engineering evidence and minimized reports: target SHA, workflow/run/job IDs, tool/test versions, result status, artifact digests and independent review.
- Correlate local and engineering streams using stable task/attempt/node/model/artifact IDs without copying private media.
- Keep operational metrics, security audit trail and qualification evidence logically distinct. Metrics do not prove authorization; an audit record does not grant authority.
- Use bounded local audit buffering with sequence/checksum and explicit retention, rotation and disk-full policy. Missing records mean evidence is incomplete, not that an action did not happen.
- If local and GitHub states conflict, reconcile before accepting the result.

## 13. State model and promotion gates

Keep these states distinct: `PLANNED`, `AUTHORIZED`, `DISPATCHED`, `RUNNING`, `EXECUTED`, `SUCCEEDED`, `VERIFIED`, `QUALIFIED`, `ACCEPTED`, `NOT RUN`, `BLOCKED`, `FAILED`, `NOT VERIFIED`, `QUARANTINED`.

No state is inferred from an empty tool result, missing run, green unrelated CI, a successful dispatch alone or the existence of documentation. Model output is not an approval. Product-state mutation, merge, deployment and qualification remain separate gates.

## 14. Implementation sequence and acceptance evidence

1. **Inventory and contract reconciliation:** refresh all node IDs, hardware capabilities, RAM/VRAM/storage, runtime versions, current health and authorization allowlists. Reconcile A0 issuer/ingress/lease/cancel/recovery and R-06 privacy/audit gates.
2. **Privacy and evidence contracts:** machine-readable data classification, task-level egress allowlist, redaction tests, retention policy and negative fixtures.
3. **Queue/recovery contracts:** schema validation, lease/fencing, cancellation, idempotency and restart/reconciliation tests for local and engineering queues.
4. **Model registry and storage:** version/digest/license/runtime/hardware metadata, bounded installer quota, local replica verification and revocation tests.
5. **Resource baselines:** benchmark representative media and engineering workloads on each actual node; establish thresholds and concurrency limits from evidence.
6. **Backup/update qualification:** encrypted backup/restore drill, key recovery drill, staged update and rollback drill including failed gates and incompatible artifacts.
7. **Contour A qualification:** immutable target, approved controller path, exact-head CI, independent review, source-bound artifact digests and actual runtime evidence. Gemini remains NOT RUN unless the approved controller gates pass.
8. **Contour B:** only after Contour A is deployed and independently accepted, under its own product and privacy gates.

Acceptance evidence must identify exact source refs/blob SHAs, node identity/capabilities, test tool versions, run/job IDs where applicable, artifact digests, failures and unresolved blockers. Documentation alone is not runtime qualification.

## 15. Architecture decisions from this discussion

**Owner-selected:**
- strict local-first privacy; explicit task-level exceptions for outbound data;
- encrypted backups on own nodes, separated keys, integrity checks and periodic restore tests;
- staged updates, automated compatibility/provenance checks, mandatory gates, controlled activation and rollback;
- GitHub engineering queue separate from local media queue;
- hybrid networking: protected outbound default plus explicitly authorized private-node transfers;
- hybrid observability: detailed local telemetry, minimized engineering evidence in GitHub;
- adaptive recovery based on lease, existing result, idempotency and executor compatibility;
- adaptive scheduling with P0–P3 priorities protecting interactive work;
- model catalog/manifests in GitHub and permitted model artifacts replicated locally, without large weights in ordinary Git history.

**Planning facts / not yet qualified:**
- Mac mini 2018, 6 cores, RAM unknown;
- Mac mini 2011, 4 cores, 16 GB RAM, Linux;
- Voktors-Mini.Dlink, historical macOS ARM64; current runtime qualification NOT VERIFIED;
- future media server budget about 100,000 RUB; candidate Ryzen 5 5600 / RTX 3060 12 GB / 32 GB RAM upgradeable to 64 GB / 1 TB NVMe. No purchase decision or performance qualification is claimed.

**Open until measured or separately approved:**
- actual RAM and storage of the 2018 Mac mini and exact third-node capabilities;
- final media-server parts list and real prices;
- model-specific memory, throughput and concurrency limits;
- retention periods and recovery-point/recovery-time objectives;
- any external/offsite backup destination;
- numeric performance thresholds and production acceptance criteria.

## 16. Persistent documentation synchronization

For each future architecture-changing `/next`, the maintainer must:
1. re-read the canonical map, Bootstrap, current checkpoint, Master Roadmap, Baseline 2.0 and relevant contracts from current refs;
2. distinguish owner decisions from proposals and runtime evidence;
3. update the dated report, map/index or map addendum, continuation checkpoint, Master Roadmap and machine-readable context when materially changed;
4. re-read changed files, record blob/commit SHA, validate JSON and links, and report exact-head CI/review status;
5. preserve open PRs and canonical-vs-working branch boundaries; do not claim a proposed PR is canonical before merge.

This is a repository workflow instruction, not a background synchronization daemon. Continuous/background synchronization is not claimed unless a separate automation is implemented, authorized and verified.

## 17. Current evidence disposition

- Documentation changes only.
- Runtime code, model weights, installer, server configuration, provider settings, secrets and workflows were not changed by this architecture record.
- No model inference, media processing, benchmark, Gemini batch or local executor task was initiated by this record.
- Implementation: **NOT IMPLEMENTED by this record**.
- Runtime verification: **NOT RUN**.
- Qualification: **NOT QUALIFIED**.
- Acceptance: **NOT ACCEPTED** pending review, required checks, reconciliation with related open documentation PRs and merge.
