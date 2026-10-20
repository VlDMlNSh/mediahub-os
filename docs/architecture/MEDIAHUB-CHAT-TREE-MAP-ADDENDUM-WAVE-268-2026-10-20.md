# MediaHub OS — map addendum, Wave 268 (2026-10-20)

- Status: owner-directed hard target requirements recorded; documentation-only; not implemented, tested, qualified, deployed, or accepted.
- Report: [Wave 268 — A0 multi-tier routing and Alamo Claude non-paid authorization hard constraints](../checkpoints/MEDIAHUB-A0-MULTI-TIER-ROUTING-AND-ALAMO-CLAUDE-NONPAID-AUTH-HARD-CONSTRAINTS-WAVE-268-2026-10-20.md).

## Hard target requirements

1. ASTRA GOLD A0 decomposes hybrid missions into bounded, dependency-aware subtasks and routes among three distinct destination classes: GitHub-hosted cloud-agent pool, admitted user-owned MediaHub devices/instances, and admitted local executors. A0 owns DAG/queue/claim/lease/dependency/retry/cancel/recovery/reconciliation.
2. Claude for this route is exclusively a local executor/client/workspace on Alamo. Anthropic API inference and paid Anthropic API credential/billing/authorization routes are prohibited. Silent cloud fallback is prohibited.
3. FCC (fcc-claude) and similar specialized Claude Code routers are candidates for non-paid authorization/routing only, subject to proof of upstream/auth/cost/billing/data-egress/host identity and compatibility with authentication, terms, limits, and access controls. “Free” does not authorize bypassing controls. Unknown/unqualified route fails closed.
4. Execution on Alamo does not prove local inference. Do not claim local model inference without evidence; the no-Anthropic-API/no-paid-API rule still applies.
5. The GitHub-hosted cloud pool remains independent of Alamo and user-owned devices. User-owned MediaHub and local executors are distinct admitted destinations, not implicit pool dependencies.
6. Executors never gain A0 or Product State Authority. Direct-local Jarvis routing requires its own authorized queue owner/lifecycle and cannot bypass A0 for hybrid missions. Cross-route work requires stable IDs, idempotency, fencing, explicit handoff, and no duplicate active claims.
7. Require issuer provenance, destination admission, capability, locality/egress, budget/quota, revocation, bounded workspaces, evidence, and independent A3 verification.
8. Before runtime use, add negative fixtures for Anthropic API/paid credential selection, unknown FCC/router, missing issuer, unknown destination, cloud fallback, duplicate claims, missing locality policy, and malformed/unbound DAG identity.

## Current blockers

Wave 267 source inspection found that AuthorizationContext lacks issuer provenance and existing task ingress lacks the hybrid destination/DAG/route envelope. Existing FCC/OmniRoute/direct entries do not prove Alamo binding, non-paid authorization, or API exclusion. No runtime qualification is implied.

- Canonical map: [MEDIAHUB-CHAT-TREE-MAP.md](MEDIAHUB-CHAT-TREE-MAP.md)
- Current checkpoint: [mediahub-next-continuation-checkpoint-2026-10-12-current.md](../checkpoints/mediahub-next-continuation-checkpoint-2026-10-12-current.md)
- Master plan: [MEDIAHUB-MASTER-DEVELOPMENT-ROADMAP-1.0.md](../checkpoints/MEDIAHUB-MASTER-DEVELOPMENT-ROADMAP-1.0.md)

- Follow-on contract draft: [Wave 269 — A0 hybrid mission envelope and destination lifecycle](../checkpoints/MEDIAHUB-A0-HYBRID-MISSION-ENVELOPE-AND-DESTINATION-LIFECYCLE-CONTRACT-DRAFT-WAVE-269-2026-10-20.md) and [map addendum](MEDIAHUB-CHAT-TREE-MAP-ADDENDUM-WAVE-269-2026-10-20.md). This is a design candidate, not a normative schema; see source gaps and negative-test plan in that report.
