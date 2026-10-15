# MediaHub OS — Contour A WB-14D: Cross-Route Lifecycle Controls and Evidence Reconciliation

- Date: 2026-10-15
- Status: **READ-ONLY CONTRACT CROSSWALK / NON-NORMATIVE / OWNER DECISIONS OPEN / NOT IMPLEMENTED / NOT QUALIFIED**
- Parent sequence: WB-14A source baseline; WB-14B ingress/authority seam; WB-14C ASTRA queue vs Route B.
- Scope: reconcile identity, idempotency, lifecycle ownership, lease/fencing, cancellation, retry, recovery and result provenance across Jarvis, ASTRA A0 and the proposed direct-local route. This pass reuses existing documentation rather than creating a new normative contract.

## 1. Result

The repository already contains a useful **non-normative technical baseline** for mission/task/result lifecycle semantics in `MEDIAHUB-CORPORATION-TASK-RESULT-TECHNICAL-BASELINE-WAVE-09-2026-10-15.md` and a **schema draft** in `MEDIAHUB-CORPORATION-MISSION-TASK-RESULT-SCHEMA-SET-DRAFT-01-2026-10-15.md`. WB-14D does not duplicate those artifacts or promote them to accepted contracts.

Across the reviewed sources, three authority domains must remain distinct:

1. **Jarvis:** corporation-level mission coordination, bounded decomposition, permitted route selection, progress and reporting.
2. **ASTRA A0:** sole writer of ASTRA-internal queue, claim, lease, heartbeat, retry/cancellation and ASTRA evidence/gate state within its accepted scope.
3. **MediaHub Product State Authority:** sole canonical product-state mutation authority in Contour B.

A direct-local executor, worker, gateway or model is not a fourth state authority. A proposed Route B still lacks an accepted lifecycle owner, caller-authenticated ingress, cross-route admission/fencing contract and qualified backend. Therefore no common end-to-end lifecycle can currently be claimed as implemented.

## 2. Source pins reviewed

| Artifact | Ref / blob SHA | Relevance and limit |
|---|---|---|
| `MEDIAHUB-CORPORATION-TASK-RESULT-TECHNICAL-BASELINE-WAVE-09-2026-10-15.md` | docs branch / `6ab5f244cb0d4e74ac2b26013c02502832170365` | Recommends distinct mission/task/attempt IDs, bounded durable idempotency, fencing, cancellation state, bounded retries, authoritative recovery and provenance-rich results. Explicitly not normative. |
| `MEDIAHUB-CORPORATION-MISSION-TASK-RESULT-SCHEMA-SET-DRAFT-01-2026-10-15.md` | docs branch / `e6c65c9949f45d247a2a57d1806da33737060619` | Candidate schema field sets; explicitly leaves ingress, issuer, A0 fencing primitive, cancel/complete race and schema registry unresolved. |
| `MEDIAHUB-DISTRIBUTED-TASK-DAG-AND-RESULT-CONTRACT-CROSSWALK-WAVE-01-2026-10-15.md` | docs branch / `9cf876b094278b4b2de9851cc488a5b3dabc147b` | Existing components cover narrower purposes; no accepted corporation-wide DAG/result wire contract. A0 remains sole writer of its internal lifecycle state. |
| `MEDIAHUB-JARVIS-ASTRA-IDENTITY-LIFECYCLE-CONTRACT-TRACE-WAVE-05-2026-10-15.md` | docs branch / `dc60ccc0af29a74ca3cf88584d66821350b20b9f` | Identifies unresolved Jarvis ingress, issuer/delegation/revocation and corporation task/result envelope. |
| `MEDIAHUB-JARVIS-ASTRA-LIFECYCLE-AUTHORITY-SECURITY-CROSSWALK-WAVE-03-2026-10-15.md` | docs branch / `bb96e35ba518ef1527f5a8d0c5699ed0b4c64b9c` | Records conflicting historical “single coordination and state authority” wording; requires controlled reconciliation, not an inferred authority change. |
| `runtime/mediahub_runtime/autonomous_queue.py` | main / `72c4a5ccb367884fb02d247b1b8848ea62c3c6b1` | Existing ASTRA queue uses fixed executor pool and explicit `github_remote_claude_only` mode; no local executor fallback in this queue path. |
| `runtime/mediahub_runtime/agent_fabric.py` | main / `3c70dda5df8c6caa9411201d754ead6b3bfdf6dd` | Claim store provides claim conflict, expiry, heartbeat and release primitives; not a full cross-route mission state machine. |
| WB-14B ingress trace | docs branch / `25e8416db8e5a8ae81557ac5b4d8c0314b906893` | No end-to-end Jarvis producer → accepted A0 ingress → trusted issuer chain established in the bounded trace. |
| WB-14C queue comparison | docs branch / `ceff02cdaf0f02b40a1822ca54a9127ccd542c60` | Alamo absent from fixed ASTRA pool; separate Route B queue/lifecycle not evidenced. |

## 3. Cross-route control matrix

| Control | Reconciled source-backed position | Status / gap |
|---|---|---|
| Mission identity | Existing sources use different identifiers (e.g. request ID, command ID, task ID). Wave 09 recommends distinct opaque mission/task/attempt IDs. | **PARTIAL** — no accepted shared namespace, collision check or wire schema. |
| Idempotent admission | Wave 09 recommends durable admission keyed to authenticated principal, operation, resource, schema revision and payload digest; same key/digest returns original admission, different digest conflicts. | **PROPOSAL ONLY** — issuer/principal, persistence, retention and accepted ingress are unresolved. No exactly-once side-effect guarantee. |
| Lifecycle ownership | Jarvis coordinates missions; A0 owns ASTRA-internal queue/claim/lease/retry/cancellation/gate state; Product State Authority owns canonical product state. | **SOURCE-ALIGNED BOUNDARY** — historical broad A0 authority wording still needs controlled reconciliation; no direct Route B owner selected. |
| Lease/fencing | Existing claim store supports expiry and heartbeat. Wave 09 recommends storage-enforced monotonically increasing claim generation or equivalent fencing, checked on every state-changing completion/publication. | **GAP** — lease expiry alone is not fencing; accepted A0 persistence/publication primitive not established in this trace. |
| Cancellation | Wave 09 recommends separating cancel request, acknowledgement and terminal disposition; preserve evidence and reject stale late publication under current ownership rules. | **PROPOSAL ONLY** — exact cancel/complete race and Route B cancellation protocol remain open. |
| Retry | ASTRA governance defines its own bounds; Wave 09 recommends a new attempt ID per retry under the same task, bounded by policy. | **SCOPE-LIMITED** — ASTRA constants must not be copied as corporation-wide defaults; retryability and side-effect replay remain executor/policy specific. |
| Restart recovery | ASTRA source has claim expiry and recovery-related behavior; Wave 09 recommends reconciliation from authoritative persisted state and immutable evidence. | **PARTIAL** — no independently owned Alamo recovery/cleanup contract. |
| Result provenance | Wave 09 recommends binding mission/task/attempt, route, executor, provider/model mode, input/source revision, artifact digests, checks, limitations and verifier disposition. | **PROPOSAL ONLY** — no accepted shared result envelope or route adapter; worker output is not self-verifying. |
| Route/egress decision | Route selection should record policy revision, locality, data class, egress, provider/gateway/model and fallback disposition. LOCAL_ONLY must fail closed. | **OPEN** — actual Alamo host and inference/backend mode remain unknown. |
| Product-state authority | Distributed compute may produce data/evidence but cannot independently mutate canonical product state. | **INVARIANT** — no second State Authority. |

## 4. Required ordering before implementation

1. Resolve the exact normative authority wording conflict through the existing owner/governance process; do not silently rewrite primary contracts.
2. Source and accept Jarvis→A0 ingress, caller identity, capability issuer/delegation/revocation and acknowledgement/error semantics.
3. Accept versioned corporation mission/task/result schemas and their ID namespace/compatibility policy; the current schema set is a draft.
4. Define A0's authoritative admission record and storage-enforced fencing/publication rule before promising cross-route idempotency.
5. If the owner later selects Route B, separately name its lifecycle owner and define queue persistence, executor identity, claim/lease/fencing, retry, cancellation, recovery and result adapter. This WB does not select Route B.
6. Admit local-only media work only after host identity, backend/provider mode, data egress, resource envelope, isolation and independent qualification are evidenced.
7. Keep implementation, testing, qualification, deployment and acceptance as separate gates. No schema draft or static source trace satisfies those gates.

## 5. Non-claims and verification boundary

- This is a read-only documentation crosswalk, not a new accepted contract or owner decision.
- No source code, normative architecture, schema or workflow was changed.
- No tests, qualification, model/provider calls, credentials, host/runtime inspection, installation, infrastructure changes, deployment or branch integration were performed.
- Source review is bounded; it is not a global proof of absence.
- Route B remains **PROPOSED / NOT IMPLEMENTED / NOT QUALIFIED / NOT ACCEPTED**.

## 6. Next bounded sub-request

**WB-14E — Provider, data-locality and workload admission:** reconcile local-only policy, provider/inference identity, egress and fallback controls, media workload admission, resource envelope and qualification evidence. Use source-pinned artifacts; leave host/runtime facts unknown and do not call models or inspect hardware.

Project map: [MEDIAHUB-CHAT-TREE-MAP.md](../architecture/MEDIAHUB-CHAT-TREE-MAP.md)
