# Wave 528 — Runner 2 design and behavioral test contract

Date: 2026-11-06  
Status: **DESIGN CONTRACT PROPOSED / NOT IMPLEMENTED / NO AGENT DISPATCH / NO PROVIDER CALL / CONTOUR A NOT ACCEPTED**

## 1. Immutable target and scope

- Repository: https://github.com/VlDMlNSh/mediahub-os
- Runtime/source target SHA: `41c13e1c2b17ac48dc51c9963a9cda140f79ddb0`
- Canonical documentation branch HEAD: `d9a289b9113f7567711b641a7017eb814d6c259d`
- Parent documentation proposal: PR [#633](https://github.com/VlDMlNSh/mediahub-os/pull/633), HEAD `bca5536189580ceafaa22caec28672e04b07c8aa`
- This proposal branch is stacked on #633 and does not change the canonical documentation branch.
- Main controller blob: `0a1246f6755020faf8b7e48d07bfff790bbaece3`
- Gemini child workflow blobs: `155a02159912ca371e6f826c51325ca269857aad`, `fff1820a6b97d379b23674f36bd62227b7d4dec2`, `781df56e8aa7c75ba453c08378611857862b2e44`
- Policy-only router blob: `e249333c1c0ce6c1c586a5f498dbfd3979418f6e`
- Existing selector policy test blob: `fcfc37d046a9670c793c7282f9c0c9369d6fdae1`

**Objective:** specify one GitHub-hosted Ubuntu job per Gemini batch, with three isolated agent containers on that same ephemeral runner, while preserving the existing signed controller as the sole dispatch authority.

**Out of scope:** implementation, dependency adoption, live model/provider calls, reading secret values or secret inventory, runner provisioning, dispatch, merge, deployment, qualification and acceptance.

## 2. Current source facts

1. The main controller dispatches three independent child workflows. Each child workflow currently declares its own `ubuntu-latest` execution job. This is three runner allocations, not one co-located Runner 2.
2. The controller owns the signed task envelope and GitHub transport. It must remain the only dispatch authority; agent containers are workers, not controllers.
3. The existing router file explicitly declares `mode: policy_only`, `direct_provider_api_calls: false`, `paid_fallback: false` and `unknown_route_behavior: fail_closed`. It is a policy contract, not a runtime key selector or dispatcher.
4. No provider-key registry, secret values, Actions secret inventory or account metadata were inspected in this pass. Source-level role credential bindings do not prove secret presence, account ownership, quota independence or runtime use.
5. PR #625 remains an unaccepted two-runner topology proposal at `01efb5e6264b4cb84aee1d9c0c162be77cd1f264`: zero exact-head workflow runs, zero formal reviews and zero inline review threads. It is not canonical architecture.
6. PR #633 remains OPEN/DRAFT/UNMERGED at `bca5536189580ceafaa22caec28672e04b07c8aa`; exact-head workflow runs, formal reviews and review threads are all absent. Its documentation is proposal evidence only.

## 3. Reuse-first component assessment

### Google Gemini CLI GitHub Action

- Upstream: https://github.com/google-github-actions/run-gemini-cli
- Inspected upstream main commit: `387c8ddb7a72078825da941758b811b9153c71e8`
- Inspected `action.yml` blob: `35af14fe781b3e02ecd20233897ec743b731bbd2`
- The Action is a composite action. It installs and invokes Gemini CLI in the current GitHub Actions job context and exposes model-authentication inputs.
- It does not itself provide three separately isolated containers on one runner. Calling the composite action three times in one job would not create three isolation boundaries; using three jobs would return to three runner allocations.
- Disposition: **REUSE CANDIDATE FOR CLI INSTALL/AUTH REFERENCE ONLY; NOT A DROP-IN RUNNER 2 ISOLATION SOLUTION; NOT ADOPTED.** A pinned CLI-in-container proof-of-fit is still required.

### GitHub Agentic Workflows / AWF

- Upstream: https://github.com/github/gh-aw
- Inspected main commit: `3decf5979cd1661c7cbd71b6701ef7c150ec6e9c`
- Inspected README blob: `4e0667b04eb87108ea18aa995aecc7c108c61d91`
- Inspected runtime guide blob: `0e437cecb0ffd2ff7e6194c4322d6c7260b9c2e3`
- Inspected sandbox guide blob: `56b3d57f136b5d460ab315ec671dd2193a681278`
- Relevant reusable patterns: AWF container isolation, domain-allowlisted egress, separation of agent execution from safe-output writes, and an API proxy that can retain model credentials outside the agent container.
- Compatibility cautions: gh-aw is a complete workflow compiler/orchestration framework, not a small container library. Its sandbox documentation describes host paths and environment handling that require exact credential-exclusion verification. Its security validation documentation explicitly distinguishes a targeted structure check from a complete current revalidation.
- Disposition: **SECURITY PATTERN / AWF REUSE CANDIDATE ONLY.** Do not replace the MediaHub controller, import a second orchestration authority, or add gh-aw wholesale. Pin and qualify any AWF binary/image independently before adoption.

### OpenHands Docker sandbox

- Upstream: https://github.com/OpenHands/docs
- Inspected main commit and Docker sandbox blob: `fe4d8345b1b994a41d954c15d73bce4dade273bd`
- The documentation describes a sandbox designed for OpenHands' own runtime. Its host-network option uses shared fixed ports and is documented for one sandbox at a time; it is not a generic three-agent Runner 2 coordinator.
- Disposition: **NOT SELECTED.** Do not add OpenHands solely to obtain containers.

## 4. Proposed Runner 2 topology

One controller-owned child workflow is dispatched for the batch. That workflow starts one ephemeral GitHub-hosted Ubuntu job and acts as a trusted coordinator. It creates exactly three isolated agent containers/workspaces for roles A1, A2 and A3, all bound to one immutable target SHA.

The coordinator is trusted infrastructure; the agent containers are untrusted execution domains. The design must not weaken the existing controller HMAC, caller, target-SHA, admission, replay or monitoring contracts.

### Required boundaries

1. **One host:** one GitHub-hosted Ubuntu job per batch; record the runner/job identity and resource profile. Do not claim a persistent VM or reserved physical host.
2. **Three workspaces:** unique workspace, temporary directory, container identity and output location per role. No shared writable volume between agents.
3. **Controller secrets:** GitHub transport token and dispatch HMAC material remain host-coordinator-only. Never mount them, pass them through environment variables, or copy them into agent containers, logs or artifacts.
4. **GitHub authority:** agent containers receive no repository write token. Prefer repository snapshot/read-only input and patch/artifact output. Any GitHub write is performed by a separate trusted, schema-validating coordinator step after output validation.
5. **Provider credentials:** each agent may receive only its explicitly assigned provider credential or a narrowly scoped credential-proxy endpoint. No sibling credential, controller credential or broad inherited environment. Credential-to-account/quota-domain mapping must be verified independently; key names or suffixes are not proof of account separation.
6. **No implicit fallback:** 401/403, 402, 429, unknown model, unavailable proxy or quota-store failure must fail closed or apply a documented cooldown. Never silently switch accounts, providers, paid routes or unknown destinations.
7. **Container hardening:** non-root user; read-only root filesystem where compatible; bounded writable workspace/tmpfs; dropped Linux capabilities; no privileged mode; no host PID/IPC/network; no Docker socket; no host home, credential directories or unrestricted filesystem mounts.
8. **Network:** per-agent egress must be mediated by an independently qualified allowlist proxy/firewall. Deny direct arbitrary egress and cross-agent traffic. Only the minimum model endpoint, artifact relay and explicitly required read-only endpoints may be reachable.
9. **Resource admission:** enforce CPU, memory, PID, disk, runtime and concurrency limits per agent and aggregate batch. Reserve host headroom for the runner and coordinator. Reject admission when measured capacity is insufficient.
10. **Lifecycle:** bounded startup, heartbeat, timeout, cancellation, cleanup and partial-failure handling. No automatic redispatch on ambiguous outcomes without a durable idempotency receipt.
11. **Provenance:** bind each role result to batch ID, task ID, role, immutable target SHA, controller run ID, child job ID, container ID, terminal status, artifact digest and source revision. Agent output is untrusted until validated.
12. **Observability:** record policy decisions, egress allow/deny events, resource usage, exit codes and artifact digests without recording credentials, authorization headers or raw secret-bearing environment values.

### Credential-proxy compatibility gate

The GH-AW architecture demonstrates the value of keeping model credentials in a trusted proxy, but this pass did not establish that the current Gemini CLI supports the required per-agent proxy endpoint and authentication contract. Do not assume that a generic proxy or environment variable is compatible. Prove this with synthetic credentials and a non-provider local HTTP fixture before any provider-backed run.

If proxy compatibility cannot be proven, stop and return an explicit design decision. Do not weaken isolation by sharing credentials or passing controller tokens to agents.

## 5. Required behavioral test contract

All tests in the first implementation increment must be deterministic and use synthetic credentials/local fixtures only. No model endpoint, real provider credential or external account is permitted.

| ID | Test | Required result |
|---|---|---|
| R2-01 | Valid signed batch envelope with three roles and one target SHA | Exactly one coordinator job admits exactly three role containers |
| R2-02 | Invalid HMAC, malformed envelope, wrong issuer, wrong role or target mismatch | Reject before container creation |
| R2-03 | Modified task payload or signature | Reject; no agent starts |
| R2-04 | Duplicate batch/dispatch ID and ambiguous retry | One durable claim; no duplicate execution |
| R2-05 | Agent A1 reads A2/A3 workspace or output path | Denied; no cross-agent writable mount |
| R2-06 | Agent reads controller token/HMAC or sibling credential | No such material exists in container environment, filesystem or mounts |
| R2-07 | Agent accesses Docker socket, host home or host credential path | Path/device absent and access denied |
| R2-08 | Agent attempts privileged mode, host network/PID/IPC or capability escalation | Configuration rejected or runtime denied |
| R2-09 | Agent accesses a non-allowlisted external domain or another agent | Network denied and auditable |
| R2-10 | Agent accesses only the approved local model-proxy fixture | Request succeeds; credential remains in proxy, not agent |
| R2-11 | CPU, memory, PID, disk, wall-clock or concurrency limit exceeded | Agent is bounded/terminated; other roles remain isolated |
| R2-12 | Cancellation, runner interruption, partial startup and partial completion | Deterministic cleanup and explicit terminal state; no false success |
| R2-13 | Agent writes outside its workspace or uses symlink/path traversal | Write rejected; host and sibling workspaces unchanged |
| R2-14 | Logs, summaries and artifacts are scanned for synthetic credential canaries | Zero credential leakage |
| R2-15 | Artifact is altered after completion or bound to another target SHA | Digest/provenance verification fails |
| R2-16 | One role fails while others succeed | Results remain role-scoped; batch summary reports partial failure, never aggregate PASS |
| R2-17 | Runner capacity is below declared admission envelope | Batch rejected before model execution |
| R2-18 | Cleanup runs after success, failure, timeout and cancellation | All containers, networks, mounts and temporary credentials removed |

### Acceptance gates before implementation

- Independent A3 review of this design and threat model.
- Source-pinned AWF/Gemini CLI compatibility proof and license/security review.
- A no-secret runner harness that passes R2-01…R2-18 or explicitly marks unsupported tests BLOCKED.
- Exact-head required CI and branch governance evidence.
- Secret/variable presence and scope metadata verified without reading values.
- Trusted-main no-secret controller probe succeeds.
- No model/provider dispatch until all existing controller admission gates and the new Runner 2 gates pass.

## 6. Current disposition and next step

- Runner 2: **DESIGN CONTRACT PROPOSED / NOT IMPLEMENTED**.
- PR #625 topology: **OPEN PROPOSAL / NOT ACCEPTED**.
- PR #633 Wave 527: **OPEN DRAFT / EXACT-HEAD CI NOT VERIFIED / INDEPENDENT REVIEW NOT VERIFIED**.
- Gemini Agents 1/2/3: **NOT RUN**; no controller run ID or child job IDs exist for this pass.
- Provider calls, secret-value access, runner provisioning, deployment, merge, qualification and Contour A acceptance: **NOT RUN**.
- No provider-key inventory or account list was inspected. Account/quota-domain mapping remains **NOT VERIFIED**.
- Master Roadmap was reviewed; no priority or accepted architecture changed, so it was not modified.

**Next bounded step:** obtain an independent A3 review of this design contract. After review, implement only the synthetic no-secret container/isolation harness on a dedicated code branch. Do not dispatch Gemini or invoke providers as part of that implementation.

## 7. Evidence and canonical navigation

- Parent proposal: https://github.com/VlDMlNSh/mediahub-os/pull/633
- Two-runner topology proposal: https://github.com/VlDMlNSh/mediahub-os/pull/625
- Issue #301: https://github.com/VlDMlNSh/mediahub-os/issues/301
- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
- Bootstrap: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CONTEXT-BOOTSTRAP-INSTRUCTION.md
- Checkpoint: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/checkpoints/mediahub-next-continuation-checkpoint-2026-10-12-current.md
- Master Roadmap: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/checkpoints/MEDIAHUB-MASTER-DEVELOPMENT-ROADMAP-1.0.md
