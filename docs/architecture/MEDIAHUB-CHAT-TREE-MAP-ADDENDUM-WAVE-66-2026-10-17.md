# MediaHub OS — Chat Tree Map Addendum, Wave 66

Date: 2026-10-17
Status: Session-to-Actions dispatch design documented; direct dispatch requires connector capability and Issue #301 gates.

Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
Dispatch bridge guide: [GitHub Session-to-Actions Dispatch Bridge, Wave 66](../operations/MEDIAHUB-GITHUB-SESSION-TO-ACTIONS-DISPATCH-BRIDGE-WAVE-66-2026-10-17.md)
Runtime evidence: [Three-Agent Runtime Evidence, Wave 65](../checkpoints/MEDIAHUB-GEMINI-THREE-AGENT-RUNTIME-EVIDENCE-WAVE-65-2026-10-17.md)
Queue acceptance issue: https://github.com/VlDMlNSh/mediahub-os/issues/301

## Findings

The existing three Gemini workflows support `workflow_dispatch` and use GitHub-hosted ephemeral runners. The current ChatGPT GitHub connector supports repository/PR operations and Actions run/job/artifact reads, but exposes no direct workflow-dispatch action. Skill catalog entries cannot extend the authenticated connector API.

Wave 66 records:
- exact existing workflow URLs, input values and credential references;
- a manual free-quota UI launch procedure;
- the future GitHub App/connector dispatch contract;
- security, quota and acceptance gates required before enabling a session-driven dispatcher;
- the currently available skill set.

No new workflow trigger or queue has been implemented. Issue/comment-triggered arbitrary task execution is intentionally excluded until issuer, ingress, lease, cancellation, recovery and audit/privacy gates are closed.

## Next ordered work

Follow Issue #301: close A0 and R-06 gates; accept runner/workspace/network manifest; validate schemas with Draft 2020-12 and positive/negative fixtures; independently review semantic references; harden current workflows; then qualify the smallest bounded read-only worker/queue slice.

Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
