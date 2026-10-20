# MediaHub OS — map addendum, Wave 270 (2026-10-20)

- Status: owner reaffirmation of hard target architecture requirements; documentation/navigation synchronization only; not an accepted runtime schema and not implemented or qualified.
- Report: [Wave 270 — owner hard requirements and plan synchronization](../checkpoints/MEDIAHUB-A0-OWNER-HARD-REQUIREMENTS-AND-ROADMAP-SYNC-WAVE-270-2026-10-20.md).
- Binding predecessor: [Wave 268 hard constraints](../checkpoints/MEDIAHUB-A0-MULTI-TIER-ROUTING-AND-ALAMO-CLAUDE-NONPAID-AUTH-HARD-CONSTRAINTS-WAVE-268-2026-10-20.md).
- Contract-design predecessor: [Wave 269 A0 hybrid mission envelope and destination lifecycle draft](../checkpoints/MEDIAHUB-A0-HYBRID-MISSION-ENVELOPE-AND-DESTINATION-LIFECYCLE-CONTRACT-DRAFT-WAVE-269-2026-10-20.md).

## Hard requirements reaffirmed
1. A0 decomposes missions into bounded dependency-aware subtasks and schedules them among the GitHub-hosted cloud pool, admitted user-owned MediaHub instances/devices, and admitted local executors. A0 owns DAG, queue, claims/leases, scheduling, retry, cancellation, recovery, fencing, handoff, and cross-route reconciliation.
2. Claude/Claude Code for this target is exclusively a local Alamo executor. Anthropic API use, paid Anthropic API credentials/billing/authorization routes, and silent fallback are prohibited.
3. FCC/fcc-claude and similar routers are conditional non-paid authorization/routing candidates only. Verify upstream, auth/cost class, billing, terms/limits, router identity/version, data egress, and Alamo binding. “Free” is not proof of permission; no bypass of provider controls. Unknown or unqualified routes fail closed.
4. Alamo execution does not prove local inference. Do not claim local inference without evidence; the Anthropic API/paid-route exclusion still applies.
5. The GitHub-hosted cloud pool remains independent of Alamo and user-owned devices.
6. Preserve issuer/capability provenance, destination admission, locality/egress and budget policy, idempotency/fencing, no duplicate active cross-route claims, structured evidence, and independent A3 verification.
7. Before runtime use, add negative fixtures for paid Anthropic API, unknown router/destination, missing issuer, silent fallback, duplicate claims, missing locality policy, and malformed DAG identity.

## Next step
Continue Wave 269: reconcile mission-envelope fields against accepted issuer/task contracts; add negative fixtures; require exact-head CI, independent review, and authorized qualification. Keep Contour A cloud-pool independence and the Contour B acceptance gate.

- Canonical map: [MEDIAHUB-CHAT-TREE-MAP.md](MEDIAHUB-CHAT-TREE-MAP.md)
- Checkpoint: [current continuation checkpoint](../checkpoints/mediahub-next-continuation-checkpoint-2026-10-12-current.md)
- Master roadmap: [Master Development Roadmap](../checkpoints/MEDIAHUB-MASTER-DEVELOPMENT-ROADMAP-1.0.md)
