# MediaHub OS — Chat Tree Map Addendum, Wave 76

- Date: 2026-10-17
- Working documentation branch: `docs/contour-a-a0-r06-evidence-reconciliation-wave68-20261017`
- Status: **SOURCE-ONLY REVIEW / CANDIDATE NOT ADMITTED / R-06 OPEN**
- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
- Governing tracker: https://github.com/VlDMlNSh/mediahub-os/issues/301

## Wave 76 — WebSocket authorization, replay and GitHub execution-tool inventory

Primary report: [WebSocket Authorization and Replay Review — Wave 76](../checkpoints/MEDIAHUB-OPENHANDS-WEBSOCKET-AUTH-REPLAY-AND-GITHUB-EXECUTION-TOOL-INVENTORY-WAVE-76-2026-10-17.md)

- At the pinned OpenHands source revision, WebSocket auth accepts connections unconditionally if `session_api_keys` is empty. With keys configured, first-frame auth is supported, but deprecated query-string and header credentials remain accepted.
- Both event sockets resolve a conversation event service after shared-key auth and support historical replay. The reviewed path does not establish principal/issuer/capability binding to the exact conversation. This is an admission gap, not evidence of a live exposure.
- Legacy event socket supports full replay (`resend_mode=all` / deprecated `resend_all`) and timestamp replay; session socket supports sequence replay including `after_seq=-1` for full history.
- Reviewed `sockets.py` and `session_socket.py` blobs match at the candidate pin and upstream `main`; API and dependency blobs differ.
- GitHub connector exposes repo/file/branch/commit/PR management, search and Actions log/artifact inspection, plus reruns for existing failed workflows/jobs. No dedicated fresh `workflow_dispatch` action was found in the exposed catalog.
- Browser automation is present, but listed browser profiles have no recorded signed-in sites. Authenticated browser execution is not verified.
- No workflow was dispatched; no credentials or provider were used; no tests, installation, runtime inspection, qualification, merge or deployment occurred.
- Next: inspect repository workflows, dispatch permissions, existing Gemini evidence and the smallest safe read-only worker entrypoint. Dispatch remains a separate permission gate.

## Navigation

Use the canonical map above for domain navigation. The Contents API returned an empty `content` field for the map despite returning blob SHA `0141454f29b3da6c84488f9464be30812e0b13a3`; do not interpret that response as an empty file.
