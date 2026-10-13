# MediaHub — единый план автономной среды разработки
Дата: 2026-10-13
Ref: `docs/mediahub-chat-tree-map-20261012`
Статус: WORKING PLANNING CHECKPOINT / DOCUMENTARY ONLY / NOT A NEW CANONICAL BASELINE

> **Plan-of-record notice (2026-10-13):** This document is retained as the original hardware-and-contour planning note. Its sequencing is superseded by [MEDIAHUB-MASTER-DEVELOPMENT-ROADMAP-1.0.md](MEDIAHUB-MASTER-DEVELOPMENT-ROADMAP-1.0.md), which is the single working plan of record for subsequent sequencing. This supporting note does not create a parallel execution plan. Architecture authority, phase gates and restrictions in the master roadmap apply.

## 1. Цель и границы

По прямому уточнению владельца от 2026-10-13 работу разделяем на два последовательных контура:

- **Контур A — автономная среда разработки:** облачная среда разработки, серверы разработчика, Jarvis, ASTRA/Astra Gold как ограниченная подсистема, модельная/инструментальная маршрутизация, инженерная память, GitHub, developer compute, мобильное приложение разработчика, установка, обновление, восстановление и доказательства.
- **Контур B — MediaHub OS как продукт:** отдельная продуктовая система, которую начинаем разрабатывать автономно после развёртывания и документально подтверждённой готовности контура A.

Контуры связаны требованиями и трассируемостью, но не являются одной плоской средой и не разделяют автоматически полномочия, данные, секреты, очереди или жизненные циклы. Этот checkpoint не меняет Baseline 2.0, доменные контракты или статус квалификации.

## 2. Источники, непосредственно прочитанные из GitHub

| Источник | Ref | Blob SHA | Что подтверждает / ограничение |
|---|---|---|---|
| Bootstrap instruction | `docs/mediahub-chat-tree-map-20261012` | `4ced4a9249591d218e8949f498c862fc21274b16` | Обязательный протокол чтения, authority boundaries, lifecycle gates |
| Chat Tree Map | `docs/mediahub-chat-tree-map-20261012` | `753d56adf2b68bea8100b4082406f7e1de211aa9` | Навигация и история проекта; не заменяет первичные документы |
| Functional Baseline 2.0 | `main` | `1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f` | Текущий принятый функциональный reference |
| Functional Baseline 1.0 | `main` | `9df4892ed0734050ac79732603d15bb414717310` | Исторический literal source; не смешивать с B2 без change control |
| Distributed AI Infrastructure | `main` | `e549692f207fbc91d9b9b9b92b8e665404f07290` | Принятая целевая топология разработки, но runtime не квалифицирован |
| Canonical Component Manifest 2.0 | `main` | `45988bf9da202c9597d0ca2de50e92e5c2e6ed55` | Выбор компонентов закрыт; реализация открыта; production admission gated |
| MH-15 OS/Appliance Architecture | `main` | `f817925c69ce4484713f952e47aacad283af8eeb` | Hardware/OS architecture work in progress; acceptance/freeze/implementation not authorized |
| MH-15 Acceptance Criteria | `main` | `082642e67dc66cb359a5566773c143854cafaa00` | Hardware, OS, lifecycle, security, resource and evidence gates remain required |
| MH-16 Master/Reverse Prompt | `main` | `62924d4686aa3f55fce442a3c4bab66c82ae19e5` | Installer/update/recovery authority boundaries; current MH-16 status remains proposed/not frozen/not authorized |
| Unified architecture/deployment contract v0.1 | `docs/mediahub-chat-tree-map-20261012` | `1057776ca9192b307a4e6de72db5d12cdbcc1a39` | Cross-domain deployment plan; proposed/not accepted/not frozen |
| Unified traceability matrix v0.1 | `docs/mediahub-chat-tree-map-20261012` | `9af75da0b1383a51bb95cb3cd5dd62bf22b571f7` | Cross-domain matrix and phases P00–P20; proposed/not accepted/not frozen |
| Jarvis gap reconciliation | `docs/mediahub-chat-tree-map-20261012` | `39720b11e5e6777b86ffd71e0fec1214982e0d95` | AG-01…AG-21; working analysis, not new accepted baseline |
| System Passport v3 | `docs/mediahub-chat-tree-map-20261012` | `467aedfc655db966597f564f4bf3074185aca6e9` | Working integrated passport; not canonical |
| Verifiable Architecture Contract 01 | `docs/mediahub-chat-tree-map-20261012` | `c248956417cc61d66c968a4c58a56e799f653354` | Working contract; architecture acceptance remains open |
| Current continuation checkpoint | `docs/mediahub-chat-tree-map-20261012` | `0f9e2b4dc06930a1a45bb4d9f2d5f402ccc56a98` | Existing latest continuation history; next-step routing still needs this new plan linked from the map |

Main HEAD observed in live compare: `1d45bbccbbbd27309c39cb9e9351bb291cdb47a8`. At this pass the documentation branch was DIVERGED from main, 536 commits ahead / 2 behind, merge base `f0f406feb9f9816b009f4e6e756813541e53b9bc`. No merge/rebase is authorized or performed.

## 3. Hardware and trust-domain inventory

### Primary developer-fabric target stated by owner

1. **Mac Pro 2013 / macOS** — primary developer workstation and, in the target topology, central developer infrastructure node for Jarvis/control services, routing, registry/coordination and local model endpoint (Alamo working name). Exact CPU, RAM, GPU, disks, interfaces and macOS build are not evidenced by this documentary pass.
2. **Mac mini Server 2011 / clean Linux / 16 GB RAM** — existing low-resource developer/server node. Only model-year and 16 GB RAM are currently owner-reported here. CPU, exact model identifier, disk/NIC/firmware, supported Linux/kernel, security lifecycle and workload capacity remain UNKNOWN. Do not make it a mandatory dependency for modern build/model services before compatibility evidence.
3. **Future remote GPU/video server** — planned owned remote compute pool. It is an optional later capacity extension, not a prerequisite for initial developer-fabric operation. Exact hardware, location, OS, GPU/VRAM, model/runtime, networking, cost and security profile remain TBD.

### Other roles already present in project sources — keep separate

- MacBook developer clients and cloud-authenticated Codex path.
- Client-site Mac mini M2 prototype: separate customer trust domain; must not silently join the developer compute pool or inherit developer secrets/data.
- Existing server test stand / developer hosts such as mh-dev-01 and mh-dev-02: TEST/STAGING until individually reclassified; no host inspection or cleanup is authorized by this checkpoint.
- MediaHub user-contributed compute Pool B: untrusted by default, opt-in/consent/isolated/quotas/verification/revocation required; not the same as the owned future GPU server Pool A.
- European VPS: narrow API-key registration/management workflow only; not a general model gateway, inference proxy or ordinary data transit path.
- Developer Mobile: client to Jarvis over approved private mesh/P2P interfaces; mesh membership is not application authorization and does not grant shell/admin rights.

The source gap register also records a future product deployment ambiguity: whether a future production Mac Pro is the same physical asset as the current developer Mac Pro or a separate unit. Do not silently assign one asset to both roles. Any role transition requires an explicit owner decision and separate identity, data, credential, install and recovery plan.

## 4. Architecture facts and unresolved conflicts

### Established target direction

- Jarvis is the umbrella engineering/orchestration architecture; ASTRA/Astra Gold is a bounded execution/queue/evidence subsystem, not the entire system.
- MediaHub product state authority remains separate from engineering workflow state. Jarvis/ASTRA do not become Product State Authority.
- The Mac Pro is described in `MEDIAHUB-DISTRIBUTED-AI-INFRASTRUCTURE.md` as the central developer node with Jarvis, model/API routing, task coordination, monitoring, registry and local model endpoint Alamo.
- Claude/Codex provider paths remain distinct. The Claude Code path has an FCC integration/control layer in the accepted target document; FreeLLMAPI is a cloud-provider path; the developer mobile client uses a private mesh/P2P path.
- Local-only mode must fail closed: no silent fallback from local inference to cloud. Model/provider identity, policy, data classification, credentials, quota, latency, cost and retention must be visible/controlled.
- Component manifest selection status is CLOSED, but implementation is OPEN and production admission is qualification-gated. Inclusion in the manifest is not installation or qualification.

### Conflicts / owner decisions still required

1. **Local inference identity:** the accepted target topology names `Alamo` as the Mac Pro local inference endpoint; the working cross-domain contract names local Ollama as an owner-directed candidate; the component manifest lists ONNX Runtime/llama.cpp as target-gated. Decide whether these are complementary layers/adapters or competing alternatives. Do not silently choose or install one.
2. **Jarvis vs ASTRA lifecycle ownership:** avoid duplicate independent queues, claim/lease domains, retry engines or gate-promotion stores. Before implementation, select one lifecycle owner and define adapters/delegation.
3. **Mac Pro role and capacity:** current role is developer workstation/central node; exact hardware facts and sustainable local-inference capacity are unknown. A future production role cannot be assumed to use the same physical machine.
4. **Mac mini 2011 fit:** Linux baseline is a direction, not compatibility evidence. Establish exact hardware/OS/security support and workload fit before assigning critical services.
5. **Mobile app and mesh:** developer-only scope is explicit; exact identity, authorization, revocation, API and network profiles remain to be accepted/qualified.
6. **Cloud/provider policy:** provider versions, exact API compatibility, terms, quotas, retention, data classes and failover must be verified; free capacity is not guaranteed.
7. **Install/lifecycle:** MH-15 is not accepted/frozen and MH-16 remains proposed/not frozen/implementation not authorized. No installer, OS change, deployment or recovery action is authorized by this checkpoint.
8. **Global qualification:** ASTRA current truth is `NOT_PROVEN / BLOCKED` (G0–G11 blocked in the referenced snapshot); MH-22 qualification gates are not promotable; project-wide verdict remains `NO-GO / NOT PROVEN`. This is not a statement about the current physical host state beyond the cited evidence snapshot.
9. **Product architecture blocker:** P0-07→P0-05 authorization/canonical-read/publication bridge remains `NOT EVIDENCED / GOVERNANCE-API GAP`; P0-05 v1.1 remains non-normative/not accepted/not frozen. This blocks claims dependent on that contract, not the read-only planning work recorded here.

## 5. Unified development plan

### Phase A0 — scope and source-of-truth lock
- Keep developer-fabric work separate from MediaHub product implementation.
- Use Baseline 2.0 as current functional reference and Baseline 1.0 as historical literal provenance; preserve all historical IDs.
- Keep map, passport, contract, matrix and checkpoints as navigation/traceability artifacts, not substitute authorities.
- Exit: source precedence and two-contour boundary are explicitly cross-linked; no unresolved source conflict is silently normalized.

### Phase A1 — inventory existing architecture and requirements
- Reconcile `MEDIAHUB-DISTRIBUTED-AI-INFRASTRUCTURE.md`, Jarvis gap report, Passport v3, Verifiable Architecture Contract 01, MH-15/MH-16, deployment contract, component manifest and the unified matrix.
- Build per-node inventory rows: asset role, trust domain, OS/profile, service placement, dependencies, data class, credentials, network planes, lifecycle owner, failure behavior, evidence status.
- Track each file as discovered/fetched/classified/reviewed/superseded/unresolved; avoid claiming a full-repository semantic scan from a bounded review.
- Exit: all relevant claims point to exact path/ref/SHA/status and all conflicts have IDs/owners.

### Phase A2 — hardware/OS profile definition (documentary first)
- Mac Pro: record exact model/configuration, macOS build/support, CPU/RAM/GPU/storage/NIC, thermals/power and target workloads.
- Mac mini 2011: record exact model/CPU/storage/NIC/firmware and Linux/kernel/security lifecycle compatibility; classify safe low-resource role.
- Future GPU server: define minimum/target GPU/VRAM/RAM/storage/network/security/remote-management/cost requirements without selecting hardware prematurely.
- Distinguish current developer nodes, customer-site prototype, test stand, user-contributed pool and future owned GPU pool.
- Exit: per-node target profile is complete enough to determine compatibility; unknown facts remain explicitly UNKNOWN. No host/runtime inspection is included in this pass.

### Phase A3 — architecture decisions and component admission
- Resolve local inference composition (Alamo/Ollama/ONNX Runtime/llama.cpp) and exact model-service boundary.
- Resolve single lifecycle owner for Jarvis/ASTRA queue/lease/retry/evidence promotion.
- Define APIs/schemas/versioning, node identity, admission, lease, dispatch, heartbeat, cancellation, result validation, evidence, revocation and failure/degraded modes.
- Pin candidate repository, release/tag/commit, license, provenance, dependency lock, SBOM/signature/security status, supported OS/architecture and resource envelope.
- Keep target-gated/future-gated/reference components inactive until their admission gates pass.
- Exit: owner decisions recorded; no duplicate authority/queue; each selected component has an explicit role and acceptance evidence plan.

### Phase A4 — deployment package design
- Produce a versioned, provenance-bound bundle per supported profile, with pinned source/build identity, dependency manifest, SBOM/license notices, checksums/signature policy, configuration templates, secret references, preflight, service identities/permissions, network rules, health/readiness gates, diagnostics, update/rollback and recovery procedures.
- Keep macOS and Linux profiles distinct; future GPU-server profile is optional and independently versioned.
- Do not assume containerization, Kubernetes, a second database/broker or distributed orchestration framework without a demonstrated capability gap.
- Exit: deployment package is reproducible on paper and has explicit rollback/restore and evidence schemas; this does not yet authorize installation.

### Phase A5 — explicitly authorized deployment
- Only after A0–A4 gates and separate owner permission, deploy to the intended developer targets.
- Install Mac Pro and Mac mini roles separately; keep user/client-site and contributed compute isolated.
- Add remote GPU server only when available and its own admission/profile is accepted.
- Do not use credentials or perform installation/host/infrastructure changes under this documentary checkpoint.
- Exit: deployment IDs, exact versions/configuration, secrets custody, health checks, logs and post-deploy evidence captured for each node.

### Phase A6 — developer-fabric qualification and operational readiness
- Independently verify Jarvis task lifecycle, ASTRA boundaries, GitHub provenance, mobile access/revocation, model routing/no-silent-fallback, network segmentation, resource quotas, failure/degraded operation, restart/recovery, updates/rollback and evidence publication.
- Bind evidence to exact commit/build, hardware and OS profile. Distinguish architecture, implementation, verification, qualification, release and production acceptance.
- Exit: explicit gate-by-gate evidence and owner acceptance for the developer environment. Current project status is not promoted by this plan.

### Phase B0 — start MediaHub OS product development
- Begins only after the developer fabric is deployed and accepted against its own gates.
- Then route through MH-01…MH-25 and Baseline 2.0, complete the unified contract matrix and resolve product-specific owner/governance blockers.
- Product-state, Smart Home, privacy, persistence, update/recovery, domain and qualification contracts remain independent of Jarvis/Astra authority.
- No product deployment or production acceptance is implied.

## 6. Immediate next bounded pass

1. Re-read the live map/checkpoint and the sources listed above.
2. Build a source-anchored node/service placement matrix from existing documents, without inventing hardware specifications.
3. Extract every existing component/provider/model/router/mobile/network choice and classify it as ACCEPTED TARGET, SELECTED, TARGET-GATED, CANDIDATE, PROPOSED, UNKNOWN or NOT AUTHORIZED.
4. Produce a conflict/decision register, prioritizing Alamo vs Ollama/ONNX/llama.cpp, Jarvis vs ASTRA lifecycle ownership, Mac Pro role transition, Mac mini compatibility, and developer mobile trust/authorization.
5. Only after the documentary crosswalk, ask the owner for the minimal decisions that cannot be resolved from accepted sources.

## 7. Explicit non-claims and restrictions

- No software was installed; no tests or qualification were run; no model/provider was invoked; no credentials or host/runtime data were inspected.
- No hardware capability or compatibility is asserted from model name/RAM alone.
- No deployment, migration, merge, rebase, cherry-pick or infrastructure change occurred.
- This checkpoint is a working plan, not a new accepted baseline and not deployment authorization.


## Continuation addendum — plan-of-record handoff refresh (2026-10-13)

This supporting plan remains a historical hardware/contour planning note. Sequencing is controlled only by `MEDIAHUB-MASTER-DEVELOPMENT-ROADMAP-1.0.md`.

The node/service placement artifact already exists at `docs/checkpoints/MEDIAHUB-NODE-SERVICE-PLACEMENT-AND-DECISION-REGISTER-01.md`; the owner-decision packet now exists at `docs/checkpoints/MEDIAHUB-OWNER-DECISION-PACKET-01.md`. Do not duplicate the placement inventory.

Next documentary pass: validate DEC-DEV-01…08 against exact primary clauses and live refs/SHA; update only confirmed mappings in the working unified traceability matrix and Passport; then prepare a minimal owner questionnaire with options, consequences and recommendations. Preserve all open owner decisions and Contour A → Contour B gate. Do not run tests/qualification or perform installation, provider/model calls, host/runtime inspection, credential use, deployment or infrastructure changes without separate authorization.
