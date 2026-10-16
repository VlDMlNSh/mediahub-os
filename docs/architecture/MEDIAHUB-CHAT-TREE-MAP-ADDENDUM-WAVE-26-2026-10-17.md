# MediaHub OS — Chat Tree Map Addendum, Wave 26

- Date: 2026-10-17
- Status: READ-ONLY SECURITY SOURCE REVIEW / CANDIDATE ONLY
- Canonical map: [MEDIAHUB-CHAT-TREE-MAP.md](MEDIAHUB-CHAT-TREE-MAP.md)
- Direct canonical map URL: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md

## §36 — OpenHands Agent Server security boundary

Primary report: [Wave 26 Agent Server Security Boundary Crosswalk](../checkpoints/MEDIAHUB-OPENHANDS-AGENT-SERVER-SECURITY-BOUNDARY-CROSSWALK-WAVE-26-2026-10-17.md), blob SHA `b940a2c440a610baf6d1bd7390214baccbb8541c`.

- Source pin: `OpenHands/software-agent-sdk@6530325e9dd0ea1b6b4f1994d7dab52764cfc3f1`.
- Source-bound finding: entrypoint selects loopback when host is unspecified and session auth is absent; configured session auth changes the implicit bind to wildcard. Explicit wildcard without auth warns and proceeds.
- Separate security surfaces: header-authenticated API routes, X-Init-API-Key privileged warm-pool initialization, workspace-session cookie/static-file routes, workspace CORS branch, configurable environment/path/webhook fields, Docker mount and forwarded-environment controls.
- Traceability controls CAF-72…CAF-74; source registry SRC-092; evidence ledger EVD-046.
- Runtime remains BLOCKED: A0 issuer/ingress/lifecycle, MH-12, R-06, accepted target manifest and independent qualification remain open.
- OpenHands remains candidate only. No selection, installation, implementation, testing, qualification, deployment or branch integration.

Related: [Wave 25 contract crosswalk](../checkpoints/MEDIAHUB-OPENHANDS-TASK-REGISTRY-EVIDENCE-CONTRACT-CROSSWALK-WAVE-25-2026-10-17.md), [Wave 24 source pin](../checkpoints/MEDIAHUB-JARVIS-SOURCE-PIN-AND-CAPABILITY-CROSSWALK-WAVE-24-2026-10-17.md), [Wave 23 reuse-first gate](../checkpoints/MEDIAHUB-REUSE-FIRST-UPSTREAM-DISCOVERY-GATE-WAVE-23-2026-10-17.md).

The canonical map remains authoritative; this addendum provides navigation only.
