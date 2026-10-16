# MediaHub OS — Contour A WB-14AA: ASTRA A0 ingress contract candidate

- Date: 2026-10-16
- Status: **PROPOSED / NOT ACCEPTED / NOT FROZEN / NOT IMPLEMENTED**
- Purpose: define a transport-neutral review artifact for Jarvis → ASTRA A0 engineering-mission ingress.
- Authority boundary: Jarvis coordinates corporation-level missions and routes work; ASTRA A0 owns ASTRA-internal queue/claim/lease/retry/cancellation/recovery and evidence/gate state; MediaHub Product State Authority alone mutates canonical product state.
- Non-goals: selecting transport, endpoint, schema ID, crypto algorithm, issuer, persistence, numeric TTLs, implementation, tests, qualification, deployment or acceptance.

## 1. Normative status and source basis

This is a proposal, not a normative contract. It does not supersede any accepted baseline, ASTRA internal workflow contract, MH-12 authorization constraints, or owner decision. It is not evidence that an interface exists.

Source basis:
- [WB-14Z source-contract census](MEDIAHUB-CONTOUR-A-WB-14Z-A0-INGRESS-SOURCE-CONTRACT-CENSUS-2026-10-16.md): internal A0 workflow policy exists; accepted Jarvis-facing API/issuer/admission/result contract was not established by the bounded source set.
- [WB-14Y route-boundary correction](MEDIAHUB-CONTOUR-A-WB-14Y-A0-INGRESS-VS-PRODUCT-MUTATION-BOUNDARY-CORRECTION-2026-10-16.md): engineering ingress is distinct from P0-07 → P0-05 → P0-04 product mutation.
- [Owner decision packet](MEDIAHUB-OWNER-DECISION-PACKET-01.md), §8: DEC-DEV-02 Option C is owner-approved; source wording reconciliation and runtime evidence remain separate.
- [Jarvis Control Plane/GitHub Adapter Contract Draft 01](MEDIAHUB-JARVIS-CONTROL-PLANE-GITHUB-ADAPTER-CONTRACT-DRAFT-01-2026-10-14.md): draft only; not accepted as this contract.
- [WB-14B ingress caller/authority trace](MEDIAHUB-CONTOUR-A-WB-14B-JARVIS-TO-A0-INGRESS-CALLER-AND-AUTHORITY-SEAM-TRACE-2026-10-15.md): local file Task Contract consumer and signed operational-command workflow are separate paths; no accepted end-to-end Jarvis producer-to-A0 contract was established.
- [Wave 07 A0 lifecycle/MH-12 issuer trace](MEDIAHUB-A0-LIFECYCLE-MH12-CAPABILITY-ISSUER-SOURCE-TRACE-WAVE-07-2026-10-15.md): internal lifecycle constraints do not by themselves define the external API.

## 2. Authority and invariant requirements

R-01. Jarvis is the corporation-level mission coordinator and permitted executor router. It may request A0 engineering work but cannot write A0-owned internal queue/lease state directly.

R-02. ASTRA A0 is the authority for its own admitted engineering-work lifecycle and associated evidence/gate state, under its accepted internal contract.

R-03. A0 ingress must not create, authorize or commit canonical MediaHub product-state mutations. Any such mutation remains on the separately governed P0-07 → P0-05 → P0-04 route and its own authorization/acceptance gates.

R-04. Admission, execution, verification, qualification, release and deployment are distinct states/events. A request accepted into A0 is not proof of execution or successful verification.

R-05. Fail closed when identity, authorization, request integrity, freshness, idempotency, policy revision, target binding or state transition cannot be established. Do not silently fall back to cloud execution or an alternate authority path.

R-06. Every externally observable disposition and result must be auditable and correlated to the accepted request identity, caller identity, target/revision, applicable policy/contract revision and evidence references.

## 3. Transport-neutral operation inventory

This table names logical operations only. It does not define URL, RPC method, message topic, database schema or serialization.

| Logical operation | Intent | Required response semantics | Status |
|---|---|---|---|
| SubmitMission | Ask A0 to admit a bounded engineering mission | Explicit accepted/rejected/indeterminate disposition; stable correlation ID if accepted | PROPOSED |
| GetMissionStatus | Read the current A0-owned lifecycle status for an admitted mission | Status with revision/observation time and correlation to mission | PROPOSED |
| GetMissionResult | Retrieve a terminal attempt/result and evidence references | Explicit result disposition; source/target revision and producer identity; no implication of independent qualification | PROPOSED |
| RequestCancellation | Request cancellation of A0-owned work | Distinguish cancellation requested, cancellation accepted, cancellation complete, too-late/terminal, and indeterminate | PROPOSED |
| ProbeA0 | Verify a challenged response from the intended A0 service | Correlated challenge, responder identity and freshness; separate liveness/readiness/authorization | PROPOSED / OPTIONAL |
| ReconcileAdmission | Resolve an uncertain submit/ack outcome using request identity and digest | Same request resolves to the original durable disposition; never silently create a second mission | PROPOSED |

No operation above is accepted or implemented. Whether ProbeA0 and ReconcileAdmission are separate wire operations or are represented by a chosen transport remains OPEN.

## 4. Minimum logical request envelope

The candidate request envelope should be capable of representing these fields, without prescribing names or wire encoding:

- Contract identifier and revision.
- Globally unique request/mission identifier and idempotency key.
- Canonical request digest over the immutable mission intent.
- Caller principal identity and issuer/attester provenance.
- Intended audience/receiver identity.
- Authorized operation, resource, scope and permitted execution boundary.
- Target repository/project/artifact plus immutable target revision/digest where applicable.
- Mission intent, bounded deliverables, constraints, allowed executor class, required evidence and acceptance criteria.
- Creation time, not-before/expiry or equivalent freshness bounds; replay protection context.
- Authorization/capability reference or verifiable signed context, including delegation chain if delegation is supported.
- Applicable policy/contract revision and audit correlation ID.
- Explicit prohibition on implicit product-state mutation or unapproved provider/cloud fallback.

The exact field set, optionality, canonicalization, digest algorithm and signature format remain OPEN. A caller-provided principal string or capability label is not trusted identity evidence.

## 5. Admission, lifecycle and result semantics

### Admission
A0 must establish a durable admission decision before returning an accepted disposition. The contract must define the atomic commit boundary, uniqueness scope, idempotency-key reuse rules, digest mismatch behavior, duplicate response, acknowledgement meaning, and recovery after a lost response or uncertain commit. No persistence mechanism or retention interval is selected here.

### Lifecycle
The accepted contract must distinguish at minimum:
- submitted/request received;
- rejected before admission;
- accepted durably by A0;
- queued;
- claimed/leased;
- executing;
- cancellation requested;
- cancellation completed or too late;
- retry/recovery pending;
- execution terminal (succeeded/failed/cancelled/expired/indeterminate);
- evidence collection complete;
- verification/gate outcome;
- qualification outcome, when explicitly in scope.

These are candidate semantic distinctions, not accepted enum strings. A0's internal canonical lifecycle remains authoritative; external status may be a governed projection. Admission acceptance must not be represented as “success.”

### Fencing and cancellation
The contract must define monotonic attempt/generation or equivalent fencing, stale-worker rejection, result commit preconditions, lease loss/reclaim races, cancellation races, late results, retries and terminal-state immutability. Internal numeric lease/retry settings must not be reused as external request TTL or token expiry.

### Result and evidence
A result must distinguish executor-reported outcome from independently verified evidence and from qualification/acceptance. It should bind to request ID/digest, target SHA/revision, attempt/generation, executor principal, relevant policy/contract revision, artifact/evidence references and timestamps. An A0 success cannot authorize canonical product mutation or imply release/deployment.

## 6. Trust and security profile — unresolved selection

Before acceptance, governance must select or explicitly defer:
1. Trusted principal source and service identity lifecycle.
2. Issuer/attester authority, verifier responsibility, key/credential rotation and revocation.
3. Audience, operation/resource/scope restrictions and delegation rules.
4. Request integrity and target/request-digest binding.
5. Freshness, expiry, replay resistance, clock assumptions and duplicate retention.
6. Audit record integrity, attribution and access control.
7. Fail-closed behavior when the issuer, policy source, verifier or audit path is unavailable.

MH-12 principles are constraints, not a choice of issuer, token format or cryptographic technology. The signed operational-command path is not automatically the mission-ingress trust profile.

## 7. Failure/disposition matrix

| Condition | Required semantic disposition | Must not happen |
|---|---|---|
| Unknown/untrusted caller or invalid issuer context | Reject before durable admission; audit if safe | Admit based on caller-supplied identity text |
| Wrong audience, insufficient scope or target mismatch | Reject | Broaden authority or silently retarget |
| Stale, expired or replayed request | Reject or return the prior idempotent disposition where the same accepted request is proven | Create duplicate work |
| Same idempotency key with different digest | Explicit conflict/rejection | Treat as same mission |
| Durable commit succeeded but acknowledgement was lost | Indeterminate until reconciled, then return original disposition | Admit a second mission |
| Queue/lease generation is stale | Reject stale claim/result transition | Allow stale worker to overwrite current attempt |
| Cancellation races with terminal result | Return explicit race/terminal disposition according to accepted policy | Claim cancellation succeeded without evidence |
| Policy/authority/verification unavailable | Fail closed or return explicit unavailable/indeterminate status | Bypass controls |
| Result lacks required evidence or target binding | Mark evidence/gate incomplete or failed per accepted policy | Treat executor assertion as qualification |
| Requested operation would mutate canonical product state | Reject or route through separately accepted P0-07/P0-05/P0-04 contract | Use A0 as a second state authority |

Exact error codes, retryability, HTTP/RPC mapping and timeouts remain OPEN.

## 8. Decisions required before this can become normative

| Decision ID | Question | Required authority/evidence | Current state |
|---|---|---|---|
| A0-ING-01 | Who owns and accepts the Jarvis-facing A0 contract and version lifecycle? | Named accountable owner plus accepted document path/revision | OPEN |
| A0-ING-02 | Which service identity, issuer/attester and verifier lifecycle is trusted? | Security/governance decision and source-backed trust chain | OPEN |
| A0-ING-03 | Which transport and caller/adapter edge are accepted? | Architecture decision plus source-backed producer-to-consumer path | OPEN |
| A0-ING-04 | What are the durable admission, idempotency and uncertain-commit rules? | A0 state/persistence owner decision and consistency model | OPEN |
| A0-ING-05 | What exact external status/result/cancel vocabulary maps to A0 internal state? | A0 lifecycle owner decision with race/fencing semantics | OPEN |
| A0-ING-06 | What are freshness, expiry, replay, clock and deduplication-retention rules? | Security decision with explicit assumptions | OPEN |
| A0-ING-07 | Is a challenge-response health probe required and what does it prove? | Service-health/identity contract owner decision | OPEN |
| A0-ING-08 | What target binding, evidence requirements and verification boundaries apply? | ASTRA evidence/gate contract reference and acceptance owner | OPEN |
| A0-ING-09 | How is the contract tested, qualified and independently accepted once implemented? | Approved qualification plan and independent acceptance authority | OPEN |

These IDs are local proposal identifiers only. They are not registered project decision IDs and must be collision-checked before promotion to a canonical registry.

## 9. Acceptance checklist

The proposal may only be promoted after:
- all decision owners and acceptance authority are identified;
- contract ID/version and source-of-truth path are approved;
- trust issuer/attester/verifier and caller edge are evidenced;
- request/response, durable admission, idempotency, cancellation, fencing, result and failure semantics are accepted;
- status projection does not merge execution, verification, qualification, release or deployment;
- product-state mutation remains exclusively on the governed product route;
- test/qualification/independent-acceptance criteria are approved separately;
- source SHA and explicit owner/governance acceptance are recorded.

No item is claimed complete by this document. No tests, validators, credentials/provider calls, host/runtime inspection, installations, infrastructure changes, deployment, migration, branch integration or implementation occurred.

- Project map: [MEDIAHUB-CHAT-TREE-MAP.md](../architecture/MEDIAHUB-CHAT-TREE-MAP.md).
