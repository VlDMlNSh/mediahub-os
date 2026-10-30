# A0 Issuer and Verifier Contract — Wave 487

**Status: DRAFT NORMATIVE CANDIDATE / NOT ACCEPTED / NOT IMPLEMENTED.**
**Target parent:** Wave 486 head `824bb2568b2ac8bb3dceb3608366668e99bab95e`.
**Purpose:** turn the owner-directed Wave 486 dispositions into technology-neutral, testable security and lifecycle requirements. This document defines behavior, not a cryptographic protocol, token format, vendor, endpoint or deployed service.

## 1. Authority, scope and precedence

This contract applies to mission-to-A0 ingress, issuer proof, service-principal identity, capability verification, protected downstream consumers, durable acceptance, A0 lifecycle transitions, replay/idempotency and security audit/privacy.

It preserves the already owner-approved DEC-DEV-02 Option C:

- Jarvis coordinates corporation-level missions and submits bounded requests. It does not own an A0 shadow queue, mint A0 grants, or directly mutate A0 lifecycle.
- A separately governed Security Issuer Authority controls issuer identity, grant policy, issuance, service-principal admission and revocation governance.
- ASTRA A0 independently verifies incoming authority and solely owns its internal queue, claim, lease, heartbeat, retry, cancellation, recovery, ASTRA evidence and gate transitions.
- Each protected consumer independently verifies the authority relevant to its own audience and protected effect. An A0 ingress decision is not a transferable approval.
- MediaHub Product State Authority remains the sole canonical product-state mutation authority and independently enforces that boundary.
- Executors, models, providers, GitHub Actions, cloud workers and transport acknowledgements gain no authority by implication.

This contract does not override Baseline 2.0, existing historical IDs, product-state authority, or higher-level governance. If a conflict is found, stop the affected protected path and record it; do not resolve it by implicit privilege expansion.

## 2. Normative vocabulary and security invariants

The terms MUST, MUST NOT, REQUIRED, SHOULD and MAY are used in their ordinary normative sense. Because this is a draft, these requirements are proposed and do not become binding until independent review and formal acceptance.

1. **No caller authority:** caller-supplied `approval_state`, `approved=true`, enum, role string, object type, workflow identity or transport ACK MUST NOT establish issuer authority.
2. **No self-issuance:** Jarvis, A0, an executor, provider adapter, model or workload MUST NOT issue or approve its own capability.
3. **Separation of duties:** issuer policy administration, trust-anchor custody, A0 operation, product-state mutation and independent security review MUST remain separately accountable.
4. **Default deny:** missing, ambiguous, malformed, unverifiable, stale or contradictory evidence MUST deny the protected effect.
5. **Audience confinement:** proof accepted for one consumer MUST NOT be replayable as authorization for another consumer.
6. **Least authority:** every grant MUST be bound to a finite subject, audience, operation set, resource/target, task identity, constraints and expiry. Wildcards are denied unless a separately approved policy explicitly defines a bounded wildcard class.
7. **No amplification:** delegation MUST preserve or reduce all authority dimensions; it MUST NOT broaden subject, audience, operation, resource, environment, constraints or lifetime.
8. **Atomic acceptance:** A0 MUST durably bind one idempotency identity to one immutable request digest before reporting acceptance.
9. **Fencing:** stale lease generations and revoked/expired authority MUST NOT commit protected effects.
10. **Evidence integrity:** protected decisions MUST produce correlated, tamper-evident audit evidence without recording credential material.

## 3. Principal and issuer lifecycle

### 3.1 Principal identity

A service principal MUST have a stable, non-secret identifier and an explicit lifecycle state: `PENDING`, `ACTIVE`, `SUSPENDED`, `REVOKED` or `RETIRED`. State transitions MUST be authorized by the Security Issuer Authority under a versioned policy.

Enrollment MUST bind:
- principal identifier and verified workload identity;
- accountable owner/team reference and declared purpose;
- environment and workload class;
- permitted audiences;
- maximum operation/resource classes;
- enrollment policy version and approval evidence;
- activation time and identity generation.

Enrollment MUST default to deny. Privileged enrollment, recovery and re-enrollment SHOULD require dual approval. Suspension MUST prevent new protected actions. Re-enrollment after compromise MUST create a new identity generation; the prior identity MUST NOT be silently reactivated.

### 3.2 Issuer authority

The Security Issuer Authority MUST be distinct from Jarvis, A0 and protected consumers. It MUST:
- authenticate the requesting principal independently of request-supplied claims;
- evaluate versioned grant policy;
- enforce subject/audience/operation/resource/constraint bounds;
- refuse self-grant and unauthorized delegation;
- issue proof only for an admitted principal and approved task;
- expose revocation state with an explicit freshness/version indicator;
- audit issuance, denial, policy change, suspension, revocation and key lifecycle events.

The issuer service's existence, deployment and operational staffing are NOT established by this contract.

## 4. Capability semantics (format-neutral)

A capability is an issuer-authenticated statement of bounded authority. The eventual wire representation is an ADR decision. Regardless of format, the authenticated semantic claim set MUST include:

| Claim | Required meaning |
|---|---|
| issuer | Stable issuer identity and trust/key version reference |
| subject | Exact enrolled principal and identity generation |
| audience | Exact intended verifier/consumer |
| capability_id | Unique, non-secret capability identifier |
| task_id | Exact admitted task/mission identity |
| operations | Finite allowlisted operation set |
| resources | Exact resource/target identifiers or policy-bounded class |
| constraints | Environment, data classification, limits and other policy conditions |
| issued_at / not_before / expires_at | Authenticated time bounds |
| policy_version | Issuer policy version used to authorize issuance |
| delegation | Parent/grant provenance and attenuation chain, if delegated |
| revocation_ref | Revocation generation or lookup reference with freshness semantics |
| request_binding | Immutable request digest or an unambiguous binding to it |

The proof MUST authenticate the complete canonical semantic claim set. Duplicate keys, ambiguous encodings, unrecognized critical fields, non-canonical representations and downgrade attempts MUST be rejected before authorization. The implementation ADR MUST define canonicalization, cryptographic algorithms, serialization, key identifiers, rotation and verifier interoperability.

The verifier MUST NOT accept a proof merely because it parses or because it was signed by any trusted key. It MUST validate all claim bindings against the current request and consumer policy.

## 5. Delegation and Jarvis-to-A0 ingress

Jarvis submits a bounded mission request with a stable correlation ID and immutable payload digest. Jarvis does not mint or transfer an A0 capability.

The Security Issuer Authority evaluates the request and, if permitted, issues a distinct capability whose subject is the admitted A0 service principal and whose audience is the A0 ingress verifier. The grant MUST be limited to:
- the exact mission/task identity;
- a finite operation set supported by A0;
- exact resources/targets or an approved constrained class;
- an explicit environment and data-classification ceiling;
- a bounded expiry no later than the issuer's maximum lifetime;
- the approved policy and delegation provenance.

A0 MUST reject a grant if any delegation step broadens scope, changes audience unexpectedly, loses provenance, increases lifetime, introduces an unregistered principal or permits canonical product-state mutation. Downstream workers receive only separately issued, attenuated capabilities for their exact consumer and task. A0 acceptance MUST NOT be forwarded as a universal downstream authorization.

## 6. Verification algorithm and decision point

Every protected consumer MUST perform the following logical checks immediately before the protected effect. Implementations may optimize retrieval, but MUST preserve equivalent semantics and freshness.

1. Parse strictly; reject malformed, ambiguous, oversized or unsupported critical fields.
2. Resolve issuer identity and trust-anchor version from an approved trust set.
3. Verify proof integrity and issuer authorization status.
4. Resolve subject identity and current principal generation; require `ACTIVE`.
5. Match exact audience to the current verifier.
6. Match task identity and immutable request digest.
7. Require requested operation to be in the finite grant set.
8. Require exact resource/target and all environment/data constraints to match.
9. Validate not-before, expiry and clock confidence.
10. Resolve revocation state; require age no greater than 30 seconds and a monotonic/non-rollback generation.
11. Validate delegation chain and prove attenuation at every hop.
12. Verify the consumer's own policy and decision version.
13. Emit a correlated allow/deny audit decision before the effect; if evidence cannot be durably recorded, deny the privileged effect.
14. Re-check the relevant grant, revocation generation and lease fencing immediately before commit if any state may have changed since the initial check.

The initial target defaults are maximum capability lifetime **300 seconds** and maximum revocation-state age **30 seconds**. A verifier MUST reject when it cannot establish these bounds. Clock-skew tolerance remains an implementation ADR parameter; uncertainty outside the approved bound MUST deny. No offline fail-open is permitted.

## 7. Expiry, revocation and in-flight work

Revocation MUST prevent new protected effects as soon as the consumer observes the newer revocation generation. A consumer MUST NOT rely on a cached state older than 30 seconds.

For active A0 work:
- A0 MUST fence the current lease generation and initiate its own cancellation/containment transition.
- A stale worker MUST be unable to heartbeat, renew, claim, complete or commit protected effects.
- Only explicitly enumerated non-mutating safe cleanup may proceed after revocation/expiry, and only if that cleanup is independently authorized.
- Recovery MUST create a new lease generation and MUST NOT allow an old worker to resume with stale authority.
- Revocation, cancellation, completion and recovery races MUST resolve deterministically with one durable terminal outcome and no duplicate protected effect.

If revocation service, trusted clock, issuer state or required audit is unavailable or too stale, new privileged ingress and protected mutations MUST fail closed. A0 may perform only the safe containment behavior explicitly specified in its accepted lifecycle policy.

## 8. Replay, idempotency and durable acceptance

A0 MUST atomically reserve an idempotency key against:
- request digest;
- task/mission ID;
- issuer and subject identity generation;
- capability identifier/digest;
- audience and operation/resource binding;
- policy and revocation generation;
- acceptance state and durable receipt ID.

Required semantics:
- same key + same immutable digest: return the existing receipt/state; do not create a second task or effect;
- same key + different digest: reject, emit a security event and do not mutate the accepted request;
- concurrent identical requests: at most one durable acceptance and one logical task;
- crash after reservation/acceptance but before response: recover from the durable receipt and return the same outcome;
- crash before durable reservation: no acceptance may be reported;
- receipt storage unavailable or integrity uncertain: reject; do not return a transport-level success as task acceptance.

A durable A0 acceptance receipt MUST include receipt ID, request digest, task ID, issuer/subject/capability references, policy version, audience, accepted operation/resource scope, expiry/revocation generation, idempotency key digest, decision timestamp and evidence correlation ID. It MUST NOT contain raw bearer tokens or secret material.

## 9. A0 lifecycle and fencing contract

A0 alone owns its internal lifecycle. At minimum, the implementation MUST define durable states and legal transitions for queued, claimed, leased, running, retry-pending, cancellation-requested, cancelled, recovery-pending, completed and terminal-failed work (exact state names may map to existing canonical IDs).

Every lease MUST carry a monotonically increasing generation/fencing token. Every heartbeat, renewal and completion MUST prove current lease ownership, current generation and valid capability. A0 MUST reject:
- heartbeat or completion from an expired lease;
- writes from a superseded generation;
- completion after cancellation/revocation has won the transition;
- stale worker resumption after recovery;
- retries that create duplicate external effects without an idempotency contract.

Queue state, lease state and terminal evidence MUST be durable and reconciled after process restart. No external transport may mutate these lifecycle states directly.

## 10. Audit, privacy and evidence integrity (R-06)

Security Audit owns integrity and controlled access to security events. Privacy/Data Governance owns classification and retention policy. A concrete operational team is not assigned here.

Events MUST be correlated and tamper-evident for:
- principal enrollment, activation, suspension, recovery and retirement;
- issuer policy changes and grant issuance/denial;
- verifier allow/deny and reason code;
- expiry, revocation, replay and delegation;
- durable ingress receipt and idempotency conflict;
- lease claim/renewal/fencing, retry, cancellation, recovery and terminal transition;
- privileged downstream effect and audit access itself.

Minimum fields: event ID, event type, timestamp/time confidence, correlation ID, stable principal/issuer IDs, identity generation, capability ID/digest (not raw capability), audience, operation/resource classification, policy version, decision/reason, revocation generation, A0 receipt/lease generation and source/evidence reference.

MUST NOT log raw capability/token, authorization header, API key, password, private key, session cookie, HMAC key or full sensitive payload. Use payload digests and classified references. Audit reads MUST be least-privilege and themselves auditable.

Initial retention targets from Wave 486: 365 days for security decision/issuer/revocation evidence and 90 days for routine task-operational metadata, subject to stricter law, contract, privacy classification, deletion and legal-hold rules. These are target defaults, not legal approval. Audit sink outage, integrity failure or unverifiable sequence MUST block new privileged ingress and protected mutation; active work is fenced/contained rather than silently continued.

## 11. Versioning and migration

The implementation MUST version the semantic contract, policy, schema and trust set independently. Verifiers MUST reject unsupported major versions, ambiguous downgrade, unknown critical semantics and non-monotonic trust/revocation generations. A migration MUST define dual-read/write windows, issuer key overlap, revocation continuity, rollback limits and evidence continuity. Rollback MUST NOT restore revoked authority or accept an older policy generation.

No specific serialization, token standard, signature algorithm, KMS/HSM product, identity provider, database or endpoint is selected by this contract.

## 12. Acceptance matrix

All tests below are REQUIRED for implementation qualification. They are specifications only; no tests are claimed executed by Wave 487.

| ID | Fixture / fault injection | Required assertion |
|---|---|---|
| AUTH-01 | Caller sets `approval_state=approved` without issuer proof | Deny before protected effect; audit reason |
| AUTH-02 | Missing, malformed, tampered or unknown issuer proof | Deny; no fallback to caller metadata |
| AUTH-03 | Unknown, suspended, revoked issuer or inactive principal generation | Deny |
| AUTH-04 | Wrong issuer trust version / untrusted key | Deny; no key trial outside trust set |
| AUTH-05 | Wrong subject, identity generation or audience | Deny |
| AUTH-06 | Wrong task ID or request digest | Deny |
| AUTH-07 | Operation absent from finite allowlist | Deny |
| AUTH-08 | Resource/target mismatch or wildcard escalation | Deny |
| AUTH-09 | Environment/data-classification constraint mismatch | Deny |
| AUTH-10 | Not-before in future, expired grant or uncertain clock | Deny |
| AUTH-11 | Revocation state older than 30 seconds or generation rollback | Deny |
| AUTH-12 | Revoked grant during active task | Fence worker; no subsequent protected effect |
| AUTH-13 | Delegation broadens subject/audience/operation/resource/lifetime | Deny |
| AUTH-14 | Duplicate keys, ambiguous canonicalization, unknown critical field or downgrade | Deny before authorization |
| IDEM-01 | Same idempotency key and same digest | Return same receipt; one logical task |
| IDEM-02 | Same key and different digest | Reject and audit; preserve original receipt |
| IDEM-03 | N concurrent identical ingress requests | One durable acceptance and one logical task |
| IDEM-04 | Crash after durable receipt before response | Recover and return same receipt; no duplicate effect |
| IDEM-05 | Crash before durable reservation | No acceptance reported |
| IDEM-06 | Receipt store unavailable or uncertain | Deny; transport ACK not treated as acceptance |
| LIFE-01 | Old lease generation heartbeats/completes after reassignment | Reject stale writer |
| LIFE-02 | Heartbeat after lease expiry or capability expiry | Reject; do not renew expired authority |
| LIFE-03 | Cancellation races with completion | One deterministic terminal state; no late effect |
| LIFE-04 | Recovery races with old worker resumption | New generation fences old worker |
| LIFE-05 | Retry after ambiguous external side effect | Reconcile by idempotency; no duplicate effect |
| LIFE-06 | Revocation races with lease renewal/commit | Revocation wins before protected commit |
| AUD-01 | Audit sink unavailable or event integrity fails | Deny new privileged work; fence/contain active work |
| AUD-02 | Audit event omits required correlation/principal/policy fields | Test fails |
| AUD-03 | Token, secret, key or sensitive payload injected into logs/artifacts | Test fails; no material emitted |
| AUD-04 | Unauthorized audit read or unlogged audit access | Deny and alert |
| VER-01 | Consumer B receives proof intended for consumer A | Deny audience mismatch |
| VER-02 | A0 accepted request then downstream consumer checks authority | Downstream performs its own verification |
| VER-03 | Product-state mutation attempted through A0/executor grant | Deny; Product State Authority boundary preserved |
| VER-04 | Revocation/clock/audit service unavailable | Fail closed; no privileged side effect |
| VER-05 | Contract/policy/trust version rollback | Reject downgrade or stale generation |

## 13. Qualification evidence required

Before runtime integration or dispatch to an executor that can change code, collect:
1. Independent A3 source review of this contract and the Wave 486 dispositions.
2. A protocol/identity/trust-anchor/audit ADR with threat model, data-flow, provider and cost/quota analysis.
3. Canonical schema(s) with strict parsing and Draft 2020-12 validation where JSON is used; format assertions explicitly enabled.
4. Positive, negative, mutation, replay, concurrency, crash-recovery, expiry/revocation, fencing, audit-outage and secret-leak fixtures.
5. Source proof that every protected consumer checks its own authority before the effect.
6. Exact-head required CI and reviewer identity/independence evidence.
7. Separate qualification, deployment readiness, deployment and production acceptance evidence.

## 14. Explicit non-goals and unresolved ADR items

This document does not choose a cryptographic algorithm, JWT/PASETO/CWT or other token format, signature encoding, canonical JSON/CBOR profile, KMS/HSM vendor, identity source, database, queue technology, audit sink, endpoint, secret name, staff identity, clock-skew tolerance or service topology. Those require a source-backed ADR and security review.

This document does not authorize reading or changing secrets, invoking a provider, dispatching Gemini/Claude, runtime modification, migration, merge, deployment or qualification. The existing Wave 482 `A0-ISSUER-01` source-level provenance gap remains HIGH until verified remediation; it is not characterized here as a confirmed exploit.

## 15. Source basis

- Wave 486 owner-directed disposition: blob `13e6745463dbc05a7c188423bb45ffb2b210c789`.
- Wave 485 contract skeleton: blob `14cf0194504824a17569433d4478154eb44afc3f`.
- WB-05 authority options: blob `1b562c6546b1216f2ee89095cd6a78427a967dc5`.
- Wave 149 governance matrix: blob `9c1a02dc125b37abea9284f0c0aa5deb571f13e7`.
- Contour A ordered gates: [Issue #301](https://github.com/VlDMlNSh/mediahub-os/issues/301).
- Canonical map: [MEDIAHUB-CHAT-TREE-MAP.md](MEDIAHUB-CHAT-TREE-MAP.md).

**Disposition:** DRAFT NORMATIVE CANDIDATE / NOT ACCEPTED / NOT IMPLEMENTED / INDEPENDENT REVIEW NOT RUN.
