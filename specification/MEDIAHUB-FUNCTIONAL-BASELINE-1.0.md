# MEDIAHUB OS 11.x LTS / MEDIAHUB iOS
# FUNCTIONAL BASELINE 1.0 — NORMATIVE SINGLE SOURCE OF TRUTH

**Status:** NORMATIVE / SINGLE SOURCE OF TRUTH
**Scope:** MediaHub OS 11.x LTS / MediaHub iOS
**Purpose:** единственный эталонный функциональный паспорт платформы.
**Change policy:** baseline 1.0 immutable; изменения только через новую версию и governance-проход.

## 0. НОРМАТИВНЫЙ СТАТУС

Этот документ фиксирует утверждённый Functional Baseline 1.0 проекта MediaHub.
Он имеет приоритет над всеми capability, contract, architecture, planning, implementation,
test и operational документами в части функционального смысла системы.

Противоречащий артефакт не расширяет и не изменяет baseline: он должен быть исправлен,
помечен obsolete или отправлен на reconciliation. Запрещён silent architectural drift.

Документы нижнего уровня являются реализацией, детализацией или доказательством соответствия,
но не альтернативным источником функциональной истины.

## 1. НАЗНАЧЕНИЕ И ФИЛОСОФИЯ

MediaHub — локально-ориентированная единая ОС для Smart Home, мультимедиа, документов,
зданий, Digital Twin, инженерии, AI, локальных и распределённых вычислений, сети,
мобильного доступа и профессиональной/коммерческой эксплуатации.

Философия: **Local First → Unified State → Unified UI → AI Assisted → Controlled Cloud Escalation**.

Основные уровни:
Hardware/Infrastructure → MediaHub OS Core → State Authority → domain systems → AI tiers
→ Mobile Access Layer / Cloud Development AI → controlled development infrastructure.

## 2. STATE AUTHORITY

**MediaHub State Authority** — единственный канонический источник истины платформенного состояния.
AI, cloud, mobile, HA UI, external ecosystem и отдельный automation engine не являются
альтернативной authority.

State Authority работает fail-closed. Её отказ не создаёт fallback authority.
Все домены интегрируются через формальные контракты; скрытые прямые authority-links запрещены.

## 3. SMART HOME AUTHORITY

**Home Assistant Core** является единственным authority домена Smart Home: integrations,
devices, entities, states, events, services, triggers, conditions, actions, scenes и automations.

Пользовательский интерфейс — MediaHub UI; HA UI не является пользовательским UI.
AI и внешние интерфейсы не обходят HA Core или Smart Home Layer.

Цепочка: Physical Device → Vendor Protocol/Integration → HA Core → MediaHub Smart Home Layer
→ MediaHub API → MediaHub UI → User/AI/Voice.

## 4. SMART HOME И ИНТЕГРАЦИИ

Smart Home Layer расширяем через adapters/integrations. Целевые производители: Центр Свет,
Arlight, Maytoni, Kincony, Dahua, Hikvision, Ajax, Keenetic, Ubiquiti.

Поддержка производителя считается фактической только после qualification. Процесс нового устройства:
Discovery → Identification → Compatibility → Integration Proposal → User Confirmation → Installation
→ Verification → MediaHub UI.

Kincony/KCS: USB auto-detection board/model/firmware/compatibility; предложение latest compatible
KCS firmware; параметры KCS доступны через MediaHub UI/API. Web UI KCS не является MediaHub UI.

Wired: DALI, RS-485, KNX и иные engineering protocols через gateways/hubs/adapters/controllers.
Wireless: расширяемые integrations/adapters с seamless coverage через совместимую инфраструктуру.
Virtual Ubiquiti Server допускается для централизованного управления совместимой Ubiquiti infra
при соблюдении лицензий, API, ToS и security; он не является State Authority.

Smart Home automation: automations, scenes, triggers, conditions, actions, schedules, events,
presence, energy, security. AI advisory/proposal only; изменения проходят controlled mechanisms.

Экспорт: Yandex Alice, Loxone, Apple HomeKit, Remote MediaHub Hub app. Внешние системы никогда
не становятся authority. Голосовой порядок строго: Google Assistant → Яндекс Алиса → Apple Siri.

## 5. MEDIAHUB UI И MEDIA

MediaHub UI — единая пользовательская система управления: минималистичная, преимущественно серая,
интуитивная, с UX максимально близким к Apple macOS при собственной идентичности.

Пользователь не обязан знать backend, компонент, database, adapter или local/cluster topology.

Media domain: audio, video, TV, streaming, playback, multiroom, local/network media, HDMI, 4K,
phone endpoints, gaming и external projection. Media не является альтернативной authority.

iPhone media redirect: iPhone → MediaHub, включая 4K через AirPlay при совместимости,
network/auth, codec, latency, resolution и bandwidth constraints.

## 6. DOCUMENTS / DIGITAL TWIN / ENGINEERING

Document System — professional/paid: documents, OCR, classification, search, metadata,
provenance, knowledge extraction, workflows and structured information. Mature OSS, включая
PaddleOCR, допускается только после qualification.

Digital Twin физически присутствует в Full editions для Mac mini/Mini PC; это не отдельная OS.
Professional functionality locked/unlicensed до paid entitlement: buildings, rooms, equipment,
engineering, spatial/3D, BIM, simulation, monitoring.

Engineering System — professional/paid: calculations, buildings, networks, spatial/BIM,
Digital Twin, simulation, technical documentation, inspection and analysis.
OSS используется только после license/security/provenance/benchmark/adapter qualification.

## 7. NETWORK И DISCOVERY

Network: wired/wireless/mesh/VLAN/routing/monitoring/diagnostics/discovery/controlled remote access,
seamless coverage; vendor APIs/adapters используются только через governed boundaries.

Equipment discovery охватывает cameras, intercoms, controllers, hubs, network и Smart Home.
Идентификация, compatibility, integration, onboarding и UI проходят через MediaHub.
AI может помогать, но не bypass security.

## 8. AI АРХИТЕКТУРА

Mobile Access Layer — не AI tier. Каноническая цепочка:
**Mobile Access Layer → Local AI → Local Cluster AI → Cloud Development AI**.

Local AI: local inference, natural language, analysis, assistance, automation assistance,
equipment setup/instructions, search, local data, Smart Home, media и documents.
Local AI advisory/proposal only и не является State Authority.

Local Cluster AI — trusted MediaHub Cluster: heavy inference, batch, CV, media, generation,
engineering, Digital Twin и distributed tasks. Доступ через AI Gateway.

Cloud Development AI — корпоративная облачная вычислительная среда MediaHub. Обычные пользователи
не имеют прямого доступа. Local/Cluster могут эскалировать через AI Gateway только при нехватке
local resources и при policy, privacy, authorization, residency и egress controls.
Cloud не является authority.

Эскалация определяется latency, privacy, capability, resources, data classification, criticality,
user policy, cost и network. Ни один AI tier не получает mutation authority автоматически.

## 9. TRUSTED SOURCES INTELLIGENCE ENGINE

Trusted Sources Intelligence Engine — first-class Cloud Development AI subsystem:
discovery, source search/classification, retrieval, verification, provenance, source comparison,
change detection, evidence и verified knowledge.

Должны различаться verified evidence, external source, inferred information и AI-generated content.
AI-generated content автоматически verified не считается.

## 10. AI HUMAN CLONE

AI Human Clone — отдельная Cloud Development AI subsystem для авторизованного media content:
visual/audio, video, presentations, education, marketing и commercial use.

Обязательны consent, authorization, identity provenance, rights-holder authorization, scope,
voice/appearance authorization, model/asset provenance, audit, revocation и separation
real/synthetic. Human Clone не является State Authority, Smart Home authority или заменой человека.

## 11. MOBILE ACCESS LAYER — РОВНО ДВА ПРИЛОЖЕНИЯ

### 11.1 MediaHub Core for iPad / MediaHub Core iOS/iPadOS

Полноценная минимальная локальная версия MediaHub, непосредственно устанавливаемая на iPad.
Это не remote client. В пределах ресурсов устройства содержит Local Core/UI/Smart Home/media/
AI и работает с локальным state. Это первое мобильное полноценное минимальное Core-издание.
Продукт платный, one-time payment at installation on device.

### 11.2 Remote Mobile Application

Отдельное remote access application через MediaHub API: access, management, monitoring,
notifications, interaction и разрешённые services. Это не local Core.

### 11.3 Mobile invariants

Ни одно мобильное приложение не является authority. Нет прямого physical-device bypass MediaHub.
Нет alternative State Authority. Действуют contracts, authentication, authorization, trust,
privacy, audit и revocation.

Remote chain: Remote Mobile → MediaHub API → MediaHub Core/State Authority/subsystem.
Local iPad chain: iPad → MediaHub Core iOS/iPadOS → Local MediaHub Core → State/Smart Home/Media/Local AI.

## 12. CLOUD DEVELOPMENT AI И DEVELOPMENT ENVIRONMENT

Cloud Development AI включает Website, Trusted Sources Intelligence, AI Human Clone,
Engineering/Commercial Infrastructure, Digital Twin processing, AI/GPU и development/commercial
capabilities.

Cloud Development Environment — корпоративный engineering contour MediaHub, а не пользовательское
облако. Обычный пользователь прямого доступа не получает.

Cloud boundary: authorization, minimization, residency, egress control, audit, metering,
revocation, isolation, workload identity, quotas. Запрещён uncontrolled cloud access к State Authority.

## 13. EDITIONS

- MediaHub OS Full for Mac mini
- MediaHub OS Full for Mini PC
- Hub OS Raspberry Pi
- MediaHub Core iOS/iPadOS — paid one-time
- MediaHub iOS Remote
- OS Developer
- iOS Developer
- Digital Twin — не отдельная OS

AI-помощь для добавления устройств, configuration, instructions и explanation доступна в подходящих editions.
Document System, Digital Twin professional, Engineering и relevant commercial capabilities — paid.

## 14. UPDATE / BACKUP / RECOVERY

Update UX: Settings → Update; notification о новой версии; current/new version, changes,
functions, fixes, warnings; explicit user confirmation; lifecycle eligibility, integrity,
compatibility, provenance, authorization, secure install, health и activation; rollback/recovery.
State/config/data/provenance/security должны сохраняться.

Target OTA: RAUC. RAUC и Mender не используются одновременно как две production authorities без
отдельного решения и qualification.

Backup/recovery/migration/rollback/disaster recovery должны сохранять integrity и не создавать
alternative authority.

## 15. SECURITY / TRUST

Security: secure boot, identity, authentication, authorization, trust boundaries, least privilege,
secrets, audit, provenance, encryption, isolation, secure update, rollback/recovery, device trust,
cloud boundary и egress control.

Unknown/untrusted devices: DENY или QUARANTINE. Ambiguity: FAIL CLOSED.

LOCAL_ONLY должен сохранять State Authority, Smart Home, local control/automation/AI/media,
diagnostics и recovery без Internet/Cloud.

## 16. CLUSTER / OBSERVABILITY / DATA

Trusted Local MediaHub Cluster: distributed compute/GPU/storage/scheduling, node identity,
health, telemetry, recovery и scaling. Cloud Development Cluster — отдельный trust/control plane.

Observability: telemetry, metrics, logs, traces, health, readiness, diagnostics, alerts и audit.
Целевые технологии: OpenTelemetry и Prometheus.

Storage baseline: PostgreSQL + pgvector + S3-compatible object storage + backup/local storage
+ provenance metadata. Qdrant допускается только если benchmark докажет необходимость.

Knowledge/search: semantic/full-text, knowledge graph, provenance, evidence, document search,
source verification. Knowledge/search не является State Authority.

## 17. OSS FOUNDATION

P0: Home Assistant Core, IfcOpenShell, web-ifc, PaddleOCR, OpenCV, ONNX Runtime, llama.cpp,
PostgreSQL, pgvector, Temporal, OpenTelemetry, Prometheus, Cosign, Syft, Trivy, restic,
RAUC, OpenBao, S3-compatible object storage, OCI registry.

P1: ComfyUI, Qdrant only if needed, OpenDroneMap, VTK/vtk.js, K3s/Kubernetes, Argo CD,
Harbor if needed, distributed object storage, GPU cluster, Roc if needed, Paperless-ngx adapter,
PhotoPrism adapter, Owncast, vLLM/SGLang benchmark/select one if needed.

Reference/integration: Jellyfin, Immich, FreeCAD, Massing, CloudCompare, Mender, n8n.
Reference products не становятся core authority.

OSS adoption rule: Real Capability Gap → Mature Component Search → License Review → Security Review
→ Provenance → Adapter → Benchmark → Adoption.

## 18. ARCHITECTURAL PROHIBITIONS

Запрещено: второй State Authority; AI как canonical authority; Cloud как uncontrolled authority;
Bypass Home Assistant Core; альтернативная production OTA authority без отдельного решения;
overlapping storage без доказанной необходимости; несколько production AI runtimes без benchmark;
reference product как core authority; self-review как independent qualification; hidden direct links.

## 19. QUALIFICATION / RELEASE GATES

Production chain:
Implementation → unit/integration/negative-path tests → security → regression → provenance
→ independent review → MH-05 → T5 → F-03 → release qualification → production authorization.

AI/autonomous agent не может объявить independent qualification, release или production authorization.
Release locked until qualified. Production not authorized до прохождения всех обязательных gates.

## 20. CONTRACT / TRACEABILITY INVARIANT

Для каждого функционального требования должна существовать трасса:
Passport → Capability → Contract → Architecture → Implementation → Tests → Qualification Evidence.

Интеграционный принцип: Contract → Adapter → Validation → Integration → Qualification.
Все домены связаны через contracts; hidden direct links запрещены.

## 21. GIT / PROVENANCE INVARIANTS

Immutable R4 baseline не изменяется: no rebase, amend, reset, force-push или modification.
Ранее технически проверенный R4 anchor:
- commit: `471f709f5633feab7aeb62dd3ea52effad6d2bc4`
- tree: `2279612908135418b2b5448d598274ea6741deaa`

В исходном тексте утверждённого паспорта указан SHA с окончанием `...2bc584`.
Это расхождение не исправляется молча и не изменяет immutable R4 anchor; требуется отдельная
technical reconciliation перед использованием SHA как machine identity.

## 22. AUTONOMOUS DEVELOPMENT

Локальные AI/developer agents, GitHub, ECC, Claude, Codex и другие исполнители действуют
только в пределах governance. AI — advisory/proposal only; не authority, не release approver
и не независимый квалификатор.

Каждое изменение должно быть reproducible, traceable, testable и привязано к commit SHA.
При ambiguity или hard governance gate автоматическая цепочка останавливается.
