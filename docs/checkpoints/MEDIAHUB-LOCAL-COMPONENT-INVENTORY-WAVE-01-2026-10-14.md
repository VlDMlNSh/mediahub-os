# MediaHub OS — Local Component Inventory Wave 01

- Date: 2026-10-14
- Repository: `VlDMlNSh/mediahub-os`
- Documentation branch: `docs/mediahub-chat-tree-map-20261012`
- Status: **READ-ONLY DISCOVERY; NOT QUALIFICATION; NOT DEPLOYMENT ACCEPTANCE**
- Scope: two Desktop Commander-connected development nodes, repository-local component/provider registries, process/service inventory, and Ollama model listing where its daemon was already available.
- Safety: no credential values were read or emitted; no model inference/provider calls, tests, qualification scripts, installations, configuration changes, deployments, merges, or infrastructure changes were performed.

## 1. Method and evidence limits

Read-only checks used Desktop Commander to inspect each connected node's platform, selected process/service metadata, executable availability, relevant repository paths and provider registry entries. On Linux, `ollama list` queried the already-running local Ollama service; this does not invoke inference. On macOS, `ollama list` returned a daemon-connection error, so no model inventory is claimed there. `docker ps` on Linux returned no containers. No repository inventory/qualification script was executed.

The two checkouts have the same project tree shape, but this pass did not establish that their local Git worktrees, source SHAs or runtime configuration are identical. The inventory is point-in-time evidence from 2026-10-14 and must not be generalized to offline nodes.

## 2. Host findings

| Component / signal | Linux worker `mh-dev-02` | macOS node `Voktors-Mini.Dlink` | Evidence interpretation |
|---|---|---|---|
| Astra GitHub Agent | Process observed: `python3 /home/mediahub/astra-work/astra_github_agent.py`; `mediahub-astra-github-bootstrap.service` active | Process observed: `astra_github_agent.py`; launchd label `com.mediahub.astra.github-agent` present | Running/present process evidence only; end-to-end transport and authority qualification remain separate. |
| GitHub Actions runner | Runner service and listener observed | Runner listener / launchd runner label observed | Runner process presence does not prove the required qualification paths or least-privilege scopes. |
| Docker | Docker daemon service active; `docker ps` returned no running containers | Not established in this pass | No active Linux container workload was observed at the time of the query. |
| Ollama CLI/service | `/usr/local/bin/ollama`; `ollama.service` active; `ollama serve` process observed | `/opt/homebrew/bin/ollama` exists; `ollama list` failed because no Ollama server was reachable | Linux runtime is present; macOS CLI presence does not mean its daemon is running. |
| Ollama models | `qwen2.5-coder:1.5b`, `qwen2.5-coder:3b`, `qwen2.5-coder:7b`, `claude-sonnet-4-6:latest` listed by the local service | Unknown; daemon unavailable | Model tags are inventory labels only. The shared model digest shown for `qwen2.5-coder:7b` and `claude-sonnet-4-6:latest` is a provenance/alias concern to investigate later; this pass does not infer model equivalence or vendor identity from the tag. |
| Claude Code CLI | `/home/mediahub/.local/bin/claude` found | `/Users/voktor/.local/npm/bin/claude` found | Executable presence only; no provider selected or called. |
| Codex CLI | `/home/mediahub/.local/bin/codex` found | `/Users/voktor/.local/npm/bin/codex` found | Executable presence only. |
| OmniRoute CLI | No `omniroute` executable found by command lookup | `/Users/voktor/.local/npm/bin/omniroute` found | Installed on macOS node only in this scan; no OmniRoute process/runtime session was observed. CLI presence is not gateway connectivity or qualification. |
| FCC | No standalone `fcc` command found | No standalone `fcc` command found | FCC remains a documented integration/control-layer identity. Absence of a command named `fcc` does not prove the adapter is absent; exact implementation/package/process mapping remains unresolved. |
| FreeLLMAPI | No executable/process/service identified by the bounded checks | No executable/process/service identified by the bounded checks | Registry has a local-gateway candidate/pending status; do not claim runtime deployment from registry presence. |
| Additional macOS service labels | N/A | `com.mediahub.df3-llama` and `com.mediahub.df3-autonomous` labels observed | Labels indicate registered services only; their API, model, health, trust boundary and relation to Alamo/Ollama were not inspected or proven. |

## 3. Repository evidence

1. `profiles/providers/astra-gold-hybrid-agent-fabric.yaml`:
   - `claude` is represented as a cloud gateway using the OmniRoute credential reference, status `NOT_PROVEN`.
   - `freellmapi` is represented as a local gateway, status `PENDING`.
   - `ollama` is listed in the local fabric as a local model, without a qualification claim in the inspected excerpt.
2. `profiles/agent-registry.json` distinguishes the Claude provider/gateway identity from FCC, which is described as transport/gateway rather than an agent.
3. `evidence/provider-model.json` is historical evidence from 2026-09-27 (source commit `7bdd382e5cceb1b380f4985ce9b36c351161407f`), not fresh qualification evidence for these two nodes. Its provider statuses cannot be used to assert present-day connectivity.
4. `control/qualification/g4-115.json` defines five mandatory paths, including FCC and OmniRoute paths. The adjacent local qualification report dated 2026-10-02 records G2/G3/G4 and launch gates as BLOCKED, with 0/115 fresh rounds. This remains a historical gate record, not a new qualification result.
5. `architecture/MEDIAHUB-DISTRIBUTED-AI-INFRASTRUCTURE.md` on `main` (blob `e549692f207fbc91d9b9b9b92b8e665404f07290`) defines FCC as the required Claude Code integration/control layer, FreeLLMAPI as a cloud-model path and Alamo as the intended local inference endpoint. It explicitly says the topology is logical and does not prove deployment or compatibility.

## 4. Component state ledger

| Component | Observed state | Qualification/admission state | Next evidence needed |
|---|---|---|---|
| Astra GitHub Agent | Process present on both connected nodes | NOT QUALIFIED BY THIS INVENTORY | Fresh identity, source SHA, transport/claim/queue/heartbeat evidence, authority-scope review. |
| Claude Code | CLI found on both nodes | NOT QUALIFIED BY THIS INVENTORY | Exact version/provenance and controlled route evidence that identifies the actual provider without exposing secrets. |
| Codex CLI | CLI found on both nodes | NOT QUALIFIED BY THIS INVENTORY | Exact version/provenance and separately authorized execution evidence. |
| Ollama | Linux daemon active and four tags listed; macOS CLI present but daemon unavailable | Linux local model service DISCOVERED; neither node newly qualified | Verify model digest/provenance, service identity, API boundary, resource limits and local-only routing. No inference was run. |
| OmniRoute | CLI found only on macOS node; no runtime process observed | INSTALLED-CLI ONLY / NOT PROVEN | Version/source provenance, configured gateway identity and policy-bounded connectivity evidence; no provider call in this pass. |
| FCC | Architectural/registry references found; no standalone command identified | INTEGRATION MAPPING UNRESOLVED | Identify the exact pinned implementation, invocation path and routing/control contract; do not equate it with a provider or agent. |
| FreeLLMAPI | Repository registry entry only; no local service/process found by bounded checks | PENDING / NOT PROVEN | Identify deployment host and service contract, then obtain separately authorized evidence; no fallback or connectivity assumed. |
| Docker | Daemon active on Linux, no running containers reported | No container workload evidenced | If relevant later, inventory declared units/images without changing infrastructure. |
| DF3 local services | Two macOS launchd labels observed | IDENTITY / FUNCTION / HEALTH UNVERIFIED | Read service definitions and non-secret health metadata in a separately bounded pass; do not assume either is Alamo or Ollama. |

## 5. Routing and safety implications

- A provider/router registry entry, CLI binary, launchd/systemd label, process or historical evidence file is not proof of a working end-to-end execution path.
- Treat Claude Code as the client/agent surface; record the actual executor/provider separately for every task.
- Local-only routing must fail closed. No silent fallback to Anthropic or another cloud gateway is acceptable.
- OmniRoute, FCC, FreeLLMAPI and Ollama have distinct roles and must not be conflated: gateway/router, integration/control layer, provider path, and local inference runtime respectively.
- Keep Product State Authority as the sole canonical product-state mutation authority. Neither a provider, router, CLI, runner nor ASTRA process gains that authority by being installed or running.
- The documentation branch currently diverges from `main`; this inventory was committed only to the documentation branch and does not integrate either branch.

## 6. Limits and next bounded work

This was a narrow read-only inventory of two online Desktop Commander nodes and selected repository evidence, not a complete scan of every local server, offline node, package, service, network endpoint or provider account. No secrets were inspected; no provider was called. The absence of a process or executable in these bounded checks is not proof of absence from every path or host.

**Next:** draft the Jarvis Control Plane / GitHub Adapter contract against the live permission design and these inventory findings: mission submission to A0-ASTRA with a single-writer boundary, least-privilege repository scopes, auditable per-task routing decision records (including provider/model identity, data classification, egress, budget and explicit fallback), evidence requirements, and prohibited merge/release/deployment/production mutations. Keep implementation and qualification blocked until their separate gates are met.
