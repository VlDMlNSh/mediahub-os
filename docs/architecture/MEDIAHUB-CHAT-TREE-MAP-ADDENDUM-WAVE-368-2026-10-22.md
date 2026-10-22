# Wave 368 — SentinelX post-restart runtime reconciliation (2026-10-22)

- Report: [Wave 368 post-restart runtime reconciliation](../checkpoints/MEDIAHUB-NEXT-SENTINELX-POST-RESTART-RUNTIME-RECONCILIATION-WAVE-368-2026-10-22.md).
- Host `host_5f7264034bdf0b51` is connected; ping succeeds, but runtime reports `0.22.0`.
- Installed package metadata in `/Users/voktor/sentinelx/.venv` reports core `0.23.30`, protocol `1.13.2`; config SHA-256 remains `898725a1939383514101db2a0c68325182a8342d5393362068bc12a47618d50d`.
- On-disk config includes `/Users/voktor/dev/mediahub-pr437-sync`, but effective runtime policy still exposes only `/Users/voktor/sentinelx/workspace` and `/Users/voktor/sentinelx/config.yaml`. Runtime reload and service state are NOT VERIFIED; service status includes sudo-required and duplicate-session errors.
- Gemini 1–3 NOT RUN; prior run `39773148250` was a probe only. PR #441 OPEN/non-mergeable; PR #454 OPEN/DRAFT at `4f7ca451304eb36d6bba85556a6d07ca7af79729`, current exact-head CI/review NOT VERIFIED.
- Contour A NOT QUALIFIED / NOT ACCEPTED. This evidence is on the unmerged working branch; the canonical map remains on `docs/mediahub-chat-tree-map-20261012`.
- [Canonical map](https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md).
