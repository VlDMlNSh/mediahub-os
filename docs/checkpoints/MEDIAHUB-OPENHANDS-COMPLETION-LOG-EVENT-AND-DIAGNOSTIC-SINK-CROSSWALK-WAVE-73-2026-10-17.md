# MediaHub OS — Completion-Log Event and Diagnostic Sink Crosswalk, Wave 73

- Date: 2026-10-17
- Contour: A — Developer Fabric
- Status: **SOURCE-ONLY DATA-FLOW REVIEW / CANDIDATE NOT ADMITTED / R-06 OPEN**
- Source pin: `OpenHands/software-agent-sdk@6530325e9dd0ea1b6b4f1994d7dab52764cfc3f1`
- Tracker: [Issue #301](https://github.com/VlDMlNSh/mediahub-os/issues/301)
- Prior pass: [Wave 72 pinned-to-head delta](MEDIAHUB-OPENHANDS-PINNED-HEAD-TELEMETRY-ERROR-DELTA-WAVE-72-2026-10-17.md)
- Canonical project map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md

## 1. Scope and immutable source evidence

Inspected the pinned Agent Server event flow, LLM completion-log event model, remote conversation callback and SDK logger configuration. Relevant upstream source links:

- [Pinned event service](https://github.com/OpenHands/software-agent-sdk/blob/6530325e9dd0ea1b6b4f1994d7dab52764cfc3f1/openhands-agent-server/openhands/agent_server/event_service.py) — blob `7323213c8a9eddb414b54996398a6bd3ca1c2ea9`
- [Pinned completion-log event model](https://github.com/OpenHands/software-agent-sdk/blob/6530325e9dd0ea1b6b4f1994d7dab52764cfc3f1/openhands-sdk/openhands/sdk/event/llm_completion_log.py) — blob `47207bcf0f5236904fd92e5958d75137a9192180`
- [Pinned remote conversation handler](https://github.com/OpenHands/software-agent-sdk/blob/6530325e9dd0ea1b6b4f1994d7dab52764cfc3f1/openhands-sdk/openhands/sdk/conversation/impl/remote_conversation.py) — blob `df0455e92fc8743e8de6928dceaa952ed5e3c843`
- [Pinned SDK logger](https://github.com/OpenHands/software-agent-sdk/blob/6530325e9dd0ea1b6b4f1994d7dab52764cfc3f1/openhands-sdk/openhands/sdk/logger/logger.py) — blob `b728923d85817abd79954018c28bf47b01072556`
- [Pinned conversation error model](https://github.com/OpenHands/software-agent-sdk/blob/6530325e9dd0ea1b6b4f1994d7dab52764cfc3f1/openhands-sdk/openhands/sdk/event/conversation_error.py) — blob `dd2a093dcba9b9bc4c8e3e5952787ec0c78ef48d`
- [Agent Server README](https://github.com/OpenHands/software-agent-sdk/blob/6530325e9dd0ea1b6b4f1994d7dab52764cfc3f1/openhands-agent-server/openhands/agent_server/README.md) — blob `a64ff0840230ff5ae2d7c167c824048eaf72da9f`

## 2. Primary finding: completion logs are not solely a local-disk flow

The README describes LLM completion logging as full prompts, responses and raw provider payloads stored on local disk. The pinned implementation shows an additional transport/persistence path when `llm.log_completions` is enabled:

1. Agent Server registers a completion callback for each LLM with `log_completions=True`.
2. The callback constructs `LLMCompletionLogEvent(filename, log_data, model_name, usage_id)`. `log_data` is the JSON-encoded log content.
3. The event is sent through `_emit_event_from_thread`, which invokes the conversation's normal `_on_event` path. The code comment explicitly says this makes the event persisted and sent to WebSocket subscribers.
4. The remote SDK callback receives the event and writes `event.log_data` to the configured client-side completion-log folder.

This means the content can traverse the Agent Server event/WebSocket channel and be persisted in the conversation event log before or in addition to the remote client's local completion-log file. The README's statement that completion logging is not forwarded to product telemetry does **not** mean that the content never traverses the network or enters server-side conversation persistence.

**Security consequence:** enabling completion logging can expand sensitive-data exposure to event persistence, WebSocket authorization, API transport, event-log backups and the remote client's filesystem. Treat it as a high-sensitivity content-export capability, not merely a local debug flag.

## 3. Diagnostic/error path

- The pinned `ConversationErrorEvent` exposes `code` and free-form `detail`; its model performs classification but does not itself establish that detail text has been redacted.
- The current-head event-service path identified in Wave 72 formats an exception traceback and logs it as plain text; it also constructs a detailed conversation error event for UI delivery. This current-head observation is not attributed to the older source pin.
- The pinned SDK logger supports a rotating `app.log` file handler (default backup count shown in source) and a Rich console handler. These are separate sinks from product telemetry and conversation events.
- No reviewed source establishes a universal redaction layer for all exception messages, completion-log payloads, WebSocket events, application logs and backups.

The exact runtime logging handler selection and deployment sinks are not established by this source review. Do not infer that a configured file handler is necessarily enabled in the proposed deployment.

## 4. Control crosswalk

| Data path | Source-level evidence | Admission requirement |
|---|---|---|
| LLM completion payload | Raw `log_data` placed in `LLMCompletionLogEvent` | Hard-disable `log_completions` for normal operation; prove effective config in exact artifact |
| Conversation event persistence | Event is routed through conversation `_on_event` path | Treat event store as sensitive content storage; bounded TTL, access isolation, deletion and backup policy |
| WebSocket subscribers | Same event flow is sent to subscribers | AuthZ test, subscriber isolation, no cross-conversation delivery and explicit egress classification |
| Client completion-log file | Remote SDK writes raw `event.log_data` to configured folder | Ephemeral isolated directory, permissions, expiry, cleanup and artifact export policy |
| Conversation error detail | Free-form `detail`; classification is not redaction | Normalize to approved error code/category for product events; raw details confined to controlled diagnostics |
| Application logs | SDK logger supports console and rotating file handlers | Explicit sink inventory, safe formatter/redaction, access policy and bounded retention |
| Backups / derived artifacts | Not proven by inspected code | Independent inventory, TTL and deletion evidence for all copies |

## 5. Disposition and next step

OpenHands Agent Server remains **CANDIDATE / NOT SELECTED / NOT ADMITTED / RUNTIME-UNVERIFIED**. Recommended baseline for any future separately authorized evaluation: completion logging disabled, telemetry exporter absent unless explicitly approved, no User Domain data, and no raw exception text in broadly accessible product events. These are design recommendations, not claims of runtime configuration.

Next source-only pass: trace the event-store serialization and deletion APIs plus WebSocket authorization boundaries to establish whether completion-log event bodies are retained, who can retrieve them, and what deletion semantics are implemented. Keep source pin unchanged. Package/image digest, source-to-artifact binding, R-06 disposition and target runtime manifest remain open.

No installation, tests, qualification, provider/model calls, credential use, workflow dispatch, runtime/host inspection, infrastructure changes, merge, rebase, deployment or branch integration occurred.
