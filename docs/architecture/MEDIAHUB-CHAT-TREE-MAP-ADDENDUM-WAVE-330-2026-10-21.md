# Wave 330 — Gemini dispatch gates and Voktors executor status

Date: 2026-10-21. Report: [Wave 330 dispatch-gates report](../checkpoints/MEDIAHUB-NEXT-GEMINI-DISPATCH-GATES-WAVE-330-2026-10-21.md). Canonical map: [MEDIAHUB-CHAT-TREE-MAP.md](MEDIAHUB-CHAT-TREE-MAP.md) on [`docs/mediahub-chat-tree-map-20261012`](https://github.com/VlDMlNSh/mediahub-os/tree/docs/mediahub-chat-tree-map-20261012).

- `main` HEAD `79196054d84b1197cea1447dd1db5ad075302834`; controller blob `9453403bba899a2400ee3fb874d32badd034c704`.
- Controller expects secret `MEDIAHUB_DISPATCH_HMAC_KEY`; `MEDIAHUB_DISPATCH_NMAC_KEY` and Cyrillic-lookalike `MEDIAHUB_DISPATCH_НМАС_KEY` do not match.
- Controller runs [39667761725](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39667761725), [39667424495](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39667424495), [39665960179](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39665960179) all completed with every job SKIPPED. No child Gemini runs/artifacts.
- `main.protected=false`; independent review, exact-current-head CI, effective secret scopes and trusted-main no-secret probe remain open gates.
- SentinelX inventory reports Voktors-Mini operational, but capability/state/ping calls disconnected/timed out. agent-browser and Claude/FCC remain NOT RUN; no server used for Gemini.
- No dispatch, model call, local execution, failover test, qualification or acceptance is claimed.


## Live recheck superseding stale refs above — 2026-10-21 20:24 UTC

- Live `main` HEAD is now `5cac2f27685c88e5e5e391fcf315d07fc16c6a6b` (commit `docs: remove misplaced Wave 329 addendum from main`), not the older SHA above. The controller blob remains `9453403bba899a2400ee3fb874d32badd034c704`.
- Current-main controller run [39669477347](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39669477347) completed SKIPPED with all four jobs skipped and no artifacts. It was associated with report comment `6325680146`, not exact body `/next`. The current-main check inventory also contains [39669722103](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39669722103) with controller jobs skipped; [Astra Verify 39669337754](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39669337754) succeeded but does not prove child model execution.
- PR #437 remains OPEN/DRAFT at `e7e99c2fe5f090df3a731b0b1a7f3fcb5335bd14`; formal review listing is empty and exact-head combined status/workflow-run wrappers returned no entries. GitHub branch metadata reports `main.protected=false`, with required checks disabled.
- The controller requires exact ASCII `MEDIAHUB_DISPATCH_HMAC_KEY`; `MEDIAHUB_DISPATCH_NMAC_KEY` and Cyrillic-lookalike `MEDIAHUB_DISPATCH_НМАС_KEY` are different identifiers. No secret values were read; effective variable/token/secret metadata remain NOT VERIFIED.
- Full SentinelX capabilities/allowlist calls repeatedly timed out or disconnected. Host identity is confirmed (`Voktors-Mini.Dlink`, `host_5f7264034bdf0b51`, macOS 14.7.4 ARM64), and ping intermittently succeeds, but bounded script execution returned `agent_disconnected / duplicate_session`. agent-browser core retrieval, browser session and Claude/FCC run remain NOT RUN.
- Detailed current report: [Wave 330 Gemini dispatch and Voktors recheck](../checkpoints/MEDIAHUB-NEXT-GEMINI-DISPATCH-AND-VOKTORS-RECHECK-WAVE-330-2026-10-21.md). Canonical map remains [MEDIAHUB-CHAT-TREE-MAP.md](MEDIAHUB-CHAT-TREE-MAP.md).
