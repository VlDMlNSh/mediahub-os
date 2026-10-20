# MediaHub Chat Tree Map — Addendum Wave 264 (2026-10-20)

## Jarvis dual-route target clarified
Owner clarified that Jarvis should support both:
- Direct-local autonomous queue submission to an admitted local executor such as Claude Code on Alamo.
- Hybrid distributed mission submission to ASTRA GOLD A0, which decomposes work into dependency-aware subtasks and routes eligible work to GitHub-hosted cloud workers and admitted local executors such as Claude/Alamo.

The intended device-role topology (Claude on Alamo, described as Mac mini 2018; Codex API/tooling on MacBook) is an owner-supplied target, not verified device inventory. Keep Claude Code client, Anthropic-hosted Claude model, and Claude-compatible local backend distinct.

## Existing contracts / unresolved gaps
- WB-14 source reconciliation on main, blob 4dead9e249603679f4193a5a0b0b0a13a04aa177, already identifies missing Jarvis authenticated ingress, no Alamo lane in the current fixed queue, unnamed direct-route queue owner, and open cross-route retry/cancel/recovery.
- Corporation crosswalk on main, blob 721e4c994d4800df4605af52630ea75339971a27, says DAG decomposition and the full corporation contract remain partial/proposed.
- ASTRA GOLD unified design on main, blob e2067dc41b52983fc4e0b2549fb6af3c099cbc60, establishes A0 as single coordination/state authority; executors are not authority.
- CLAUDE_CODE_DIRECT in ops/agent-fabric/providers/local-executor-routing-v2.yaml is qualification-gated, not proof Alamo is admitted. Current autonomous queue has no established Alamo lane.

## Required invariants
- A0 owns ASTRA queue/claim/lease/recovery lifecycle for hybrid-route tasks; Jarvis cannot directly mutate A0 internals.
- Direct-local Route A needs a separately named queue owner, authenticated issuer/capability, idempotency/fencing and auditable result envelope.
- A task cannot be active in both routes without an explicit handoff/fencing protocol.
- Cloud-pool availability must not depend on the Mac mini or another customer-managed server.
- No silent cloud fallback in local-only mode; A3 independent verification and Product State Authority boundary remain intact.
- The owner clarification does not qualify or authorize execution.

Full evidence: [Wave 264 report](../checkpoints/MEDIAHUB-JARVIS-DUAL-ROUTE-AND-ASTRA-HYBRID-QUEUE-TOPOLOGY-WAVE-264-2026-10-20.md)

Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md