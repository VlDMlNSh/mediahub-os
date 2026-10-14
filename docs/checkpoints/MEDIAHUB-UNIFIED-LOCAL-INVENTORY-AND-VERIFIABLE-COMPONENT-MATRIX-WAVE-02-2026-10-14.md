# MediaHub OS — Unified Local Inventory and Verifiable Component Matrix, Wave 02

- Date: 2026-10-14
- Documentation ref: docs/mediahub-chat-tree-map-20261012
- Status: READ-ONLY DISCOVERY + DOCUMENTARY RECONCILIATION / NOT QUALIFIED / NOT ACCEPTED AS A NEW BASELINE
- Scope: all Desktop Commander nodes visible in this session; live inventory of two online nodes; selected project component/provider registries and cross-domain contracts.
- This artifact supplements but does not replace Functional Baseline 2.0, domain-primary contracts, the canonical component manifest, ASTRA governance, or the proposed unified traceability matrix.

## 1. Executive findings

1. Two nodes are online: mh-dev-02 (Linux) and Voktors-Mini.Dlink (macOS). mh-dev-01 is offline, last seen about 11 hours before this pass. Its live host inventory is NOT OBSERVED.
2. Both online checkouts report branch main, HEAD 1d45bbccbbbd27309c39cb9e9351bb291cdb47a8, and clean git status --short at the time of inspection. These local checkouts are at the observed main HEAD, not the divergent documentation branch.
3. Linux has active Astra GitHub Agent, GitHub Actions runner, Ollama, Docker daemon, Caddy, SentinelX Cloud Core and fail2ban processes/services in the bounded inventory. No running Docker containers were returned.
4. macOS has an active ops.local_autonomous_agent Python process, Astra GitHub Agent, runner processes and launchd labels including com.mediahub.astra.github-agent, com.mediahub.df3-llama and com.mediahub.df3-autonomous. Labels do not prove service identity, health or relationship to Alamo/Ollama.
5. Version observations: Linux Python 3.12.3, Node 22.23.3, Git 2.43.0, Ollama 0.34.4, Claude Code 2.1.291, Codex CLI 0.151.0. macOS Python 3.14.8, Node 22.23.3, Git 2.55.0, Ollama CLI 0.34.4 (server unavailable), Claude Code 2.1.282, Codex CLI 0.157.1, OmniRoute CLI 3.8.50.
6. Linux Ollama listed qwen2.5-coder:1.5b, qwen2.5-coder:3b, qwen2.5-coder:7b and claude-sonnet-4-6:latest. The last two displayed the same digest in the CLI output. This is a provenance/alias anomaly to investigate later, not proof of vendor or model identity. No inference was run.
7. Material registry mismatch: the distributed AI architecture describes a FreeLLMAPI cloud/provider route in its routing narrative, while profiles/agent-registry.json and profiles/providers/astra-gold-hybrid-agent-fabric.yaml classify FreeLLMAPI as local_gateway; provider fabric status is PENDING. Do not silently choose one meaning. Reconcile the pinned implementation/deployment boundary and data-egress semantics.
8. Provider registry has separate unorouter and claude/OmniRoute references; the Claude record points to gateway omniroute and credential reference OMNIROUTE_API_KEY. Similar names are not interchangeable. No credentials were read.
9. The unified deployment contract and unified traceability matrix are PROPOSED / NOT ACCEPTED / NOT FROZEN. This inventory does not elevate them to normative status.

## 2. Inventory coverage and method

| Target | Availability | Coverage | Limitation |
|---|---|---|---|
| mh-dev-02 Linux | Online | Selected processes/services, CLI paths/versions, repository tree, Git branch/HEAD/status, read-only Ollama tag listing | Not every package, process, port, image, endpoint, service definition or worktree was examined. |
| Voktors-Mini.Dlink macOS | Online | Selected processes, launchd labels, CLI paths/versions, repository tree, Git branch/HEAD/status, Ollama availability check | No model inventory because Ollama server was unavailable; no provider called. |
| mh-dev-01 | Offline | Device registry metadata only | No live commands; cannot infer component presence/absence. |
| GitHub main | Available | HEAD, source contracts, component/provider registries, integration matrix | Declarations are not runtime evidence. |
| Documentation branch | Available | Map, checkpoint, roadmap and existing inventory/crosswalk records | Diverged from main; no integration performed. |

Only read-only commands were used. No tests, qualification workflows/scripts, provider/model inference, credentials, installations, configuration changes, deployment, migrations, merges, rebases or cherry-picks were performed.

## 3. Local node evidence ledger

### 3.1 mh-dev-02 (Linux)

| Item | Observation | Status |
|---|---|---|
| Git checkout | branch main; HEAD 1d45bbccbbbd27309c39cb9e9351bb291cdb47a8; clean short status | Observed at inventory time |
| Python / Node / Git | 3.12.3 / 22.23.3 / 2.43.0 | Version observed |
| Claude Code / Codex | 2.1.291 / 0.151.0 | CLI present; provider execution not tested |
| Ollama | 0.34.4; ollama.service active; ollama serve process observed | Local service present |
| Ollama model tags | Four tags listed in §1 | Inventory only; no inference/qualification |
| Astra GitHub Agent | python3 /home/mediahub/astra-work/astra_github_agent.py process | Process present |
| GitHub Actions runner | Runner service/listener process | Process present |
| Docker | daemon/containerd present; docker ps returned no running containers | Daemon present; no running containers observed |
| Caddy | caddy run with /etc/caddy/Caddyfile process | Process present; routes not inspected |
| SentinelX | sentinelx-cloud-core process observed | Process present; permissions/trust boundary not qualified |
| fail2ban | Service process observed | Process present |
| OmniRoute / FreeLLMAPI / FCC | No OmniRoute executable found by bounded lookup; no FCC command or FreeLLMAPI process/executable identified | Not found in bounded checks; not proof of global absence |

Three named Git worktree directories were observed on Linux: astra-gold-mh2-3, astra-gold-mh2-4 and astra-gold-mh2-b28. Their HEADs, dirtiness and lease ownership were not inspected.

### 3.2 Voktors-Mini.Dlink (macOS)

| Item | Observation | Status |
|---|---|---|
| Git checkout | branch main; HEAD 1d45bbccbbbd27309c39cb9e9351bb291cdb47a8; clean short status | Observed at inventory time |
| Python / Node / Git | 3.14.8 / 22.23.3 / 2.55.0 | Version observed |
| Claude Code / Codex | 2.1.282 / 0.157.1 | CLI present; provider execution not tested |
| OmniRoute | CLI at /Users/voktor/.local/npm/bin/omniroute; version 3.8.50 | CLI present; gateway connectivity not tested |
| Ollama | CLI 0.34.4; ollama list could not connect to server | CLI present; server unavailable |
| Astra GitHub Agent | Agent process and com.mediahub.astra.github-agent label observed | Process/label present |
| GitHub Actions runner | Runner process/label observed | Process present |
| Local autonomous agent | python -m ops.local_autonomous_agent process observed | Process present; role/permissions/output not inspected |
| DF3 services | com.mediahub.df3-llama and com.mediahub.df3-autonomous launchd labels observed | Labels only; function/health/routing unknown |
| FCC / FreeLLMAPI | No standalone FCC executable or FreeLLMAPI service/process found by bounded checks | Implementation/deployment mapping unresolved |

Six named Git worktree directories were observed on macOS: astra-gold-mac-025, astra-gold-mac-3, astra-gold-mac-4, astra-gold-mac-b28, astra-gold-recovery-20261011 and astra-nightly-recovery. Their HEADs, dirtiness and lease ownership were not inspected.

### 3.3 mh-dev-01 (offline)

Desktop Commander reported the node offline, last seen about 11 hours before this pass. The provider registry associates Codex and Cursor tooling with mh-dev-01 and marks activation/qualification pending; this is repository metadata, not live host proof. Status: NOT OBSERVED / BLOCKED BY OFFLINE NODE.

## 4. Unified component and authority matrix

Status vocabulary: TARGET = architecture intent; DECLARED = registry/source entry; OBSERVED = live local evidence; NOT PROVEN = required runtime/qualification evidence absent; BLOCKED = prerequisite/evidence gap. These states are not interchangeable.

| Component / domain | Intended role and authority boundary | GitHub declaration | Local observation | State / follow-up |
|---|---|---|---|---|
| MediaHub Product State Authority | Sole canonical product-state mutation authority | Unified contract + domain contracts | Not established by developer-node inventory | MUST REMAIN SOLE AUTHORITY; product runtime is outside this scan |
| ASTRA A0 | Owns ASTRA-internal queue/claim/lease/gate state; accepts bounded missions | ASTRA contracts/provider fabric | GitHub Agent process on both online nodes | Process present; authority correctness not qualified; preserve single-writer boundary |
| Jarvis control plane | Engineering orchestration; no product-state authority | Owner-accepted target framing D-03; unified draft remains proposed | No distinct Jarvis service identity proven | Target only; deployment not proven; draft control-plane contract next |
| Claude Code | Engineering client/agent surface | CLI/provider registries | Versioned CLI on both nodes | CLI present; actual provider route not tested |
| OmniRoute | Gateway/router for external provider path | Claude gateway with OMNIROUTE_API_KEY reference; NOT_PROVEN | CLI only on macOS, v3.8.50 | CLI present; route/auth/endpoint not tested |
| FreeLLMAPI | Provider/gateway route; cloud-vs-local semantics unclear across sources | local_gateway, status PENDING in provider fabric | No process/service identified on online nodes | Not proven; resolve classification conflict and deployment host |
| FCC | Required Claude Code integration/control layer | Architecture target; exact pinned implementation needed | No standalone fcc command identified | Runtime mapping unknown; inspect non-secret package/service metadata later |
| Ollama / Alamo | Local inference runtime / intended local endpoint | Ollama local model; Alamo is architecture service label | Linux service active; macOS CLI but no daemon; four Linux tags listed | Linux service discovered, not qualified; Alamo-to-Ollama identity unproven |
| Codex CLI | Local engineering tool | Registry has a candidate association with mh-dev-01 | CLI on both online nodes | Tool present; authorization/qualification separate |
| Astra GitHub Agent | Repository coordination/transport | Source and launch service definitions | Process on both online nodes | Process present; queue/heartbeat/authority not freshly qualified |
| GitHub Actions Runner | CI execution substrate | Qualification and verification workflows exist | Runner processes on both nodes | Runner present; workflow existence is not proof of a passing gate |
| Docker / containerd | Container substrate where used | Container/workflow declarations exist | Linux daemon active; no running containers | Daemon present; workloads not observed |
| Caddy | Local HTTP/TLS proxy candidate/runtime | Process config path observed | Linux process active | Routes/TLS/access controls unverified |
| SentinelX Cloud Core | Host management/monitoring connector | External management plane; not product-state authority | Linux process active | Permissions and trust boundary unverified |
| DF3 local services | Potential local model/autonomous services | Labels not mapped to accepted architecture role | Two macOS launchd labels | Identity/health/routing unknown; do not equate with Alamo/Ollama |
| Home Assistant Core | Smart Home authority only if admitted; never global product state | Target-selected / gated in component registry | Not identified in bounded checks | Target-gated; bounded absence is not global absence |
| PostgreSQL / pgvector | Future persistence/vector capability | Target-selected, future-gated | No running Linux containers; service inventory not exhaustive | Not activated by this pass; current foundation remains single-node/in-memory |
| etcd / NATS JetStream | Future coordination/event transport only | Target-gated integration matrix | Not identified in bounded checks | Not active by evidence; no second State Authority |
| SOPS/age, Cosign, Syft, Trivy | Secret protection, artifact signing, SBOM, vulnerability scanning | Selected/foundation entries in registry | Complete executable inventory not performed | Declared; local presence not established |
| Git worktrees | Isolated engineering workspaces | Multiple worktree directories | Three named Linux, six named macOS | Directory names only; HEAD/dirty/lease ownership unchecked |

## 5. Documentary consistency findings

### C-01 — FreeLLMAPI route classification

The distributed AI architecture describes a FreeLLMAPI cloud/provider route in its routing narrative. profiles/agent-registry.json and profiles/providers/astra-gold-hybrid-agent-fabric.yaml classify FreeLLMAPI as local_gateway; provider fabric status is PENDING. These could refer to different sides of a locally hosted gateway and upstream provider, but that interpretation is not evidenced by a pinned deployment contract.

Disposition: OPEN CONTRACT CONFLICT. Define service location, upstream provider, egress boundary, authentication, model identity and local-only behavior. Do not normalize by assumption.

### C-02 — OmniRoute / UnoRouter identity

The agent registry has separate unorouter and claude records; the Claude record points at gateway omniroute and credential reference OMNIROUTE_API_KEY. Do not merge unorouter, omniroute, openrouter or a model identity based on similar names.

Disposition: resolve names against pinned package/source and non-secret configuration metadata. Never read or log credential values.

### C-03 — Model-tag provenance

Linux Ollama lists qwen2.5-coder:7b and claude-sonnet-4-6:latest with the same digest in captured CLI output. A local tag can be a custom alias; it does not prove vendor, model family, license or safety behavior.

Disposition: later, under explicit authorization, collect non-secret model metadata/provenance and verify exact digest/source/license. Do not infer equivalence.

### C-04 — Unified source matrices remain drafts

docs/checkpoints/mediahub-unified-architecture-and-deployment-contract-v0.1.md and docs/checkpoints/mediahub-unified-system-traceability-matrix-v0.1.md state PROPOSED / NOT ACCEPTED / NOT FROZEN. The component registry and integration matrix have September 2026 review dates and retain future-gated selections.

Disposition: this Wave 02 matrix is a reconciliation aid, not acceptance. Owner/governance approval and domain-source reconciliation remain required before freezing a unified contract.

### C-05 — Runtime and declared state are different

Workflow files, manifests, launchd/systemd labels, processes and installed CLIs each prove only their own narrow fact. A runner does not prove qualification pass; a model tag does not prove provenance; a CLI does not prove provider connectivity; an agent process does not prove exclusive queue/state authority.

Disposition: require revision-bound, fresh evidence for each lifecycle transition.

## 6. Canonical per-component evidence schema

Every component row should ultimately carry:

- stable historical component ID; exact version; immutable source ref and source digest;
- stable node ID; exact OS/architecture; one bounded role; allowed and forbidden operations;
- data classification; egress policy; provider identity; exact model digest where applicable;
- non-secret configuration revision and secret reference identifier only, never secret value;
- runtime process/service evidence; verification evidence; exact qualification gate and status;
- release status and production acceptance as separate fields;
- UTC observation time, evidence source and independent reviewer identity/status.

Missing required fields mean UNKNOWN, never implicit PASS. Status promotion must be evidence-gated.

## 7. Required control-plane invariants

1. Jarvis submits bounded missions to A0-ASTRA; it does not write ASTRA-internal queue/claim/lease/gate state directly.
2. Product State Authority alone owns canonical product-state mutation. ASTRA queue-state authority is a separate engineering-plane scope.
3. GitHub adapter uses least-privilege repository/branch/path capabilities and emits auditable evidence for every mutation.
4. Routing records task/data class, allowed egress, executor, provider, exact model identity, policy/config revision, budget/authorization and fallback decision.
5. local-only must fail closed. No silent fallback to Anthropic, OmniRoute or another cloud route.
6. Merge, release, deployment, production mutation, credential access, governance bypass and qualification remain prohibited without separate explicit authorization.
7. Design, implementation, test, verification, qualification, release, deployment and acceptance each require distinct evidence.

## 8. Limits and next bounded pass

This is a broad-but-bounded inventory of two online nodes, repository tree and selected service/process/provider metadata. It is not a complete scan of all local servers, packages, services or network endpoints. mh-dev-01 was offline. Worktree contents, listening ports, service configuration bodies, network routes, credentials, inference, provider connectivity and host hardware/thermal data were not inspected.

Next bounded step: draft the Jarvis Control Plane / GitHub Adapter contract and a machine-readable component inventory schema. Resolve C-01/C-02 at the source-contract level before any route implementation. A separate explicitly authorized read-only pass can inspect worktree HEAD/dirty status and non-secret launch/service metadata, including mapping the two DF3 labels. No installation, tests, qualification or deployment should be included.
