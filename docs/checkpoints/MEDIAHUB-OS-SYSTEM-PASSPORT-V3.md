# MediaHub OS / MediaHub iOS — системный паспорт v3

- **Дата составления:** 2026-10-12
- **Ветка:** `docs/mediahub-chat-tree-map-20261012`
- **Статус:** `INTEGRATED WORKING DRAFT / NOT YET ACCEPTED AS A NEW BASELINE`
- **Назначение:** свести действующие функциональные решения, архитектурные инварианты, доменные контракты, hardware-профили, component status и gates в один проверяемый обзор.
- **Нормативное ограничение:** этот паспорт не переписывает и не заменяет Baseline 2.0, Baseline 1.0 или доменные контракты. До отдельного решения владельца он служит обзором и индексом к первичным источникам.

## 1. Краткое определение системы

MediaHub OS — единая local-first платформа для локального пользовательского контура MediaHub OS/Core и MediaHub iOS/iPadOS, а также отдельно изолированного корпоративного контура инженерной разработки. Платформа объединяет управление доменным состоянием, Smart Home, медиа, документы и знания, Digital Twin/Engineering, сеть, локальный и кластерный AI, мобильные интерфейсы, recovery/update и управляемый developer compute fabric.

**Jarvis (latest owner-provided target framing, 2026-10-12):** Jarvis is the umbrella multi-agent engineering architecture for source discovery, project memory, dependency-aware task planning, bounded execution, independent verification and reproducible release preparation. ASTRA/Astra Gold is one candidate execution/queue/evidence subsystem within that umbrella, not the architectural foundation for the whole system. Jarvis and Astra remain engineering-plane entities; neither gains MediaHub product-state authority. “Jarvis” is a working architecture label recorded in this branch, not evidence of a deployed runtime or a renamed repository.

**Текущая функциональная точка отсчёта:** Functional Baseline 2.0, принятый и обозначенный как canonical immutable reference. Baseline 1.0 сохраняется как неизменяемый исторический literal source своей редакции. Принятие baseline не доказывает реализацию, верификацию, qualification или production readiness.

- B2: `docs/checkpoints/mediahub-functional-baseline-2.0.md`, `main`, blob SHA `1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f`.
- B1: `specification/MEDIAHUB-FUNCTIONAL-BASELINE-1.0.md`, `main`, blob SHA `9df4892ed0734050ac79732603d15bb414717310`.
- MH-24 reconciliation: `docs/checkpoints/mediahub-mh24-reconciliation-report.md`, `main`, blob SHA `d07d162ebaa57643a7bdd84d6fb13a1102b87bfc`.

## 2. Source-of-truth hierarchy

При чтении источников применяются разные роли источников, а не единое недифференцированное правило «самый новый файл выигрывает».

1. **Продуктовая семантика:** принятый B2 задаёт текущую функциональную reference-модель. B1 сохраняет буквальные исторические требования редакции 1.0 и используется для source-anchored crosswalk; его требования не считаются автоматически сопоставленными с B2.
2. **Доменные контракты:** уточняют только собственную явно указанную область. Принятый доменный контракт действует в своих границах; PROPOSED, CANDIDATE, FUTURE-GATED и branch-only материалы не являются автоматическим расширением B2.
3. **Последующие одобренные решения:** могут уточнять предшествующие решения в рамках полномочий и области решения. Нужны явный approval record, refs и scope. Дата/новизна документа сама по себе не подтверждает approval.
4. **Матрицы, reconciliation reports и checkpoints:** показывают трассируемость, историю и состояние на дату; не подменяют baseline или runtime evidence.
5. **Generated truth / gate evidence:** фактическая истина о квалификации берётся из канонического машинного источника и свежих evidence для точного SHA. Исторические run и документы не продвигают текущий gate.
6. **Этот паспорт и сводный контракт:** являются рабочими синтезирующими документами; не отменяют первичные источники без отдельного принятия.

### Контрольные источники и SHA

| Source | Ref | Blob SHA | Использование |
|---|---|---|---|
| B2 functional baseline | `main` | `1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f` | Текущий функциональный reference |
| B1 functional baseline | `main` | `9df4892ed0734050ac79732603d15bb414717310` | Literal historical provenance, 68 sections |
| MH-24 reconciliation report | `main` | `d07d162ebaa57643a7bdd84d6fb13a1102b87bfc` | Evidence of B2 acceptance/closure |
| MH-24 traceability matrix, corrected working copy | `docs/mediahub-chat-tree-map-20261012` | `73377891072bac3c739c44055ceeb0874154f64c` | 68-row section matrix; implementation/qualification remain open |
| Canonical component manifest 2.0 | `main` | `45988bf9da202c9597d0ca2de50e92e5c2e6ed55` | Development component selection, not production approval |
| ASTRA GOLD governance contract | `main` | `1d3ac25e7817f365807ad85d0d7c9007bd48bebf` | ASTRA qualification gates and internal workflow controls |
| ASTRA launch/qualification schema, annotated working copy | `docs/mediahub-chat-tree-map-20261012` | `0b86b07dfa916d4485ce1f8f54d19de136d98491` | Qualification/lifecycle schema; clarified ASTRA internal state scope |
| ASTRA execution blueprint, annotated working copy | `docs/mediahub-chat-tree-map-20261012` | `9f199ba8e872d5ae188fcdac9635a53f16973534` | Roles and execution gates; clarified ASTRA internal state scope |
| Generated ASTRA current truth | `main` | `48d581a8f6a6a5fd380abbb7a7ce938b3b1e6731` | Current reported result: `NOT_PROVEN / BLOCKED` |
| Jarvis blueprint gap reconciliation (legacy file name includes ASTRO) | `docs/mediahub-chat-tree-map-20261012` | `8495c9436b967bd77afae57ccb1e42959ab86a56` | Latest owner-provided Jarvis scope, 20 scoped findings including AG-20 asset allocation, component candidates and 13 documentary review cycles |

## 3. Authority, command and state model

### 3.1 Authority boundaries

| Domain / responsibility | Authority | Explicitly not authority |
|---|---|---|
| Canonical MediaHub platform state | MediaHub Product State Authority | AI, cloud, UI, adapters, provider, event bus, graph/search/vector/object store, scheduler, telemetry, backup or update mechanism |
| Smart Home operational/device state | Home Assistant Core within the Smart Home domain | MediaHub UI/AI and external smart-home ecosystem integrations |
| Engineering queue, leases, workflow evidence and qualification-gate state | A0-ASTRA inside the ASTRA engineering control plane | MediaHub Product State Authority; product-state mutations |
| Architecture definition | A1 role within ASTRA workflow | Final product/security/release authorization |
| Bounded implementation | A2 | Independent verification or self-promotion |
| Independent verification | A3 | Self-verification of its own change |
| Final release/launch authority | Human approval gate | Autonomous agents, models, workers or candidate systems |

ASTRA uses the term `state_authority` only for its own workflow/control state: queue, claim/lease, evidence and gate progression. It does not establish ASTRA as authority for MediaHub canonical product state. A0-ASTRA coordinates engineering; it is not the product State Authority.

### 3.2 Canonical mutation path

`Command → Validation → Authorization/Policy → Consumer/Integration Contract → owning Domain Authority → Canonical Mutation → Event/Fact → Observers`

The owning authority depends on the domain; Smart Home domain operations remain under Home Assistant Core. Events and telemetry describe facts, they do not themselves authorize mutations. UI, AI, plugin, provider, adapter, knowledge graph, persistence and workflow mechanisms do not gain authority merely by being connected.

### 3.3 State vocabulary

Do not conflate `reported`, `observed`, `desired`, `policy-allowed`, `commanded`, `committed`, `applied`, `confirmed` and `predicted` state. A request is not a committed result; a dispatched command is not proof of physical application; observation is not authority. Accepted mutations must carry authoritative version/revision and provenance under the relevant domain contract.

### 3.4 Failure behavior

- Unknown, malformed, stale, unauthorized, ambiguous or unqualified inputs are rejected, denied, quarantined or handled as defined by the owning contract; critical ambiguity fails closed.
- Failure of Product State Authority must not manufacture a second product authority or an ungoverned fallback path.
- Degraded operation is permitted only for a specifically qualified capability profile and explicit policy; it is not a generic bypass of authorization, privacy or state ownership.
- Health is observational. `UNKNOWN` does not become `READY` optimistically.
- Recovery restores authoritative state and provenance; recovery mechanisms are not themselves state authority.

## 4. Product boundaries and functional coverage

The product is one functional architecture deployed across hardware-qualified profiles.

| Capability family | Contract boundary / status |
|---|---|
| OS/Core and platform | Capability profile and explicit runtime contracts; do not infer target installation from architecture text |
| Smart Home and devices | Home Assistant Core owns Smart Home operations; adapters are qualification-gated |
| UI and navigation | Unified MediaHub UI; UI4-04 remains `HOLD / CROSS-LINK-ONLY` until unique residual requirement evidence exists |
| Media and camera/NVR | Separate media/data plane; device/media services remain target-gated until each capability is qualified |
| Documents and knowledge | B2 defines PostgreSQL + pgvector + S3-compatible storage as the functional target baseline; Component Manifest marks the concrete implementations TARGET-GATED, so installation/qualification is not implied; OCR/graph/search integrations are derived |
| Digital Twin / Engineering | Domain-owned metadata and provenance; large artifacts use object contract; candidate tools are target-gated |
| Local / cluster AI | AI proposes or computes under policy; no direct physical/product authority |
| Cloud development | Separate corporate domain, no default raw-user-data mirror or canonical product authority |
| Mobile | MediaHub Core on iOS/iPadOS is a local profile; Remote Access is a separate role; Developer Mobile is separate from user-data domain |
| Identity/security/privacy | Identity, trust, authorization, policy, least privilege, segmentation, egress and audit precede mutation/egress |
| Persistence and knowledge | Storage/indexes/caches are not authority unless the approved domain contract explicitly assigns authority; no silent authority transfer |
| Update / backup / recovery / migration | Lifecycle/recovery authorities remain distinct from State Authority; RAUC is a target only where the selected OS/profile supports it and qualification passes; no competing unapproved OTA authority |
| Observability | Metrics/logs/traces are non-mutating; minimise payloads and exclude secrets |
| Developer Compute Fabric | Corporate engineering domain; qualified contributed compute is not user-data access and not a flat shared cloud |
| Astra Gold | Independent engineering qualification/control plane with exact-SHA-bound evidence and explicit human launch gate |

This table indicates functional coverage and boundaries, not that every listed component is implemented or production-qualified.

## 5. Hardware and deployment profiles

### 5.1 Design direction

The target architecture must support a Mac Pro-class developer/build profile, Mac mini service/prototype profiles and optional later GPU/video expansion. The specific inventory below is **owner-reported intent**, not independent hardware discovery or qualification. Do not conflate the developer Mac mini 2011 with the client-site Mac mini M2 prototype or with an unspecified future Mac mini production profile.

| Hardware / node class | Owner-reported role | Admission constraint |
|---|---|---|
| Purchased Mac Pro | Primary developer workstation; also informs the future high-performance Mac Pro profile | Exact model/year/chip/GPU/RAM/storage/OS are not provided; no capability claim until inventory and workload benchmark |
| Mac mini 2011, 16 GB | Developer “Lynx” / low-resource or legacy test node | Exact identifier, OS support, security-update status and runtime compatibility are unknown; it must not be a mandatory dependency for the future stack |
| Mac mini M2 at the customer site | First working MediaHub prototype at the client location | Separate customer trust domain; not retained in the developer-server pool, no inherited developer secrets/data or automatic worker registration |
| Current developer servers | Test/qualification stand only | Not the target production environment; operate only after fresh host/identity/disk/health preflight and separate authorization |
| Future GPU/video server | Optional later expansion for admitted media/video/GPU workloads | Not required for core correctness; requires workload-specific driver, codec, isolation, thermal, memory and recovery evidence |

**OS/boot/install profile gap:** B2 §9 states that clean Mac mini/Mini PC installations use Linux as the baseline implementation direction, while Apple platforms remain integrated adaptations where the base OS cannot be replaced. The Mac Pro, developer Mac mini 2011 and customer-site Mac mini M2 role labels do not pin each target's OS/build, boot mode, installer, update path or recovery image. These must be approved and qualified per node; do not infer an OS from the hardware name.

The owner-reported deployment intent is “toward the end of October 2026”. This is a planning window, not a guaranteed release date or production authorization. The current component and runtime evidence does not demonstrate readiness for this window.

### 5.2 Capability evidence required per node

At a minimum, profile CPU, GPU/NPU and VRAM, RAM, NVMe and other storage I/O, network interfaces and measured bandwidth/latency, Thunderbolt/USB4 capability where present, media/AI acceleration, thermal and power envelope, reliability/uptime, available capacity, OS/runtime compatibility, security posture, isolation ability and current identity/source revision.

Admission follows:

`Hardware Detection → Capability Qualification → Capability Profile → Trust/Policy Admission → Workload Lease → Execution → Verification/Evidence`

Capability drift triggers requalification or a policy downgrade. Marketing specifications alone are not scheduling evidence.

### 5.3 Hardware roles

- **Mac mini node:** prototype, low-resource or service role only when the exact profile is supported and measured; no inherent permanent coordinator/master role. The 2011 development node and customer-site M2 prototype are distinct trust/profile entries.
- **Mac Pro / GPU expansion:** a potential high-throughput build/compute target admitted per workload, privacy classification, capacity and qualification evidence. The purchased developer Mac Pro and any future production Mac Pro are not assumed to be the same physical asset; resolve P-20 before production admission. GPU presence does not imply pooled VRAM, compatible runtime or workload admission.
- **Developer/test servers:** retain TEST/STAGING status until an explicit per-node reclassification; no production inference from a hostname, installed process or prior run.
- **Future GPU/video node:** optional accelerator pool behind workload admission; the platform must retain useful core operation when this node is absent.
- **Mac/iOS/iPadOS and specialist profiles:** feature availability follows qualified OS and hardware capabilities; shared UX does not mean identical capability.
- **Single-node profile:** valid. HA, multi-node quorum, durable persistence and distributed State Authority are not assumed merely because future clustering is intended.

## 6. Network and data planes

Maintain explicitly separate policy-controlled planes:
1. user-facing MediaHub control/API plane;
2. local Media/Data plane;
3. Smart Home and physical-device integration boundaries;
4. developer mesh/control plane;
5. qualified HIGH_SPEED developer compute/storage interconnect;
6. optional storage plane;
7. bounded API egress/cloud-development paths;
8. qualification/evidence transport and management plane.

The HIGH_SPEED developer fabric must not become a default path for ordinary user MediaHub traffic. CPRG is bounded to API-key registration; it is not a general VPN, user traffic gateway or shared egress. Media/Data, developer compute, user data and development artifacts are not interchangeable scopes.

AP/radio, Wi-Fi controller, gateway/router, switching, roaming, backhaul and vendor interoperability are separate capabilities. “Seamless Wi-Fi” is a functional target whose implementation requires hardware/vendor qualification, not a license to assume compatibility.

## 7. Canonical component-selection interpretation

The current Component Manifest 2.0 is a **canonical development input**, not a declaration that each selected or listed runtime is installed or production-qualified.

| Subsystem | Current documented selection posture |
|---|---|
| Relational substrate | PostgreSQL target-gated implementation under MediaHub schemas/invariants |
| Vectors and knowledge | pgvector in the foundation; Qdrant only with benchmark evidence |
| Object storage | S3-compatible interface selected; implementation replaceable; SeaweedFS target-gated |
| Contracts/RPC | Protobuf and gRPC selected |
| Telemetry | OpenTelemetry Collector and Prometheus; telemetry is never correctness/authority |
| Secrets and supply chain | SOPS + age, Cosign, Syft and Trivy selected for their respective bounded purposes |
| Updates | RAUC target; target-gated by platform qualification |
| General compute | Ray primary candidate for AI/data workloads; Nomad secondary/general infrastructure candidate; neither presumed deployed or qualified |
| Compute mesh | OpenFabric feasibility candidate; does not transparently pool GPU VRAM; not qualified by its inclusion |
| Workflow/events/coordination | Temporal, NATS JetStream and etcd future-gated until a measured capability gap and governance decision |
| Knowledge/search | OpenSearch/Neo4j future-gated; not foundation by default |
| Local inference | ONNX Runtime / llama.cpp target-gated; vLLM/SGLang future-gated |
| Media | MediaMTX, go2rtc and whole-product candidates remain target-gated/conditional per device, privacy, performance and recovery qualifications |
| Network primitives | WireGuard/Netmaker and high-speed interconnect remain subject to plane-specific qualification |

No candidate receives authority by inclusion in this table. Licensing, provenance, security, performance, data locality, operations and recovery gates must all be satisfied before production admission.

## 8. Privacy and security invariants

- User Data X Developer Cloud / Developer Compute Fabric / Developer Personnel Access.
- Prefer local processing; external processing must be policy-approved, workload-scoped, minimised, time-bounded and auditable.
- Synthetic, sanitised or explicitly permitted non-user fixtures are used for qualification.
- Identity, authorization, policy, capability admission and credential boundaries are enforced before work/egress.
- Credentials are not committed to Git or included in evidence. Credentials require expiry, rotation, revocation and audit.
- Admitted workloads use isolated workspaces, bounded capabilities, leases/timeouts and provenance-bound results.
- Provider availability, model presence, registration, installation and process visibility do not equal qualification.
- Any unresolved security, data-classification or authority ambiguity blocks the risky operation.

## 9. Lifecycle and release truth

Keep these states distinct:

`IDEA → DESIGN → IMPLEMENTED → TESTED → VERIFIED → QUALIFICATION CANDIDATE → QUALIFIED → RELEASED → DEPLOYED → OBSERVED → PRODUCTION ACCEPTED`

The actual owning workflow may contain more specific states, but no stage is skipped by inference. Human authorization is required where the launch/production contract requires it. Historical CI/run evidence cannot qualify a different SHA or current live deployment.

ASTRA Gold current truth in the inspected main source reports `NOT_PROVEN / BLOCKED`; live three-node transport is not yet qualified and historical soak evidence is not current qualification. No claim of active autonomous queue execution, successful 24-hour soak, GOLD, release or production is made by this passport.

## 10. Known reconciliation gaps and risks

| ID | Issue | Current disposition | Evidence / next gate |
|---|---|---|---|
| P-01 | B1 literal atom ↔ B2 semantic mapping not complete for every parent/atom | OPEN | Batch 04 source-anchored crosswalk has 48 historical parents: 4 `MAPPED`, 3 `NO_DIRECT_COUNTERPART`, 41 `NOT_REVIEWED`, 0 `CONFLICT` at parent level; atom-level mapping still required |
| P-02 | Historic backlog says “47” while there are 48 unique parent IDs | PRESERVE HISTORY / USE VERIFIED COUNT IN NEW RECORDS | Do not rewrite historical backlog; count is verified in validation/crosswalk artifacts |
| P-03 | UI4-04 unique requirement not evidenced | HOLD / CROSS-LINK-ONLY | Owner decision; do not mint child ID/claim literal requirement before evidence |
| P-04 | B2 accepted but former matrix status was pre-acceptance candidate | CORRECTED IN WORKING BRANCH | Corrected matrix SHA `73377891072bac3c739c44055ceeb0874154f64c`; `main` was not changed |
| P-05 | Astra `state_authority: A0-ASTRA` wording could be confused with product authority | SEMANTIC SCOPE CLARIFIED IN WORKING BRANCH | Schema and blueprint comments, and executor-capability matrix; machine values preserved to avoid unauthorized schema change |
| P-06 | HA Core vs Product State Authority boundary | DOMAIN SPLIT DOCUMENTED; DETAIL OPEN WHERE CONTRACT IS PROPOSED | B2 §§3,14; `architecture/STATE-HA-INTEGRATION-CONTRACT.md` remains future/proposed, not current runtime authority |
| P-07 | HA/persistence target vs MH-03 frozen single-node in-memory runtime | KEEP SEPARATE; GOVERNANCE GATE REQUIRED | Do not promote PostgreSQL/etcd/NATS HA target without explicit governance, compatibility and acceptance |
| P-08 | Mac Pro/GPU and heterogeneous node profiles | FUTURE TARGET; NOT QUALIFIED | Hardware inventory, benchmarks, drivers/runtime, thermals, isolation, privacy and workload-specific evidence required |
| P-09 | Component selection may be mistaken for installation/qualification | NO INFERENCE PERMITTED | Manifest gate §8; all target/future-gated components require measured evidence |
| P-10 | Current ASTRA GOLD / live queue state | NOT PROVEN / BLOCKED | Fresh exact-SHA node, executor, transport, runtime, scheduler, fencing, recovery, A3 and soak evidence required |
| P-11 | Full domain stage acceptance for MH-01…MH-25 is not uniform | OPEN / SOURCE-BY-SOURCE | Chat tree map is inventory/navigation, not proof of full stage closure |
| P-12 | Whole-repository semantic completeness | NOT CLAIMED | Tree inventory contains 826 entries; this session audited the baseline, key contracts, manifests, traceability and qualification sources, not every line of every Markdown file |
| P-13 | Jarvis umbrella vs Astra subsystem was not explicit in the original v3 synthesis | WORKING SCOPE ADDED; NOT CANONICAL | Jarvis gap reconciliation SHA 8495c9436b967bd77afae57ccb1e42959ab86a56; implementation/runtime evidence absent |
| P-14 | Owner-reported hardware roles require exact inventory | OPEN / NOT QUALIFIED | Mac Pro model, mini 2011 identifier/OS, customer M2 site profile and future GPU server specs are not independently verified |
| P-15 | Jarvis must not duplicate task lifecycle/state across orchestration and Astra/framework candidates | OPEN DESIGN DECISION | Select one owner for queue/claim/lease/retry/evidence; use adapters around other execution frameworks |
| P-16 | Master-context packet for MH-01…MH-23 is not implemented as an auditable release mechanism | DESIGN REQUIREMENT | Global context + domain packets must carry source refs/SHA, current decisions, dependencies and change deltas |
| P-17 | Reusable-repository scorecard and pinned release bundle are not yet implementation artifacts | DESIGN REQUIREMENT / OPEN | Exact pins, license/SBOM/security, compatibility, preflight, rollback and post-install evidence required |
| P-18 | Public multi-agent repositories are candidate sources only | NOT SELECTED / NOT QUALIFIED | New review document lists Temporal, LangGraph, Microsoft Agent Framework, Pydantic AI, OpenHands and AutoGen status; no component installed or qualified |
| P-19 | Target OS/build/boot/install/update/recovery profiles are not pinned for the named Apple hardware roles | OPEN / PLATFORM PROFILE REQUIRED | B2 §9, blob SHA `1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f`; gap reconciliation §15, latest blob SHA `8495c9436b967bd77afae57ccb1e42959ab86a56` |
| P-20 | Purchased Mac Pro is described as the primary developer workstation while a future production Mac Pro is also named; physical-asset identity/transfer is unresolved | OPEN / ASSET ALLOCATION REQUIRED | Gap reconciliation §17 / AG-20, latest blob SHA `8495c9436b967bd77afae57ccb1e42959ab86a56`; owner blueprint |

## 11. Acceptance checklist for a future Passport v3 release
- [ ] Resolve AG-20/P-20: distinguish the developer Mac Pro from the future production Mac Pro, or approve and evidence an explicit role transition with a replacement developer workstation and credential/data boundary.

The owner/governance acceptance package must verify at least:
- [ ] No semantic contradiction with accepted B2.
- [ ] B1-to-B2 crosswalk and applicable literal/derived classifications reviewed at atom level.
- [ ] Every architecture claim has a primary-source path, ref, blob SHA and status.
- [ ] Every capability has an owning authority, command/event path, failure behavior and acceptance criteria.
- [ ] No non-authority subsystem is implicitly promoted.
- [ ] Product and developer domains, traffic planes and data boundaries remain separated.
- [ ] Hardware targets are explicitly separated from measured/qualified profiles.
- [ ] Candidate/selected/target-gated/future-gated/installed/verified/qualified statuses are not conflated.
- [ ] UI4-04 remains HOLD until evidence.
- [ ] Astra Gold claims are consistent with fresh generated current truth and exact-SHA evidence.
- [ ] Independent architecture review and owner approval are recorded.
- [ ] Any baseline supersession is a separate explicit decision; B1/B2 are not edited by this draft.
- [ ] Jarvis is explicitly defined as an engineering umbrella; Astra remains a bounded subsystem and neither crosses the MediaHub product authority boundary.
- [ ] Mac Pro, developer mini 2011, client-site mini M2, test servers and future GPU/video node are distinct inventory/profile/trust records.
- [ ] A Jarvis task envelope has source/base SHA, domain, dependencies, allowed capabilities, isolated workspace, acceptance criteria, independent verifier and evidence digest.
- [ ] One and only one selected subsystem owns task lifecycle/claims/leases/retries; agent frameworks cannot create a competing queue or state authority.
- [ ] The reusable-component scorecard and pinned, reproducible deployment/rollback bundle have independent review and measured profile evidence.
- [ ] A global Jarvis context packet and all MH-01…MH-23 domain packets point to primary docs instead of copying or silently overwriting them.

## 12. Change history

| Date | Change |
|---|---|
| 2026-10-12 | Initial integrated working draft created from current B2, B1 provenance, MH-24 report/matrix, component manifest and architecture/qualification contracts. |
| 2026-10-12 | Records corrected working-matrix status and ASTRA internal-control-state clarification without changing B1, B2, machine contract values or main. |
| 2026-10-12 | Added owner-provided Jarvis umbrella framing, separated Astra subsystem scope, detailed owner-reported hardware roles, and linked the Jarvis blueprint gap report; remains a working draft. |

**Final status:** integrated working passport, not a new accepted baseline; implementation, tests, qualification, deployment and production acceptance are not established by this document.

| 2026-10-12 | Applied the latest owner terminology: Jarvis supersedes the earlier draft label Astro. Updated the gap-report SHA to its latest read-back; retained the legacy filename for cross-reference provenance. |
| 2026-10-12 | Added a per-node OS/boot/install/update/recovery profile gate from B2 §9 and refreshed the gap-reconciliation blob SHA; no baseline or runtime changed. |
| 2026-10-12 | Added a read-only GitHub API metadata snapshot for seven orchestration/agent candidates to gap-report §16; recorded current commit/license/activity observations without treating stars or activity as qualification. Updated all gap-report references to blob SHA `406e33a480d195915f7ab8963836066988ee2fd0`; no candidate selected and no runtime or baseline changed. |

- 2026-10-12 — added P-20 after cross-reading the owner blueprint and the working hardware matrix: developer and future production Mac Pro asset identity/role transfer remains unresolved. Updated current AG-20 gap-report pointers to SHA `8495c9436b967bd77afae57ccb1e42959ab86a56`; no host or baseline changed.
