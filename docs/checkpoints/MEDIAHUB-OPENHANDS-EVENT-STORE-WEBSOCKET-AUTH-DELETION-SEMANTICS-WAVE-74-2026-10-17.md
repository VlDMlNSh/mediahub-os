# MediaHub OS — Event Store, WebSocket Authorization and Deletion Semantics, Wave 74

- Date: 2026-10-17
- Contour: A — Developer Fabric
- Status: **SOURCE-ONLY REVIEW / CANDIDATE NOT ADMITTED / R-06 OPEN**
- OpenHands pin: `OpenHands/software-agent-sdk@6530325e9dd0ea1b6b4f1994d7dab52764cfc3f1`
- Issue: https://github.com/VlDMlNSh/mediahub-os/issues/301
- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md

## 1. Source evidence reviewed

- [EventLog](https://github.com/OpenHands/software-agent-sdk/blob/6530325e9dd0ea1b6b4f1994d7dab52764cfc3f1/openhands-sdk/openhands/sdk/conversation/event_store.py) — blob `ddfd38f13662ddb7c28e4d5142862e91d05716ca`
- [Event router](https://github.com/OpenHands/software-agent-sdk/blob/6530325e9dd0ea1b6b4f1994d7dab52764cfc3f1/openhands-agent-server/openhands/agent_server/event_router.py) — blob `6c17e33dbfe8ccc7a7691e7b1f18cd0fbb1885a6`
- [WebSocket endpoints](https://github.com/OpenHands/software-agent-sdk/blob/6530325e9dd0ea1b6b4f1994d7dab52764cfc3f1/openhands-agent-server/openhands/agent_server/sockets.py) — blob `33d7a4b1666e9cdcf004b157470e9be16cdfe693`
- [Authentication dependencies](https://github.com/OpenHands/software-agent-sdk/blob/6530325e9dd0ea1b6b4f1994d7dab52764cfc3f1/openhands-agent-server/openhands/agent_server/dependencies.py) — blob `d1d2a6aece2056adc15824aed6cdccc4c3c33ead`
- [Conversation deletion/service](https://github.com/OpenHands/software-agent-sdk/blob/6530325e9dd0ea1b6b4f1994d7dab52764cfc3f1/openhands-agent-server/openhands/agent_server/conversation_service.py) — blob `70e357a44ee6e3be5444ac564e073e1178ea0ac4`
- [Conversation DELETE route](https://github.com/OpenHands/software-agent-sdk/blob/6530325e9dd0ea1b6b4f1994d7dab52764cfc3f1/openhands-agent-server/openhands/agent_server/conversation_router.py) — blob `e57ae2b1260e97ca06743dbd15487eaab1672ccd`
- [Upstream F06 conversation-events feature map](https://github.com/OpenHands/software-agent-sdk/blob/6530325e9dd0ea1b6b4f1994d7dab52764cfc3f1/.agents/skills/verify-agent-server/references/feature-map/F06-conversation-events.md) — blob `999beb22416a4c7b3d1c89890781a3175364a204`

## 2. Persistence semantics

The pinned `EventLog` describes itself as persistent, append-only and process/thread-safe, writing events to the configured FileStore and reconstructing its index from disk. The inspected class exposes append/read/index operations; no event-level retention/TTL or event-by-event deletion API was found in the inspected source. This is a bounded source observation, not proof that no other layer can remove events.

The F06 source map explicitly states that conversation events survive server restart and that WebSocket replay can resend the persisted log. Thus completion-log event bodies, once appended, should be treated as durable conversation data until the containing conversation storage is actually removed.

## 3. WebSocket boundary

The pinned socket implementation documents first-frame authentication as the recommended method; it also accepts a deprecated query parameter and an API-key header. It authenticates before subscribing, resolves the requested conversation, and supports replay modes `all` and `since`. The F06 feature map describes the replayed records as raw JSON.

Security implications:
- A valid session key is a coarse server/session boundary; the reviewed code does not demonstrate per-user/per-tenant ownership authorization. For MediaHub, require a separate authorization decision binding principal + capability + conversation ID before subscription and before history retrieval.
- Query-string API-key compatibility can place credentials in URL-bearing logs; disable it in the target configuration if possible and use first-frame authentication or an appropriate protected header.
- The event API routes themselves rely on dependency wiring outside the route file; this pass does not establish the effective auth dependency for every REST route in the exact deployment. Verify router mounting and default-key behavior against the exact artifact before admission.
- Replay is a bulk historical-data export capability and must be included in authorization, audit and rate-limit policy.

The shared `check_session_api_key` dependency only rejects a key mismatch when `config.session_api_keys` is non-empty. The target must prove that startup/configuration cannot leave protected APIs exposed in an unintended no-key state; the source alone does not establish the deployment's effective posture.

## 4. Deletion semantics and limits

The conversation DELETE route calls `ConversationService.delete_conversation`. The service closes the event service, removes in-memory catalog/credential-binding records and calls `safe_rmtree` on the conversation directory. The source comment explicitly allows directory removal to fail without preventing the conversation from being marked deleted. It separately removes a shared worktree only when no remaining conversation refers to it.

Therefore:
- API-level successful deletion is **not by itself proof of physical erasure** of event files.
- A failed directory removal can leave persisted data behind; the inspected source does not show a durable tombstone/retry queue or independent erasure verification in this path.
- Event storage does not show an event-level TTL. Conversation/workspace retention policies elsewhere must not be mistaken for a universal event-log TTL.
- No evidence in this pass establishes erasure from filesystem snapshots, backups, external log collectors, WebSocket clients, exported artifacts or provider-side logs.
- Conversation deletion closes following sockets according to F06, but disconnecting subscribers is not the same as deleting copies already received by clients.

## 5. Required MediaHub admission gates

1. Bind every read/replay/delete action to explicit principal, issuer, capability, conversation scope and audit decision; do not treat possession of a shared session key as tenant authorization.
2. Verify exact API router mounting and auth dependencies; fail closed if required session keys/issuer configuration is missing.
3. Disable query-string credential transport in the production target; prefer first-frame auth or protected headers.
4. Keep completion logging disabled in normal operation.
5. Define deletion as a multi-stage state machine: deny new reads first, close subscribers, delete primary event/workspace stores, verify absence, retry/report failures, then account for backups and downstream copies under their own retention rules.
6. Define and evidence TTL/retention separately for event log, workspace, server logs, backup snapshots, client-side logs and telemetry.
7. Add independently reviewed negative tests for cross-conversation replay, unauthorized REST event reads, no-key startup, deletion failure, restart recovery after deletion and residual-file verification. Running tests remains separately permissioned.

## 6. Disposition

OpenHands Agent Server remains **CANDIDATE / NOT SELECTED / NOT ADMITTED / RUNTIME-UNVERIFIED**. R-06, target runtime manifest and source-to-artifact binding remain open. This is source review only; no tests, installs, provider calls, credentials, workflow dispatch, runtime inspection, infrastructure changes, merge, rebase or deployment occurred.

Next bounded pass: trace exact router mounting/auth dependencies and the `safe_rmtree` implementation/test contract, then crosswalk the confirmed requirements to MH-12/MH-13/R-06 without executing the runtime.
