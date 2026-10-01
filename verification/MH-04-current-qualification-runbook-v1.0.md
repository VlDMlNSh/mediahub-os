# MH-04 Current Qualification Runbook v1.0

Status: EXECUTION PLAN / NOT QUALIFICATION

## Scope
This runbook defines the current evidence-producing pass for the authorized in-memory MH-04 State Authority foundation. It does not authorize physical persistence, HA, release, or any unaccepted downstream subsystem.

## Required current evidence
V-01 authorization; V-02 direct mutation boundary; V-03 valid mutation path; V-04 stale writer; V-05 concurrency; V-06 idempotency; V-07 event causality; V-08 event-driven re-entry; V-09 validation/integrity failure; V-10 shadow-authority failure behavior; V-11 restart/recovery boundary; V-12 deterministic local operation; V-13 physical persistence (BLOCKED by current foundation); V-14 independent security; V-15 reproducible evidence identity.

## Qualification rule
A successful test run is evidence for the tested property only. Qualification remains OPEN until every applicable case has current, reproducible evidence and all gaps/contradictions are dispositioned.

## Security and privacy constraints
Tests must preserve deny-by-default, least privilege, no authority delegation to observers/caches/cloud/UI/AI, local-first operation, and fail-closed behavior. No test fixture may contain production credentials or personal data.

## Current disposition
MH-04 implementation is authorized only for the in-memory foundation. Physical persistence remains explicitly out of scope until separately accepted architecture/contract authorization is recorded.
