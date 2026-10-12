# Jarvis / MediaHub multi-agent architecture — blueprint gap reconciliation 01 (stable historical path: MEDIAHUB-ASTRO-BLUEPRINT-GAP-RECONCILIATION-01.md)

- **Date:** 2026-10-12
- **Ref:** docs/mediahub-chat-tree-map-20261012
- **Status:** OWNER-SUPPLIED BLUEPRINT ANALYSIS / WORKING DOCUMENT — NOT A NEW ACCEPTED BASELINE
- **Nomenclature update (2026-10-12):** the latest owner-provided blueprint names the umbrella concept **Jarvis**. An earlier same-day wording used “Astro”; Jarvis supersedes that draft label for the current working architecture. The repository path is retained for provenance and backward-compatible references. This does not rename ASTRA, rename the MediaHub product, or assert that Jarvis is implemented or deployed.
- **Purpose:** reconcile the latest user-provided Jarvis concept with the current MediaHub architecture, source-of-truth hierarchy, hardware profile plans, ASTRA workflow contracts, component-selection policy and qualification truth.
- **Scope:** documentary architecture only. No software installed; no tests/qualification executed; no infrastructure or production changed; no changes to B1/B2 or main.

## 1. Executive finding

The latest owner-provided blueprint establishes a new system-level framing: **Jarvis is the umbrella multi-agent engineering architecture; Astra is one subsystem within it, not the architectural foundation for the whole system.** That framing is compatible with MediaHub’s existing authority invariants only when three planes remain separate:

1. **Jarvis engineering/orchestration plane** — project memory, requirements, agents, source collection, planning, task coordination, verification, evidence and controlled deployment preparation.
2. **Astra subsystem** — a candidate execution/queue/evidence component within Jarvis. Its current architecture and useful contracts may be reused selectively, but current runtime truth is NOT_PROVEN / BLOCKED; it is not assumed to be a qualified foundation.
3. **MediaHub product plane** — MediaHub OS/Core, MediaHub State Authority and domain systems. Jarvis/Astra workers cannot acquire product-state mutation authority. Home Assistant Core remains authority only in the Smart Home domain.

At the start of the earlier blueprint pass, Passport v3 and Verifiable Architecture Contract 01 lacked explicit umbrella scope, complete hardware-role separation, reusable deployment-package requirements, MH-01…MH-23 context packet requirements and a repository-selection scorecard. Those omissions were added to the working branch copies. Their read-back SHAs at that stage—Passport v3 `33ccb08dd098562f6ae9172044e205fc4810e336` and Contract 01 `15c272e31a4276dccc6d7e0b15d1dc1ac836b49a`—are historical provenance, not current pointers. Current blob SHAs are maintained in `MEDIAHUB-CHAT-TREE-MAP.md` to avoid circular self-references between companion artifacts. Both documents remain drafts, not canonical baselines. Measured hardware facts, lifecycle ownership, component qualification, implementation, independent review and owner acceptance remain open. No baseline was silently replaced.

## 2. Authority and source precedence

### 2.1 Governing sources read

| Source | Ref / blob SHA | What it proves | Limitation |
|---|---|---|---|
| Functional Baseline 2.0 | main / 1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f | Accepted current functional reference; defines product/domain authority and developer boundary | Does not prove implementation or qualification |
| Functional Baseline 1.0 | main / 9df4892ed0734050ac79732603d15bb414717310 | Historical literal passport source; contains the original functional design | No silent semantic equivalence with B2 |
| MH-24 reconciliation report | main / d07d162ebaa57643a7bdd84d6fb13a1102b87bfc | Reports B2 accepted/canonical; keeps implementation/qualification separate | Documentation acceptance is not runtime evidence |
| Traceability matrix | working branch / 73377891072bac3c739c44055ceeb0874154f64c | Reconciled matrix status; implementation/qualification remains open | Some implementation and qualification cells remain empty or partial |
| MH-03 master prompt | main / e99035f596e236645bf8f2235fc4d375716ce476 | Current foundation is single-node, in-memory State Authority; single-node/no HA; physical persistence not authorized | Proposed changes need separate governance |
| State/HA integration contract | main / aa68e876d06980ced3e6b6b3995ea6a117446423 | PostgreSQL/etcd/NATS are future candidates only | Explicitly not current runtime authority |
| Component manifest 2.0 | main / 45988bf9da202c9597d0ca2de50e92e5c2e6ed55 | Development component selection and qualification gates | Selection is not installation, acceptance or production admission |
| Astra current truth | main / 48d581a8f6a6a5fd380abbb7a7ce938b3b1e6731 | G0–G11 BLOCKED; overall NOT_PROVEN / BLOCKED | Generated evidence is time/ref specific |
| Astra 24h runbook | main / efb1c8af47578cbe14f8e788676d71ba4c665966 | Live three-node transport not yet qualified; stale worker health schema is a blocker described there | Not proof of current host status after the source date |
| Jarvis owner blueprint | conversation input dated 2026-10-12 | Owner’s intended framing and hardware role descriptions | Conversational input has no repository blob SHA; physical models/inventory not independently verified |

### 2.2 Precedence rule

The new blueprint is the current owner-provided design direction for the working draft. It does **not** silently amend accepted B2, unfreeze B1, promote a proposed domain contract, or prove a component or host is operational. Any baseline change remains a separate explicit governance action.

## 3. Gap register

| ID | Gap / conflict | Evidence | Required correction | Current disposition |
|---|---|---|---|---|
| AG-01 | Jarvis is named as the overarching system, but the repo’s canonical engineering workflow is currently named Astra/Astra Gold | Owner blueprint versus ASTRA qualification contracts | Define Jarvis as an umbrella architecture and Astra as a replaceable/adaptable subsystem; do not rename existing machine identifiers or schemas implicitly | DRAFTED; owner review still required |
| AG-02 | “Do not rely on the current Astra implementation” can be misread as “discard all Astra contracts” or “assume Astra works” | Owner blueprint; ASTRA current truth is NOT_PROVEN / BLOCKED | Reuse validated concepts/interfaces selectively; runtime admission remains blocked until fresh evidence; compare before replacing scheduler/claim stores | OPEN until implementation comparison and qualification |
| AG-03 | Product authority and engineering workflow state can be conflated | B2 §§3–4; MH-03 master prompt; ASTRA schema comment clarifies its internal state | Jarvis/Astra owns engineering task state only. MediaHub State Authority owns canonical product state; HA Core owns Smart Home state within its domain | Architectural boundary specified; conformance evidence open |
| AG-04 | Four node roles are not explicit together in the current passport | Latest owner input versus existing hardware and network checkpoints | Distinguish Mac Pro developer workstation, Mac mini 2011 16-GB developer/low-resource node, client-site Mac mini M2 prototype, current server test stand, and future optional GPU/video server | Documented as owner-reported target intent; hardware evidence open |
| AG-05 | Hardware identity is not sufficiently specified for deterministic deployment | “Mac Pro” model/year and the 2011 mini model/build are missing | Record model identifier, CPU/GPU/NPU, RAM, disks, NIC, OS build/support, driver/runtime, thermals and workload benchmarks before profile qualification | BLOCKED for hardware qualification |
| AG-06 | Mac mini 2011 compatibility is assumed by role name rather than capability evidence | Only 16 GB RAM and model year provided in owner input | Do not make it a mandatory dependency for modern build/runtime services; prove OS, architecture, security updates, dependency and resource compatibility; otherwise limit it to isolated legacy/low-resource tests | OPEN; no compatibility claim made |
| AG-07 | Client Mac mini M2 might inadvertently remain in developer compute or credential scope | Owner says it is the first customer-site prototype and should not remain with developer servers | Define separate customer trust domain, identities, secrets, logs and data; no automatic worker registration into developer cluster; admission requires explicit site policy | Contract requirement drafted |
| AG-08 | Current servers are being used as test stand but may be conflated with production | Owner blueprint; historical project constraints mention full root disk on mh-dev-01; ASTRA evidence reports transport/health gaps | Label all current server resources TEST/STAGING until individually reclassified; no cleanup or host operation without fresh diagnosis and authorization | Mandatory boundary; no host action taken |
| AG-09 | “Deploy, do not build from scratch” lacks a release-package contract | Owner blueprint; Component Manifest and qualification gates | Produce versioned, signed/provenance-bound deployment bundle, per-profile manifest, preflight, dependencies/SBOM/licenses, secrets provisioning, health gates, backup/rollback and post-deploy evidence | Design requirement; no installer/package exists by this report |
| AG-10 | Reuse policy lacks uniform candidate scorecard and rejection rules | Owner blueprint; existing component manifest §8 | Require repository identity, license, maintained release, provenance, dependencies, vulnerability policy, compatibility, offline/local mode, resource use, recovery, tests and integration cost; never use stars alone | Scorecard specified below |
| AG-11 | The existing custom Astra queue may overlap with a new Jarvis orchestrator | ASTRA workflow contracts have claims, leases, scheduling, evidence and promotion; blueprint elevates Jarvis | Avoid two independent task queues/state stores. Jarvis must either wrap one admitted executor/scheduler behind an adapter or explicitly delegate the entire execution lifecycle to that subsystem | Architecture decision required before implementation |
| AG-12 | “Agents” may be implemented as too many permanent bots | ASTRA capability matrix and B2 role/capability model | Define stable capability profiles; instantiate workers per task/dependency. 26 ECC/specialist roles, if retained, are capabilities/catalogue entries—not a target of 26 always-on processes | Draft rule; resource benchmark open |
| AG-13 | Master prompt distribution across MH-01…MH-23 can fork knowledge or rewrite domain decisions | Project map and per-domain primary documents | One global context contract plus a domain-routing manifest; generate bounded domain packets with exact source refs/SHA, invariants, dependencies, status and change delta; each packet must point back to canonical documents | Design requirement; implementation not built |
| AG-14 | “Complete GitHub and chat scan” can be claimed beyond actual coverage | The prior tree snapshot at commit 58305d5a9a5b1593f15d2dfb0ff79838c1bddaec counted 826 entries / 445 Markdown files; earlier review read selected critical sources, not every line of every file | Keep a machine-readable inventory and per-file states: discovered, fetched, classified, reviewed, superseded, unresolved. Report percentage and unreviewed scope; never call a partial semantic review “full” | Mandatory audit discipline |
| AG-15 | Component maturity and compatibility evidence can decay | External repositories release continuously; GitHub search is only candidate discovery | Pin exact tag/commit and retrieval date; record license, release/activity, advisories, SBOM, tested platforms and benchmark evidence; rerun qualification at target hardware | No third-party candidate qualified |
| AG-16 | The “end of month” target can be interpreted as a release guarantee | Owner reports deployment expected toward the end of October 2026 | Treat it as a planning window, not a release/production date; exit depends on all gates and approved hardware, not calendar pressure | Schedule/acceptance date remains unapproved |
| AG-17 | The current architecture does not define a stable Jarvis-to-domain interface | MH-01…MH-25 domain map; B2 and component manifest | Each Jarvis module must declare capabilities, input/output schema, source refs, owner, dependencies, timeout/retry/idempotency, security boundary and acceptance tests | Contract fields proposed |
| AG-18 | External multi-agent frameworks could create competing graph, scheduler, memory and state layers | Candidate frameworks each offer different workflow abstractions | Separate durable execution from agent reasoning; select one owner for task lifecycle; agent framework remains an adapter/worker runtime, not policy or product authority | Candidate comparison required; no selection yet |
| AG-19 | Apple hardware names do not determine the actual target OS, boot/install path or update-recovery model | B2 §9, line 227: clean Mac mini/Mini PC installs use Linux as baseline direction; Apple platforms are integrated adaptations where the base OS cannot be replaced | Pin an explicit OS/build, boot mode, supported runtime, update and recovery profile for each node before release packaging; do not infer macOS/Linux from the hardware name | OPEN — PLATFORM PROFILE REQUIRED |

## 4. Target architecture proposed by the owner blueprint

This is a **working architecture proposal**, not a deployment diagram for an already-running system.

### 4.1 Planes

1. **Jarvis governance and project-memory plane** — chat-tree map; source inventory; decision/evidence ledger; versioned global and domain context packets; architecture contract registry; requirement and change traceability.
2. **Jarvis orchestration plane** — decomposes approved work, orders dependencies, limits concurrency, assigns capability profiles, tracks retries/leases, stops on conflicts and coordinates independent verification.
3. **Agent execution plane** — source collector, domain analyst, validator, normalizer, bounded builder, documentation author and independent reviewer. Profiles are task-scoped and may be backed by different providers/models, subject to admission.
4. **Tool and integration plane** — GitHub, browser/web retrieval, filesystem, CI, provider/model adapters and local runtime tools; each adapter has explicit read/write capabilities and an audit record.
5. **Verification/evidence plane** — structural/schema validation, semantic cross-check, source-anchor verification, security/privacy checks, independent A3 review, hash-bound artifact manifest and read-back.
6. **Astra subsystem boundary** — may implement task/claim/worker/verification/evidence flows after qualification. It is not the Jarvis source of truth by default; no second scheduler or evidence store without an explicit decision.
7. **MediaHub product plane** — MediaHub OS/Core and product/domain state. No Jarvis/Astra agent, model, plugin, network, workflow or cloud service can bypass MediaHub State Authority.
8. **Deployment plane** — prepares an immutable release package, profile-specific configuration and preflight/rollback evidence; installation and production activation remain separately authorized stages.

### 4.2 Agent flow

SOURCE INVENTORY → REQUIREMENT / DECISION CLASSIFICATION → DEPENDENCY DAG → CLAIMED ISOLATED WORKSPACE → TASK-SCOPED WORKER → STRUCTURAL VALIDATION → SEMANTIC REVIEW → INDEPENDENT A3 VERIFICATION → HASHED EVIDENCE / MANIFEST → READ-BACK → CONTROLLED INTEGRATION.

No source mutation is implied by discovery. One writer per shared file or contract surface. A worker must declare base ref/SHA and changed paths. Failed or contradictory evidence moves the task to BLOCKED / RECONCILIATION_REQUIRED; it does not self-promote. A3 cannot certify its own work.

### 4.3 Minimal task envelope

Every dispatched task should carry: task ID and parent ID; MH domain; requirement IDs; owner/approval reference; base ref and exact SHA; source inventory and trust level; task role/capability profile; declared dependencies; allowed tools/files/network/egress; isolated workspace; timeout/lease/retry/idempotency policy; acceptance criteria; verifier identity; outputs and changed-path manifest; evidence digest; exit status and next allowed lifecycle state. No credential value is written to the task/evidence record.

## 5. Hardware and deployment profile matrix

| Node/profile | Owner-reported role | Intended allowed use | Explicitly not assumed | Required admission evidence |
|---|---|---|---|---|
| Purchased Mac Pro | Developer primary workstation | Source analysis, builds, integration, local test orchestration, artifact preparation according to measured profile | Exact year/chip/GPU/RAM/OS and performance are unknown; not automatically a production server | Exact model and system inventory; supported OS/toolchain; disk/backup; CPU/GPU and workload benchmarks; security, isolation and recovery |
| Mac mini 2011, 16 GB | Developer “Lynx” / MediaHub low-resource node | Legacy/compatibility test profile and bounded low-resource services only if supported by measured compatibility | Not a mandatory dependency for the target system; not assumed to support current OS or dependency versions; not a customer production node | Exact identifier/architecture/OS; support and patch state; storage/NIC; thermal/resource measurements; all required runtimes and security controls |
| Mac mini M2 at client site | First customer-site MediaHub prototype | Customer-isolated prototype and acceptance; deployment rehearsal using the approved bundle | Not a permanent developer-server member; no inherited developer credentials/data or automatic compute contribution | Customer trust-domain setup; approved identity/secrets; network/egress profile; privacy test; rollback/recovery; customer acceptance |
| Current developer servers | Test/staging stand only | Reproducible tests and qualification after explicit authorization and safe host diagnosis | Not the production target; no assumption that ASTRA queue/three-node transport is qualified | Fresh inventory, disk/health preflight, node identity, exact commit/SHA, isolated test data, task/transport evidence |
| Future GPU/video server | Optional future expansion | Media/video acceleration or admitted GPU/AI workloads behind resource and privacy policy | Not required for core correctness or first deploy; GPU presence is not workload qualification | GPU/model/driver/codec matrix; thermals/power; memory and throughput tests; sandbox and data residency/egress gate; failure/recovery behavior |

**Boundary:** host class is descriptive only. Admission is capability-based; no node earns a profile from its product name. The “end of October” date is an owner-reported planning window, not a guaranteed release date.

### 5.1 Reproducible deployment package

The target is deployment of a previously built and verified release, not ad hoc assembly on new hardware. The package contract should include:
- versioned manifest with source/build SHA, supported architecture/OS ranges, dependency locks and checksums;
- license notices and SBOM/provenance metadata for reused components;
- profile configuration and secret references (never secret values);
- preflight results and resource/capability compatibility gate;
- deterministic install/upgrade steps with checkpoints;
- schema/config migration plan where relevant;
- health/readiness probes and operator-visible failure reasons;
- backup/restore and a tested rollback target;
- post-install evidence bound to the same release SHA and node profile.

Containerization is not made mandatory by this blueprint: packaging must account for different OS/CPU generations and avoid making the 2011 test node a hidden dependency. No deployment artifact or production acceptance is claimed here.

## 6. Reusable component / repository decision matrix

Public repositories are discovery candidates only. This is a documentary desk review as of 2026-10-12; no repository was installed, benchmarked or qualified in this session.

| Concern | Candidate | Evidence observed | Fit / risk | Working status |
|---|---|---|---|---|
| Durable task execution / recovery | Temporal — https://github.com/temporalio/temporal | Public durable-execution service; workflows survive process/service failures through recorded execution state | Strong candidate for evaluating durable tasks, retries and restart recovery. Operational footprint and another task-state layer could conflict with Astra’s queue; decide only after an architecture spike | CANDIDATE / NOT SELECTED |
| Agent state graph / human approval | LangGraph — https://github.com/langchain-ai/langgraph | Describes stateful, long-running agents, persistence and human-in-the-loop control | Candidate for agent-local control flow; not a replacement for project policy or canonical task/claim authority. Avoid duplicating durable orchestration if Temporal or Astra owns lifecycle | CANDIDATE / NOT SELECTED |
| Multi-agent framework / .NET + Python | Microsoft Agent Framework — https://github.com/microsoft/agent-framework | Microsoft announced v1.0 on 2026-04-03 as production-ready for Python and .NET; supports multi-agent workflows and interoperability | Candidate where cross-language integration and maintained support matter; test offline/local execution, dependency size, provider coupling and Mac profile compatibility | CANDIDATE / NOT SELECTED |
| Typed Python agents and handoffs | Pydantic AI — https://github.com/pydantic/pydantic-ai | Official guide covers delegation, programmatic handoffs and graph-based control flow; docs explicitly say graphs are not necessary for every use case | Good candidate for typed task envelopes and schema validation in a Python-heavy repo; keep control flow simple until measured complexity requires a graph | CANDIDATE / NOT SELECTED |
| Isolated coding worker / SDK | OpenHands — https://github.com/OpenHands/OpenHands ; SDK: https://github.com/OpenHands/software-agent-sdk | Public coding-agent project and modular SDK are actively maintained according to GitHub’s repository page (observed Oct 2026) | Candidate execution adapter for bounded coding tasks, not project memory, scheduler, A0, State Authority or verifier of its own work; inspect isolation, dependencies, licensing and runtime resource costs | CANDIDATE / NOT SELECTED |
| Legacy multi-agent framework | AutoGen — https://github.com/microsoft/autogen | Repository states it is in maintenance mode and directs new projects to Microsoft Agent Framework | Do not start a new Jarvis integration on AutoGen without an explicit exception and migration rationale | NOT RECOMMENDED FOR NEW ADOPTION |

### 6.1 Selection rule

Do not combine several frameworks merely to maximize agent count. The initial evaluation should compare:
1. one durable execution owner (existing Astra queue versus a durable workflow engine such as Temporal);
2. one agent runtime/graph option (Pydantic AI, LangGraph or Microsoft Agent Framework);
3. one isolated coding-worker option if required (OpenHands SDK or a qualified existing worker).

Use a stable Jarvis adapter contract so candidates can be replaced without changing product authority, task envelope or evidence format. A selection decision requires pinned version/tag/commit, license and supply-chain review, platform compatibility, bounded isolated PoC, recovery/replay evidence, resource profile on actual hardware and independent review. Stars, marketing statements, repository existence and historical CI do not qualify a component.

## 7. Master context and MH-01…MH-23 distribution

Create one versioned global Jarvis context packet that contains only system-wide invariants, source precedence, status vocabulary, change protocol and links to the current map. Each MH domain packet should be generated or maintained as a bounded view containing:
- domain purpose and interfaces;
- exact primary-source paths/refs/blob SHAs and decision status;
- dependencies and consumers;
- non-negotiable invariants relevant to the domain;
- accepted, superseded, proposed and open decisions separated explicitly;
- required changes since the previous packet;
- acceptance criteria, evidence and next gate.

Do not paste full duplicated domain documents into every chat. A packet points to primary documents and carries only an auditable summary. The global prompt routes work; it does not grant architecture approval or authorize writes. After each accepted change, update the source document first, read it back, then refresh the map and only then refresh dependent packets. MH-24/MH-25 are reconciliation/control stages, not new MH-01…MH-23 product requirements.

## 8. Reuse and repository review scorecard

Every candidate repository or extracted module needs a record with: canonical repository identity; exact source URL and pin; release/tag and last activity observed; maintainers/review process; SPDX license and redistribution obligations; security policy/advisories; dependency/SBOM and provenance; supported CPU/OS matrix; required services and resource profile; offline/local mode; sandbox and permissions; persistence/migration model; network/egress behavior; API/extension boundary; test coverage and failure/recovery probes; adapter cost; rollback/removal path; decision owner; and lifecycle status.

Scorecard outcomes:
- **REJECT** — unacceptable license/security, identity ambiguity, unbounded egress, incompatible runtime or competing authority.
- **REFERENCE ONLY** — useful design but not an executable dependency.
- **CANDIDATE** — promising, but unqualified.
- **POC QUALIFIED** — passes a bounded test on a recorded profile; not production-admitted.
- **SELECTED FOR DEVELOPMENT** — governance decision plus pinned source and integration plan.
- **PRODUCTION QUALIFIED** — only after independent workload-specific qualification and production approval.

## 9. Thirteen analysis → correction → re-analysis cycles

The following are 13 focused review cycles for the newly supplied Jarvis blueprint. They are documentary source/contract passes; **they are not 13 runtime test runs or production qualification runs**.

| Cycle | Initial defect / risk found | Correction applied in this reconciliation | Re-analysis result / residual gate |
|---|---|---|---|
| 01 — Identity | Jarvis and Astra could be treated as synonyms | Set Jarvis as umbrella; Astra as one subsystem | Names separated in the proposed architecture; repository-wide renaming is prohibited without a separate decision |
| 02 — Baseline precedence | Latest blueprint could be treated as silent B2 replacement | Kept B2 accepted and B1 immutable/historical; new design is a supplement | No baseline changed; v3 acceptance remains open |
| 03 — Authority | Orchestration state could be mistaken for product state | Separated Jarvis/Astra engineering state from MediaHub State Authority and HA Smart Home authority | Architectural rule clear; runtime conformance not verified |
| 04 — ASTRA truth | Existing queue docs could be treated as proof ASTRA runs | Checked generated current truth and runbook; preserved NOT_PROVEN/BLOCKED | No current-GOLD claim; fresh exact-SHA runtime gates remain blocked |
| 05 — Agent cardinality | “Multi-agent” could imply one daemon per role / 26 always-on bots | Recast specialist roles as capability profiles instantiated per task | Correctness/resource testing still required |
| 06 — Hardware roles | Test servers, dev nodes and client prototype could mix trust and release responsibilities | Defined distinct Mac Pro, 2011 mini, client M2, test stand and future GPU profile | Hardware facts need node inventory and owner acceptance |
| 07 — Legacy compatibility | 2011 mini could become a hidden dependency for modern build/runtime | Made it an optional constrained/legacy profile pending OS/runtime evidence | Compatibility remains unknown; no unsupported claim |
| 08 — Deployment | “Deploy, do not build” lacked a verifiable release envelope | Added pinned manifest, SBOM/license metadata, preflight, health, backup/rollback and post-deploy evidence | No bundle/installer created or tested |
| 09 — Reuse | Repository maturity could be inferred from stars or README alone | Added license, provenance, security, support, platform, recovery and benchmark scorecard | Candidate scan is not qualification |
| 10 — Orchestration overlap | Jarvis, Astra, Temporal and an agent framework might each own scheduling/state | Separated durable execution from agent reasoning; require one task-lifecycle owner and adapters | Selection is intentionally open pending comparison |
| 11 — MH context | Master prompt copies could drift across 23 domains | Specified one global packet plus domain packets that point to primary docs and exact SHAs | Packet generator/workflow is not implemented |
| 12 — Qualification/release | Calendar pressure or a deployment commit might imply production acceptance | Required independent per-profile gates and explicit promotion decisions | “End of month” remains planning intent only |
| 13 — Completeness claims | Prior repository inventory could be misreported as a line-by-line semantic audit | Preserved 826-entry/445-Markdown historical snapshot scope and disclosed focused semantic coverage | Full-repository semantic completion remains open |

## 10. Proposed requirement-to-component matrix

| Requirement / outcome | Candidate owner/component | Status | Principal risk | Acceptance evidence |
|---|---|---|---|---|
| Cross-session project memory and source map | Existing chat-tree map + versioned Jarvis context packet | DESIGN DRAFT | stale copied context; untraceable decisions | source refs/SHA and read-back for every changed packet |
| Task DAG, dependencies and ownership | Jarvis contract + one selected scheduler/queue | OPEN | duplicated state and non-idempotent retries | conflict, lease, retry, fencing and replay probes |
| Durable tasks across process/node failures | Astra subsystem or Temporal candidate | CANDIDATE | double scheduler; operational complexity | interrupted task and state-restore PoC on exact SHA |
| Multi-agent delegation | Pydantic AI / LangGraph / Microsoft Agent Framework candidates | CANDIDATE | framework lock-in; agents share excess context | isolated delegation, schema validation, human pause/stop and A3 review |
| Bounded coding execution | OpenHands SDK or existing qualified worker | CANDIDATE | unsafe filesystem/network access; own-work certification | workspace/network sandbox tests and independent result review |
| Independent verification | A3 capability profile; distinct executor identity | DESIGN REQUIREMENT | same model/identity reviews its own edits | reviewer independence evidence and changed-path/source checks |
| Repo reuse | Candidate registry and scorecard | DESIGN REQUIREMENT | stale, incompatible or license-incompatible dependencies | exact pin, license/SBOM/security and compatibility report |
| Local-first operation | Local orchestrator and qualified local execution profile | B2 INVARIANT / IMPLEMENTATION OPEN | cloud/provider outage becomes hard dependency | negative egress and cloud-loss tests when authorized |
| MediaHub product state | MediaHub State Authority; HA Core only for Smart Home | B2 INVARIANT | Jarvis/Astra/AI bypass | command-path, authorization and negative-path evidence |
| Mac Pro developer profile | hardware capability profile | OWNER-REPORTED / NOT MEASURED | unknown SKU/resources | inventory, benchmark, disk/recovery and toolchain check |
| Mac mini 2011 low-resource profile | compatibility/legacy testing | OPEN | obsolete OS/runtime/security assumptions | exact model/OS and supported dependency matrix |
| Client Mac mini M2 prototype | isolated customer deployment profile | OWNER-REPORTED / NOT QUALIFIED | developer/customer data and credential crossover | separate identity/network, privacy, recovery and acceptance |
| Future GPU/video capacity | optional GPU executor/media pool | FUTURE-GATED | unqualified driver/codec/data path; core dependence | per-workload GPU/codec benchmark, isolation and failover |
| Reproducible deployment | signed versioned release bundle | DESIGN REQUIREMENT | drift/manual setup/rollback failure | clean-profile install, preflight, health, restore and rollback evidence |
| Full architecture acceptance | passport v3 + integrated contract + map/crosswalk | DRAFT / OPEN | claiming acceptance from documentation alone | independent review, owner approval, explicit version/change-control action |

## 11. Decisions intentionally not taken

- No framework (Temporal, LangGraph, Microsoft Agent Framework, Pydantic AI or OpenHands) was installed or chosen as canonical.
- Existing ASTRA is neither discarded nor promoted as the foundation; it remains a candidate subsystem whose current qualification status is blocked.
- No live server or client device was inspected or changed in this pass.
- Mac Pro exact model, Mac mini 2011 OS/support state, and GPU server specifications remain unknown.
- No assumption is made that current test hardware is production hardware.
- No deployment date, production acceptance, release, or “Astra Gold” status is granted.
- B1, B2, main, existing domain contracts and the canonical component manifest are unchanged.

## 12. External reference set checked on 2026-10-12

- Temporal repository: https://github.com/temporalio/temporal
- Temporal durable-execution documentation: https://docs.temporal.io/temporal
- LangGraph repository and documented capabilities: https://github.com/langchain-ai/langgraph
- Microsoft Agent Framework: https://github.com/microsoft/agent-framework
- Microsoft Agent Framework 1.0 announcement (2026-04-03): https://devblogs.microsoft.com/agent-framework/microsoft-agent-framework-version-1-0/
- Pydantic AI multi-agent guide: https://github.com/pydantic/pydantic-ai/blob/main/docs/multi-agent-applications.md
- Pydantic Graph guidance: https://github.com/pydantic/pydantic-ai/blob/main/docs/graph.md
- OpenHands: https://github.com/OpenHands/OpenHands
- OpenHands Software Agent SDK: https://github.com/OpenHands/software-agent-sdk
- AutoGen repository status (maintenance mode; new projects directed to Microsoft Agent Framework): https://github.com/microsoft/autogen

These are source leads checked for capability and lifecycle signals, not a substitute for pinned-version, license, security, integration, performance and recovery qualification.

## 13. Next controlled gates

1. Preserve the updated Passport v3 and Contract 01 as branch-only drafts; their Jarvis/hardware changes have been read back and indexed in the map.
2. Build the source/branch inventory and exact node-profile inventory; distinguish user-reported equipment intent from independently measured facts.
3. Define Jarvis public interfaces and choose one owner for task lifecycle, claims, evidence and qualification promotion.
4. Run read-only component evaluation and scorecard first; any PoC tests, installation or qualification require a separate authorized step.
5. Generate the MH-01…MH-23 domain context packets only from reviewed primary sources; retain each source ref/SHA and open conflict.
6. Pin each node’s OS/boot/install/update/recovery profile against B2 §9 before packaging; do not infer it from the Apple hardware name.
7. Obtain independent architecture review and an explicit owner acceptance/change-control record before calling Passport v3 or the Jarvis contract accepted or canonical.

## 15. Follow-up source finding: hardware role does not specify operating-system profile

The accepted B2 document (`docs/checkpoints/mediahub-functional-baseline-2.0.md`, `main`, blob SHA `1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f`, §9) says clean Mac mini/Mini PC installations use Linux as the baseline implementation direction, while Apple platforms remain integrated platform adaptations where the base OS cannot be replaced. The owner’s role labels (Mac Pro, developer Mac mini 2011 and customer-site Mac mini M2) do not by themselves specify which OS/build, boot mode, installation path, update mechanism or recovery image is intended for each target. This is an unresolved profile decision, not evidence of a contradiction or permission to change the baseline.

**Required gate:** record the OS/runtime/boot/install/update/recovery profile separately for each hardware target and verify compatibility, support status, security updates, drivers and rollback before producing a release bundle. No OS, firmware, runtime or deployment was changed in this follow-up.

**Final disposition:** the owner’s Jarvis concept is captured as a structured working architecture and gap register, now with 19 scoped findings. It is not yet a fully accepted system contract, does not imply implementation, and does not authorize live-system changes.

## 14. Nomenclature change history

The current owner wording “Jarvis” supersedes the earlier working label “Astro” from the same date. The report filename is intentionally unchanged to preserve existing map/cross-reference lineage. The distinction between Jarvis (umbrella engineering architecture), ASTRA (bounded engineering subsystem), and MediaHub (product/domain plane) is unchanged. This update is documentary only; no runtime, installation, qualification, deployment, baseline or production state changed.
