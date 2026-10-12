# MediaHub OS / Jarvis — Unified System Traceability Matrix v0.1

- Date: 2026-10-12
- Status: **PROPOSED / INVENTORY AND RECONCILIATION DRAFT / NOT ACCEPTED / NOT FROZEN**
- Scope: cross-domain architecture, component admission, deployment lifecycle, evidence gates, and hardware-independent preparation before purchasing equipment.
- Parent contract: `docs/checkpoints/mediahub-unified-architecture-and-deployment-contract-v0.1.md`
- Navigation authority: `docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md` on `docs/mediahub-chat-tree-map-20261012`
- Current functional authority: `docs/checkpoints/mediahub-functional-baseline-2.0.md` on `main`, blob `1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f`.
- Historical provenance: Baseline 1.0 blob `9df4892ed0734050ac79732603d15bb414717310`; do not merge implicitly.
- Current observed `main` HEAD during this pass: `1d45bbccbbbd27309c39cb9e9351bb291cdb47a8`.
- This matrix is not a replacement for domain primary sources, Baseline 2.0, the canonical component manifest, or domain acceptance records. It does not authorize implementation, purchase, installation, runtime invocation, qualification, deployment, or merge.

## 1. Status vocabulary

| Status | Meaning |
|---|---|
| ACCEPTED CANONICAL | Explicitly accepted normative reference within its declared scope. |
| PROPOSED | Design direction awaiting owner/governance acceptance. |
| SELECTED | Component admitted for the stated role, not necessarily deployed or qualified. |
| TARGET-GATED | Cannot be activated until target, authority, operational and qualification evidence exists. |
| FUTURE-GATED / CANDIDATE | Reference option only; do not treat as chosen implementation. |
| UNKNOWN / NOT PROVEN | Insufficient revision-bound evidence; never equivalent to PASS. |
| NOT AUTHORIZED | Explicitly no permission for the stated action. |
| NOT APPLICABLE | A documented, reasoned non-applicability decision; not a substitute for missing evidence. |

Every row must distinguish **decision**, **implementation**, **verification**, **qualification**, **release**, and **production acceptance**.

## 2. Non-negotiable system invariants

1. Functional Baseline 2.0 is the current accepted functional reference. Baseline 1.0 remains preserved historical provenance; no silent merge.
2. MediaHub Product State Authority remains the sole canonical authority for product state. AI models, Claude, Ollama, agents, plugins, cloud services, queues, persistence targets, workflow engines and observability systems cannot create a second authority.
3. Preserve the existing P0-03 through P0-06 contracts. P0-07 remains a blocker for production mutation/publication until its governance/API gap is explicitly resolved.
4. Canonical mutation follows the approved chain: intent/input → boundary → policy evaluation → authorization → command → Consumer Boundary → State Authority → canonical state → observation/evidence.
5. Home Assistant, if admitted later, owns Smart Home domain state only; it does not replace MediaHub Product State Authority.
6. Jarvis is the engineering orchestration umbrella; ASTRA remains a bounded engineering execution/queue/evidence subsystem; MediaHub is the product/domain plane. Their state and authority must not be conflated.
7. Claude is an external model/service path; Ollama serves compatible local model artifacts. Claude is not literally hosted inside Ollama. Jarvis may integrate distinct adapters and a policy-controlled router.
8. External egress is default-deny in architecture. Classification, purpose, destination/provider eligibility, minimization/redaction, authorization, bounded transfer, audit and retention policy precede transfer. No silent local-to-cloud fallback.
9. Model output, tool output, retrieval results and cloud results are untrusted data until independently validated. Model confidence or task completion does not grant authorization.
10. Reliability baseline remains SINGLE NODE / NO HA until an accepted decision and exact-target evidence establish otherwise.
11. Unknown hardware is not a target profile. The historical Mac mini Server 2011 mention is only a candidate; no suitability for modern local inference, secure boot, current OS support or sustained workload is implied.
12. Architecture work can proceed without buying hardware, but hardware-specific selection, benchmarks, secure boot, driver/thermal/power qualification and production readiness remain open until an exact target is selected.

## 3. Global cross-domain matrix (MH-01…MH-25)

The statuses below are reconciled from the current map and source audits, not newly granted acceptances. Exact detailed source pointers and SHA history remain in the map and domain documents.

| Domain | System responsibility | Required inputs/dependencies | Required outputs/contracts | Current disposition / open gate |
|---|---|---|---|---|
| MH-01 Charter | Product intent, scope, system goals | Owner decisions, B2, governance | Scope, non-goals, acceptance ownership | PARTIALLY CLOSED; provenance/closure must remain explicit |
| MH-02 Boundaries | Product/developer/security domains | Charter, threat model, B2 | Trust boundaries, allowed flows | RECONCILED in map; retain domain-primary authority |
| MH-03 Runtime Foundation | Runtime and State Authority foundation | MH-01/02, P0-03…P0-06 | Canonical state and runtime contracts | Preserve single logical authority; no implied HA |
| MH-04 Security | Identity, authentication, authorization, trust | MH-02/03, threat model | Security invariants and capability controls | PARTIALLY CLOSED; production proof separate |
| MH-05 Consumer Integration / Smart Home | External integrations and consumer boundary | MH-03/04, policy | Typed adapters and bounded integration commands | PARTIALLY CLOSED; HA owns Smart Home only if later admitted |
| MH-06 Core Runtime Services | Core service interfaces and lifecycle | MH-03, MH-04, MH-07 | Service contracts, health and failure semantics | PARTIALLY CLOSED; no global freeze |
| MH-07 Configuration / Policy | Configuration, policy distribution/evaluation | MH-04, MH-10/12/13 | Versioned policy and authorization inputs | PARTIALLY CLOSED; P0-07 remains blocking |
| MH-08 Plugins | Extensible tool/plugin boundary | MH-04/05/07/12 | Capability-scoped adapters and manifests | PARTIALLY CLOSED; plugin presence is not trust |
| MH-09 UI / Presentation | User interaction and presentation | B2, MH-03/07/12 | UI flows and safe command intents | PROPOSED / not accepted; UI4-04 HOLD remains |
| MH-10 AI / Intelligence | Model roles, inference semantics, agent behavior | MH-04/07/09/12/13/14/21 | AI contracts, provenance, proposal-only semantics | PROPOSED / NOT ACCEPTED / NOT FROZEN; P0-07 and MH-21 ownership coordination open |
| MH-11 Observability | Logs, metrics, traces, operational evidence | MH-03/06/12/22 | Correlated telemetry and alerting | PARTIALLY CLOSED; telemetry is not correctness authority |
| MH-12 Security Analysis | Threat model and security invariants | MH-02/04/08/10/13/21 | Threats, controls, assurance evidence | RECONCILED in map; runtime assurance still separate |
| MH-13 Privacy / Data Governance | Classification, purpose, minimization, retention | MH-04/10/14/21 | Data-handling rules and deletion/retention contracts | PARTIALLY CLOSED; provider terms/data residency need evidence |
| MH-14 Persistence | Durable representation of canonical state | MH-03, approved schema/transactions, MH-16 | Persistence contract, atomicity, backup/restore and recovery | Physical implementation NOT AUTHORIZED; storage engine unresolved |
| MH-15 OS / Appliance | Host, OS, boot, process, storage, network boundary | Exact hardware/firmware/OS profile, MH-04/12/16 | Reproducible node profile and hardening evidence | NOT ACCEPTED / NOT FROZEN; implementation authorization NONE |
| MH-16 Installer / Update / Recovery | Build/install/enroll/update/rollback/recovery | MH-15, signed artifacts, MH-14, MH-22 | Lifecycle contract and recovery evidence | PROPOSED / governance pending / implementation not authorized |
| MH-17 Devices / Protocols | Device and protocol adapters | MH-05/12/13/22 | Device identity, protocol and safety contracts | PARTIALLY CLOSED; device qualification open |
| MH-18 Media | Media ingest, transform, playback, delivery | B2, MH-05/14/15/17 | Codec, metadata, access and resource contracts | PARTIALLY CLOSED; target/hardware compatibility open |
| MH-19 Knowledge Graph / Digital Twin | Derived knowledge and twin representations | MH-13/14, provenance, B2 | Versioned derived data and source lineage | PARTIALLY CLOSED; derived knowledge is not canonical authority |
| MH-20 Automation / Energy / Self-Healing | Bounded automation and remediation proposals | MH-04/07/11/12/16/22 | Policy-bound actions, audit, safe failure | NOT ACCEPTED / NOT FROZEN; no autonomous destructive fixes |
| MH-21 Hybrid Cloud / Distributed AI | External compute, routing, egress and workload placement | MH-10/12/13/15/22 | External-compute contract and egress evidence | NOT ACCEPTED / NOT FROZEN; provider/runtime enforcement UNKNOWN |
| MH-22 Qualification / Operations | Release evidence, operations, SLO, incident and qualification gates | All domains, exact target and release identity | Revision-bound qualification decision | NO-GO pending evidence; production qualification not granted |
| MH-23 Evolution / Migration | Compatibility, schema/software evolution, migration | MH-14/16/22 and accepted authority contracts | Prepare/protect/verify/migrate/validate/rollback contracts | NOT ACCEPTED / NOT FROZEN; branch diverged; no merge authorization |
| MH-24 UI / Navigation + baseline reconciliation | Functional traceability and interface reconciliation | B1 provenance, B2, domain contracts | Traceability matrix and reconciliation record | B2 accepted; individual implementation and UI4-04 status remain separate |
| MH-25 Stage reconciliation / control inventory | Cross-stage inventory and discrepancy control | All MH domains and checkpoints | Current source-bound inventory, owner decisions, gap register | Inventory/reconciliation layer; not proof that all domains are closed |
| Jarvis (umbrella) | Engineering orchestration and model/tool routing | MH-10/12/13/21, ASTRA contracts, repo policy | Task envelope, router decisions, bounded tool calls, evidence | Owner direction recorded; global architecture not accepted/frozen |
| ASTRA Gold | Bounded engineering queue/execution/evidence subsystem | Task contract, executor identity, transport, scheduler, qualification | Queue state, execution evidence, independent verification | CURRENT TRUTH NOT_PROVEN / BLOCKED; no qualification claim |
| MediaHub product plane | User-facing product and canonical product state | B2, MH-03, domain contracts | Product capabilities and canonical state | B2 is functional authority; runtime readiness not implied |

## 4. Claude + local Ollama decision matrix

| Dimension | Claude path | Local Ollama path | Jarvis enforcement |
|---|---|---|---|
| Execution location | External provider/service path | Selected local host | Record actual destination per invocation |
| Model identity | Exact Claude model/interface/API version where exposed | Exact model tag/digest, quantization and artifact provenance | Reject unresolved or unapproved model identifiers |
| Data egress | External processing; must be policy-authorized | Local by default, but local endpoint/logs still need privacy controls | Classify before routing; no silent fallback |
| Credentials | Approved external credential mechanism | Local endpoint access control; no assumption of built-in authentication | Secret broker/least privilege; never place credentials in prompts |
| Tool access | Separate tool gateway; no arbitrary shell by model | Same rule | Capability-scoped tools, per-task allowlists and approval gates |
| Quality/performance | Must measure task-specific quality, latency, cost and provider limits | Must measure model quality, RAM/VRAM, context, throughput, thermals and latency on exact hardware | Route only to admitted profiles with evidence-based thresholds |
| Failure/fallback | Rate limit, network loss, provider rejection, timeout, cancellation | Model unavailable, resource exhaustion, context overflow, degraded quality | Explicit failure states; fallback requires a new policy decision |
| Privacy/retention | Provider terms, region, retention and training use need current evidence | Local logs, cache, model files, backups and endpoint exposure need controls | Data-minimization and audit; no secrets/raw sensitive prompts by default |
| State authority | None | None | Outputs remain untrusted data until validated |
| Current status | TARGET DESIGN; access mode not selected | TARGET DESIGN; host/model not selected | PROPOSED; no runtime activated |

**Architecture shape still to select:** (A) Claude as engineering operator with Ollama as a distinct local model/tool endpoint; or (B) Jarvis policy router selects Claude/Ollama per task. Do not assume that Claude Code or a Claude interface can transparently use an Ollama endpoint; compatibility must be verified against the exact interface and supported configuration.

## 5. Component admission and deployment profile matrix

| Capability | Current manifest posture | Design rule before activation |
|---|---|---|
| Protobuf / gRPC | SELECTED for typed contracts/RPC | Define schemas, compatibility, deadlines, auth, errors and version policy |
| OpenTelemetry Collector / Prometheus | SELECTED observational foundation | Observability only; no authorization or state correctness authority |
| SOPS + age | SELECTED secret/config mechanics | Key custody, rotation, recovery, access and audit still need design |
| Syft / Cosign / Trivy | SELECTED supply-chain tools | SBOM/signature/scan output feeds gates; tools do not approve release themselves |
| S3-compatible object interface | SELECTED interface; backend replaceable | Define object identity, integrity, retention, deletion, encryption and recovery |
| FFmpeg / OpenCV | SELECTED primitives in manifest scope | Exact build/license/codec/input boundary and target-resource qualification |
| PostgreSQL / pgvector | TARGET-GATED | MH-14 approval, schema/transaction authority, migration, restore and performance evidence |
| Home Assistant Core | TARGET-GATED integration | Smart Home scope only; explicit adapter, auth and safety qualification |
| restic | TARGET-GATED | Restore integrity, key recovery, retention and tested RPO/RTO |
| RAUC | TARGET-GATED | Only if exact target/boot/storage design supports it; atomic update and rollback evidence |
| ONNX Runtime / llama.cpp | TARGET-GATED local inference candidates | Exact model, hardware, runtime, isolation, licensing, quality/performance and gateway policy |
| Ollama | OWNER-DIRECTED local model-serving candidate; target-gated | Pin runtime/model versions; verify local endpoint binding/auth, logs, model provenance, resource and security profile |
| Claude interface | OWNER-DIRECTED external reasoning path; exact access mode unresolved | Verify supported interface, auth, data terms, retention, model availability, rate/cost limits and egress |
| containerd / OCI | CANDIDATE | Select only after process isolation, update, storage, observability and operations trade-off |
| Ray | CANDIDATE | Demonstrate distributed workload need; not a product-state authority |
| Netmaker / Headscale / WireGuard | REFERENCE CANDIDATES | Threat model, routing, key lifecycle, node identity, segmentation and failure evidence |
| Harbor | TARGET-GATED | Demonstrate registry need; identity/signing/retention/restore and operational burden |
| NATS/JetStream / etcd | FUTURE-GATED | Do not introduce a second durable workflow or canonical state authority |
| Temporal | REFERENCE / FUTURE-GATED | Requires a demonstrated workflow durability gap and explicit authority mapping |
| Kubernetes/K3s | REFERENCE ONLY | Not mandatory; no cluster assumed before target inventory and operating-cost analysis |
| Caddy | REFERENCE / TARGET-GATED | Routing/TLS only; not identity or policy authority |

The canonical component manifest controls final component status. This matrix does not promote any candidate.

## 6. Deployment and architecture preparation phases (hardware-independent first)

| Phase | Name | Required artifacts | Exit evidence / gate | Current permission |
|---|---|---|---|---|
| P00 | Scope and authority freeze | System context, B2 mapping, ownership/RACI, non-goals | No unresolved authority conflict for the scoped contract; explicit owner decision | Documentation work only |
| P01 | Source reconciliation | Map, checkpoints, primary-source index, SHA/ref register | Contradictions and stale refs listed with owner/disposition | Authorized read-only/doc reconciliation |
| P02 | Requirements traceability | B2-to-MH-to-component-to-test/evidence matrix | Every requirement has owner, source, status, acceptance evidence | Draft allowed; acceptance pending |
| P03 | Trust/threat/privacy model | Threat model, data classification, egress and secrets contracts | Threat/control/verification mapping and no bypass by design | Draft allowed |
| P04 | Logical architecture | Context/container/component/data-flow diagrams; authority boundary | All calls, stores, trust boundaries and failure paths mapped | Draft allowed |
| P05 | Claude/Ollama integration design | Adapter/router/tool-gateway contract, routing and fallback state machine | Exact interface shape selected; external egress behavior and local-only mode defined | Design only |
| P06 | Component and supply-chain decision | ADRs, manifest, license/provenance, SBOM/signature policy | Each component SELECTED/TARGET-GATED/CANDIDATE with rationale | No install |
| P07 | Hardware-independent software contracts | API/schema, versioning, errors, timeouts, cancellation, audit | Contract lint/review plan defined; no runtime assertion | Documentation only |
| P08 | Hardware procurement specification | Minimum/target profiles, capacity model, interfaces, power/thermal/noise/supportability | Exact target profile and owner purchase decision | Not ready until P00-P07 decisions mature |
| P09 | Host/OS profile | Hardware BOM, firmware, OS/kernel, storage/network, secure boot and support lifecycle | Reproducible per-node target profile | Blocked until hardware selected |
| P10 | Build and artifact trust | Reproducible build plan, pinned deps, SBOM, signatures, provenance | Exact build identity and artifact-verification rules | Design only |
| P11 | Install/enroll/updates | Installer, trust bootstrap, config, update, rollback and recovery contracts | Failure-state table and safe recovery proof plan | Implementation unauthorized |
| P12 | Persistence and backup | State schema, transaction semantics, key custody, backup/restore, deletion | Explicit MH-14 authorization, RPO/RTO and recovery acceptance | Physical implementation unauthorized |
| P13 | Core services and integrations | Service contracts, device/media/HA adapters and boundaries | Per-adapter compatibility, permission and failure evidence | Target-gated |
| P14 | AI and agent execution | Model manifest, gateway, retrieval provenance, tool sandbox, policy routing | Local/cloud paths tested independently; no model self-authorization | Runtime activation not authorized |
| P15 | Network and cloud | Network planes, identity, VPN/segmentation, egress policy, cloud workload contract | No forbidden path; data-egress enforcement evidence | Infrastructure changes unauthorized |
| P16 | Developer compute fabric | Node roles, queue, scheduler, worktree isolation, executor identity | Bounded task execution and independent verification design | Runtime not qualified |
| P17 | Backup, updates, rollback, DR | Recovery runbooks, restore verification, incident response | Restore and rollback evidence tied to exact release/target | Tests/qualification require separate authorization |
| P18 | Qualification | Test plans, threat model, performance/capacity, soak, failure injection, operations | Exact-SHA/target/release evidence; all gates PASS or justified N/A | Current NO-GO; no test run in this pass |
| P19 | Release and operations | Release record, SBOM, signature, runbooks, SLO/SLI, ownership/escalation | Explicit release and production acceptance | Not authorized |
| P20 | Change/evolution | Compatibility matrix, schema/API migrations, deprecation, rollback | No authority drift; versioned migration evidence | No migration/merge authorization |

Phases are a proposed dependency sequence, not a claim that earlier gates have been accepted or that later operations are authorized.

## 7. Cross-domain gates

| Gate | Decision question | Mandatory evidence | Failure disposition |
|---|---|---|---|
| G0 Scope | Is the target scope and owner explicit? | Charter, non-goals, accountable owner | BLOCKED |
| G1 Authority | Is there exactly one canonical product-state authority and a permitted mutation chain? | P0-03…P0-07 contracts, sequence/data-flow review | BLOCKED on ambiguity |
| G2 Security/privacy | Are identities, capabilities, data classes and egress bounded? | Threat model, privacy/retention, negative-path evidence plan | BLOCKED on unknown bypass |
| G3 Source/build | Can artifacts be traced to source, dependencies and signer? | Commit, build provenance, SBOM, signature, vulnerability disposition | BLOCKED on unverifiable artifact |
| G4 Target profile | Is exact hardware/firmware/OS/network/storage known? | Per-node inventory, supported lifecycle, compatibility | BLOCKED while unknown |
| G5 Install/recovery | Are install, update, rollback and restore bounded and recoverable? | State machine, failure semantics, recovery/restore evidence | BLOCKED on unknown recovery |
| G6 AI/provider | Are model identity, data handling, tools, routing and fallback controlled? | Model manifest, provider terms, sandbox, egress and audit evidence | BLOCKED on silent fallback/bypass |
| G7 Operations | Can faults be detected, contained, diagnosed and escalated? | SLI/SLO, alerting, runbooks, owner/escalation, incident records | BLOCKED on operational gaps |
| G8 Qualification | Is exact release/target evidence sufficient? | Test/verification/soak/capacity/security/restore evidence tied to exact identities | NO-GO if missing |
| G9 Release | Has authorized owner accepted this exact release? | Signed release identity, explicit approval, rollback/operations readiness | No promotion without approval |

## 8. Mandatory artifact set for a verifiable architecture

Each requirement/decision row should ultimately include:
- Stable ID; domain owner; requirement text; source path/ref/blob SHA and line/section pointer.
- Decision state, implementation state, verification state, qualification state, release state and production-acceptance state as separate fields.
- Dependencies and affected authority/security/privacy invariants.
- Positive and negative acceptance criteria, failure semantics, observability/audit fields and rollback/recovery requirements.
- Exact target/profile, model/runtime/component versions, commit/build/artifact digests where applicable.
- Evidence URI, timestamp, evaluator, reproducible procedure and freshness/current-head relationship.
- Conflict ID and explicit owner decision if sources disagree.
- Status values from §1; missing evidence must remain UNKNOWN / NOT PROVEN.

## 9. Known blockers and open owner decisions

1. MH-10/MH-21 ownership overlap: resolve formally; preserve AI semantics under MH-10 and hybrid/external compute under MH-21 until governance decides otherwise.
2. P0-07 remains blocking for production mutation/publication; do not invent an authorization bridge.
3. Exact Claude access mode: Claude Code/operator vs approved API integration vs another supported interface.
4. Jarvis topology: Claude as engineering operator plus Ollama as a distinct local model/tool, or a policy router selecting per task.
5. Exact local inference target, Ollama runtime, model artifact/license/provenance, resource profile and acceptance thresholds.
6. Hardware BOM and node roles are not frozen; do not infer modern local inference capability from the legacy Mac mini candidate.
7. MH-14 physical persistence is not authorized; no database/object-store/backup component becomes canonical by inclusion in a list.
8. MH-15 host/OS profile is not accepted/frozen; MH-16 implementation not authorized.
9. MH-21 production egress/provider controls are unverified; MH-22 qualification is NO-GO.
10. MH-23 branch is divergent and branch-specific; no merge/cherry-pick/rebase.
11. Full semantic reconciliation of all MH domains against B2 and the 68-section traceability matrix remains a tracked task. This matrix is a cross-domain inventory draft, not proof that every source line has been exhaustively reconciled.
12. Baseline 1.0 and Baseline 2.0 are not silently merged; only explicitly accepted change control can alter that status.

## 10. Acceptance and change control

This matrix may become an accepted cross-domain contract only after:
1. Each primary source is re-read at an exact ref/blob SHA and every row is traceable to the relevant clause.
2. Contradictions and scope overlaps have explicit owner/governance decisions.
3. The matrix is reviewed against Baseline 2.0 and the 68-section traceability matrix without rewriting B2.
4. Each domain owner confirms their responsibilities and acceptance evidence.
5. Independent review confirms authority, security, privacy, recovery, AI/cloud and lifecycle invariants.
6. The owner explicitly accepts a specific revision and its change-control method.
7. Implementation, verification, qualification and production acceptance remain separate subsequent gates.

## 11. Work performed in this revision

- Read current bootstrap, map, continuation checkpoint, unified contract, System Passport v3, Verifiable Architecture Contract 01, Jarvis gap report, Baseline 2.0, canonical component manifest, and MH-15/MH-16/MH-21/MH-22 primary sources.
- Observed `main` HEAD: `1d45bbccbbbd27309c39cb9e9351bb291cdb47a8`.
- This is a documentary cross-domain synthesis only. No tests, qualification, provider calls, model/runtime invocation, installation, purchase, infrastructure change, host inspection, deployment, migration, or merge were performed.
- Status remains **NOT ACCEPTED / NOT FROZEN / NOT IMPLEMENTED / NOT QUALIFIED**.


## 12. Revision-bound source crosswalk — MH-10 and MH-21 (2026-10-12)

Status: **PARTIAL / SOURCE-BOUND / OWNER ACCEPTANCE OPEN**. This pass re-read the exact primary source files on `main`; this section does not claim exhaustive domain coverage or acceptance.

| Stable requirement ID | Primary source and revision | Requirement / invariant | Dependency / responsible domain | Acceptance evidence required | Current state / unresolved issue |
|---|---|---|---|---|---|
| JARVIS-AI-01 | `docs/architecture/MH-10-acceptance-criteria.md` @ `main`, blob `7c0746defea6635494208e04bf940579b254a25f`, criteria 1–7 | AI output is data, not command or canonical state; policy + authorization precede mutation; Consumer Boundary mandatory; tools cannot self-grant; confidence and retrieved content do not grant authority | MH-10; State Authority; Policy; Authorization; Consumer Boundary; security boundary | Trace every mutation path and show enforced deny cases, authority separation, prompt/tool-injection tests, and governance approval | `NOT ACCEPTED / NOT FROZEN`; no test or runtime evidence collected in this documentary pass |
| JARVIS-AI-02 | Same MH-10 source, criteria 8–15 | Local/cloud models are untrusted until qualified; egress classified, bounded, authorized and observable; critical operations cannot rely solely on AI; safe deterministic/manual degradation; model provenance/rollback; resource/privacy/audit controls | MH-10; MH-6; MH-13; MH-21; model supply chain and observability | Model inventory/provenance, resource budgets, data-flow/egress evidence, offline/failure scenarios, privacy/retention controls, rollback record | Open; Claude access mode, Ollama placement/router, model qualification and data classes are not yet decided/evidenced |
| JARVIS-AI-03 | Same MH-10 source, criteria 16–20 | Security/red-team coverage, cross-chat contradiction disposition, closure of production-critical unknowns, traceability to MH-1…MH-10 and P0-03…P0-07, explicit governance freeze commit | MH-10 governance; security; MH-24 traceability; P0 boundaries | Reviewed test plan/results, contradiction register, closed requirement links, signed/explicit acceptance and freeze commit | Open; this pass did not run tests, qualify components, or accept/freeze MH-10 |
| HYBRID-AI-01 | `docs/architecture/MH-21-hybrid-cloud-distributed-ai.md` @ `main`, blob `a76f6b35ec31d6b8fff2b0a3e8a1fd22bdbec71c`, “Canonical principle” and “Method” | Hybrid cloud is external compute, not authority; local/remote AI, agents, RAG, providers, GPUs and tools are compute; output stays data until local validation and controlled authority chain | MH-21; MH-10; State Authority; Policy → Authorization → Consumer Boundary | Architecture/data-flow review and negative evidence that no external component can mutate canonical state directly | `ARCHITECTURE WORK AUTHORIZED / NOT ACCEPTED / NOT FROZEN`; no implementation inference |
| HYBRID-AI-02 | Same MH-21 source, “Mandatory boundaries” | Identity/authentication/authorization/capability/trust/authority are distinct; egress is classified/minimized/authorized; arbitrary egress/provider fallback forbidden; cloud failure preserves safe local operation | MH-21; identity/trust; privacy/security; local-first runtime | Egress policy matrix, provider allowlist, deny-by-default tests, audited routing/failure behavior and offline acceptance evidence | Open; explicit no-silent-fallback invariant retained; provider/data-egress enforcement not verified |
| HYBRID-AI-03 | Same MH-21 source, “Placement” and “Acceptance” | Placement is policy-driven across LOCAL, REMOTE_TRUSTED, REMOTE_UNTRUSTED, PROVIDER_API, OFFLINE, BLOCKED; no accepted/frozen/production-ready claim without complete evidence | MH-21; MH-10; MH-22 qualification | Workload placement table, data classification, policy decisions, observability/failure/security test evidence, governance acceptance | Open; user direction establishes Claude-centered Jarvis plus local Ollama as a desired direction, not a frozen topology |

### Cross-domain decisions preserved as OPEN

1. **Claude access surface:** not selected (e.g. approved provider API versus an explicitly approved Claude-operated engineering interface). Do not infer credentials, invoke a provider, or send project data externally.
2. **Routing topology:** not selected between Claude-as-operator with a separately invoked local Ollama tool and a per-task policy router. Claude is not an Ollama-hosted model.
3. **Data egress classes:** define which task/data classes may reach a remote provider, required minimization/redaction, retention and audit; default remains no external egress without explicit policy authorization.
4. **Model/tool trust:** Claude/Ollama outputs remain untrusted data; neither model may grant itself tools, permissions, or authority.
5. **Acceptance boundary:** MH-10/MH-21 remain unaccepted/unfrozen; no qualification or production readiness is claimed.

### Source availability limitation

The map points to canonical component-manifest blob `45988bf9da202c9597d0ca2de50e92e5c2e6ed55` on `main`, but the candidate path attempted in this pass did not resolve through the repository contents API. The P0-07 path recorded by the map likewise returned 404 on the selected ref. Their mapped blob/path must be resolved via the map's branch/source navigation before any conclusions about their current contents; this is a retrieval limitation, not evidence that the documents are absent from the repository. These sources are **not** marked reviewed in this crosswalk.

### Work performed and limits

- Re-read bootstrap, map, checkpoint, matrix, parent contract, Baseline 2.0, MH-10 acceptance criteria and MH-21 hybrid/cloud architecture.
- Baseline 2.0 remains `ACCEPTED / CANONICAL / IMMUTABLE`; Baseline 1.0 remains historical provenance.
- `main HEAD` observed from the repository's recent commit listing: `1d45bbccbbbd27309c39cb9e9351bb291cdb47a8`; this pass did not change `main`.
- No tests, qualification, provider/model calls, credentials, installation, host inspection, infrastructure change, deployment, migration or merge occurred.
- Matrix remains **PROPOSED / NOT ACCEPTED / NOT FROZEN / NOT IMPLEMENTED / NOT QUALIFIED**.


## 13. Revision-bound source crosswalk — component admission and P0-07 boundary (2026-10-12)

Status: **PARTIAL / SOURCE-BOUND / NOT ACCEPTED**. Exact source contents were retrieved in this pass; this adds requirements, not implementation or qualification evidence.

| Stable requirement ID | Primary source and revision | Requirement / invariant | Responsible domain / dependencies | Required acceptance evidence | Current state |
|---|---|---|---|---|---|
| COMPONENT-ADMIT-01 | `docs/checkpoints/mediahub-github-component-final-manifest-2.0.md` @ `main`, blob `45988bf9da202c9597d0ca2de50e92e5c2e6ed55`, §§1, 2, 7 | Component selection does not grant production qualification; MediaHub owns public contracts, State Authority, identity/policy, privacy, recovery/update authority, production admission, provenance and audit. Third-party internal state is never canonical MediaHub state. | Component admission; MH-1…MH-24; State Authority; security/privacy; recovery/update | Trace selected component to a MediaHub-owned adapter/contract; prove no authority transfer; record exact source/version/license/SBOM/signature/provenance | Manifest status `CANONICAL DEVELOPMENT INPUT`; implementation open; no component qualification inferred |
| COMPONENT-ADMIT-02 | Same manifest, §§4–6, 8–9 | Target-gated/future-gated components require evidence-based capability gap, immutable provenance/version, security and adapter review, functional/negative/failure/degraded-mode tests, recovery/rollback where applicable, performance/resource benchmark, independent qualification and replacement plan. Explicit exclusions and no duplicate authority/runtime remain binding. | Component selection; MH-6 resource governance; MH-12 security; MH-15/16 lifecycle; MH-22 qualification | Per-component gate dossier with all §8 evidence and governance decision before production admission | Selection reconciliation closed in manifest; implementation and production admission remain open/qualification-gated |
| P007-READ-01 | `docs/architecture/P0-07-read-validate-boundary.md`, blob `ceb4e40ea3c41e0b4ec1d3e70eccc4616c77001f` (retrieved by immutable blob SHA; path listed in map) | Read operations are observation-only; no second canonical config/policy store and no State Authority mutation. An explicitly supplied immutable domain object must not be represented as canonical persisted state. | P0-07; P0-03…P0-06; State Authority; config/policy ownership | Static trace and negative tests showing read path cannot write or persist and has no implicit canonical source | Source verified; implementation/qualification evidence not inspected in this pass |
| P007-VALIDATE-01 | Same P0-07 source, “Validate” | Validation is deterministic and bounded; reject unsupported resource types, malformed identity/namespace/schema/scope, excessive structure/size, non-finite numbers, secret/credential fields, executable policy, unsupported effects/rules and unauthorized scope expansion. | P0-07; schema/contracts; security; authorization | Boundary tests for each rejection class, bounded-input tests and evidence of deterministic results | Requirements recorded; tests not run and no implementation claim |
| P007-POLICY-01 | Same P0-07 source, “Policy evaluation” and “Current implementation boundary” | Policy evaluation is observation-only; `ConfigurationPolicyOperationBoundary` is authorization/validation only and does not publish state while the P0-07 → P0-05 mutation authorization gap remains unresolved. P0-07 is not persistence/cache/checkpoint/recovery/alternate authority. | P0-07 → P0-05; Policy; Authorization; Consumer Boundary; State Authority | Explicit authority-path contract; prove no write path bypass; governance resolution of mutation authorization gap before implementation is treated as complete | Mutation authorization gap explicitly unresolved; production qualification not granted |

### Confirmed source-location correction

- The canonical component manifest is at `docs/checkpoints/mediahub-github-component-final-manifest-2.0.md`, not the initially attempted `mediahub-canonical-component-manifest-2.0.md` path. Its current `main` blob SHA matches the map pointer: `45988bf9da202c9597d0ca2de50e92e5c2e6ed55`.
- The P0-07 source path in the map returned 404 via Contents API, but the exact blob SHA recorded in the map (`ceb4e40ea3c41e0b4ec1d3e70eccc4616c77001f`) was retrievable and its contents were read. This verifies source content by immutable blob, not that the path currently exists on `main`.
- No tests, qualification, provider/model calls, credentials, installation, host inspection, infrastructure changes, deployment, migration or merge occurred. Matrix remains **PROPOSED / NOT ACCEPTED / NOT FROZEN / NOT IMPLEMENTED / NOT QUALIFIED**.
