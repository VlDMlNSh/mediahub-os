# MH-06 — Decision Log

Status: PROPOSED / USER DECISIONS RECORDED / REQUIRES RECONCILIATION

DL-01: P0-04 remains the sole canonical mutation authority.
DL-02: P0-05 remains the mandatory runtime mutation/integration boundary.
DL-03: Runtime service responsibilities are conceptual until topology ADRs exist.
DL-04: Lifecycle, health and readiness are separate models.
DL-05: Generic health states must not be silently added to the accepted P0-06 lifecycle relation.
DL-06: Recovery is bounded and risk-tiered.
DL-07: Technology choices remain candidates until evidence, compatibility/security review, ADR and governance approval.
DL-08: Single-node/no-HA remains baseline.
DL-09: P0-07 governance/API gap is not bypassed.
DL-10: MH-6 architecture is not frozen until reconciliation/evidence/acceptance are complete.

## User architectural decisions — MH-6 continuation

Recorded from the user's explicit selection Q1-Q12 = D:

Q1 — Core Services model: D
Hybrid model: minimum necessary authority/coordination services plus modular services where justified by lifecycle, security or failure boundaries.

Q2 — Workflow: D
Unified workflow foundation with domain-specific workflows layered above it; Workflow is coordination, not authority.

Q3 — Configuration: D
Single logical Configuration Authority with distributed execution, versioning, policy and rollback.

Q4 — Service Discovery: D
Policy-driven hybrid discovery: trusted qualified nodes may be automatic; unknown nodes require DENY/QUARANTINE and qualification.

Q5 — Service failure: D
Adaptive failure handling: restart, failover, degraded mode or quarantine selected by criticality, dependency graph and policy.

Q6 — Core Service extensibility: D
Core Platform remains closed; extensions are permitted only through official extension/plugin boundaries without access to internal authorities.

Q7 — Service state: D
Hybrid state model: canonical state belongs to the appropriate authority; operational/ephemeral state may be local; derived state may be distributed.

Q8 — Scheduling: D
Internal control-plane Scheduling interface; domain services express intent, while Runtime/Scheduler retains final resource-admission authority.

Q9 — Time: D
Hybrid time architecture covering wall, monotonic, logical and event time with qualified synchronization policy and safe behavior under clock divergence.

Q10 — Core Service API: D
Internal service contracts plus one unified public MediaHub API; internal service APIs are not public automatically.

Q11 — Core Runtime Services visibility: D
Ordinary users receive aggregated MediaHub state; engineering/admin layers receive full service/runtime diagnostics.

Q12 — Final service architecture: D
A distributed MediaHub Core Service Platform with explicit authority boundaries, minimum necessary modularity, and a unified contract/security/runtime foundation.

## Governance interpretation

These Q1-Q12 selections are recorded as explicit product-architecture decisions. They do not by themselves constitute final MH-6 governance acceptance or freeze.

The selected D model must be reconciled against MH-1 through MH-5, P0-03/P0-04/P0-05/P0-06, State Authority boundaries, Runtime Foundation ownership, Security Architecture, Consumer Integration Boundary, resource/scheduling ownership, cluster model, storage/network boundaries, and subsequent MH-7+ architecture ownership.

No implementation authorization is inferred from these decisions.
