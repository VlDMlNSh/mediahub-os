# MediaHub OS — GitHub-hosted Astra control-plane boundary (Wave 383)

Date: 2026-10-22

Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md

Related PR: https://github.com/VlDMlNSh/mediahub-os/pull/483

## Requested topology

- **Astra Gold A0 / issuer:** accepts and authenticates a task envelope, establishes task ID, immutable target SHA, scope, capability, lease/expiry, budget/provider policy and cancellation identity. It does not silently gain Jarvis or Product State Authority.
- **GitHub-hosted supervisor:** owns durable queue orchestration, dependency resolution, leases, retries, timeouts, cancellation, agent assignment, result collection and audit evidence. Queue transitions must not depend on a permanent self-hosted runner being online.
- **Cloud agents:** execute only through the approved GitHub Actions controller and its signed/allowlisted child workflows. The supervisor must not dispatch Gemini children directly or create an alternate credential path.
- **Local executor on Voktors-Mini.Dlink:** remains an execution-only endpoint for explicitly local tasks. It initiates outbound HTTPS/polling or receives a narrowly scoped authorized dispatch; no public inbound listener is assumed. It cannot change issuer, capability, budget, provider policy or canonical product state.
- **Jarvis:** remains a separate local service/authority boundary. It is not a fallback issuer, does not inherit Astra A0 capabilities, and must not be conflated with Product State Authority.
- **Product State Authority:** remains the sole authority for canonical MediaHub product-state mutations.

## What this pass adds

Workflow [Astra GitHub-hosted queue transition proof](https://github.com/VlDMlNSh/mediahub-os/blob/test/autonomous-queue-task-transition-wave382-20261022/.github/workflows/astra-github-hosted-queue-transition-proof.yml) runs on `ubuntu-latest`, with `contents: read`, no configured provider/dispatch secrets, and a pinned checkout action. It runs deterministic queue-state tests only. It is intentionally not a production dispatcher and does not claim to execute Gemini, Claude, Jarvis or a local worker.

The existing queue module has a permanent executor pool that includes `mh-dev-01`, `mh-dev-02` and `Voktors-Mac-mini.local`. That module cannot be treated as a server-independent supervisor without separating scheduling/control-plane logic from worker execution and revising its authority and persistence contracts. Do not weaken hostname assertions or impersonate canonical nodes.

## Required implementation stages

1. **GitHub-hosted transition proof:** exact-head CI verifies `QUEUE-A -> VERIFIED -> QUEUE-B -> VERIFIED -> IDLE` using deterministic worker doubles. This is state-machine evidence only.
2. **Control-plane extraction:** move queue selection, durable task state, leases, retry/cancel and audit manifest to a GitHub-hosted-safe controller module. Remove implicit dependence on local paths and the permanent self-hosted pool from the control plane. Keep worker adapters separate.
3. **A0 ingress and durable store:** specify signed task envelope, issuer identity, idempotency key, immutable target SHA, allowed task types, budget, route/model policy, expiry, cancellation and recovery. Missing/ambiguous authority must fail closed. A GitHub issue/documentary task list alone is not a scheduler.
4. **Cloud-agent adapter:** extend the existing Gemini controller only through a reviewed contract change. Verify it accepts the exact task envelope or signed task reference, preserve HMAC/capability checks, secret isolation, unique child dispatch IDs/branches, quota resume and artifact provenance. Do not invoke child workflows directly.
5. **Local-executor adapter:** qualify the third host ID/capabilities/allowlist and a permitted free route. Executor should pull only a signed, leased task addressed to its registered identity, return a signed result/evidence manifest, and support cancellation/expiry. No Gemini traffic may be routed through the Mac.
6. **Independent security review and qualification:** negative tests for replay, stale SHA, duplicate lease, revoked capability, wrong executor, provider/budget mismatch, cancellation race, secret leakage, poisoned artifact, and result/provenance mismatch.
7. **Activation:** only after all relevant gates pass, enable production ingress and controlled dispatch. Design, implementation, CI, qualification and acceptance remain separate statuses.

## Current status

- GitHub-hosted queue proof workflow: **IMPLEMENTED ON PR BRANCH / CI NOT VERIFIED** until exact-head run finishes.
- Deterministic transition test: present on PR #483 branch; the hosted workflow is intended to execute it.
- Production GitHub-hosted supervisor / durable scheduler: **PLANNED / NOT IMPLEMENTED**.
- Task-specific signed Gemini dispatch: **NOT VERIFIED**; existing controller uses fixed role prompts and must not be assumed to accept arbitrary task focus.
- Local worker polling/lease/result protocol: **NOT IMPLEMENTED / NOT VERIFIED**.
- Full topology qualification and acceptance: **NOT ACCEPTED**.

## Evidence and next step

- Base SHA at start of Wave 382: `11d04d2f2687e9ba9215e4b67af2e450516960bb`.
- PR #483 initially targeted the deterministic queue transition test; this wave adds a GitHub-hosted test runner and topology contract.
- Workflow file blob SHA and exact-head CI must be re-read after the branch settles.
- Next: inspect the exact-head workflow run, then implement the smallest isolated control-plane extraction only after mapping current A0 issuer/lease/cancel and agent-fabric contracts. Do not activate real agent dispatch from this test workflow.
