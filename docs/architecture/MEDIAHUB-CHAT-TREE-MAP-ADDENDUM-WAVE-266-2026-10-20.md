# MediaHub project map addendum — Wave 266 (2026-10-20)

## Owner-mandated hard constraints
- ASTRA GOLD A0 decomposes hybrid missions into bounded dependency-aware tasks and routes across the GitHub-hosted cloud pool, admitted user-owned MediaHub instances/devices, and admitted local executors.
- Claude Code execution for this requirement is local to Alamo. Anthropic API and paid Anthropic API credential/billing routes are explicitly forbidden for that route; no silent cloud fallback.
- FCC (fcc-claude) and similar specialized routers are candidate non-paid Claude Code authorization/routing mechanisms, but remain qualification-gated. Prove actual upstream, auth/credential class, terms/policy compatibility, cost class, egress and host identity. Never infer authorization from the word “free” or bypass authentication, provider terms, rate limits or access controls.
- Executor location is distinct from inference location. Alamo runs the Claude Code executor/workspace; that alone does not prove local model inference. Do not claim a local model unless verified.
- A0 owns hybrid queue/task lifecycle, claims/leases, DAG dependencies, retry/cancel/recovery and cross-route reconciliation. Executors are not ASTRA or Product State Authority. User-owned MediaHub is a separate destination class with admission, issuer/capability, locality/egress, quota/budget, revocation and evidence controls.
- Cloud pool must work without Alamo/user-owned devices. Direct-local Jarvis queueing, if retained, needs a separate owner/authorization lifecycle and cannot bypass A0 for A0 hybrid missions. Unknown route/auth/authority fails closed.
- Static negative fixtures must reject Anthropic API/paid credentials for Alamo Claude, unknown/unqualified FCC variants and silent fallback. Real runtime qualification remains separately gated.

## Evidence
- [Wave 266 report](../checkpoints/MEDIAHUB-A0-ALAMO-CLAUDE-FCC-AUTH-BOUNDARY-WAVE-266-2026-10-20.md)
- [Wave 265 A0 multi-tier requirements](../checkpoints/MEDIAHUB-A0-MULTI-TIER-ROUTING-AND-ALAMO-LOCAL-CLAUDE-REQUIREMENTS-WAVE-265-2026-10-20.md)
- Existing routing candidate: ops/agent-fabric/providers/local-executor-routing-v2.yaml@main, blob af3d96fe91055af6ba79eded9c800d28d8c0c5c9. Its presence does not prove active admission or FCC auth properties.
- Current project map is an inventory, not implementation/qualification acceptance. Contour A remains NOT_PROVEN / BLOCKED.

## Next
Reconcile accepted A0 ingress and typed AuthorizationContext/issuer contracts with mission/task/destination schemas, then add schema-level and mock-based negative tests before any real dispatch.
