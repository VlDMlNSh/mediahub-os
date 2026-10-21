# Wave 329 — Gemini admission and Voktors executor status

Date: 2026-10-21. Report: [Wave 329 Gemini batch admission and Voktors executor recovery check](../checkpoints/MEDIAHUB-NEXT-GEMINI-BATCH-AND-VOKTORS-RECOVERY-WAVE-329-2026-10-21.md). Canonical map: [MEDIAHUB-CHAT-TREE-MAP.md](MEDIAHUB-CHAT-TREE-MAP.md) on [`docs/mediahub-chat-tree-map-20261012`](https://github.com/VlDMlNSh/mediahub-os/tree/docs/mediahub-chat-tree-map-20261012).

- `main` HEAD `79196054d84b1197cea1447dd1db5ad075302834`; controller blob `9453403bba899a2400ee3fb874d32badd034c704`.
- Controller runs [39667761725](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39667761725), [39667424495](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39667424495), and [39665960179](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39665960179) all completed with every job SKIPPED and no artifacts. No Gemini child dispatch/run IDs or reports exist.
- The controller expects exact ASCII `MEDIAHUB_DISPATCH_HMAC_KEY`; the owner-supplied spelling `MEDIAHUB_DISPATCH_НМАС_KEY` is not equivalent because it contains Cyrillic characters. Verify the exact configured name in GitHub Settings without revealing the secret value.
- PR #437 remains OPEN/DRAFT at `e7e99c2fe5f090df3a731b0b1a7f3fcb5335bd14`; exact-head CI/status and independent review remain absent. `main.protected=false` in the branch response; rulesets list empty; detailed protection API unavailable to this integration. Do not dispatch until gates are closed.
- SentinelX lists `Voktors-Mini.Dlink` (`host_5f7264034bdf0b51`) as operational, but ping/capabilities/state/help timed out and a read-only command probe disconnected due to duplicate session. No allowlist verification, browser CLI guide retrieval, browser session, Claude/FCC execution or paid fallback.
- Gemini Agents 1–3: NOT RUN. Claude/FCC: NOT RUN. agent-browser: NOT RUN. No qualification or acceptance.
- Next: verify exact ASCII secret name, variable scope/value, token permissions and governance; then, only after review/exact-head CI/trusted-main probe, consider one controller-only batch on a shared immutable SHA. Separately restore host stability and qualify browser/Claude routes.


Owner's latest spelling clarification: `MEDIAHUB_DISPATCH_NMAC_KEY` is ASCII but still does not match the controller's exact `MEDIAHUB_DISPATCH_HMAC_KEY`. Earlier conversation used visually similar Cyrillic characters as well. Verify the exact configured name in GitHub Settings; never expose the value.
