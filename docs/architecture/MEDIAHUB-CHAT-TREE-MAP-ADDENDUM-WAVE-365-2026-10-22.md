# MediaHub Chat Tree Map — Wave 365 addendum (2026-10-22)

This is a working-branch addendum, not a replacement for the canonical map on `docs/mediahub-chat-tree-map-20261012`.

## Owner-confirmed hardware identity

- Alamo is hosted on `Voktors-Mini.Dlink`, identified by the owner as the Mac mini 2018.
- This corrects the earlier interpretation that Alamo was separate from the superseded hardware label central role.
- See merged [PR #450](https://github.com/VlDMlNSh/mediahub-os/pull/450), merge commit `25a2883bb8e3099df49c9bd688c028958102bc95`.
- The current working branch corrects the exact superseded hardware label in three source documents. The final branch-wide search and exact-head CI remain required before acceptance.

## Four-executor lane status

- Gemini agents 1–3: historical independent runs exist, but current Wave 365 manual tasks are NOT RUN. Controller probe [39773148250](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39773148250) succeeded only in non-launching mode; admission and dispatch jobs were skipped.
- Claude-fcc-Ollama on `Voktors-Mini.Dlink`: NOT RUN in Wave 365. Current SentinelX capabilities full-view timed out, then a read-only CLI check returned `duplicate_session`. The project repo path is outside the host's current file-operation allowlist.
- `SENTINEL_REQUEST_API_KEY` is a SentinelX API credential; it does not turn on the GitHub Actions variable `MEDIAHUB_GEMINI_BATCH_ENABLED` and does not bypass SentinelX host policy.

## Evidence record

Detailed report: [Wave 365 executor blockers and Mac mini 2018 identity sweep](../checkpoints/MEDIAHUB-NEXT-MAC-MINI-2018-IDENTITY-AND-FOUR-EXECUTOR-BLOCKERS-WAVE-365-2026-10-22.md).

Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md

Canonical checkpoint: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/checkpoints/mediahub-next-continuation-checkpoint-2026-10-12-current.md

Bootstrap: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CONTEXT-BOOTSTRAP-INSTRUCTION.md

Master roadmap: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/checkpoints/MEDIAHUB-MASTER-DEVELOPMENT-ROADMAP-1.0.md
