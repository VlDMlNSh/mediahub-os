# MediaHub OS — OpenHands Agent Server Admission Review, Wave 40

- Date: 2026-10-17
- ID: MH-OPENHANDS-SERVER-REVIEW-40
- Contour: A — Developer Fabric
- Status: **SOURCE-ONLY SECURITY / ADMISSION REVIEW / CANDIDATE BLOCKED / RUNTIME-UNVERIFIED**
- Upstream repository: https://github.com/OpenHands/software-agent-sdk
- Immutable source ref: `6530325e9dd0ea1b6b4f1994d7dab52764cfc3f1`
- Upstream commit tree: `54c039b002905c0c7c4db7c9f8d7a6c7cd5b46c4`
- Upstream commit signature: GitHub commit API reports `verified: true`; this is source-commit signature evidence, not artifact provenance or code-safety approval.
- Project navigation: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md

## 1. Scope and method

Read exact source files at the immutable upstream commit, focusing on Agent Server authentication, route boundaries, workspace/tool execution, Docker runtime configuration, cleanup hooks, telemetry and package metadata. Compared these source observations with the existing MediaHub Component Admission Crosswalk, A0/MH-12/R-06 gates, and the Contour A task-scoped worker boundary.

This pass used GitHub source reads only. No package download, installation, dependency resolution, test, scan, provider/model call, credential use, host/runtime inspection, qualification, deployment or infrastructure change occurred.

## 2. Exact source ledger

| Upstream file | Blob SHA | Review use |
|---|---|---|
| Commit `6530325e9dd0ea1b6b4f1994d7dab52764cfc3f1` | Commit API, verified signature | Immutable source identity; commit date 2026-10-16T16:04:36Z |
| `openhands-sdk/pyproject.toml` | `160610fcba9b379a10340f16ab77c3bf504f2609` | Package version 1.55.1; Python `>=3.12`; dependency ranges |
| `LICENSE` | `b0bd86a6335a564bd3766666bebbf014fd6a8013` | Repository license text is MIT; transitive notices remain open |
| `openhands-agent-server/openhands/agent_server/__main__.py` | `226f43dca5a2d1799c84199bbd85bd07bfc98339` | Bind-host decision and unauthenticated wildcard warning |
| `openhands-agent-server/openhands/agent_server/dependencies.py` | `d1d2a6aece2056adc15824aed6cdccc4c3c33ead` | REST/session authentication semantics |
| `openhands-agent-server/openhands/agent_server/api.py` | `1916fd4b00e798e27f85f37db1e634bbef6a48c2` | Route grouping, REST auth dependencies and initialization boundary |
| `openhands-agent-server/openhands/agent_server/sockets.py` | `33d7a4b1666e9cdcf004b157470e9be16cdfe693` | WebSocket authentication methods |
| `openhands-agent-server/openhands/agent_server/config.py` | `a5830083eb110eadc6262287c5242f50e2296b66` | Local runtime default, optional session keys, resource and telemetry configuration |
| `openhands-agent-server/openhands/agent_server/docker_runtime/registry.py` | `27803eeab90bf50b900ed7c238b083e855aba3d9` | Docker launch controls, per-conversation mounts and cleanup lifecycle |
| `openhands-agent-server/openhands/agent_server/docker_runtime/routers.py` | `fa6eb7f58f6e5281cff2f0b358c6abcd2aa0e2d7` | Docker-backed conversation and workspace routing |
| `openhands-agent-server/openhands/agent_server/workspace_router.py` | `e38f5f99e6efb8b464c31c8e06fcdf4e06ce064c` | Workspace path resolution and static-file boundary |
| `openhands-agent-server/openhands/agent_server/telemetry/policy.py` | `64e3b567352d4b3fef36327b5d8c5d8b30613403` | Telemetry consent and exporter policy |
| `openhands-agent-server/openhands/agent_server/telemetry/sanitizer.py` | `3f56a1b00dab0643f2f2bda925eba9386e823854` | Allowlisted telemetry sanitization |
| `openhands-agent-server/openhands/agent_server/README.md` | `a64ff0840230ff5ae2d7c167c824048eaf72da9f` | Deployment guidance and documented security/telemetry behavior |

## 3. Findings

### OH-40-01 — Agent Server authentication is optional by configuration

The configuration describes an empty `session_api_keys` list as an unsecured server. REST authentication accepts requests when the configured key list is empty; WebSocket authentication likewise accepts connections when no session key is configured. The CLI defaults to loopback when no session key exists. An explicit wildcard bind without a key is permitted with a warning.

**Disposition:** deployment admission must require a non-empty scoped session-key set, explicit bind address, TLS/reverse-proxy trust boundary, restricted inbound access and independent checks of every REST, WebSocket, initialization and bridge route. The CLI warning is a guardrail, not a policy enforcement substitute. No live server behavior was tested.

### OH-40-02 — Upstream README and executable bind defaults conflict

The Agent Server README says the default host is `0.0.0.0`; the pinned `__main__.py` chooses `127.0.0.1` when no session API key is configured and `0.0.0.0` when authentication is configured, unless an explicit host overrides it.

**Disposition:** treat the exact entrypoint code as the source observation for this revision and record the documentation discrepancy as upstream drift. A MediaHub target manifest must specify host, port, reverse proxy, TLS, network ACLs and required authentication explicitly; avoid reliance on prose defaults.

### OH-40-03 — Local execution is the default and is not an isolation boundary

The configuration defaults `conversation_runtime` to `local`. The README states that local workspaces and the configured workspace filesystem are accessible to the server process, and explicitly says backend subprocesses are not OS-isolated. The SDK README also describes direct local-machine workspaces.

**Disposition:** local runtime is unsuitable for untrusted autonomous tasks under the current MediaHub admission boundary. Keep it blocked unless an explicitly accepted task class and filesystem/process policy proves it appropriate. Prefer a separately qualified isolated worker profile for untrusted tasks.

### OH-40-04 — Docker mode provides useful controls, but network egress remains unbounded by the inspected launch command

The Docker launch code applies a non-root UID/GID, `--cap-drop ALL`, `no-new-privileges`, core-dump restriction, memory/CPU/PID limits, per-conversation workspace/persistence mounts, and a host port published on `127.0.0.1`. It adds `host.docker.internal:host-gateway`. The inspected `docker run` command contains no explicit network-disable flag or destination allowlist.

**Disposition:** these controls are positive source evidence for a Docker-backed runtime, but they do not establish network isolation or destination control. Admission requires a source- and target-bound egress policy, host-gateway exposure review, image digest pin, mount review, resource envelope, cleanup proof and exact-target qualification. Docker mode is optional configuration, not the default.

### OH-40-05 — Browser, shell, file and Git capabilities require task-level mediation

The server exposes shell execution and multiple filesystem, Git, tool, MCP, plugin, provider and workspace routes. Browser capability defaults to enabled in configuration. These are broad worker capabilities whose safety depends on the selected runtime, authenticated route, task policy and target environment.

**Disposition:** a MediaHub adapter must admit only an explicit capability intersection: task grant ∩ agent profile ∩ allowed paths ∩ data class ∩ tool/effect allowlist ∩ target policy. MCP is an interface protocol and grants no authority. A worker must return artifacts and evidence; it must not own ASTRA queue/lease state, product State Authority, policy decisions, merge/release or qualification promotion.

### OH-40-06 — Telemetry has a disabled-by-default product-analytics exporter, plus separate observability channels

The telemetry policy defaults the product-analytics exporter to `none` and requires effective consent before delivery. The README distinguishes this from LLM completion logging, which can retain full prompts/responses/provider payloads locally, and Laminar/OpenTelemetry tracing, which may send traces to a separately configured backend. The sanitizer limits the product-analytics event shape.

**Disposition:** R-06 remains a hard gate. The target profile must specify completion logging and tracing defaults, egress destinations, consent authority, minimal event fields, access, retention/deletion, integrity and outage behavior. A claim that “telemetry is off” must name the channel and exact configuration.

### OH-40-07 — Runtime and dependency evidence remains incomplete

The pinned source commit is signature-verified and the SDK metadata declares version 1.55.1 with Python `>=3.12`; repository license text is MIT. The Agent Server is a separate package with its own dependency/runtime surface. The `uv.lock` contents returned empty through the current connector, so its resolved dependency graph was not inspected. Exact distribution artifact digests, source-to-artifact binding, transitive SBOM/license/advisory closure and MediaHub target compatibility remain open.

**Disposition:** source pin and repository license alone are insufficient for admission. Obtain readable lock contents and exact distribution hashes through a reliable source, then complete the dependency and target-specific review under separate authorization.

### OH-40-08 — Cleanup routines exist in source, but cleanup effectiveness is unqualified

The Docker registry contains stale-container cleanup, idle-runtime handling, per-conversation runtime removal and storage reclamation paths. Static source presence does not establish correct behavior across process crash, host restart, cancellation races, credential revocation, partial deletion or failed cleanup.

**Disposition:** define lifecycle and cleanup acceptance criteria with A0: cancellation, lease loss, process termination, restart recovery, workspace retention/deletion, secret destruction, artifact provenance and audit reconciliation. Validate only under separately authorized test/qualification scope.

## 4. MediaHub admission matrix

| Gate | Source result | MediaHub disposition |
|---|---|---|
| Immutable source identity | Verified signed upstream commit `6530325e9dd0ea1b6b4f1994d7dab52764cfc3f1` | Source pin established for this review only |
| Package/artifact provenance | Exact wheel/sdist hashes and source-to-artifact binding remain open | BLOCKED |
| Dependency lock/SBOM/licenses/advisories | Lock body unavailable; complete transitive closure absent | BLOCKED |
| Python/OS/CPU target | SDK requires Python `>=3.12`; accepted MediaHub target remains unbound | BLOCKED |
| Authentication and route policy | Optional auth; separate REST, WebSocket, init and bridge surfaces | BLOCKED pending accepted target policy |
| Workspace/process isolation | Local default; Docker mode optional | BLOCKED pending isolated profile |
| Network egress and provider identity | Docker launch lacks explicit egress restriction in inspected command | BLOCKED |
| Telemetry/privacy/audit R-06 | Product analytics default-off; completion logging/tracing are separate channels | BLOCKED |
| A0 issuer, task admission, lease/cancel/recovery | External Jarvis→A0 contract and issuer lifecycle remain unaccepted | BLOCKED |
| Runtime cleanup/recovery | Source routines present; no target/runtime evidence | BLOCKED |
| Owner-approved capability gap and component admission | No admission decision found | CANDIDATE / NOT SELECTED / NOT ADMITTED |

## 5. Recommendation

Keep the OpenHands SDK and Agent Server as **RESEARCH CANDIDATE / NOT SELECTED / NOT ADMITTED / NOT READY FOR INSTALLATION OR RUNTIME EVALUATION**. Reuse the SDK only if the existing capability crosswalk establishes a concrete gap; treat Agent Server as a separate admission decision rather than an automatic SDK dependency. Any future evaluation must start with an accepted target profile, A0 issuer/lifecycle, MH-12 authorization, R-06 audit/privacy, task-scoped capability and network-egress controls.

This pass closes a source-review step only. It does not establish runtime safety, deployment readiness, qualification or acceptance.

## 6. Source links

- Upstream immutable commit: https://github.com/OpenHands/software-agent-sdk/commit/6530325e9dd0ea1b6b4f1994d7dab52764cfc3f1
- SDK metadata: https://github.com/OpenHands/software-agent-sdk/blob/6530325e9dd0ea1b6b4f1994d7dab52764cfc3f1/openhands-sdk/pyproject.toml
- Agent Server entrypoint: https://github.com/OpenHands/software-agent-sdk/blob/6530325e9dd0ea1b6b4f1994d7dab52764cfc3f1/openhands-agent-server/openhands/agent_server/__main__.py
- Agent Server auth dependencies: https://github.com/OpenHands/software-agent-sdk/blob/6530325e9dd0ea1b6b4f1994d7dab52764cfc3f1/openhands-agent-server/openhands/agent_server/dependencies.py
- Agent Server API routing: https://github.com/OpenHands/software-agent-sdk/blob/6530325e9dd0ea1b6b4f1994d7dab52764cfc3f1/openhands-agent-server/openhands/agent_server/api.py
- Docker runtime registry: https://github.com/OpenHands/software-agent-sdk/blob/6530325e9dd0ea1b6b4f1994d7dab52764cfc3f1/openhands-agent-server/openhands/agent_server/docker_runtime/registry.py
- Agent Server README: https://github.com/OpenHands/software-agent-sdk/blob/6530325e9dd0ea1b6b4f1994d7dab52764cfc3f1/openhands-agent-server/openhands/agent_server/README.md
