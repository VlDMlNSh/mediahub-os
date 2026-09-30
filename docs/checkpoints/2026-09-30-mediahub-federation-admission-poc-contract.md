# MediaHub Federation Admission PoC Contract

Date: 2026-09-30

## Purpose

Define the non-production correctness contract for the boundary between the Local MediaHub Cluster and the Cloud Development Cluster.

This PoC validates admission, isolation, bounded execution, and termination of cloud-escalated user work before any data synchronization or production deployment.

## Administrative domains

### Local MediaHub Cluster

User-facing cluster assembled inside the user's local network.

Responsibilities:
- user capability and settings extension;
- local AI/compute/storage capacity extension;
- expansion of seamless wireless coverage;
- ordinary local media and workload processing;
- local resource coordination.

### Cloud Development Cluster

Permanent MediaHub company/development environment.

Responsibilities:
- product development;
- CI/CD;
- developer compute;
- engineering storage and artifacts;
- internal development services;
- company operational workloads.

The cloud cluster is closed to users by default.

## Admission contract

Every cross-domain request must have:
- a unique job ID;
- originating cluster identity;
- workload class;
- requested capability;
- explicit admission decision;
- bounded input scope;
- execution deadline/lease;
- result scope;
- audit record.

Default decision: DENY.

Allowed user execution class:
CLOUD_ESCALATED_USER

This class grants execution for one admitted request. It does not grant cluster membership.

## Required state machine

DENIED
  -> ADMITTED
  -> RUNNING
  -> RESULT_READY
  -> CLOSED

Failure paths:

DENIED -> CLOSED
ADMITTED -> EXPIRED -> CLOSED
RUNNING -> FAILED -> RETRY_OR_CLOSED
RUNNING -> LEASE_EXPIRED -> TERMINATED -> CLOSED

No terminal state may create persistent user membership in the Cloud Development Cluster.

## Required isolation properties

1. A local user request cannot enumerate cloud resources before admission.
2. A denied request transfers no user payload.
3. Admission authorizes only the declared workload scope.
4. Cloud execution cannot enumerate the Local MediaHub Cluster.
5. Development Mesh connectivity does not grant Media Data Plane access.
6. Provider credentials remain exclusively in GitHub Secrets.
7. Provider credentials are never stored in cluster identity, job metadata, logs, or node-local persistent state.
8. Request-scoped access expires automatically.
9. Retry preserves the same job boundary and does not broaden authorization.
10. Closing a request removes its temporary cloud execution authority.

## Data transfer contract

Before admission:
- zero user payload transfer.

After admission:
- transfer only the minimum required input;
- identify input by job ID;
- integrity-check transferred data;
- enforce an explicit size/time boundary;
- return only the declared result;
- do not synchronize the user's full media library or local storage fabric.

## PoC scenarios

### S1 — default denial
Submit CLOUD_ESCALATED_USER without admission.

Expected:
- DENIED;
- zero payload transfer;
- no cloud execution.

### S2 — valid admission
Submit a bounded request with valid cluster identity and scope.

Expected:
- ADMITTED;
- lease created;
- only declared capability available.

### S3 — bounded execution
Execute the admitted request.

Expected:
- RUNNING;
- execution remains within declared scope;
- result associated with the same job ID.

### S4 — bounded result
Return the result to the local cluster.

Expected:
- only declared result crosses the boundary;
- integrity verification succeeds;
- request becomes RESULT_READY then CLOSED.

### S5 — lease expiry
Allow the execution lease to expire.

Expected:
- execution authority terminates;
- request cannot continue without a new explicit admission;
- no persistent membership remains.

### S6 — retry after failure
Fail execution and request retry.

Expected:
- retry remains bound to the original job scope;
- no privilege expansion;
- audit contains the failure and retry transition.

### S7 — isolation probe
Attempt undeclared cloud/resource access from an admitted user job.

Expected:
- access denied;
- admission remains limited to declared scope.

### S8 — company workload separation
Submit CLOUD_DEVELOPMENT_ONLY through the user escalation interface.

Expected:
- rejected as a user escalation;
- internal company workload remains in the company execution domain.

## Evidence requirements

Each scenario must produce machine-readable evidence containing at least:
- scenario ID;
- job ID;
- source cluster;
- destination domain;
- workload class;
- admission decision;
- state transitions;
- payload byte counts;
- capability scope;
- lease/expiry state;
- execution result;
- failure/retry information;
- final authorization state;
- evidence timestamp.

Secrets and credential values must never appear in evidence.

## PASS criteria

The federation PoC passes only if all required scenarios demonstrate:
- default deny;
- explicit admission;
- bounded authorization;
- bounded transfer;
- correct execution;
- bounded result return;
- automatic termination;
- retry without privilege expansion;
- isolation of undeclared resources;
- separation of user and company workloads;
- complete auditable state transitions.

A design review or simulated PASS is not sufficient for final federation qualification. Runtime evidence from the actual PoC is required.

## Network policy

The PoC must not require a permanent full-tunnel connection between local and cloud domains.

Preferred topology:
- Local MediaHub Cluster: direct LAN/P2P;
- Cloud Development Cluster: private Development Mesh;
- Local-to-cloud: request-scoped federation gateway/API;
- API egress: separately policy-controlled.

VPN is connectivity infrastructure and must not be used to bypass provider or regional restrictions.

## Scope restrictions

This checkpoint authorizes design/PoC work only.

It does not authorize:
- production deployment;
- changes to GOLD #176;
- changes to immutable R4 baseline;
- movement of provider credentials out of GitHub Secrets;
- permanent user membership in the Cloud Development Cluster;
- full-library synchronization.

## Next execution order

1. Implement or locate the non-canonical federation PoC harness.
2. Add deterministic admission/state-machine tests.
3. Add isolation and payload-boundary tests.
4. Run the PoC without touching GOLD #176.
5. Collect machine-readable evidence.
6. Independently verify evidence.
7. Only after correctness PASS proceed to transport/data-transfer benchmarking.
