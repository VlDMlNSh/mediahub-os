# MediaHub OS — Wave 285: A0 ingress, issuer, approval and producer trace

- Date: 2026-10-20
- Status: **SOURCE-BOUND TRUST-BOUNDARY FINDING / GOVERNANCE AND PRODUCER PROVENANCE OPEN / NO RUNTIME QUALIFICATION**
- Canonical map: [MEDIAHUB-CHAT-TREE-MAP.md](../architecture/MEDIAHUB-CHAT-TREE-MAP.md) on [the canonical docs branch](https://github.com/VlDMlNSh/mediahub-os/tree/docs/mediahub-chat-tree-map-20261012)
- Governing tracker: [Issue #301](https://github.com/VlDMlNSh/mediahub-os/issues/301)
- Target topology: [Wave 283 three-pool and Claude free-route hard requirements](../architecture/MEDIAHUB-ASTRA-GOLD-THREE-POOL-ROUTING-AND-CLAUDE-FREE-AUTH-HARD-REQUIREMENTS-WAVE-283-2026-10-20.md)
- Prior contract candidates: [Wave 269 envelope/lifecycle draft](MEDIAHUB-A0-HYBRID-MISSION-ENVELOPE-AND-DESTINATION-LIFECYCLE-CONTRACT-DRAFT-WAVE-269-2026-10-20.md), [Wave 271 source reconciliation](MEDIAHUB-A0-ISSUER-TASK-CONTRACT-RECONCILIATION-WAVE-271-2026-10-20.md), [Wave 276 issuer/approval gap](MEDIAHUB-A0-TASK-INGRESS-ISSUER-AND-APPROVAL-TRUST-GAP-WAVE-276-2026-10-20.md), [Wave 278 A0/Product State Authority crosswalk](MEDIAHUB-ASTRA-GOLD-A0-VS-PRODUCT-STATE-AUTHORITY-CROSSWALK-WAVE-278-2026-10-20.md).

## 1. Executive result

The direct source read reconfirms the key gap: the existing local file ingress treats `approval_state: "approved"` as a plain input string and passes it into the cloud-first gateway; the gateway's sensitive-command gate accepts that value without independently validating the issuer or approval record in the inspected path. **This establishes an unproven trust boundary, not proof that an exploit occurred or that any sensitive operation ran.** A legitimate external inbox writer/ACL/approval verifier could exist outside the inspected files, but no such trusted producer/verifier or its evidence was found in this bounded source pass.

The right next step is still contract/governance reconciliation, not a production verifier or another queue. Wave 269 stays a non-normative design candidate. Existing signed-command, heartbeat-attestation and provider/task schema mechanisms serve distinct contracts and must not be silently repurposed as Jarvis → ASTRA A0 mission-issuer proof.

## 2. Current refs and evidence

| Source | Ref/blob SHA | Evidence | Limitation |
|---|---|---|---|
| Repository implementation baseline | `main` HEAD `80be45a70732b1d568164571d4273a6397792c3b` | Exact source below re-read on `main`. | This pass does not integrate the docs branch into `main`. |
| `runtime/mediahub_runtime/task_ingress.py` | `main`, blob `59e1254aa61cc8f55f53bd1e179631e81c441393` | `FileTaskIngress` accepts a caller-supplied inbox path, enumerates `*.json`, parses schema-shaped fields, rejects duplicate request IDs in that read batch and constructs `AstraTaskRequest`. `task_to_contract()` serializes ordinary fields including `approval_state`. | No issuer/signature/audience/expiry/revocation/replay check is present in this file. The inbox path is injected; this code does not establish its owner, ACLs, producer or approval provenance. |
| `runtime/mediahub_runtime/astra_gateway.py` | `main`, blob `10985e4ad8f682313d08e7492ecc1856a8bce20f` | `AstraTaskRequest.approval_state` is a string. The sensitive-action check rejects unless the string equals `approved`; when it does equal `approved`, the inspected path proceeds to capability/provider execution. | No link to a separately verified approval record or typed trusted issuer context is shown in this path. The gateway is cloud-first with an Ollama local extension, not proof of the requested multi-pool A0 scheduler. |
| `runtime/mediahub_runtime/authorization.py` | `main`, blob `4d8df5d3c1c26f7f133a8093cd270635b085f4d5` | `AuthorizationContext` contains only `principal` and `capability`; policy denies tuples absent from its explicit in-process grants. | Helpful local authorization seam; no issuer authenticity, audience, resource, lifetime, revocation or external trust-chain evidence by itself. |
| `runtime/mediahub_runtime/astra_service.py` | `main`, blob `6aa2d09fc8737ccc0ba7f05bd13a15a0ebde7129` | Constructs the gateway and idles; comment says the resident service remains inert until an application/API boundary submits Task Contracts. | Does not wire a producer or a file inbox in this service. This is evidence about this entry point only, not proof no outside caller exists. |
| `runtime/mediahub_runtime/autonomous_queue.py` | `main`, blob `72c4a5ccb367884fb02d247b1b8848ea62c3c6b1` | Bounded local file-backed state, fixed local executor catalog and target-SHA guards. | Not evidence of a distributed A0 multi-pool ingress, trusted issuer or cross-pool fencing. |
| `ops/mesh/admission.py` / `ops/mesh/validators.py` | `main`, blobs `46e92d3c4f9b9865356443403e9ebd34587996cd` / `416a7ecaf4add9d0b81f0467cf426d9c7deb3ec7` | Validate node/capability records, execution authority and qualification state; heartbeat auth has a separate HMAC/freshness/sequence path. | Record-shape/admission and heartbeat auth are not a verified mission-issuer signature, task approval or destination-bound envelope. |
| `ops/control/sign_command.py` | `main`, blob `fc6943a79cefdf06e59d6e32771d2df551b2f0e9` | Uses a distinct per-node HMAC-signed control-command schema with command ID, node ID, operation, target SHA and freshness window. | Not demonstrated to authorize Jarvis missions or the file-ingress `approval_state`; do not reuse without an explicit accepted crosswalk. |
| `ops/qualification/produce_distributed_node_attestation.py` | `main`, blob `d2d423325558e877845f848314ceaf583a71fd8e` | Signs per-node qualification observations bound to node, command and target SHA. | Qualification attestation is not the task-approval issuer. |
| `architecture/ASTRA-GOLD-GOVERNANCE-CONTRACT.yaml` | `main`, blob `1d3ac25e7817f365807ad85d0d7c9007bd48bebf` | Canonical G11 human-launch record requires a signature, approver, approved source SHA, release target, fresh evidence, A3, soak and rollback evidence; unsigned/stale approval never launches. | The inspected task-ingress path does not consume or validate this G11 record. Do not claim G11 automatically closes the local task-approval gap. |
| `docs/checkpoints/MEDIAHUB-CLOUD-AGENT-TASK-ENVELOPE-SCHEMA-V0.2-WAVE-16-2026-10-16.json` | docs branch, blob `6f3cd3d40b2c5fe3f21bb6085536769fbef8322a` | Proposed GitHub-hosted cloud-agent task schema includes admission refs, source SHA, data/egress policy, route, quota/budget, idempotency and evidence fields. | PROPOSED ONLY; it is not the canonical schema for `mediahub.ai.astra-task@1.0.0` and does not prove an issuer/verifier exists. |
| Wave 269 mission-envelope draft | docs branch, blob `920963bf811219653b17ff8c3da300cc5d39b3c7` | Candidate field matrix calls for mission/task identity, issuer, audience, expiry, nonce, authorization decision, destination, DAG, budget and evidence. | Explicitly NOT an accepted normative runtime contract. |
| Wave 149 issuer decision gate | docs branch, blob `9c1a02dc125b37abea9284f0c0aa5deb571f13e7` | GOV-CAP-01…07 remain unselected/open; issuer/attester ownership and trusted-context lifecycle are undecided. | This governance gate prevents selecting a new protocol, issuer role or key lifecycle by implementation convenience. |

### Producer and inbox boundary disposition

The main tree contains the ingress, serializer and gateway, but no tracked file with a canonical schema definition for the hard-coded `mediahub.ai.astra-task@1.0.0`. The resident service does not instantiate `FileTaskIngress`; this bounded source scan did not establish the writer that places files in the injected inbox, its filesystem permissions, who may change `approval_state`, or an independently trusted approval verifier. Exact-string repository search did not return indexed caller matches in the connected search surface; that result is non-diagnostic and is **not** used as absence proof.

Accordingly, mark the producer/ACL/approval chain **UNKNOWN / NOT PROVEN**, rather than claiming no outside producer exists. Before runtime changes, identify the actual writer and deployment/runtime binding from an authoritative source, verify inbox directory ownership and write permissions, and map the trusted approval record through to the point that consumes it.

## 3. Field-level responsibility and contract gap matrix

| Field / invariant | Existing source | Target responsibility (candidate only) | Current disposition |
|---|---|---|---|
| Request/mission/task identity | Ingress has `request_id`, `session_id`; gateway may use `task_id` but ingress does not populate it. | Jarvis supplies correlation/intent; A0 validates stable mission and task IDs, parent relation, source digest and idempotency. | Partial local request shape only; no mission DAG identity. |
| Issuer and AuthorizationContext | Local `AuthorizationContext(principal, capability)`; no ingress propagation. | A separately accountable issuer and verifier bind authenticated principal, capability, operation/resource/scope, audience/destination, issue/expiry, revocation and replay/freshness data to a canonical signed envelope. | Governance open; no production issuer implementation authorized. |
| Approval decision | Plain `approval_state` string is read from JSON. | Trusted approval authority creates an auditable approval decision bound to exact command/task digest, target SHA, scope and expiry; consumer validates it independently. | Trust gap; a caller-written `approved` string is insufficient evidence. |
| Destination and admission | Ingress request has no destination or admitted node fields. | A0 chooses exactly one registry-admitted destination per claim; cloud, opted-in user node and Alamo Claude each have distinct eligibility policy. | Missing in ingress type; do not infer route eligibility from executor registration. |
| Route, upstream, cost and quota | Existing gateway chooses an available cloud-first provider with an Ollama local extension; provider schemas are separate. | Task-bound allowlisted route/provider/model/auth-cost/quota IDs; Alamo Claude must prove zero-cost/free eligibility and `paid_fallback=false`. Unknown cost/route fails closed. | Not bound in this ingress; no provider route qualifies from this evidence. |
| Data class, locality and egress | Ingress exposes `context_refs`, not a task-bound locality/egress policy. | A0 combines task data classification with destination egress/retention policy and validates it before dispatch. | Missing; no silent transfer/fallback between pools. |
| Source, workspace and writes | Ingress does not bind source commit/ref or allowed paths. A different worker path validates `ASTRA_TARGET_SHA`. | Task envelope binds immutable repo/ref/SHA, allowed/forbidden paths, workspace isolation and change cap. | Separate contracts not joined to ingress; preserve fixed-target guards. |
| DAG, dependencies, claim/lease/fencing | File ingress processes flat JSON entries; local autonomous queue has file-backed claims and a fixed worker pool. | A0 exclusively owns DAG, dependencies, claim/lease/retry/cancel/recovery, per-task fencing and cross-pool handoff. | No proven global multi-pool queue; do not add a parallel queue/controller. |
| Evidence and acceptance | Gateway has output/provider/model metadata; local task path does not bind the proposed evidence manifest/A3 record. | Executors return evidence with immutable source/task IDs and digest; A3 verifies independently. Executor success is not acceptance. | Partial lower-level evidence only; no Contour A acceptance. |
| Product State Authority | A0/qualification contract naming remains ambiguous in some artifacts; Wave 278 crosswalk is proposal-only. | A0 owns its engineering mission/queue state. Product State Authority separately owns canonical product state. | Governance reconciliation needed before schema changes; no implied domain authority for A0/Jarvis/executors. |

## 4. Static/mock-only negative-test candidate

These are required cases for the eventual accepted contract, not tests claimed implemented or executed in this pass:

1. Missing issuer, unrecognized issuer, wrong signature, wrong audience/resource/scope/destination, expired envelope, revoked capability, stale approval, reused nonce/replay, duplicate mission/task ID and changed target SHA.
2. Sensitive request with `approval_state="approved"` but no independently verifiable approval reference must deny; `pending`, `rejected`, malformed or unknown state must deny. Test against a mocked gateway/provider that cannot call out.
3. Unknown destination/node/router/model/auth-cost class denies. For Alamo Claude specifically, deny paid Anthropic endpoint/credential/subscription path, unverified free entitlement, unknown OpenFlux identity, quota exhaustion with paid fallback, and mismatched host binding.
4. User-owned node without explicit enrollment/consent, revoked/offline node, missing data classification, missing egress policy or locality-incompatible task denies without automatic cross-pool transfer.
5. DAG with missing/duplicate task IDs, invalid/cyclic dependencies, two active claims for one task, stale lease, unfenced cross-pool handoff, cancelled task returning as active, or retry not bound to the same idempotency key denies.
6. Executor or A0 attempting canonical product-state mutation outside Product State Authority denies; unsigned/stale G11 release approval remains blocked.

Implementation boundary: synthetic fixtures and static contract assertions only, after governance confirms the canonical extension point and authority semantics. No real signatures, key material, credentials, provider calls or runtime verifier are to be introduced in this documentary pass.

## 5. Controller PR #421 revalidation — separate blocker

- PR #421 remains **OPEN / DRAFT / UNMERGED**, currently based on main `80be45a70732b1d568164571d4273a6397792c3b`; latest head recorded for this report must be refreshed immediately before final readback.
- Earlier exact-head CI exposed stale static expectations in the caller guard and probe description; those were repaired. A subsequent run of the now-expanded `actionlint` command then identified real probe lint defects: empty `secrets: {}` is rejected and backticks in shell summary lines trigger ShellCheck. These were repaired by omitting the secrets mapping entirely, using safe `printf` lines and adding the probe workflow itself to the lint target list.
- The most recent probe run returned `startup_failure` with zero jobs and no job log; therefore its actual runtime caller context remains **NOT OBSERVED**. A permissions-ceiling adjustment did not resolve that failure in the next observed run, so no cause is asserted. Exact-head CI for the most recent revision must be checked independently.
- The main branch API currently reports `protected=false`. Required branch protection is therefore not evidenced/enabled in the current public repository response. PR review list has returned no submitted independent review. Do not merge or dispatch Gemini.

## 6. Work boundaries and result

Completed: source readback and trace; field responsibility/gap matrix; negative-test candidate; repair of statically proven probe lint defects in the separate PR #421 branch.

Not performed: no runtime ingress or queue changed; no production issuer/verifier or new schema implemented; no credentials/secrets/host access; no local tests run by this pass; no provider/model call, workflow dispatch or Gemini launch; no merge, deployment, qualification or acceptance.

**Disposition:** the current local task ingress approval chain is **NOT PROVEN / BLOCKED**. Wave 269 remains a design candidate. Contour A remains **NOT_PROVEN / BLOCKED**; Contour B remains gated on deployment and independent acceptance.

## 7. Next bounded step

1. Identify the authoritative Task Contract writer and actual inbox runtime binding/ACL from deployment/source evidence; decide who owns signed approval/attestation under the open GOV-CAP gates.
2. Reconcile A0 mission authority vs Product State Authority wording and choose the canonical extension point before implementing schema/verifier changes.
3. Finish PR #421 exact-head lint/unit CI and diagnose the non-launching probe startup failure. Obtain genuine independent security review and repository-protection evidence before any Gemini dispatch.

Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
