# MH-04 — State Authority Verification Specification v1.0

**Status:** PROPOSED / NOT ACCEPTED  
**Contract:** CTR-001  
**Purpose:** define executable verification targets before any production implementation authorization.

## Gate rule

A test existing is not evidence of execution. A passing test is not automatically qualification. Every result requires command, environment, actual output, and traceable evidence.

## V-01 Command identity and authorization

**Goal:** every mutation is attributable and authorization-scoped.

Positive: authorized command with valid identity/context reaches State Authority.  
Negative: missing, invalid, revoked, or insufficient authorization is rejected and canonical state is unchanged.

Evidence: command ID, correlation ID, authorization result, pre/post state/version.

## V-02 Boundary enforcement

Attempt mutation from each consumer class: UI, AI, cloud, plugin, device adapter, automation reaction, telemetry, health/readiness, cache, persistence/storage, recovery.

Expected: no consumer has a direct canonical mutation path; governed mutation must enter through command + authorization + State Authority.

## V-03 State transition correctness

For every initial state/operation pair define expected accept/reject result.

Expected: legal transitions mutate exactly once; illegal transitions do not mutate.

## V-04 Stale command handling

Submit a command against an obsolete state/version/concurrency token.

Expected: deterministic rejection or explicitly defined conflict result; no stale overwrite.

## V-05 Concurrent commands

Execute conflicting and non-conflicting commands concurrently.

Expected: deterministic ordering/conflict behavior matching the accepted contract; no invariant violation.

## V-06 Idempotent retry

Repeat the same retryable command with the same idempotency identity.

Expected: no unintended duplicate transition or duplicate external side effect.

## V-07 Event semantics

Execute a successful mutation and capture the command → mutation → event trace.

Expected: event represents a fact after canonical mutation; event contains required identity/correlation/causality; event alone cannot mutate state.

## V-08 Event-driven mutation re-entry

Trigger an event consumer that needs a state change.

Expected: it creates a governed command and re-enters authorization + State Authority; direct event→state mutation is rejected.

## V-09 Failure/partial failure

Inject failures at validation, authorization, consumer boundary, State Authority commit, and event publication boundaries as technically applicable.

Expected: no silent invalid canonical state; failure semantics are deterministic and evidence-backed.

## V-10 State Authority unavailable

Make the State Authority unavailable.

Expected: mutation stops; no cache/database/cloud/AI/recovery fallback becomes authority; system enters defined non-mutating degraded behavior.

## V-11 Restart/recovery

Restart the runtime around an in-flight or completed command according to the accepted recovery model.

Expected: lifecycle re-establishes safely; stale/incomplete operations are handled according to contract; no shadow authority appears.

## V-12 Offline-first

Remove Internet/cloud/external AI/RAG dependencies.

Expected: deterministic local State Authority semantics remain testable and operational within the authorized foundation scope.

## V-13 Persistence boundary

Current baseline: physical persistence is not authorized. Verification therefore first proves that no physical persistence component is acting as hidden authority.

Future durability tests are blocked until a separate accepted persistence decision authorizes them.

## V-14 Security negative suite

Test authentication bypass, authorization bypass, privilege escalation, physical connection abuse, discovery/trust confusion, replay, malformed input, secret leakage, and remote/cloud escalation.

Expected: fail closed and preserve authority boundaries.

## V-15 Evidence integrity

Verify that evidence records are attributable, correlated, reproducible, and observational.

Expected: evidence cannot rewrite canonical state and cannot be accepted merely because a test reports success.

## Qualification prerequisites

- Master Architecture ACCEPTED;
- MH-03 ACCEPTED;
- MH-04 contract ACCEPTED;
- architecture-impacting decisions accepted;
- implementation authorization explicitly recorded;
- executable test environment available;
- reproducible CI workflow available;
- security/red-team review available.

Until all prerequisites are satisfied, verification work may be prepared and infrastructure may be built, but production State Authority implementation remains BLOCKED.
