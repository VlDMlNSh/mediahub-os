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
| AG-20 | The purchased Mac Pro is named as the developer primary workstation, while the owner blueprint also names a Mac Pro in the future production target; the text does not establish whether this is one physical asset or two | Owner blueprint and §5 hardware profile matrix | OPEN / ASSET ALLOCATION REQUIRED | Create distinct inventory/profile entries, or record an explicit role-transfer decision and developer replacement plan before production admission; never assume one unit can serve both roles concurrently |

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
| Durable task execution / recovery | Temporal — https://github.com/temporalio/temporal | GitHub release page observed 2026-10-12 lists v1.32.1, released 2026-10-08; repository describes durable workflows, retries and fault-tolerant execution | Strong lifecycle candidate; service/operational footprint and a second queue/state layer could conflict with Astra. Compare at the same requirement set before choosing | CANDIDATE / NOT SELECTED |
| Agent state graph / human approval | LangGraph — https://github.com/langchain-ai/langgraph | Release page observed 2026-10-12 lists langgraph 1.2.13 dated 2026-10-05; repository activity shows recent maintenance; documentation covers stateful workflows and human-in-the-loop control | Candidate for agent-local control flow; not a replacement for project policy or canonical task/claim authority. Avoid duplicating lifecycle if Temporal or Astra owns it | CANDIDATE / NOT SELECTED |
| Multi-agent framework / .NET + Python | Microsoft Agent Framework — https://github.com/microsoft/agent-framework | Microsoft’s 2026-04-03 v1.0 announcement describes a production-ready release, stable APIs and long-term support for Python and .NET, plus A2A/MCP interoperability | Strong candidate for cross-runtime needs; vendor readiness statements do not prove MediaHub fit. Evaluate offline/local operation, dependency size, provider coupling and Mac profile compatibility | CANDIDATE / NOT SELECTED |
| Typed Python agents and handoffs | Pydantic AI — https://github.com/pydantic/pydantic-ai | Multi-agent guide covers delegation, programmatic handoffs and graph-based control flow; release page observed 2026-10-12 lists v2.51.0 dated 2026-09-25 | Good candidate for typed task envelopes and Python agents; rapid release cadence means exact pins, migration policy and regression qualification are required | CANDIDATE / NOT SELECTED |
| Isolated coding worker / SDK | OpenHands — https://github.com/OpenHands/OpenHands ; SDK: https://github.com/OpenHands/software-agent-sdk | Public SDK supplies Python, TypeScript and REST interfaces; Agent Server can use ephemeral isolated workspaces, while the associated automation project owns scheduling/dispatch history | Candidate bounded coding-worker adapter, not Jarvis project memory, lifecycle authority, MediaHub State Authority or independent verifier; inspect isolation, licensing, egress and resource cost | CANDIDATE / NOT SELECTED |
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
- Temporal release tags: https://github.com/temporalio/temporal/releases
- LangGraph releases and activity: https://github.com/langchain-ai/langgraph/releases and https://github.com/langchain-ai/langgraph/activity
- Pydantic AI releases: https://github.com/pydantic/pydantic-ai/releases
- OpenHands Software Agent SDK repository: https://github.com/OpenHands/software-agent-sdk

These are source leads checked for capability and lifecycle signals, not a substitute for pinned-version, license, security, integration, performance and recovery qualification.

## 13. Next controlled gates

1. Preserve the updated Passport v3 and Contract 01 as branch-only drafts; their Jarvis/hardware changes have been read back and indexed in the map.
2. Build the source/branch inventory and exact node-profile inventory; distinguish user-reported equipment intent from independently measured facts.
3. Define Jarvis public interfaces and choose one owner for task lifecycle, claims, evidence and qualification promotion.
4. Run read-only component evaluation and scorecard first; any PoC tests, installation or qualification require a separate authorized step.
5. Generate the MH-01…MH-23 domain context packets only from reviewed primary sources; retain each source ref/SHA and open conflict.
6. Pin each node’s OS/boot/install/update/recovery profile against B2 §9 before packaging; do not infer it from the Apple hardware name.
7. Obtain independent architecture review and an explicit owner acceptance/change-control record before calling Passport v3 or the Jarvis contract accepted or canonical.

## 14. Nomenclature change history

The current owner wording “Jarvis” supersedes the earlier working label “Astro” from the same date. The report filename is intentionally unchanged to preserve existing map/cross-reference lineage. The distinction between Jarvis (umbrella engineering architecture), ASTRA (bounded engineering subsystem), and MediaHub (product/domain plane) is unchanged. This update is documentary only; no runtime, installation, qualification, deployment, baseline or production state changed.

## 15. Follow-up source finding: hardware role does not specify operating-system profile

The accepted B2 document (`docs/checkpoints/mediahub-functional-baseline-2.0.md`, `main`, blob SHA `1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f`, §9) says clean Mac mini/Mini PC installations use Linux as the baseline implementation direction, while Apple platforms remain integrated platform adaptations where the base OS cannot be replaced. The owner’s role labels (Mac Pro, developer Mac mini 2011 and customer-site Mac mini M2) do not by themselves specify which OS/build, boot mode, installation path, update mechanism or recovery image is intended for each target. This is an unresolved profile decision, not evidence of a contradiction or permission to change the baseline.

**Required gate:** record the OS/runtime/boot/install/update/recovery profile separately for each hardware target and verify compatibility, support status, security updates, drivers and rollback before producing a release bundle. No OS, firmware, runtime or deployment was changed in this follow-up.

**Final disposition:** the owner’s Jarvis concept is captured as a structured working architecture and gap register, now with 20 scoped findings. AG-20 is a post-cycle follow-up; it does not change the recorded 13-cycle documentary review ledger. The report is not yet a fully accepted system contract, does not imply implementation, and does not authorize live-system changes.


**External evidence refresh (2026-10-12):** release/activity signals above are snapshots for shortlist quality only. They do not select a component, establish compatibility with the target Mac profiles, prove security suitability or authorize a PoC. The working decision remains one lifecycle owner, one agent-runtime choice as needed, and an isolated coding worker only if requirements justify it. Exact candidate commits/tags, licenses, dependency/security posture, supported-platform matrix and bounded verification evidence remain required.

## 16. GitHub repository metadata snapshot — read-only, 2026-10-12

**Method:** read-only GitHub API requests to each repository endpoint and `/commits?per_page=1` on 2026-10-12. This records an observation snapshot, not a future-pinned dependency selection. Star/fork counts are discovery context only and are not a maturity score. GitHub API license identifiers do not substitute for a full transitive-license/legal review.

| Candidate | Repository / current default branch | API license | Stars / forks at retrieval | Repository pushed_at | Latest commit SHA / committer date | Role assessed | Current decision |
|---|---|---:|---:|---|---|---|---|
| Temporal Server | [temporalio/temporal](https://github.com/temporalio/temporal), `main` | MIT | 23,626 / 1,992 | 2026-10-12T11:40:19Z | `30c625664a2bbc1bd4cd9022d71982cc473e6979` / 2026-10-10T21:03:36Z | Durable workflow execution, retries and restart recovery | CANDIDATE / NOT SELECTED; separate server + database add operational cost and could duplicate task state |
| LangGraph | [langchain-ai/langgraph](https://github.com/langchain-ai/langgraph), `main` | MIT | 43,125 / 7,329 | 2026-10-12T02:54:17Z | `799c2f04fd3a56186e24e9fb8bbf3568e543cfbe` / 2026-10-11T12:51:09Z | Stateful agent graph, checkpoints and human-in-the-loop | CANDIDATE / NOT SELECTED; agent-local flow only unless explicitly chosen as the single lifecycle owner |
| Microsoft Agent Framework | [microsoft/agent-framework](https://github.com/microsoft/agent-framework), `main` | MIT | 14,075 / 2,460 | 2026-10-12T11:36:44Z | `a75e803ef6ec5c01adb2859e4a4a2f2867694533` / 2026-10-12T09:39:28Z | Cross-language Python/.NET agent and workflow framework | CANDIDATE / NOT SELECTED; evaluate local/offline mode, dependencies, host profile, and provider coupling |
| Pydantic AI | [pydantic/pydantic-ai](https://github.com/pydantic/pydantic-ai), `main` | MIT | 20,571 / 2,904 | 2026-10-12T09:29:32Z | `ff25d3d83ff5d8e0bf5bde433cdc26f4f9959c2f` / 2026-10-12T09:28:55Z | Typed Python agents, delegation/handoff, optional graph control flow | CANDIDATE / NOT SELECTED; promising for typed contracts, but does not decide durable queue ownership |
| OpenHands application | [OpenHands/OpenHands](https://github.com/OpenHands/OpenHands), `main` | MIT | 90,689 / 12,007 | 2026-10-12T10:42:38Z | `738b23d2d63cac01db3a4cf37263b87aaba3a195` / 2026-10-12T09:48:32Z | Coding-agent application and execution experience | CANDIDATE / NOT SELECTED; must prove isolation, filesystem/network permissions, provider data handling and actual-node resource fit |
| OpenHands Software Agent SDK | [OpenHands/software-agent-sdk](https://github.com/OpenHands/software-agent-sdk), `main` | MIT | 1,242 / 644 | 2026-10-12T09:13:30Z | `e3a26821f8f7c85e98078c7b5e1a80647fc7d0c7` / 2026-10-12T05:23:46Z | Modular coding-agent runtime/SDK | CANDIDATE / NOT SELECTED; compare its runtime boundaries and dependency footprint against the application repo before selecting either |
| AutoGen | [microsoft/autogen](https://github.com/microsoft/autogen), `main` | CC-BY-4.0 (repository-level metadata) | 61,375 / 9,280 | 2026-04-15T11:59:09Z | `027ecf0a379bcc1d09956d46d12d44a3ad9cee14` / 2026-04-06T22:35:32Z | Legacy multi-agent framework | NOT RECOMMENDED FOR NEW ADOPTION; repository explicitly says maintenance mode and directs new users to Microsoft Agent Framework |

**Evidence source:** public GitHub API `GET /repos/{owner}/{repo}` and `GET /repos/{owner}/{repo}/commits?per_page=1`, retrieved 2026-10-12. The table pins a latest-commit observation for comparison only; it does not approve that commit as a dependency pin.

**Analysis limits and decision rule:**
- Temporal is the strongest listed *durable execution* candidate in this list, not automatically the right Jarvis orchestrator: its service/database footprint and overlap with an existing queue must be evaluated.
- LangGraph and Pydantic AI are primarily agent-control/runtime abstractions; do not treat either as a substitute for an explicit owner of task lifecycle, claims, leases, fencing and promotion.
- Microsoft Agent Framework merits a bounded shortlist evaluation due to its current 1.0 release posture and multi-agent workflow support, but “production-ready framework” does not qualify the MediaHub integration or the named Apple hardware.
- OpenHands application and SDK should remain separate candidates; repository activity and popularity do not establish sandbox safety, repeatability or fit for the developer Mac mini 2011.
- AutoGen’s maintenance-mode status plus repository-level CC-BY-4.0 metadata makes it a poor default for new adoption absent explicit exception and a separate legal/dependency review.
- No candidate was installed, benchmarked, tested, security-reviewed transitively, selected as canonical or production-qualified in this metadata pass. The next decision requires a pinned version, license/SBOM analysis, supported OS/CPU matrix, isolated proof of concept, failure/recovery evidence, measured resource use on the admitted profile, removal/rollback plan and independent review.


## 17. Follow-up finding: developer Mac Pro versus future production Mac Pro

**Finding AG-20 — OPEN / ASSET ALLOCATION REQUIRED.** The supplied blueprint assigns the purchased Mac Pro to the developer environment as the primary workstation and also describes a future production deployment centered on Mac Pro + Mac mini. The source does not establish whether the production Mac Pro is a separate future asset or the same purchased developer workstation. This is a physical-asset and trust-domain ambiguity, not permission to transfer or reclassify a host.

**Safe contract:** maintain separate inventory/profile records for the developer workstation and the production target. If they are different physical machines, the asset records must prove that distinction. If they are the same machine at different times, require an explicit role-transfer decision, a replacement developer-workstation plan, removal of developer/customer credential crossover, a clean deployment profile, and an approved recovery/rollback path before promotion. No serial numbers, hostnames or model names alone prove qualification.

**Evidence required to close:** owner-confirmed asset allocation; exact model/year/CPU/architecture/RAM/storage/OS for each profile; designated trust domain and allowed data/secrets; approved role transition if applicable; release manifest and post-deployment evidence bound to the exact package SHA/profile. No host was inspected or changed as part of this documentary finding. The recorded 13 cycles remain the earlier scoped review ledger; AG-20 is a subsequent follow-up, not an added runtime test or retroactively counted cycle.


## 18. Follow-up finding: B1 §15 document-assistance mapping points to the wrong B2 section

**Finding AG-21 — OPEN / TRACEABILITY CORRECTION REQUIRED.** A direct read-back of the immutable B2 source at `docs/checkpoints/mediahub-functional-baseline-2.0.md@main`, blob SHA `1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f`, confirms that §16 is “Documents and Knowledge”, §18 is “AI architecture”, and §19 is “Update / Recovery / Migration”. Audit 01, `docs/checkpoints/MH24-B1-SECTIONS-03-06-12-15-17-CLAUSE-COVERAGE-AUDIT-01.md`, blob SHA `d0938f14ed4110545118f075175dee3be412097b`, currently maps B1 atom `B1-15-13` (“Assist with documents”, B1 §15 line 246) to B2 §19. That section reference is incorrect for document assistance. The correct review target is B2 §§16/18.

**Classification:** confirmed cross-reference / traceability defect in a derived audit pointer; **not** evidence of a semantic contradiction between B1 and B2. B1 remains the immutable literal source for its edition; B2 remains the accepted current functional reference. Do not rewrite the historical Audit 01 artifact or infer implementation from this correction.

**Controlled correction:** the working atom-level crosswalk `docs/checkpoints/MH24-BATCH-04-ATOM-LEVEL-CROSSWALK-BATCH-06-DRAFT.md`, blob SHA `9df96aca53d1004c33d45f038501dc6b7f52c0c9`, uses B2 §§16/18 and explicitly records the historical Audit 01 mismatch. Its review `docs/checkpoints/MH24-BATCH-04-ATOM-LEVEL-CROSSWALK-BATCH-06-REVIEW-01.md`, blob SHA `1edc976dd663ae16a1b61876a2dbbde9411be095`, confirms the B2 heading names and the correction. Both are documentary drafts; semantic acceptance remains OPEN.

**Required disposition:** preserve Audit 01 as history; correct current derivative references when those derivative artifacts are next approved/maintained; include this mismatch in source-pointer validation so a future crosswalk does not propagate it. Do not promote the associated requirement mapping or acceptance criteria based solely on a corrected section number.

**Cycle accounting:** AG-21 is a post-cycle source-reference follow-up. It does not increase or rewrite the recorded 13 blueprint-specific documentary cycles and is not a runtime test, qualification, or production evidence.

**Boundaries:** no B1/B2, main-branch matrix, canonical backlog, runtime, infrastructure or hardware was changed or operated. No test, qualification, installation, deployment, host action or merge occurred.