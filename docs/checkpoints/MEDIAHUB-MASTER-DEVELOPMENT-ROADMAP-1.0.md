# MediaHub — Master Development Roadmap 1.0
- Date: 2026-10-13
- Owner direction: user explicitly directs that this roadmap be the single working plan of record for subsequent development sequencing.
- Ref: `docs/mediahub-chat-tree-map-20261012`
- Status: **OWNER-DIRECTED MASTER PLAN / WORKING CONTROL DOCUMENT**. This is not a replacement for accepted architecture, Baseline 2.0, domain contracts, or governance decisions. It grants no permission to install software, inspect hosts/runtime, run tests/qualification, invoke models/providers, change infrastructure, deploy, merge, rebase, or cherry-pick.
- Navigation authority: `docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md` on the same ref.
- Supporting initial plan: `docs/checkpoints/MEDIAHUB-DEVELOPER-FABRIC-UNIFIED-PLAN-2026-10-13.md`.
- Functional authority: `docs/checkpoints/mediahub-functional-baseline-2.0.md@main`, blob `1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f`.
- Historical provenance: `specification/MEDIAHUB-FUNCTIONAL-BASELINE-1.0.md@main`, blob `9df4892ed0734050ac79732603d15bb414717310`; do not merge implicitly with Baseline 2.0.

## 0. Executive decision and operating rule

The work is divided into two sequentially gated contours:

- **Contour A — Developer Fabric:** cloud development services, developer-controlled servers, Mac Pro 2013/macOS, Mac mini Server 2011/Linux/16 GB, future remote owned GPU/video server, Jarvis, ASTRA/Astra Gold, model/provider/tool routing, engineering memory and provenance, GitHub integration, developer mobile app, reproducible install/update/recovery and evidence.
- **Contour B — MediaHub OS product:** product architecture and implementation in autonomous development begins only after Contour A has been deployed and independently accepted against explicit readiness gates. Product work must not be silently mixed into the developer fabric.

The roadmap governs **work order and traceability**, not architecture authority. Where an accepted primary source conflicts with a proposal, preserve the conflict and route it to the owner; do not normalize it by editing the baseline. All decisions and claims must be labeled by status and linked to source evidence.

### Non-negotiable operating rules

1. Read this roadmap, the current project map, latest continuation checkpoint and linked primary sources before each material action.
2. Check branch/ref, blob SHA, relevant commit, status, dependencies and current `main HEAD`; record divergences and never merge/rebase to “fix” them without separate authorization.
3. Preserve historical IDs. Check identifier collisions before minting any new stable ID.
4. Baseline 2.0 is the current canonical functional reference. Baseline 1.0 is historical provenance only unless the owner explicitly directs otherwise.
5. The map is an index; it is not a replacement for source contracts or evidence.
6. Never mark a design implemented, tested, verified, qualified, released, deployed, observed or production-accepted without the corresponding evidence and authority.
7. Separate reported, observed, desired, policy-allowed, commanded, committed, applied, confirmed and predicted states.
8. Product State Authority alone owns canonical MediaHub product-state mutation. Jarvis/ASTRA are engineering coordination/execution components, not Product State Authority. Home Assistant Core remains the Smart Home authority within approved boundaries.
9. Default to least privilege, local-first where required, fail-closed on unknown authorization, and explicit data-egress/provider policy. Local-only inference must not silently fall back to cloud.
10. Do not install software, run tests/qualification, invoke models/providers, use credentials, inspect host/runtime, modify infrastructure, deploy, migrate, merge, rebase or cherry-pick without the relevant explicit authorization.

## 1. Source hierarchy and status vocabulary

### 1.1 Source precedence

1. Explicit owner decisions and governance records within their authority.
2. Accepted Baseline 2.0 and accepted domain primary contracts/acceptance records.
3. Canonical Component Manifest 2.0 for component selection boundaries.
4. Accepted target architecture documents, including Distributed AI Infrastructure, within their declared scope.
5. Domain design/acceptance/evidence documents.
6. Working cross-domain matrix, unified deployment contract, passport and this roadmap as planning/traceability artifacts.
7. Chat history and inferred expectations (never sufficient evidence on their own).

Baseline 1.0 remains a historical source and must not be blended into Baseline 2.0 without explicit change control.

### 1.2 Statuses must not be conflated

Use the existing project status vocabulary where defined. At minimum distinguish:
- `OWNER-DECIDED`
- `ACCEPTED CANONICAL`
- `ACCEPTED TARGET / NOT RUNTIME-QUALIFIED`
- `SELECTED / NOT DEPLOYED`
- `TARGET-GATED` / `FUTURE-GATED`
- `PROPOSED`
- `UNKNOWN / NOT EVIDENCED`
- `BLOCKED`
- `IMPLEMENTED`
- `TESTED`
- `VERIFIED`
- `QUALIFICATION CANDIDATE`
- `QUALIFIED`
- `RELEASED`
- `DEPLOYED`
- `OBSERVED`
- `PRODUCTION ACCEPTED`

A component being selected is not proof of compatibility, installation or qualification. A document being written is not proof that its requirement is satisfied.

## 2. Hardware and trust-domain plan of record

| ID | Node / domain | Target role | Constraints and required evidence | Plan status |
|---|---|---|---|---|
| HW-DEV-01 | Mac Pro 2013, macOS | Primary developer workstation and central developer-fabric node: Jarvis/control services, model/API routing, task coordination, monitoring, node registry and proposed local inference endpoint | Exact CPU/RAM/GPU/storage/NIC/macOS build, service resource envelope, supported security lifecycle, local inference capacity and recovery evidence remain unknown | Owner-directed target; compatibility not evidenced |
| HW-DEV-02 | Mac mini Server 2011, clean Linux, 16 GB RAM | Existing low-resource developer/server worker for explicitly assigned auxiliary services after compatibility review | Exact identifier, CPU, storage, NIC, firmware/EFI, Linux/kernel support, security maintenance, resource and thermal/power behavior unknown | Owner-directed target; MH-15 acceptance/implementation not authorized |
| HW-DEV-03 | Future remote owned GPU/video server | Optional later compute capacity for GPU/video/model workloads | Hardware/location/OS/GPU/VRAM/RAM/storage/network/remote management/cost/data classification/security profile unknown | Future-gated; not required for initial fabric |
| HW-DEV-04 | MacBook developer clients | Developer UI/client access and approved workflows | Device identity, endpoint security, session/revocation and access scope | Existing architectural role; acceptance evidence required |
| HW-DEV-05 | Developer Mobile app | Developer-only client to approved Jarvis interfaces over private mesh/P2P where selected | Mesh membership is not application authorization; identity, authorization, revocation, audit and lost-device handling required | Scope owner-confirmed; implementation/qualification not evidenced |
| HW-DEV-06 | European VPS | Narrow API-key registration/management workflow only | Must not become a general inference gateway or ordinary data transit; secret custody and network/API boundary need evidence | Restricted role from accepted target architecture |
| HW-TEST-* | Existing development/test servers | Test/staging only until individually classified | No host/runtime inspection or reclassification without authorization; identity and evidence must be per-host | Existing assets; inventory incomplete |
| HW-CUSTOMER-* | Client-site Mac mini M2 prototype | Separate customer trust domain/prototype | No implicit access to developer secrets, queues, data or compute pool | Separate domain |
| HW-POOL-B | User-contributed compute | Opt-in, isolated, quota-limited, verifiable, revocable untrusted pool | Explicit consent, job/data classification, sandbox, egress restrictions, result validation and revocation | Not equivalent to owned GPU server |

**Asset identity rule:** do not assume a future production Mac Pro is the same physical machine as the current developer Mac Pro. Any role transfer requires an owner decision and a separate identity, data, credential, installation and recovery plan.

## 3. Work breakdown and phase gates

Every phase has an output, an exit gate and a no-go condition. Phases may overlap only for read-only inventory work; downstream implementation or deployment gates may not be bypassed.

### Phase 00 — Bootstrap and source-of-truth reconciliation (P0)
**Actions**
- Read map, latest continuation checkpoint and this roadmap.
- Refresh the relevant primary sources from their stated refs and record blob SHA/commit SHA.
- Re-check `main HEAD` and branch divergence.
- Establish source precedence, scope boundaries and current status of each referenced artifact.
- Create no duplicate ID and no silent baseline rewrite.

**Outputs:** source register; current ref/sha ledger; confirmed blockers; map/checkpoint links.
**Exit:** all planned work items have a source route and a named decision owner (or explicitly UNKNOWN).
**No-go:** stale/unavailable source, unresolved ref ambiguity, or missing authority.

### Phase 01 — Developer-fabric requirements and traceability (P0)
**Actions**
- Extract existing requirements from Distributed AI Infrastructure, Jarvis gap report, canonical component manifest, MH-15/MH-16, deployment contract, unified matrix, Passport v3 and domain security/network sources.
- For each requirement record: stable ID (preserve historical IDs), source clause, source ref/SHA, status, owner, dependencies, target node, data class, failure behavior, acceptance criterion, evidence type, unresolved decision.
- Reconcile duplicates, contradictions and omissions; do not treat the draft unified matrix as canonical without owner/governance review.

**Outputs:** source-anchored requirement/contract crosswalk and discrepancy register.
**Exit:** every material developer-fabric requirement is traceable to a source and acceptance/evidence plan; uncovered requirements remain visibly OPEN.
**No-go:** an assertion relies only on chat memory or an unaccepted draft.

### Phase 02 — Hardware profiles and service placement (P0)
**Actions**
- Build a service-placement matrix for each service: role, host, OS/architecture, CPU/RAM/GPU/storage/network envelope, dependencies, trust zone, identity, ports/flows, data class, secret access, lifecycle owner, health/readiness semantics, restart/recovery, backup/restore, acceptance evidence.
- Define the Mac Pro profile without presuming unreported specifications.
- Define a conservative Mac mini 2011/Linux eligibility profile; do not assign critical services before OS/security/resource compatibility is evidenced.
- Define future GPU server as optional profile with an admission interface, not an initial dependency.
- Preserve separation between owned developer nodes, customer-site prototype, test hosts, VPS and contributed pool.

**Outputs:** hardware capability unknowns list; node/service placement matrix; network/trust-zone sketch; per-node acceptance plan.
**Exit:** every service has an explicit intended placement or a recorded decision/blocker.
**No-go:** guessed hardware specifications, unsupported OS assumptions or implicit trust-domain joins.

### Phase 03 — Jarvis / ASTRA responsibility and lifecycle reconciliation (P0)
**Actions**
- Define Jarvis as the umbrella engineering/orchestration system; ASTRA/Astra Gold is a bounded subsystem.
- Assign exactly one authoritative owner for task state, queue lifecycle, claim/lease, retry/cancellation, result validation, evidence promotion and gate transitions; adapters may delegate but must not create competing authorities.
- Specify task envelope, idempotency, timeouts, cancellation, retries, worker heartbeat, provenance, audit, cost/resource quota, concurrency, failure/recovery and operator intervention.
- Define the boundary between engineering task state and canonical MediaHub product state.
- Check existing ASTRA G0–G11 and MH-22 evidence; do not promote blocked gates.

**Outputs:** ownership/sequence diagram; lifecycle contract; failure-mode and recovery table; open owner decisions.
**Exit:** no duplicate state authority or queue owner; all transition authority and evidence obligations explicit.
**No-go:** ASTRA/Jarvis silently mutates product state or promotes qualification without authorized evidence.

### Phase 04 — Models, providers, tools and engineering memory (P0)
**Actions**
- Reconcile Alamo (service/endpoint name), Ollama, ONNX Runtime and llama.cpp: classify each as service, runtime, adapter, candidate or alternative only from source evidence; request owner decision where evidence cannot disambiguate.
- Inventory Claude/Codex, FCC, FreeLLMAPI and all other provider/tool paths already recorded in the repo. Do not invent additional mandatory providers.
- Define provider/model identity, API compatibility, allowed data classes, egress policy, retention, quota/cost, timeouts, retry policy, rate limits, credential reference (never credential value), audit and degradation mode.
- Define explicit local-only/cloud-allowed policy; local-only failure must fail closed without silent cloud fallback.
- Define memory/context scope, provenance, retention, deletion, retrieval isolation and secret exclusion.
- Define tool capabilities as typed, least-privilege contracts with authorization, confirmation and audit.

**Outputs:** model/provider/tool registry; data-egress matrix; memory/context contract; explicit architecture decisions.
**Exit:** every route has a defined policy and observable behavior; unresolved choices are owner-owned.
**No-go:** no evidence of API compatibility, silent provider failover, secret exposure or uncontrolled egress.

### Phase 05 — Developer Mobile and remote access (P1, blocks mobile acceptance)
**Actions**
- Specify developer-only user journeys and APIs.
- Separate private mesh connectivity from application identity and authorization.
- Define enrollment, strong identity, session expiry, device revocation, lost-device handling, audit, API scopes and prohibited actions.
- Do not expose shell/admin/host control solely through network membership.
- Define offline and degraded behavior and the data visible on the mobile device.

**Outputs:** mobile API contract, identity/authorization matrix, revocation and acceptance plan.
**Exit:** every mobile operation is authorized by an application-level policy and auditable.
**No-go:** mesh membership grants implicit privileges or revoked devices retain access.

### Phase 06 — Component admission and reproducible software bill of materials (P0)
**Actions**
- Treat Canonical Component Manifest 2.0 as the component-selection input within its declared scope.
- For each component record official repository, pinned release/commit, license, provenance, dependency lock, SBOM, signature/checksum policy, supported OS/CPU, resources, network requirements, secrets, upgrade/rollback path and acceptance evidence.
- Classify components SELECTED, TARGET-GATED, FUTURE-GATED, CANDIDATE or PROPOSED using source-defined semantics.
- Do not add infrastructure (orchestration framework, broker, database, container platform, second state store) unless a documented capability gap and owner-approved ADR justify it.

**Outputs:** pinned component registry, software BOM/SBOM plan, license/security review queue, per-component gate table.
**Exit:** all selected components have provenance and compatibility/acceptance plans.
**No-go:** moving target tags, unverified binaries, unclear licenses, or a gated component entering runtime without admission.

### Phase 07 — Installation, update, rollback and recovery design (P0)
**Actions**
- Follow MH-15 and MH-16 source contracts; do not treat this roadmap as authorization to implement them.
- Create distinct deployment profiles for macOS and Linux; future GPU profile is separately versioned.
- Define preflight and non-destructive checks, dependency ordering, service identity/permissions, network rules, config templates, secret references, health/readiness checks, diagnostics, backups, restore, update, rollback and recovery.
- Define idempotency, partial-failure behavior, interrupted-install recovery, version compatibility and security-floor enforcement.
- Distinguish host boot, service started, service READY, fabric healthy and fabric accepted.

**Outputs:** reproducible install bundle specification; configuration templates; operations/recovery guide; explicit destructive-action approval boundaries.
**Exit:** complete deployment/rollback/restore/evidence design accepted by the owner and applicable architecture governance.
**No-go:** MH-15/MH-16 authorization missing, destructive behavior ambiguous, or rollback violates security/data invariants.

### Phase 08 — Authorized deployment of Contour A (P0; explicit authorization required)
**Actions after separate authorization only**
- Deploy the Mac Pro profile and Mac mini profile independently, respecting compatibility and security gates.
- Keep optional GPU server disconnected from initial critical path until its profile is accepted.
- Deploy developer mobile client only after API and identity contracts are accepted.
- Keep VPS, customer-site prototype, test hosts and contributed pool in their own trust boundaries.
- Capture exact artifact/build/config identity and evidence per node; never record secret values.

**Outputs:** per-node deployment record, exact versions, approved configuration hashes, readiness evidence, diagnostics and rollback record.
**Exit:** every in-scope node passes its approved deployment gate and owner accepts the resulting evidence.
**No-go:** missing authorization, failed preflight, unknown identity/configuration, or failed security/health gate.

### Phase 09 — Independent Developer Fabric qualification (P0; not yet passed)
**Required evidence families**
- GitHub source provenance and change authorization.
- Task lifecycle, single-owner state transitions, cancellation/retry/idempotency and audit.
- Provider/model routing, local-only fail-closed behavior and egress enforcement.
- Mobile identity, authorization, revocation and audit.
- Network segmentation and trust-domain isolation.
- Resource quotas, concurrency, cost controls and degraded operation.
- Restart/recovery, update/rollback, backup/restore and data integrity.
- Security baseline, secret handling, dependency provenance and license compliance.
- Monitoring/diagnostics and evidence reproducibility.

**Outputs:** gate-by-gate qualification dossier tied to exact build, commit, configuration, hardware and OS profile.
**Exit:** independent reviewer verifies evidence; owner explicitly accepts Contour A readiness.
**No-go:** missing evidence, inferred PASS, failed control or unresolved critical blocker. Current global qualification remains NO-GO / NOT PROVEN until new authorized evidence says otherwise.

### Phase 10 — Start MediaHub OS product development (Contour B; gated by Phase 09)
**Actions**
- Start only after Contour A deployment and acceptance are explicitly evidenced.
- Follow MH-01…MH-25 navigation in the current map and Baseline 2.0.
- Build the unified contract matrix from primary domain sources, not by flattening draft documents.
- Resolve Product State Authority, security/privacy, persistence, Smart Home, installer/update/recovery, qualification and domain-specific governance contracts separately.
- Keep Jarvis/ASTRA engineering state outside canonical product state.

**Outputs:** accepted product development workspace and domain-by-domain work queue.
**Exit:** product work begins under accepted Baseline 2.0/domain contracts, with source traceability and gate ownership.
**No-go:** Contour A not accepted, canonical contract missing, or owner decision unresolved.

## 4. Immediate priority backlog

1. **P0-01 — Source/ref freshness ledger:** recheck current map/checkpoint and source SHAs; record current `main HEAD` and branch divergence.
2. **P0-02 — Node/service placement matrix:** derive rows only from the accepted target architecture and component/domain sources; label unknowns.
3. **P0-03 — Decision register:** resolve Alamo/Ollama/ONNX/llama.cpp composition; Jarvis/ASTRA lifecycle ownership; developer-vs-production Mac Pro identity; Mac mini compatibility; mobile identity/revocation; provider egress/retention.
4. **P0-04 — Component registry:** reconcile canonical component manifest with actual target placement, pinned refs, platform support, license/provenance and gate status.
5. **P0-05 — Requirements/contract crosswalk:** trace each service-placement row to contract, acceptance criteria and evidence.
6. **P0-06 — Deployment package contract:** complete macOS/Linux profile design and rollback/recovery gates without executing installation.
7. **P0-07 — Developer-fabric qualification dossier schema:** define evidence package and reviewer/owner gates before deployment.
8. **P0-08 — Product contour handoff:** explicitly define the Contour A acceptance artifact that unlocks Contour B; do not begin product implementation before it passes.

P0-01 through P0-05 are documentary/source-reconciliation work. P0-06 and P0-07 are design work gated by existing MH-15/MH-16 authority. P0-08 is a governance/handoff definition. Deployment, tests and qualification remain separately authorized work.

## 5. Decision register — currently unresolved, do not guess

| Decision ID | Question | Current evidence | Required owner output |
|---|---|---|---|
| DEC-DEV-01 | Is Alamo a service name above a selected runtime, or does it denote a particular runtime? How do Ollama, ONNX Runtime and llama.cpp relate? | Different source documents use these labels; composition not proven | One approved composition diagram and role assignment, or explicit deferment |
| DEC-DEV-02 | Who owns authoritative task lifecycle, queue/claim/lease/retry/cancel and evidence promotion across Jarvis and ASTRA? | Jarvis umbrella / ASTRA subsystem framing exists; detailed single-owner boundary unresolved | One lifecycle owner plus typed adapter contract |
| DEC-DEV-03 | Is future production Mac Pro the same physical unit as developer Mac Pro? | Role ambiguity recorded in source reconciliation | Explicit same-asset/separate-asset decision |
| DEC-DEV-04 | Which services may run on Mac mini Server 2011? | 16 GB and Linux are owner-reported; detailed compatibility unknown; MH-15 not accepted | Hardware/OS compatibility evidence and approved workload profile |
| DEC-DEV-05 | Which model/provider routes may receive which data classes? | Local-only fail-closed target exists; provider details need pinned compatibility and policy evidence | Data-egress and provider policy approval |
| DEC-DEV-06 | What authorization/revocation contract governs Developer Mobile? | Private mesh/P2P is a connectivity path, not sufficient authorization | Identity/API scopes/revocation policy |
| DEC-DEV-07 | What exact hardware/OS profile will the future GPU server use? | Future node is a target capacity extension; specifications absent | Profile constraints first; hardware selection when appropriate |
| DEC-DEV-08 | What evidence and authority formally unlock Contour B? | This roadmap proposes Phase 09 acceptance as gate; not yet a new canonical governance rule | Owner acceptance of gate package and link to governing record |

No decision is silently made by this table. If an answer cannot be found in accepted primary sources, ask the owner at the point it blocks progress.

## 6. Required artifact set and maintenance

The following are maintained as linked, source-aware artifacts:
1. Project map — navigation index and status history.
2. This master roadmap — single sequencing/work-control plan.
3. Current continuation checkpoint — exact resume point, refs/SHAs, completed bounded work, blockers and next action.
4. Unified traceability matrix — working cross-domain crosswalk until governance accepts it.
5. Component manifest/registry — component selection and provenance.
6. Domain primary contracts and acceptance criteria — authority for domain decisions.
7. Decision/conflict register — unresolved owner choices and contradiction evidence.
8. Per-node service placement matrix — hardware and trust-domain mapping.
9. Deployment records and qualification dossier — only after separately authorized execution.

For each substantive pass, update the map and continuation checkpoint when there is a new verified fact, changed status, new artifact or next-step routing change. Re-read the changed files from GitHub after write and verify SHA/content. Avoid duplicating large documents or declaring a gap closed based on a proposed draft.

## 7. Change control for this roadmap

- This roadmap is the single working plan of record for **sequencing**. Earlier planning notes remain provenance/supporting detail and do not create parallel sequences.
- Any material change to order, phase gates, Contour A/B boundary, hardware roles or acceptance criteria must be recorded as a dated change note with rationale, source evidence, owner/authority, affected IDs and impact.
- Architecture decisions still belong in the relevant ADR/domain contract/governance record. Updating the roadmap alone does not accept an architecture decision.
- If a primary source or accepted owner decision contradicts this plan, stop the affected work, preserve the discrepancy, update the decision register and request resolution; do not silently follow the plan over the higher-authority source.
- No baseline, canonical matrix, domain acceptance state or qualification status is changed by this roadmap.

## 8. Current blockers and explicit non-claims

- Unified deployment contract v0.1 and unified traceability matrix v0.1 remain `PROPOSED / NOT ACCEPTED / NOT FROZEN`.
- Passport v3 and Verifiable Architecture Contract 01 remain working drafts, not canonical replacements.
- MH-15 acceptance/freeze and implementation authorization are absent.
- MH-16 remains proposed/not frozen; implementation is not authorized.
- ASTRA G0–G11 and MH-22 G1–G9 are blocked/not promotable in the inspected evidence snapshot.
- Overall project qualification remains `NO-GO / NOT PROVEN`.
- P0-07 → P0-05 canonical-read/authorization/publication gap remains open.
- Hardware compatibility, runtime state and actual deployment are not asserted by this document.
- No tests, qualification, model/provider invocation, credential use, host/runtime inspection, installation, infrastructure change, deployment, migration, merge, rebase or cherry-pick was performed.

## 9. Next bounded action

Follow the current map and checkpoint. The next pass is strictly documentary:

1. Extract source-anchored service-placement rows from `MEDIAHUB-DISTRIBUTED-AI-INFRASTRUCTURE.md`, the component manifest, MH-15/MH-16 and relevant network/security contracts.
2. For each row capture exact clause, path/ref/blob SHA, status, host target, dependency, unknowns, acceptance criterion and evidence type.
3. Create/update a dedicated placement-and-decision artifact only after confirming the path does not already exist and checking historical IDs.
4. Update map and checkpoint, read back every changed file, then report verified SHAs and remaining blockers.


## 10. Операционный контракт продолжения и актуальности ссылок (revision 2026-10-13)

Этот раздел уточняет исполнение единого плана и не меняет принятые доменные контракты, Baseline 2.0 или owner decisions.

### 10.1 Единая точка планирования

- Этот документ остаётся ЕДИНСТВЕННЫМ рабочим планом последовательности. Supporting plan — историческая исходная записка; его порядок работ не параллелен и не имеет приоритета над этим roadmap.
- Каждый `/next` должен выбрать следующий незакрытый шаг именно отсюда, проверить, не был ли он уже выполнен в более поздних commits/checkpoints, и завершить один ограниченный проход до проверяемого результата.
- Не начинать новый широкий аудит только потому, что он возможен. Продвигать конкретный незакрытый deliverable, его зависимости и критерии выхода; не повторять завершённое без обнаруженного расхождения или отсутствующего доказательства.
- После каждого запроса обновлять GitHub-контрольную запись. Карта обновляется, когда меняются навигация, source-of-truth, статусы или маршруты; current checkpoint обновляется после каждого существенного прохода. Матрица/паспорт обновляются только при изменении подтверждённой трассировки, а не ради формального дублирования.
- Не заменять отсутствующее решение владельца рекомендацией агента. Вынести минимальный набор вариантов, последствия и рекомендацию, затем ждать только там, где без решения нельзя безопасно продолжить; независимую документальную работу продолжать.

### 10.2 Проверка живого GitHub-состояния на каждом /next

До выбора работы заново проверить фактические refs/ветки, HEAD и доступность документов в GitHub; перечитать Bootstrap, карту, этот roadmap и current checkpoint по живой документационной ветке. Сверить blob SHA и содержание первичных источников, для которых важны другие refs, включая `main`. Перепроверить divergence/merge base и права на запись. Сохранённые в документах SHA — исторические контрольные значения, а не гарантия актуальности.

Изменение blob SHA при обычном коммите само по себе не означает, что надо менять URL. Если документационная ветка переименована/удалена, канонический checkpoint или файл перемещён, ссылка недоступна либо больше не указывает на актуальный артефакт, агент обязан:
1. восстановить корректные ссылки из фактических refs/paths;
2. обновить затронутые ссылки в доступных проектных документах в рамках разрешённых документальных изменений;
3. выполнить read-back и проверить SHA/содержимое;
4. в том же финальном ответе выдать готовое задание на замену ChatGPT Project Instructions с полным новым текстом и прямыми URL. Не утверждать, что пользовательские настройки ChatGPT изменены автоматически, если они не были изменены самим пользователем.

### 10.3 Критерий завершения каждого прохода

Проход считается завершённым, только если есть: (a) конкретный изменённый/проверенный deliverable; (b) source/ref/blob SHA; (c) критерий проверки и результат; (d) обновлённая checkpoint-запись; (e) обновлённая карта, если изменились навигация/статус/источники; (f) явные блокеры и следующий ограниченный шаг. Не заявлять тестирование, квалификацию, реализацию, deployment или acceptance без соответствующего независимого evidence.

### 10.4 Текущий следующий проход

Следующий незакрытый deliverable остаётся source-anchored node/service placement matrix плюс decision/conflict register. Он должен ссылаться на первичные пункты Distributed AI Infrastructure, Canonical Component Manifest 2.0, MH-15/MH-16 и применимые security/network contracts; различать accepted target, selected, target-gated, proposed, unknown и not authorized. Не выбирать за владельца между Alamo/Ollama/ONNX Runtime/llama.cpp и не назначать единого Jarvis/ASTRA lifecycle owner без решения владельца.
