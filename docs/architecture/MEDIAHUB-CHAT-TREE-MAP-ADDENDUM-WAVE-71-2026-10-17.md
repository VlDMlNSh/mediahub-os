# MediaHub OS — Chat Tree Map Addendum, Wave 71

- Date: 2026-10-17
- Working documentation branch: `docs/contour-a-a0-r06-evidence-reconciliation-wave68-20261017`
- Status: **SOURCE-ONLY REVIEW / CANDIDATE NOT ADMITTED / R-06 OPEN**
- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
- Governing tracker: https://github.com/VlDMlNSh/mediahub-os/issues/301

## Wave 71 — Agent Server telemetry, completion logging and secret retention

Primary report: [MEDIAHUB-AGENT-SERVER-TELEMETRY-RETENTION-REVIEW-WAVE-71-2026-10-17.md](../checkpoints/MEDIAHUB-AGENT-SERVER-TELEMETRY-RETENTION-REVIEW-WAVE-71-2026-10-17.md)

### Findings
- OpenHands Agent Server documentation describes telemetry as opt-in/disabled by default with an allowlisted event schema; completion logging is a separate local-disk surface containing full prompts, responses and raw provider payloads.
- Stored conversations/events and workspaces use local filesystem paths. The README does not establish a bounded retention period or complete deletion/backup-erasure guarantee.
- `OH_SECRET_KEY` protects specified persisted secret fields, but is not evidence of general workspace/log redaction or lifecycle deletion.
- Prior Waves 26–30 and 40 establish source pin `OpenHands/software-agent-sdk@6530325e9dd0ea1b6b4f1994d7dab52764cfc3f1`; pinned README SHA `a64ff0840230ff5ae2d7c167c824048eaf72da9f`, telemetry policy SHA `64e3b567352d4b3fef36327b5d8c5d8b30613403`, event service SHA `7323213c8a9eddb414b54996398a6bd3ca1c2ea9`. Fresh compare reports upstream `main` 48 commits ahead / 0 behind. README, policy and telemetry models are unchanged by blob SHA; event service and telemetry subscriber have changed and need a focused source delta review. Exact package/container digest and source-to-artifact binding remain unverified.
- MH-13 on `main` remains an accepted reconstruction with partial historical fidelity, not frozen; production implementation is not authorized. R-06 remains open.

### Disposition
OpenHands Agent Server remains **CANDIDATE / NOT SELECTED / NOT ADMITTED / RUNTIME-UNVERIFIED**. Proposed conservative defaults for any future authorized evaluation: completion logging disabled, telemetry exporter `none`, no user-domain data, explicit retention/deletion policy, session authentication and isolated ephemeral workspace. These are recommendations only, not runtime configuration or acceptance.

No install, tests, qualification, provider calls, credentials, dispatch, runtime inspection, infrastructure change, merge or deployment occurred.
