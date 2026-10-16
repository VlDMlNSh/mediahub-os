# MediaHub OS — Chat Tree Map Addendum, Wave 27

- Date: 2026-10-17
- Status: READ-ONLY SECURITY SOURCE REVIEW / CANDIDATE ONLY
- Canonical map: [MEDIAHUB-CHAT-TREE-MAP.md](MEDIAHUB-CHAT-TREE-MAP.md)
- Direct canonical map URL: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md

## §37 — Workspace cookie, tenant boundary and tool controls

Primary report: [Wave 27 OpenHands Workspace Cookie and Tool Control Crosswalk](../checkpoints/MEDIAHUB-OPENHANDS-WORKSPACE-COOKIE-AND-TOOL-CONTROL-CROSSWALK-WAVE-27-2026-10-17.md), blob SHA `c5380aa274a8f156e668eafd0d28e4e1ed059e03`.

- Source pin: `OpenHands/software-agent-sdk@6530325e9dd0ea1b6b4f1994d7dab52764cfc3f1`.
- Cookie finding: workspace cookie value is the downstream session API key; nominal Max-Age is 10 years; HttpOnly/SameSite=None; Secure and Partitioned depend on secure-context detection, which reads forwarding headers.
- Workspace route finding: session-key membership and resolved path containment are visible; an explicit caller-to-tenant/conversation ownership binding is absent from the reviewed router functions. Deployment-level enforcement remains unknown.
- Tool finding: default preset includes terminal, file editor and task tracker; browser is enabled by default unless disabled; sub-agent delegation is configurable. Optional analyzer/hooks do not by themselves prove mandatory complete mediation.
- Traceability controls CAF-75…CAF-77; source registry SRC-093; evidence ledger EVD-047.
- Runtime remains BLOCKED: A0 issuer/ingress/lifecycle, MH-12, R-06, accepted target manifest and independent qualification remain open.
- OpenHands remains candidate only. No implementation, installation, test, qualification or deployment.

Related: [Wave 26 Agent Server security boundary](../checkpoints/MEDIAHUB-OPENHANDS-AGENT-SERVER-SECURITY-BOUNDARY-CROSSWALK-WAVE-26-2026-10-17.md), [Wave 25 contract crosswalk](../checkpoints/MEDIAHUB-OPENHANDS-TASK-REGISTRY-EVIDENCE-CONTRACT-CROSSWALK-WAVE-25-2026-10-17.md).

The canonical map remains authoritative; this addendum provides navigation only.
