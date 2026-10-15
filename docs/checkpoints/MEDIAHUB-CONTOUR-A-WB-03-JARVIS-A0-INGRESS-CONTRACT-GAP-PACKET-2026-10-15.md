# MediaHub OS — Contour A WB-03 Jarvis → ASTRA A0 Ingress Contract Gap Packet

- Date: 2026-10-15
- Status: **SOURCE-BOUND GAP ANALYSIS / DESIGN ONLY / NOT NORMATIVE / NOT IMPLEMENTED / NOT ACCEPTED**
- Scope: WB-03; one bounded source-only pass.
- Ref: `docs/mediahub-chat-tree-map-20261012`
- Purpose: specify what an accepted Jarvis→A0 ingress contract must decide, without choosing endpoints, protocols, credential formats or authority semantics on behalf of the owner.

## 1. Current result

The source set documents responsibility and security invariants, but **does not establish an accepted end-to-end Jarvis→ASTRA A0 ingress edge**. No dispatch implementation or operational route is inferred. The existing GitHub adapter contract and corporation mission/task/result schemas remain drafts.

## 2. Live source anchors read

| Source | Ref / blob SHA | What it establishes | What it does not establish |
|---|---|---|---|
| `docs/checkpoints/MEDIAHUB-CONTOUR-A-CONTROL-PLANE-INTERFACE-EDGE-TRACE-WAVE-10-2026-10-15.md` | docs branch / `540bdccde6bb53f570dd6ef96718eddf25f50375` | E-02 Jarvis→A0 is blocked; E-07 verifier/issuer lifecycle open; result/fencing gaps | No accepted API or runtime wiring |
| `docs/checkpoints/MEDIAHUB-JARVIS-ASTRA-IDENTITY-LIFECYCLE-CONTRACT-TRACE-WAVE-05-2026-10-15.md` | docs branch / `dc60ccc0af29a74ca3cf88584d66821350b20b9f` | A-01 ingress, A-02 capability lifecycle, A-03 task/result and A-04 authority wording are open/draft | No accepted wire contract |
| `docs/checkpoints/MEDIAHUB-A0-LIFECYCLE-MH12-CAPABILITY-ISSUER-SOURCE-TRACE-WAVE-07-2026-10-15.md` | docs branch / `49ca0b69737bf8d44fe3a42daa47fd9157c9097d` | Existing context/capability typing is not proof of issuance or caller wiring; P0-07→P0-05 edge not established in its traced subsystem | No issuer, attestation, revocation or accepted cross-domain handoff |
| `docs/architecture/MH-12-security-architecture.md` | docs branch path / main-origin blob `cf4ebfd5bf471ca676f075c51d3a24906504e490` | Canonical path: integration boundary → consumer contract → identity → authentication → trust → capability → authorization → policy → consumer boundary → State Authority; fail-closed | Technology choices remain UNKNOWN pending evidence and ADR; governance review required |
| `docs/checkpoints/MEDIAHUB-JARVIS-CONTROL-PLANE-GITHUB-ADAPTER-CONTRACT-DRAFT-01-2026-10-14.md` | docs branch / `e112cc73178eef5f71b8a814296e4902c2e80390` | Draft intent, proposed mission envelope, lease/evidence boundaries and acceptance gates | Explicitly a draft; cannot be promoted by inference |
| `docs/checkpoints/MEDIAHUB-CHAT-TO-GITHUB-OWNER-DECISIONS-AND-CORPORATION-DIRECTION-WAVE-01-2026-10-15.md` | docs branch / `70376a2709e055972ceddc4a280d26992977213c` | Owner-approved DEC-DEV-02 Option C and hybrid-routing direction | Does not choose ingress API, authentication profile, capability issuer or wire schemas |

## 3. Boundary and authority invariant

- **Jarvis** coordinates corporation-level missions and tracks outcomes through accepted interfaces.
- **ASTRA A0** alone owns ASTRA-internal queue/claim/lease/heartbeat/retry/cancellation/recovery and ASTRA evidence/gate transitions under its accepted contract.
- **MediaHub Product State Authority** remains the sole canonical Contour B product-state mutation authority.
- Jarvis must not write A0's internal queue/claim state directly or create a shadow ASTRA queue.
- An accepted ingress request does not by itself authorize an executor, a provider route, a canonical product-state mutation or a release/deployment transition.
- Missing/ambiguous identity, authentication, trust, capability, authorization, policy, replay/fencing or authority state must fail closed.

## 4. Contract decision matrix

Every row is a required contract decision; entries under “minimum closure” are requirements to resolve, not selected implementation technology.

| ID | Contract surface | Minimum closure needed before implementation | Current status |
|---|---|---|---|
| I-01 | Interface ownership | Named service principal/owner for Jarvis caller and A0 receiver; explicit authority boundary; lifecycle/version owner | OPEN |
| I-02 | Transport and endpoint | Accepted protocol, endpoint/service discovery, trust boundary, TLS/channel requirements, versioning and compatibility | UNKNOWN / OWNER-GOVERNANCE INPUT |
| I-03 | Caller identity and authentication | Principal type, enrollment/rotation/revocation, peer/request authentication, authentication failure behavior | OPEN; technology UNKNOWN |
| I-04 | Trust and capability | Explicit issuer/attester authority; capability subject, issuer, operation, resource, scope, constraints, provenance, lifetime and revocation context; attenuation and delegation rules | OPEN; no issuer accepted |
| I-05 | Authorization and policy | Operation/resource-specific decision, policy source/revision, deny precedence, decision attribution and fail-closed behavior | OPEN |
| I-06 | Request envelope | Versioned mission submission envelope, stable IDs, target/base SHA, constraints, deadline/budget, classification, acceptance criteria and correlation/audit IDs | DRAFT ONLY; schema governance open |
| I-07 | Acknowledgement and errors | Distinguish transport receipt from accepted/queued/rejected; stable error taxonomy; retryability and safe disclosure | OPEN |
| I-08 | Replay and idempotency | Request identity, bounded deduplication scope/retention, same-key/same-digest behavior, conflicting-digest behavior and replay audit | OPEN |
| I-09 | A0 lifecycle handoff | A0-owned queue insertion, claim/lease state, cancellation, retry and recovery semantics; Jarvis cannot mutate them directly | Existing ASTRA semantics partial; ingress handoff OPEN |
| I-10 | Result/status return | Accepted result/event/status contract, cursor/replay rules, immutable evidence links, duplicate/conflicting result behavior | DRAFT ONLY / BLOCKED |
| I-11 | Fencing and stale workers | A0-authoritative lease generation/fencing, stale-writer rejection, worker stop/renew behavior, timeout and recovery interaction | OPEN |
| I-12 | Audit and secrets | Who/when/operation/target/policy/result evidence; correlation without logging tokens, secrets, private keys or session material | Requirements documented; event schema OPEN |
| I-13 | Route/executor selection | Separate identity for executor, gateway, provider, model and egress; admission policy and LOCAL_ONLY fail-closed behavior | Separate contract; not granted by ingress |
| I-14 | Failure and availability | Authority/verifier unavailable, malformed request, expired/revoked capability, policy unknown, A0 unavailable and partial response behaviors | Fail-closed invariant known; detailed contract OPEN |
| I-15 | Change governance | Accepted normative source set, versioned schemas, historical ID collision review, compatibility/deprecation and rollback policy | OPEN |
| I-16 | Verification and acceptance | Contract tests and negative security cases, independent verifier, target-SHA-bound evidence, separate authorization for test/qualification | NOT AUTHORIZED / NOT RUN |

## 5. Required request lifecycle — logical only

The following is a **review checklist, not a selected protocol/state machine**:

1. Receive a request at the approved integration boundary.
2. Establish the caller principal and authenticate the request.
3. Establish trust and validate issuer-backed, operation/resource-bound capability context.
4. Evaluate explicit authorization and policy; deny safely on ambiguity.
5. Validate schema/version, stable identity, target/base revision, constraints and acceptance criteria.
6. Apply bounded replay/idempotency checks before creating an A0-owned lifecycle item.
7. Let A0 perform its own authoritative queue/lifecycle transition; return a response that distinguishes receipt from accepted disposition.
8. Publish status/results only through an accepted result interface; reject stale or conflicting publishers using A0-owned fencing.
9. Emit auditable, secret-safe evidence bound to request, decision, target and result.
10. Keep qualification, release, deployment and independent acceptance as separate transitions.

The exact order of transport-level authentication and application-level validation, as well as all state names and response fields, must be specified by the accepted contract. This list does not claim those steps are implemented.

## 6. Negative cases required in a future authorized verification plan

No tests were run. Before implementation can be accepted, the contract owner should require explicit outcomes for:
- unknown/un-enrolled caller; authentication failure; revoked identity;
- absent, malformed, expired, revoked, wrong-audience, wrong-resource or overbroad capability;
- delegated capability with expanded authority or missing issuer provenance;
- unknown policy revision or unavailable authorization authority;
- duplicate request with identical digest and duplicate request with conflicting digest;
- stale correlation/request timestamp or replay outside the permitted window;
- malformed/unsupported schema version or conflicting stable ID;
- A0 unavailable before and after durable acceptance, lost acknowledgement, retry after timeout;
- cancellation racing with claim/lease renewal or result publication;
- stale worker attempting a write after lease expiry/reassignment;
- duplicate or conflicting result publication and unavailable evidence store;
- secret/token material accidentally present in ordinary logs or result payload;
- LOCAL_ONLY request with no eligible local executor, ensuring no silent cloud fallback.

These are verification requirements to design later, not test results.

## 7. Decisions required vs. technology not to invent

**Owner/governance decisions required:** ingress ownership and service principal; accepted trust boundary; mission submission semantics; authoritative request/response and status schemas; replay/idempotency policy; capability issuer/attester authority and revocation semantics; fencing/publication authority; compatibility and acceptance gates.

**Not selected by this packet:** HTTP/gRPC/queue protocol; OAuth/OIDC/JWT/mTLS or any other credential/profile; key storage; endpoint/port; token fields beyond MH-12 semantic constraints; database/event broker; issuer product; cloud/local provider. These remain UNKNOWN until evidence and ADR/governance decisions.

## 8. Branch and verification boundary

Live GitHub compare at this pass: `main` HEAD `608d7463011798ca75e36bfce4b749a9caf4f9a0`; documentation branch `docs/mediahub-chat-tree-map-20261012` is DIVERGED, 1369 ahead / 3 behind; merge base `f0f406feb9f9816b009f4e6e756813541e53b9bc`. No integration performed.

Read-only source inspection and documentation writes only. No tests, installations, provider/model calls, credentials, host/runtime inspection, security scan, qualification, infrastructure change, deployment, merge, rebase or cherry-pick occurred. No normative contract was changed. This packet is not an accepted API, implementation, qualification or deployment claim.

## 9. Next bounded step

WB-04: source-only capability issuer / trusted-context lifecycle closure matrix, cross-referencing MH-12, A0 lifecycle trace and the current source-code seams without treating a typed context as proof of issuance or caller wiring. Keep ingress blocked until the dependent authority and schema decisions are accepted.

Project map: [MEDIAHUB-CHAT-TREE-MAP.md](../architecture/MEDIAHUB-CHAT-TREE-MAP.md)
