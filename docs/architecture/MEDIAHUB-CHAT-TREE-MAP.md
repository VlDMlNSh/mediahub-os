# MediaHub — карта дерева архитектурных чатов и доменов

- Дата инвентаризации: 2026-10-12
- Репозиторий: `VlDMlNSh/mediahub-os`
- Базовая ветка для этой карты: `main`
- Ветка карты: `docs/mediahub-chat-tree-map-20261012`
- Статус карты: **ИНВЕНТАРИЗАЦИЯ / НЕ ПОЛНАЯ ПРИЁМКА**
- Назначение: единая точка входа для восстановления дерева MH-01…MH-25 и предотвращения повторного поиска одних и тех же материалов.

## 1. Правила интерпретации

1. Номер MH обозначает архитектурный/рабочий домен. Сам по себе номер не доказывает существование отдельного чата, его закрытие или принятие архитектуры.
2. Наличие файла, master prompt, ветки или упоминания в checkpoint не означает, что домен принят, заморожен, реализован, квалифицирован или допущен в production.
3. Отсутствие файла по одному ожидаемому пути не доказывает отсутствия документа: проверить варианты имени, другие каталоги, ветки и исторические checkpoints.
4. Статусы ниже зафиксированы по доступным репозиторным артефактам, прежде всего по `docs/checkpoints/mediahub-mh25-stage-reconciliation.md`; это не заявление о текущем выполнении всех работ.
5. Нельзя пересоздавать Functional Baseline 2.0 с нуля. Использовать существующий канонический baseline и его traceability matrix, исправляя только подтверждённые расхождения.
6. Перед merge любых архитектурных изменений нужно проверить локальные незакоммиченные файлы и происхождение источника. Не перезаписывать локальные изменения.

## 2. Дерево верхнего уровня

```text
MediaHub OS / MediaHub iOS
├── MH-01…MH-05  Исторические основания и базовые границы
├── MH-06…MH-12  Runtime services, policy, plugins, UI, AI, observability, security
├── MH-13…MH-19  Privacy, persistence, OS/appliance, lifecycle, devices, media, knowledge
├── MH-20…MH-23  Architecture audit, hybrid cloud, operational qualification, migration
├── MH-24         Visual interface/navigation + reconciliation
├── MH-25         Stage reconciliation / control inventory
├── Functional Baseline 1.0 — историческая provenance, сохраняется
├── Functional Baseline 2.0 — текущая каноническая функциональная точка отсчёта
├── Canonical Component Manifest 2.0 — выбор компонентов для development; не production qualification
└── Astra Gold — распределённый контур автономной инженерной разработки и квалификации
```

MH-24 и MH-25 подтверждены контрольными документами. Не считать их автоматически обычными пользовательскими чатами: документы описывают стадии согласования/контроля.

## 3. Реестр MH-01…MH-25

Статусы воспроизводят инвентаризацию из MH-25 checkpoint, а не новую оценку готовности.

| Домен | Предмет | Статус из MH-25 | Подтверждённые артефакты / замечания |
|---|---|---|---|
| MH-01 | Charter | PARTIALLY_CLOSED | Отдельный stage closure artifact не найден в checkpoint. Есть ветки `architecture/mh01-chat-qualification-20260930` и `architecture/mh01-chat-qualification-20260930-v2`; требуется сравнение файлов и commits. |
| MH-02 | Boundaries | RECONCILED | Есть ветки `architecture/mh02-boundaries-20260930`, `architecture/mh-02-reference`; dedicated provenance/closure artifact не найден в checkpoint. |
| MH-03 | Runtime Foundation | RECONCILED | `architecture/MH-03-master-prompt.md` и пакет acceptance/decision/contradiction/evidence/runtime/sync. Следить за согласованием State Authority. |
| MH-04 | Security | PARTIALLY_CLOSED | Ветка `architecture/mh-04-security-trust-authorization`; прямой closure/evidence package не подтверждён в checkpoint. |
| MH-05 | Consumer Integration / Smart Home | PARTIALLY_CLOSED | Ветка `architecture/mh-05-consumer-integration-boundary`; найден `docs/architecture/MH-5-consumer-integration-boundary.md` со статусом PROPOSED — GOVERNANCE REVIEW REQUIRED. Есть отдельная redistribution-reconciliation ветка. |
| MH-06 | Core Runtime Services | PARTIALLY_CLOSED | Полный архитектурный пакет и master/reverse prompts; общий этап не заморожен. |
| MH-07 | Configuration / Policy | PARTIALLY_CLOSED | Ветка `architecture/mh-7-configuration-policy`; найден `docs/architecture/MH-7-master-prompt.md`. Имена используют вариант MH-7, а не MH-07. |
| MH-08 | Plugins | PARTIALLY_CLOSED | Ветка `architecture/mh-8-plugin-extension`; dedicated closure provenance в MH-25 checkpoint не найден. |
| MH-09 | UI / Presentation | PARTIALLY_CLOSED | Ветка `architecture/mh-09-presentation-ui`; найдены `docs/architecture/MH-09-master-prompt.md` и `docs/architecture/MH-09-reverse-master-prompt.md`. Acceptance не предоставлен, production blocked. |
| MH-10 | AI | RECONCILED | Полный пакет архитектуры, master/reverse prompts, decisions, contradictions, evidence. Провайдеры/runtime требуют отдельной квалификации. |
| MH-11 | Observability | PARTIALLY_CLOSED | Ветка `architecture/mh-11-diagnostics-observability`; dedicated stage closure/evidence package не найден в MH-25 checkpoint. |
| MH-12 | Security Analysis | RECONCILED | Полный пакет, master/reverse prompts, threat model и security invariants. Production qualification отдельно. |
| MH-13 | Privacy / Data Governance | PARTIALLY_CLOSED | `docs/architecture/MH-13-master-prompt.md`, `docs/architecture/MH-13-reverse-master-prompt.md`; ветка `reconstruction/mh-13-privacy-data-governance`. Исторический оригинал не восстановлен; статус — принятая реконструкция, не frozen. |
| MH-14 | Persistence | PARTIALLY_CLOSED | Пакет архитектурных passes; физическая persistence implementation не авторизована. |
| MH-15 | OS / Appliance | PARTIALLY_CLOSED | Пакет master/reverse, acceptance/audit; acceptance/freeze и implementation qualification не подтверждены. |
| MH-16 | Installation / Recovery / Updates | PARTIALLY_CLOSED | `docs/architecture/MH-16-master-prompt.md` и completion record. Отдельный `MH-16-reverse-master-prompt.md` по проверенному пути отсутствует; master prompt может содержать объединённый интерфейс. Governance pending, implementation blocked. |
| MH-17 | Devices / Protocols | PARTIALLY_CLOSED | Ветка `arch/mh-17-device-protocol`; найдены `docs/architecture/MH-17-master-prompt.md` и `docs/architecture/MH-17-reverse-master-prompt.md`. Governance acceptance и production evidence открыты. |
| MH-18 | Media | PARTIALLY_CLOSED | Ветки `mh-18-media-content-architecture`, `mh-18-media-content-architecture-handoff`, `mh-18-media-content-architecture-handoff-v2`, `mh-18-media-content-architecture-sync`. Нужно сравнить версии; dedicated closure/provenance и полная qualification matrix не подтверждены. |
| MH-19 | Knowledge Graph / Digital Twin | PARTIALLY_CLOSED | Ветка `architecture/mh-19-knowledge-graph-digital-twin`; dedicated stage architecture/closure artifact не найден в MH-25 checkpoint. |
| MH-20 | Architecture Audit | PARTIALLY_CLOSED | Полный пакет; статус NOT YET ACCEPTED / NOT FROZEN. |
| MH-21 | Hybrid Cloud | RECONCILED | Полный пакет cloud/privacy/AI/egress/trust/workload placement. Production qualification и окончательный выбор реализации остаются открытыми. |
| MH-22 | Operational Qualification | RECONCILED | Есть интерфейс `docs/architecture/MH-22-master-prompt-interface.md`; qualification pass summary сообщает production qualification NO-GO. |
| MH-23 | Migration | PARTIALLY_CLOSED | Ветка `architecture/mh-23-long-term-evolution`; dedicated stage closure/evidence artifact не найден в MH-25 checkpoint. Название ветки и домена следует сверить по содержимому, не переименовывать автоматически. |
| MH-24 | Visual Interface / Navigation + reconciliation | PARTIALLY_CLOSED на старте MH-25 | Dedicated checkpoints/reports/matrix; связан с Functional Baseline 2.0. В отдельном отчёте MH-24 закрыт и baseline принят; сохранить обе даты/стадии и выяснить расхождение статусов по времени. |
| MH-25 | Stage reconciliation / control inventory | INVENTORY COMPLETE — RECONCILIATION IN PROGRESS (по checkpoint) | `docs/checkpoints/mediahub-mh25-stage-reconciliation.md`. Контрольный слой; не считать доказательством закрытия всех MH-1…MH-24. |

## 4. Основные контрольные документы

| Путь в репозитории | Роль |
|---|---|
| `docs/checkpoints/mediahub-mh25-stage-reconciliation.md` | Исторический реестр состояния MH-1…MH-24 на старте MH-25; фиксирует пробелы доказательств |
| `docs/checkpoints/mediahub-mh24-reconciliation-report.md` | Отчёт согласования MH-24 |
| `docs/checkpoints/mediahub-functional-baseline-2.0.md` | Каноническая функциональная точка отсчёта; supersedes Baseline 1.0 как текущий reference |
| `docs/checkpoints/mediahub-master-architecture-reconciliation.md` | История согласования мастер-архитектуры |
| `docs/checkpoints/mediahub-github-component-final-manifest-2.0.md` | Канонический компонентный манифест для разработки; выбор не означает production qualification |
| `docs/checkpoints/2026-10-02-astra-gold-hybrid-component-reconciliation.md` | Инвентаризация и согласование компонентов Astra Gold |
| `docs/MASTER_SYSTEM_GUIDE.md` в ветке `docs/master-system-guide-audit-20261012` | Обновлённый мастер-гайд v1.2; не считать автоматически присутствующим в локальном checkout или `main` |

## 5. Архитектурные инварианты, которые нельзя терять при сведении

- Runtime coordinates; State Authority mutates. Не создавать второй путь канонических мутаций.
- Product State Authority и A0-ASTRA — разные полномочия: первый владеет каноническим состоянием продукта, второй координирует инженерные работы/очередь. Старый blueprint, где A0-ASTRA обозначен как `state_authority`, требует governance reconciliation.
- Device adapters, AI/provider, workflow engine, tools и MCP не получают полномочий State Authority по факту подключения.
- MH-14 persistence, MH-16 lifecycle, MH-17 device protocol и MH-21 cloud остаются подчинены каноническому State Authority и policy.
- Статусы ARCHITECTURE / IMPLEMENTATION / VERIFICATION / QUALIFICATION / RELEASE / DEPLOYMENT / PRODUCTION ACCEPTANCE ведутся раздельно.
- Три claims/lanes в старом qualification contract не превращать в целевую concurrency норму без изоляционного и capacity обоснования.
- MH-03 proposed HA через PostgreSQL/etcd/NATS не продвигать в текущую single-node/in-memory foundation без отдельного governance gate.

## 6. Обнаруженные пробелы и конфликты

1. Для MH-01, MH-02, MH-04, MH-05, MH-07, MH-08, MH-11, MH-18, MH-19, MH-23 исторический checkpoint отмечает отсутствие dedicated stage-named closure artifacts, хотя поздние документы ссылаются на решения этих этапов.
2. Отсутствие отдельного reverse prompt не обязательно означает отсутствие процесса обратной передачи: MH-16 требует проверки объединённого документа.
3. MH-18 имеет несколько веток handoff/sync; каноническая версия пока не выбрана на основании сравнения commit ancestry и содержимого.
4. MH-23 имеет ветку `architecture/mh-23-long-term-evolution`, хотя checkpoint называет MH-23 Migration. Требуется сверить артефакты и историческое переименование.
5. MH-24 stage checkpoint фиксирует PARTIALLY_CLOSED на старте MH-25, а отдельный MH-24 reconciliation report фиксирует CLOSED / Baseline 2.0 ACCEPTED. Это временная последовательность, а не повод удалить один из статусов.
6. В локальном checkout master guide v1.2 отсутствовал; его наличие подтверждено в отдельной audit-ветке. Перед синхронизацией надо сравнить ветки и сохранить локальные изменения.
7. MH-25 checkpoint говорит, что в репозитории было 597 tree entries и что статус всех этапов нельзя вывести из существования чатов/файлов.

## 7. Безопасный протокол завершения карты

1. Для каждой специализированной ветки сохранить HEAD SHA и сравнить с `main`.
2. Получить список путей по каждому branch tree и сопоставить MH-specific artifacts, master/reverse prompts, decisions, contradictions, acceptance/evidence.
3. Сопоставить MH-18 handoff/sync branches и определить ancestry/содержательные различия.
4. Проверить MH-23 branch against Migration references in Baseline 2.0 and MH-25.
5. Верифицировать MH-01…MH-23 against Functional Baseline 2.0 traceability matrix.
6. Сформировать таблицу `domain → canonical path → branch/commit → master prompt → reverse handoff → dependencies → status → gaps`.
7. Только после read-only сверки обновлять эту карту новым commit в этой документационной ветке. Не делать merge в `main` автоматически.
8. При финальной синхронизации не удалять старые контрольные точки; фиксировать supersession и provenance.

## 8. Критерий полноты

Карта считается восстановленной только когда каждый MH-01…MH-25 имеет:
- подтверждённое назначение и связь с соседними доменами;
- канонический путь и версию/commit;
- статус с указанием источника доказательства;
- ссылку на master prompt и reverse handoff либо явную запись, что механизм не найден после поиска по путям и веткам;
- перечень противоречий, superseded decisions и открытых gates.

**Текущий статус:** базовая карта создана, но критерий полноты ещё не выполнен. Нельзя утверждать, что все чаты найдены или что все этапы закрыты.


## 9. Результаты следующего прохода: branch diff и историческая карта (2026-10-12)

### 9.1 Проверенный метод

Выполнено сравнение специализированных веток с `main` через GitHub compare API. Эти ветки в основном **diverged**, а не обычные актуальные feature branches: у некоторых сотни/тысячи commits behind `main`, а файлы показываются как добавленные относительно общей точки сравнения. Поэтому статус `added` в compare не означает, что документ отсутствует в текущем `main`; это означает, что документ находится в уникальной истории этой ветки относительно выбранной базы. Перед переносом обязательно проверить наличие и содержимое файла в `main`.

### 9.2 Важные уточнения по доменам

| Домен | Новое подтверждение | Следствие |
|---|---|---|
| MH-01 | Ветка `architecture/mh01-chat-qualification-20260930-v2` содержит `docs/architecture/MH-01-ARCHITECTURE-CHAT-CHARTER.md`, `docs/architecture/MH-01-chat-qualification-blueprint-2026-09-30.md`, qualification JSON. Другая ветка с похожим названием фактически содержит материалы MH-02, а не чистый MH-01 пакет. | Не объединять ветки по названию; canonical MH-01 package подтверждать по содержимому и SHA. |
| MH-01…MH-23 | `architecture/mh3-runtime-foundation-20260930` — крупная divergence: compare показал 1,044 commits ahead, 1,365 behind, до 300 изменённых файлов в ответе compare, включая широкую серию MH-01, MH-04/05 и инфраструктуру. | Это не просто ветка MH-03. Это крупный исторический срез/комбинированная ветка; нельзя автоматически cherry-pick/merge. |
| MH-02 | `architecture/mh-02-reference` содержит 17 профильных файлов под `architecture/mh-02/`, включая `MH-02-MH01-MH23-map.md`, dependency graph, decision/contradiction/evidence registers, traceability matrix. | Использовать как ценный источник исторической карты, но сверить с baseline 2.0 и текущим main. |
| MH-04 | `architecture/mh-04-security-trust-authorization` содержит 26 MH-04 документов, включая master/reverse prompts, acceptance, decision/contradiction/evidence, identity, authorization, credential, quarantine и trust boundary. | Предыдущая запись об отсутствии direct artifact слишком осторожна: пакет существует в ветке; статус stage closure остаётся отдельным вопросом. |
| MH-05 | `architecture/mh-05-consumer-integration-boundary` содержит 54 файла, включая acceptance criteria, consumer integration boundary, command model, decision/contradiction/evidence/dependency map, trust/privacy/security boundaries. | Есть полноценный архитектурный пакет в отдельной ветке; это не доказывает принятие или freeze. |
| MH-07 | `architecture/mh-7-configuration-policy` содержит 87 файлов, в том числе MH-07 acceptance, configuration/policy model, dependency/decision/evidence/contradiction registers и master prompt. | Искать с обоими вариантами нумерации MH-7 и MH-07. |
| MH-08 | Ветка `architecture/mh-8-plugin-extension` в compare с main дала 0 commits ahead и 1,638 behind, 0 файлов в diff. | Ветка указывает на предка/историю, полностью содержащуюся в сравнительном предке main; это не доказательство отсутствия MH-08 документов. Проверять main и историю, а не считать ветку источником уникальных файлов. |
| MH-09 | Ветка содержит 43 файла; подтверждены master prompt, reverse prompt, acceptance, decision/contradiction/evidence, UI domains. | Сохраняется оговорка: пакет документов не равен acceptance/freeze/production. |
| MH-11 | Ветка содержит 27 файлов; `MH-11-INDEX.md`, `MH-11-CHAT-MASTER-PROMPT.md`, `MH-11-REVERSE-MASTER-PROMPT.md` и architecture/evidence registers найдены. | Обновить предыдущую запись: dedicated prompt/index package существует в ветке; stage closure по MH-25 всё ещё PARTIALLY_CLOSED. |
| MH-13 | Ветка reconstruction при сравнении имеет 0 commits ahead и 1,385 behind, 0 diff files. | Ветка не показывает уникальных файлов относительно main в данном compare; это согласуется с наличием reconstruction artifacts на main, но не подтверждает исторический оригинал. |
| MH-17 | Ветка содержит 27 профильных файлов, включая protocol integration architecture, device identity/lifecycle/trust, command lifecycle, normalization, security, acceptance/evidence. | Архитектурный пакет есть; governance/production acceptance отдельно. |
| MH-18 | Четыре ветки `mh-18-media-content-architecture*` показали одинаковые основные параметры сравнения (65 commits ahead, 1,638 behind, 60 файлов); в них найдено `MH-18-chat-sync.md` и большой набор профильных документов. | По одному compare против main нельзя установить порядок версий: одинаковая статистика может означать идентичный снимок. Нужен прямой compare ветка-к-ветке и SHA HEAD. |
| MH-19 | Ветка содержит 57 профильных файлов, включая acceptance, identity/entity model, digital twin, consistency, evidence, decision/contradiction registers. | Пакет существует; closure и production evidence остаются отдельными воротами. |
| MH-23 | Ветка содержит 66 файлов, включая `MH-23-CHAT-MASTER-PROMPT.md`, `MH-23-REVERSE-MASTER-PROMPT.md`, compatibility/migration/decision/evidence/contradiction registers и `MEDIAHUB-MASTER-ARCHITECTURE-INDEX.md`. | MH-23 — это не только абстрактное «долгосрочное развитие»: конкретный пакет явно включает Evolution/Compatibility/Migration. Но необходимо сопоставить это с MH-25 nomenclature. |

### 9.3 Историческая карта MH-01…MH-23 из MH-02 reference

В `architecture/mh-02/MH-02-MH01-MH23-map.md` зафиксирована такая рабочая последовательность:

1. MH-01 — Product / Governance
2. MH-02 — Reference Architecture / System Boundaries
3. MH-03 — Runtime Foundation
4. MH-04 — State Authority
5. MH-05 — Consumer / Integration Boundary
6. MH-06 — Core Runtime Services
7. MH-07 — Configuration / Policy
8. MH-08 — Plugin / Extension
9. MH-09 — Presentation / UI
10. MH-10 — AI / Intelligence
11. MH-11 — Diagnostics / Observability
12. MH-12 — Security
13. MH-13 — Privacy / Data Governance
14. MH-14 — Persistence
15. MH-15 — OS / Appliance
16. MH-16 — Installer / Recovery / Update
17. MH-17 — Device / Protocol Integration
18. MH-18 — Media / Content
19. MH-19 — Knowledge Graph / Digital Twin
20. MH-20 — Automation / Energy / Self-Healing
21. MH-21 — Hybrid Cloud / Distributed AI
22. MH-22 — Production / Qualification / Operations
23. MH-23 — Evolution / Compatibility / Migration

**Ключевая коррекция:** предыдущая таблица карты называла MH-20 «Architecture Audit». Это не соответствует найденной исторической карте MH-01…MH-23. В MH-25 stage matrix и других checkpoints нужно выяснить, откуда взялось имя Architecture Audit и к какому этапу/артефакту оно относится. До выяснения обозначать MH-20 как **Automation / Energy / Self-Healing (historical map; verify against Baseline 2.0)**, а «Architecture Audit» — как отдельное название найденного пакета/стадии, не как подтверждённое каноническое имя MH-20.

В master architecture index на ветке MH-23 говорится, что MH-01…MH-22 exact repository linkage требует проверки там, где не подтверждена, и что серия MH-01…MH-23 — цель полного архитектурного ряда. Этот документ находится в отдельной ветке и не должен считаться автоматически каноническим на `main`.

### 9.4 Содержательные факты MH-18

Файл `docs/architecture/MH-18-media-content-architecture.md` в ветке `mh-18-media-content-architecture-handoff-v2` явно помечен `PROPOSED / NOT ACCEPTED / NOT FROZEN`. В нём определены:
- медиа как домен, а не State Authority;
- различение Content / Asset / Object-File / Storage Locator / External ID / Digest-Fingerprint / Version;
- ingestion pipeline, validation, provenance и policy;
- derived index/cache/transcodes как перестраиваемые данные;
- изоляция обработки недоверенных медиа;
- privacy/rights/DRM boundaries;
- разделение media lifecycle и device lifecycle;
- отсутствие авторизации production ingestion, bulk import/export/deletion, storage migration, codec installation, provider/DRM integration и camera/live capture без отдельных gates;
- FFmpeg/GStreamer/VLC и storage/search backends остаются кандидатами до ADR и доказательств.

В `MH-18-chat-sync.md` следующий архитектурный handoff указан как MH-19. Это подтверждает задуманную последовательность MH-18 → MH-19, но не доказывает, что все документы уже перенесены в main.

### 9.5 Канонические инварианты из исторических карт

- State Authority — единственная власть канонической мутации.
- Поток: Input → Boundary → Authorization → State Authority → Canonical State → Observation → Evidence.
- AI, cloud, plugins, devices, UI, persistence, policy engine, observability и knowledge graph не становятся authority.
- Архитектурный чат и development chat разделены: development возвращает Reverse Master Prompt/evidence; архитектурная истина обновляется только после governance review и синхронизации.
- Архитектурные пакеты могут быть PROPOSED / NOT ACCEPTED / NOT FROZEN, даже если имеют полный набор файлов.

### 9.6 Следующие проверки (read-only)

1. Сравнить четыре MH-18 ветки напрямую друг с другом, проверить SHA HEAD и уникальные изменения; не выбирать «v2» канонической только по имени.
2. Сравнить MH-01 v2, MH-02 branches и крупную MH-03 ветку на уровне commits и файлов, чтобы восстановить реальные связи/переиспользование истории.
3. Сверить MH-20 naming collision между `MH-25`, `MH-02-MH01-MH23-map.md`, Functional Baseline 2.0 и MH-23 master index.
4. Для MH-04, MH-05, MH-07, MH-09, MH-11, MH-17, MH-19, MH-23 подтвердить текущие пути на `main` отдельно от веток и проверить содержимое acceptance/evidence registers.
5. Только после этого обновить таблицу «canonical path → branch/commit → prompts → status». Никаких merge в main на этой стадии.
