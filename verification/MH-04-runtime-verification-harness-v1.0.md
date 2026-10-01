# MH-04 Runtime Verification Harness v1.0

**Status:** PROPOSED / NOT ACCEPTED
**Classification:** verification-only; no implementation authorization

## Purpose

Define the executable harness required to generate current runtime evidence for the MH-04 State Authority contract. The harness MUST test the canonical mutation boundary without introducing a second authority.

## Required cases

- V-01: authorized mutation succeeds.
- V-02: direct mutation by each non-authoritative consumer class is rejected.
- V-03: valid command follows Boundary → Authorization/Policy → Command → Contract → State Authority.
- V-04: stale generation/version writer is rejected.
- V-05: concurrent writers produce deterministic conflict behavior.
- V-06: duplicate command identity is idempotent or explicitly rejected according to the accepted contract.
- V-07: successful mutation emits an event causally linked to the command/correlation identity.
- V-08: event-driven mutation cannot bypass the governed command path.
- V-09: invalid state/command input is rejected without canonical mutation.
- V-10: no shadow authority can mutate canonical state when the State Authority is unavailable.
- V-11: restart/recovery preserves the accepted in-memory semantics; physical persistence remains blocked unless separately authorized.
- V-12: operation is deterministic without cloud/external AI/RAG.
- V-13: physical persistence tests remain blocked until separately authorized.
- V-14: security/authorization negative tests are independently executed.
- V-15: every result emits reproducible evidence with exact SHA, environment, command, identity and observed before/after state.

## Evidence requirements

Every executed case MUST record test ID, contract/invariant references, exact Git SHA, branch, environment, command, timestamp, command/correlation identity, authorization context, pre/post state, result, emitted events, artifact hash and reproducibility information.

Evidence is observational. Evidence MUST NOT grant acceptance, implementation authorization or production authorization.

## Gate

Current result: **RUNTIME VERIFICATION NOT YET EXECUTED**.

The historical P0-04 implementation remains candidate evidence only. This harness does not authorize copying or merging that implementation.
