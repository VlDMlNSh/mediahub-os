# MediaHub OS — OpenHands Current-Head Delta and Route-Boundary Reconciliation, Wave 40

- Date: 2026-10-17
- Contour: A — Developer Fabric
- Status: CURRENT-UPSTREAM SOURCE REVIEW / ROUTE-ASSEMBLY DELTA VERIFIED / RUNTIME ADMISSION BLOCKED
- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
- MediaHub `main` HEAD at pass start: `6c2e8dbdee81c798b64e65546e7ded07093f100a`
- Documentation branch HEAD at pass start: `82ecb1a0be728e20b584b0c1031e413306fb913e`
- MediaHub branch comparison at pass start: DIVERGED, documentation branch ahead 1986 / behind 14; merge base `f0f406feb9f9816b009f4e6e756813541e53b9bc`
- OpenHands candidate pin: `OpenHands/software-agent-sdk@6530325e9dd0ea1b6b4f1994d7dab52764cfc3f1`
- OpenHands current `main` at pass time: `bf9b6057b00e1b2b532ecff508c0d92d818adced`, signed commit verified by GitHub API.
- Upstream comparison: current `main` is 9 commits ahead of the pin, 0 behind.

## 1. Purpose and source boundary

Refresh the existing Wave 26–30 OpenHands route, workspace, tool, bridge and secret-flow reviews against the current upstream default branch. Source retrieval only. No clone, install, code execution, tests, provider calls, credentials, host/runtime inspection, infrastructure change, deployment or qualification.

Primary prior reports:
- [Wave 26 — Agent Server route and workspace security crosswalk](MEDIAHUB-OPENHANDS-AGENT-SERVER-ROUTE-WORKSPACE-SECURITY-CROSSWALK-WAVE-26-2026-10-17.md)
- [Wave 27 — Workspace cookie and tool control](MEDIAHUB-OPENHANDS-WORKSPACE-COOKIE-AND-TOOL-CONTROL-CROSSWALK-WAVE-27-2026-10-17.md)
- [Wave 28 — Route-to-capability matrix](MEDIAHUB-OPENHANDS-ROUTE-TO-CAPABILITY-MATRIX-WAVE-28-2026-10-17.md)
- [Wave 29 — App-backend bridge threat crosswalk](MEDIAHUB-OPENHANDS-APP-BACKEND-BRIDGE-THREAT-CROSSWALK-WAVE-29-2026-10-17.md)
- [Wave 30 — Provider secret flow and egress](MEDIAHUB-OPENHANDS-PROVIDER-SECRET-FLOW-AND-EGRESS-CROSSWALK-WAVE-30-2026-10-17.md)

## 2. Immutable source identity and delta

The upstream compare endpoint reports 9 commits from the reviewed pin to current `main`. The pinned commit is the comparison base; current `main` contains the following material source deltas relevant to task execution:

| File | Pinned blob | Current blob | Source-level change |
|---|---|---|---|
| `openhands-agent-server/openhands/agent_server/bash_router.py` | `94367077b00fdb1d5508cef2bb2f6213264352b6` | `90b5bcde9d8f200843354e5778faa27ff60fbb4b` | Collects all paginated BashOutput chunks; absent exit code maps to `-1` |
| `openhands-agent-server/openhands/agent_server/bash_service.py` | `585e0ad8a83cd78023ca495d7bcc8e7b550823ba` | `3bba2504e2188f719212a0498c8b7112991e0d13` | Applies filters before page limits and advances cursor to a matching event |
| `openhands-agent-server/openhands/agent_server/event_service.py` | `7323213c8a9eddb414b54996398a6bd3ca1c2ea9` | `59bfa63127303af4c81730c67869d4a5973ce428` | Adds run-slot reservation and stale goal-state reconciliation; adjusts event/run admission flow |
| `openhands-agent-server/openhands/agent_server/profiles_router.py` | `6f976924c3a0210766d9aa60f0e22129f5978022` | `55291e3c0d2f1c797baa43378c169879244f6e05` | Adds a 15-second bounded, single-attempt profile preflight; quota exhaustion fails validation |
| `openhands-agent-server/openhands/agent_server/openai/service.py` | changed in compare | changed in compare | Reserves run capacity before persisting the incoming message; releases the reservation afterwards |
| `clients/typescript/src/workspace/remote-workspace.ts` | changed in compare | changed in compare | Missing exit code maps to `-1` rather than success |
| `tests/agent_server/test_run_admission.py` | added after pin | present at current head | Adds source-level test cases for run-slot admission; tests were not executed |

Core route/auth files remained byte-identical by Git blob SHA between the pin and current head:

| File | Blob SHA at both refs |
|---|---|
| `openhands-agent-server/openhands/agent_server/api.py` | `1916fd4b00e798e27f85f37db1e634bbef6a48c2` |
| `openhands-agent-server/openhands/agent_server/init_router.py` | `aae09786c40388b371cc5060a90a9a67bfbf4f3d` |
| `openhands-agent-server/openhands/agent_server/dependencies.py` | `d1d2a6aece2056adc15824aed6cdccc4c3c33ead` |
| `openhands-agent-server/openhands/agent_server/runtime_router.py` | `fddc306f933c5a9fd28ff31589d0b08864e7cd19` |
| `openhands-agent-server/openhands/agent_server/mcp_router.py` | `71e3fb649fb41a857a7d83f0ff75996ab3f09073` |

The unchanged blobs establish that the 9-commit upstream delta did not modify these reviewed route assembly, initialization, dependency, runtime-route or MCP-route files. They do not establish deployment configuration or runtime behavior.

## 3. Interpretation of the delta

1. **Bash result handling is more fail-closed.** The current route gathers all stored output chunks and maps a missing exit code to `-1`. This reduces false success from incomplete output or an absent status.
2. **Run admission is more explicit.** The current event service reserves capacity before saving input for the OpenAI-compatible path, reducing the chance that a 429 leaves an input message behind. New admission tests exist in source; no test execution is claimed.
3. **Profile preflight is bounded.** The current route limits a single validation attempt to at most 15 seconds, removes retries/fallback for that preflight, and treats reported exhausted quota as invalid configuration.
4. **These are reliability and correctness improvements, not MediaHub authority controls.** They do not establish an A0 issuer/grant contract, tenant ownership, task-bound capability scope, lease fencing, replay prevention, cancellation/recovery, MH-12 complete mediation, R-06 audit/privacy, egress allowlisting, or an accepted target manifest.
5. **The earlier security findings remain open.** The source pin still has an optional server session key and a separate initialization key; route families use different auth dependencies; workspace-cookie/browser routes have separate origin/session semantics; MCP probe/configuration can initiate outbound connections and optionally call a tool; local workspace path checks alone do not prove isolation.

## 4. Admission disposition

Keep OpenHands as a reusable source candidate, not an admitted runtime. The upstream update contains useful reliability changes, while the reviewed MediaHub-specific authority, tenant, capability, egress, evidence and lifecycle boundaries remain unresolved.

No MediaHub source code, workflow, registry, credentials, runtime, infrastructure or branch integration was changed. No tests, qualification, deployment or provider interaction occurred.

## 5. Next bounded step

Prepare a narrowly scoped adapter/qualification proposal that maps the unchanged upstream route families to MediaHub-owned A0/MH-12/R-06 enforcement and lists the minimum accepted target manifest. Reuse OpenHands routing, workspace, event, tool and provider abstractions where qualified; keep the adapter and runtime blocked until the authority and target contracts are accepted.

- Project map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
