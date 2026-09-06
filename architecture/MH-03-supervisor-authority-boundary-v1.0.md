# MH-03 — Supervisor Authority Boundary v1.0

Status: PROPOSED / REQUIRES GOVERNANCE ACCEPTANCE

## Purpose
Resolve contradiction C03-04: Runtime Supervisor must not become a second canonical State Authority.

## Allowed Supervisor authority
- coordinate lifecycle: bootstrap, start, stop, restart, and bounded degraded-mode transitions;
- observe health/readiness and dependency status;
- schedule execution work that is already authorized;
- initiate recovery procedures that preserve the State Authority boundary;
- fail closed when lifecycle or dependency preconditions are not satisfied.

## Prohibited Supervisor authority
- create, mutate, or delete canonical domain state directly;
- authorize privileged user, device, cloud, AI, or plugin operations;
- bypass the Consumer / Integration Boundary;
- publish canonical state independently of State Authority;
- become a fallback or shadow State Authority;
- treat health, readiness, liveness, discovery, physical connection, or remote access as authorization;
- silently persist canonical state outside the canonical persistence boundary;
- rewrite commands or events to obtain authority.

## Required mutation path
All canonical mutation remains:

Command → Validation → Authorization/Policy → Consumer Contract → State Authority → Canonical Mutation → Event → Observers.

Supervisor-triggered mutation MUST enter the same governed command path. Recovery cannot create a parallel mutation path.

## Failure semantics
If State Authority is unavailable or canonical-state integrity cannot be established, Supervisor MUST fail closed for canonical mutation. It may expose diagnostic/degraded status and perform non-mutating lifecycle actions, but it cannot substitute another authority.

## Acceptance evidence
Executable negative tests must prove that Supervisor cannot:
1. mutate canonical state directly;
2. authorize a denied command;
3. bypass Consumer / Integration Boundary;
4. publish an authoritative state snapshot independently;
5. create shadow state after State Authority failure;
6. convert readiness/health into authorization.

## Governance
This artifact proposes the bounded-authority resolution for C03-04. It does not self-accept MH-03 or MH-01 and does not grant MH-04 implementation authorization. Governance acceptance and explicit freeze remain separate actions.
