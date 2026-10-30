# A0 Issuer, Ingress and Lifecycle Contract Skeleton — Wave 485

**Status: DRAFT / NON-NORMATIVE / NOT ACCEPTED.** This is a requirements skeleton, not an accepted security contract. It does not select an issuer, attester, verifier owner, trust-anchor custodian, cryptographic protocol, token format, storage system, retention period, or fail-open exception. Runtime implementation remains blocked pending governance decisions and independent review.

## Fixed authority boundaries

- Jarvis coordinates corporation-level missions; it does not own or shadow the ASTRA A0 internal queue.
- ASTRA A0 owns its internal queue, claim, lease, heartbeat, retry, cancellation, recovery and ASTRA evidence/gate transitions.
- MediaHub Product State Authority remains the sole authority for canonical product-state mutation.
- Provider adapters, LLMs, GitHub Actions, cloud workers and executors gain no canonical mutation authority by implication.
- A caller-provided approval flag or enum is not proof of issuer authority or capability.

These preserve the already owner-approved DEC-DEV-02 Option C; this wave does not reopen that decision.

## Governance decisions required

| ID | Decision | Required evidence | Status |
|---|---|---|---|
| GOV-CAP-01 | Accountable issuer/attester role and grant scope | Named authority, subject classes, permitted operations/resources, exclusions, separation of duties | TBD |
| GOV-CAP-02 | Service-principal enrollment, suspension, recovery and re-enrollment | Enrollment authority, identity proofing, lifecycle and compromise handling | TBD |
| GOV-CAP-03 | Mandatory verification boundaries | Exact ingress/downstream consumers and independent verification requirements | TBD |
| GOV-CAP-04 | Trust-anchor custody, rotation and compromise response | Custodian, quorum, rotation, emergency revocation and recovery | TBD |
| GOV-CAP-05 | Expiry/revocation freshness and active-work behavior | Maximum staleness, online/offline policy and in-flight behavior | TBD |
| GOV-CAP-06 | Jarvis-to-A0 delegation bounds | Delegation chain, attenuation, audience, operation/resource scope | TBD |
| GOV-CAP-07 | Ingress acceptance evidence and independent reviewer | Durable acceptance record, reviewer independence and evidence retention | TBD |
| R-06 | Audit and privacy authority | Event ownership, fields, access, retention, integrity, audit outage behavior and data minimization | TBD |

No decision is inferred from DEC-DEV-02. No implementation technology is selected in place of governance.

## Contract concepts to specify after decisions

1. Principal identity, enrollment state and provenance; identity, credential, session, capability and authorization remain distinct.
2. Verifiable issuer proof over a canonical representation; caller-supplied approval metadata alone is insufficient.
3. Capability binding to issuer, subject, audience, operation, resource/target, scope, constraints, provenance, lifetime and revocation reference, subject to approved decisions.
4. Explicit delegation with no privilege amplification; audience and operation/resource restrictions are preserved or attenuated.
5. Verification at every mandatory consumer before protected actions, including trust, binding, lifetime and revocation freshness.
6. Replay/idempotency: unique request identity, atomic durable acceptance, duplicate semantics, concurrency behavior and recovery after ambiguous outcomes.
7. A0-owned durable acceptance, claim, lease generation/fencing, heartbeat, retry, cancellation, recovery and terminal evidence. Transport ACK is not durable A0 acceptance.
8. Audit/privacy: correlated event IDs, principal/issuer/capability references without credential material, access controls, integrity, retention and audit-unavailable behavior.
9. Fail-closed behavior for absent, malformed, ambiguous, untrusted, expired, revoked, mismatched or unverifiable authority. Exceptions require explicit governance approval.
10. Versioning, canonicalization, migration, downgrade prevention and compatibility.

## Negative and race acceptance matrix

These are required future tests, not evidence of implementation or test execution.

| ID | Scenario | Required outcome |
|---|---|---|
| NEG-01 | Approval flag/enum supplied without issuer proof | Reject; no protected action |
| NEG-02 | Missing, malformed or invalid issuer proof | Reject |
| NEG-03 | Unknown, suspended or untrusted issuer | Reject |
| NEG-04 | Wrong audience, subject, operation, resource or target | Reject |
| NEG-05 | Not-yet-valid or expired capability | Reject |
| NEG-06 | Revoked capability or stale revocation state | Reject or explicitly governed safe-unavailable outcome; never silently allow |
| NEG-07 | Delegation broadens scope or changes audience | Reject |
| NEG-08 | Concurrent duplicate request/dispatch | At most one durable acceptance/effect; deterministic idempotent response |
| NEG-09 | Same idempotency key with different payload digest | Reject and audit |
| NEG-10 | Crash after durable acceptance but before response | Reconcile from durable receipt; no duplicate effect |
| NEG-11 | Stale lease generation completes after reassignment | Reject stale writer using fencing |
| NEG-12 | Heartbeat after lease expiry or revocation | Apply accepted rule; stale worker cannot extend authority |
| NEG-13 | Cancellation races with claim/execution/completion | Deterministic A0-owned transition; no stale completion |
| NEG-14 | Recovery races with old worker resuming | New generation fences old worker; duplicate effects prevented |
| NEG-15 | Audit sink unavailable or integrity check fails | Follow explicit R-06 decision; no implicit fail-open |
| NEG-16 | Logs/artifacts contain token, secret, key or credential material | Test fails; sensitive material must not be emitted |
| NEG-17 | Schema downgrade or ambiguous canonicalization | Reject before authorization |
| NEG-18 | Transport ACK without durable A0 acceptance | Do not report task accepted |

## Acceptance evidence

- Recorded owner/governance dispositions for GOV-CAP-01…07 and R-06.
- Normative contract version, canonical schemas and exact verification semantics.
- Standards-compliant schema validation and positive, negative, mutation, replay, concurrency and crash-recovery fixtures.
- Source-bound review proving every protected consumer verifies accepted authority evidence.
- Durable receipt and A0 lifecycle evidence, including fencing and cancellation/recovery races.
- Audit/privacy tests for integrity, access, retention and credential-leak prevention.
- Exact-head CI, independent security review, then separate qualification/deployment/production acceptance records.

## Current disposition

- Issuer options A–D remain unselected; governance decisions are not fabricated.
- Wave 482 A0-ISSUER-01 remains a HIGH source-level provenance gap, not a confirmed exploitable vulnerability.
- No runtime changes, tests, secrets, provider calls, Gemini/Claude dispatch, server work, merge, deployment, qualification or acceptance occurred in this wave.
- Contour A remains NOT QUALIFIED / NOT DEPLOYED / NOT ACCEPTED; Contour B remains GATED.

## Related records

- [Wave 484 governance reconciliation](../checkpoints/MEDIAHUB-A0-ISSUER-GOVERNANCE-AND-LIFECYCLE-RECONCILIATION-WAVE-484-2026-10-30.md)
- [Issue #301](https://github.com/VlDMlNSh/mediahub-os/issues/301)
- [Canonical chat tree map](MEDIAHUB-CHAT-TREE-MAP.md)
- [Master Development Roadmap](../checkpoints/MEDIAHUB-MASTER-DEVELOPMENT-ROADMAP-1.0.md)
