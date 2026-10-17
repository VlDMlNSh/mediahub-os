# MediaHub OS — OpenHands Pinned-to-HEAD Telemetry and Error-Path Delta, Wave 72

- Date: 2026-10-17
- Contour: A — Developer Fabric
- Status: **SOURCE-ONLY DELTA REVIEW / CANDIDATE NOT ADMITTED / R-06 OPEN**
- Source pin: `OpenHands/software-agent-sdk@6530325e9dd0ea1b6b4f1994d7dab52764cfc3f1`
- Tracker: [Issue #301](https://github.com/VlDMlNSh/mediahub-os/issues/301)
- Prior pass: [Wave 71 telemetry/retention review](MEDIAHUB-AGENT-SERVER-TELEMETRY-RETENTION-REVIEW-WAVE-71-2026-10-17.md)
- Canonical project map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md

## 1. Bounded pass

Compared selected upstream source files at the established immutable source pin against current `main`. GitHub compare says `main` is 48 commits ahead and 0 behind the pin. This is source inspection only: no tests, installs, provider calls or runtime activity.

| File | Pinned blob SHA | Current `main` blob SHA | Delta |
|---|---|---|---|
| `openhands-agent-server/openhands/agent_server/telemetry/policy.py` | `64e3b567352d4b3fef36327b5d8c5d8b30613403` | same | No blob change |
| `openhands-agent-server/openhands/agent_server/telemetry/models.py` | `14a163b1b597edd59a45c35e94249d66170b55fa` | same | No blob change |
| `openhands-agent-server/openhands/agent_server/telemetry/subscriber.py` | `cc45c7f8db79e6d832e3fa78694619a990f20c43` | `0da40d7930d0d7886818a4f547e155437c248600` | Changed |
| `openhands-agent-server/openhands/agent_server/event_service.py` | `7323213c8a9eddb414b54996398a6bd3ca1c2ea9` | `83721a6da19e40ae3b2eee6ffea62607aed0c646` | Changed |
| `openhands-agent-server/openhands/agent_server/config.py` | `a5830083eb110eadc6262287c5242f50e2296b66` | `ed6b9fa790caebfd672446b3a15632ef9f500d4a` | Changed |
| `openhands-agent-server/openhands/agent_server/persistence/store.py` | `fc59869567ce7dc699f9482898dd752274d9a7f7` | `1a1c7fdaa7fbc3b9524b805a805404f8e0f275e4` | Changed |

## 2. Findings from the delta

### 2.1 Telemetry subscriber

Current `main` moves usage capture into the shared state-update handler, including the terminal status update that can arrive before the final full-state snapshot. The documented telemetry policy and event-model schema are unchanged by blob SHA in this comparison. The code delta appears oriented toward completeness/timing of usage measurement; it does not by itself demonstrate payload leakage. Nevertheless, any deployed exporter needs a pinned schema test proving emitted properties contain no prompts, raw messages, file content, tool output, secrets or direct identifiers outside an approved contract.

### 2.2 Error path now logs a formatted traceback

Current `main` changes the conversation-run exception path to format a traceback into a plain string and pass it to `logger.error`, rather than using `logger.exception`. The code comment says this avoids a slow Rich-console rendering path and also publishes a detailed error event for the UI where applicable.

**Privacy implication:** changing the logging call does not redact the traceback. Chained LLM/provider errors can contain endpoint details, request metadata or snippets supplied by downstream libraries. The code path is a separate diagnostic sink from product telemetry. Before admission, identify the actual logger handler, persistence/collection destination, access boundary and retention policy, then verify redaction with synthetic adversarial exceptions. No claim is made that this path leaks secrets; the unqualified data boundary is the finding.

### 2.3 Secret-key fallback has identity implications

Current `main` documents a telemetry salt fallback to `OH_SECRET_KEY`, which itself can default to the first session API key; absent that key, a process-random salt is used. A stable salt may make pseudonymous conversation identifiers linkable across restarts. Pseudonymization is not anonymization, and reusing a session API key as a salt couples identity stability to credential lifecycle. The deployment policy must explicitly approve or prohibit this fallback, document rotation effects, and ensure the credential is never emitted.

### 2.4 Persistence change is not a retention guarantee

The reviewed persistence-store delta concerns atomic workspace updates and skipping no-op updates. It does not establish TTL expiry, complete conversation/event deletion, log cleanup, backup erasure or a deletion audit. These remain separate evidence requirements.

## 3. Admission crosswalk

| Requirement | Result this pass | Remaining gate |
|---|---|---|
| Immutable source pin | ESTABLISHED for source inspection | Bind source pin to exact package/container digest |
| Telemetry consent/allowlist implementation | Policy/model blobs unchanged at current head | Exact pinned-version tests and deployment config evidence; no exporter unless explicitly approved |
| Usage metrics minimization | Changed subscriber path identified | Schema/property-level review and adversarial test evidence |
| Error/traceback handling | Current-head logging/event path identified | Redaction test, sink inventory, access controls and bounded retention |
| Identifier pseudonymization | Stable-salt fallback documented in config | Decide approved salt source and rotation/linkability policy |
| Conversation/workspace/log retention | NOT ESTABLISHED | TTL, cleanup, deletion/backup semantics and audit evidence |
| Artifact integrity | OPEN | Package/image digest and source-to-artifact attestation |
| R-06 and target runtime | OPEN | Accepted privacy/egress disposition and runner/workspace/network manifest |

## 4. Disposition and next step

OpenHands Agent Server remains **CANDIDATE / NOT SELECTED / NOT ADMITTED / RUNTIME-UNVERIFIED**. Do not replace the existing pin with current `main` based on this delta. The next source-only step is to read the exact pinned error-event and completion-log event models plus logger configuration, and cross-check the current-head delta for those surfaces. Runtime verification, tests, installation, provider calls, credentials, workflow dispatch and qualification remain behind separate explicit authorization gates.

No repository installation, test execution, qualification, provider/model call, credential use, workflow dispatch, host/runtime inspection, infrastructure modification, merge, rebase, deployment or branch integration occurred.
