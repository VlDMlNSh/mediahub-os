# MediaHub OS — OpenHands Route-to-Capability Matrix, Wave 28

- Date: 2026-10-17
- ID: MH-OPENHANDS-ROUTE-CAPABILITY-28
- Contour: A — Developer Fabric
- Status: READ-ONLY SOURCE REVIEW / CANDIDATE ONLY / QUALIFICATION OPEN
- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
- Parent: [Wave 27 Workspace Cookie and Tool Control Crosswalk](MEDIAHUB-OPENHANDS-WORKSPACE-COOKIE-AND-TOOL-CONTROL-CROSSWALK-WAVE-27-2026-10-17.md)

## 1. Source pin and review boundary

All OpenHands source references are pinned to `OpenHands/software-agent-sdk@6530325e9dd0ea1b6b4f1994d7dab52764cfc3f1`.

| File | Blob SHA | Role |
|---|---|---|
| `openhands-agent-server/openhands/agent_server/api.py` | `1916fd4b00e798e27f85f37db1e634bbef6a48c2` | Router assembly and top-level dependencies |
| `.../server_details_router.py` | `5f7187ea3d4bce7f1725f8e7d72ddbeefce5d928` | Health/readiness/server info |
| `.../init_router.py` | `aae09786c40388b371cc5060a90a9a67bfbf4f3d` | Deferred initialization and init-key auth |
| `.../dependencies.py` | `d1d2a6aece2056adc15824aed6cdccc4c3c33ead` | Session and workspace auth dependencies |
| `.../auth_router.py` | `6549bb7403656a5a6cf96fbd3ce3a8382e9b5397` | Workspace cookie minting/deletion |
| `.../sockets.py` | `33d7a4b1666e9cdcf004b157470e9be16cdfe693` | WebSocket auth and conversation/bash socket endpoints |
| `.../session_socket.py` | `4e02c35e6e4fd67ca5adea31e3f9346f59a29f38` | Session WebSocket and replay/event stream |
| `.../conversation_registry.py` | `69301fb4da8747a1e10418f5acf21c63571a9e66` | Execution, event, workspace and socket router composition |
| `.../runtime_router.py` | `fddc306f933c5a9fd28ff31589d0b08864e7cd19` | Conversation-scoped runtime file/git/bash/VS Code routes |
| `.../event_router.py` | `6c17e33dbfe8ccc7a7691e7b1f18cd0fbb1885a6` | Conversation event read/write routes |
| `.../openai/router.py` | `05183baaae77a8e27cad7c2ea03c5060c5a9443c` | OpenAI-compatible API auth |
| `.../canvas_extensions_bridge_router.py` | `2b16348eb9c99a07725aa01a2301b5b030045169` | Browser app backend HTTP/WebSocket bridge |
| `.../tool_router.py` | `fadc4c14b1970f81266c1c9acaedadd3199014d3` | Tool registry/catalog |
| `.../mcp_router.py` | `71e3fb649fb41a857a7d83f0ff75996ab3f09073` | MCP connection probe and optional tool invocation |
| `.../plugins_router.py` | `f2a766e0d0bad3e0b063fad535eb37f3554522b0` | Plugin install/manage surfaces |
| `.../skills_router.py` | `7b53f010d66b041a87c707f73a105eb18aca9def` | Skill loading and marketplace |
| `.../sub_agents_router.py` | `da5c09b9e52be2353f8e209557ff63261a87ddb5` | Sub-agent discovery/configuration surface |
| `.../llm_router.py` | `05dee5feaa2446e026b1aab0bd5f86415f66c2a9` | Model/provider/device-login operations |
| `.../provider_connections_router.py` | `58a5653caf2e8280d60c2374f63c9d4c448a4469` | Provider credential CRUD |
| `.../settings_router.py` | `4b909015ed53dbea46ca3ee313c2fd67adc40e9a` | Settings/secrets/MCP and profile configuration |
| `.../workspaces_router.py` | `5ee50edc58774be6a7c0b07c0e5b7dc1f6bc0a56` | Persisted workspace paths |
| `.../bash_router.py` | `94367077b00fdb1d5508cef2bb2f6213264352b6` | Bash event/command API |
| `openhands-tools/openhands/tools/preset/default.py` | `d70b10f95435faac5d0cfa527ccd15c74a25fe30` | Default tool registrations |

Read-only GitHub inspection only. No clone/download/install, execution, test, qualification, model/provider invocation, credential use, host/runtime inspection, infrastructure change, deployment or branch integration occurred.

## 2. Route-to-capability matrix

Classifications: **M** = mandatory in reviewed code path; **C** = configuration-dependent; **O** = optional feature/capability; **E** = external enforcement required for MediaHub's trust model; **U** = coverage unresolved pending complete source and target review. A server dependency is not proof of tenant authorization.

| Route family / mount | Source-level control | Capability / risk | MediaHub control required | Classification |
|---|---|---|---|---|
| `/alive`, `/health`, `/ready`, `/server_info` | Mounted from server-details router before protected API groups; no session-key dependency visible on these routes | Liveness, readiness and build/tool inventory disclosure | Restrict public exposure at ingress; return only approved operational metadata | C + E |
| `/api/init` | Separate `X-Init-API-Key`; deliberately bypasses session-key auth and dormant gate | Installs per-session keys, secret key, workspace/conversation path and other runtime config | Isolate init network path; separate issuer from session key; one-time/rotating init capability, strict payload allowlist, replay protection, audit and tenant binding | M auth dependency; E lifecycle |
| Main `/api/*` router | `require_initialized` + `check_session_api_key`; header-only, no workspace cookie | Conversation lifecycle, event, bash, file, git, VS Code, tools, settings, secrets, MCP, plugins, skills, profiles, provider connections | Validate tenant/task/conversation scope on every route; capability allowlist; audit reads and writes; rate/resource budgets | M if configured keys exist; C when key list empty |
| Workspace static/file routes | Separate group with `require_initialized` + `check_workspace_session`; accepts header or workspace cookie | Browser iframe/image/file access | Replace downstream key cookie with scoped short-lived capability; tenant binding; trusted proxy and origin policy; path/mount allowlist | M if keys exist; C by key config; E |
| OpenAI-compatible routes | Separate dependency: `require_initialized` + `check_openai_api_key`; accepts session key via header or Bearer | Chat/completions/responses can create agent work | Enforce per-tenant quotas, model/provider policy, task scope and audit; fail closed when exposed outside a trusted local boundary | M dependency; C because empty session-key config accepts requests |
| Conversation and bash WebSockets | Global `require_initialized`; handler performs WebSocket auth. Supports first-frame auth, legacy query key and header | Live event stream, message/run control and bash event channels | Disable query-key compatibility at MediaHub edge; use first-frame/header with short timeout; ensure key-required fail-closed config; tenant binding per conversation; origin/rate controls | M handler path; C when configured keys absent; E |
| Session WebSocket `/sockets/session/{conversation_id}` | Uses shared authenticated-WebSocket helper; streams durable/transient conversation events and accepts session interactions | Conversation content, actions, confirmation responses | Scope session token to tenant/task/conversation; sequence/replay and revocation semantics; bounded queues and connection quotas | M helper; E scope/lifecycle |
| App-backend session creation/deletion | Route-specific `check_session_api_key`; bridge manager checks origin and issues app-scoped session | Browser access to installed Canvas app backend | Preserve separate origin; allowlisted Origin; short-lived app-scoped cookie, revocation, backend readiness and per-app/tenant binding | M on session endpoints; E browser session |
| App-backend HTTP/WebSocket proxy | Global `require_initialized`; proxy handlers delegate to app-backend session store/bridge | Arbitrary HTTP methods and WebSocket forwarding to installed app backend | Verify session store's auth, origin, target mapping, path normalization and revocation; bind app to tenant and allowlisted backend; no direct public backend exposure | M init gate; E; bridge details need deeper review |
| Runtime routes under `/api/conversations/{runtime_conversation_id}` | Main API key dependency plus `bind_local_conversation_runtime`; resolves workspace path and validates requested paths/trajectory ID | Terminal/bash, file operations, git, VS Code/runtime proxy | Treat local runtime as shared-host code execution, not a sandbox; prefer Docker isolation; non-root, host mount allowlist, egress restrictions, resource quotas, lease/fencing and cleanup | M route guard; C runtime mode; E |
| Event routes under `/api/conversations/{conversation_id}/events` | Main API key dependency; conversation/event service resolves IDs | Read/search/count events; send messages; accept/reject confirmations | Per-tenant conversation ownership check, explicit approval semantics, durable audit and anti-replay idempotency | M auth; E ownership/lifecycle |
| Tool catalog and tool selection `/api/tools` | Main API key dependency; catalog reports registered/usable tools; presets register tools | Terminal, file, git, browser and other execution capabilities | Immutable task-class allowlist; deny by default; enforce at execution layer, not only UI/catalog; record policy decision | M auth; C tool/browser availability; E policy |
| MCP `/api/mcp` | Main API key dependency; probe may connect to a supplied remote server and optionally invoke a caller-chosen tool | Outbound network, external tools, credentials and OAuth state | Egress allowlist, SSRF protection, credential broker, approved tool names, read-only probe allowlist, response redaction and audit | M auth; O probe/tool-call; E network |
| Plugins, skills, canvas extensions `/api/plugins`, `/api/skills`, related routes | Main API key dependency; install/enable/update/uninstall and project/user skill loading | Adds executable hooks, commands, extension bundles and prompts | Disable by default for unattended jobs; signed/pinned source and digest; approval gate; sandboxed install; separate permissions and provenance | M auth; O/C feature; E supply chain |
| Sub-agent discovery `/api/sub-agents`, profiles and meta-profiles | Main API key dependency; discovery may load user/project/built-in definitions; definitions expose tools, MCP, hooks, permission mode and budgets | Delegation and inherited execution authority | Enforce transitive capability ceiling; sub-agent cannot exceed parent task scope; pin definitions and budgets; tenant-bound workspace | M auth; O/config; E |
| LLM/provider connections, settings and secrets | Main API key dependency; dedicated settings/provider-connection storage and secret handling | Provider API keys, base URLs, model selection, OAuth/device flows | MediaHub-owned provider identity and secret vault; egress/provider allowlist; scoped grants; no credential values in task/model output; redact audit and revoke on completion | M auth; C provider features; E |
| Docker runtime conversation proxy | Runtime-specific registry/router; conversation path normalized to container workspace; mounts/config remain target-dependent | Container execution, host mounts and forwarded auth/environment | Accepted target manifest, immutable image digest, non-root, seccomp/capabilities, mount and egress allowlists, resource limits and cleanup evidence | C runtime mode; E target isolation |
| CORS/middleware and browser origins | Middleware branch configured separately; workspace cookie and app backend have browser-specific semantics | Cross-origin requests and browser credential handling | Explicit origin allowlist and trusted proxy normalization; CORS is not authentication; CSRF/Origin review per route family | C config; E policy |

## 3. Mandatory versus optional versus external enforcement

### Mandatory in source path (conditional on mount)
- Main REST API uses the dormant/initialization gate and session-key dependency.
- Workspace static-file routes use a separate cookie-capable dependency.
- OpenAI-compatible routes use their own key-check dependency.
- WebSockets invoke a dedicated authentication helper.
- `/api/init` uses a distinct initialization key.
- Runtime conversation paths include workspace/path binding logic.

### Configuration-dependent or optional
- Session-key enforcement changes behavior when `session_api_keys` is empty; reviewed dependencies permit requests in that state. Public-facing deployment must therefore require a non-empty, rotated key configuration or a separately accepted identity adapter.
- Docker versus local runtime changes the isolation boundary. Local runtime path checks are routing safeguards, not a shell sandbox.
- Browser, MCP, plugins, skills, hooks and sub-agents vary by tool registration and configuration. Hiding an option in UI/catalog is weaker than denying execution at the trusted boundary.
- Deferred initialization is optional; when enabled, init can set the per-session runtime configuration.
- OpenAI-compatible Bearer auth is an alternate input form for the same session key, not a separate identity domain.

### External enforcement required
- Tenant/task/conversation ownership, A0 issuer lifecycle, token expiry/revocation, lease/fencing/replay/cancellation.
- Trusted ingress, proxy-header normalization, origin allowlists, public route exposure and rate limiting.
- Egress controls, secret brokerage, audit retention/deletion, immutable target manifest and independent qualification.
- Route-to-policy coverage across REST, WebSocket, workspace, runtime and app-backend bridge surfaces.

## 4. High-priority findings

1. **Public control-plane surface:** health and server-details routes are mounted outside the session-key-protected API groups. Review exactly which fields `/server_info` returns and restrict ingress exposure.
2. **Empty-key permissive mode:** the source's session-key dependencies intentionally permit requests when the configured key list is empty. A MediaHub deployment contract must fail closed at admission.
3. **WebSocket compatibility:** query-string key support remains for backward compatibility, despite first-frame auth being recommended. Query tokens can enter access logs; MediaHub ingress should reject that mode.
4. **App-backend bridge split:** create/delete session routes require session-key auth, while backend proxy HTTP/WebSocket routes rely on bridge/session state. Trace session issuance, Origin, cookie attributes, path normalization, backend selection and revocation as a distinct security review.
5. **MCP probe is an outbound action:** the route can connect to supplied endpoints and optionally invoke a selected tool. It must be treated as network-capable work, not harmless configuration validation.
6. **Local runtime is not a sandbox:** source comments explicitly characterize path checks as routing safeguards while local processes and VS Code share the host. Use the accepted isolated target rather than relying on path validation.
7. **Extension/configuration surfaces:** plugins, skills, MCP, hooks, provider connections and sub-agent definitions can expand execution authority. Enforce a trusted policy below user interface and agent prompt layers.

## 5. Reuse-first disposition

Reuse OpenHands' router composition, SDK abstractions, event stream, tool registry and runtime adapters where qualified. Do not duplicate these subsystems. MediaHub must retain the identity/tenant boundary, task envelope, capability issuer, admission policy, secrets, canonical evidence and lifecycle state. Upstream authentication remains a local session mechanism rather than the canonical MediaHub trust model.

## 6. Contract impact and admission

- Task envelope v0.2, agent registry v0.2 and evidence manifest v0.2 remain proposed-only.
- A0 issuer/ingress/lifecycle, MH-12 capability semantics, R-06 audit/privacy and accepted target manifest remain open.
- Personal Jarvis canonical upstream identity remains unresolved.
- OpenHands remains **candidate only**: not selected, admitted, qualified or deployed.
- The route map is a source inventory and design input, not runtime verification or a security certification.

## 7. Next bounded pass

Review the Canvas app-backend bridge session store and proxy authorization path, plus route-level credential/provider secret handling. Produce a source-pinned threat table for token issuance, Origin binding, cookie attributes, path/target selection, revocation and audit. Keep all runtime gates closed.
