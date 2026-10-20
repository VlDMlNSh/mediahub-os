# Wave 269 — A0 hybrid mission envelope and destination lifecycle contract draft (2026-10-20)

## Status

SOURCE-RECONCILED CONTRACT DESIGN DRAFT; NOT ACCEPTED AS A NORMATIVE RUNTIME CONTRACT. This pass translates the owner-directed hard requirements consolidated in Wave 268 into a reviewable field/ownership matrix. It does not change Baseline 2.0, introduce a second controller, or authorize runtime use.

## Source evidence pinned

- `runtime/mediahub_runtime/task_ingress.py@main`, blob `59e1254aa61cc8f55f53bd1e179631e81c441393`: `FileTaskIngress` accepts `mediahub.ai.astra-task@1.0.0` with request/session/user-command/approval fields; no authenticated issuer provenance, destination class, DAG, route policy, locality policy, or cross-route fencing contract.
- `runtime/mediahub_runtime/astra_gateway.py@main`, blob `10985e4ad8f682313d08e7492ecc1856a8bce20f`: describes a cloud-first gateway with a local Ollama adapter; not evidence of A0's target multi-tier scheduler or Alamo Claude policy enforcement.
- `runtime/mediahub_runtime/autonomous_queue.py@main`, blob `72c4a5ccb367884fb02d247b1b8848ea62c3c6b1`: bounded local file-backed queue and claims; not a distributed hybrid queue or proof of three-destination admission.
- `ops/agent-fabric/providers/local-executor-routing-v2.yaml@docs/mediahub-chat-tree-map-20261012`, blob `af3d96fe91055af6ba79eded9c800d28d8c0c5c9`: lists `CLAUDE_FCC`, `CLAUDE_OMNIROUTE`, and `CLAUDE_CODE_DIRECT` as qualification-gated candidates; it does not prove Alamo host binding, non-paid authorization, upstream identity, or Anthropic API exclusion.
- Owner-directed Wave 268 hard constraints: [report](MEDIAHUB-A0-MULTI-TIER-ROUTING-AND-ALAMO-CLAUDE-NONPAID-AUTH-HARD-CONSTRAINTS-WAVE-268-2026-10-20.md) and [map addendum](../architecture/MEDIAHUB-CHAT-TREE-MAP-ADDENDUM-WAVE-268-2026-10-20.md).

## Proposed mission envelope v0.1 — design candidate only

The eventual versioned contract should have a single mission identity and immutable source provenance, then bind every child task to one explicit destination and policy decision. Field names below are design suggestions, not an accepted schema.

| Field group | Minimum semantic content | Owner / enforcement |
|---|---|---|
| `contract` | schema ID, version, canonicalization/digest rules | Contract validator; unknown version fails closed |
| `mission` | stable mission ID, parent/correlation ID, created-at, expiry/deadline | Jarvis creates intent; A0 validates and binds execution identity |
| `issuer` | authenticated principal, issuer identity, issuer type, capability reference, audience, issued-at, expiry, nonce/replay binding, signature/verification reference | Trusted ingress verifies; missing/ambiguous provenance denies |
| `authorization` | requested actions, scope, approval state/reference, policy decision ID | Policy authority; no executor self-approval |
| `task_graph` | stable task IDs, parent mission ID, dependency edges, bounded input/output contracts, workspace claims, retry budget, timeout, cancellation semantics | A0 validates DAG and owns scheduling/lifecycle |
| `destination` | exactly one of `github_hosted_cloud`, `user_owned_mediahub`, `local_executor`; admitted destination ID and capability set | A0 selects only from admitted registry; unknown target denies |
| `route_policy` | allowed provider/auth class, explicitly denied routes, local-only/no-fallback mode, egress class, data class, region/location constraints where applicable | Policy enforcement before dispatch and at adapter boundary |
| `quota_budget` | task and mission budgets, quota domain, max attempts, concurrency ceiling, expiry | A0/authorized quota service; no implicit paid fallback |
| `claim_fencing` | claim generation/fencing token reference, idempotency key, lease/heartbeat, handoff state | A0 is sole owner of hybrid claims/leases; stale generations cannot commit |
| `result_evidence` | terminal state, source/task/route identity, executor identity, artifact digests, logs redaction status, verification reference | Executor emits; A0 reconciles; independent A3 verifies |
| `audit` | decision IDs, policy/version digests, state transition references, timestamps | Append-only evidence path; secrets never serialized |

The contract must not carry raw API keys, OAuth refresh tokens, session cookies, or reusable provider credentials. Credential material is resolved only through an authorized runtime secret boundary and never becomes part of task payloads, logs, artifacts, or evidence manifests.

## Destination responsibility matrix

| Destination class | Admission and execution constraints | Required failure behavior |
|---|---|---|
| GitHub-hosted cloud pool | Ephemeral GitHub-hosted runner; independent of Alamo and user devices; fixed source SHA/workspace boundaries; runtime-only secret references; outbound egress allowlist/policy; evidence captured | Missing hosted-runner admission, source pin, capability, or egress policy => DENY; no implicit self-hosted/server fallback |
| User-owned MediaHub | Explicit opt-in/enrollment; authenticated device/instance identity; scoped capability; owner data-locality and egress policy; quotas, revocation, isolated workspace; task-specific evidence | Offline/revoked/unknown device or missing locality policy => BLOCKED; no automatic transfer to cloud |
| Local executor (Alamo Claude) | Alamo identity must be proven; Claude/Claude Code is executor-only; FCC/fcc-claude or equivalent is only a candidate non-paid authorization/routing component after upstream, terms, auth/cost class, egress, version, and host binding review; Anthropic API and paid Anthropic API authorization are explicitly denied | Any paid Anthropic API route, unknown router, unknown auth/cost class, missing Alamo identity, or ambiguous provider path => DENY; no cloud fallback |

“Claude Code runs on Alamo” describes execution placement, not necessarily model inference placement. Do not claim local inference unless separately evidenced. The owner prohibition on Anthropic API and paid API authorization remains absolute for this route regardless of how an adapter labels or proxies the upstream call.

## Lifecycle ownership and invariants

1. Jarvis expresses mission intent and requests an authorized A0 ingress; it does not mutate A0's internal queue state.
2. A0 validates issuer/capability, admission, DAG, destination policy, data class, quota, and deadline before creating claims.
3. A0 owns task graph, queue, claim/lease/fencing, dependency scheduling, retry, cancellation, recovery, handoff, and cross-route reconciliation.
4. A task has at most one active claim across all destination classes. Cross-route movement requires a terminal/expired fenced claim plus explicit handoff evidence; no simultaneous duplicate execution.
5. Executors are least-privilege workers and cannot grant themselves admission, choose a forbidden route, change mission authority, or promote results to accepted state.
6. A3 verification is independent of the builder/executor and A0's scheduling success. “Completed” is not “accepted.”
7. MediaHub Product State Authority remains the sole authority for canonical product-state mutation. A0 is engineering workflow authority only.
8. The cloud pool remains operable if Alamo and all user-owned MediaHub destinations are unavailable.

## Required static/contract negative fixtures

- Missing, expired, malformed, untrusted, wrong-audience, or replayed issuer provenance.
- Unknown schema version, destination class, executor ID, router ID/version, provider ID, or authorization/cost class.
- Alamo Claude route selecting Anthropic API inference, paid API credentials, paid API billing, or a paid API authorization path hidden behind a proxy/router.
- FCC/OmniRoute candidate selected without exact version, upstream identity, auth/cost evidence, terms/policy review, egress policy, or Alamo host binding.
- Local-only route with cloud fallback or any automatic route substitution after denial/timeout.
- User-owned MediaHub target without opt-in/admission, locality/egress policy, quota, or revocation check.
- Missing DAG parent binding, duplicate task IDs, dependency cycle, undeclared dependency, workspace overlap, expired deadline, or unbounded retry.
- Two active claims for the same stable task ID, stale fencing generation committing a result, or cross-route handoff without reconciliation record.
- Executor result without route identity, exact source SHA, artifact digest, or independent verification reference.
- Any attempt by Jarvis/A0/executor to mutate canonical product state without Product State Authority.

## Implementation sequence

1. Governance/review: approve or revise this contract design without changing Baseline 2.0 implicitly.
2. Source contract: locate the existing canonical task envelope and issuer lifecycle contract; version/reconcile rather than create a competing schema.
3. Add Draft 2020-12 schema validation and positive/negative fixtures using mock-only providers and destinations.
4. Add static tests proving paid Anthropic API rejection, local-only fail-closed behavior, issuer/destination/DAG validation, and claim fencing.
5. Independently review the exact diff and test outputs.
6. Only after issuer/admission and governance gates pass, plan a separately authorized non-provider runtime test. Do not invoke Claude, FCC, Anthropic, or any cloud agent as part of this documentation/design pass.

## Result and next step

The owner constraints are already recorded as binding target requirements in Wave 268; this wave turns them into a source-grounded contract candidate and makes current implementation gaps explicit. No source code, schema, provider configuration, credentials, hosts, workflows, or runtime were changed or invoked. No tests were run. Nothing is implemented, qualified, deployed, or accepted by this report.

Next bounded action: locate the authoritative issuer and task-envelope contracts in the repository tree and compare them against this field matrix; then add mock-only negative fixtures only after identifying the correct existing test harness and change-control boundary.

- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
- Governance tracker: https://github.com/VlDMlNSh/mediahub-os/issues/301
