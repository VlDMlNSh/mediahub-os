# Wave 271 — A0 issuer/task contract reconciliation (2026-10-20)

## Status
READ-ONLY SOURCE RECONCILIATION; owner-directed hard requirements remain binding target requirements. This pass did not modify runtime code, accept Wave 269 as a normative contract, or authorize execution.

## Refreshed repository state
- Canonical documentation branch before this commit: `docs/mediahub-chat-tree-map-20261012` at `1232734db801e08e5d16951ee247740ee06bf0d0`.
- `main` HEAD: `80be45a70732b1d568164571d4273a6397792c3b`.
- Issue #301: OPEN, last updated 2026-10-20T14:17:18Z.
- PR #421: OPEN / DRAFT; head `84e2d0bbb4163942f5ba010591cb5d3c9d6a7581`, base `80be45a70732b1d568164571d4273a6397792c3b`. No merge or acceptance inferred.
- Source files below were read from the exact refs and blob SHAs listed.

## Source-to-contract reconciliation
1. `runtime/mediahub_runtime/task_ingress.py@main`, blob `59e1254aa61cc8f55f53bd1e179631e81c441393`: `FileTaskIngress` accepts `mediahub.ai.astra-task@1.0.0`, validates request/session/user-command/approval and basic context refs, and passes the request into the existing bounded gateway. It does **not** authenticate an issuer, validate a capability/audience/signature/replay nonce, admit a destination, represent a DAG, bind locality/egress or cost class, or implement cross-route claim fencing.
2. `runtime/mediahub_runtime/authorization.py@main`, blob `4d8df5d3c1c26f7f133a8093cd270635b085f4d5`: `AuthorizationContext` is only `principal` + `capability`; `AuthorizationPolicy` is an explicit in-process allow-list. This is a useful fail-closed authorization seam, but by itself does not prove trusted ingress provenance, signature verification, audience, expiry, replay protection, destination admission or a signed A0 mission envelope.
3. `runtime/mediahub_runtime/astra_gateway.py@main`, blob `10985e4ad8f682313d08e7492ecc1856a8bce20f`: the gateway is explicitly cloud-first and the shown local executor is Ollama. Its source does not prove the target A0 multi-tier scheduler or Alamo Claude route policy. It must not be silently reinterpreted as the requested hybrid controller.
4. `runtime/mediahub_runtime/autonomous_queue.py@main`, blob `72c4a5ccb367884fb02d247b1b8848ea62c3c6b1`: the queue uses local filesystem state and a fixed executor pool; this is not a distributed A0 queue and does not prove Alamo host identity, user-owned MediaHub admission, or global cross-route fencing.
5. `ops/agent-fabric/providers/local-executor-routing-v2.yaml@docs/mediahub-chat-tree-map-20261012`, blob `af3d96fe91055af6ba79eded9c800d28d8c0c5c9`: FCC/OmniRoute/direct Claude Code entries are explicitly qualification-gated candidates. They do not prove upstream, auth/cost class, terms, egress, version or Alamo binding.
6. `schemas/ai/ai-provider-registry.schema.json@main`, blob `9537a64bc948b1bea3e2a640670f48e107760a50`, and `schemas/ai/ai-provider-adapter.schema.json@main`, blob `e0dab7002222451579e649a7d1d29985393d9a42`: these describe provider/adapter records, not the A0 mission issuer, task DAG, destination admission or cross-route lifecycle. They cannot be treated as validating Wave 269's proposed envelope.

## Requirements that remain hard constraints
- A0 is the sole hybrid mission/task DAG, queue, claim/lease, retry, cancel, recovery, handoff, fencing and cross-route reconciliation authority.
- A0 distributes bounded, dependency-aware tasks only among the GitHub-hosted cloud pool, explicitly admitted user-owned MediaHub, and explicitly admitted local executors.
- The GitHub-hosted cloud pool must remain operational without Alamo or user-owned devices.
- Claude/Claude Code in this target is exclusively a local Alamo executor. Anthropic API use, paid Anthropic API credentials/billing/authorization routes and silent fallback are prohibited. FCC/fcc-claude or similar routes are candidates only after upstream/auth-cost/terms/limits/version/egress/Alamo-binding evidence. “Free” is not proof of permission; do not bypass provider controls.
- Alamo execution does not prove local inference. No route may be enabled while issuer, destination, provider/auth class, locality/egress or budget is unknown.
- Product State Authority remains separate; executor completion is not acceptance; independent A3 verification remains required.

## Gap disposition and next bounded step
The existing issuer seam is too small to validate the candidate mission envelope, while the provider schemas solve a different contract layer. Do not wire Wave 269 into runtime or create a parallel controller. Next, inspect the authoritative Task Contract producer/writer and approval/attestation lifecycle, then draft a field-by-field mapping to existing contracts. Add schema/static/mock-only negative fixtures only after that mapping identifies the canonical extension point. Required denials include missing/untrusted/replayed issuer, unknown destination/router/auth class, paid Anthropic API on Alamo, silent fallback, missing locality/egress policy, malformed DAG identity and cross-route duplicate claims.

## Verification limits
This was a read-only source pass plus documentation synchronization. No tests were run; no provider calls, secrets, host inspection, agent dispatch, merge, deployment, qualification or acceptance occurred. Contour A remains NOT_PROVEN / BLOCKED. Contour B remains blocked until Contour A deployment and independent acceptance.

- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
- Issue #301: https://github.com/VlDMlNSh/mediahub-os/issues/301
- PR #421: https://github.com/VlDMlNSh/mediahub-os/pull/421
