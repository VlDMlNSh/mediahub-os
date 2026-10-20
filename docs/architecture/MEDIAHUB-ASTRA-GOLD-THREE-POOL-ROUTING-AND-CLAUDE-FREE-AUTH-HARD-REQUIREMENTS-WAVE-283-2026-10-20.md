# ASTRA GOLD — Three-Pool Task Routing and Claude Free-Route Hard Requirements

- Date: 2026-10-20
- Ref: `docs/mediahub-chat-tree-map-20261012`
- Status: **OWNER-DIRECTED HARD REQUIREMENT / TARGET CONTRACT / RUNTIME NOT QUALIFIED**
- Authority note: this records the project owner's explicit architecture direction. It is not, by itself, a governance approval, a merge into `main`, or evidence that any executor/router is installed, admitted, available, safe, or production-qualified.
- Canonical implementation baseline remains Baseline 2.0. Contour B remains gated on Contour A deployment and independent acceptance.

## 1. Mandatory target topology

For delegated multi-pool engineering missions, Jarvis submits a mission to ASTRA GOLD A0. A0 is responsible for decomposing the mission into a bounded task DAG, assigning dependencies and claims, dispatching each eligible subtask, coordinating completion, and reconciling results/evidence.

A0 may dispatch only to these three executor pools, with separate per-pool admission and policy checks:

1. **GitHub-hosted cloud pool** — ephemeral GitHub-hosted execution workers. This pool must remain independently operable without an Alamo device, any user-owned workstation, or a self-hosted/server dependency.
2. **Admitted user machines in the MediaHub pool** — user-owned or user-contributed machines enrolled with explicit consent, per-node identity, least privilege, revocation, bounded workload isolation, data/egress policy, quota limits, and independent result verification. Merely being a user's machine or being connected to a mesh grants no worker eligibility.
3. **Local Claude executor on Alamo only** — the Claude Code/local Claude execution client may run as a local executor on the designated Alamo host. This requirement does not establish Alamo's device identity, software inventory, installed client, provider route, or qualification; each must be evidenced independently. Do not register this local Claude lane on other hosts by inference.

For these delegated multi-pool missions, **A0 is the dispatch and task-lifecycle authority**. Jarvis must not bypass A0 to dispatch directly to a local Claude queue or create a competing queue/claim/lease/recovery authority. The previous direct-local-lane alternative described in Wave 264 is superseded for this target topology unless a separate explicit owner/governance change is recorded.

A0 owns the ASTRA task DAG, queue/claim/lease coordination, retry/cancel/recovery decisions, and evidence reconciliation under the accepted contract. Workers only execute bounded assigned work and return evidence. Neither Jarvis, A0, an executor, nor a router gains MediaHub Product State Authority. Canonical product-state mutation remains with the designated Product State Authority.

## 2. Hard Claude routing and cost boundary

The local Claude executor on Alamo must use only a specifically admitted Claude Code-compatible authentication/routing configuration that has been verified to route through an approved **zero-cost/free-tier-eligible upstream path**. Owner-designated candidates include FCC / Free Claude Code, FreeLLMAPI, OmniRoute, OpenFlux, and similar specialized components. The names are candidate references, not blanket approvals.

**Forbidden for this Claude lane:**
- direct Anthropic paid API routes, including use of a paid Anthropic API credential or direct paid Anthropic endpoint;
- paid Claude/Anthropic account or subscription authorization as the execution credential path for this lane;
- a router profile, downstream provider, model mapping, account authorization, or fallback that can charge a paid route;
- silent fallback to an Anthropic paid path or any other paid route when a free quota, free authorization, provider, or router is unavailable;
- credential sharing, borrowed/session-token reuse, reverse-engineered or unauthorized authentication, quota evasion, or violation of provider terms.

Permitted routing must use valid, explicitly authorized authentication and must conform to each upstream provider's terms. "Free" must mean a verified free entitlement for the selected account/model/path at dispatch time; it must not be inferred from the router's name, an OpenAI-compatible/Anthropic-compatible protocol, a community setup guide, or a default configuration. A route that cannot prove free eligibility and no paid fallback is **BLOCKED**.

On free-quota exhaustion, authorization denial, an unknown or changed endpoint, cost ambiguity, provider policy rejection, or route identity mismatch, the lane must fail closed and report a typed route/eligibility failure to A0. A0 may reassign only if task policy explicitly permits another already-admitted, non-paid route. There must be no implicit cost escalation.

## 3. Router and component admission

Each candidate must be source-pinned (repository, release/tag or commit), identity-checked, and reviewed for install/supply-chain provenance, authentication semantics, downstream endpoint selection, account entitlements, cost/quota behavior, request logging/telemetry, data egress, secret handling, failover, retry/idempotency, cancellation, and evidence output before admission.

- FCC / Free Claude Code, FreeLLMAPI, and OmniRoute are candidates for Claude Code-compatible transport/routing, not authorities or agents.
- The existing `architecture/ASTRA-GOLD-UNIFIED-AUTONOMOUS-DEVELOPMENT-SYSTEM.md@main` identifies the specific EDEAI/OpenFlux candidate as a qualification-gated desktop agent, not as a proven free-only router. Therefore **OpenFlux's exact project identity and role must be reconciled before it is used as a router or placed in the Claude auth path**.
- A component's ability to support both free and paid modes requires an explicit free-only profile and negative tests; selecting the component itself is not enough.
- Secrets must remain outside Git and evidence/artifacts. Store only non-secret route identifiers, endpoint identity, policy/result metadata, quota/cost class, and evidence digests in the route manifest.

Required route-manifest controls before execution include an explicit route ID, host binding (Alamo for the local Claude lane), client/executor identity, router source pin, upstream provider/model identity, auth class, declared cost class, free entitlement/expiry evidence, paid-fallback=false, egress/data classification, quota/failure semantics, bounded timeout, isolated workspace, and independent A3 verification.

## 4. Mission decomposition and cross-pool safety

- The mission is decomposed into bounded child tasks with declared dependencies, required capabilities, data classification, budget/quota constraints, target/workspace, acceptance tests, timeout, and evidence requirements.
- A task may be claimed by only one active executor at a time. Cross-pool handoff requires A0-controlled fencing/reconciliation; no silent duplicate claim or split-brain queue.
- Workspace overlap must be serialized or isolated through disjoint claims. Shared-file work requires explicit ordering.
- A completed child task is not accepted solely because a worker reports success. A3 independent verification and provenance checks remain mandatory.
- Local-only or free-only constraints are hard route filters, not preferences. A fallback that violates them is a policy failure.

## 5. Sequencing and acceptance gates

This document makes the three-pool topology and Claude free-route boundary mandatory target requirements; it does not authorize immediate runtime activation.

1. Preserve the independent GitHub-hosted pool path and qualify it without requiring any local executor.
2. Reconcile governance/issuer/capability, task envelope, A0 ingress, queue lifecycle, and worker evidence contracts before enabling multi-pool dispatch.
3. Admit each user machine separately with consent, identity, sandbox/isolation, data policy, resource limits, revocation, and A3 tests.
4. Admit the Alamo Claude lane only after authorized device/backend inventory and non-mutating qualification prove the exact local client + source-pinned router + free-only upstream path.
5. Add static negative tests for paid Anthropic endpoint/credential, paid downstream route, quota-exhaustion paid fallback, unknown router, unknown OpenFlux identity, unadmitted node, and route-host mismatch.
6. Do not treat documentation, configuration presence, passing static tests, or a route label as runtime qualification, deployment, or acceptance. Contour A remains blocked until its full evidence and independent acceptance gates pass; Contour B remains gated thereafter.

## 6. Source reconciliation and evidence links

- ASTRA GOLD unified target architecture on `main`: [ASTRA-GOLD-UNIFIED-AUTONOMOUS-DEVELOPMENT-SYSTEM.md](https://github.com/VlDMlNSh/mediahub-os/blob/main/architecture/ASTRA-GOLD-UNIFIED-AUTONOMOUS-DEVELOPMENT-SYSTEM.md), blob `e2067dc41b52983fc4e0b2549fb6af3c099cbc60`.
- Existing qualification-gated executor routing candidate on `main`: [local-executor-routing-v2.yaml](https://github.com/VlDMlNSh/mediahub-os/blob/main/ops/agent-fabric/providers/local-executor-routing-v2.yaml), blob `af3d96fe91055af6ba79eded9c800d28d8c0c5c9`. Its `CLAUDE_FCC`, `CLAUDE_OMNIROUTE`, and `CLAUDE_CODE_DIRECT` entries do not prove Alamo identity, free-only downstream policy, or runtime qualification.
- Prior Jarvis/A0/direct-local source reconciliation: [WB-14 source reconciliation](https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/checkpoints/MEDIAHUB-CONTOUR-A-WB-14-JARVIS-A0-AND-DIRECT-LOCAL-ROUTE-SOURCE-RECONCILIATION-2026-10-15.md), blob `4dead9e249603679f4193a5a0b0b0a13a04aa177`.
- FCC project source: https://github.com/bitplz/fcc — describes both free, paid, and local provider choices; a free-only MediaHub profile still must be enforced and tested.
- OmniRoute Claude Code configuration docs: https://omniroute.hagicode.com/en-US/guides/claude-code-configuration/ — supports configured gateway routing; route mode and upstream must be pinned and reviewed.
- FreeLLMAPI overview reference: https://kossolapov.com/en/blog/freellmapi-claude-code — secondary description of free-tier routing and the distinction between Claude Code client and upstream model. This is not supply-chain or provider qualification evidence.

## 7. Change-control status

Owner-directed requirement: **recorded** in this document and its linked Wave 283 report. Governance ratification, normative source reconciliation, implementation, test coverage, runtime route admission, deployment, qualification, and acceptance: **not yet evidenced**.
