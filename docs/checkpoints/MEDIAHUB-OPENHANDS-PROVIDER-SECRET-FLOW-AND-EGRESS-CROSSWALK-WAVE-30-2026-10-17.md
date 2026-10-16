# MediaHub OS — Provider Secret Flow and Egress Crosswalk, Wave 30

- Date: 2026-10-17
- ID: MH-OPENHANDS-SECRET-EGRESS-CROSSWALK-30
- Contour: A — Developer Fabric
- Status: READ-ONLY SOURCE REVIEW / CANDIDATE ONLY / RUNTIME ADMISSION BLOCKED
- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
- Parent: [Wave 29 App-Backend Bridge Threat Crosswalk](MEDIAHUB-OPENHANDS-APP-BACKEND-BRIDGE-THREAT-CROSSWALK-WAVE-29-2026-10-17.md)
- Immutable upstream pin: `OpenHands/software-agent-sdk@6530325e9dd0ea1b6b4f1994d7dab52764cfc3f1`

## 1. Scope and method

Read-only inspection of the pinned upstream source. The pass traces provider credentials, secret serialization and decryption, MCP configuration and probing, credential-binding activation, and route authorization boundaries. It does not clone or install code, execute tools, run tests, invoke models/providers, use credentials, inspect hosts/runtimes, change infrastructure, deploy, or integrate branches.

## 2. Source anchors

| Source file | Blob SHA | Source-backed scope |
|---|---|---|
| `openhands-agent-server/openhands/agent_server/provider_connections_router.py` | `58a5653caf2e8280d60c2374f63c9d4c448a4469` | Provider connection CRUD, key rotation, response redaction |
| `openhands-sdk/openhands/sdk/llm/provider_connection_store.py` | `32536844dc604cb9c93815e56dcc6a73a476aaa4` | File-backed shared provider keys and cipher-dependent persistence |
| `openhands-agent-server/openhands/agent_server/_secrets_exposure.py` | `779fc6d3fc66200b2aabecdfb182a0feeb7af12b` | Secret exposure modes and encrypted-input handling |
| `openhands-sdk/openhands/sdk/mcp/config.py` | `0fe8d582088547353a1b255e880607411da28f09` | MCP auth secrets, serialization and decryption helpers |
| `openhands-agent-server/openhands/agent_server/mcp_router.py` | `71e3fb649fb41a857a7d83f0ff75996ab3f09073` | MCP stdio/HTTP configuration, outbound probes, optional tool invocation, OAuth state |
| `openhands-sdk/openhands/sdk/mcp/utils.py` | `0cb5887ad31dd406108d14a7ea5105819e6411b4` | MCP client construction and HTTP transport behavior |
| `openhands-agent-server/openhands/agent_server/credential_binding.py` | `3674e52b3eb4af5684b8e90077b0f72358704911` | Caller-supplied credential-source URL and headers; activation probe |
| `openhands-agent-server/openhands/agent_server/api.py` | `1916fd4b00e798e27f85f37db1e634bbef6a48c2` | Protected API group and separately mounted bridge/socket/init routes |
| `openhands-agent-server/openhands/agent_server/config.py` | `a5830083eb110eadc6262287c5242f50e2296b66` | Server configuration, session keys and cipher configuration |

## 3. Secret-flow findings

### 3.1 Provider connections

- The provider connection API accepts API keys as Pydantic `SecretStr`; normal list/create/update responses expose `api_key_set`, rather than the key value.
- The file-backed store encrypts stored keys when a cipher is supplied. The server obtains that cipher from configuration; `get_cipher()` returns `None` when `OH_SECRET_KEY` is unset.
- In the no-cipher path, the store serializer uses `expose_secrets=True`. Therefore encryption at rest is conditional on effective configuration, and the reviewed code permits plaintext key persistence when the cipher is absent.
- Key rotation updates the shared connection. Profiles resolve the linked connection at load/activation time. Deletion is rejected while a profile or active settings still references the connection.
- The `base_url` is caller-configurable. Source review alone establishes no MediaHub egress allowlist, destination-class policy, or provider-specific route authorization.

**MediaHub requirement:** make cipher presence and key custody explicit admission requirements; fail closed for production-like profiles if the accepted secret-custody policy requires encryption. Keep provider identity, secret custody, execution placement and network egress as separate policy dimensions.

### 3.2 Secret exposure and profile/settings flows

- `X-Expose-Secrets` supports `encrypted` and `plaintext` modes; legacy `true` maps to encrypted mode.
- Incoming Fernet-prefixed LLM secret fields are decrypted before downstream profile/conversation use.
- API group wiring applies `check_session_api_key` to the main `/api/*` router, including provider connections, MCP configuration and settings. This is a useful upstream boundary, but it is a shared session-key mechanism rather than the MediaHub A0 issuer/grant contract.
- Route protection does not by itself establish caller-to-task authorization, tenant isolation, secret-reader authorization, retention policy or audit completeness.

**MediaHub requirement:** adapter code must reject implicit plaintext exposure, bind every secret read to task scope and accepted policy, and emit privacy-minimized durable audit evidence under an accepted R-06 disposition.

### 3.3 MCP configuration, probing and tool invocation

- The MCP probe accepts either a stdio configuration (executable, arguments, environment and working directory) or remote HTTP-family configuration (URL, headers and auth).
- The probe constructs an MCP client and connects to the supplied server. An optional caller-selected tool is invoked when `tool_call` is supplied. Thus the endpoint is an execution and outbound-network capability, rather than a passive configuration validator.
- MCP credentials include API-key, bearer, basic, header and OAuth forms. Secret serialization supports redaction and encrypted/plaintext exposure contexts.
- OAuth probe state can be returned to the caller for persistence. Probe jobs are held in process memory with a 15-minute TTL; this is not a durable MediaHub authorization or audit ledger.
- The reviewed code does not establish a MediaHub-owned executable allowlist, remote-destination allowlist, DNS/IP egress enforcement, workload identity, per-task budget, or an independent read-only guarantee for arbitrary caller-supplied MCP tool names.
- The SDK has origin-bound header handling for a package-declared remote MCP path. That specialized path is not evidence that all user-configured MCP endpoints share an equivalent destination policy.

**MediaHub requirement:** treat MCP probe and tool execution as privileged outbound actions. Admission needs a bounded transport registry, executable policy, destination validation plus network-layer egress controls, secret scoping, explicit tool authorization, budget/time limits, cancellation, and evidence binding.

### 3.4 Credential-binding activation

- `PUT /api/conversations/{conversation_id}/credential-bindings/{secret_name}` accepts a source URL and headers, probes the source, then activates a versioned credential binding.
- Header count and string lengths are bounded, and supported secret names are checked. These checks do not replace destination policy, identity binding, or network egress enforcement.
- The source review does not prove that a supplied URL is restricted to an approved secret broker or that its target is tied to the current MediaHub task/tenant.

**MediaHub requirement:** only accept an immutable, policy-resolved credential reference issued by the accepted credential authority. Direct arbitrary URLs remain outside the candidate admission contract.

## 4. Route and authority summary

| Surface | Upstream behavior observed | MediaHub disposition |
|---|---|---|
| Provider connection CRUD | Main session-key-protected API; key output redacted in ordinary response; cipher-dependent at-rest encryption | Candidate pattern; add A0 grants, explicit cipher gate, reader scope, egress policy and audit |
| Settings/profile secret exposure | Explicit `X-Expose-Secrets` modes | Plaintext exposure requires strict scope, explicit policy and audit; default to redaction |
| MCP test / OAuth probe | Authenticated API surface can create subprocesses or outbound HTTP and optionally call a tool | Privileged capability; block runtime admission pending allowlists and egress enforcement |
| MCP runtime | Configured remote servers and tools can make outbound requests | Resolve destinations through MediaHub policy; no silent fallback |
| Credential binding | Caller-supplied URL and headers are probed before activation | Replace arbitrary endpoint with accepted credential-authority reference |
| Init, bridge and WebSocket groups | Mounted under distinct dependencies from the main API group | Preserve the separate threat model and verify each route group against A0/R-06; shared API key alone is insufficient |

## 5. Required contract gaps

1. A0 issuer/grant schema, audience, expiry, revocation, key rotation, task binding and fail-closed verification.
2. Accepted credential vault/custody model; mandatory encryption behavior and key-rotation/recovery evidence.
3. Provider route identity and egress policy, including DNS resolution, private/link-local ranges, redirects, TLS and proxy behavior.
4. MCP server admission registry: transport, executable/image pin, destination policy, tool allowlist, scopes, time/budget limits and revocation.
5. Task/tenant/workspace binding for provider connections, credential binding, MCP sessions and artifacts.
6. Secret exposure policy, minimized audit schema, durable acknowledgement, outage behavior, retention/deletion and authorized readers under R-06.
7. Independent negative/degraded-mode qualification, followed by separately authorized release and deployment decisions.

These are proposed closure criteria. No test or qualification was run.

## 6. Decision and next step

**Disposition:** retain OpenHands as a source-pinned candidate only. Reuse provider-connection and MCP SDK abstractions solely through a MediaHub-owned adapter after authority, secret-custody, egress, tenant-isolation and audit contracts close. The v0.2 task envelope, agent registry and evidence manifest remain PROPOSED ONLY. Runtime admission remains BLOCKED.

Next bounded pass: compare the discovered secret and egress requirements with the current MediaHub A0/MH-12/R-06 contracts and accepted target-manifest work; produce a closure crosswalk that distinguishes upstream capability, adapter control, infrastructure enforcement and independent evidence.

## 7. Verification boundary

Evidence consists of GitHub source reads at the immutable upstream commit and MediaHub document reads. No code was installed or executed; no test, provider/model call, credential operation, host/runtime inspection, infrastructure change, deployment or branch integration occurred.
