# MediaHub OS — OpenHands Agent Server Security Boundary Crosswalk, Wave 26

- Date: 2026-10-17
- ID: MH-OPENHANDS-SECURITY-BOUNDARY-26
- Contour: A — Developer Fabric
- Status: READ-ONLY SOURCE REVIEW / CANDIDATE ONLY / QUALIFICATION OPEN
- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
- Parent: [Wave 25 contract crosswalk](MEDIAHUB-OPENHANDS-TASK-REGISTRY-EVIDENCE-CONTRACT-CROSSWALK-WAVE-25-2026-10-17.md)

## 1. Scope and source pins

Read-only review of source and documentation at the exact OpenHands Software Agent SDK commit `6530325e9dd0ea1b6b4f1994d7dab52764cfc3f1`. No clone, download, install, execution, test, qualification, model/provider call, credential use, host/runtime inspection, infrastructure change, deployment or branch integration occurred.

| Upstream source | Blob SHA | Reviewed scope |
|---|---|---|
| `openhands-agent-server/openhands/agent_server/__main__.py` | `226f43dca5a2d1799c84199bbd85bd07bfc98339` | Effective bind host and session-key startup guard |
| `openhands-agent-server/openhands/agent_server/config.py` | `a5830083eb110eadc6262287c5242f50e2296b66` | Session keys, CORS and workspace paths |
| `openhands-agent-server/openhands/agent_server/api.py` | `1916fd4b00e798e27f85f37db1e634bbef6a48c2` | Route-level authentication grouping |
| `openhands-agent-server/openhands/agent_server/dependencies.py` | `d1d2a6aece2056adc15824aed6cdccc4c3c33ead` | Header and workspace-cookie authentication |
| `openhands-agent-server/openhands/agent_server/middleware.py` | `d2c4edec9742fd8c287ef4e258acad33340bdb5a` | Separate CORS policy for workspace cookie routes |
| `openhands-agent-server/openhands/agent_server/init_router.py` | `aae09786c40388b371cc5060a90a9a67bfbf4f3d` | Warm-pool initialization, per-user keys, paths and environment |
| `openhands-agent-server/openhands/agent_server/workspace_router.py` | `e38f5f99e6efb8b464c31c8e06fcdf4e06ce064c` | Static workspace file serving and path containment |
| `openhands-agent-server/openhands/agent_server/README.md` | `a64ff0840230ff5ae2d7c167c824048eaf72da9f` | Operator-facing setup/configuration claims |
| `openhands-workspace/openhands/workspace/docker/workspace.py` | `64ea81d2d4d7dfedcd8c6fea6081e75049edf782` | Container workspace, mounts, forwarded environment |

All URLs are revision-pinned under https://github.com/OpenHands/software-agent-sdk/tree/6530325e9dd0ea1b6b4f1994d7dab52764cfc3f1.

## 2. Source-backed findings

### F26-01 — README/runtime bind-default discrepancy

The Agent Server README documents `0.0.0.0` as the default bind host. At the reviewed source pin, `__main__.py` selects loopback `127.0.0.1` when no explicit host and no session API key are configured; with a session key it selects `0.0.0.0`. An explicitly supplied wildcard host without a key emits a warning and continues. Therefore the blanket claim “default always binds to all interfaces” is inaccurate for this source revision; explicit wildcard binding without authentication remains a documented exposure path. Container examples intentionally bind inside the container and publish host loopback ports, which is a distinct network boundary.

Disposition: adapter deployment configuration must pin the actual command, effective config, container port mapping and ingress policy. Require an authenticated route and a private network boundary; warnings alone are not a security control.

### F26-02 — Authentication is optional and route-class-specific

The server supports session API keys via `SESSION_API_KEY` / `OH_SESSION_API_KEYS_0`. The main API router groups most `/api/*` endpoints under `require_initialized` and `check_session_api_key`; `/api/init` uses a distinct `X-Init-API-Key` path. Workspace static-file routes are intentionally separated and accept either the session header or a workspace-session cookie. Authentication configuration is therefore a runtime precondition, not an intrinsic guarantee supplied by the SDK interface.

Disposition: MediaHub must own external ingress and caller authorization, with explicit audience, expiry, revocation, target/scope binding, replay protection, rotation and audit controls. Upstream API keys must remain a downstream transport credential, never the canonical MediaHub capability issuer.

### F26-03 — Workspace file serving is a separate data-exposure surface

The workspace router serves files from a conversation's local workspace. The source resolves the workspace path and rejects a resolved target outside the workspace root. That path-containment control is useful, but it does not by itself prove workspace confidentiality, authorization correctness, secret exclusion, or isolation between conversations/tenants. Workspace cookie routes use a distinct CORS branch that echoes HTTP(S) origins; the cookie route policy is intentionally broader than the ordinary configured CORS allowlist. This is an explicit browser/data-boundary review item, not by itself a demonstrated exploit.

Disposition: keep workspace serving disabled or isolated from external exposure until cookie minting, SameSite/Secure/HttpOnly scope, origin behavior, conversation ownership checks, cross-tenant isolation and artifact classification are independently reviewed against the exact deployment target.

### F26-04 — Warm-pool initialization can set per-user environment and filesystem roots

The `POST /api/init` request model supports per-user session keys, secret key, conversation paths, worktree root, webhooks, CORS origins, concurrency, telemetry, and an `env` map applied through `os.environ.update` before conversation services start. This is a powerful orchestrator interface. Its safety depends on the distinct init-key trust boundary, orchestrator integrity, strict payload construction, tenant isolation and prevention of credential cross-contamination.

Disposition: the MediaHub adapter must treat init payloads as privileged control-plane data, generated only by an accepted issuer/orchestrator; prohibit task/model content from setting arbitrary environment, webhooks, storage roots or auth material. Use an explicit per-field allowlist and auditable per-tenant configuration digest.

### F26-05 — Docker workspace defaults forward selected environment and support volume mounts

The Docker workspace declares `SESSION_API_KEY` and `OH_SESSION_API_KEYS_0` among default forwarded variables, and accepts additional volume mappings. This supports an isolated execution abstraction, but the SDK declaration alone establishes no MediaHub-specific mount allowlist, host privilege profile, network-egress policy, image digest, cleanup guarantee or tenant isolation.

Disposition: require immutable image digest, exact mount allowlist, non-privileged runtime, read-only mounts where practical, network policy, resource ceilings, workspace lease/fencing, cleanup/recovery evidence and a source-bound target manifest.

## 3. Reuse-first capability disposition

| Capability | Existing upstream reuse | MediaHub-owned gap / boundary | State |
|---|---|---|---|
| Agent Server API and WebSocket transport | Reuse as a candidate interface | MediaHub ingress, identity, capability grants, route policy and lifecycle | BLOCKED |
| Session-key authentication | Reuse as downstream server auth | Accepted issuer, audience/scope binding, revocation, replay and audit | BLOCKED |
| Workspace cookie/static serving | Reuse only if required by approved UX | Cookie security, tenant ownership, origin/CORS and data classification | REVIEW REQUIRED |
| Container workspace abstraction | Reuse as candidate executor wrapper | Target image pin, mounts, privilege, egress, resource limits and cleanup proof | TARGET-GATED |
| Warm-pool per-user initialization | Potentially reuse behind trusted orchestrator | Strictly typed allowlisted init envelope and credential separation | BLOCKED |
| Path traversal containment | Existing source control | Independent review of all access-control and symlink/ownership assumptions | SOURCE REVIEW ONLY |

No new MediaHub queue, agent registry, provider router or canonical evidence store is justified by these findings. The preferred design remains a narrow adapter around upstream capabilities.

## 4. Cross-contract implications

- Task envelope v0.2, agent registry v0.2 and evidence manifest v0.2 remain PROPOSED ONLY; their schema references and policy refs require immutable resolution.
- A0 issuer/ingress/lifecycle, lease/fencing/replay/cancellation semantics, MH-12 security, R-06 governance and the accepted execution-target manifest remain open.
- Personal Jarvis authoritative upstream identity remains unresolved; lookalike repositories remain provenance leads only.
- OpenHands remains a research candidate, NOT SELECTED, NOT ADMITTED, NOT QUALIFIED and NOT DEPLOYED.
- This source review establishes design constraints only. It does not establish effective runtime configuration, vulnerability exploitability, or qualification.

## 5. Required evidence before any future runtime proposal

1. Immutable image and dependency artifact digests with provenance/SBOM/license/advisory closure.
2. Accepted A0 issuer and ingress contract; independent authorization, expiry/revocation, replay, cancellation and lease/fencing semantics.
3. Exact accepted target manifest and verified network, host, workspace and mount boundaries.
4. Authenticated route matrix covering every REST/WebSocket, init, webhook and workspace-cookie path.
5. Cookie/CORS review including cross-origin behavior and conversation/tenant ownership.
6. Init payload schema and strict field allowlist; proof that task/model output cannot set credentials or privileged environment.
7. Egress, telemetry, secret storage, log redaction, retention and deletion controls.
8. Independent negative-path review and target-specific qualification under separate authorization.

## 6. Disposition

**Source review complete for the listed files; candidate admission remains blocked.** The principal result is a more precise boundary than the Wave 24 README-only finding: the reviewed entrypoint contains a conditional loopback default and authentication-aware bind selection, while workspace cookie serving and privileged warm-pool initialization remain separate high-value control surfaces. The source itself also preserves a warning-only path for explicit wildcard binding without session auth.

No tests, execution, installation, provider invocation, credential use, host/runtime inspection, infrastructure change, deployment or branch integration occurred.

Next: continue read-only source tracing for exact workspace-cookie minting/security attributes and the server's tool/execution configuration surface; preserve all runtime gates.
