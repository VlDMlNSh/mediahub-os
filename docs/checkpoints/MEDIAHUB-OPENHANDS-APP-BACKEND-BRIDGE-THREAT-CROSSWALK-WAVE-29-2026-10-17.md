# MediaHub OS — OpenHands Canvas App-Backend Bridge Threat Crosswalk, Wave 29

- Date: 2026-10-17
- ID: MH-OPENHANDS-APP-BRIDGE-THREAT-29
- Contour: A — Developer Fabric
- Status: READ-ONLY SOURCE REVIEW / CANDIDATE ONLY / RUNTIME ADMISSION BLOCKED
- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
- Parent: [Wave 28 route-to-capability matrix](MEDIAHUB-OPENHANDS-ROUTE-TO-CAPABILITY-MATRIX-WAVE-28-2026-10-17.md)

## 1. Scope and source pin

Reviewed OpenHands source at immutable pin `OpenHands/software-agent-sdk@6530325e9dd0ea1b6b4f1994d7dab52764cfc3f1`. This pass covers Canvas app-backend session issuance, Origin and ingress binding, cookie construction, backend selection, path normalization, revocation, WebSocket expiry and route-level auth assembly. Source inspection only; no application execution or test invocation.

| Source | Blob SHA | Evidence scope |
|---|---|---|
| `canvas_extensions/bridge.py` | `7a73dccb24c3895993ed08212eac239020e2712a` | Session store, Origin validation, backend selection, proxy path and cookie |
| `canvas_extensions_bridge_router.py` | `2b16348eb9c99a07725aa01a2301b5b030045169` | HTTP/WS route declarations and session bootstrap auth |
| `canvas_extensions_router.py` | `c0d8f9020435e980ec98ef6ab5938d17b08e3d66` | Extension lifecycle and backend revocation/stop path |
| `canvas_extensions/backend.py` | `bd69ac58fd35b9cf0354b47ae27f5d97f4a3a54e` | Backend lifecycle manager and artifact controls |
| `dependencies.py` | `d1d2a6aece2056adc15824aed6cdccc4c3c33ead` | Session-key dependency |
| `api.py` | `1916fd4b00e798e27f85f37db1e634bbef6a48c2` | Router-level auth and initialization gates |

## 2. Source-bound control matrix

| Surface | Observed upstream control | Classification | MediaHub disposition |
|---|---|---|---|
| Session creation | `POST /app-backends/{extension_name}/session` has `check_session_api_key` dependency; requires configured ingress host and allowed control Origin; rejects same-origin ingress | Mandatory in this route path; behavior also depends on config | Keep behind MediaHub identity/tenant authorization and short-lived task-scoped capability |
| Session token | Random URL-safe token; SHA-256 digest stored server-side; authorization compares digest and binds session to extension name plus exact endpoint tuple | Mandatory in reviewed implementation | Positive property; add tenant, task, issuer, expiry and revocation lineage in MediaHub authority |
| Cookie | Five-minute TTL; path scoped to extension; `Secure`, `HttpOnly`, `SameSite=None`, Partitioned attribute append | Mandatory in reviewed helper; secure-context check gates issuance | Preserve short TTL; verify browser/proxy behavior during authorized qualification |
| Ingress origin | Host/scheme derived from request, with forwarded headers used only when `trust_forwarded_headers` is enabled; configured public URL comparison | Config-dependent trust boundary | Proxy must strip client forwarding headers and write authoritative values; enforce canonical host at edge |
| Control Origin | Localhost and configured CORS origin/regex paths can qualify; same public ingress origin is rejected for bootstrap | Config-dependent allowlist | Production policy should use explicit origins; regex and environment-derived exceptions require review |
| Proxy Origin | HTTP unsafe methods require Origin matching configured public origin; WebSocket path always requires matching Origin | Mandatory in reviewed proxy functions | Preserve method-aware CSRF control; test missing, null, malformed and cross-origin Origin cases |
| Backend selection | Ready endpoint resolved by extension name; accepted target must be loopback host | Mandatory in reviewed path | Positive SSRF boundary; additionally bind immutable admitted artifact/revision and tenant/workspace |
| Path normalization | Repeated URL decoding to fixed point; rejects backslash and dot/dot-dot segments; auth query stripped before forwarding | Mandatory in reviewed path | Retain canonicalization; verify upstream decoding equivalence and encoded separators with negative-path qualification |
| HTTP proxy | Uses selected loopback endpoint; rejects redirects; forwards constructed path/query | Mandatory in reviewed helper | Add explicit request/response size, timeout, method and header policy in MediaHub wrapper |
| WebSocket proxy | Authenticates session before accept; attaches current task to session; reaper cancels active sockets at expiry; revocation cancels tasks | Mandatory in reviewed implementation | Positive expiry/revocation design; verify race behavior and cancellation propagation independently |
| Session deletion | Requires session API key and bootstrap Origin; revokes token found in cookie and clears cookie | Mandatory route dependency and checks | Confirm logout/revocation semantics for concurrent sessions and tenant offboarding |
| Extension lifecycle | Disable/uninstall/revision changes route through revoke-and-stop helper in observed paths | Route-dependent | Map every mutation path to revocation; verify force reinstall, crash and server shutdown cases |
| API auth grouping | Main `/api/*` routes receive initialization and session-key dependencies; workspace routes use separate header-or-cookie dependency; bridge gets initialization dependency plus route-specific bootstrap auth | Mandatory in router assembly; some groups have separate auth models | Keep route-by-route allowlist and explicit public-route inventory; avoid assuming a single global auth policy |
| Backend process/artifact | Backend manager constrains platform and has artifact byte cap, redirect cap and secure URL policy knobs; execution is a local subprocess manager | Configuration-dependent and lifecycle-specific | Localhost binding is not a sandbox; require isolated target, pinned artifact digest, least privilege and egress limits |

## 3. Security interpretation

1. The app bridge has meaningful controls in source: extension-bound sessions, digest-only token storage, five-minute expiry, cookie scope, Origin/ingress checks, loopback backend target selection, path traversal checks, redirect rejection and WebSocket revocation.
2. These controls reduce specific risks but do not establish tenant ownership, task-level capability semantics, process isolation, secret separation, outbound network policy, comprehensive audit evidence or safe deployment configuration.
3. `trust_forwarded_headers`, public ingress URL, CORS allowlists/regex, backend manager lifecycle and runtime environment are configuration-sensitive. Source inspection does not establish deployed values.
4. The app-backend bridge proxy endpoints are declared separately from session-creation endpoints. The source relies on cookie session authorization and Origin/ingress checks for proxy routes; router-wide initialization is applied. Review of this route group alone cannot certify every surrounding middleware/proxy deployment.
5. Session-store revocation cancels tracked WebSocket tasks and expiry reaping exists for active sockets. HTTP requests are individually authorized; in-flight HTTP cancellation and full lifecycle race guarantees require separate verification.
6. Loopback backend restriction is a useful SSRF boundary but is not equivalent to process sandboxing or tenant isolation.

## 4. Required MediaHub-owned controls

- Bind each issued capability to tenant, task, conversation, workspace, issuer, target revision, allowed methods/routes and expiration.
- Keep authorization in a MediaHub-owned control plane; upstream session keys are adapter credentials, not the canonical identity model.
- Apply explicit origin allowlists and a trusted-proxy contract; strip inbound forwarding headers before setting authoritative proxy values.
- Enforce per-task route/tool allowlists, request and response size limits, timeouts, concurrency/resource quotas and egress restrictions.
- Admit only immutable extension/backend revisions with verified artifact digests and approved execution profiles.
- Emit append-only evidence for issue, use, denial, expiry, revoke, backend start/stop, target resolution and policy version; redact credentials and request secrets.
- Qualify expiry, revocation, path traversal, Origin, proxy spoofing, redirect, target substitution, race, crash-recovery and cross-tenant negative paths on an explicitly accepted target.

## 5. Admission status

- OpenHands remains a candidate only; no selection, integration, qualification or deployment is claimed.
- Task envelope v0.2, agent registry v0.2 and evidence manifest v0.2 remain proposed-only.
- A0 issuer/ingress/lifecycle, MH-12 capability semantics, R-06 audit/privacy disposition and accepted target manifest remain open.
- Personal Jarvis authoritative upstream identity remains unresolved.
- Runtime gates remain closed.

## 6. Verification boundary

Read-only GitHub source retrieval and documentation writes only. No installation, clone, execution, tests, qualification, model/provider calls, credential use, host/runtime inspection, infrastructure changes, deployment, merge or rebase.

## 7. Next bounded pass

Trace provider credential storage/decryption, provider-connection routes, MCP server configuration and outbound probes/tool calls. Produce a source-bound secret-flow and egress matrix, distinguishing stored credentials, request-supplied values, runtime process environment and external-network calls. Preserve all runtime gates.
