# Wave 329 — Gemini queue and Voktors executor status

Date: 2026-10-21. Detailed report: [Wave 329 — Gemini queue and Voktors executor status](../checkpoints/MEDIAHUB-NEXT-GEMINI-QUEUE-AND-VOKTORS-EXECUTOR-WAVE-329-2026-10-21.md). Canonical map: [MEDIAHUB-CHAT-TREE-MAP.md](MEDIAHUB-CHAT-TREE-MAP.md) on [`docs/mediahub-chat-tree-map-20261012`](https://github.com/VlDMlNSh/mediahub-os/tree/docs/mediahub-chat-tree-map-20261012).

- Main SHA `79196054d84b1197cea1447dd1db5ad075302834`; controller blob SHA `9453403bba899a2400ee3fb874d32badd034c704`.
- The controller expects `secrets.MEDIAHUB_DISPATCH_HMAC_KEY`, while the latest user text names `MEDIAHUB_DISPATCH_NMAC_KEY`. This exact identifier mismatch needs a name-only check; secret values must never be exposed. Connector cannot enumerate Actions secret metadata.
- PR #437 is OPEN/DRAFT at live head `e7e99c2fe5f090df3a731b0b1a7f3fcb5335bd14`; no exact-head checks/statuses and no formal review. No controller trigger posted. Gemini Agents 1–3 NOT RUN; no run IDs or artifacts.
- SentinelX ping/capabilities succeeded, but agent-browser CLI execution timed out and script runs failed/timed out with duplicate-session/agent response errors. Core skill/browser session not obtained. Claude/Ollama remain unverified; no paid fallback or allowlist changes.
- Cloud Gemini stays independent of physical hosts. Next: close governance/CI/secret-name evidence gates, then approved GitHub-controller dispatch; separately restore Voktors command execution.
