# MediaHub OS — Contour A WB-14T: ASTRA A0 ingress owner/governance decision packet

- Date: 2026-10-16
- Status: **DECISION OPTIONS / RECOMMENDATIONS ONLY / NO NEW OWNER DECISION / NOT IMPLEMENTED / NOT TESTED / NOT QUALIFIED**
- Repository: VlDMlNSh/mediahub-os
- Documentation ref: docs/mediahub-chat-tree-map-20261012
- Purpose: present only the unresolved A0 ingress decisions that materially affect authority, trust, replay safety, state ownership and schema interoperability. Preserve existing owner decisions; do not re-ask settled questions or select a technology by inference.

## 1. Executive result

WB-14S established a strict proposed operation family, ownership/mutability map and separate status domains. WB-14R reconciled source conflicts and showed that existing identity/capability/command/health schemas do not constitute an accepted Jarvis→ASTRA A0 wire contract. This packet advances the work by organizing the remaining blockers into decision-ready options with consequences and a bounded recommendation.

**No final JSON Schema, endpoint, protocol, issuer, credential profile, key store, database, broker, freshness threshold or lifecycle enum is selected here.** Recommendations below are not owner decisions. The proposed ingress remains design-only and must fail closed until its governing contracts are accepted.

### Recommended disposition

1. Retain the owner-approved DEC-DEV-02 split: Jarvis owns corporation-level mission coordination; ASTRA A0 owns ASTRA-internal engineering workflow lifecycle; Product State Authority alone owns canonical MediaHub product-state mutation.
2. Define a named, separately enrolled Jarvis caller principal and A0 receiver/service principal, with issuer/attester authority assigned through governance. Do not let the ingress adapter self-issue authority.
3. Keep authentication mechanism transport-neutral until security governance selects either a trusted transport-authenticated context or an explicitly signed request envelope; either path must provide equivalent caller, audience, integrity, freshness, replay and audit guarantees.
4. Require one A0-authoritative durable admission/idempotency commit boundary. A separate gateway may relay but must not maintain a shadow queue or independently accept missions.
5. Specify freshness semantics before choosing numeric limits; distinguish request expiry, clock skew, health challenge lifetime, revocation freshness, idempotency retention and evidence freshness.
6. Keep health probe outcome separate from service health, operation readiness, trust and authorization. Resolve the existing MH-06/domain health vocabulary discrepancy with its owners before final schema registration.

These recommendations minimize duplicated authority and premature technology lock-in. They do not close any blocker without owner/governance acceptance.

## 2. Live branch context and source anchors

At the start of this pass:
- `main` HEAD: `ab36db009d034db8dca723691e23b331322287e7`.
- `docs/mediahub-chat-tree-map-20261012` HEAD: `b49be25266e1dc5b4c9fe8cb7726d50d2ff4c3b8`.
- Compare: **DIVERGED**, docs ahead 1495 / behind 4; merge base `f0f406feb9f9816b009f4e6e756813541e53b9bc`.
- No merge, rebase, cherry-pick or main ref movement was attempted.

Sources read for this decision packet:
- Bootstrap instruction blob `a3c51f3ddf17827bf6193cce52387a5daad3b6e0`.
- WB-14S schema ownership/operation map blob `6b5159fdbe0c99d34e754047dd7c0a8afde8c61c`.
- WB-14R authority/schema crosswalk blob `dc827eb6ad53c03c0bb26a2989e4646f6f5a6b1d`.
- WB-03 ingress gap packet blob `e2f13fe8250fedef02b27bb221072b582db1f3d1`.
- WB-04 capability issuer lifecycle matrix blob `dac5e9eab9ec69ab7d15ac8eea45d7a1c8922387`.
- WB-05 issuer/authority decision packet blob `1b562c6546b1216f2ee89095cd6a78427a967dc5`.
- WB-07 ingress/command seam trace blob `89fab594f9a9ae9a729d63ecb14dad2543edc9af`.
- MH-12 security architecture blob `cf4ebfd5bf471ca676f075c51d3a24906504e490`.
- MH-06 Core Runtime Services blob `d118299a8828e65409fda4a0e6eaf926df40823b`.
- Domain health schema blob `8b85c4c1dd271ca53efb0e4b50fd8654e0f2d58e`.
- Owner-decision register blob `8a8847bfc6fd3885c8f87ed6212442098f11482a`.
- Owner decision/corporation direction record blob `70376a2709e055972ceddc4a280d26992977213c`.

These are documentation/source observations, not evidence of a deployed A0 endpoint, runtime identity, accepted security implementation or qualification.

## 3. Decision D-ING-01 — Jarvis/A0 service principal and capability issuer authority

### Established constraints
- Human and service principals are distinct; human privileges are not inherited automatically by a service.
- Identity, authentication, trust, capability and authorization are distinct concepts.
- A caller-provided `issuer` field or typed `AuthorizationContext` is not proof of trusted issuance.
- Capability authority must bind subject, issuer, audience, operation, target/resource, scope, constraints, provenance, lifetime and revocation context.
- Delegation may narrow but must not expand authority; unknown/unverifiable context fails closed.

### Options

| Option | Model | Benefits | Risks / obligations |
|---|---|---|---|
| A — Dedicated authority issuer | A governed issuer/attester issues scoped capability grants to enrolled service principals; A0 verifies issuer provenance and lifecycle. | Explicit trust root and revocation/delegation ownership; strongest separation between request transport and authority. | Requires owner assignment, enrollment, issuer lifecycle, verifier trust distribution and outage/revocation policy. No issuer product is implied. |
| B — Existing governed authority service | Reuse an already accepted MediaHub authority service if its contract demonstrably supports service principals, audience, target/scope, expiry, revocation and delegation. | Avoids introducing a parallel issuer and may reuse governance/audit. | Current source set does not establish a fully accepted, end-to-end issuer/verifier path for Jarvis→A0; reuse is conditional on evidence and explicit admission. |
| C — Caller-supplied typed context / static allow-list only | Caller sends principal/capability strings and A0 matches them against a local allow-list without a trusted issuer lifecycle. | Simple initial implementation. | **Not recommended for the normative ingress.** Does not establish provenance, audience, expiry, revocation or delegation; invites identity spoofing and stale grants. A local allow-list can be one policy input but cannot replace authentication and issuer-backed context. |

**Recommendation:** choose the authority model (A or evidenced B) through governance; reject C as a complete trust model. Until selected, issuer/attester and service enrollment remain OPEN. Do not create token fields or claim trusted context is implemented.

### Required decision record
- Issuer/attester authority and accountable owner.
- Jarvis caller principal and A0 receiver principal, audience binding and enrollment/revocation process.
- Grant subject, operation, resource/target, scope, constraints, provenance, expiry and delegation attenuation.
- Verification behavior when issuer/revocation source is unavailable.
- Audit evidence requirements and secret-safe logging boundaries.

## 4. Decision D-ING-02 — Authentication and integrity profile

### Options

| Option | Model | Benefits | Risks / obligations |
|---|---|---|---|
| A — Transport-authenticated caller context | A selected transport authenticates the peer and supplies a trusted principal/audience context to A0; application contract binds body digest, operation and request identity to that context. | Can avoid duplicate application-level signatures if peer identity and integrity guarantees are proven end-to-end. | Security review must prove the context cannot be forged by an untrusted proxy/caller, survives adapter boundaries safely, and binds the request bytes/digest to the authenticated peer. |
| B — Signed application request envelope | A defined signer creates a canonical request envelope; A0 verifies signer, audience, integrity, time/freshness and replay context. | Explicit portable request provenance across transport boundaries; useful where transport identity does not survive delegation. | Requires canonical serialization, algorithm/key registry, rotation/revocation, signing service, signature verification and anti-replay lifecycle. |
| C — Combine transport authentication and signed envelope | Both mechanisms are mandatory for each request. | Defense in depth and clear identity plus payload integrity. | Additional key lifecycle and operational complexity; may be redundant or create inconsistent identities unless threat model requires it. |

**Recommendation:** do not choose by convention. Security governance should approve A if an evidence-backed end-to-end authenticated context satisfies all required properties; otherwise choose B. Choose C only if the threat model identifies a distinct residual risk. The existing node-bound HMAC operational-command family and the separate generic signer are not candidate canonical Jarvis ingress contracts without a dedicated compatibility/security decision.

### Required profile properties, independent of mechanism
- Authenticated service identity, correct audience and operation/resource binding.
- Integrity binding to the exact canonical request digest.
- Expiry/freshness and replay detection.
- Key/credential rotation, revocation, unknown-key and verifier-unavailable behavior.
- Secret-safe audit and redaction.
- No implicit fallback to a weaker authentication route.
- Explicit separation of transport authentication from authorization and capability validity.

## 5. Decision D-ING-03 — Durable admission and idempotency authority

### Invariant
There must be one authoritative A0 admission/lifecycle boundary. An adapter or ingress gateway must not create a second queue, independently accept work, or report successful durable admission before the authoritative commit point.

### Options

| Option | Model | Benefits | Risks / obligations |
|---|---|---|---|
| A — A0-owned durable admission ledger | A0 atomically records canonical request digest, idempotency key, admission disposition and lifecycle reference at the accepted commit point. | Clear ownership; reliable duplicate detection and recovery; gateway remains stateless/relay-only. | A0 must define storage semantics, retention, consistency, recovery and handling of partial/uncertain commit. Storage technology remains open. |
| B — Separate admission service with delegated A0 authority | A dedicated service performs admission persistence only under an explicit A0-owned contract and fencing/transaction boundary. | Could isolate persistence concerns or support multiple ingress transports. | High coordination and split-brain risk; requires a formal single-writer/transaction contract proving no shadow queue and no divergent acceptance. |
| C — Best-effort in-memory deduplication or gateway-local store | Gateway tracks seen IDs locally and forwards work. | Low complexity. | **Not recommended.** Restart, replica or network failure can lose deduplication state; duplicate admission and ambiguous commit are unresolved. |

**Recommendation:** A. Consider B only with evidence that A0 remains the single logical authority and the commit/fencing semantics are explicit. Reject C for durable admission.

### Required idempotency contract
- Key scope and canonical payload-digest algorithm/serialization.
- Same key + same digest: return the existing admission/lifecycle reference without a second admission.
- Same key + different digest: reject a conflict; never overwrite the original request.
- Commit-point definition: exactly when the response may claim `ACCEPTED`.
- Timeout after possible commit: return an indeterminate disposition; query by existing key before retry.
- Retention and cleanup must not permit a still-valid replay to create duplicate work.
- Acknowledgement means durably admitted, not started, completed or qualified.
- Do not claim exactly-once execution or side effects; idempotent admission is not exactly-once execution.

## 6. Decision D-ING-04 — Freshness, expiry, nonce and revocation policy

Freshness is not one number. At minimum, distinguish:

1. Request validity window (`issued_at` / expiry or equivalent).
2. Allowed clock skew and clock-failure behavior.
3. Health challenge/nonce lifetime and single-use/replay behavior.
4. Capability validity and revocation-status freshness.
5. Idempotency/deduplication retention.
6. Evidence freshness and qualification freshness, owned by their existing contracts.

### Options

| Option | Model | Benefits | Risks / obligations |
|---|---|---|---|
| A — Per-contract bounded policy | Each owner defines limits for its semantic object; the ingress references versioned policy IDs. | Correctly separates security, health and evidence lifetimes; allows evidence-based changes. | More policy references and governance work; requires explicit clock and failure semantics. |
| B — One global freshness TTL | A shared TTL applies to requests, health challenges, revocation, idempotency and evidence. | Superficially simple. | **Not recommended.** These objects have different replay, availability and assurance requirements; one value creates either unsafe windows or unnecessary failure. |
| C — No expiry until later | Requests/capabilities remain valid absent explicit revocation. | Easy for prototypes. | **Not acceptable for a trusted ingress.** Stale requests and grants cannot be safely bounded; a delayed/replayed request may be admitted. |

**Recommendation:** A. Numeric thresholds must be set by the respective security, A0 lifecycle, health and evidence owners based on threat model and operational constraints. Do not copy old command age settings or the ASTRA evidence-freshness threshold into a new health nonce policy.

### Required policy semantics
- One canonical timestamp representation and explicit timezone/precision.
- Reject malformed or impossible timestamps; define allowed skew and missing-clock disposition.
- Nonce/challenge bound to request ID/digest, expected responder identity and one-use semantics.
- Explicit expiry/revocation checks at admission and any later authority-sensitive transition required by the contract.
- Behavior when revocation data is stale/unavailable: fail closed for authority-bearing operations unless an approved bounded grace policy explicitly says otherwise.
- Preserve evidence time, capture time and source revision separately; do not let a fresh response make stale underlying evidence fresh.

## 7. Decision D-ING-05 — Health/readiness vocabulary and probe response

### Source discrepancy
- The domain health schema (`schemas/domain/health.schema.json`, blob `8b85c4c1dd271ca53efb0e4b50fd8654e0f2d58e`) defines canonical entity health vocabulary.
- MH-06 Core Runtime Services and its health/readiness ADR define scoped health and operation-readiness semantics, with the ADR's health set including UNKNOWN, HEALTHY, DEGRADED, FAILED, QUARANTINED and readiness values UNKNOWN, NOT_READY, READY, DEGRADED, QUARANTINED.
- WB-14Q used lowercase handshake examples (`ready`, `not_ready`, `degraded`) for a proposed ingress probe.
- These are not yet reconciled into one accepted A0 health wire contract. MH-06 itself remains proposed pending full reconciliation/governance acceptance.

### Options

| Option | Model | Benefits | Risks / obligations |
|---|---|---|---|
| A — Separate probe outcome from health/readiness | HealthResponse has a narrow protocol/probe outcome plus distinct, optionally referenced health and operation-readiness values governed by their owners. | Avoids conflating reachability, authenticated identity, service health and operation readiness; allows source-specific status domains. | Requires explicit mappings and a rule for absent/not-applicable health/readiness fields. |
| B — Map all values into one universal enum | Convert transport, service health, operation readiness and trust into one status. | Simpler consumer code. | **Not recommended.** Loses semantics and encourages health-as-authentication/authorization inference. |
| C — Reuse the existing domain health enum only | Health probe returns the entity health value and no distinct protocol outcome/readiness. | Reuses an existing schema. | Cannot independently express challenge correlation, authentication failure, stale response, protocol error or operation-specific readiness. |

**Recommendation:** A. The probe outcome should report only whether the expected authenticated responder answered the fresh correlated challenge under the expected contract revision. Health and readiness should remain distinct typed fields/references under their own contract owners. A healthy response never grants authorization.

### Required health response semantics
- Echo/correlate request ID, fresh challenge/nonce and request digest.
- Identify the authenticated responder from trusted channel/security context, not from an untrusted response string alone.
- Include capture/response time and exact ingress contract/source revision.
- Reject stale/replayed challenge, wrong responder, mismatched digest or unsupported revision.
- Keep probe result, entity health, operation readiness, trust and authorization distinct.
- Define unavailable/unknown/not-applicable handling; never convert missing evidence into READY.

## 8. Cross-decision dependencies and proposed order

| Order | Decision | Must be accepted before |
|---|---|---|
| 1 | D-ING-01 principal, enrollment and issuer/attester authority | Normative capability/auth-context schema and trust-boundary implementation |
| 2 | D-ING-02 authentication/integrity profile | Normative authenticated request envelope and verification implementation |
| 3 | D-ING-03 A0 admission commit and idempotency ownership | ACCEPTED response semantics, retry behavior and persistence implementation |
| 4 | D-ING-04 freshness/expiry/replay policies | Timestamp/nonce/capability fields and freshness verifier implementation |
| 5 | D-ING-05 health/readiness mapping | Final HealthChallenge/HealthResponse schema and readiness gate mapping |
| 6 | Schema ownership/version/registry rules | Registration of versioned Draft 2020-12 schemas |
| 7 | Cancellation/fencing/late-result transitions | Normative cancellation/status/result transition schemas and A0 lifecycle adapter |

Some decisions may be reviewed in parallel, but schema finalization must not silently pick defaults to unblock implementation. No transport is selected by this packet.

## 9. Stable operation family retained from WB-14S

The following are separate proposed contract shapes, not registered schema IDs or implemented APIs:

- `SubmitRequest → AdmissionResponse`
- `StatusQueryRequest → StatusResponse`
- `CancelRequest → CancelResponse`
- `ResultQueryRequest → ResultResponse`
- `HealthChallenge → HealthResponse`

The schema family must distinguish:
- admission disposition;
- A0 lifecycle state;
- attempt outcome;
- independent verifier disposition;
- qualification gate state;
- probe outcome;
- entity health;
- operation readiness;
- trust state;
- authorization decision.

No single generic `status` field may collapse these domains. Mission/task DAG intent comes from Jarvis; A0 owns its internal lifecycle; executor output is untrusted until independently checked; canonical product state remains with Product State Authority.

## 10. Decisions that must not be reopened or inferred here

- DEC-DEV-02's lifecycle split is owner-approved. This packet does not reverse it or use the route-adapter A/B/C labels to rename it.
- No silent cloud fallback in local-only mode remains a binding invariant.
- Contour A must be deployed and independently accepted before Contour B product development.
- Old host/node identities and paths are historical only, not target topology.
- Baseline 2.0 remains the canonical functional baseline; Baseline 1.0 is historical.
- The current branch divergence is not authorization to merge or rewrite main.
- No option in this packet becomes accepted merely because it is recommended.

## 11. Owner/governance response template

Record each choice in the established owner/governance register and the appropriate ADR/contract. Preserve stable IDs; do not mark a choice accepted until the owner/governance authority explicitly approves it.

| Decision | Recommendation | Owner response / accepted choice | Conditions/evidence required |
|---|---|---|---|
| D-ING-01 principal + issuer | Dedicated governed issuer (A), or evidenced reuse (B); reject typed context alone (C) | **OPEN** | Named authority/owner, principal enrollment, delegation/revocation and verifier lifecycle |
| D-ING-02 authentication/integrity | A if end-to-end trust is evidenced; otherwise B; C only if threat model requires | **OPEN** | Security ADR, authenticated audience, digest binding, freshness/replay and key/credential lifecycle |
| D-ING-03 admission/idempotency | A0-owned durable ledger (A) | **OPEN** | A0 single-authority commit point, key/digest rules, uncertain-commit recovery and retention |
| D-ING-04 freshness | Per-contract policy (A) | **OPEN** | Security/A0/health/evidence owner limits and clock/revocation failure semantics |
| D-ING-05 health/readiness | Separate probe outcome and health/readiness (A) | **OPEN** | MH-06/domain-owner mapping and explicit status ownership |

This table is a decision worksheet, not a request to interrupt all work. Continue independent source reconciliation and schema ownership work while choices remain open; do not implement the blocked trust/admission path.

## 12. Verification boundary and next step

Completed:
- Refreshed current Git refs and branch comparison.
- Read bootstrap, WB-14S, WB-14R, WB-03/04/05/07, MH-12, MH-06, domain health schema and owner-decision artifacts.
- Converted unresolved issues into option/consequence tables and explicit dependencies.
- Preserved existing owner decisions and kept all new options OPEN.

Not performed:
- No tests, validators, security scans, qualification, workflow dispatch, model/provider calls, credentials, host/runtime inspection, installs, infrastructure change, deployment, migration, merge, rebase or cherry-pick.
- No normative contract, schema, code or configuration was modified.
- No runtime availability, readiness, qualification or acceptance is claimed.

Next bounded step: **WB-14U — source-only closure of health/readiness vocabulary ownership and lifecycle-status transition ownership**, using existing MH-06/domain schema and A0 lifecycle sources. If the conflicting status vocabularies cannot be reconciled from accepted source, record a precise owner decision rather than selecting an enum. In parallel, preserve D-ING-01…05 as OPEN pending explicit approval.

- Project map: [MEDIAHUB-CHAT-TREE-MAP.md](../architecture/MEDIAHUB-CHAT-TREE-MAP.md).
