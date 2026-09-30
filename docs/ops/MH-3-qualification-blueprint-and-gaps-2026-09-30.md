# MH-3 Qualification Blueprint and Gaps — 2026-09-30

## Truth status

MH-3 is OPEN. This document is a qualification blueprint, not a qualification result.

## Gaps

### G-01 — Governance boundary
The historical MH-03 decision log retains the single-node/no-HA constraint, while the continuation requires cluster execution and Dynamic Primary Development Node semantics.

Impact: canonical acceptance cannot be claimed until the constraint is explicitly scoped.

### G-02 — Independent acceptance evidence
The MH-03 acceptance criteria remain PROPOSED / NOT ACCEPTED. Existing architecture prose is not independent qualification evidence.

Impact: acceptance gate is not yet demonstrated.

### G-03 — Supervisor authority review
Contradiction register item C03-04 remains OPEN FOR REVIEW: supervisor authority must remain bounded to lifecycle/execution control and must not become an authority path.

### G-04 — Cross-lane boundary evidence
MH-3 requires explicit handoff verification against MH-4/MH-6/MH-7/MH-11/MH-14/MH-15/MH-16/MH-17/MH-21/MH-22.

Impact: cross-architecture consistency is not yet independently evidenced.

### G-05 — Executable qualification
A fresh targeted qualification pass is required against current repository state. Prior evidence cannot be reused as fresh proof of the expanded MH-3 scope.

### G-06 — Governance-only decisions
Four decisions remain outside autonomous authority:
1. scope of the historical single-node/no-HA constraint;
2. acceptance of non-authoritative cluster execution fabric;
3. acceptance of Dynamic Primary Development Node as execution-fabric role only;
4. exact MH-3/MH-21 distributed/cloud boundary.

## Blueprint

### Wave 1 — Baseline
- Read current authoritative branch and candidate branch through GitHub.
- Verify SHA, tree, R4 ancestry and changed surface.
- Verify no unrelated changes.

### Wave 2 — Parent compatibility
- Reconcile MH-1 and MH-2 constraints.
- Reconcile P0-03/P0-04/P0-05/P0-06.
- Verify canonical mutation path remains singular.

### Wave 3 — Runtime model
Check node, service, workload, execution target, resource abstraction, lifecycle, dependency graph, discovery, admission, qualification, health/readiness/liveness, supervision and recovery.

### Wave 4 — Distributed semantics
Check local-first execution, qualified cluster execution, Dynamic Primary Development Node, partition, State Authority epoch, split-brain prevention, rescheduling, requalification and controlled cloud as optional target.

### Wave 5 — Isolation and authority
Check User vs Developer, identity, capability, resource, storage, network, secret boundaries, and Runtime vs Security/Policy/State/Domain authorities.

### Wave 6 — Platform/resource semantics
Check Linux, macOS, iPadOS, Raspberry Pi, CPU/GPU/NPU, local/remote/distributed memory, storage distinction, Thunderbolt/USB4 transport semantics and thermal/power/mobile degradation.

### Wave 7 — Failure/recovery
Check process/service/node/cluster/partition failures, bounded retry/backoff, cancellation, quarantine, reintegration and offline behavior.

### Wave 8 — Invariant qualification
Independently evaluate R-01…R-23. Each invariant must have direct evidence or be classified GAP.

### Wave 9 — Security/observability/update handoffs
Verify MH-4/MH-11/MH-16 boundaries without importing their authority into MH-3.

### Wave 10 — Verdict
Return PASS / PARTIAL / FAIL / INCONCLUSIVE, requirement-to-evidence matrix, unresolved gaps, remediation queue items and governance decisions still required.

No autonomous worker may mark MH-3 ACCEPTED/FROZEN, merge, release or authorize production.

## Qualification exit

MH-3 may be proposed for governance acceptance only when no material contradiction remains, every mandatory acceptance criterion has direct evidence, R-01…R-23 are evidenced, governance questions are explicitly resolved, provenance is complete and independent qualification evidence is recorded.

Final governance status remains human-controlled.
