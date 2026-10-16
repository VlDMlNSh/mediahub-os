# MediaHub OS — Project Map Addendum, Wave 37 (Post-Merge Gemini Diagnostic)

- Date: 2026-10-17
- Parent map: [MEDIAHUB-CHAT-TREE-MAP.md](MEDIAHUB-CHAT-TREE-MAP.md)
- Parent map blob SHA observed: `fcef1bf0c8329b76ad640f774d23493cfa9157a5`
- Documentation ref: `docs/mediahub-chat-tree-map-20261012`
- Main HEAD observed: `6c2e8dbdee81c798b64e65546e7ded07093f100a`
- Branch comparison: `diverged`; docs branch ahead 1961 / behind 14; merge base `f0f406feb9f9816b009f4e6e756813541e53b9bc`.
- Status: **NAVIGATION ADDENDUM / SOURCE-BOUND DIAGNOSTIC / PROPOSED / RUNTIME UNVERIFIED**

## Navigation entry

### MH-CLOUD-AGENT-PORTABILITY-W37 — Post-Merge Gemini Diagnostic and Portable Cloud-Agent Fabric

Primary report:
- [Post-Merge Gemini Diagnostic and Cloud-Agent Portability, Wave 37](../checkpoints/MEDIAHUB-POST-MERGE-GEMINI-DIAGNOSTIC-AND-CLOUD-AGENT-PORTABILITY-WAVE-37-2026-10-17.md), blob SHA `b13a347b904de03393a393f72942cae67bf3acf8`.

Related control/evidence sources:
- [Master Development Roadmap 1.0](../checkpoints/MEDIAHUB-MASTER-DEVELOPMENT-ROADMAP-1.0.md), Wave 37 companion appended.
- [Unified System Traceability Matrix v0.1](../checkpoints/mediahub-unified-system-traceability-matrix-v0.1.md), Wave 37 controls CAF-84…CAF-89; blob SHA `cfc56fa4142b051e9ad48265e190c65d9dccaf1c`.
- [Canonical Source Registry and Security Evidence Ledger](../checkpoints/MEDIAHUB-CANONICAL-SOURCE-REGISTRY-AND-SECURITY-EVIDENCE-LEDGER-WAVE-03-2026-10-16.md), SRC-096…SRC-100 and EVD-050…EVD-053; blob SHA `db6ca40d5c12a0d87323604dfd955e14da35ac41`.
- [Current continuation checkpoint](../checkpoints/mediahub-next-continuation-checkpoint-2026-10-12-current.md), Wave 37 resume record appended.

## Confirmed findings

- PR #305 (MCP tool names) and PR #306 (token interpolation) are merged into main.
- Main at this review: `6c2e8dbdee81c798b64e65546e7ded07093f100a`. The current Gemini dispatch workflow blob: `9be13613ae79f316ca410c16c6e69e2aea7283a4`.
- Astra Verify run #38976598150 succeeded on current main; that is CI evidence only.
- Gemini dispatch run #38976095754 failed the final response validator. Its archived artifact contains an empty response, `INVALID_STREAM`, `MALFORMED_FUNCTION_CALL`, and MCP “Tool ... not found” errors. Earlier run #38972774167 produced a false-positive wrapper success despite invalid stream/tool-call output.
- Fresh post-merge Gemini MCP invocation and PR creation remain unverified.
- Cloud runner placement can be independent of a permanent owner-operated server. Credential identity remains provider/account/project or approved repository/environment scoped; actual network egress, region, provider terms and data-use rules remain explicit policy inputs.
- The existing catalog, architect/builder/verifier roles, provider schemas and 23-lane manifest are reuse-first components. The 16-entry activation queue is documentary, with no qualified live scheduler; A0 and R-06 remain open.
- Existing three-node topology remains unchanged: Mac mini 2018/macOS, Mac mini 2011/Linux and remote video server. Hosted cloud compute is an additive lane.

## Next route

1. Read the pinned OpenHands Agent Server routes/configuration and workspace/tool enforcement at the exact source revision already recorded by Wave 24/25.
2. Compare route exposure, session-key enforcement, command/file capabilities, workspace isolation and outbound egress to A0, MH-12 and R-06.
3. Carry evidence into the existing matrix and canonical source registry after collision checks.
4. Propose a bounded implementation/qualification slice only after unresolved authority, privacy and target gates are addressed.

## Parent map handling

The current GitHub contents connector returns the large canonical map blob SHA but an empty body, including ranged content reads. The parent map remains unchanged and authoritative. This addendum preserves navigation until a safe full-body revision procedure is available.

Current project map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md


## Agent-browser operational verification and registry admission route

Additional bounded pass on 2026-10-17:
- Installed `agent-browser` CLI version `0.27.0` was invoked directly.
- `agent-browser skills get core` returned the installed CLI workflow guide.
- A public GitHub checkpoint page opened; `get url` returned the target URL; `snapshot -i -d 2` exposed the checkpoint title and latest commit link.
- Use `agent-browser` as the default browser automation CLI for future browser tasks, with fresh snapshots after navigation and existing authorization gates retained.
- Primary evidence: [Agent Browser Operational Verification and Registry Admission Inventory, Wave 37](../checkpoints/MEDIAHUB-AGENT-BROWSER-OPERATIONAL-VERIFICATION-AND-REGISTRY-INVENTORY-WAVE-37-2026-10-17.md).

Registry admission crosswalk:
- `profiles/agent-registry.json` v1.2.0, blob `993cbbe1b2b2a88da7d8884a897b404f055981a8`.
- `schemas/ai/ai-provider-registry.schema.json` is a distinct provider-registry contract, not an agent-profile schema.
- `.github/workflows/mediahub-agent-fabric-verify.yml` has no visible direct path trigger or validation step for the agent profile catalog.
- Full consumer inventory remains OPEN because GitHub code search returned incomplete results. Complete source-tree crosswalk before proposing a schema or validator.
