# MediaHub Chat Tree Map — Addendum Wave 261 (2026-10-20)

## Direction
Cloud-pool design must evaluate mature, ready-made multi-agent frameworks and corporation-enabling components, not merely model API endpoints. Compare and integrate the smallest compatible stack from existing projects before custom orchestration.

## Existing sources checked on main snapshot `80be45a70732b1d568164571d4273a6397792c3b`
- Provider registry `ops/qualification/provider_model_registry.json`, blob `62328126fd2cd8879a73bb6812adcacd3e2abe84`.
- ECC integration decision `docs/operations/ASTRA-ECC-INTEGRATION.md`, blob `c707a83777ae5970081bd6bb1e3027c88bbf3fa1`: ECC is not adopted as a second controller/dependency; selected development practices are used under Astra's executable gates.
- Proposed cloud router ADR `docs/architecture/MEDIAHUB-CLOUD-MULTIAGENT-ROUTER-ADR-WAVE-42-2026-10-17.md`, blob `f445e2ab6b43dfcae275ffa598e44ab18049e504`; remains proposed/source review partial/implementation gated.
- Agent Fabric runtime `runtime/mediahub_runtime/agent_fabric.py`, blob `3c70dda5df8c6caa9411201d754ead6b3bfdf6dd`, contains bounded file-backed claims/leases, not a full distributed cloud orchestrator.
- Local executor routing qualification `ops/agent-fabric/providers/local-executor-routing-v2.yaml`, blob `af3d96fe91055af6ba79eded9c800d28d8c0c5c9`, remains qualification-gated.

## Candidate stack layers
1. Multi-agent orchestration frameworks (e.g. LangGraph, AutoGen, CrewAI, OpenHands/SWE-agent; ECC only within its existing governance boundary).
2. Durable queue/state, atomic leases, retries, idempotency and recovery.
3. Provider/model router with quota/reset/cooldown/concurrency reservation and fail-closed fallback.
4. Isolated execution substrate and secret boundary.
5. Evidence, tracing, audit, budget control, revocation and independent verification.
6. Corporate roles/pools, coordinator/supervisor, task assignment, conflict control, escalation and human approval.

Every upstream component is a candidate until exact version/source, license, maintenance, security, isolation, authority boundaries, test evidence and rollback are reviewed. Mock-provider prototypes precede real provider calls. The existing Astra controller and Product State Authority boundaries remain intact; adopting ECC as a second controller requires explicit governance change control.

## Current status
Planning/source inventory only; no components installed, provider calls made, agents launched, routes enabled, or deployment/qualification accepted.

## Next
Build a source-grounded component comparison matrix and mock-provider proof of the smallest viable orchestration/router/state stack. Treat the Wave 42 router ADR as proposed and address its documented fail-open, non-atomic quota selection, credential-in-URL and missing task-policy issues before adoption.


## Wave 262 — infrastructure boundary refinement

The cloud pool is GitHub-cloud-only for orchestration, scheduling/dispatch, worker execution, coordination, artifacts and evidence. No dedicated hardware, VPS, self-hosted runner, local workstation, NAS, or always-on listener is a pool dependency. External model APIs are permitted only as authorized endpoints called from GitHub-hosted jobs, not as alternate orchestration infrastructure. Servers are reserved for later Jarvis/local compute; Jarvis/local executor work follows cloud-pool deployment and independent acceptance. Any requirement for an external hosted queue/database/router must be raised as an explicit governance capability gap, not introduced silently.

Evidence: [Wave 262 report](../checkpoints/MEDIAHUB-GITHUB-CLOUD-ONLY-POOL-AND-LOCAL-JARVIS-BOUNDARY-WAVE-262-2026-10-20.md).

Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
