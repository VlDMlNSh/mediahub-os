# MediaHub OS — Jarvis Source Pin and Capability Crosswalk, Wave 24

- Date: 2026-10-17
- ID: MH-JARVIS-SOURCE-CROSSWALK-24
- Contour: A — Developer Fabric
- Status: READ-ONLY SOURCE INTAKE / CANDIDATE ONLY / QUALIFICATION OPEN
- Reuse-first gate: [Wave 23](MEDIAHUB-REUSE-FIRST-UPSTREAM-DISCOVERY-GATE-WAVE-23-2026-10-17.md)
- Canonical project map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md

## 1. Purpose and result

Apply the Wave 23 Component Discovery Record (CDR) to the two Jarvis candidates. This pass reads public GitHub source and MediaHub contracts only. It performs no clone, install, execution, test, qualification, provider call, credential use, host/runtime inspection, infrastructure change or deployment.

Outcome:
- OpenHands Software Agent SDK has a source-pinned candidate snapshot suitable for further contract mapping, not production admission.
- The exact canonical upstream identity for Personal Jarvis remains unresolved. Public repositories with similar names contain materially different version/license claims, so no fork or mirror is promoted as the authoritative upstream.
- No candidate is selected for integration. The three-server topology and MediaHub authority boundaries remain unchanged.

## 2. OpenHands Software Agent SDK — source-pinned candidate

- Repository: https://github.com/OpenHands/software-agent-sdk
- Default branch observed: `main`
- Reviewed commit pin: `6530325e9dd0ea1b6b4f1994d7dab52764cfc3f1`
- Commit URL: https://github.com/OpenHands/software-agent-sdk/commit/6530325e9dd0ea1b6b4f1994d7dab52764cfc3f1
- Commit date observed: 2026-10-16T16:04:36Z
- Commit message: marketplace loads skills from registered repositories without a manifest.
- Recent release commit observed in preceding history: `5fa4dea24c52fe3ac53fa4e3e67a1376b72189e2`, release v1.55.1 (2026-10-16).
- License source: `LICENSE`, blob SHA `b0bd86a6335a564bd3766666bebbf014fd6a8013`, MIT.
- Workspace manifest: `pyproject.toml`, blob SHA `2da88a5a9f278947e6c6978ff0e0c398f27515d5`.
- README blob SHA `386dc8945133cb51969192b0b29c8396719cbff6`.
- Public README describes Python, TypeScript and REST APIs for coding agents. The workspace includes `openhands-sdk`, `openhands-tools`, `openhands-workspace` and `openhands-agent-server`.

### Security and integration constraints

The source at the pinned commit documents that the Agent Server:
- binds to `0.0.0.0` by default;
- has full access to the configured workspace directory;
- stores conversations, events and workspace files locally;
- requires deliberate CORS/network restriction and workspace isolation for a deployment.

These are direct upstream documentation claims, not independent security qualification. The default network binding and workspace access make a direct, unmodified deployment unsuitable until the target-specific ingress, authentication, workspace containment, secret handling, audit and recovery controls are source-bound and independently qualified.

### Proposed subsystem mapping

| Upstream module | Potential MediaHub role | Contract/authority boundary | Disposition |
|---|---|---|---|
| SDK / agent runtime | Execute a bounded engineering task | Input must derive from accepted MediaHub task envelope; outputs are untrusted evidence until reviewed | Candidate |
| Tools | Capability-limited task tools | Allowlist and operation scope derive from MediaHub policy/A0; no implicit tool authority | Candidate; permissions review open |
| Workspace | Isolated task worktree/files | Must bind to an accepted target/workspace lease; no access to canonical product state or unrelated user data | Target compatibility open |
| Agent Server / REST / WebSocket | Optional remote execution interface | No direct public ingress; A0 issuer, authentication, network route, session scope and audit remain MediaHub-controlled | Security gate open |
| Conversation/event persistence | Execution-local state | Must not become MediaHub canonical task, product or provenance state | Adapter/provenance design open |

### Admission blockers

1. Accepted A0 issuer, ingress, lease, revocation and replay lifecycle remain open.
2. MH-12 capability issuer semantics and R-06 audit/privacy disposition remain open.
3. The authoritative physical target manifest is UNKNOWN/BLOCKED; the reviewed target-reconciliation source says historical Mac mini examples are context only and do not qualify current targets.
4. The task-envelope v0.2 and agent-registry v0.2 documents explicitly label their schemas PROPOSED ONLY and require accepted A0/MH-12/R-06, provider/egress policy and independent review before runtime use.
5. Source review alone supplies no SBOM, vulnerability disposition, functional/negative/degraded-mode tests, performance data, recovery/rollback evidence or independent qualification.

## 3. Personal Jarvis — upstream identity and provenance discrepancy

The previous candidate intake referenced `PersonalJarvis/PersonalJarvis` and linked its README, architecture and licensing pages. Direct GitHub connector reads for that exact repository/path did not return readable content, and exact repository search did not resolve it as a repository record in this pass.

Two public lookalikes were inspected as provenance checks, not as approved upstreams:

- `vanderstark/personaljarvis`, default branch `master`, current source commit observed `8b10dd39297197325ee88af19c7a3f658d4793d4`, whose message is “Initial commit from personaljarvis clone”. Its README advertises version 2.9.0 and Apache-2.0; its pyproject and requirements are large, and the project classifies itself as Beta. This single clone-origin commit does not establish authoritative upstream provenance.
- `Ruben884-oos/PersonalJarvis`, default branch `main`, latest commit observed `2259ed0b7731fdd4730176d9c75f5f9d4dc7b343`, message “release: v1.0.10 — headless one-line install fix”, dated 2026-07-16. Its README points back to `PersonalJarvis/PersonalJarvis`, but its own source advertises version 1.0.10 and MIT. README blob SHA `485cda926523ab7b32108ea8de3dcad2a84b43df`; LICENSE blob SHA `d2735afd11d83a1dd03a4a56e6038bb728e12d4b`; pyproject blob SHA `15fc8fb26d64cf9149176d9c75f5f9d4dcdb4f5`.

These materially different version/license states are a source-identity and provenance discrepancy. They may represent forks, mirrors, or separate snapshots; the reviewed evidence does not establish the relationship conclusively. Therefore:
- do not pin either lookalike as canonical Personal Jarvis;
- do not infer the Apache-2.0 license for every source snapshot;
- require a reachable authoritative repository URL, immutable commit/release, matching LICENSE/NOTICE and dependency inventory before admission.

## 4. Reuse-first CDR disposition

| Candidate | Discovery result | Source pin | License/provenance | Capability fit | Decision |
|---|---|---|---|---|---|
| OpenHands SDK | Official repository found | Commit `6530325e9dd0ea1b6b4f1994d7dab52764cfc3f1` | MIT source read; provenance record started | Strong candidate for coding-agent execution/workspaces | Continue read-only contract/security crosswalk; not selected |
| Personal Jarvis | Canonical repository identity unresolved by this pass; two lookalikes differ | No canonical pin | Conflicting public snapshots: Apache-2.0/version 2.9.0 vs MIT/version 1.0.10 | Potential desktop/voice/personal-agent UX | Hold candidate pending authoritative source identity |

## 5. MediaHub authority invariants

Any eventual integration must preserve:
- MediaHub-owned mission and task policy;
- ASTRA A0 as a bounded engineering control-plane interface, subject to its accepted contract;
- MediaHub task/agent/evidence/provenance contracts as the canonical records;
- Product State Authority as the only canonical product-state mutation authority;
- external execution output as untrusted until validation and promotion;
- existing three-server topology: Mac mini 2018/macOS, Mac mini 2011/Linux and remote video server. Physical target identity remains governed by the accepted target manifest, currently unresolved.

No third-party internal database, task queue, workspace state or conversation history becomes canonical MediaHub state.

## 6. Next bounded step

1. Continue read-only mapping of the pinned OpenHands SDK modules to the task-envelope v0.2, agent-registry v0.2, evidence-manifest v0.2 and accepted A0/MH-12/R-06 requirements.
2. Record a complete source/dependency inventory and identify which security controls can be configured versus which require a MediaHub adapter or upstream contribution.
3. Resolve the canonical Personal Jarvis upstream identity and immutable source pin before deeper source intake.
4. Keep runtime use blocked until the accepted target manifest and A0/MH-12/R-06 gates are closed and separate execution/qualification authorization is granted.

Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
