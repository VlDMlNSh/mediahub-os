# MH-06 — Final Architecture Pass Report

Status: CANDIDATE / REQUIRES VERIFICATION
Date: 2026-09-04

## A. Canonical Current State
Core Runtime Services are an orchestration layer. They manage lifecycle, execution, supervision, scheduling, health/readiness and bounded recovery. They do not own canonical state mutation.

## B. Historical / Accepted Baselines
P0-04 remains the sole canonical mutation authority. P0-05 remains the mandatory integration and authorization boundary. P0-06 architecture/service/lifecycle contracts are treated as accepted baseline; implementation and production qualification remain separate evidence gates.

## C. Runtime Service Model
Minimal conceptual core: Runtime Coordinator, Lifecycle Service, Health/Readiness. Supervisor, Scheduler, Resource Governance, Execution Context, Dependency Coordination, Recovery, Startup/Shutdown and Observability remain capabilities requiring evidence/ADR before topology or implementation is made canonical.

## D. Lifecycle
Canonical P0-06 lifecycle remains PROVISIONING, INITIALIZING, SELF_TEST, READY, DEGRADED, SAFE_MODE, RECOVERY with its accepted transition relation. Generic STOPPING, STOPPED, FAILED and QUARANTINED belong to service/health/supervision domains unless separately governed.

## E. Startup / Shutdown
Required behavior is ordered initialization with fail-closed handling of critical failures; no partially initialized service is published as healthy. Shutdown must reject new work and handle in-flight work according to explicit cancellation/transaction semantics.

## F. Health / Readiness
Liveness is distinct from readiness. Health does not grant capability, and readiness does not imply trust.

## G. Supervision
Supervision may observe liveness/health, apply bounded restart policy and quarantine, and coordinate dependency readiness. It cannot bypass authorization or mutate canonical state.

## H. Scheduling
Scheduler responsibilities are admission, priority, deadline, fairness, concurrency and resource constraints. Technology and numeric limits remain unresolved candidates.

## I. Resource Governance
Resource classes include CPU, memory, storage, file descriptors, network/IPC, concurrency and queue depth. Concrete limits require host/hardware evidence.

## J. Execution Context
Execution context carries identity, capability/authorization context, correlation, deadline, cancellation, resource and security context. It is not a state authority.

## K. Dependency Model
Dependencies must distinguish hard, soft, optional and runtime relationships. Critical cycles require explicit ADR. Full graph remains open.

## L. Recovery / Self-Healing
Recovery is bounded and risk-tiered. Safe recovery candidates may include restart/reconnect/cache rebuild/bounded retry/degraded mode. Restricted and operator-only actions require stronger gates. No destructive autonomous recovery.

## M. Failure Domains
Failure must remain contained within task/service/dependency/runtime/host/storage/network/external-service domains and must not silently become canonical state corruption.

## N. IPC Boundary
Internal IPC is not implicitly trusted. Authentication, authorization, bounded payloads, request identity, timeout, cancellation, replay handling and audit context are required. Transport technology remains undecided.

## O. Observability
Metrics, logs, traces, health and audit context are observational and non-authoritative.

## P. Security Invariants
All 20 recorded MH-06 security invariants remain mandatory architectural constraints. Any violation is a contradiction requiring governance review.

## Q. Configuration / Policy
Runtime consumes governed configuration/policy; it does not invent hidden policy, hidden mutation, or a bypass around the P0-07 governance/API gap.

## R. AI Interaction
AI remains non-authoritative: analysis/recommendation/proposal only until policy, authorization and Consumer Boundary gates are satisfied.

## S. Persistence Boundary
No hidden runtime persistence or second canonical state store is authorized. Physical persistence implementation remains outside the MH-6 architecture decision.

## T. Update / Recovery Boundary
Runtime restart, application update, host update, data migration, security update and recovery are distinct operations with explicit rollback/governance requirements.

## U. Contradictions
C-01 lifecycle terminology; C-02 evidence continuity; C-03 architecture versus implementation qualification; C-04 P0-07 governance/API gap remain tracked. None authorizes changes to frozen baselines.

## V. Unknowns
Process topology, init framework, IPC transport, scheduler technology, resource limits, restart/backoff, host integration, observability stack, hardware constraints, isolation, deadlines, recovery rate limits, complete dependency graph, configuration schema integration and MediaHub iOS integration remain open.

## W. Decisions / ADR Candidates
Topology, lifecycle/health relation, scheduler, resource governance, IPC transport, supervisor policy, recovery authorization, startup/shutdown orchestration, isolation, observability and host integration require evidence and/or ADR before becoming canonical implementation choices.

## X. Acceptance State
MH-6 is not FROZEN and not PRODUCTION READY. The architecture pass is reconciled at the record level, but acceptance remains gated on complete evidence reconciliation, implementation verification, contradiction disposition, unknown handling and governance acceptance.

## Development boundary
This report is an architecture/governance artifact. Production implementation and debugging must occur in a separate development workspace and consume MH-6 through the master/reverse-master prompt mechanism.
