# MediaHub OS — Greenfield / Legacy Artifact Ledger, Wave 01

- Date: 2026-10-15
- Status: **SOURCE-BOUNDED CLASSIFICATION / NOT A DELETION MANIFEST / NOT A TARGET COMPONENT APPROVAL**
- Repository: `VlDMlNSh/mediahub-os`
- Documentation ref: `docs/mediahub-chat-tree-map-20261012`
- Purpose: separate new-system requirements from old-host operational artifacts so the new MediaHub OS can be designed cleanly for new hardware without importing failed deployment assumptions.
- Owner direction: Mac Pro, Mac mini/server, remote video server, Jarvis, Astra, multi-agent system and corporation discussions describe the **new target system to design from scratch**. Prior old-server installation attempts are not target runtime evidence.
- Safety boundary: source/document inspection only. No tests, installs, host/runtime access, credentials, provider/model calls, deployment, migration, workflow invocation, or bulk deletion.

## 1. Classification rules

| Class | Meaning | Target treatment |
|---|---|---|
| TARGET-REQUIREMENT | Desired capability or owner direction, independent of prior deployment | Keep and normalize into target requirements; not implementation evidence |
| HISTORICAL-EVIDENCE | Prior decisions, failed attempts, audit records, provenance or old status evidence | Preserve only as history where useful; label clearly; never treat as current target state |
| LEGACY-OPERATIONAL | Hostnames, user accounts, filesystem paths, runner labels, service definitions, launchers, model tags, secrets references or commands tied to old hosts | Not target configuration; remove/quarantine only after reference/dependency/ID review |
| CANDIDATE-DESIGN | Architecture proposal or upstream component not yet accepted | Keep as proposal; no installation or selection implied |
| SHARED-OR-UNKNOWN | Artifact may contain reusable contracts/logic or its old-target exclusivity is unproven | HOLD; trace references and semantics before deletion |
| TARGET-ACCEPTED | Explicitly accepted for the new system with evidence and owner decision | None established by this ledger |

## 2. Initial source-backed ledger

| Artifact / area | Classification | Evidence / reason | Disposition |
|---|---|---|---|
| Discussions of Mac Pro, Mac mini/server, remote video server, Jarvis, Astra, multi-agent system and corporation | TARGET-REQUIREMENT | Owner explicitly says these concepts form the new system being designed from scratch | Extract capabilities, roles, constraints and acceptance criteria into target requirements; do not infer installed components |
| Failed installation attempts and old-server operating instructions | HISTORICAL-EVIDENCE / LEGACY-OPERATIONAL | Owner says old-server attempts are not to be reused | Exclude from target baseline; retain only minimal provenance needed to explain retired assumptions |
| `ops/agent-fabric/providers/local-executor-routing-v2.yaml` | LEGACY-OPERATIONAL / SHARED-OR-UNKNOWN | Contains executor IDs and routes tied to old execution topology; runtime consumption was not established in the bounded trace | Do not use as target routing contract; trace inbound references before deletion/quarantine |
| `ops/agent-fabric/providers/node-role-map.yaml` | LEGACY-OPERATIONAL | Contains `mh-dev-02`, `Voktors-Mac-mini.local`, old pools/model tags | Not target hardware inventory; dependency/ID review required before removal |
| `ops/qualification/run_distributed_local_worker.py` | LEGACY-OPERATIONAL / SHARED-OR-UNKNOWN | Hard-coded old node IDs, users, model tags, pools and host-specific paths | Not target worker implementation by default; inspect callers/imports and shared contract dependencies before removal |
| `.github/workflows/astra-distributed-local-worker.yml` | LEGACY-OPERATIONAL | Runner labels, host checks, user checks, local model tags and old node names | Disable from target planning; reference/trigger/permission review required before deleting |
| `.github/workflows/astra-chat-control.yml` | LEGACY-OPERATIONAL / SHARED-OR-UNKNOWN | Command workflow binds old node/executor values and host-specific environment paths | Not target control-plane design; trace dispatchers, task contracts and shared policy references before deletion |
| `control/qualification/distributed-runner-contract.json` | LEGACY-OPERATIONAL / SHARED-OR-UNKNOWN | Explicitly encodes old node IDs, runner labels, hostnames, users and OS/architecture | Do not inherit node identities; determine whether any generic admission invariant is independently reusable |
| `ops/astra_orchestrator.py`, `ops/control/sign_command.py`, `control/commands/*.json` | SHARED-OR-UNKNOWN | Present in source tree and related to command/dispatch flow; target-specificity and full reference closure not yet established | HOLD; map dependencies and classify each file individually; no blanket deletion |
| Old-node-specific LaunchAgent, systemd/mesh unit, path-specific diagnostics and old supervisor workflows | LEGACY-OPERATIONAL unless reference tracing proves shared use | Project map identifies these as old-node-bound artifacts; exact dependency closure remains open | Prepare path-level deletion/quarantine proposals only after reverse-reference and historical-ID checks |
| `profiles/agent-registry.json`, `profiles/providers/astra-gold-hybrid-agent-fabric.yaml`, `ops/qualification/provider_model_registry.json` | SHARED-OR-UNKNOWN / CANDIDATE-DESIGN | Registries describe different namespaces/semantics; no single target registry or production loader has been established in reviewed paths | Do not blindly delete or promote; rebuild a target component inventory and explicit namespace/schema contract |
| `schemas/ai/*`, `runtime/mediahub_runtime/*`, existing State Authority/security contracts and Baseline documents | SHARED-OR-UNKNOWN | May encode reusable requirements, security invariants or implementation assumptions; current owner instruction does not by itself supersede accepted normative contracts | Preserve pending domain-by-domain review and explicit change control; do not assume old runtime code is reusable |
| GitHub projects discussed as possible mature components (including agent frameworks, workflow engines, routers, databases and observability tools) | CANDIDATE-DESIGN | Discussion/repository existence is not acceptance, compatibility, qualification or permission to install | Re-evaluate upstream source, immutable version, license, maintenance/security, SBOM/dependencies, isolation, egress, hardware/OS fit and contract fit |
| New hardware/OS/topology inventory | OPEN INPUT | No authoritative model numbers, OS versions, RAM/storage/network/GPU/accelerator or role-to-machine allocation recorded in reviewed evidence | Must be supplied/confirmed before hardware-specific component admission and deployment planning |

## 3. Deletion / quarantine gate

No deletion is executed by this ledger. Before any path is removed or quarantined, its row must include:

1. exact path and current blob SHA;
2. classification and rationale;
3. inbound references (code, workflows, docs, schemas, generated files, tests and external entry points where inspectable);
4. historical IDs/status/evidence that must be preserved;
5. whether the artifact contains an independently reusable contract or security invariant;
6. proposed action: keep as history, move/archive, remove, or replace;
7. owner decision for ambiguous or normative content;
8. post-change read-back and reference-closure evidence.

A file that looks old or host-specific is not sufficient proof that deleting it is safe. Do not delete historical audit evidence merely to make the active target map look clean. Retire old operational configuration from the target baseline first; perform physical repository deletion as a separately reviewable change.

## 4. New target source-of-truth package

The greenfield design should converge on one coordinated set of artifacts:

1. **Target system map** — domains, responsibilities, trust boundaries, data/control/evidence flows and dependencies.
2. **Versioned system contract** — identities/namespaces, interfaces, schemas, lifecycle states, failure semantics, authorization, ownership and compatibility policy.
3. **Component admission ledger** — candidates, immutable upstream pins, provenance/license/security/dependency evidence, target role, interface fit, owner decision and lifecycle status.
4. **Requirements-to-evidence matrix** — requirement → domain/component → interface/contract → verification method/evidence → status/owner.
5. **Decision and discrepancy register** — conflicts, affected artifacts, options, recommendation, owner decision and closure evidence.
6. **Hardware/OS deployment profile** — confirmed target inventory and role allocation, kept separate from abstract architecture.

No item becomes ACCEPTED, IMPLEMENTED, VERIFIED, QUALIFIED, DEPLOYED or INDEPENDENTLY ACCEPTED without its corresponding evidence.

## 5. Current gaps and next pass

- The ledger is source-bounded, not an exhaustive repository-wide deletion manifest.
- Full reverse-reference closure for the listed old-node artifacts is still OPEN.
- New hardware/OS/topology details are OPEN.
- A single target component set, versioned contract and traceability matrix are not yet complete.
- The next pass should map target domains and derive a requirements catalogue from owner-directed system concepts, while continuing per-path dependency closure for legacy artifacts. Do not begin product implementation or deployment from this ledger alone.
