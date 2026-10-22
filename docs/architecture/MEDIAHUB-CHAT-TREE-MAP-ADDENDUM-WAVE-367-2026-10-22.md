# Wave 367 — controller admission and SentinelX restart blocker (2026-10-22)

- Evidence report: [Wave 367 controller and SentinelX recheck](../checkpoints/MEDIAHUB-NEXT-CONTROLLER-AND-SENTINELX-RESTART-BLOCKER-WAVE-367-2026-10-22.md).
- Live `main` observed as `cae0134dadf67eaa02828c43bc81cd8c71284f75`; controller blob SHA `3becd61702b3cad5a40f7d2a4de0b7fd6aee4b4f`.
- PR #454 remains OPEN/DRAFT at `2220c06616ab67b20b8ce190326717ab23f88573`; combined status result empty, so exact-head CI is NOT VERIFIED. PR #441 reports `mergeable=false`.
- Historical controller run `39773148250` was a successful non-launching probe; admission and dispatch jobs were skipped and no Gemini child runs/artifacts were created. Current batch-variable value and effective token scope remain NOT VERIFIED. No direct workflow-dispatch action was available in the connected GitHub tool set; no bypass attempted.
- SentinelX host `host_5f7264034bdf0b51` is connected, but runtime reports `0.22.0` after package install of core `0.23.30` and protocol `1.13.2`. Restart is BLOCKED by a required sudo password in the noninteractive path; effective path allowlist remains NOT VERIFIED.
- Gemini 1–3 NOT RUN; local Claude/browser NOT RUN; Contour A NOT QUALIFIED / NOT ACCEPTED.
- Canonical map branch: [MEDIAHUB-CHAT-TREE-MAP.md](https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md).
- This addendum is on an unmerged working branch and is not canonical until reviewed and merged.
