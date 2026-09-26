# MH-05 Parallel Model Development Method

**Status:** ACTIVE DEVELOPMENT METHOD
**Effective checkpoint:** 2026-09-07
**Repository:** VlDMlNSh/mediahub-os
**Scope:** MH-05 qualification/remediation only

## 1. Purpose

This document fixes the development method for MediaHub OS 11.x LTS / MediaHub iOS during MH-05 qualification. Work is organized as a controlled parallel specialist-agent workflow coordinated through the repository and GitHub audit trail.

## 2. Authority

Git SHA, exact-SHA execution evidence, executable test results, and explicit qualification gates are authoritative. Model output, model consensus, static reasoning, or agent agreement is supporting evidence only.

The immutable forensic target remains:

`25f7e3e50708d4bcad37fa712a5000dd2a7dea06`

Remediation branch:

`remediation/mh05-r3-event-evidence`

The forensic target is never modified, force-pushed, or rewritten.

## 3. Parallel specialist method

The orchestration roles are:

- ORCHESTRATOR — coordinates HEAD, dependencies, conflicts, scope and status.
- ARCHITECT — protects frozen architecture and MH-04 semantics.
- R3-EVIDENCE — provenance, causation, canonical Event projection and Event→Evidence.
- IMMUTABILITY — deep immutability and serialization isolation.
- SCHEMA — canonical Event/Evidence schema validation.
- R4-RESTORE — exact-SHA restore reachability/security analysis.
- COMPOSITION — production composition root and dependency graph.
- BYPASS RED TEAM — system-wide negative verification.
- TEST — MH-05 qualification test matrix.
- CI-EVIDENCE — exact workflow/commit execution evidence.
- FORENSICS — exact-SHA repository structure and history analysis.
- EVIDENCE RECONCILIATION — current qualification evidence packet.
- INDEPENDENT REVIEW — adversarial review independent of implementation claims.
- RELEASE GATE — qualification decision only; no implementation authority.

## 4. Model routing

Where external model execution is actually available through a controlled orchestration layer, specialist work may be routed by capability:

- High-reasoning models: architecture, orchestration, independent review, release gate.
- Fast models: inventory, static search, repetitive contract comparison, test-matrix assistance, documentation reconciliation.
- Multiple independent models: red-team, bypass, restore reachability and adversarial review.

No model receives authority to qualify the system. Model consensus never substitutes for executable evidence or independent review.

## 5. GitHub as the development control plane

GitHub is the canonical repository/audit plane for this method. Every meaningful implementation or documentation change must be traceable to:

- branch;
- parent SHA;
- resulting SHA;
- changed files;
- finding/reason;
- test result;
- workflow result;
- evidence classification.

GitHub Actions must execute against the exact implementation revision being claimed. `workflow_runs=[]` means execution evidence is absent, not PASS.

## 6. External model credentials

Model credentials are integration secrets, not project evidence. They must be supplied only through the external orchestration environment, environment variables, GitHub Actions secrets, or an equivalent secret store supported by the execution layer.

Never place API keys in prompts, source files, issues, evidence packets, logs, generated artifacts, commits, or chat output.

The current ChatGPT runtime must never claim that Google, Groq, or another external model was called unless an actual execution path and result are available.

## 7. Safe parallelism

Independent analysis passes may run in parallel. Writes to the same file or architectural surface are serialized. Agents do not independently redesign shared authority surfaces.

Dependency order:

`HEAD → independent analysis → targeted remediation → tests → exact-SHA execution → independent review → evidence reconciliation → release gate`

## 8. Qualification discipline

Claims use these levels only:

- IMPLEMENTED
- STATIC_SUPPORT
- IMPLEMENTED_NOT_EXECUTED
- EXECUTED
- INDEPENDENTLY_REVIEWED
- QUALIFIED
- PRODUCTION_AUTHORIZED

No status is upgraded merely because code exists or tests were written.

## 9. Scope lock

Until MH-05 is qualified, this method forbids MH-06 work, durable persistence, HA/cluster, production authorization/release, recovery redesign, changes to frozen MH-04 Event semantics, canonical-authority redesign, and unrelated capability implementation.

## 10. Continuation rule

Every new orchestration cycle starts by querying the actual current HEAD. The latest repository state supersedes stale prompt metadata. Historical evidence is retained and classified rather than deleted.

## 11. Current state at adoption

Known checkpoint HEAD at adoption: `7e0534def9358984e27a5b0ba6e8152670bfa1de`.

Known executable remediation revision with successful runtime/security workflow evidence: `5541c08fef8257368d06acd75b1f547659b4d804`.

MH-05 remains NOT QUALIFIED; production remains NOT AUTHORIZED; MH-06 remains LOCKED until all mandatory qualification gates are satisfied.
