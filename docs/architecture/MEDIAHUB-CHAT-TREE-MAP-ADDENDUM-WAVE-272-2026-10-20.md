# Map addendum — Wave 272: A0 hybrid routing and Alamo Claude hard auth restrictions (2026-10-20)

## Binding owner-directed target requirements

See the full requirements and evidence in the [Wave 272 report](../checkpoints/MEDIAHUB-A0-MULTI-TIER-ROUTING-AND-ALAMO-CLAUDE-NONPAID-AUTH-HARD-REQUIREMENTS-WAVE-272-2026-10-20.md).

- ASTRA GOLD A0 is the single hybrid mission/DAG/queue lifecycle authority. It decomposes bounded dependency-aware subtasks and routes eligible work only to admitted GitHub-hosted cloud workers, admitted user-owned MediaHub, and admitted local executors.
- A0 owns queue/claim/lease, retry/cancel/recovery, handoff/fencing, cross-route reconciliation and evidence aggregation. Executors do not mutate A0 coordination state or gain Product State Authority. Independent A3 verification remains required.
- The GitHub-hosted cloud pool must work without Alamo or user-owned devices.
- Claude/Claude Code for this target is exclusively a local executor on Alamo. Anthropic API, paid API credentials/billing/authorization, proxy-mediated paid API use, and silent fallback are prohibited on that route.
- FCC/fcc-claude and equivalent specialized auth/router components are conditional only after evidence proves permitted upstream/auth mode, non-paid auth/cost class, billing behavior, terms/limits, version, egress and Alamo binding. “Free” alone is not authorization. No provider-control bypass.
- “Executor runs on Alamo” is not evidence that model inference itself is local. State only the locality demonstrated by source and egress evidence.
- Unknown issuer, capability, destination, router/auth class, locality, budget or revocation state must fail closed; no duplicate cross-route active claim without explicit fenced handoff.

## Required next work

Trace the authoritative Task Contract producer/writer and approval/attestation lifecycle; reconcile Wave 269 candidate fields against accepted contracts; produce the destination/lifecycle responsibility matrix and static/schema/mock-only negative tests. Keep runtime wiring behind exact-head CI, independent review and route qualification.

## Status

This addendum captures hard owner-directed target constraints, not implementation or route qualification. Wave 272 report, current checkpoint and Master Roadmap provide linked continuation state.

- Canonical map: [MEDIAHUB-CHAT-TREE-MAP.md](MEDIAHUB-CHAT-TREE-MAP.md)
- Current checkpoint: [continuation checkpoint](../checkpoints/mediahub-next-continuation-checkpoint-2026-10-12-current.md)
- Master roadmap: [Master Development Roadmap](../checkpoints/MEDIAHUB-MASTER-DEVELOPMENT-ROADMAP-1.0.md)
- Issue [#301](https://github.com/VlDMlNSh/mediahub-os/issues/301); PR [#421](https://github.com/VlDMlNSh/mediahub-os/pull/421).
