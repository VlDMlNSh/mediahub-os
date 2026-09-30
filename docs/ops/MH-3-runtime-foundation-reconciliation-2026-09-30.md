# MH-3 Runtime Foundation — Reconciliation 2026-09-30

Status: OPEN / ARCHITECTURE RECONCILIATION EVIDENCE
Parent chain: MH-01 → MH-02 → MH-03
Canonical acceptance is NOT granted by this document.

## Scope

This record reconciles the current MH-03 repository architecture with the Runtime Foundation continuation requirements for heterogeneous local, cluster and controlled-cloud execution.

## Current repository baseline

- Branch source: `engineering/mh21-sandbox-lifecycle-20260910`
- Source commit: `7eaa0d3fb74013f216a0be2eaf47424287c7db9a`
- R4: `471f709f5633feab7aeb62dd3ea52effad6d2bc4`
- R4 ancestry: verified by GitHub compare; source is 696 commits ahead and 0 behind.
- Existing MH-03 canonical documents remain PROPOSED / NOT ACCEPTED.
- P0-03/P0-04/P0-05/P0-06 authority and boundary constraints remain inherited.

## Problem

The continuation scope is materially broader than the historical MH-03 reference model. The historical model explicitly preserves a single-node/no-HA constraint, while the continuation introduces cluster execution, dynamic Developer/Compute Fabric roles, capability-driven placement, distributed resource abstractions and controlled cloud execution.

## Impact

Without an explicit boundary, cluster execution could be misread as State Authority HA or as a second canonical mutation path. That would contradict the inherited authority model.

## Resolution

MH-3 Runtime Foundation is reconciled as an execution foundation, not an authority foundation:

1. State Authority remains the sole canonical mutation authority.
2. Runtime coordinates lifecycle, admission, scheduling hooks, execution and recovery; it never becomes canonical authority.
3. Cluster execution is an execution-fabric capability. It does not create a second State Authority.
4. Dynamic Primary Development Node is a Developer/Compute Fabric role only. It is not State Authority leadership.
5. Local execution remains the preferred qualified target.
6. Controlled cloud execution is an optional, policy-gated execution target and is never a required dependency for deterministic local core operation.
7. Node qualification is capability-driven: hardware/platform detection → qualification → capability profile → policy → runtime admission.
8. Workload admission is explicit and bounded by identity, capability, resource, network, storage, secret and policy scopes.
9. Process liveness, readiness, health, qualification and trust remain distinct predicates.
10. Discovery does not imply trust or authorization.
11. Runtime events are evidence/facts and do not mutate canonical state.
12. Runtime operational state must not become a shadow canonical store.
13. Failure recovery may restart/reschedule/requalify execution, but may not reconstruct or mutate canonical state outside the governed authority path.
14. Thunderbolt/USB4 are high-speed transport capabilities; they are not shared physical RAM by default.
15. Remote/distributed memory is a logical abstraction and remains distinct from storage.
16. User and Developer runtime namespaces remain logically isolated even on one physical host.
17. Service boundaries are logical; native process, sandbox, container, VM and platform-native mechanisms remain implementation candidates selected by evidence.
18. Scheduler behavior is an interface; business criticality and policy remain outside MH-3 authority.
19. Observability is exposed through hooks to MH-11 rather than duplicated inside MH-3.
20. Security decisions are requested from MH-4/MH-12; policy decisions from MH-7; persistence authority from MH-14; cloud semantics from MH-21.

## Lifecycle model

Node:
Hardware Detection → Identity Bootstrap → Security Qualification → Capability Qualification → Runtime Bootstrap → Policy Load → State Synchronization → Service Admission → Health Qualification → Eligible Execution.

Service:
Discovered → Qualified → Admitted → Starting → Ready → Running → Degraded → Draining → Stopping → Stopped / Failed → Recovering → Requalified → Running.

Workload:
Proposed → Validated → Admitted → Scheduled → Starting → Running → Completed / Cancelled / Failed → Recovered or Terminal.

Recovery:
Failure Detection → Isolation → Classification → Restart / Reschedule / Failover where policy permits → State Verification → Requalification → Reintegration.

## Authority boundary

Canonical path remains:

Request → Identity → Authorization → Policy → Contract → State Authority → Canonical State → Event → Observers.

Runtime may read permitted state, submit governed requests, report execution state and publish runtime events. Runtime cannot self-authorize, self-promote, or create a competing canonical state store.

## Failure and partition semantics

- Process failure: bounded restart.
- Service failure: dependency-aware recovery.
- Node failure: reschedule/failover of eligible workloads; node requalification before reintegration.
- Cluster partition: degraded execution only where policy permits.
- State Authority partition/failure: no independent canonical commits by secondary execution nodes.
- Reconnection: reconciliation before resumed privileged execution.
- Repeated failure: bounded backoff, threshold and quarantine; no infinite restart loop.
- Unknown or ambiguous component: no production admission.

## Resource interface

MH-3 defines the runtime-facing abstraction for CPU, GPU, NPU, RAM, remote/distributed memory, storage, network, Thunderbolt/USB4, accelerators, camera, audio and display. Full resource governance remains delegated to the appropriate architecture and implementation contracts.

## Required invariants

R-01 Runtime ≠ State Authority.
R-02 Runtime ≠ Security Authority.
R-03 Runtime ≠ Policy Authority.
R-04 Runtime executes authorized workloads.
R-05 Workload admission is qualification-driven.
R-06 Process alive ≠ trusted.
R-07 Process alive ≠ qualified.
R-08 Domain ≠ deployment unit.
R-09 Node ≠ permanent authority.
R-10 Primary Development Node is dynamic within Developer/Compute Fabric only.
R-11 Local execution is preferred where qualified.
R-12 Cloud is optional where policy permits.
R-13 Developer runtime cannot access User Data by default and requires an explicit governed contract for any exceptional crossing.
R-14 Thunderbolt/USB4 ≠ shared RAM by default.
R-15 Remote/Distributed Memory is a logical abstraction.
R-16 Memory ≠ storage.
R-17 Unknown runtime component → no production admission.
R-18 Failure recovery requires requalification where appropriate.
R-19 Service health ≠ authorization.
R-20 Discovery ≠ trust.
R-21 Runtime events ≠ canonical state.
R-22 Runtime cannot bypass domain authority.
R-23 Critical workloads receive explicit failure/recovery semantics.

## Reconciliation result

The expanded Runtime Foundation can coexist with the inherited single-authority model only when cluster execution and dynamic primary roles are explicitly scoped to execution/development fabric and never to canonical State Authority.

The historical MH-03 architecture documents should therefore remain PROPOSED until governance accepts the expanded scope and records the exact relationship between execution-fabric clustering and the inherited single-node/no-HA canonical authority constraint.

## Open governance decisions

1. Explicitly accept cluster execution as a non-authoritative execution fabric under MH-3.
2. Explicitly accept Dynamic Primary Development Node as a Developer/Compute Fabric role only.
3. Confirm whether the inherited single-node/no-HA constraint applies to canonical authority only or to the entire runtime deployment topology.
4. Confirm the final boundary between MH-3 execution/resource abstractions and MH-21 distributed execution/cloud semantics.

No other user decision is required at this pass.

## Handoffs

- MH-4/MH-12: security qualification, trust, secrets and isolation enforcement.
- MH-6: concrete core runtime services and scheduler/supervisor implementation.
- MH-7: policy and admission decisions.
- MH-8: plugin execution boundaries.
- MH-10: AI workload semantics without authority.
- MH-11: observability contracts.
- MH-14: persistence boundary.
- MH-15: platform-specific runtime mechanisms.
- MH-16: update/recovery orchestration.
- MH-17: device capability and protocol qualification.
- MH-21: distributed/cloud execution semantics.
- MH-22: qualification and production gates.

## Status

MH-3 STATUS: OPEN

Reason: architecture is substantially reconciled, but canonical acceptance cannot be claimed while the four governance questions above remain unresolved and the historical MH-03 acceptance gate remains PROPOSED / NOT ACCEPTED.
