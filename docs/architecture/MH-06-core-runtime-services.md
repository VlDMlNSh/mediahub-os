# MH-06 — Core Runtime Services

Status: PROPOSED / REQUIRES VERIFICATION

## Canonical invariant
Core Runtime Services orchestrate lifecycle, execution, supervision, scheduling, health and controlled recovery; P0-04 State Authority remains the sole canonical mutation authority.

## Mandatory path
Runtime request -> P0-05 Consumer Boundary -> P0-04 State Authority.

## Minimal conceptual core
Runtime Coordinator, Lifecycle Service, Health/Readiness, plus proposed Supervisor, Scheduler, Resource Governance, Execution Context, Dependency Coordination, Recovery, Startup/Shutdown and Observability adapters. Conceptual service does not imply separate process/package/API.

## Exclusions
No second state authority, hidden persistence, unrestricted network/filesystem/subprocess authority, autonomous AI mutation, HA/consensus, or technology-specific implementation choice is canonical.

## Status boundary
P0-06 architecture/service/lifecycle contracts are accepted; production qualification is not granted. MH-06 remains proposed until complete reconciliation, evidence register and governance acceptance.
