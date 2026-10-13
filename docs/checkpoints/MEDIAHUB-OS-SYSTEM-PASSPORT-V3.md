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
| Jarvis blueprint gap reconciliation (legacy file name includes ASTRO) | `docs/mediahub-chat-tree-map-20261012` | `39720b11e5e6777b86ffd71e0fec1214982e0d95` | Latest owner-provided Jarvis scope, 21 scoped findings including AG-20 and AG-21 asset allocation, component candidates and 13 documentary review cycles |
| Product Owner Decision Record 01 — D-06 | `docs/mediahub-chat-tree-map-20261012` | `eb6fcbad3c8324ebbdf01f71305cb3d7d4b4c0bd` | TSI-12 remains a historical sub-aspect of TSI-07; does not accept the full TSI contract |
| Batch 09 TSI crosswalk draft | `docs/mediahub-chat-tree-map-20261012` | `5e1b73c73c951638b549a30d569df2d1c7de8b31` | 17 provisional traceability labels; 3 MAPPED / 13 NOT_REVIEWED / 1 NO_DIRECT_COUNTERPART / 0 CONFLICT |
| Batch 09 TSI Review 03 | `docs/mediahub-chat-tree-map-20261012` | `184a99ef85143c2ad3048dca5c8d85b17f8651a3` | Bounded source-anchored semantic consistency review; full TSI acceptance remains OPEN |
| Batch 07 Local Cluster AI crosswalk | `docs/checkpoints/MH24-BATCH-04-ATOM-LEVEL-CROSSWALK-BATCH-07-DRAFT.md` | `d6323442e3059dda091d0ad8b2a33fa91cad6ea0` | B1 §16; 11 provisional rows; 1 MAPPED / 9 NOT_REVIEWED / 1 NO_DIRECT_COUNTERPART / 0 CONFLICT |
| Batch 07 semantic Review 02 | `docs/checkpoints/MH24-BATCH-04-ATOM-LEVEL-CROSSWALK-BATCH-07-REVIEW-02.md` | `0af17bf0db6f8b1c93d01aae3e8a8b5d8a0d9064` | One bounded documentary mapping correction; full Local Cluster AI semantic acceptance remains OPEN |
| Batch 10 AI Human Clone crosswalk | `docs/checkpoints/MH24-BATCH-04-ATOM-LEVEL-CROSSWALK-BATCH-10-AI-HUMAN-CLONE-DRAFT.md` | `44b9369fea0be06e4e64f2052fd49f6d493f6603` | 19 provisional §19 labels; 5 MAPPED / 13 NOT_REVIEWED / 1 NO_DIRECT_COUNTERPART / 0 CONFLICT; semantic and owner acceptance OPEN |
| Batch 10 Review 01 | `docs/checkpoints/MH24-BATCH-04-ATOM-LEVEL-CROSSWALK-BATCH-10-AI-HUMAN-CLONE-REVIEW-01.md` | `36148379d7d1e39252bd918ad17772036cf0d972` | Bounded structural/source-anchor/status review PASS; semantic and owner acceptance OPEN |
| Batch 10 semantic Review 02 | `docs/checkpoints/MH24-BATCH-04-ATOM-LEVEL-CROSSWALK-BATCH-10-AI-HUMAN-CLONE-REVIEW-02.md` | `612162b164b7d2585fa9646871839274cec5a343` | Bounded semantic consistency pass; 5/13/1/0 distribution remains; clone-specific semantics/owner acceptance OPEN |
| Batch 11 Mobile Access crosswalk | `docs/checkpoints/MH24-BATCH-04-ATOM-LEVEL-CROSSWALK-BATCH-11-MOBILE-ACCESS-DRAFT.md` | `0c102e5071ed5a33cbc02b00872da78eebd5bf9c` | 9 provisional §20 labels; 4 MAPPED / 5 NOT_REVIEWED / 0 NO_DIRECT_COUNTERPART / 0 CONFLICT; semantic/owner acceptance OPEN |
| Batch 11 Review 01 | `docs/checkpoints/MH24-BATCH-04-ATOM-LEVEL-CROSSWALK-BATCH-11-MOBILE-ACCESS-REVIEW-01.md` | `2a11ae52c4401a51fc562df5c9ddbe07cb83b2ef` | Structural/source-anchor/status consistency pass; Mobile Access scope, implementation and qualification OPEN |
| Batch 11 Mobile Access Review 02 | `docs/checkpoints/MH24-BATCH-04-ATOM-LEVEL-CROSSWALK-BATCH-11-MOBILE-ACCESS-REVIEW-02.md` | `c143d1b349bcf2ba3a76ffdad03b1d4258a1ebe9` | Bounded semantic review; MA-20-05 documentary MAPPED only; full Mobile Access owner/contract acceptance OPEN |
| Batch 12 Mobile Access Invariants crosswalk | `docs/checkpoints/MH24-BATCH-04-ATOM-LEVEL-CROSSWALK-BATCH-12-MOBILE-INVARIANTS-DRAFT.md` | `dcbc0a0e8a8186e926315ea318eff902e491f0e7` | 6 provisional §21 labels; 4 MAPPED / 2 NOT_REVIEWED / 0 NO_DIRECT_COUNTERPART / 0 CONFLICT; semantic/owner acceptance OPEN |
| Batch 12 Review 01 | `docs/checkpoints/MH24-BATCH-04-ATOM-LEVEL-CROSSWALK-BATCH-12-MOBILE-INVARIANTS-REVIEW-01.md` | `ece804af67ea66d0b0121b1e91c42451aa8143d8` | Structural/source-anchor/status consistency pass; concrete command/API route and enforcement OPEN |
| Batch 12 semantic Review 02 | `docs/checkpoints/MH24-BATCH-04-ATOM-LEVEL-CROSSWALK-BATCH-12-MOBILE-INVARIANTS-REVIEW-02.md` | `f8d50509014f8c72476ab845476dcc40569c3357` | Semantic consistency pass; distribution remains 4/2/0/0; MAI-21-04 history field corrected in a separate draft read-back |
| Batch 13 iPhone Media / AirPlay draft | `docs/checkpoints/MH24-BATCH-04-ATOM-LEVEL-CROSSWALK-BATCH-13-IPHONE-MEDIA-DRAFT.md` | `2f05bcf0b67200e44aaec7ba4e3a3164238270bf` | B1 §22; 9 provisional labels; 1 MAPPED / 7 NOT_REVIEWED / 1 NO_DIRECT_COUNTERPART / 0 CONFLICT; semantic/owner acceptance OPEN |
| Batch 13 Review 01 | `docs/checkpoints/MH24-BATCH-04-ATOM-LEVEL-CROSSWALK-BATCH-13-IPHONE-MEDIA-REVIEW-01.md` | `abf9c5f669b59434c3a9bb52068b8f226efa129c` | Bounded structure/source-anchor/status-consistency PASS; AirPlay scope, semantic/owner acceptance and qualification OPEN |
| Batch 13 semantic Review 02 | `docs/checkpoints/MH24-BATCH-04-ATOM-LEVEL-CROSSWALK-BATCH-13-IPHONE-MEDIA-REVIEW-02.md` | `36f171bf4ef6e9bec388cacc5ddc4ff8989d168e` | One bounded generic media-codec mapping correction; 1/7/1/0; full AirPlay and owner acceptance OPEN |
| Batch 14 Media System draft | `docs/checkpoints/MH24-BATCH-04-ATOM-LEVEL-CROSSWALK-BATCH-14-MEDIA-SYSTEM-DRAFT.md` | `d05218ff37d217016135beb8bc7a559686ec5933` | B1 §23; 14 provisional labels; 13 MAPPED / 1 NOT_REVIEWED / 0 NO_DIRECT_COUNTERPART / 0 CONFLICT; AT-16 OPEN—CONTRACT |
| Batch 14 Review 01 | `docs/checkpoints/MH24-BATCH-04-ATOM-LEVEL-CROSSWALK-BATCH-14-MEDIA-SYSTEM-REVIEW-01.md` | `5774a1fc87605296ba4adb6e2ef5014ffeb7d09f` | Bounded structure/source-anchor/status consistency PASS; semantic/owner acceptance OPEN; historical Audit Batch 04 B2 §16 pointer defect noted |
| Batch 15 Document System draft | `docs/checkpoints/MH24-BATCH-04-ATOM-LEVEL-CROSSWALK-BATCH-15-DOCUMENT-SYSTEM-DRAFT.md` | `3f20f36806cd91bc76ca5749fa4b06b8be651d7b` | B1 §24; 12 provisional labels; 9 MAPPED / 2 NOT_REVIEWED / 1 NO_DIRECT_COUNTERPART / 0 CONFLICT; AT-17 OPEN—OWNER DECISION |
| Batch 15 Review 01 | `docs/checkpoints/MH24-BATCH-04-ATOM-LEVEL-CROSSWALK-BATCH-15-DOCUMENT-SYSTEM-REVIEW-01.md` | `50d5ac25a4c32eb21dd8c7ac71205ae2051c8ef1` | 12/12 rows and all 12 fields structurally checked; bounded source/status consistency PASS; paid-tier semantics and AT-17 remain OPEN |

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
| P-01 | B1 literal atom ↔ B2 semantic mapping is incomplete across the full baseline | OPEN / STRUCTURAL UNION PASS; SEMANTIC ACCEPTANCE OPEN | Parent crosswalk: 48 historical parent IDs (4 `MAPPED` / 3 `NO_DIRECT_COUNTERPART` / 41 `NOT_REVIEWED` / 0 `CONFLICT`). Atom-level Batches 01–08 cover 153/153 Audit 01 labels for B1 §§3–6, 12, 15–17 (23 `MAPPED` / 119 `NOT_REVIEWED` / 11 `NO_DIRECT_COUNTERPART` / 0 `CONFLICT`). Structural union/schema/pointer checks pass; semantic owner acceptance and canonical-backlog promotion remain open. Coverage is not all 68 sections. Union review SHA: `e9ccafef5a3cca75f41e84bf3c4397dcc2285fd4` |
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
| P-12 | Whole-repository semantic completeness | NOT CLAIMED | Historical snapshot at commit `58305d5a9a5b1593f15d2dfb0ff79838c1bddaec` contained 826 entries / 445 Markdown files. A later pre-update branch snapshot at commit `572dfade59961e2e58c9bcaac16d09d996b997b6` contained 846 entries (465 Markdown, 193 Python, 47 YAML, 54 JSON; `truncated=false`). These are historical inventory snapshots, not a current-head inventory or a line-by-line semantic review. Reviewed source set is listed in the contract/review; unreviewed scope remains open. |
| P-13 | Jarvis umbrella vs Astra subsystem was not explicit in the original v3 synthesis | WORKING SCOPE ADDED; NOT CANONICAL | Jarvis gap reconciliation SHA 39720b11e5e6777b86ffd71e0fec1214982e0d95; implementation/runtime evidence absent |
| P-14 | Owner-reported hardware roles require exact inventory | OPEN / NOT QUALIFIED | Mac Pro model, mini 2011 identifier/OS, customer M2 site profile and future GPU server specs are not independently verified |
| P-15 | Jarvis must not duplicate task lifecycle/state across orchestration and Astra/framework candidates | OPEN DESIGN DECISION | Select one owner for queue/claim/lease/retry/evidence; use adapters around other execution frameworks |
| P-16 | Master-context packet for MH-01…MH-23 is not implemented as an auditable release mechanism | DESIGN REQUIREMENT | Global context + domain packets must carry source refs/SHA, current decisions, dependencies and change deltas |
| P-17 | Reusable-repository scorecard and pinned release bundle are not yet implementation artifacts | DESIGN REQUIREMENT / OPEN | Exact pins, license/SBOM/security, compatibility, preflight, rollback and post-install evidence required |
| P-18 | Public multi-agent repositories are candidate sources only | NOT SELECTED / NOT QUALIFIED | New review document lists Temporal, LangGraph, Microsoft Agent Framework, Pydantic AI, OpenHands and AutoGen status; no component installed or qualified |
| P-19 | Target OS/build/boot/install/update/recovery profiles are not pinned for the named Apple hardware roles | OPEN / PLATFORM PROFILE REQUIRED | B2 §9, blob SHA `1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f`; gap reconciliation §15, current blob SHA `39720b11e5e6777b86ffd71e0fec1214982e0d95` (read back 2026-10-12) |
| P-20 | Purchased Mac Pro is described as the primary developer workstation while a future production Mac Pro is also named; physical-asset identity/transfer is unresolved | OPEN / ASSET ALLOCATION REQUIRED | Gap reconciliation §17 / AG-20, latest blob SHA `39720b11e5e6777b86ffd71e0fec1214982e0d95`; owner blueprint |
| P-21 | B1 §15 document-assistance atom `B1-15-13` is incorrectly pointed to B2 §19 in historical Audit 01 | OPEN / DERIVED POINTER CORRECTION RECORDED | Gap reconciliation §18 / AG-21, blob SHA `39720b11e5e6777b86ffd71e0fec1214982e0d95`; B2 §§16/18 are the correct review target; historical Audit 01 remains unchanged |
| P-22 | B1 §18 names a first-class Trusted Sources Intelligence Engine, while reviewed B2 §§16/18 provide related knowledge/provenance/evidence controls but not a complete named-subsystem lifecycle contract | OPEN / OWNER-GOVERNANCE SCOPE AND CONTRACT REQUIRED | Batch 09 draft SHA `5e1b73c73c951638b549a30d569df2d1c7de8b31`; Review 03 SHA `184a99ef85143c2ad3048dca5c8d85b17f8651a3`; D-06 SHA `eb6fcbad3c8324ebbdf01f71305cb3d7d4b4c0bd`; row 18 of the working matrix remains a section-level summary. Preserve TSI-12 → TSI-07; no accepted full TSI contract, final child IDs or canonical promotion |
| P-23 | Batch 07 B1 §16 mapping originally conflated full contract completeness with text-level correspondence for trusted-cluster distributed compute | PARTIAL DOCUMENTARY MAPPING CORRECTION / SEMANTIC ACCEPTANCE OPEN | Batch 07 draft SHA `d6323442e3059dda091d0ad8b2a33fa91cad6ea0`; Review 02 SHA `0af17bf0db6f8b1c93d01aae3e8a8b5d8a0d9064`; B2 §10 lines 235–249 + §18 lines 382–392 support B1-16-01 / CLAI4-01 as documentary `MAPPED`. Distribution 1/9/1/0; workload contracts, named gateway, domain ownership and qualification remain OPEN. |
| P-24 | B1 §19 expands the named AI Human Clone subsystem from B1 §17, but its clone-specific permission, rights, identity/model/asset provenance and real/synthetic contract are not accepted in the reviewed B2 clauses | OPEN / SUPPLEMENTAL CROSSWALK DRAFT — SEMANTIC AND OWNER ACCEPTANCE OPEN | Batch 10 draft SHA `44b9369fea0be06e4e64f2052fd49f6d493f6603`; Review 01 SHA `36148379d7d1e39252bd918ad17772036cf0d972`; Review 02 SHA `612162b164b7d2585fa9646871839274cec5a343`; B1 §19 lines 315–328; B2 §§3–7,15–18. Preserve lineage to B1-17-05 / CDAI4-02; AHC-19-01 is cross-link-only, no separate subsystem count or final child IDs. Mapping distribution 5/13/1/0 remains provisional. |
| P-25 | B1 §20 Mobile Access roles and details are only partially evidenced by B2: Core/Remote roles align, but local capability-by-platform, exact two-app scope vs separate Developer Mobile, one-time payment, remote feature set and API contract remain open | OPEN / SUPPLEMENTAL CROSSWALK DRAFT — SEMANTIC AND OWNER ACCEPTANCE OPEN | Batch 11 draft SHA `0c102e5071ed5a33cbc02b00872da78eebd5bf9c`; Review 01 SHA `2a11ae52c4401a51fc562df5c9ddbe07cb83b2ef`; Review 02 SHA `c143d1b349bcf2ba3a76ffdad03b1d4258a1ebe9`; B1 §20 lines 332–359; B2 §2.3 lines 63–72, §22 lines 438–455, §25 lines 508–509. Distribution 4 MAPPED / 5 NOT_REVIEWED / 0 NO_DIRECT_COUNTERPART / 0 CONFLICT. MA-20-05 is documentary constraint correspondence only; exact two-app scope, one-time payment, full capability matrix, remote feature/API contract and owner acceptance remain open. Preserve matrix rows 20–21; no child IDs or canonical promotion. |
| P-26 | B1 §21 mobile authority, bypass, defined-contract and security invariants align with generic B2 rules, but the concrete mobile device-command and Remote Mobile → API → authority/subsystem paths remain unproven | OPEN / SUPPLEMENTAL CROSSWALK DRAFT — SEMANTIC AND OWNER ACCEPTANCE OPEN | Batch 12 draft SHA `dcbc0a0e8a8186e926315ea318eff902e491f0e7`; Review 01 SHA `ece804af67ea66d0b0121b1e91c42451aa8143d8`; Review 02 SHA `f8d50509014f8c72476ab845476dcc40569c3357`; B1 §21 lines 361–374; B2 §§2.3, 3–7, 14, 18, 22–23. Distribution 4 MAPPED / 2 NOT_REVIEWED / 0 NO_DIRECT_COUNTERPART / 0 CONFLICT. Review 02 confirms current mapping labels; MAI-21-04 change-history value corrected. Preserve matrix row 21; concrete device/API chain and owner acceptance remain open; no implementation/qualification inferred. |
| P-27 | B1 §22 commits to iPhone-to-MediaHub AirPlay streaming including 4K, subject to compatibility, network, authorization, codec, latency, resolution and bandwidth constraints; reviewed B2 clauses contain generic media/capability/network rules but not an explicit accepted AirPlay contract | OPEN / SUPPLEMENTAL CROSSWALK DRAFT — SEMANTIC AND OWNER ACCEPTANCE OPEN | Batch 13 draft SHA `2f05bcf0b67200e44aaec7ba4e3a3164238270bf`; Review 01 SHA `abf9c5f669b59434c3a9bb52068b8f226efa129c`; Review 02 SHA `36f171bf4ef6e9bec388cacc5ddc4ff8989d168e`; prior Semantic Audit Batch 03 SHA `fcd006e99d812dac5071b34c531f2783f4f54e88`; B1 §22 lines 375–379; B2 §§8–9, 12, 15, 20. Distribution 1 MAPPED / 7 NOT_REVIEWED / 1 NO_DIRECT_COUNTERPART / 0 CONFLICT; IM-22-06 is generic codec correspondence only. Preserve `IPHONE-AIRPLAY-4K-01` and matrix row 22; no final IDs or canonical promotion. MH-18/MH-17 remain NOT ACCEPTED / NOT FROZEN; runtime/interop/qualification not established. |
| P-28 | B1 §23 lists Media System categories and says the subsystem is not an alternative State Authority; B2 §15 explicitly lists the same broad Media category families and B2 §§3–4 establish the authority boundary, but external ecosystem projection and per-profile integration contracts are not established | OPEN / SUPPLEMENTAL CROSSWALK DRAFT — AT-16 / SEMANTIC OWNER ACCEPTANCE OPEN | Batch 14 draft SHA `d05218ff37d217016135beb8bc7a559686ec5933`; Review 01 SHA `5774a1fc87605296ba4adb6e2ef5014ffeb7d09f`; B1 §23 lines 383–389; B2 §15 lines 346–356 and §§3–4; Audit Batch 04 SHA `e7f35460e3bf32cc3fce8b4584848907d07a7943` (historical row points to B2 §16 for Media; preserve the audit and use current B2 §15 for the active reference); AT-16 backlog SHA `ec2580f714e8f620bcf85ff7de2ae9242439e5e8` remains OPEN—CONTRACT. Distribution 13 MAPPED / 1 NOT_REVIEWED / 0 NO_DIRECT_COUNTERPART / 0 CONFLICT; mappings are category-level text correspondence, not universal support or qualification. Preserve MEDIA-SYSTEM-01 and matrix row 23; no final IDs or canonical promotion. |
| P-29 | B1 §24 specifies Document System as a paid/professional tier with OCR, classification, search, metadata, provenance, knowledge extraction, workflows and structured information; B2 §16 generally represents document functions but not edition-specific paid scope/enforcement, and does not select PaddleOCR | OPEN / SUPPLEMENTAL CROSSWALK DRAFT — AT-17 / OWNER DECISION | Batch 15 draft SHA `3f20f36806cd91bc76ca5749fa4b06b8be651d7b`; Review 01 SHA `50d5ac25a4c32eb21dd8c7ac71205ae2051c8ef1`; B1 §24 lines 391–397; B2 §16 lines 358–366 and §21 OSS adoption sequence; Semantic Audit Batch 04 SHA `e7f35460e3bf32cc3fce8b4584848907d07a7943`; AT-17 backlog SHA `ec2580f714e8f620bcf85ff7de2ae9242439e5e8` remains OPEN—OWNER DECISION. Distribution 9 MAPPED / 2 NOT_REVIEWED / 1 NO_DIRECT_COUNTERPART / 0 CONFLICT. Preserve DOCUMENT-SYSTEM-01 and matrix row 24. Paid-tier/edition entitlement, structured-information schema and OCR component selection remain open; no final IDs, PaddleOCR adoption or canonical promotion. |
| P-30 | B1 §25 Digital Twin: Full-edition presence, exact Mac mini/Mini PC profile scope, paid professional entitlement, and building/room/equipment/spatial/BIM/simulation/monitoring/workflow scope; B2 §17 provides bounded generic correspondence but exact target-profile and entitlement lifecycle semantics remain open | OPEN / SUPPLEMENTAL CROSSWALK DRAFT — AT-18 / SEMANTIC AND OWNER ACCEPTANCE OPEN | Batch 16 draft SHA `5329556d673749043c6d00ffc6bb6a7566558f59`; Review 01 SHA `5fe9c64bd0a177559e2d3a64672985e56cce1333`; B1 §25 lines 401–407; B2 §17 lines 368–378; AT-18 backlog SHA `ec2580f714e8f620bcf85ff7de2ae9242439e5e8`. Distribution 3 MAPPED / 1 NOT_REVIEWED / 0 NO_DIRECT_COUNTERPART / 0 CONFLICT. Exact named hardware profiles, entitlement lifecycle/enforcement, complete artifact schemas/workflows, implementation and qualification remain open; no final child IDs or canonical promotion. |

## 11. Acceptance checklist for a future Passport v3 release
- [ ] Resolve AG-20/P-20: distinguish the developer Mac Pro from the future production Mac Pro, or approve and evidence an explicit role transition with a replacement developer workstation and credential/data boundary.
- [ ] Validate all derived B1↔B2 section pointers against the pinned source headings; record corrections in current working crosswalks while preserving historical Audit 01 provenance.

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
- [ ] Resolve P-22 / ARC-029 / V-22: obtain an explicit owner/governance disposition for TSI subsystem identity, owner and contract scope; if retained, define source lifecycle, trust taxonomy, information categories, provenance/evidence semantics and verification criteria. Preserve D-06; do not infer acceptance from topical similarity or documentary MAPPED status.
- [ ] Batch 09 remains provisional until TSI semantic acceptance and all applicable owner/governance gates are independently evidenced.
- [ ] Resolve P-24: obtain explicit owner/governance disposition for AI Human Clone scope/owner and, if retained, approve clone-specific consent, authorization/rights-holder, identity, voice/appearance, model/asset provenance, audit/revocation, real/synthetic separation and authority-boundary contract. Preserve the B1 §17 / CDAI4-02 / B1-17-05 lineage; do not count AHC-19-01 as an independent subsystem obligation.
- [ ] Resolve P-25: clarify B1's "exactly two applications" scope against B2's separately named Developer Mobile surface; define per-platform local Core capabilities, pricing/entitlement decision, remote capability set and accepted Remote Access API/command boundaries. Preserve matrix rows 20–21; no implementation or qualification is inferred from the Batch 11 structural pass.
- [ ] Resolve P-26: confirm the mobile command path prevents direct physical-device bypass, preserves the single State Authority and HA Core's Smart Home boundary, and applies authentication, authorization, trust, privacy, audit and revocation. Define and accept the Remote Mobile → MediaHub API → Core/State Authority/subsystem path; do not infer implementation from the four generic MAPPED labels.
- [ ] Resolve P-27: obtain explicit disposition/owner and an accepted AirPlay/iPhone media contract defining supported device/OS profiles, 4K/codec behavior, authorization/rights, network/bandwidth admission, latency, resolution negotiation, degradation and failure behavior. Preserve `IPHONE-AIRPLAY-4K-01` and matrix row 22; treat generic B2 media/phone support as insufficient for AirPlay acceptance.
- [ ] Resolve P-28 / AT-16: confirm the exact Media System integration/source scope, owner and source/adapter inventory against B1 §23 line 385. Keep category-level B2 §15 correspondence distinct from per-device/vendor/protocol/rights/performance qualification. Decide external ecosystem projection specifically; preserve the historical Audit Batch 04 B2 §16 pointer unchanged but use correct B2 §15 Media for current references.
- [ ] Resolve P-29 / AT-17: owner defines Document System paid/pro entitlement by edition, per-function lock/unlock and denial behavior, expiry/revocation/offline/reinstall/device-transfer semantics. Keep generic document capability mapping distinct from pricing or runtime enforcement. PaddleOCR remains only a conditional B1 example unless a separate component review and adoption decision is recorded.
- [ ] Resolve P-30 / AT-18: confirm exact Full-edition/target-profile runtime scope for Mac mini and Mini PC; define authoritative professional entitlement state and grant/denial/expiry/revocation/offline/restore/reinstall/device-transfer behavior; accept the Digital Twin artifact/workflow scope and provenance/authorization/qualification requirements. Treat Batch 16 MAPPED labels as bounded textual correspondence only; keep implementation and qualification separate.
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


- 2026-10-12 — added P-21 for the confirmed B1-15-13/B2 §19 cross-reference defect; updated active AG-20/P-20 report pointers to current Gap Reconciliation SHA `fee9977fee0a5efa79ec48c652544d2c4a0d665f`. Audit 01 and both baselines remain immutable; this follow-up is not an added qualification or a 14th cycle.

- 2026-10-12 — corrected the active P-19 pointer: gap reconciliation §15 now uses current read-back SHA `fee9977fee0a5efa79ec48c652544d2c4a0d665f`, not the superseded pre-AG-21 SHA. Historical change records and B1/B2 are unchanged; this is pointer maintenance only.


- 2026-10-12 — reconciled the active finding count from 20 to 21 after AG-21 was added; refreshed active gap-report links in the source inventory and P-19/P-20/P-21 rows to current Gap Reconciliation SHA `39720b11e5e6777b86ffd71e0fec1214982e0d95`. Dated historical pointer records remain intact; B1/B2 and runtime are unchanged.
- 2026-10-12 — corrected active P-13 source pointer to current Gap Reconciliation SHA `39720b11e5e6777b86ffd71e0fec1214982e0d95`; preserved the former SHA only in older dated history. No architecture rule or baseline changed.

- 2026-10-12 — added P-22 for the open B1 §18 Trusted Sources Intelligence Engine scope/contract disposition, linking D-06 and Batch 09 Review 03. The 17 traceability labels and 3/13/1/0 mapping distribution remain provisional; B1, B2, matrix and canonical backlog are unchanged.

- 2026-10-12 — added P-23 after Batch 07 semantic Review 02. B1-16-01 / CLAI4-01 is recorded as bounded documentary `MAPPED` using B2 §10 and §18; workload-level Local Cluster AI semantics, gateway disposition, owner approval and qualification remain open. Updated the active Batch 07 draft pointer to `d6323442e3059dda091d0ad8b2a33fa91cad6ea0`; Review01 remains historical and Review02 is separate.
- 2026-10-12 — added P-24 for the supplemental B1 §19 AI Human Clone crosswalk. Batch 10 records 19 provisional traceability labels and links the repeated subsystem identity to existing B1-17-05 / CDAI4-02; mapping and owner acceptance remain OPEN. No canonical backlog or baseline changed.
- 2026-10-12 — updated P-24 to link the separately named Batch 10 Review 02 (SHA `612162b164b7d2585fa9646871839274cec5a343`). Review 02 confirms bounded semantic consistency without changing the 5/13/1/0 distribution; full semantic and owner acceptance remain OPEN. Batch 08 lineage, Audit 01, B1/B2 and canonical backlog unchanged.
- 2026-10-12 — added P-25 for the supplemental B1 §20 Mobile Access crosswalk. Batch 11 has nine provisional rows and a bounded structural/source-anchor review; 3 MAPPED / 6 NOT_REVIEWED / 0 NO_DIRECT_COUNTERPART / 0 CONFLICT. The exact app-count scope, one-time purchase policy, full capability matrix and API contract remain open. B1/B2, matrix and canonical backlog unchanged.
- 2026-10-12 — added P-26 for the B1 §21 Mobile Access Invariants crosswalk. Batch 12 has six provisional rows and a bounded structural/source-anchor review; 4 MAPPED / 2 NOT_REVIEWED / 0 NO_DIRECT_COUNTERPART / 0 CONFLICT. The concrete physical-device bypass and remote command/API chain remain open. B1/B2/matrix/canonical backlog unchanged.

- 2026-10-12 — linked Batch 11 semantic Review 02 (SHA `c143d1b349bcf2ba3a76ffdad03b1d4258a1ebe9`) and the corrected working draft SHA `0c102e5071ed5a33cbc02b00872da78eebd5bf9c` to P-25. MA-20-05 is now bounded documentary `MAPPED`; distribution 4/5/0/0. Full app-count/Developer Mobile scope, commercial policy, complete capability/API contracts and owner acceptance remain OPEN. Batch 12 / P-26, B1/B2, matrix and canonical backlog remain unchanged.

- 2026-10-12 — linked Batch 12 semantic Review 02 (`f8d50509014f8c72476ab845476dcc40569c3357`) and corrected working draft SHA `dcbc0a0e8a8186e926315ea318eff902e491f0e7` to P-26. Distribution remains 4 MAPPED / 2 NOT_REVIEWED / 0 NO_DIRECT_COUNTERPART / 0 CONFLICT. Review 02 keeps the direct-device bypass and exact Remote Mobile command/API route OPEN and replaces the uninformative MAI-21-04 change-history value. Batch 11/P-25, B1/B2, matrix and canonical backlog remain unchanged.

- 2026-10-12 — added P-27 for the B1 §22 iPhone Media / AirPlay crosswalk. Batch 13 contains nine provisional labels, 0 MAPPED / 8 NOT_REVIEWED / 1 NO_DIRECT_COUNTERPART / 0 CONFLICT; Review 01 confirms bounded structural/source-anchor/status consistency only. Preserve `IPHONE-AIRPLAY-4K-01` and matrix row 22; MH-18/owner acceptance, protocol behavior and qualification remain OPEN. B1/B2, matrix and canonical backlog unchanged.

- 2026-10-12 — linked Batch13 semantic Review02 SHA `36f171bf4ef6e9bec388cacc5ddc4ff8989d168e` and updated working draft SHA `2f05bcf0b67200e44aaec7ba4e3a3164238270bf` to P-27. Only IM-22-06 is now bounded documentary `MAPPED` for generic media-codec handling in B2 §15; distribution is 1/7/1/0. The historical pre-review 0/8/1/0 state remains in the draft. AT-15 remains OPEN—OWNER DECISION; exact AirPlay/4K interoperability, authorization/rights, network/performance profile, implementation and qualification remain OPEN. B1/B2/matrix/canonical backlog unchanged.

- 2026-10-12 — added P-28 for B1 §23 Media System and AT-16. Batch 14 draft/Review 01 are d05218ff37d217016135beb8bc7a559686ec5933 / 5774a1fc87605296ba4adb6e2ef5014ffeb7d09f; 14 provisional labels, 13 MAPPED / 1 NOT_REVIEWED / 0 NO_DIRECT_COUNTERPART / 0 CONFLICT. These statuses are category-level text correspondence only. External ecosystem projection, per-profile integration, owner acceptance and qualification remain OPEN. Recorded the historical Audit Batch 04 B2 §16 Media pointer defect without modifying the audit, matrix, B1/B2 or canonical backlog.

- 2026-10-12 — added P-29 for B1 §24 Document System / AT-17. Batch 15 draft/Review 01 `3f20f36806cd91bc76ca5749fa4b06b8be651d7b` / `50d5ac25a4c32eb21dd8c7ac71205ae2051c8ef1`; 12 provisional labels, 9 MAPPED / 2 NOT_REVIEWED / 1 NO_DIRECT_COUNTERPART / 0 CONFLICT. AT-17 remains OPEN—OWNER DECISION; paid entitlement, structured-information scope and PaddleOCR adoption remain unaccepted. B1/B2/matrix/AT backlog/canonical backlog/main unchanged.


- 2026-10-13 — added P-30 for B1 §25 Digital Twin / AT-18. Batch 16 draft and Review 01 blobs `5329556d673749043c6d00ffc6bb6a7566558f59` / `5fe9c64bd0a177559e2d3a64672985e56cce1333`; four provisional labels, 3 MAPPED / 1 NOT_REVIEWED / 0 NO_DIRECT_COUNTERPART / 0 CONFLICT. Exact Mac mini/Mini PC profile scope, entitlement lifecycle, complete artifact/workflow semantics and owner acceptance remain OPEN. B1/B2, atomic/canonical backlog, traceability matrix and main unchanged; no final child IDs minted.


## 13. Developer-fabric placement and unresolved owner decisions (2026-10-13)

**Status:** working passport addendum; this document remains non-canonical. Functional authority remains Baseline 2.0.

The source-anchored placement matrix is maintained at `docs/checkpoints/MEDIAHUB-NODE-SERVICE-PLACEMENT-AND-DECISION-REGISTER-01.md`; the decision interface is `docs/checkpoints/MEDIAHUB-OWNER-DECISION-PACKET-01.md`. These artifacts summarize Contour A only and do not claim deployment or acceptance.

### Confirmed target boundaries

- The accepted developer-fabric target places Jarvis/control services, model/API routing, task coordination, monitoring, registry and the Alamo local inference endpoint on the central Mac Pro, subject to hardware/runtime validation.
- Mac mini Server 2011 is a legacy/low-resource candidate with compatibility, OS lifecycle, workload and thermal facts still unknown. It is not a mandatory critical dependency.
- The future owned GPU/video server is optional later capacity; hardware and service profile are not selected.
- Developer Mobile is a client, not an authority. Mesh/P2P reachability does not grant application, shell or administrative permissions.
- The customer-site Mac mini M2 prototype, developer nodes, test hosts, registration-only VPS and user-contributed compute remain separate trust domains and must not inherit one another's credentials, data or authority.
- Alamo is the accepted target endpoint name; the relationship to proposed Ollama and target-gated ONNX Runtime/llama.cpp remains unresolved. No runtime is inferred as installed or selected by this addendum.
- Jarvis/ASTRA engineering lifecycle ownership remains unresolved. Neither gains MediaHub Product State Authority.
- MH-15 remains work in progress with acceptance/freeze and implementation authorization absent; MH-16 remains proposed/not frozen/not authorized; MH-21 remains not accepted/frozen.

### Traceability and gate state

Existing decision IDs DEC-DEV-01…DEC-DEV-08 are preserved in the owner-decision packet. The unified traceability matrix Section 57 links the cross-domain conclusions to live source refs and blob SHAs. No owner decision was made and no implementation, qualification, deployment or production acceptance is claimed.

Contour B product implementation remains gated until Contour A is deployed and independently accepted with evidence.


## 14. Source-triaged developer-fabric decisions (2026-10-13)

**Status:** working passport addendum; not canonical. Baseline 2.0 remains the accepted functional reference.

- **Answered by accepted target source:** Alamo is the local inference endpoint label. Its runtime, protocol, model and exact endpoint remain deployment facts to discover. ONNX Runtime and llama.cpp are target-gated manifest candidates; the proposed Ollama direction is not accepted selection evidence.
- **Open P0 lifecycle decision:** no accepted source reviewed in this pass assigns one authoritative Jarvis/ASTRA lifecycle owner for queue, claim, lease, retry, cancellation, evidence promotion and recovery. Continue exact contract reconciliation before asking the owner.
- **Evidence-gated hardware choices:** future production Mac Pro identity, Mac mini Server 2011 workload and future GPU-server profile remain open/deferred until the relevant asset/hardware/OS/workload evidence exists.
- **Established security invariants:** mesh/VPN/reachability is not trust or authorization; authentication, identity, capability and authorization are distinct. Developer Mobile still needs an operation-scoped identity/API/revocation/audit contract.
- **Established provider invariant:** no silent local-to-cloud/provider fallback. MH-21 remains NOT ACCEPTED / NOT FROZEN / NOT PRODUCTION READY; provider/data-class/egress/retention policies and evidence remain open.
- **Established contour gate:** Contour B must not begin until Contour A is deployed and independently accepted with evidence. DEC-DEV-08 is retained as a gate/evidence tracker, not an option to bypass.
- Detailed source anchors and decision dispositions are in Section 58 of the unified traceability matrix and Section 6 of the owner decision packet. These are working documentary artifacts, not proof of implementation, qualification or production acceptance.


## 15. Jarvis / ASTRA lifecycle authority conflict (2026-10-13)

**Status:** OPEN_CONFLICT / NOT QUALIFIED. This is a documentary reconciliation, not an acceptance or change to primary ASTRA sources.

- ASTRA GOLD's canonical design sources describe A0 as the controller for ASTRA's engineering queue, claims, leases, scheduling, evidence and recovery. This supports A0 as the intended ASTRA-internal workflow-state owner.
- The Complete Component Scheme also uses the phrase “MediaHub State Authority” for A0-ASTRA. That wording conflicts with the product-state authority boundary and must not be silently treated as valid product-state ownership.
- The working Verifiable Architecture Contract ARC-003 restricts A0 to ASTRA engineering workflow state; ARC-017 frames Jarvis as the umbrella and ASTRA as a bounded subsystem; ARC-018 requires one lifecycle owner before implementation. The independent Jarvis review leaves that cross-system owner OPEN.
- Current ASTRA truth remains NOT_PROVEN / BLOCKED with all G0–G11 blocked. Canonical design wording is not implementation, verification, qualification or acceptance evidence.
- Required reconciliation: clarify the scope of the conflicting “MediaHub State Authority” phrase through governance; determine whether A0 is the selected single engineering-task lifecycle owner under Jarvis; specify a typed adapter/delegation boundary and prevent competing queue/lease/retry/evidence-promotion stores.
- Do not change the ASTRA primary sources or choose a second lifecycle owner without the required governance decision. The next independent track is the existing P0-07 → P0-05 trust/context/authorization bridge.


## 15. MH-04 / MH-12 trusted-context lifecycle crosswalk (2026-10-13)

**Status:** working passport addendum; not canonical and not an acceptance record. Baseline 2.0 remains the accepted functional reference.

- MH-04 identity model (`architecture/mh-04-security-trust-authorization`, blob `dccded8f572bed42e8f40e4240e91e5621f24a37`) defines principal lifecycle states; authentication (`834dd3f4036ba1668e4b8af132393e25c70c85eb`), authorization (`327b7c0c7504612ff05a6654a710058dcecaf438`), credential boundary (`7b5db076bb5a948def0fc4d72dd58740828660c5`) and failure semantics (`441d110036bd7fa5a26b8c3d9f58d63a37f7915f`) establish conceptual deny/revocation requirements. The MH-04 package remains PROPOSED / REVIEW COMPLETE; no concrete issuer or security framework is accepted by those documents.
- MH-12 main sources remain architecture/governance-level: security architecture blob `cf4ebfd5bf471ca676f075c51d3a24906504e490`, authorization blob `c48641861691714017aa5b1f99fe8eee8ea0e76a`, invariants blob `0609be9c3420070434014dad4529e4ccd46b0996`. They align with the canonical authority path but do not prove an accepted/deployed issuer.
- P0-05 implementation at `303a766257b90c4356dcffc8967a5574e8e22e7a` still represents `AuthorizationContext` with only principal and capability (blob `4d8df5d3c1c26f7f133a8093cd270635b085f4d5`); the Consumer Boundary forwards the supplied context (blob `23b95f1b37cb35e311b61e3babcca4bd1aea9596`) without proving issuer provenance, expiry/freshness, audience, revocation, replay or request binding.
- P0-05 contract text at governance tree `97a01977f521ba8304a455b5d7504896235ddea7`, blob `bba8dd3e8812767b6dbc8afff1bec5bd36dc828b`, still says DRAFT / GOVERNANCE REVIEW REQUIRED despite implementation-state acceptance evidence. D6 requires explicit governance clarification; do not edit the protected header or infer normative-text acceptance.
- Disposition: DEC-DEV-02 remains OPEN_CONFLICT; P0-07→P0-05 bridge remains blocked; trusted issuer and context lifecycle remain NOT EVIDENCED; P0-05 v1.1 remains NON-NORMATIVE / NOT ACCEPTED / NOT FROZEN; qualification remains NO-GO / NOT PROVEN. No tests, implementation, provider calls or qualification were performed.
- Detailed clause-level trace: `docs/checkpoints/mediahub-unified-system-traceability-matrix-v0.1.md`, Section 62.


## 16. P0-05 D6 acceptance-scope governance discrepancy (2026-10-13)

**Status:** decision support only; no owner disposition recorded. Baseline 2.0 remains the canonical functional reference.

- Accepted implementation target: commit `303a766257b90c4356dcffc8967a5574e8e22e7a`, tree `82da63f03da20049954fe69257342cbf66b58395`.
- Contract present in that exact tree: `docs/architecture/P0-05-consumer-contract.md`, blob `bba8dd3e8812767b6dbc8afff1bec5bd36dc828b`, still marked `DRAFT — GOVERNANCE REVIEW REQUIRED`.
- Acceptance record: governance tree `97a01977f521ba8304a455b5d7504896235ddea7`, blob `a0d28b4cfd9bed27e8a80968f6beac6cfdd97242`, says P0-05 is ACCEPTED / FROZEN at the reviewed implementation state. It does not separately state that the exact contract text is accepted/frozen as normative.
- Governance packet blob `1253944ffeefcb59502d9f7deb13d38baed1d6e1` separates implementation authorization, implementation acceptance, security exit and production qualification. P0-05 v1.1 remains a non-normative proposal.
- Decision-ready options A/B/C and recommendation are recorded in proposal §9, `docs/checkpoints/p0-05-contract-revision-proposal-p0-07-existing-context-2026-10-12.md`, current blob `6d494c7311e61ec3d82e561f66af10f6dffa69b9`; detailed evidence is in unified traceability matrix §63, current blob `815ce2ecd8c75e51338043cfe0f25edfe1143229`.
- Recommendation is C (defer) on current evidence; B is only a conservative provisional planning assumption if needed, not a decision. Owner/governance disposition remains PENDING.
- Consequence unchanged: D6 OPEN / GOVERNANCE AMBIGUITY; P0-07 mutation/publication BLOCKED — GOVERNANCE/API GAP; P0-05 v1.1 NON-NORMATIVE / NOT ACCEPTED / NOT FROZEN; project qualification NO-GO / NOT PROVEN. No protected contract/header, acceptance record, code or implementation was changed; no tests/qualification were performed.


## 17. DEC-DEV-02 lifecycle authority source reconciliation (2026-10-13)

**Status:** working passport addendum; OPEN_CONFLICT / NOT ACCEPTED / NOT FROZEN. Baseline 2.0 remains the canonical functional reference.

- ASTRA GOLD primary design sources place queue, claim, lease, heartbeat, restart recovery and result publication in the A0 engineering control plane. This establishes intended ASTRA-internal workflow responsibilities only.
- The Complete Component Scheme's phrase “A0-ASTRA = single coordination and MediaHub State Authority” conflicts with the integrated architecture contract ARC-003, which limits A0 to ASTRA engineering workflow state and explicitly excludes MediaHub Product State Authority. Neither source has been silently edited or promoted.
- Jarvis is the umbrella engineering/orchestration concept and ASTRA a bounded subsystem candidate; ARC-018 requires one lifecycle owner and a typed adapter/delegation boundary before implementation. The exact cross-system owner remains open.
- ASTRA Current Truth remains NOT_PROVEN / BLOCKED with G0–G11 blocked. Design labels are not implementation or qualification evidence.
- DEC-DEV-02 options A/B/C and their consequences are documented in owner decision packet 01. Recommendation: do not choose from design labels alone; obtain a governed clarification of the “MediaHub State Authority” wording and then accept one typed lifecycle contract before implementation. No owner decision is inferred.
- Detailed source/ref/blob crosswalk and the minimal owner question: [Unified System Traceability Matrix v0.1, Section 61](mediahub-unified-system-traceability-matrix-v0.1.md), current blob `fec41118a104514b90923967212fc775bb2bf880`.
- Disposition unchanged: DEC-DEV-02 OPEN_CONFLICT; ASTRA Current Truth NOT_PROVEN / BLOCKED; Contour A → Contour B remains a binding gate. No implementation, qualification, deployment or acceptance is claimed.
