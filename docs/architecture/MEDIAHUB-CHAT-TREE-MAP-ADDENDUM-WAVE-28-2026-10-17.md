# MediaHub OS — Chat Tree Map Addendum, Wave 28

- Date: 2026-10-17
- Status: READ-ONLY SOURCE INVENTORY / CANDIDATE ONLY
- Canonical map: [MEDIAHUB-CHAT-TREE-MAP.md](MEDIAHUB-CHAT-TREE-MAP.md)
- Direct canonical map URL: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md

## §38 — Route-to-capability matrix

Primary report: [Wave 28 OpenHands Route-to-Capability Matrix](../checkpoints/MEDIAHUB-OPENHANDS-ROUTE-TO-CAPABILITY-MATRIX-WAVE-28-2026-10-17.md), blob SHA `fc60bf2fda5f1cc2d2ac20112279cd260baab4a8`.

- Source pin: `OpenHands/software-agent-sdk@6530325e9dd0ea1b6b4f1994d7dab52764cfc3f1`.
- Mapped server-details/health, init, main REST, workspace, OpenAI-compatible, WebSocket, app-backend bridge, runtime, events, tools, MCP, plugins/skills/sub-agents, provider/secrets and Docker runtime families.
- High-priority controls: public server-details routes; empty session-key permissive mode; legacy WebSocket query-key support; app-backend proxy session enforcement; outbound MCP probe/tool invocation; local runtime is not a sandbox; extension capability expansion.
- Traceability controls CAF-78…CAF-80; source registry SRC-094; evidence EVD-048.
- Runtime remains BLOCKED: A0 issuer/ingress/lifecycle, MH-12, R-06, accepted target manifest and independent qualification remain open.
- OpenHands remains candidate only; no implementation, installation, testing, qualification or deployment.

Related: [Wave 27 cookie and tool controls](../checkpoints/MEDIAHUB-OPENHANDS-WORKSPACE-COOKIE-AND-TOOL-CONTROL-CROSSWALK-WAVE-27-2026-10-17.md), [Wave 26 Agent Server security boundary](../checkpoints/MEDIAHUB-OPENHANDS-AGENT-SERVER-SECURITY-BOUNDARY-CROSSWALK-WAVE-26-2026-10-17.md).

The canonical map remains authoritative; this addendum provides navigation only.
