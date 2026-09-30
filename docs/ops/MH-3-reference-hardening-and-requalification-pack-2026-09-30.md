# MH-3 Runtime Foundation — Reference Hardening & Requalification Pack — 2026-09-30

## Status

OPEN / REQUALIFICATION-READY-PENDING-GOVERNANCE

This document hardens the MH-3 architecture contract without granting governance acceptance.

## Reference architecture contract

### Authority invariant

The canonical mutation chain remains:

Request → Identity → Authorization → Policy → Contract → State Authority → Canonical State → Event → Observers.

MH-3 may execute, schedule, supervise, recover, quarantine and report. MH-3 MUST NOT:
- mutate canonical state directly;
- become Security, Policy or Domain authority;
- create a shadow canonical store;
- infer trust from discovery/liveness/readiness;
- promote a node to authority because it is Primary Development Node;
- restore canonical state from runtime cache.

### Topology invariant

MH-3 defines two distinct planes:

1. Authority plane — State Authority and governed canonical state semantics.
2. Execution plane — qualified local nodes, qualified cluster nodes and optional controlled-cloud execution targets.

The execution plane may be distributed. Distribution of execution does not imply distribution of canonical authority.

The historical single-node/no-HA constraint remains an explicit governance dependency. MH-3 does not silently reinterpret or remove it.

### Dynamic Primary Development Node

The role is defined as:

Primary Development Node = current preferred Developer/Compute Fabric execution target.

It is NOT:
- State Authority leader;
- canonical-state owner;
- security authority;
- policy authority;
- automatic failover authority.

Role transfer requires capability qualification and policy admission. It does not transfer canonical authority.

### Workload admission

Admission requires all applicable predicates:

Identity + Authorization + Policy + Capability + Resource + Isolation + Provenance + Health/Qualification.

Failure of any mandatory predicate is fail-closed.

### Lifecycle predicates

The following remain independent:

process alive / readiness / health / qualification / trust / authorization.

No predicate may substitute for another.

### Recovery

Recovery sequence:

Failure Detection → Isolation → Classification → bounded Restart/Reschedule/Failover → State Verification → Requalification → Reintegration.

Recovery may restore execution continuity. It may not independently reconstruct canonical state.

### Resource semantics

CPU/GPU/NPU/RAM/storage/network/accelerator/device resources are exposed through provider-neutral runtime abstractions.

Remote/distributed memory is logical resource semantics, not a claim of physically shared RAM.

Thunderbolt/USB4 are transport/interconnect capabilities and are not shared RAM by default.

### Isolation

User Runtime and Developer Runtime remain separate logical security/resource domains.

Developer execution receives no implicit User Data access.

Any exceptional crossing requires an explicit governed contract.

### Cloud boundary

MH-3 owns runtime-facing execution admission/resource/lifecycle hooks.

MH-21 owns distributed/cloud execution semantics.

Controlled cloud is optional, policy-gated and non-authoritative. Local qualified execution remains independently operable.

## C03-04 supervisor contract

Supervisor authority is limited to:
- lifecycle observation;
- restart/recovery orchestration;
- bounded retry/backoff;
- quarantine;
- health/readiness reporting;
- execution admission enforcement.

Supervisor MUST NOT:
- mutate canonical state;
- issue autonomous domain commands;
- bypass policy/security;
- convert operational status into authorization;
- create an alternate authority path.

## Cross-lane handoff contract

| Boundary | MH-3 provides | Receiving lane owns |
|---|---|---|
| MH-4/MH-12 | qualification inputs and execution isolation hooks | security/trust/secrets |
| MH-6 | lifecycle/runtime interfaces | concrete runtime services |
| MH-7 | admission inputs | policy decisions |
| MH-11 | runtime evidence/events | observability semantics |
| MH-14 | persistence requests | persistence authority |
| MH-15 | capability/runtime hooks | platform mechanisms |
| MH-16 | lifecycle/recovery hooks | update/recovery orchestration |
| MH-17 | device capability hooks | device/protocol qualification |
| MH-21 | execution target contract | distributed/cloud semantics |
| MH-22 | qualification evidence hooks | production qualification gates |

No receiving lane may infer that an MH-3 hook transfers authority.

## Governance decision packet

These decisions remain HUMAN_REQUIRED:

G-01. Does single-node/no-HA constrain canonical authority only, or all runtime deployment topology?

G-02. Is non-authoritative cluster execution accepted as an MH-3 execution-fabric capability?

G-03. Is Dynamic Primary Development Node accepted only as a Developer/Compute Fabric role?

G-04. Is the MH-3/MH-21 boundary defined as runtime admission/resource/lifecycle hooks versus distributed/cloud execution semantics?

No autonomous worker may mark these decisions resolved.

## Requalification waves

1. Provenance and branch ancestry.
2. MH-1/MH-2/P0 compatibility.
3. Authority and supervisor contract.
4. Runtime lifecycle and admission.
5. Distributed execution and topology.
6. Isolation and resource semantics.
7. Failure/recovery/reintegration.
8. R-01…R-23 evidence matrix.
9. Cross-lane boundary verification.
10. Targeted executable qualification.
11. Final autonomous verdict.
12. Governance handoff if and only if all evidence gates pass.

## Exit criteria

Requalification can reach PASS only when:
- provenance is complete;
- every mandatory criterion has direct evidence;
- R-01…R-23 have direct evidence;
- C03-04 is closed by evidence;
- cross-lane boundaries are evidenced;
- fresh executable qualification exists;
- governance decisions are explicitly resolved by the authorized authority.

PASS does not itself grant ACCEPTED/FROZEN/release/production authorization.
