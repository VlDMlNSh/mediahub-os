# MediaHub OS — OpenHands Workspace Cookie and Tool Control Crosswalk, Wave 27

- Date: 2026-10-17
- ID: MH-OPENHANDS-WORKSPACE-TOOLS-27
- Contour: A — Developer Fabric
- Status: READ-ONLY SOURCE REVIEW / CANDIDATE ONLY / QUALIFICATION OPEN
- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
- Parent: [Wave 26 Agent Server Security Boundary Crosswalk](MEDIAHUB-OPENHANDS-AGENT-SERVER-SECURITY-BOUNDARY-CROSSWALK-WAVE-26-2026-10-17.md)

## 1. Scope and immutable source pin

Reviewed source from `OpenHands/software-agent-sdk@6530325e9dd0ea1b6b4f1994d7dab52764cfc3f1`. This was a GitHub source-read pass only. No clone, download, install, execution, tests, qualification, model/provider call, credential use, host/runtime inspection, infrastructure change, deployment or branch integration occurred.

| Source | Blob SHA | Relevant scope |
|---|---|---|
| `openhands-agent-server/openhands/agent_server/auth_router.py` | `6549bb7403656a5a6cf96fbd3ce3a8382e9b5397` | Cookie mint/delete, scope, lifetime and secure-context logic |
| `openhands-agent-server/openhands/agent_server/dependencies.py` | `d1d2a6aece2056adc15824aed6cdccc4c3c33ead` | Session-key and workspace-cookie validation |
| `openhands-agent-server/openhands/agent_server/workspace_router.py` | `e38f5f99e6efb8b464c31c8e06fcdf4e06ce064c` | Conversation lookup, local workspace resolution, path containment |
| `openhands-agent-server/openhands/agent_server/api.py` | `1916fd4b00e798e27f85f37db1e634bbef6a48c2` | Route auth groups and cookie scope |
| `openhands-agent-server/openhands/agent_server/models.py` | `d5f8ee4c69eeb73946af4643ebc39024d0f3c171` | Conversation workspace, confirmation policy, optional analyzer and hooks |
| `openhands-agent-server/openhands/agent_server/conversation_router.py` | `e57ae2b1260e97ca06743dbd15487eaab1672ccd` | Conversation read paths |
| `openhands-agent-server/openhands/agent_server/docker_runtime/routers.py` | `fa6eb7f58f6e5281cff2f0b358c6abcd2aa0e2d7` | Docker conversation workspace normalization and proxy setup |
| `openhands-tools/openhands/tools/preset/default.py` | `d70b10f95435faac5d0cfa527ccd15c74a25fe30` | Default terminal, file editor, task tracker, optional browser/subagent tools |

Revision-pinned source URLs use https://github.com/OpenHands/software-agent-sdk/blob/6530325e9dd0ea1b6b4f1994d7dab52764cfc3f1/.

## 2. Source-backed findings

### F27-01 — Workspace cookie contains the session API key

`POST /api/auth/workspace-session` mints the workspace cookie after the parent route validates the `X-Session-API-Key` header. The cookie value is the session API key itself. Attributes include `HttpOnly`, `SameSite=None`, path `/api/conversations`, and a nominal 10-year Max-Age. The implementation appends `Partitioned` only when it considers the request a secure context; `Secure` is likewise conditional on HTTPS or loopback. The code comments state that browsers commonly clamp persistent cookie age to about 400 days.

The secure-context decision trusts `X-Forwarded-Proto` and `X-Forwarded-Host` when present. Correctness therefore depends on a trusted proxy stripping untrusted inbound forwarding headers and setting authoritative values. The cookie path is broader than the workspace file route alone: it scopes to conversation API URLs, although server authentication code deliberately honors the cookie only in the workspace route group.

Disposition: do not expose this cookie flow through arbitrary ingress. Prefer a MediaHub-owned short-lived, workspace-only scoped capability rather than copying a long-lived downstream session API key into a browser cookie. Require trusted-proxy header normalization, explicit origin policy, key rotation/revocation, secure transport, and a bounded TTL before any runtime admission.

### F27-02 — Authentication is server/session-wide, not visibly tenant-scoped in workspace routes

The workspace authorization dependency accepts a session key from either the header or cookie if it appears in the server's configured session-key list. The workspace router then resolves a conversation by UUID and validates the local workspace path. In the reviewed functions, the conversation ID is the resource selector; the route code does not show a caller-to-conversation ownership/tenant binding.

This is a source-bound observation, not proof of an exploitable vulnerability in every deployment: a single-tenant deployment may intentionally share one trust domain, while an external orchestrator may enforce tenancy elsewhere. The reviewed router contract alone does not establish that enforcement.

Disposition: MediaHub must bind every request to tenant, task, conversation, workspace and capability scope at its own authorization boundary, and ensure downstream identifiers cannot cross tenant boundaries. Independent review must cover every REST/WebSocket route and direct/runtime proxy path, not workspace static serving alone.

### F27-03 — Tool presets include powerful execution capabilities

The default tool preset registers `TerminalTool`, `FileEditorTool` and `TaskTrackerTool`; browser tools are enabled by default in the preset unless explicitly disabled, and sub-agent delegation can be enabled separately. The Agent Server route surface includes tools, bash, git, file, VS Code, skills, sub-agents, plugins, hooks, LLM settings, provider connections, MCP, profiles and workspace routes. Conversation models expose a workspace, confirmation policy, optional security analyzer and hooks.

These are composable capabilities, not a MediaHub authorization policy. An optional analyzer and hook mechanisms are available in the source model, but their presence does not prove mandatory deny-by-default enforcement or complete mediation for all tools. Disabling browser alone would leave terminal, file, git and other server APIs as material capabilities.

Disposition: require an explicit allowlist by task class, a deny-by-default capability map, immutable tool/preset version, constrained execution target, network egress policy, resource budgets, confirmation/approval semantics for sensitive actions, and auditable decisions. Task/model content must never grant itself additional tools or modify the trusted preset.

### F27-04 — Path containment and tenant isolation are different controls

The workspace router resolves the selected workspace directory and target path, then rejects resolved targets outside that directory. This is useful path containment. It does not by itself prove tenant authorization, safe mount configuration, secret exclusion, artifact sanitization, or protection from every concurrent filesystem/runtime race.

The Docker router normalizes a conversation workspace to the container path `/workspace` and may represent a supplied host workspace as a mount source. This is another reason the accepted target manifest and strict host-path allowlist are prerequisites.

Disposition: preserve upstream path containment, while separately requiring tenant binding, mount allowlists, immutable images, non-privileged runtime, resource/egress limits, lease/fencing, cleanup and recovery evidence.

## 3. Reuse-first capability disposition

| Capability | Upstream reuse | MediaHub-owned control / gap | Status |
|---|---|---|---|
| Workspace cookie endpoint | Existing browser-embed mechanism | Replace or wrap with scoped short-lived capability; trusted proxy and origin policy | BLOCKED |
| Header/cookie validation | Existing downstream auth | Tenant/task/conversation binding and canonical issuer lifecycle | BLOCKED |
| Workspace path containment | Existing resolved-path guard | Tenant authorization, mount/secret controls, independent race review | SOURCE REVIEW ONLY |
| Tool presets | Reuse SDK tools and declarative composition | Task-class allowlist, deny-by-default authorization and egress limits | BLOCKED |
| Security analyzer/hooks | Existing extension points | Mandatory enforcement contract and full route/tool coverage evidence | UNPROVEN |
| Docker workspace proxy | Existing executor integration | Accepted target, host-path allowlist, immutable image and isolation evidence | TARGET-GATED |

Reuse existing OpenHands components where appropriate; do not create duplicate MediaHub tool implementations without a documented capability gap.

## 4. Contract impact

- Task envelope v0.2, agent registry v0.2 and evidence manifest v0.2 remain PROPOSED ONLY.
- A0 issuer/ingress/lifecycle, lease/fencing/replay/cancellation, MH-12 capability semantics, R-06 audit/privacy disposition and accepted target manifest remain open.
- Personal Jarvis authoritative upstream identity remains unresolved.
- OpenHands remains a research candidate: NOT SELECTED, NOT ADMITTED, NOT QUALIFIED, NOT DEPLOYED.
- Source reads establish code structure at the pinned revision; they do not establish deployed configuration, exploitability, or qualification.

## 5. Required evidence before runtime proposal

1. Cookie capability threat model, bounded lifetime, revocation semantics and trusted-proxy contract.
2. Complete route-to-tenant authorization matrix across REST, WebSocket, workspace and runtime proxy surfaces.
3. Task-class tool allowlist and deny-by-default enforcement, including terminal, file, git, browser, MCP, plugins and sub-agents.
4. Security analyzer and hook failure semantics; proof of complete mediation and durable audit decisions.
5. Accepted target manifest, immutable image/dependency digests, mount allowlist, egress policy, resource budgets and cleanup/recovery evidence.
6. Independent negative-path review and target-specific qualification under separate authorization.

## 6. Disposition

**Wave 27 source review complete; candidate admission remains blocked.** The key newly established facts are that the workspace cookie carries the downstream session API key with a nominal 10-year Max-Age, and the visible workspace route checks session membership plus resource/path resolution rather than an explicit tenant ownership relation. Tool defaults include terminal and file editing, with browser and sub-agent capabilities configurable. These findings strengthen the case for a MediaHub-owned capability and authorization boundary around reused upstream components.

Next: document a source-bound route-to-capability matrix for every API group and identify which upstream controls are mandatory versus optional. Preserve all runtime gates.
