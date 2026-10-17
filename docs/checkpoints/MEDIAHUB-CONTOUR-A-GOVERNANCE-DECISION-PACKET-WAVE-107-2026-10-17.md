# MediaHub OS — Contour A Governance Decision Packet, Wave 107 (2026-10-17)

- Status: **DECISIONS REQUIRED / PROPOSED OPTIONS ONLY / NO AUTHORITY GRANTED**
- Repository: https://github.com/VlDMlNSh/mediahub-os
- Governing tracker: https://github.com/VlDMlNSh/mediahub-os/issues/301
- Working documentation branch: `docs/mediahub-broad-contour-a-wave105-20261017`
- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
- Related matrix: [Unified Contract and Project Traceability Matrix](MEDIAHUB-UNIFIED-CONTRACT-AND-TRACEABILITY-MATRIX-WAVE-01-2026-10-16.md), blob `099df3001a41ea7f86a54c032d254b55efd4c158`.
- Related Wave 106 report: [Contour A Acceptance-Matrix Engineering Wave 106](MEDIAHUB-CONTOUR-A-ACCEPTANCE-MATRIX-WAVE-106-2026-10-17.md).

## Purpose

Wave 106 mapped 14 Contour A acceptance conditions to sources and evidence. The source review confirms that several blockers are not missing code tasks: they are missing owner/governance decisions or accepted primary contracts. This packet makes those decisions explicit without silently selecting a protocol, assigning authority, or treating a recommendation as accepted.

**This packet is not normative.** It does not amend Baseline 2.0, select technology, authorize provider calls or workflow dispatch, define a deployed API, or qualify/deploy Contour A. Each decision requires a named accountable authority, decision ID, scope, approval date, source revision and rollout conditions.

## Decision D-CA-01 — Jarvis ↔ ASTRA A0 ingress and caller identity

- **Why blocked:** A0 source trace `docs/checkpoints/MEDIAHUB-A0-LIFECYCLE-MH12-CAPABILITY-ISSUER-SOURCE-TRACE-WAVE-07-2026-10-15.md`, blob `49ca0b69737bf8d44fe3a42daa47fd9157c9097d`, says the accepted API base/path, transport, protocol version, caller identity, wire schema and concrete authentication profile are not established.
- **Decision required:** identify the authority that owns the inter-system contract and approve the ingress protocol and trust boundary.
- **Options for evaluation, not selections:** (A) a narrowly scoped HTTPS API with explicit versioned request/response schemas and workload identity; (B) an authenticated GitHub-native event/dispatch contract where its execution and trust limits fit; (C) another explicitly documented transport. Each option must state its identity binding, replay controls, audit path, outage behavior and migration/rollback.
- **Must not be assumed:** an endpoint, token format, JWT/OAuth/OIDC/mTLS choice, signing algorithm, audience, expiry clock, issuer service, key store or public listener.
- **Acceptance evidence:** approved ADR/decision ID; exact versioned schema and endpoint/source SHA; authenticated caller tests; malformed, replayed, wrong-audience, expired and revoked request rejection; key rotation and audit linkage; compatibility and rollback plan.

## Decision D-CA-02 — Capability issuer, verification and revocation

- **Why blocked:** MH-12 source SHA `cf4ebfd5bf471ca676f075c51d3a24906504e490` requires explicit, auditable, fail-closed capability semantics bound to principal, issuer, operation, resource/target, scope, constraints, provenance, lifetime and revocation context. It does not itself select the issuer service or token representation.
- **Decision required:** approve the issuer principal/trust root, capability representation, signature/verification profile, audience and key lifecycle; define revocation propagation and authorization-unavailable behavior.
- **Options for evaluation, not selections:** signed scoped capability; established workload-identity token plus policy decision; or a different reviewed profile. Compare blast radius, offline verification, revocation latency, key custody, replay resistance, auditability and operational support.
- **Must not be assumed:** technology named in the MH-12 candidate list is not selected; schema references and fixture digests do not constitute live authority.
- **Acceptance evidence:** threat model and security review; pinned implementation/source and version; valid/invalid signature, wrong issuer/audience, scope mismatch, expiry, revocation, replay and policy-unavailable tests; measured revocation behavior; secret isolation; no permissive fallback.

## Decision D-CA-03 — Claim lease, fencing, cancellation and replay semantics

- **Why blocked:** A0 trace records a documentary lease TTL of 600 seconds and a maximum of three concurrent autonomous claims, but no accepted fencing generation, persisted claim schema, idempotency-key scope, deduplication retention, duplicate response or cancellation-race contract. Lease expiry alone does not fence a stale worker.
- **Decision required:** approve the claim/lease state machine and the commit fence that prevents a stale claimant from publishing a result after a newer claim has taken ownership.
- **Options for evaluation, not selections:** monotonic per-task generation enforced at result commit; store-backed compare-and-swap fencing; or another proven mechanism with equivalent stale-writer rejection. Define cancellation and artifact publication as explicit states.
- **Must not be claimed:** global exactly-once execution. Use at-least-once delivery with idempotent effects only if the design and tests actually prove that bounded contract.
- **Acceptance evidence:** state-machine ADR; storage schema and transition table; tests for duplicate delivery, lost heartbeat, lease expiry/reclaim, stale-generation commit rejection, cancellation racing completion, replay after recovery, bounded retries and terminal BLOCKED; exact CI/run/artifact evidence.

## Decision D-CA-04 — R-06 audit sink and privacy/availability policy

- **Why blocked:** R-06 crosswalk blob `099ad9f6a85bd4764dd16ccbfa9695c2abd6d5bd` states that the audit sink, registered event schema, durable-emission guarantee, approved clock, retention/deletion periods, residency/legal mapping, reader access and outage behavior are not accepted.
- **Decision required:** assign audit-event ownership; approve minimal event taxonomy and classified field allowlist; select sink and integrity/access controls; resolve retention, deletion, residency, clock/skew and export; define operation-specific behavior when audit is unavailable.
- **Options for evaluation, not selections:** durable append-only event service, protected object-backed evidence, or another qualified sink. Evaluate durability, integrity, privacy, access, bounded storage, deletion obligations and failure isolation.
- **Proposed safety baseline, pending approval:** no raw prompt, user/media payload or secret by default; bounded reason/result codes and opaque references; protect audit metadata itself as potentially sensitive. Protected result publication should not proceed without required pre-action decision evidence if the approved policy so requires.
- **Acceptance evidence:** governance decision and data classification; event schema registration; sink identity/version; access and integrity tests; retention/deletion/export proof; clock source/skew; fault-injection showing the accepted operation-specific outage disposition.

## Decision D-CA-05 — Exact clean runner/workspace/network target

- **Why blocked:** target reconciliation blob `1f748bf80e08067fd85a7e1b0821cc4d12bda676` found no owner-accepted exact clean target manifest. Hardware/OS/runtime, workspace isolation, network policy, storage and qualification evidence remain UNKNOWN; MH-15 is not accepted/frozen.
- **Decision required:** name the target-manifest owner and approve the exact GitHub-hosted runner/workspace profile, isolation boundary, toolchain, resource ceilings, allowed network destinations, storage/persistence and lifecycle.
- **Options for evaluation, not selections:** GitHub-hosted ephemeral runners with isolated job workspaces and strict egress/data-route controls; or another reviewed ephemeral execution profile. Do not assume fixed egress IP or a specific region.
- **Must not be assumed:** a component catalogue, proposed deployment contract, runner label or historical successful job is the accepted clean target.
- **Acceptance evidence:** versioned manifest and owner approval; source/provenance; workspace cross-job isolation; runtime-only secret injection; no credential persistence; allowed-egress tests; resource and timeout limits; cleanup and rollback; independent qualification report.

## Decision D-CA-06 — Promotion and operational authority

- **Invariant:** Jarvis coordinates corporation-level missions; ASTRA A0 owns only ASTRA-internal engineering workflow state; MediaHub Product State Authority alone mutates canonical MediaHub product state.
- **Decision required:** identify the approvers and evidence required for transitions from design → implementation → test → verification → qualification → release → deployment → production acceptance. Define which steps require independent review or human launch approval.
- **Acceptance evidence:** source-bound authority matrix, named accountable roles, transition preconditions, immutable evidence, rollback/exception records and negative tests proving no worker/agent/queue can self-promote or acquire product-state authority.
- **No promotion is implied by:** this packet, passing schema fixtures, a green workflow, a mergeable PR flag, or a documented queue entry.

## Required decision record format

For each D-CA-01…D-CA-06, record:

1. Decision ID, accountable authority and decision date.
2. Scope and accepted source revision(s); explicit supersession/compatibility rules.
3. Selected option and rejected alternatives with security/privacy/operational rationale.
4. Trust boundary, failure modes, default-deny behavior and recovery path.
5. Migration, rollback, versioning and observability/audit implications.
6. Required acceptance tests, evidence owner, independent reviewer and exact artifacts.
7. Explicit state: PROPOSED, ACCEPTED, REJECTED, SUPERSEDED or BLOCKED.

If the accountable authority cannot be identified from the accepted source set, mark owner **UNKNOWN** and keep the dependent gate blocked. Do not infer ownership from a GitHub username or the ability to modify a file.

## Current gate disposition

| Decision | State | Downstream gate |
|---|---|---|
| D-CA-01 ingress/caller contract | OPEN / UNKNOWN | External adapter and live admission blocked |
| D-CA-02 issuer/capability/revocation | OPEN / UNKNOWN | Authorization and provider/worker admission blocked |
| D-CA-03 fencing/cancel/replay | OPEN / UNKNOWN | Qualified claim/queue execution blocked |
| D-CA-04 R-06 audit/privacy | OPEN / UNKNOWN | Protected publication/qualification blocked per accepted policy |
| D-CA-05 target manifest | BLOCKED / UNKNOWN | Worker qualification and deployment blocked |
| D-CA-06 promotion authority | OPEN | Release/deployment/production acceptance blocked |

## Next execution after governance response

1. Bind each accepted decision to exact source SHA and update the unified matrix.
2. Implement only the smallest slice whose upstream contract is accepted.
3. Run negative tests first for deny, expiry, revocation, stale worker, replay, cancellation and audit unavailability.
4. Run exact-head CI and an explicitly authorized controlled read-only dispatch only after target and credential gates pass.
5. Publish run/job/artifact identifiers and digests; keep implementation, qualification and acceptance states separate.
