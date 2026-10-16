# MediaHub OS — Contour A WB-14Z: ASTRA A0 ingress source-contract census

- Date: 2026-10-16
- Status: **BOUNDED SOURCE CENSUS COMPLETE / CANONICAL A0 INTERNAL POLICY FOUND / JARVIS-FACING CONTRACT NOT ESTABLISHED / NO IMPLEMENTATION**
- Scope: inspect the exact current A0-facing contract references identified by WB-14B, Wave 07 and the Jarvis adapter draft; distinguish reusable internal workflow policy from an accepted external ingress API.
- Boundary: documentation-only. No endpoint, transport, schema ID, issuer, TTL or implementation selected.

## 1. Result

The reviewed sources support the **intended authority model** and describe ASTRA-internal workflow semantics, but do not provide an accepted Jarvis → ASTRA A0 wire/API contract.

The best-evidenced current ingress in code is a local file-based Task Contract consumer. A separate signed operational-command workflow exists. Neither path is proven to be the accepted Jarvis mission producer-to-A0 consumer chain. The Jarvis Control Plane/GitHub Adapter document remains a design draft and explicitly refuses to invent the API, issuer or queue interface.

This is now a precise design gap, not a reason to ask again who owns each lifecycle:
- DEC-DEV-02 Option C is owner-approved: Jarvis coordinates corporation missions/routes; ASTRA A0 owns ASTRA-internal workflow state; Product State Authority alone mutates canonical product state.
- The owner decision settles the broad lifecycle split, but not the concrete A0 API, service principal, trusted issuer, admission semantics or state/result vocabulary.
- Route A (Jarvis → A0 engineering ingress) remains distinct from Route B (P0-07 → P0-05 → P0-04 product-state mutation), as WB-14Y explains.

## 2. Exact source matrix

| Source | Ref / blob SHA | What is actually established | What cannot be inferred |
|---|---|---|---|
| Jarvis Control Plane and GitHub Adapter Contract Draft 01 | Documentation ref / `e112cc73178eef5f71b8a814296e4902c2e80390` | Draft roles, mission-field inventory, narrowly scoped GitHub adapter intent, audit expectations and fail-closed routing principles | Not accepted/implemented/qualified; no endpoint, protocol, canonical schema, issuer or A0 queue interface |
| WB-14B Jarvis-to-A0 Ingress Caller and Authority Seam Trace | Documentation ref / `25e8416db8e5a8ae81557ac5b4d8c0314b906893` | Local JSON Task Contract → `FileTaskIngress` → `AstraGatewayRuntime.run_bounded`; separate signed operational-command workflow | No tracked Jarvis producer, accepted service ingress, trusted issuer-backed context, or linkage from command verifier to task-ingress/auth path |
| Wave 07 A0 Lifecycle and MH-12 Capability Issuer Source Trace | Documentation ref / `49ca0b69737bf8d44fe3a42daa47fd9157c9097d` | ASTRA internal queue/claim/lease/recovery/idempotency semantics; MH-12 capability trust constraints; target-SHA/evidence practices | No accepted Jarvis-facing API, concrete issuer lifecycle, fencing contract, cancellation races or corporation-wide DAG/result schema |
| ASTRA Executor Capability Matrix | Documentation ref / `9ad83781a8da53d1a8f540ede54eba95281f01c0` | Canonical executor-workflow policy scopes A0 to ASTRA workflow/control state, claim/lease/evidence/gate transitions; expressly excludes canonical product-state authority | Documentation branch wording does not establish that the same source-text correction is integrated into `main`; policy does not expose the Jarvis API |
| ASTRA GOLD Unified Autonomous Development System | `main` / `e2067dc41b52983fc4e0b2549fb6af3c099cbc60` | Canonical design describes internal queue → claim → lease → dispatch → heartbeat → result → recovery; source details include internal limits/policies | No external Jarvis ingress contract; “canonical/qualification-ready design” is not evidence of deployed runtime or of an accepted wire API |
| ASTRA GOLD Governance Contract | `main` / `1d3ac25e7817f365807ad85d0d7c9007bd48bebf` | Governance source has internal lease/heartbeat/timeout/retry and concurrency values | Those internal values do not define ingress request freshness, capability expiry, health-probe TTL or idempotency retention; numeric configuration is not runtime evidence |
| Owner decision packet | Documentation ref / `54900eeb040e2aa0209e02629fedc2f2fe2e487e` | §8 records DEC-DEV-02 Option C OWNER-APPROVED on 2026-10-15 | Approval does not implement or accept the A0 API, caller identity/issuer or request/result schemas |

## 3. Existing paths and trust-boundary distinction

### 3.1 Local file-based task ingress

WB-14B pins `runtime/mediahub_runtime/task_ingress.py` on `main` to blob `59e1254aa61cc8f55f53bd1e179631e81c441393` and `runtime/mediahub_runtime/astra_gateway.py` to `10985e4ad8f682313d08e7492ecc1856a8bce20f`. The trace shows file enumeration, shape/schema handling and bounded gateway execution. It does not trace an authenticated Jarvis writer, OS-level writer authorization, or an accepted network/service ingress. It remains an internal adapter candidate until its producer/trust boundary is explicitly accepted.

### 3.2 Signed operational-command path

WB-14B pins `astra_github_agent.py` and the supervisor/chat-control workflows and establishes a separate operational-command path with its own envelope, signature/freshness checks and command dispatch. The trace does not connect that verifier to FileTaskIngress or establish that its node-bound HMAC format is the canonical Jarvis mission contract. Do not merge the two trust domains by implication.

### 3.3 Internal A0 policy vs caller contract

The ASTRA governance contract and executor matrix supply useful A0-owned lifecycle semantics. Reuse them as constraints. Do not infer the external caller request/ack/status/result/cancel protocol, durable admission commit response, fencing token, or issuer lifecycle from the internal queue model alone.

Internal numeric values (for example lease or retry thresholds) stay in their current scope. Do not reuse them automatically as external token expiry, request TTL, challenge lifetime or deduplication retention.

## 4. Minimal requirements for the missing accepted interface

Before implementation, the accepted Jarvis → A0 contract must define at least:

1. **Contract ownership/version:** exact API/schema path, revision, compatibility rules, source SHA and acceptance authority.
2. **Principal and authorization:** caller and receiver principals, trusted issuer/attester, audience, operation/resource/scope, target SHA/digest binding, expiry/freshness, revocation, replay and audit. A caller-provided string or `AuthorizationContext(principal, capability)` shape is not issuer evidence.
3. **Admission/idempotency:** authoritative A0 commit boundary, idempotency key and digest rules, duplicate response, uncertain-commit reconciliation, retention ownership and ACK semantics.
4. **Lifecycle/fencing:** link accepted request identity to queue claim/lease, monotonic fencing/generation and result commit preconditions, cancellation races, late-result handling, retry/recovery and terminal-state rules.
5. **Status/result/evidence:** distinct admission disposition, A0 lifecycle status, attempt outcome, independent verification/gate status and health/readiness/trust/authorization. Bind result to target/source SHA, artifact references, producer identity and contract/policy revisions.
6. **Health probe:** if included, separately specify challenge/correlation, expected responder identity, freshness and probe outcome; do not treat transport liveness as entity health, operation readiness or authorization.
7. **Failure behavior:** fail closed on unknown identity, invalid/unverifiable issuer, stale/replayed request, ambiguous commit, fencing mismatch, unavailable policy/authority or conflicting result. No implicit cloud fallback and no Product State Authority bypass.

This is an acceptance-criteria inventory, not a newly accepted schema or selection of transport/crypto/storage.

## 5. Separate product-mutation gate

The P0-07 → P0-05 → P0-04 path remains its own workstream:
- P0-07 caller/adapter edge to P0-05: NOT ESTABLISHED by the reviewed source set.
- P0-05 baseline contract exact-text/header issue: historical contract blob `bba8dd3e8812767b6dbc8afff1bec5bd36dc828b` at commit `303a766257b90c4356dcffc8967a5574e8e22e7` says DRAFT; owner decision record requires explicit governance confirmation before any protected header/status correction.
- The owner has not selected P0-05 v1.1 as normative; its candidate remains NON-NORMATIVE / NOT ACCEPTED / NOT FROZEN.
- Product mutation remains blocked behind the product route’s own accepted caller/consumer/authority contracts. A0 cannot create an alternate mutation path.

## 6. Disposition and next step

**Reuse:** DEC-DEV-02 Option C; ASTRA internal queue/claim/lease/retry/cancel/recovery/evidence-gate policy; MH-12 fail-closed identity/capability boundaries; target-SHA/evidence controls.

**Do not reuse without a new accepted contract:** local-file ingress as proof of a Jarvis caller, operational-command signature as Jarvis mission authorization, internal lease/retry values as external freshness/idempotency policy, P0-05/P0-07 product-mutation context as A0 service identity, or an internal A0 lifecycle enum as the public status enum.

The next permitted design step is to prepare a transport-neutral **A0 ingress contract candidate** with the seven requirement groups above, explicit unresolved decisions and exact source traceability. Keep it marked PROPOSED / NOT ACCEPTED. Do not create registered schema IDs or implement until issuer/authority, owner and versioning decisions are accepted. No tests, validators, installations, credentials/provider calls, host/runtime inspection, infrastructure changes, deployment, migration, branch integration or qualification were performed.

- Project map: [MEDIAHUB-CHAT-TREE-MAP.md](../architecture/MEDIAHUB-CHAT-TREE-MAP.md).
