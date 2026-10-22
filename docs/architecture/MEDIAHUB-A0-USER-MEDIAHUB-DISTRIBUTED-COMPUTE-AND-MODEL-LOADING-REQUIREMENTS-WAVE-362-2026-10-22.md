# ASTRA GOLD A0 — User MediaHub Distributed Compute and Model Loading Requirements

- Date: 2026-10-22
- Wave: 362
- Status: **OWNER-DIRECTED DESIGN REQUIREMENTS / IMPLEMENTATION NOT VERIFIED / NOT ACCEPTED**
- Scope: architecture contract proposal for A0 task routing, GitHub Supervisor execution services, user-owned MediaHub compute nodes, model loading and reserved storage.
- This document does not supersede Functional Baseline 2.0, the A0 issuer/task contracts, or the binding Wave 272/273 requirements. Reconcile all implementation work with those sources first.

## 1. Canonical responsibility model

1. A large task may originate in ChatGPT or Jarvis.
2. ASTRA GOLD A0 is responsible for decomposing the large task into a dependency graph, selecting eligible execution pools, assigning bounded subtasks, tracking lifecycle and assembling verified results.
3. Eligible pools are:
   - admitted cloud executors;
   - admitted user-owned MediaHub compute nodes;
   - separately qualified local executors.
4. GitHub Supervisor provides execution/control-plane primitives such as durable-enough queue operations, dispatch, monitoring, retry/recovery, cancellation and evidence collection according to its actual qualified contracts. It must not become a competing decomposition authority or Product State Authority.
5. A user-owned MediaHub contributes explicitly admitted compute capacity. Enrollment does not grant the corporation unrestricted access to its filesystem, credentials, user data or product-state authority.
6. Product State Authority remains separate from Jarvis and A0. Execution capability is not authority to commit canonical product state.

## 2. User MediaHub admission and task boundary

Each node must have a unique identity and an explicit, revocable admission record. Before assigning a task, A0/Supervisor must establish:

- identity and protocol compatibility;
- owner consent and admitted scope;
- available CPU, RAM, VRAM, disk, bandwidth and relevant runtime capabilities;
- allowed model families, model/license constraints and data-egress policy;
- per-task disk, memory, time, energy and concurrency budgets;
- credential isolation, issuer/capability checks and revocation state.

Every task envelope should bind an immutable target/artifact reference, task ID, dependency IDs, allowed operation, resource budget, expiration/lease, data-handling policy and expected evidence. Workers must reject expired, unsigned, out-of-scope or over-budget tasks. Duplicate delivery must not silently cause duplicate side effects.

## 3. Quantization, selective loading and model execution

The design target is to make modest user-owned MediaHub devices useful for demanding tasks by combining the largest suitable model with a compatible execution strategy. This is a target to qualify, not a claim that every large model can run on every device.

### 3.1 Distinct mechanisms

- **Quantization** stores model weights at a lower numerical precision (for example, supported 8-bit or 4-bit formats), often reducing memory and storage requirements. Quality, compatibility and throughput must be measured for the selected model/runtime.
- **Selective/streamed loading and offload** keep only the layers, tensors, blocks or other components needed at a given stage resident in RAM/VRAM when supported by the architecture and runtime. Other weights may remain in the reserved disk cache or be staged as required.
- **Sparse/MoE execution** may activate only part of a model for a token/task, but its storage and runtime behavior depend on the implementation; it must not be assumed to eliminate the need to store all required model assets.
- Disk-backed offload can make a model feasible under tighter memory limits, but may cause significant I/O latency. A0 must route according to measured feasibility, not advertised parameter count.

Quantization alone does not mean only a subset of a model is loaded. The implementation may combine quantization with layer/tensor streaming, offload, sparse execution or other supported runtime features.

### 3.2 Task-time model staging

For an admitted task, the executor should:

1. Resolve the task's model/runtime requirement and verify license, integrity, provenance and permitted data route.
2. Check that the node's reserved disk budget and available RAM/VRAM meet the runtime's measured minimums.
3. Fetch or reuse only authorized model artifacts; verify checksums/signatures before use.
4. Stage model components into the node's designated operation space.
5. Load only the components required by the runtime's execution plan into RAM/VRAM, to the extent supported.
6. Execute within the task's time, compute, energy and storage budgets.
7. Return output plus provenance and measurements; release transient resources and apply the approved cache-retention/eviction policy.

A0 must be able to choose a smaller compatible model, another admitted node or a cloud executor if the requested model is not feasible. It must not bypass quota, licensing, consent, route or billing restrictions to force execution.

## 4. Installer-reserved disk space

The user MediaHub installer must reserve or configure a dedicated, user-visible disk budget for model assets, staging, cache and temporary task data.

Required design controls:

- show the requested size, purpose, free-space impact and retention behavior before committing the reservation;
- use a configurable quota with a safe default and minimum free-space guard;
- never silently reserve unbounded storage or consume user data outside the designated area;
- enforce per-task and aggregate quotas, including concurrent tasks;
- verify free space before downloading/staging; fail closed if the budget is insufficient;
- distinguish persistent verified model cache from task-temporary data;
- clean temporary files after success, cancellation, timeout and crash recovery, subject to forensic/evidence retention rules;
- use bounded LRU/priority eviction only for reconstructible cached assets; never delete user-owned files or required audit evidence;
- provide owner-visible controls to resize, clear cache, pause compute participation and revoke the node;
- protect model and task files with filesystem permissions and integrity checks.

“Reserved” means a managed, bounded allocation or quota in the installer-selected location; it does not automatically imply a dedicated physical partition. Partitioning is a separate product/OS decision and must not be performed without explicit consent and platform-specific safety design.

## 5. Resource-aware scheduling

A0 should schedule based on a capability manifest and live measurements, not only CPU/GPU labels. At minimum evaluate:

- model/runtime minimum RAM and VRAM, including context/KV cache and temporary buffers;
- available disk quota and model artifact size;
- compute throughput and estimated I/O overhead;
- network transfer cost/latency and data-residency restrictions;
- task deadline, dependencies, energy/thermal budget and owner-defined idle/availability policy;
- quantized-model quality requirements and reproducibility expectations.

Before routing, the scheduler must produce a decision record explaining eligible candidates, rejected candidates and the selected route. Unknown or stale measurements should lower confidence or block dispatch where safety/correctness depends on them.

## 6. Security, privacy and authority invariants

- A user node is a compute contributor, not a corporate root shell.
- A0/Supervisor only receives the task-scoped capability necessary for execution.
- No repository, provider or device-wide secret is embedded in a model prompt, task artifact or worker result.
- User files and local product state are not accessible by default; task inputs are explicitly scoped.
- No task may cause unreviewed changes to canonical product state merely because a worker returned output.
- Revocation blocks new work and invalidates credentials/leases according to the protocol.
- Provider routes, model terms, actual billing class, data egress and fallback behavior must be qualified. “Runs on a user device” does not by itself prove local inference or zero data egress.
- All failure, cancellation, quota and integrity paths must fail closed and leave auditable status/evidence.

## 7. Required lifecycle and statuses

Suggested node states: **UNREGISTERED**, **PENDING**, **ADMITTED**, **SUSPENDED**, **REVOKED**, **NOT_VERIFIED**.

Suggested task states: **PLANNED**, **ADMITTED**, **DISPATCHED**, **RUNNING**, **SUCCEEDED**, **FAILED**, **CANCELLED**, **EXPIRED**, **BLOCKED**, **NOT_VERIFIED**.

A state transition must be tied to a timestamped event and evidence. Dispatch success is not execution success; execution success is not independent verification or acceptance.

## 8. Open decisions and qualification gates

Before implementation is qualified, determine and test:

1. the exact model/runtime candidates, licenses and supported quantization/offload mechanisms;
2. minimum hardware profiles and measured quality/latency thresholds;
3. installer UX and the default/max disk reservation policy per platform;
4. cache integrity, concurrent access, crash recovery, cancellation and cleanup behavior;
5. task/data isolation, consent, revocation, capability enforcement and network-egress policy;
6. A0 scheduler integration, idempotency/lease/fencing and supervisor recovery semantics;
7. automated positive/negative tests, independent security review and reproducible benchmark evidence.

No model family, runtime, quota value, partitioning strategy or implementation is selected or accepted by this requirements document.

## 9. Related canonical sources

- Canonical map: MEDIAHUB-CHAT-TREE-MAP.md
- Bootstrap instruction: MEDIAHUB-CONTEXT-BOOTSTRAP-INSTRUCTION.md
- Current continuation checkpoint: ../checkpoints/mediahub-next-continuation-checkpoint-2026-10-12-current.md
- Master development roadmap: ../checkpoints/MEDIAHUB-MASTER-DEVELOPMENT-ROADMAP-1.0.md
- Issue #301 — Contour A qualification: https://github.com/VlDMlNSh/mediahub-os/issues/301
- Binding Wave 272/273 requirements referenced by the Bootstrap instruction.

## 10. Evidence status for Wave 362

- Architecture proposal authored: **PROPOSED IN BRANCH**.
- Runtime changes: **NOT RUN**.
- Tests and benchmarks: **NOT RUN**.
- Independent review: **NOT VERIFIED**.
- Qualification/acceptance: **NOT QUALIFIED / NOT ACCEPTED**.
