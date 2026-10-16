# MediaHub OS — Contour A WB-14Q: ASTRA A0 ingress interface design

- Date: 2026-10-16
- Status: **CONTRACT DESIGN PROPOSAL / NON-NORMATIVE / NOT ACCEPTED AS A NORMATIVE CONTRACT / NOT IMPLEMENTED / NOT QUALIFIED**
- Branch: `docs/mediahub-chat-tree-map-20261012`
- Parent: WB-14P launcher-family and bootstrap-contract reconciliation.
- Main HEAD observed at start: `ab36db009d034db8dca723691e23b331322287e7`.
- Documentation branch HEAD observed at start: `28233a78de38e5ec2b2898c98252203d35d0431e`; branch was `DIVERGED`, ahead 1477 / behind 4, merge base `f0f406feb9f9816b009f4e6e756813541e53b9bc`.
- Scope: design the **logical Jarvis → ASTRA A0 ingress interface**, independent of transport selection. This document does not authorize implementation, source edits, branch integration, runtime execution or qualification.
- Authority: owner-directed architecture allows Jarvis to use the ASTRA A0 route for engineering work requiring ASTRA lifecycle controls. This design records a proposed interface, not a new accepted baseline or a claim that an existing endpoint is available.

## 1. Decision framing and boundary

The requested design direction is: **design a new ingress through a formal ASTRA A0 interface**.

This selects the architectural seam to design; it does **not** yet choose a wire transport (GitHub polling, local IPC, HTTP, message broker or another mechanism), endpoint location, credential mechanism, implementation language, or deployment topology. Those remain open until their contracts and source evidence are reviewed.

The interface is a logical boundary:

`Jarvis Mission Coordinator → Authenticated A0 Ingress Adapter → A0 Admission → A0-owned queue/claim/lease/scheduler → admitted executor lane(s) → A0 result/evidence lifecycle`

- Jarvis owns corporation-level mission decomposition, permitted route selection, executor selection and mission-level result tracking.
- The A0 ingress adapter authenticates and structurally validates a request, then calls the A0 admission interface. It does not own a second queue or create independent claim/lease/gate state.
- ASTRA A0 is the sole writer for ASTRA-internal queue, claim, lease, heartbeat/liveness, retry/cancellation, recovery and ASTRA-specific evidence/gate transitions within its accepted contract.
- Executors, transports, providers and models are execution-only; they cannot grant themselves capability or mutate A0 state outside the interface.
- MediaHub Product State Authority remains the sole canonical product-state mutation authority in Contour B. A0 internal state is not product state.
- The direct Jarvis → local executor route remains a separate owner-directed route for eligible tasks. This document does not route all work through A0 and does not erase that distinction.
- No old host name, worktree, node profile, environment variable or HMAC key mapping becomes part of the target interface by implication.

## 2. Source-backed inputs and status

| Source | Ref / SHA | Use and limit |
|---|---|---|
| Target architecture Wave 01 | docs branch / `c9f1716de8419d66f181fc0a9c465c65a81c7d5b` | Records the owner-approved split of Jarvis, ASTRA A0 and Product State Authority; itself states it is not a normative contract. |
| Unified Architecture Contract v3 draft | docs branch / `28d5f82a80df2002d39c06d2060a822fd7aae258` | Establishes precedence and fail-closed principles; remains a working draft and does not silently replace accepted baselines/contracts. |
| Identity Lifecycle Contract Trace WB-05 | docs branch / `dc60ccc0af29a74ca3cf88584d66821350b20b9f` | Explicitly marks Jarvis→A0 ingress and capability issuer/lifecycle as open; no accepted endpoint/authentication/request/ack/error contract was identified there. |
| Agent/Task/Provider Schema Inventory WB-01 | docs branch / `81d6435b2571f7c261d08b763b6fc30c4d3c6207` | Source-bound schema inventory; corporation mission/task/result envelope is draft-only, not a registered accepted wire schema. |
| Jarvis direct route evidence matrix WB-10 | docs branch / `62101df270acd1f4e551a8fcaf69f1fe741a8b51` | Documents two distinct routes and prohibits implicit cross-route duplicate execution; direct route does not bypass security/evidence controls. |
| ASTRA executor capability matrix | main / `da26185254d9954fcee204f81ecca129bf052e7c` | Canonical executor workflow policy: A0 owns internal lifecycle, dependency-aware dispatch, claims/leases/recovery and evidence. |
| ASTRA GOLD qualification launch schema | docs branch / `0b86b07dfa916d4485ce1f8f54d19de136d98491` | Canonical qualification/launch gate schema; executor-only authority, fresh evidence and human launch approval. Not a Jarvis ingress schema. |
| ASTRA GOLD governance contract | docs branch / `1d3ac25e7817f365807ad85d0d7c9007bd48bebf` | Canonical A0 governance values include 600 s lease TTL, 900 s executor timeout, 120 s result publication timeout and 86400 s evidence freshness window. These are A0 governance values, not proposed ingress timeouts. |
| ASTRA health command contract | docs branch / `5a06ec6a649c378793063d0f4f9a8a532621c11d` | Existing node-bound operational health command; not the new corporation ingress protocol. |
| WB-14P launcher/health reconciliation | docs branch / `0c54386545395a81e0bf0fc1b0ba11913d3203ac` | Records launcher divergence and gaps in machine-enforced health freshness/correlation. |

**Source boundary:** these sources do not establish a currently accepted corporation-level ingress endpoint or universal mission/task wire schema. Existing schemas have narrower scopes. Proposed names and shapes below are design identifiers only.

## 3. Proposed interface surface

The first contract should define four logical operations, regardless of the eventual transport:

1. `SubmitMissionTask` — submit one immutable task request into A0 admission; A0 returns accepted, duplicate, rejected or deferred, never an implied execution success.
2. `GetRequestStatus` — retrieve the A0-owned lifecycle status for an authorized request/mission/task.
3. `RequestCancellation` — request cancellation through A0's lifecycle owner; acknowledgement means accepted for processing, not that the executor has already stopped.
4. `GetTaskResult` — retrieve the result envelope and immutable evidence references after A0 publication/validation.

A separate `HealthChallenge` / `HealthResponse` pair should prove the identity and freshness of the ingress/adapter path. It must not masquerade as an execution result or as full A0 qualification.

The wire transport maps these logical operations to messages, but does not redefine their semantics. No ingress adapter may mutate A0 queue/claim/lease state directly; it must call the A0-owned admission/state transition interface.

## 4. Proposed request envelope — illustrative, not registered

Suggested design ID: `mediahub.astra-a0.ingress-request.v1`. This identifier is **not registered or accepted**.

```json
{
  "schema_id": "mediahub.astra-a0.ingress-request",
  "schema_version": "1.0.0",
  "request_id": "stable-unique-id",
  "idempotency_key": "stable-caller-key",
  "issued_at": "RFC3339 UTC timestamp",
  "expires_at": "RFC3339 UTC timestamp",
  "issuer": {
    "principal_id": "authenticated-workload-identity",
    "credential_ref": "opaque-reference-only"
  },
  "audience": "astra-a0-ingress",
  "operation": "submit_task",
  "mission": {
    "mission_id": "stable-mission-id",
    "mission_revision": "immutable-revision-or-digest"
  },
  "task": {
    "task_id": "stable-task-id",
    "task_revision": "immutable-revision-or-digest",
    "dependencies": [],
    "objective": "bounded objective",
    "acceptance_criteria": [],
    "input_refs": [],
    "expected_outputs": [],
    "target_source": {
      "repository": "owner/repository",
      "commit_sha": "exact-commit-id"
    }
  },
  "route": {
    "requested_class": "astra_a0",
    "policy_ref": "versioned-policy-reference"
  },
  "capability_ref": "opaque-signed-capability-reference",
  "constraints": {
    "deadline": "RFC3339 UTC timestamp",
    "max_attempts": 1,
    "data_classification": "declared-classification",
    "egress_profile": "declared-policy-profile",
    "allowed_actions": [],
    "owned_paths": [],
    "resource_budget_ref": "opaque-budget-reference"
  },
  "trace": {
    "correlation_id": "stable-trace-id",
    "parent_request_id": null
  },
  "payload_digest": "digest-of-canonical-request-body",
  "signature": {
    "algorithm": "approved-algorithm-id",
    "key_id": "issuer-key-id",
    "value": "signature-over-canonical-envelope"
  }
}
```

Rules:
- The authenticated principal is derived from the verified credential/signature context, not trusted solely because a request body names an issuer.
- Never include raw credentials, private keys, bearer tokens or provider secrets in the envelope, task body, logs or results.
- Signature canonicalization, algorithm allow-list, key lifecycle and capability token format require the accepted MH-12 security/capability contract; do not invent a second authentication standard here.
- The immutable payload digest covers every authority-bearing field, including target revision, route, scope, dependencies, expiry and capability reference.
- A repeated idempotency key with the same canonical digest returns the original request identity/status; the same key with a different digest is rejected as a conflict.
- A replayed, expired, not-yet-valid, wrong-audience, malformed or unauthorized request fails closed and is auditable.
- The task may not instruct the ingress to mutate canonical product state or bypass required human approval gates.

## 5. Admission and acknowledgement contract

Suggested design ID: `mediahub.astra-a0.ingress-ack.v1` (unregistered proposal).

Every accepted request returns an acknowledgement containing:
- schema ID/version;
- request, mission and task IDs;
- canonical request digest;
- A0 admission decision and reason code;
- A0 lifecycle reference;
- accepted-at timestamp;
- A0 controller/service identity and source/config revision;
- correlation ID;
- retry guidance only where safe and meaningful.

Decision values (proposed):
- `ACCEPTED` — A0 has durably admitted the request into its own lifecycle state. This is not a claim that execution started.
- `DUPLICATE_SAME_PAYLOAD` — return the existing canonical lifecycle reference; do not create a second task.
- `REJECTED` — malformed, unauthorized, stale, conflicting, unsupported or policy-denied request; include stable machine-readable reason code.
- `DEFERRED` — admission is valid but cannot currently proceed due to a defined capacity/dependency/maintenance condition; response must specify whether the request is durably recorded and how status is retrieved.
- `INDETERMINATE` — adapter cannot prove whether A0 committed admission. Caller must query by request/idempotency key; it must not blindly submit a new identity.

The adapter must not claim `ACCEPTED` before the A0 lifecycle owner confirms durable admission. A network timeout after possible commit is `INDETERMINATE`, not proof of failure.

## 6. Proposed task lifecycle and authority contract

The ingress interface may request a transition; it does not itself own lifecycle state.

| Concern | Owner | Interface invariant |
|---|---|---|
| Mission decomposition and corporation-level route choice | Jarvis | Sends a bounded immutable request; cannot write A0 queue state directly. |
| Schema/size/freshness/authentication/authorization checks | Ingress adapter plus accepted policy verifier | Fail closed before admission; preserve a rejection audit record without exposing secrets. |
| Dependency graph, readiness, queue order | ASTRA A0 | One canonical A0 lifecycle; reject cycles, missing dependency identities and illegal revision mutation. |
| Claim/lease/heartbeat/fencing | ASTRA A0 | Atomic claim and lease generation; stale workers cannot commit results or lifecycle transitions. |
| Retry, cancellation and recovery | ASTRA A0 | Bounded policy, explicit state transitions, attempt identity and deterministic recovery. |
| Tool/workspace/egress limits | Admission policy + executor isolation mechanism | Enforce per-task scope; task text is not an authority grant. |
| Result creation and evidence linkage | Executor produces untrusted result; A0 validates and records lifecycle | Executor cannot self-certify, promote a gate or overwrite immutable evidence. |
| Independent verification | A3 / independent verifier under accepted gate policy | Verification identity and evidence must be separate from the producing executor where required. |
| Canonical MediaHub product state | MediaHub Product State Authority | No A0 ingress, agent, executor or result can mutate product state by implication. |
| Human launch/release approval | Human approver under qualification schema | No automatic promotion from a green health response or task success. |

A request that requires A0-owned engineering queue/claim/lease/gate semantics must use this A0 route. Tasks eligible for the explicitly separate direct-local route remain governed by its own lifecycle owner and contract; they must not be silently double-dispatched.

## 7. Health challenge/response contract

Suggested design ID: `mediahub.astra-a0.health-response.v1` (unregistered proposal).

```json
{
  "schema_id": "mediahub.astra-a0.health-response",
  "schema_version": "1.0.0",
  "challenge_id": "fresh-caller-generated-nonce",
  "request_digest": "digest-of-health-challenge",
  "responder": {
    "service_principal_id": "authenticated-a0-ingress-identity",
    "instance_id": "ephemeral-instance-identity"
  },
  "issued_at": "RFC3339 UTC timestamp",
  "observed_at": "RFC3339 UTC timestamp",
  "expires_at": "RFC3339 UTC timestamp",
  "status": "ready | not_ready | degraded",
  "protocol_version": "version",
  "contract_revision": "accepted-contract-revision",
  "source_revision": "exact-source-commit",
  "capabilities_advertised": [],
  "signature": {
    "algorithm": "approved-algorithm-id",
    "key_id": "service-key-id",
    "value": "signature-over-canonical-response"
  }
}
```

Minimum verifier requirements to be specified normatively:
1. Caller supplies a cryptographically unpredictable challenge/nonce and retains the exact challenge digest.
2. Response challenge ID and request digest must match the outstanding challenge; unsolicited cached responses are rejected.
3. Issued/observed timestamps must be parseable, within clock-skew policy, and inside an explicit short freshness window. The threshold is an owner/security-contract decision; do not reuse the 86400-second evidence freshness window as a live health nonce TTL.
4. Authenticated responder identity must match an explicitly expected service principal and audience; identity cannot be accepted merely because the payload contains a node ID.
5. Response signature must validate against the approved identity/key lifecycle, including expiry/revocation policy.
6. `status=ready` is required for readiness claims. `degraded` and `not_ready` remain valid diagnostic responses but cannot pass readiness.
7. Contract/source revisions and advertised capabilities must be allow-listed by caller policy; health does not prove a capability is qualified.
8. Timeout, replay, nonce mismatch, stale timestamp, identity mismatch, signature failure or unsupported schema fails closed.
9. Record verifier version, challenge digest, response digest, expected identity, observed time and decision in immutable audit/evidence.
10. A health response proves only the scoped ingress identity/readiness probe. It does not prove queue durability, lease fencing, executor health, full qualification, 24-hour soak or product acceptance.

The transport-health verifier gap recorded in WB-14P remains a source finding; this report does not patch or execute that verifier.

## 8. Result envelope and failure semantics

Suggested design ID: `mediahub.astra-a0.task-result.v1` (unregistered proposal).

The A0-visible result should contain:
- request/mission/task IDs, task revision and attempt ID;
- canonical request/input digests and exact target source SHA;
- executor principal/profile and route provenance;
- A0 claim/lease generation or fencing reference;
- terminal/intermediate status and stable error class;
- started/completed timestamps and duration;
- output artifact references, content digests, size/type metadata and owned-path manifest;
- checks/verifier identity and separate verification status;
- cancellation/timeout/partial-result indicators;
- evidence references, schema/policy revision and correlation ID.

Proposed status vocabulary must distinguish at least `QUEUED`, `ADMITTED`, `RUNNING`, `SUCCEEDED_UNVERIFIED`, `VERIFIED`, `FAILED`, `BLOCKED`, `CANCEL_REQUESTED`, `CANCELLED`, `TIMED_OUT`, `PARTIAL`, `REJECTED`. Exact state transitions must be aligned with the accepted A0 lifecycle contract; this list is not an authorization to alter canonical state vocabulary.

Failure rules:
- An executor-produced result is untrusted until schema, digest, target SHA, ownership, policy and evidence checks pass.
- Late results after cancellation/lease expiry or with an old fencing generation are quarantined and cannot overwrite the canonical task result.
- Publication failure is distinct from execution failure. Retain a durable local/A0 outbox or equivalent only if the accepted A0 persistence/recovery contract defines it; do not invent hidden parallel state.
- Retries require a new attempt identity and bounded policy. Idempotency must prevent duplicate side effects where possible; operations that cannot be safely replayed require explicit policy/approval.
- A successful command or green health response is not equivalent to independent A3 verification or qualification PASS.

## 9. Security and capability requirements

Before implementation, the accepted security contract must settle:
- authenticated Jarvis workload identity and audience binding;
- explicit capability issuer authority and delegation chain;
- subject, action, resource, audience, constraints, expiry, provenance and revocation semantics;
- key issuance, storage, rotation, revocation, verification and compromise response;
- canonical serialization and signature algorithm policy;
- authorization order: structural/freshness validation → identity/authentication/trust → capability and policy → A0 admission;
- anti-replay and idempotency storage semantics;
- data classification, permitted egress and minimal task payload;
- immutable audit evidence and sensitive-field redaction;
- fail-closed behavior if issuer, policy, revocation state or A0 lifecycle state cannot be verified.

Do not reuse the legacy per-node HMAC environment variable map as the target identity registry. Do not let Jarvis, the ingress adapter, an executor or a model mint authority for itself. Do not put raw secrets in a task or capability reference.

## 10. Contract requirements and failure matrix

| ID | Requirement | Failure cases | Required disposition |
|---|---|---|---|
| A0I-01 | Versioned schema and canonical digest | Missing/unknown schema, duplicate fields, canonicalization ambiguity | Reject; audit stable reason. |
| A0I-02 | Authenticated workload principal and audience | Invalid/revoked credential, spoofed issuer, wrong audience | Deny before A0 admission. |
| A0I-03 | Explicit capability and policy authorization | Missing issuer, invalid delegation, scope expansion, unknown policy | Fail closed; no implicit authority. |
| A0I-04 | Freshness and replay protection | Expired request, replay, nonce mismatch, excessive clock skew | Reject or quarantine; preserve evidence. |
| A0I-05 | Idempotent durable admission | Same key/same digest, same key/different digest, timeout after possible commit | Return canonical prior request; reject conflict; query before retry. |
| A0I-06 | A0-owned lifecycle state | Adapter writes claims directly, duplicate queue owner, ambiguous state transition | Deny; one A0 lifecycle writer. |
| A0I-07 | Immutable source/task binding | Branch name without commit, target SHA changes, input digest mismatch | Reject or require new immutable task revision. |
| A0I-08 | Dependency and route correctness | DAG cycle, missing dependency, cross-route duplicate | Reject/defer with stable reason; never double-dispatch implicitly. |
| A0I-09 | Scoped execution | Unbounded actions, paths, resources, egress or secret access | Deny or request explicit authorized policy change. |
| A0I-10 | Claim/lease fencing | Stale claim, expired lease, old generation result | Reject stale transition/result. |
| A0I-11 | Cancellation/deadline/retry | Late result, unbounded retry, unknown stop state | Mark indeterminate/blocked as defined; no false cancellation success. |
| A0I-12 | Result/evidence integrity | Invalid schema, digest mismatch, missing provenance, self-certification | Quarantine; no gate promotion. |
| A0I-13 | Health identity/freshness | Stale response, wrong principal, replayed challenge, status not ready | Fail readiness check. |
| A0I-14 | Authority separation | A0/adapter/executor attempts product-state mutation | Deny; use Product State Authority contract. |
| A0I-15 | Auditability | Missing correlation or evidence digest, secret leakage | Reject or block as policy defines; redact sensitive data. |
| A0I-16 | Human qualification/release gates | Health or task success interpreted as qualification/release | Block promotion; require exact gate evidence and human approval. |

## 11. Open decisions before normative contract and implementation

1. **Transport selection:** GitHub pull adapter, local IPC, authenticated HTTP, broker, or other. Choose after evaluating threat model, availability, replay, network boundary and operations. This report deliberately does not choose one.
2. **Ingress service principal and credential lifecycle:** accepted issuer, key custody, rotation, revocation propagation, signing/canonicalization and recovery.
3. **Durable idempotency/admission store:** authoritative owner, atomicity boundary, retention and recovery behavior. Must not create a second A0 queue.
4. **Exact schema governance:** registry path, schema ID/versioning, canonicalization rules, compatibility policy and generated validation evidence.
5. **Clock/freshness policy:** maximum request age, health challenge TTL, clock-skew allowance and revocation cache behavior.
6. **A0 status/query contract:** stable lifecycle states, acknowledgement durability point, query consistency and indeterminate commit recovery.
7. **Capability issuer:** explicit authority and delegation/revocation semantics under MH-12; currently open in WB-05.
8. **Result/evidence storage:** immutable artifact/evidence references, digest algorithm, retention and publication recovery under existing governance.
9. **Route arbitration:** conditions for A0 route vs direct local route and cross-route idempotency/fencing.
10. **Normative source reconciliation:** exact ASTRA reference-architecture statements that conflict with owner-approved authority split must be reconciled through controlled change, not this proposal.
11. **Target revision policy:** allowed repository/ref/SHA forms, signed source provenance and clean-worktree/isolation guarantees.
12. **Operational limits:** payload size, rate limits, concurrency admission and timeout values. Do not duplicate numeric A0 governance constants in the ingress schema.

## 12. Proposed implementation sequence after approval

1. Owner reviews the logical boundary and unresolved choices; accept/revise the design posture.
2. Reconcile source authority wording and designate the normative contract owner.
3. Freeze security principal/capability lifecycle and schema governance before selecting transport-specific authentication details.
4. Author separate normative request, acknowledgement/status, health challenge/response and task/result schemas; map each field to existing schemas or explicitly record a gap.
5. Define a transport-neutral A0 admission interface and state-transition API; require the transport adapter to call it rather than mutate queue state.
6. Only after explicit authorization, implement the selected adapter in Contour A and add static/schema/unit coverage.
7. With separate authorization, run tests and then qualification in distinct stages; do not equate source checks, unit tests, live identity verification, qualification and acceptance.
8. Independently verify exact SHA, replay/idempotency, fencing, recovery, freshness, authority boundaries and evidence integrity before any deployment decision.

No implementation step is authorized by this document.

## 13. Verification boundary

- Read-only source inspection and documentation authoring only.
- No tests, qualification, workflow dispatch, credentials, provider/model calls, host/runtime inspection, installation, infrastructure changes, deployment, migration, merge, rebase, cherry-pick or source-code edits occurred.
- Existing schema/test files were read as source evidence only; tests were not run.
- Main and documentation branches remain diverged; no branch integration or main ref change was attempted.

## 14. Next bounded step — WB-14R

Create a statement-level source reconciliation packet for ASTRA authority wording and map the proposed A0 ingress fields to exact source schemas/owners. Resolve field-level collisions and identify which new schemas must be proposed, without changing normative contracts or selecting a transport. Keep capability issuer and transport selection explicitly open until owner decision.

- Project map: [MEDIAHUB-CHAT-TREE-MAP.md](../architecture/MEDIAHUB-CHAT-TREE-MAP.md).
