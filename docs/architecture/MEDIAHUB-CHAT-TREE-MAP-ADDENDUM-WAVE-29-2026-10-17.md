# MediaHub OS — Chat Tree Map Addendum, Wave 29

- Date: 2026-10-17
- Status: READ-ONLY SOURCE REVIEW / CANDIDATE ONLY
- Canonical map: [MEDIAHUB-CHAT-TREE-MAP.md](MEDIAHUB-CHAT-TREE-MAP.md)
- Direct canonical map URL: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md

## §39 — Canvas app-backend bridge threat crosswalk

Primary report: [OpenHands App-Backend Bridge Threat Crosswalk, Wave 29](../checkpoints/MEDIAHUB-OPENHANDS-APP-BACKEND-BRIDGE-THREAT-CROSSWALK-WAVE-29-2026-10-17.md).

- Source pin: `OpenHands/software-agent-sdk@6530325e9dd0ea1b6b4f1994d7dab52764cfc3f1`.
- Covered session issue/store, token digest, 5-minute cookie, Origin/ingress checks, trusted forwarded headers, loopback backend selection, path canonicalization, redirect policy, WebSocket expiry/revocation and router auth groups.
- Controls CAF-81…CAF-83; source registry SRC-095; evidence EVD-049.
- Upstream has meaningful local bridge protections, but these do not prove tenant/task identity, sandbox isolation, egress policy or complete audit.
- OpenHands remains candidate only. Runtime admission remains BLOCKED pending A0/MH-12/R-06, accepted target manifest and independent qualification.
- No install, execution, test, qualification or deployment occurred.

Next: source-bound provider secret-flow and egress matrix, including provider connections, MCP configuration/probes and tool invocation.

The canonical map remains authoritative; this addendum provides navigation only.
