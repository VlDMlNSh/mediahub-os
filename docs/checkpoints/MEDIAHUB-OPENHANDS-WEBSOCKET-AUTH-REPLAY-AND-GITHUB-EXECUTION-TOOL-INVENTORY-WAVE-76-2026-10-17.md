# MediaHub OS — WebSocket Authorization and Replay Review, Wave 76

- Date: 2026-10-17
- Contour: A — Developer Fabric
- Status: **SOURCE-ONLY REVIEW / CANDIDATE NOT ADMITTED / R-06 OPEN**
- Candidate source pin: `OpenHands/software-agent-sdk@6530325e9dd0ea1b6b4f1994d7dab52764cfc3f1`
- Current upstream comparison ref: `main`
- Governing tracker: https://github.com/VlDMlNSh/mediahub-os/issues/301
- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md

## 1. Repository and PR state observed before this pass

- PR #333 remains **open, Draft, unmerged**: https://github.com/VlDMlNSh/mediahub-os/pull/333
- Base ref `docs/mediahub-chat-tree-map-20261012`, base SHA `a0c432273914fa5c4bd9e756736f9c9b72b41a77`.
- Working ref `docs/contour-a-a0-r06-evidence-reconciliation-wave68-20261017`, HEAD before this pass `9129f9bc708200952e8a759c47fc26cb12916041`.
- Compare: `ahead`, 29 commits ahead, 0 behind; 16 changed files at the time of inspection.
- Canonical map Contents API returned an empty content field but a non-empty blob SHA `0141454f29b3da6c84488f9464be30812e0b13a3`. This is an API representation limitation, not evidence that the file is empty. Bootstrap and prior addenda/checkpoint remain available and corroborate the map's role.

## 2. Source refs and read-back identities

Pinned revision:
- [WebSocket auth and legacy events socket](https://github.com/OpenHands/software-agent-sdk/blob/6530325e9dd0ea1b6b4f1994d7dab52764cfc3f1/openhands-agent-server/openhands/agent_server/sockets.py) — blob `33d7a4b1666e9cdcf004b157470e9be16cdfe693`.
- [Resumable session socket](https://github.com/OpenHands/software-agent-sdk/blob/6530325e9dd0ea1b6b4f1994d7dab52764cfc3f1/openhands-agent-server/openhands/agent_server/session_socket.py) — blob `4e02c35e6e4fd67ca5adea31e3f9346f59a29f38`.
- [REST/session API router mounting](https://github.com/OpenHands/software-agent-sdk/blob/6530325e9dd0ea1b6b4f1994d7dab52764cfc3f1/openhands-agent-server/openhands/agent_server/api.py) — blob `1916fd4b00e798e27f85f37db1e634bbef6a48c2`.
- [Session API-key dependency](https://github.com/OpenHands/software-agent-sdk/blob/6530325e9dd0ea1b6b4f1994d7dab52764cfc3f1/openhands-agent-server/openhands/agent_server/dependencies.py) — blob `d1d2a6aece2056adc15824aed6cdccc4c3c33ead`.

Current upstream `main`:
- `sockets.py` — blob `33d7a4b1666e9cdcf004b157470e9be16cdfe693`.
- `session_socket.py` — blob `4e02c35e6e4fd67ca5adea31e3f9346f59a29f38`.
- `api.py` — blob `f7b4f5e5857fe3b32bcfb3c0123f20530d6450be`.
- `dependencies.py` — blob `e8092086c3d6b8ac12c21e883dfc9c4faf3c2a88`.

The socket and session-socket blobs are identical at the reviewed pin and current `main`; the API and dependency blobs differ. This is a source comparison only, not a deployment or runtime comparison.

## 3. Findings

### F76-1 — Authentication has a fail-open empty-key branch

`_accept_authenticated_websocket` accepts the socket unconditionally when `config.session_api_keys` is empty. With keys configured, first-message authentication is supported, but the deprecated query parameter and `X-Session-API-Key` header are still accepted. The shared REST dependency has the same conditional empty-list issue (Wave 75).

This establishes a source-level fail-open configuration path. It does **not** establish that any live instance is configured this way or exposed.

### F76-2 — Conversation-specific authorization is not established by the shared session key

After the shared key check, both the events socket and session socket resolve an event service by `conversation_id` and proceed to subscription/replay if the conversation exists. The reviewed paths do not establish an independent principal + issuer + capability + conversation binding. A shared session key is not evidence of per-conversation authorization.

This is an admission gap to close, not proof that a live cross-conversation read has occurred.

### F76-3 — Historical replay is potentially broad within the addressed conversation

The legacy events socket supports `resend_mode=all` (and deprecated `resend_all`) to replay the full event history, or `resend_mode=since` using timestamps. The resumable session socket supports `after_seq=-1` for full history and cursors for subsequent replay. These semantics are documented in source and feature maps. Authorization is performed before history access, but the reviewed auth is a shared session key rather than a conversation-scoped capability.

A validly authenticated caller who can name a conversation ID may be able to request a broad historical replay unless the surrounding deployment supplies stronger isolation. The exact effective access depends on configuration and the target deployment, which were not inspected.

### F76-4 — Query-string credential transport remains enabled

The `session_api_key` query parameter is still accepted for compatibility. Source comments explicitly warn that query tokens can enter reverse-proxy/load-balancer access logs. First-message authentication is preferred but does not disable the legacy query/header routes.

### F76-5 — Resource controls are present but do not substitute for authorization

The session socket includes ordered durable replay, cursor resumption, byte-bounded writes and slow-consumer closure. Subscriber limits and frame/queue bounds reduce resource-exhaustion risk; they do not provide issuer, principal or conversation authorization.

## 4. Required gates before admission

1. Fail closed at startup if authentication keys/authority configuration are absent, malformed, or ambiguous; no unauthenticated fallback.
2. Bind every socket to authenticated principal, issuer, capability, task/lease, and exact conversation ID; reject cross-conversation replay.
3. Remove or explicitly disable query-string credentials; verify header and first-frame handling against the approved client matrix.
4. Apply an explicit replay policy: deny by default, bound history range/volume, enforce retention and authorization for every requested cursor/range, and audit access without recording secrets or raw completion content.
5. Add negative qualification cases: empty auth config; missing/wrong/revoked key; query-string key; wrong issuer/capability; conversation ID substitution; full replay and cursor replay across two principals; deletion during active subscription; oversized replay and slow reader.
6. Verify source-to-artifact binding and target manifest before any runtime qualification. Keep tests/qualification as a separate explicit permission gate.

## 5. Tooling discovery — GitHub execution from this ChatGPT session

The connected GitHub toolset currently exposes:
- repository/file/branch/commit/PR operations, including create/update files and branches;
- code/issue/PR search, compare refs, commit status and PR metadata;
- GitHub Actions run/job log and artifact inspection;
- rerun of a failed workflow or individual job, subject to GitHub Actions write permission.

No dedicated GitHub `workflow_dispatch`/start-workflow tool was found in the currently exposed GitHub action catalog. Therefore this session can inspect and document GitHub-hosted execution, and may be able to retry an existing failed run, but cannot claim a general fresh workflow-dispatch path is available through the GitHub connector. Browser automation capabilities also exist as separate tools/skills, but the available browser profiles have no recorded signed-in sites; authenticated browser execution is not yet verified.

Issue #301 remains the governing sequence. It explicitly says workflow dispatch, credential use, provider calls, tests/qualification, deployment and merge each need their own authorization. This review did not dispatch workflows or invoke any provider.

## 6. Disposition

- Candidate: **CANDIDATE / NOT SELECTED / NOT ADMITTED / RUNTIME-UNVERIFIED**.
- R-06 remains open.
- No tests, installations, model/provider calls, credential access, workflow dispatch, runtime/host inspection, infrastructure changes, merge, rebase, cherry-pick or deployment were performed.
- Next bounded pass: inspect the repository's actual GitHub Actions workflows and permissions/dispatch configuration, correlate the existing successful Gemini evidence and Issue #301 queue, and identify the narrowest safe read-only workflow entrypoint. Do not dispatch it without separate explicit authorization.
