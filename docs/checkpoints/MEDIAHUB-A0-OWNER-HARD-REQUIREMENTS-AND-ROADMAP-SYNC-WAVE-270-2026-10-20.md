# Wave 270 — Owner hard requirements reaffirmation and plan synchronization (2026-10-20)

## Status
OWNER-DIRECTED ARCHITECTURE REQUIREMENTS; documentation-only. This record explicitly reaffirms the owner's latest clarification and links it to Wave 268 hard constraints and the Wave 269 contract draft. It does not amend Functional Baseline 2.0, accept the proposed schema, or bypass governance and qualification.

## Binding target requirements
1. **ASTRA GOLD A0 coordinates hybrid work.** A0 decomposes missions into bounded, dependency-aware subtasks and distributes eligible work among (a) the GitHub-hosted cloud-agent pool, (b) admitted user-owned MediaHub instances/devices, and (c) admitted local executors. A0 owns task DAG, queue/claim/lease, dependency scheduling, retry, cancellation, recovery, explicit handoff, fencing, and cross-route reconciliation.
2. **Claude is exclusively a local Alamo executor on this route.** Claude/Claude Code execution must be anchored to Alamo. Anthropic API use, paid Anthropic API credentials/billing/authorization routes, and silent fallback to cloud or paid routes are prohibited. An intermediary router does not make a prohibited API route acceptable.
3. **FCC and similar specialized routers are conditional candidates only.** FCC/fcc-claude or equivalent may be assessed for non-paid Claude Code authorization/routing only after verification of upstream, authorization and cost class, billing, terms/usage limits, router identity/version, data egress, and Alamo binding. “Free” is not proof of authorization. Do not bypass authentication, subscription terms, provider controls, or rate limits. Unknown/unqualified routes fail closed.
4. **Execution locality is not inference locality.** Claude Code on Alamo does not prove that inference is local or that the upstream route is permitted. Make no local-inference claim without independent evidence; the Anthropic API/paid API exclusion remains absolute for this route.
5. **The GitHub-hosted cloud pool remains independent.** Alamo and user-owned MediaHub are optional, separately admitted destinations and must not become dependencies of the cloud execution plane.
6. **Authority remains separated.** A0 coordinates engineering missions but is not MediaHub Product State Authority. Executors cannot self-admit, elevate capabilities, or accept their own output. A direct Jarvis-to-local queue, if retained, requires a separately named owner, issuer/capability contract, and lifecycle; it cannot bypass A0 for hybrid missions.
7. **Fail-closed execution and evidence.** Require authenticated issuer provenance, destination admission, capabilities, locality/egress policy, quotas/budgets, revocation, bounded workspaces/claims, stable task identity, idempotency/fencing, explicit handoff, structured evidence, and independent A3 verification. No duplicate active claim across destinations.
8. **Negative tests before runtime use.** Schema/static/mock-only tests must reject paid Anthropic API routes for Alamo Claude, unknown router/destination, missing issuer, silent fallback, cross-route duplicate claims, missing locality/egress policy, and malformed/unbound DAG/task identity. Runtime/provider/host/secret/dispatch activity requires separate authorization and evidence.

## Source reconciliation
- Wave 268 already records the requirements as hard target constraints: [report](MEDIAHUB-A0-MULTI-TIER-ROUTING-AND-ALAMO-CLAUDE-NONPAID-AUTH-HARD-CONSTRAINTS-WAVE-268-2026-10-20.md).
- Wave 269 translates them into a candidate mission envelope and destination/lifecycle matrix, explicitly not an accepted normative contract: [draft](MEDIAHUB-A0-HYBRID-MISSION-ENVELOPE-AND-DESTINATION-LIFECYCLE-CONTRACT-DRAFT-WAVE-269-2026-10-20.md).
- Existing source gaps remain: issuer provenance, destination/DAG/route/locality envelope, and enforcement of Alamo's non-paid/API-exclusion rule are unproven in current ingress/gateway.
- FCC, OmniRoute, and Claude Code direct entries are candidates, not runtime admission or qualification evidence.

## Next steps
1. Reconcile Wave 269 fields against authoritative issuer/task contracts.
2. Produce a field-level destination responsibility/lifecycle matrix and static/schema/mock-only negative fixtures.
3. Prove issuer provenance, destination admission, Alamo host binding, router upstream/auth/cost class, and API exclusion before real execution.
4. Require exact-head CI and independent review before authorized qualification.
5. Preserve cloud-pool independence. Contour B remains blocked until Contour A is deployed and independently accepted.

## Evidence / status
- Canonical map: [MEDIAHUB-CHAT-TREE-MAP.md](https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md)
- [Issue #301](https://github.com/VlDMlNSh/mediahub-os/issues/301); [PR #421](https://github.com/VlDMlNSh/mediahub-os/pull/421)
- Refreshed docs branch HEAD before this pass: `82df9b91688200e709a8c6a9b2a26d0bc924b13c`; main HEAD observed: `80be45a70732b1d568164571d4273a6397792c3b`. Issue #301 and draft PR #421 were open in the fetched metadata.
- This documentation pass did not execute tests, invoke providers, inspect hosts, read secret values, dispatch agents, merge, deploy, qualify, or accept the system.

**Result:** requirements reaffirmed and plan/navigation synchronization recorded; implementation/runtime enforcement NOT VERIFIED; tests NOT RUN; Contour A NOT_PROVEN / BLOCKED.
