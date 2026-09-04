# MH-22 — Production Model

**Status:** PROPOSED / NOT ACCEPTED / NOT FROZEN

## Production is an evidence-backed system state

Production is not a source-code state, branch state, successful build, passing test suite, existing binary, container, installer, or deployment event.

Production acceptance requires evidence across architecture, security, correctness, recovery, update, observability, operational readiness, and governance.

## Required state transitions

IDEA → DESIGN → IMPLEMENTED → TESTED → VERIFIED → QUALIFICATION CANDIDATE → QUALIFIED → RELEASED → DEPLOYED → OBSERVED → PRODUCTION ACCEPTED

Each transition requires its own evidence and decision.

## Separation of concerns

BUILD, TEST, QUALIFY, APPROVE, RELEASE, DEPLOY, PROMOTE, ROLLBACK, and ACCEPT are distinct governance/operational activities.

## Current baseline

SINGLE NODE / NO HA. No replication, multiple processes, containers, workers, or cloud services are to be interpreted as HA unless a future architecture decision explicitly establishes HA semantics.

## Production acceptance

A candidate is not production accepted until required qualification gates are satisfied, critical blockers are resolved, operational ownership exists, recovery and rollback are understood and validated, observability is sufficient, and governance approval is recorded.
