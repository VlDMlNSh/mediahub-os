# MediaHub OS — Chat Tree Map Addendum, Wave 72

- Date: 2026-10-17
- Working branch: `docs/contour-a-a0-r06-evidence-reconciliation-wave68-20261017`
- Status: **SOURCE-ONLY DELTA REVIEW / CANDIDATE NOT ADMITTED / R-06 OPEN**
- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
- Tracker: https://github.com/VlDMlNSh/mediahub-os/issues/301

## Wave 72 — OpenHands pinned-to-head telemetry and error-path delta

Primary report: [MEDIAHUB-OPENHANDS-PINNED-HEAD-TELEMETRY-ERROR-DELTA-WAVE-72-2026-10-17.md](../checkpoints/MEDIAHUB-OPENHANDS-PINNED-HEAD-TELEMETRY-ERROR-DELTA-WAVE-72-2026-10-17.md)

- Reconfirmed source pin `6530325e9dd0ea1b6b4f1994d7dab52764cfc3f1`; current upstream `main` is 48 commits ahead / 0 behind.
- Telemetry policy and telemetry model blobs are unchanged; subscriber, event service, config and persistence store have changed.
- Current-head event service formats a conversation-run traceback into a plain string for logging and may publish a detailed error event. This is not evidence of a leak, but it creates a distinct diagnostic-data sink requiring redaction, destination, access and retention evidence.
- Current-head config documents telemetry salt fallback to `OH_SECRET_KEY`, which can fall back to a session API key; stable pseudonyms may be linkable across restarts. Explicit deployment approval and rotation semantics remain required.
- Workspace persistence delta does not establish retention TTL or complete deletion/backup erasure.
- Candidate remains NOT SELECTED / NOT ADMITTED / RUNTIME-UNVERIFIED. Source-to-artifact binding, R-06 and accepted target runtime manifest remain open.
- No install, tests, qualification, provider calls, credentials, dispatch, runtime inspection, infrastructure changes, merge, rebase or deployment occurred.
