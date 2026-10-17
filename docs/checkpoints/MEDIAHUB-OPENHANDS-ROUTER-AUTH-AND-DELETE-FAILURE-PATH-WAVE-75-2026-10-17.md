# MediaHub OS — OpenHands Router Authorization and Delete Failure Path, Wave 75

- Date: 2026-10-17
- Contour: A — Developer Fabric
- Status: **SOURCE-ONLY REVIEW / CANDIDATE NOT ADMITTED / R-06 OPEN**
- Candidate source pin: `OpenHands/software-agent-sdk@6530325e9dd0ea1b6b4f1994d7dab52764cfc3f1`
- Governing tracker: https://github.com/VlDMlNSh/mediahub-os/issues/301
- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md

## 1. Source refs and read-back identities

Pinned revision:
- [API/router mounting](https://github.com/OpenHands/software-agent-sdk/blob/6530325e9dd0ea1b6b4f1994d7dab52764cfc3f1/openhands-agent-server/openhands/agent_server/api.py) — blob `1916fd4b00e798e27f85f37db1e634bbef6a48c2`.
- [Session authorization dependency](https://github.com/OpenHands/software-agent-sdk/blob/6530325e9dd0ea1b6b4f1994d7dab52764cfc3f1/openhands-agent-server/openhands/agent_server/dependencies.py) — blob `d1d2a6aece2056adc15824aed6cdccc4c3c33ead`.
- [Conversation DELETE route](https://github.com/OpenHands/software-agent-sdk/blob/6530325e9dd0ea1b6b4f1994d7dab52764cfc3f1/openhands-agent-server/openhands/agent_server/conversation_router.py) — blob `e57ae2b1260e97ca06743dbd15487eaab1672ccd`.
- [Conversation deletion service](https://github.com/OpenHands/software-agent-sdk/blob/6530325e9dd0ea1b6b4f1994d7dab52764cfc3f1/openhands-agent-server/openhands/agent_server/conversation_service.py) — blob `70e357a44ee6e3be5444ac564e073e1178ea0ac4`.
- [safe_rmtree implementation](https://github.com/OpenHands/software-agent-sdk/blob/6530325e9dd0ea1b6b4f1994d7dab52764cfc3f1/openhands-agent-server/openhands/agent_server/utils.py) — blob `de54c3b6417d1950a5a3d6db65f175ae6a1b2786`.
- [Trash helper](https://github.com/OpenHands/software-agent-sdk/blob/6530325e9dd0ea1b6b4f1994d7dab52764cfc3f1/openhands-agent-server/openhands/agent_server/storage/trash.py) — blob `35f2ee2206eada8f5e93852df9265ebf39010009`.

Upstream drift:
- Source comparison from the candidate pin to upstream `main`: 48 commits ahead, 0 behind.
- Relevant upstream-main blobs observed during this pass: `api.py` `f7b4f5e5857fe3b32bcfb3c0123f20530d6450be`; `dependencies.py` `e8092086c3d6b8ac12c21e883dfc9c4faf3c2a88`; `conversation_service.py` `e7df77d9a14958d2861f3c13a09883f12a2c4094`; `utils.py` `de54c3b6417d1950a5a3d6db65f175ae6a1b2786`; `storage/trash.py` `35f2ee2206eada8f5e93852df9265ebf39010009`.
- API, dependency and deletion-service files have changed since the candidate pin. Findings below are therefore version-scoped and do not qualify any artifact or deployment.

## 2. REST router mounting and authorization

The pinned `api.py` constructs an `APIRouter(prefix="/api", dependencies=[Depends(require_initialized), Depends(check_session_api_key)])` and includes the conversation catalog and conversation router within it. This resolves the previous source-only uncertainty about whether those conversation REST routes inherit the common API dependencies.

However, `check_session_api_key` raises 401 only when `config.session_api_keys` is non-empty and the supplied header is not in that list. With an empty configured key list, this dependency does not reject the request. The API code also documents `require_initialized` as a no-op for non-deferred deployments. Therefore the source establishes a conditional fail-open configuration path; it does not establish that a particular deployed target is actually configured that way.

The sockets router is mounted with the initialization dependency at the app boundary and has its own authentication path. It must be verified against the exact admitted build and target configuration; the REST router result must not be generalized to WebSocket authorization.

**Admission requirement:** require a fail-closed startup invariant for all protected API and socket routes, with tests/negative fixtures proving that absent or empty session-key configuration cannot expose protected endpoints. Separately require principal/capability/conversation binding; a shared session key is not equivalent to tenant or per-conversation authorization.

## 3. Deletion failure semantics

The pinned DELETE route returns success when `ConversationService.delete_conversation` returns true. In the service, the event service is closed and in-memory event/catalog/credential-binding records are removed, then `safe_rmtree(event_service.conversation_dir, ...)` is called. The boolean return value from `safe_rmtree` is not checked before the service logs successful deletion and returns true.

The pinned `safe_rmtree` explicitly returns false when recursive removal fails and logs that temporary files may remain. Thus a filesystem deletion failure can coexist with a successful logical-delete result. This is a source-confirmed semantic gap, not proof that a deletion failure occurred in any live deployment.

The repository also contains a `Trash` helper that atomically renames discarded storage and retries failed entries on a later start. The reviewed conversation deletion path calls `safe_rmtree` directly, not `Trash.discard`; the helper's existence therefore does not close this path's failure-reporting gap.

**Admission requirement:** deletion must be a state machine with separate logical-delete and physical-erasure outcomes; stop new reads/subscriptions; account for active readers and client copies; record failure, retry and escalate failed erasure; verify primary-store absence; define backup/export/collector retention separately. Do not report “physically erased” from a successful HTTP DELETE alone.

## 4. Crosswalk to MediaHub gates

- MH-12/A0: route authentication is not proof of A0-issued capability authorization or per-task scope.
- R-06: data-access, replay, retention and deletion evidence remains incomplete.
- Target manifest: exact configuration, route exposure, runtime topology and data stores remain owner-accepted gates.
- Provenance: source pin does not establish the built artifact digest or source-to-artifact binding.
- Qualification: source review only; no runtime acceptance.

## 5. Disposition and next step

OpenHands remains **CANDIDATE / NOT SELECTED / NOT ADMITTED / RUNTIME-UNVERIFIED**. Next source-only step: inspect the pinned and current-head WebSocket auth/replay paths and map them to the target-manifest and R-06 control matrix; then identify exact negative-test cases for a separately authorized qualification plan.

No installation, tests, qualification, provider/model calls, credential use, workflow dispatch, runtime/host inspection, infrastructure changes, merge, rebase, cherry-pick or deployment occurred.
