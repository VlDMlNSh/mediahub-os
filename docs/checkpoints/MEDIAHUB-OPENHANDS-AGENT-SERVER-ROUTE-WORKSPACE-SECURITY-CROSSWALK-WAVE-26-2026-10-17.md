# MediaHub OS — OpenHands Agent Server Route and Workspace Security Crosswalk, Wave 26

- Date: 2026-10-17
- Status: SOURCE-ONLY REVIEW / CANDIDATE ONLY / RUNTIME ADMISSION BLOCKED
- Parent: [Wave 25 task/registry/evidence crosswalk](MEDIAHUB-OPENHANDS-TASK-REGISTRY-EVIDENCE-CONTRACT-CROSSWALK-WAVE-25-2026-10-17.md)
- Upstream repository: https://github.com/OpenHands/software-agent-sdk
- Immutable upstream revision: `6530325e9dd0ea1b6b4f1994d7dab52764cfc3f1`

## 1. Exact source files read

| Source | Blob SHA | Evidence scope |
|---|---|---|
| `openhands-agent-server/openhands/agent_server/init_router.py` | `aae09786c40388b371cc5060a90a9a67bfbf4f3d` | Deferred initialization, init authentication gate, per-user workspace and credentials attachment, CORS-origin updates |
| `openhands-agent-server/openhands/agent_server/middleware.py` | `d2c4edec9742fd8c287ef4e258acad33340bdb5a` | Default CORS and workspace-cookie CORS dispatch |
| `openhands-agent-server/openhands/agent_server/README.md` | `a64ff0840230ff5ae2d7c167c824048eaf72da9f` | Host default, optional session API key, configuration, workspace and deployment security notes |
| `openhands-workspace/openhands/workspace/agent_sandbox/workspace.py` | `4de732d3a3730aea6c48ec1eb83bf22f769e0b11` | Kubernetes Agent Sandbox claim lifecycle, remote server connection, port-forward and sandbox operations |

Source links:
- [Init router](https://github.com/OpenHands/software-agent-sdk/blob/6530325e9dd0ea1b6b4f1994d7dab52764cfc3f1/openhands-agent-server/openhands/agent_server/init_router.py)
- [CORS middleware](https://github.com/OpenHands/software-agent-sdk/blob/6530325e9dd0ea1b6b4f1994d7dab52764cfc3f1/openhands-agent-server/openhands/agent_server/middleware.py)
- [Agent Server README](https://github.com/OpenHands/software-agent-sdk/blob/6530325e9dd0ea1b6b4f1994d7dab52764cfc3f1/openhands-agent-server/openhands/agent_server/README.md)
- [Agent Sandbox workspace](https://github.com/OpenHands/software-agent-sdk/blob/6530325e9dd0ea1b6b4f1994d7dab52764cfc3f1/openhands-workspace/openhands/workspace/agent_sandbox/workspace.py)

## 2. Findings bound to inspected source

1. The Agent Server README documents `0.0.0.0:8000` as the default bind, an optional `SESSION_API_KEY`, and broad access to its configured workspace. A safe MediaHub adapter therefore requires explicit network placement, authentication enforcement, and OS/workspace isolation; defaults alone do not establish these controls.
2. The init router includes a dedicated authentication gate for `POST /api/init`, while its status endpoint is intentionally public for warm-pool readiness. This is a lifecycle-specific mechanism, not evidence of MediaHub A0 issuer, audience, expiry, revocation, lease fencing, replay prevention, cancellation, or recovery conformance.
3. The middleware applies a separate CORS policy to workspace-cookie routes, including a regex that echoes HTTP(S) origins. CORS is browser policy, not caller authentication or network access control. The workspace-cookie surface requires a separately reviewed origin/session/CSRF threat model before hosted exposure.
4. The Agent Sandbox workspace implementation claims a sandbox from a Kubernetes warm pool, initializes a remote workspace, and can establish a local port-forward. This is a reusable isolation integration point, but the inspected adapter alone does not prove cluster policy, pod security, identity binding, egress policy, lease fencing, cleanup guarantees, or target-specific confinement.
5. Source evidence supports a narrow adapter hypothesis only. MediaHub must retain canonical task admission, identity and policy authority, credential-reference resolution, accepted target selection, and canonical evidence disposition.

## 3. Contract crosswalk and disposition

| MediaHub gate | Source evidence | Gap / disposition |
|---|---|---|
| A0 issuer, audience, expiry, revocation | Init auth gate and optional server key | OPEN: map accepted issuer/lifecycle contract to every REST/WebSocket route |
| Lease, fencing, replay, cancellation, recovery | Deferred init and sandbox claim lifecycle | OPEN: no source evidence here establishes MediaHub-compatible fencing or cancellation semantics |
| MH-12 least-privilege capability enforcement | Workspace/tool access and remote execution | OPEN: require explicit capability-to-tool/filesystem/network enforcement evidence |
| R-06 audit/privacy | README telemetry and server behavior documentation | OPEN: independently verify payload allowlist, retention, redaction and data-flow boundaries |
| Target manifest | Kubernetes namespace, warm pool, host/port, local port-forward configuration | UNKNOWN: no accepted inventory binding runner identity, workspace boundary, network policy, storage and cleanup target |
| Browser/session surface | Workspace-cookie CORS branch | OPEN: review cookie scope, origin trust, CSRF, WebSocket auth and reverse-proxy behavior |
| Independent qualification | Source files only | OPEN: no tests, deployment, runtime inspection or qualification performed in this pass |

## 4. Decision

Retain OpenHands Software Agent SDK as a source-pinned candidate for an engineering-task execution subsystem. The source contains useful primitives, but its server and workspace abstractions are not a drop-in implementation of MediaHub contracts. Preserve the reuse-first direction: build only a narrow MediaHub-owned adapter if and when accepted A0/MH-12/R-06 contracts and the target manifest establish the required controls.

## 5. Next bounded steps

1. Reconcile the actual route table, WebSocket authentication and workspace/file-serving routes against the accepted A0 issuer/lifecycle contract.
2. Close the accepted target manifest and identify the authoritative runner, workspace, network, storage and cleanup boundaries.
3. Complete R-06 privacy/audit and MH-12 capability-control mapping.
4. Keep implementation, tests, provider dispatch, installation, host/runtime inspection, qualification and deployment gated by their separate authorizations.

## 6. Verification boundary

This pass read source files at the immutable upstream revision and recorded their returned blob SHAs. It did not run code or tests, install packages, access credentials, call providers, inspect a live host, alter infrastructure, deploy, or qualify a runtime. The findings are source review, not implementation or acceptance evidence.
