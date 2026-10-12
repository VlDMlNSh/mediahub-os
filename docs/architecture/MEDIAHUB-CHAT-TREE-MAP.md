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
├── Functional Baseline 1.0 — актуальный паспорт редакции 1.0 по прямому указанию владельца; сохранён как отдельная версия
├── Functional Baseline 2.0 — отдельный документ со статусом ACCEPTED/CANONICAL/IMMUTABLE; семантическая сверка с 1.0 ещё открыта
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


### 9.7 Прямое сравнение веток — подтверждённые результаты

- Четыре MH-18 ветки (`mh-18-media-content-architecture`, `...-handoff`, `...-handoff-v2`, `...-sync`) сравниваются как **IDENTICAL**: 0 ahead / 0 behind / 0 файлов различий. Это означает, что их текущие refs указывают на одинаковое состояние по compare API; не требуется выбирать «v2» как более новую версию только по имени. В карте можно считать их aliases одного содержимого на момент проверки, сохранив все имена веток как исторические ссылки.
- Ветки `architecture/mh01-chat-qualification-20260930` и `architecture/mh01-chat-qualification-20260930-v2` **DIVERGED**: при сравнении первая имеет 11 уникальных commits, вторая 16 уникальных commits относительно первой. В v2 присутствуют MH-01 charter/blueprint и контрольные документы MH-24/MH-25/Baseline 2.0; однако среди diff также есть MH-02 документы в первой ветке. Следовательно, эти ветки нельзя трактовать как две линейные версии одного чистого MH-01 пакета; v2 включает более широкий контрольный срез.
- Эти выводы основаны на прямом сравнении refs через GitHub. Перед любым переносом всё равно проверить SHA и состояние target branch на момент изменения.


## 10. Следующий проход: Baseline 2.0 против MH-20/MH-23 (2026-10-12)

### 10.1 Проверка текущего main

Проверены точные пути в `main` и blob SHA:

- `docs/checkpoints/mediahub-functional-baseline-2.0.md` — найден, blob SHA `1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f`, статус в документе **ACCEPTED — CANONICAL IMMUTABLE REFERENCE POINT**.
- `docs/checkpoints/mediahub-mh24-traceability-matrix.md` — найден, blob SHA `8bdd364493ebbe2ef6f87400f80bc7eca8fb95c6`; матрица сама помечена **RECONCILIATION CANDIDATE**, поэтому не называть её отдельно принятой/замороженной без дополнительного подтверждения.
- `docs/architecture/MH-20-CHAT-MASTER-PROMPT.md` — найден, blob SHA `0f185752a288ef494d3217d501c4cb64a2cff46f`.
- `docs/architecture/MH-20-REVERSE-MASTER-PROMPT.md` — найден, blob SHA `04b3137a19b3f25f69fa5172965b4999948cb266`.
- `docs/architecture/MH-17-master-prompt.md` — найден, blob SHA `a750ee5b292043a1f1b18ec317a4b5b2c44aad24`.

Точные ожидаемые пути `docs/architecture/MH-20-master-prompt.md`, `MH-20-architecture-audit.md`, `MH-23-CHAT-MASTER-PROMPT.md`, `MH-23-REVERSE-MASTER-PROMPT.md`, `MEDIAHUB-MASTER-ARCHITECTURE-INDEX.md` и `MH-01-ARCHITECTURE-CHAT-CHARTER.md` в `main` не найдены. Это результат проверки точных путей, а не заявление об отсутствии соответствующих документов во всех ветках/истории.

### 10.2 Каноническое назначение MH-20 — важная коррекция

Текущий `MH-20-CHAT-MASTER-PROMPT.md` описывает MH-20 как **automation governance**: Automation / Energy / Self-Healing, evidence, canonical state, decisions, contracts, invariants, traceability, verification, acceptance/freeze. Он прямо фиксирует:
- Automation is orchestration, not authority.
- Любая мутация следует цепочке Policy → Authorization → Consumer Boundary → State Authority.
- Scheduler, Rule Engine, Energy Engine, Self-Healing Engine и AI не являются authority.
- Рабочий цикл: Evidence → Canonical State → Decision → Architecture → Implementation → Verification → Governance Acceptance → Freeze.

Это согласуется с исторической картой MH-01…MH-23, где MH-20 — Automation / Energy / Self-Healing. Поэтому предыдущую формулировку «MH-20 = Architecture Audit» нужно считать **неподтверждённой/конфликтующей меткой**, а не каноническим назначением. Не переименовывать файлы автоматически; в индексе использовать назначение Automation / Energy / Self-Healing, а «Architecture Audit» оставить как неразрешённый алиас/ошибочную метку до выяснения её происхождения.

Матрица Baseline 2.0 дополнительно ссылает на MH-20 для State Authority (в связке MH-3/MH-14/MH-20), OSS foundation/adoption, architectural prohibitions, Git/provenance и autonomous development. Это означает, что MH-20 — не только runtime automation design: его governance scope распространяется на безопасное принятие OSS, архитектурные запреты и доказуемость разработки.

### 10.3 MH-23: подтверждённая роль и пробел канонического пути

Ветка `architecture/mh-23-long-term-evolution` содержит отдельные `MH-23-CHAT-MASTER-PROMPT.md` и `MH-23-REVERSE-MASTER-PROMPT.md`, плюс compatibility/migration/decision/evidence/contradiction registers и master architecture index. Однако эти точные prompt paths не найдены на `main` в `docs/architecture/`.

Текущий Functional Baseline 2.0 относит Migration к отдельному control plane, не к authority, и требует сохранять State Authority identity, contracts, provenance, security и data integrity при migration. Traceability matrix использует MH-23 вместе с MH-16 для backup/recovery и MH-21 для cloud/developer fabric, а также связывает MH-20/MH-23 с OSS foundation, Git/provenance, autonomous development, release lock и development chain.

**Рабочее назначение MH-23:** Evolution / Compatibility / Migration (историческая архитектурная ветка); миграция должна сохранять идентичность канонического состояния, provenance и security. **Канонический путь prompts в main пока не подтверждён.** Не копировать их из ветки в main автоматически.

### 10.4 Что эта проверка изменила в понимании дерева

- Functional Baseline 2.0 — текущая каноническая функциональная точка отсчёта; исторические MH-1…MH-23 — provenance, а не автоматически действующие отдельные frozen specifications.
- Traceability matrix — полезная карта соответствия 68 разделов, но в заголовке имеет статус reconciliation candidate. Её содержимое нельзя путать с доказательством квалификации.
- MH-20 в текущем main имеет точные master/reverse prompts; домен — governance автоматизации/OSS/provenance, не «Architecture Audit».
- MH-23 имеет подробный пакет в специализированной ветке, но его точные prompts/index не подтверждены на main.
- Несколько точных путей из отдельных веток отсутствуют на main. До любого переноса следует проверить полный путь, blob SHA, ancestry и возможный эквивалент с другим именем.

### 10.5 Следующий проход

1. Извлечь из `MH-02-MH01-MH23-map.md` полный граф зависимостей и сопоставить его с 68 строками traceability matrix.
2. Для каждого MH-домена установить текущий `main` path и SHA либо отметить `BRANCH-ONLY` с точной веткой/commit.
3. Сопоставить список «master prompt / reverse prompt / decision / evidence / acceptance / freeze» и отметить реальные пробелы.
4. Отдельно разобрать происхождение метки «Architecture Audit» и проверить, не относится ли она к MH-25/MH-24 reconciliation или иному audit package.
5. В итоговой карте указать дату проверки refs, чтобы будущая сессия начиналась с проверенного снимка, а не с повторения старых предположений.


## 11. Проверка точных путей в main — реестр prompt-файлов (2026-10-12)

### 11.1 Подтверждённые файлы в main

Ниже указаны точные пути и blob SHA, полученные прямым чтением GitHub `main`. SHA фиксирует проверенную версию файла, а не квалификационный статус домена.

| Домен | Файл в main | Blob SHA | Примечание |
|---|---|---|---|
| MH-03 | `architecture/MH-03-master-prompt.md` | `e99035f596e236645bf8f2235fc4d375716ce476` | Файл находится вне `docs/architecture/`; поиск только в docs давал бы ложное отсутствие. |
| MH-06 | `docs/architecture/MH-06-CHAT-MASTER-PROMPT.md` | `6940d601e968b196d8c46366bfd83ee0bdef79e4` | Найден также `docs/architecture/MH-06-REVERSE-MASTER-PROMPT.md`, SHA `5d7a9e4eb2d9d92177eb7fa71b770aee352c185d`. |
| MH-10 | `docs/architecture/MH-10-CHAT-MASTER-PROMPT.md` | `6ea847ddbf1604878303572b21b506102b23c930` | Master prompt найден. Наличие отдельного reverse prompt этой проверкой не установлено. |
| MH-12 | `docs/architecture/MH-12-CHAT-MASTER-PROMPT.md` | `dea79d709fea274cc5fd08cca4f0d6aec2ad6d93` | Master prompt найден. |
| MH-13 | `docs/architecture/MH-13-master-prompt.md` | `de00bea7f972fca30295c0855b0d324f845c0bc4` | Найден reverse prompt `docs/architecture/MH-13-reverse-master-prompt.md`, SHA `d590b6541870d3f77fbb1e48159b78d5d2f1f203`. |
| MH-15 | `docs/architecture/MH-15-CHAT-MASTER-PROMPT.md` | `2ee7dde1b625305c2b04f2c8e5269bd8aff459cd` | Master prompt найден. |
| MH-16 | `docs/architecture/MH-16-master-prompt.md` | `62924d4686aa3f55fce442a3c4bab66c82ae19e5` | Сам заголовок указывает на combined Master Prompt / Reverse Master Prompt; отдельный reverse-файл не требуется считать обязательным без проверки содержимого/контракта. |
| MH-17 | `docs/architecture/MH-17-master-prompt.md` | `a750ee5b292043a1f1b18ec317a4b5b2c44aad24` | Найден reverse prompt `docs/architecture/MH-17-reverse-master-prompt.md`, SHA `13cb56ec5a96aa7d420aa7755cf420e5cc8fe2c2`. |
| MH-20 | `docs/architecture/MH-20-CHAT-MASTER-PROMPT.md` | `0f185752a288ef494d3217d501c4cb64a2cff46f` | Найден reverse prompt `docs/architecture/MH-20-REVERSE-MASTER-PROMPT.md`, SHA `04b3137a19b3f25f69fa5172965b4999948cb266`. |
| MH-21 | `docs/architecture/MH-21-CHAT-MASTER-PROMPT.md` | `61d552db4d1a1abefa2cef9f44eebcf634d11111` | Master prompt найден. |
| MH-22 | `docs/architecture/MH-22-master-prompt-interface.md` | `9278e49d453bf1a6a68d40f99b842fcf52ad216d` | Единый интерфейс Master Prompt / Reverse Master Prompt. |

### 11.2 Контрольные документы в main

| Путь | Blob SHA | Статус/роль |
|---|---|---|
| `docs/checkpoints/mediahub-mh25-stage-reconciliation.md` | `6efbd86287357698370c17df909ea7303d616264` | Исторический inventory MH-01…MH-24; не заменяет проверку актуального состояния доменов. |
| `docs/checkpoints/mediahub-mh24-reconciliation-report.md` | `d07d162ebaa57643a7bdd84d6fb13a1102b87bfc` | Отчёт MH-24. |
| `docs/checkpoints/mediahub-functional-baseline-2.0.md` | `1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f` | Канонический Functional Baseline 2.0. |
| `docs/checkpoints/mediahub-master-architecture-reconciliation.md` | `f3a66e292302984be95ae8085f17e03cd538baae` | Историческая сверка мастер-архитектуры. |

### 11.3 Проверенные пути, не найденные в main

Следующие **точные пути** дали NOT_FOUND в `main`; это не означает, что домен или документ отсутствует во всём репозитории.

- MH-01: `docs/architecture/MH-01-ARCHITECTURE-CHAT-CHARTER.md`, `docs/architecture/MH-01-chat-qualification-blueprint-2026-09-30.md` — ранее найдены в специализированной ветке MH-01 v2, но не по этим путям в main.
- MH-02: `architecture/mh-02/MH-02-MH01-MH23-map.md` — найден в `architecture/mh-02-reference`, не найден по тому же пути в main.
- MH-04: проверенные пути `docs/architecture/MH-04-master-prompt.md`, `MH-04-CHAT-MASTER-PROMPT.md`, `MH-04-REVERSE-MASTER-PROMPT.md` не найдены. Полный MH-04 пакет ранее найден в `architecture/mh-04-security-trust-authorization`; точные пути следует извлекать из tree/diff этой ветки, а не предполагать.
- MH-05: `docs/architecture/MH-05-consumer-integration-boundary.md` и `MH-05-CHAT-MASTER-PROMPT.md` не найдены по этим путям в main. Документ consumer integration boundary найден в специализированной ветке.
- MH-07: `docs/architecture/MH-07-master-prompt.md` не найден; подтверждён вариант `docs/architecture/MH-7-master-prompt.md` в ветке MH-07.
- MH-08: `docs/architecture/MH-08-CHAT-MASTER-PROMPT.md` не найден по точному пути; требуется искать альтернативное написание MH-8 и другие каталоги.
- MH-09: варианты `docs/architecture/MH-09-master-prompt.md` и `MH-09-reverse-master-prompt.md` не найдены по этим путям в main; оба файла найдены в ветке `architecture/mh-09-presentation-ui`.
- MH-11: `docs/architecture/MH-11-INDEX.md`, `MH-11-CHAT-MASTER-PROMPT.md`, `MH-11-REVERSE-MASTER-PROMPT.md` не найдены по этим путям в main; они найдены в ветке `architecture/mh-11-diagnostics-observability`.
- MH-14: `docs/architecture/MH-14-CHAT-MASTER-PROMPT.md` не найден по точному пути.
- MH-18: `docs/architecture/MH-18-media-content-architecture.md` не найдено в main; найдено в MH-18 специализированной ветке и помечено PROPOSED / NOT ACCEPTED / NOT FROZEN.
- MH-19: `docs/architecture/MH-19-CHAT-MASTER-PROMPT.md` не найдено по точному пути в main; пакет найден в специализированной ветке MH-19.
- MH-23: `docs/architecture/MH-23-CHAT-MASTER-PROMPT.md` и `MH-23-REVERSE-MASTER-PROMPT.md` не найдены по точным путям в main; найдены в `architecture/mh-23-long-term-evolution`.

Для MH-02/MH-04/MH-05/MH-07/MH-08/MH-09/MH-11/MH-14/MH-18/MH-19/MH-23 необходим следующий шаг: получить полный список путей конкретной ветки, затем сравнить blob SHA и историю с main. Нельзя автоматически копировать документы только потому, что ожидаемый путь отсутствует.

### 11.4 Статус реестра

Это первый реестр с проверенными main paths и blob SHA, а не завершённая canonicalization. Master prompt existence, branch-only package, governance acceptance, freeze, implementation, tests and production qualification остаются разными фактами. На момент этой проверки main не изменялся.


## 12. Branch-only канонические пути: уточнение по compare API (2026-10-12)

Эта секция фиксирует **пути файлов, реально возвращённые GitHub Compare** для конкретной ветки. Это сильнее предположения по имени, но ещё не эквивалентно проверке каждого файла и его статуса. Compare показывает разницу относительно merge-base/выбранной базы; он не доказывает, что файл отсутствует в `main` под другим путём.

| Домен | Ветка | Подтверждённые точные пути из compare | Статус |
|---|---|---|---|
| MH-02 | `architecture/mh-02-reference` | `architecture/mh-02/MH-02-MH01-MH23-map.md`; `architecture/mh-02/MH-02-acceptance-criteria.md`; `architecture/mh-02/MH-02-evidence-register.md`; `architecture/mh-02/MH-02-traceability-matrix.md` | Branch-only candidate; 17 файлов в diff |
| MH-04 | `architecture/mh-04-security-trust-authorization` | `docs/architecture/mh-04/MH-04-master-prompt.md`; `docs/architecture/mh-04/MH-04-reverse-master-prompt.md`; `docs/architecture/mh-04/MH-04-acceptance-criteria.md`; `docs/architecture/mh-04/MH-04-evidence-register.md` | Branch-only candidate; 26 файлов в diff |
| MH-05 | `architecture/mh-05-consumer-integration-boundary` | `docs/architecture/MH-05-acceptance-criteria.md`; `docs/architecture/MH-05-dependency-map.md`; `docs/architecture/MH-05-evidence-register.md` | 54 файла в diff; основной boundary doc найден ранее в этой ветке |
| MH-07 | `architecture/mh-7-configuration-policy` | `docs/architecture/MH-07-master-prompt.md`; `docs/architecture/MH-07-reverse-master-prompt.md`; `docs/architecture/MH-07-acceptance-criteria.md`; `docs/architecture/MH-07-dependency-map.md`; `docs/architecture/MH-07-evidence-register.md` | 87 файлов в diff; учитывать разные варианты имени MH-7/MH-07 |
| MH-09 | `architecture/mh-09-presentation-ui` | `docs/architecture/MH-09-master-prompt.md`; `docs/architecture/MH-09-reverse-master-prompt.md`; `docs/architecture/MH-09-acceptance-criteria.md`; `docs/architecture/MH-09-dependency-map.md`; `docs/architecture/MH-09-evidence-register.md` | 43 файла в diff |
| MH-11 | `architecture/mh-11-diagnostics-observability` | `docs/architecture/MH-11-CHAT-MASTER-PROMPT.md`; `docs/architecture/MH-11-INDEX.md`; `docs/architecture/MH-11-REVERSE-MASTER-PROMPT.md`; `docs/architecture/MH-11-acceptance-criteria.md`; `docs/architecture/MH-11-evidence-register.md` | 27 файлов в diff |
| MH-18 | `mh-18-media-content-architecture-handoff-v2` | `docs/architecture/MH-18-acceptance-criteria.md`; `docs/architecture/MH-18-dependency-map.md`; `docs/architecture/MH-18-evidence-register.md`; `docs/architecture/MH-18-indexing.md`; `docs/architecture/MH-18-migration.md` | 60 файлов в diff; основные MH-18 ветки идентичны между собой |
| MH-19 | `architecture/mh-19-knowledge-graph-digital-twin` | `docs/architecture/mh-19/MH-19-master-prompt.md`; `docs/architecture/mh-19/MH-19-reverse-master-prompt.md`; `docs/architecture/mh-19/MH-19-acceptance-criteria.md`; `docs/architecture/mh-19/MH-19-dependency-map.md`; `docs/architecture/mh-19/MH-19-evidence-register.md` | 57 файлов в diff |
| MH-23 | `architecture/mh-23-long-term-evolution` | `docs/architecture/MH-23-CHAT-MASTER-PROMPT.md`; `docs/architecture/MH-23-REVERSE-MASTER-PROMPT.md`; `docs/architecture/MH-23-acceptance-criteria.md`; `docs/architecture/MH-23-evidence-register.md`; `docs/architecture/MH-23-final-architecture-index.md`; `docs/architecture/MEDIAHUB-MASTER-ARCHITECTURE-INDEX.md` | 66 файлов в diff |
| MH-01…MH-23 / control-plane | `architecture/mh3-runtime-foundation-20260930` | Compare вернул материалы `architecture/MH-01-*`, `architecture/MH-04-state-authority-*`, `architecture/MH-05-consumer-boundary-*`, `docs/ops/MH-3-*-closure-*` и многие autonomous-evidence artifacts | 1,044 commits ahead / 1,365 behind; compare response ограничен 300 файлами. Это широкий исторический срез, не чистая ветка MH-03; merge/cherry-pick запрещён до отдельного forensic review. |
| MH-01 | `architecture/mh01-chat-qualification-20260930-v2` | Compare с `main` показывает 3 уникальных commits и 3 файла, но не вернул их имена в фильтрованной выборке | Требуется прямое чтение tree/commit paths; не делать вывод об отсутствии charter. |
| MH-01/MH-02 | `architecture/mh01-chat-qualification-20260930` | `architecture/MH-02-boundary-architecture-v1.0.md`; `architecture/MH-02-boundary-interface-contract.md`; `architecture/MH-02-contradiction-register.md` | 11 commits ahead; ветка с MH-01 в имени включает MH-02 artifacts. |
| MH-17 | `arch/mh-17-device-protocol` | Compare вернул `docs/architecture/MH-17-acceptance-criteria.md`, `docs/architecture/MH-17-evidence-register.md`; ранее найдено 27 профильных файлов | Сверить полные пути мастер-промптов в ветке и их соответствие main. |
| Redistribution / handoff | `architecture/mh-05-redistribution-reconciliation` | `recovery/MASTER-PROMPT-NEW-CHAT-MH01-23-REDISTRIBUTION-FINAL-2026-09-05.md`; `recovery/MH01-23-REDISTRIBUTION-ARCHITECTURE-CHAT-HANDOFF-MASTER-PROMPT-2026-09-05.md`; `recovery/architecture-traceability.yaml`; `recovery/master-prompt-mh01-23-redistribution-2026-09-05.md` | 73 файла в diff; это handoff/recovery provenance, не автоматически каноническая архитектура |
| MH-08 | `architecture/mh-8-plugin-extension` | Compare: 0 ahead, 1,638 behind, 0 файлов diff | Ref полностью позади main относительно сравнения; проверять документы в main/истории, не считать ветку активным source of truth |
| MH-13 | `reconstruction/mh-13-privacy-data-governance` | Compare: 0 ahead, 1,385 behind, 0 файлов diff | Реконструкция не добавляет уникального diff относительно выбранного base; это не доказывает историческую подлинность оригинала |

### 12.1 Что это говорит о синхронизации

1. Специализированные ветки MH-04/MH-05/MH-07/MH-09/MH-11/MH-17/MH-18/MH-19/MH-23 содержат документы, которые нельзя потерять при проектировании итогового дерева.
2. Их ветки значительно отстают от `main` и расходятся с ним; это **не безопасные кандидаты на прямой merge**. Нужен выборочный документный reconciliation с сохранением provenance, а не merge всей ветки.
3. Крупная ветка `architecture/mh3-runtime-foundation-20260930` содержит множество cross-domain artifacts и 1,044 уникальных commits в compare. Её необходимо рассматривать как архивный/комбинированный срез, пока не доказано иное.
4. Следующий технический шаг — зафиксировать HEAD SHA веток и для каждого branch-only файла выполнить read-only fetch, получить blob SHA, сравнить семантику и определить target path в canonical map.
5. В `main` не выполнялись записи. Ветка карты обновляется отдельно; этот документ не выполняет merge архитектурных пакетов и не объявляет их принятыми.


## 13. Проверка содержимого acceptance/evidence: статусы не равны наличию файлов (2026-10-12)

Выполнено прямое чтение acceptance criteria и evidence registers в профильных ветках. Проверены SHA файлов и явные статусные формулировки. Результат показывает, что наличие пары Master/Reverse Master Prompt не означает архитектурное принятие.

| Домен | Acceptance/evidence artifact | Зафиксированный статус в файле | Вывод |
|---|---|---|---|
| MH-04 | `docs/architecture/mh-04/MH-04-acceptance-criteria.md` — blob `a75f5c1849ad67cc380a0ba3552bf7f2c5ec82b6` | `PROPOSED / REVIEW COMPLETE` | Не ACCEPTED и не FROZEN; файл явно требует отдельного governance approval и отдельного freeze decision. |
| MH-04 | `docs/architecture/mh-04/MH-04-evidence-register.md` — blob `dcf91d19cc494155e3c006a95f1ba35665d90e94` | Регистр содержит унаследованные P0-03…P0-06 как ACCEPTED/FROZEN | Статус унаследованных P0-контрактов не переносится автоматически на весь MH-04. |
| MH-05 | `docs/architecture/MH-05-acceptance-criteria.md` — blob `db18ab4416516240af394a6a9f57831f95edb802` | `NOT ACCEPTED — REQUIRES VERIFICATION` | Требуются доказательства, включая проверку единственности authority path. |
| MH-05 | `docs/architecture/MH-05-dependency-map.md` — blob `7ad2d3fe528a88326401eb1310cc08ab75d5b842`; `MH-05-evidence-register.md` — blob `0f8a3a3d8d16d1953ffa452484061a42a2312132` | `PROPOSED — GOVERNANCE REVIEW REQUIRED` | Схема зависимостей и evidence register остаются предложенными артефактами. |
| MH-07 | `docs/architecture/MH-07-acceptance-criteria.md` — blob `1f3160b9d07ac6e74c1b70be0bbf7eb1cd9bcf53` | `CANDIDATE / NOT ACCEPTED` | Нельзя считать MH-07 принятым или замороженным. Сам Reverse Prompt запрещает обход P0-03…P0-06. |
| MH-09 | `docs/architecture/MH-09-acceptance-criteria.md` — blob `09dd9a3bab69ea039152a3aeaaac830b8961ab8b` | `NOT ACCEPTED` | Проверка должна подтвердить, что UI — потребитель, не authority, и что persistence не переносится в MH-09. |
| MH-11 | `docs/architecture/MH-11-acceptance-criteria.md` — blob `342989e3954aee5eefd3ffdd707c9dde0aa403e6` | `PROPOSED — NOT ACCEPTED / NOT FROZEN` | Наблюдаемость и telemetry не могут считаться State Authority; тесты не дают автоматического статуса ACCEPTED/FROZEN/QUALIFIED. |
| MH-18 | `docs/architecture/MH-18-acceptance-criteria.md` — blob `1ce114d92ce401609d536138982a4c89408064dc` | `NOT ACCEPTED / NOT FROZEN` | Media/content architecture и её indexing остаются предложенными. Индекс определён как производный, перестраиваемый и неавторитетный. |
| MH-18 | `docs/architecture/MH-18-dependency-map.md` — blob `4be9091f6e4eb7db37069e6f55ab07790e4df233`; `MH-18-evidence-register.md` — blob `931e2fe80f2675469e4701f4e59ae483de850dd6` | `PROPOSED / NOT ACCEPTED`; `PROPOSED / AUDIT BASELINE` | Нельзя переводить в accepted по факту наличия документов. |
| MH-19 | `docs/architecture/mh-19/MH-19-acceptance-criteria.md` — blob `9bc038123f01beb9c66e71d5f27cbc82ad3e4501` | `NOT ACCEPTED / NOT FROZEN` | Knowledge Graph/Digital Twin — семантический/проекционный слой, не State Authority и не Policy Engine. |
| MH-19 | `docs/architecture/mh-19/MH-19-evidence-register.md` — blob `854fe2c0fc604d80b4e1af7d384ec1fb943fe6df` | `OBSERVED / PROPOSED REGISTER` | Наличие VERIFIED отдельных оснований не означает принятие домена целиком. |
| MH-23 | `docs/architecture/MH-23-acceptance-criteria.md` — blob `9ae5ba64882a3f98e5df0a9a907da0c0ced5d5a1` | `NOT ACCEPTED / NOT FROZEN` | Совместимость, миграции, rollback и coexistence требуют доказательств и governance acceptance. |
| MH-23 | `docs/architecture/MH-23-evidence-register.md` — blob `a9330b0373c4b329990d056553c0d7ac556d3bfc` | P0-07 / PR-кандидаты частично VERIFIED; точный P0-03 frozen artifact на main требует проверки | VERIFIED PR/кандидат не означает merged, accepted или canonical. |

### 13.1 Практические архитектурные выводы

1. **Не назначать канонический статус по названию файла, ветке или наличию reverse prompt.** Статус подтверждается отдельным governance record и evidence.
2. В MH-04/MH-05/MH-07/MH-09/MH-11/MH-18/MH-19/MH-23 есть прямые текстовые признаки незавершённой приёмки. До разрешения статуса они остаются кандидатами/предложениями, а не frozen архитектурой.
3. P0-03…P0-06 следует рассматривать как наследуемые ограничения там, где это указано в документах. MH-домен не может отменить или обходить их локальным решением.
4. Следующий шаг — сверить каждый заявленный ACCEPTED/FROZEN статус с независимым governance commit/ADR и конкретным canonical artifact на `main`, а не только с branch-local register.
5. Никакие установки, тесты на реальном оборудовании, квалификация Astra Gold или изменения `main` в этом проходе не выполнялись.


## 14. Паспорт системы: найденный первичный источник и актуальная иерархия истины (2026-10-12)

Запрос о первом паспорте проверен через полный recursive Git tree `main` (798 entries) и сравнение деревьев известных архитектурных веток. В текущем `main` нет отдельного файла с буквальным именем `passport.md` / `паспорт системы`; найдены исходный функциональный паспорт Baseline 1.0, checkpoint его согласования, принятая редакция Baseline 2.0 и отдельное расширение сетевого паспорта. Поэтому первичный паспорт нельзя отождествлять только с одноимённым checkpoint-файлом.

### 14.1 Главный первичный паспорт — Functional Baseline 1.0

- **Путь:** `specification/MEDIAHUB-FUNCTIONAL-BASELINE-1.0.md`
- **Blob SHA:** `1a2f06f50dd69990be58b12a98376b92f12fd14f`
- **Заголовок:** `MEDIAHUB OS 11.x LTS / MEDIAHUB iOS — FUNCTIONAL BASELINE 1.0 — NORMATIVE SINGLE SOURCE OF TRUTH`
- **Самоопределение документа:** «единственный эталонный функциональный паспорт платформы».
- **Политика изменений:** Baseline 1.0 immutable; изменения допускаются только через новую версию и governance-проход.
- **Назначение:** фиксирует функциональный смысл продукта; нижележащие capability, contract, architecture, planning, implementation, test и operational документы не могут молча расширять или менять этот смысл.

**Решение для карты:** считать Baseline 1.0 первичным историческим функциональным паспортом MediaHub и сохранять его как неизменяемую provenance-запись. Не редактировать его задним числом и не использовать как единственную текущую функциональную редакцию после принятия Baseline 2.0.

### 14.2 Текущий функциональный источник истины — Functional Baseline 2.0

- **Путь:** `docs/checkpoints/mediahub-functional-baseline-2.0.md`
- **Blob SHA:** `1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f`
- **Версия:** `2.0.0`
- **Заявленный статус:** `ACCEPTED — CANONICAL IMMUTABLE REFERENCE POINT`
- **Архитектурная ревизия:** MH-24 / 2026-10-01.
- **Связь с Baseline 1.0:** явно supersedes Baseline 1.0 как текущую функциональную ссылку, при этом сохраняет 1.0 как immutable historical provenance.
- **Область:** MediaHub OS 11.x LTS / MediaHub iOS и связанная инфраструктура разработки.

Baseline 2.0 заявляет, что согласован с пользовательским функциональным паспортом из 68 разделов, решениями MH-01…MH-23, контрольными документами и текущим состоянием GitHub. Его принятие **не** означает, что реализация, верификация, квалификация или production уже завершены.

**Иерархия для функциональных вопросов:** Baseline 2.0 — текущий принятый функциональный источник; Baseline 1.0 — первичный неизменяемый исторический паспорт. При конфликте текущих архитектурных/implementation документов с Baseline 2.0 конфликт направляется на reconciliation; baseline не меняется молча.

### 14.3 Checkpoint согласования — важная provenance-запись, но не сам паспорт

- **Путь:** `docs/checkpoints/mediahub-master-architecture-reconciliation.md`
- **Blob SHA:** `f3a66e292302984be95ae8085f17e03cd538baae`
- **Дата в документе:** 2026-09-30.
- **Текущий заголовочный статус:** `active master checkpoint / MH-24 reconciliation candidate`.
- **Passport field:** `MEDIAHUB OS 11.x LTS / MEDIAHUB iOS — FUNCTIONAL BASELINE 1.0`.

Этот документ хранит процесс согласования, продуктовые уточнения, происхождение и открытые решения. Он содержит исторический снимок состояния, поэтому его старые отметки о незапущенных/незавершённых разделах нельзя трактовать как текущий статус после Baseline 2.0. Это контрольный checkpoint и provenance, а не замена самому первичному паспорту.

В истории GitHub найдено создание checkpoint коммитом `3eb51f7935d2baf63b09dc6b2e9b82cbb9ea89ed` с сообщением `docs: establish MediaHub passport reconciliation master checkpoint`; последующее уточнение Section 1 записано коммитом `e37ebfde0687027f4307eb14358a39e6efd1da78`. У checkpoint заявлен исторический R4 SHA `471f709f5633feab7aeb62dd3ea52effad6d2bc584`, но сам документ фиксирует, что GitHub API не смог разрешить этот SHA на момент проверки. Сохранять как историческое утверждение, не выдавать за независимо подтверждённый commit.

### 14.4 Сетевое расширение паспорта

- **Путь:** `docs/checkpoints/2026-09-30-mediahub-network-system-passport-extension.md`
- **Blob SHA:** `43877c776889c58ae25a18d3ad60d2bb3a028578`
- **Заголовок:** `MediaHub Network Infrastructure — System Passport Extension v1`
- **Статус в файле:** нормативное описание требований сетевой инфраструктуры; реализация архитектуры — последующий этап.

Это дочернее тематическое расширение пользовательских требований: Ethernet/RJ45 как обычный upstream/backhaul, единая Wi-Fi-среда, участие узлов MediaHub в сетевой инфраструктуре и совместимость с подходящими точками доступа. Оно дополняет паспорт в области сети, но не заменяет общий функциональный baseline.

В истории GitHub оно внесено коммитом `b2eafbe42e16ae877487572b5006272679fdc93f` (`docs: record MediaHub network system passport extension`).

### 14.5 Поиск первичного паспорта: границы вывода

- Recursive tree `main` на момент проверки содержал 798 записей; из passport-related файлов обнаружены Functional Baseline 1.0, Baseline 2.0, reconciliation checkpoint и сетевое расширение.
- В проверенных деревьях `docs/master-system-guide-audit-20261012` и `architecture/mh01-chat-qualification-20260930-v2` обнаружены те же основные passport/baseline paths; отдельный более ранний файл с буквальным названием «паспорт системы» не обнаружен.
- Это не доказывает, что пользовательский исходник из чата когда-либо имел отдельный файл с таким именем или что его нет в других репозиториях/экспортах. Для восстановления самого исходного 68-раздельного документа следует отдельно проверить его provenance и возможные архивы/вложения. Baseline 2.0 уже заявляет, что согласован с этим 68-раздельным пользовательским паспортом.
- `docs/checkpoints/2026-09-30-mediahub-network-system-passport-extension.md` — именно расширение сети, не общий первичный паспорт.

### 14.6 Правило истины для последующих аудитов

1. Functional Baseline 2.0 — текущий принятый функциональный источник.
2. Functional Baseline 1.0 — первичный исторический immutable паспорт.
3. Master Architecture Reconciliation — история решений, сверки и provenance; учитывать его временные отметки как исторические.
4. Domain MH-01…MH-23 artifacts — детализация/контракты/доказательства в пределах baseline и governance.
5. Implementation, tests, logs, PRs и qualification evidence — доказательства соответствующего этапа; сами по себе не переписывают функциональный паспорт.
6. При конфликте сохранять исходные документы, фиксировать contradiction, определять владельца и принимать изменение только через версионирование и governance.

Эта иерархия добавлена в карту; никакие исходные baseline/checkpoint документы не изменялись, `main` не менялся.


## 15. Новая сверка паспорта по предоставленному пользователем полному тексту (2026-10-12)

Пользователь предоставил в текущей сессии полный документ «MEDIAHUB OS 11.x LTS / MEDIAHUB iOS — ПОЛНЫЙ ПАСПОРТ СИСТЕМЫ — FUNCTIONAL BASELINE 1.0» с разделами 1–68 и финальным статусом. Этот текст является отдельным первичным свидетельством требований и должен быть сохранён без потери содержания. Его нельзя автоматически считать побайтно идентичным одноимённому файлу в GitHub.

### 15.1 Фактическое состояние файла в GitHub

- Путь: `specification/MEDIAHUB-FUNCTIONAL-BASELINE-1.0.md`
- Ветка проверки: `main`
- Blob SHA: `1a2f06f50dd69990be58b12a98376b92f12fd14f`
- Размер: 14,527 символов на момент чтения.
- Создающий коммит: `17b4b47dcc03d7c61f33cb7636a35d9ad0bcde35`
- Сообщение коммита: `docs: establish MediaHub Functional Baseline 1.0`
- Дата коммита: 2026-09-08 19:40 UTC.
- Файл имеет верхнеуровневые разделы 0–22 (включая вложенные 11.1–11.3), а не структуру 1–68 из предоставленного пользователем текста.
- Проверка искала заявленные в пользовательском тексте R4 SHA `471f709f5633feab7aeb62dd3ea52effad6d2bc584` и подтвердила, что эта строка отсутствует в текущем содержимом GitHub-файла. Tree SHA `2279612908135418b2b5448d598274ea6741deaa` в файле присутствует.

**Вывод:** GitHub-файл Baseline 1.0 и предоставленный сейчас пользователем 68-раздельный паспорт нельзя считать идентичными артефактами без полного diff. Это существенное расхождение, а не косметическое форматирование. Предыдущая формулировка, будто текущий файл в GitHub полностью представляет 68-раздельный паспорт, была слишком сильной и исправляется этой записью.

### 15.2 Источники истины до reconciliation

До фиксации происхождения и полного сравнения поддерживать три разных объекта, не смешивая их:

1. **Пользовательский полный паспорт из 68 разделов** — предоставленный в текущем чате первичный текст требований. Он должен быть архивирован без редакторских исправлений, с зафиксированным происхождением и контрольной суммой после сохранения.
2. **GitHub Baseline 1.0** — существующий immutable-артефакт по пути `specification/MEDIAHUB-FUNCTIONAL-BASELINE-1.0.md`, созданный коммитом `17b4b47dcc03d7c61f33cb7636a35d9ad0bcde35`. Не переписывать и не переименовывать задним числом.
3. **GitHub Baseline 2.0** — текущий принятый функциональный ориентир по пути `docs/checkpoints/mediahub-functional-baseline-2.0.md`, заявленный как `ACCEPTED — CANONICAL IMMUTABLE REFERENCE POINT`. Его отношение к полному 68-раздельному тексту требует проверки по содержимому, а не только по декларации внутри документа.

### 15.3 Обязательные следующие шаги

- Сохранить предоставленный пользователем текст 68-раздельного паспорта в отдельный новый файл, не затирая существующий Baseline 1.0; перед публикацией проверить полноту разделов 1–68, начало/конец, кодировку и SHA.
- Выполнить diff: пользовательский 68-раздельный паспорт ↔ существующий GitHub Baseline 1.0 ↔ Baseline 2.0.
- Построить матрицу: требование/раздел → статус в Baseline 1.0 → статус в Baseline 2.0 → домен MH-01…MH-23 → конфликт/решение/владелец.
- Проверить происхождение и доступность R4 commit SHA `471f709f5633feab7aeb62dd3ea52effad6d2bc584` и tree SHA `2279612908135418b2b5448d598274ea6741deaa` независимо; наличие tree SHA в тексте не подтверждает существование commit.
- Не объявлять паспортную reconciliation завершённой до полного diff и governance-решения по расхождениям.

### 15.4 Ограничение текущего изменения

В этой итерации обновлена только карта архитектуры. Полный 68-раздельный текст не был повторно записан в новый GitHub-файл, потому что необходимо гарантировать его точное сохранение, а не реконструировать или сокращать по памяти. Существующие baseline-файлы и `main` не изменялись.


---

## 16. ПОЛЬЗОВАТЕЛЬСКИЙ ПАСПОРТ 1.0 СИНХРОНИЗИРОВАН С GITHUB — 2026-10-12

**Статус изменения:** `COMMITTED TO MAIN — CONTENT READ-BACK VERIFIED`  
**Canonical path for the 1.0 edition:** `specification/MEDIAHUB-FUNCTIONAL-BASELINE-1.0.md`  
**Commit:** `dc5ca59e0df9dfc385fa66c26edc08be27073c15`  
**Blob SHA:** `ab190e67b39264d5fe83944e1cf9603e8da7d062`  
**Read-back:** 33,518 characters; 68 numbered section headings detected; section 68 and `END OF PASSPORT` marker present.

### 16.1 Решение по паспорту первой версии

- Файл `specification/MEDIAHUB-FUNCTIONAL-BASELINE-1.0.md` обновлён по прямому указанию пользователя. Он теперь представляет актуальный паспорт **редакции 1.0** с 68 разделами и финальным статусом, переданным пользователем.
- Предыдущая версия файла сохранена в истории Git коммитом `17b4b47dcc03d7c61f33cb7636a35d9ad0bcde35`; историю не переписывали.
- Это не означает, что Baseline 2.0 автоматически отменён: `docs/checkpoints/mediahub-functional-baseline-2.0.md` по-прежнему содержит собственное заявление `ACCEPTED — CANONICAL IMMUTABLE REFERENCE POINT`. Отношение 1.0 и 2.0 требует явной reconciliation/governance-решения. Формулировка «актуальный паспорт первой версии» означает актуальный документ редакции 1.0, а не доказательство того, что 1.0 supersedes 2.0.
- Текущий файл оформлен в Markdown с нормализацией форматирования и группировкой перечней; 68 разделов и их функциональное содержание сохранены. Для побайтного сравнения с исходным сообщением нужен оригинальный текстовый файл пользователя.

### 16.2 Независимая проверка R4 provenance

- GitHub API не разрешает commit SHA `471f709f5633feab7aeb62dd3ea52effad6d2bc584` в репозитории `VlDMlNSh/mediahub-os`: ответ `422 No commit found for SHA`.
- GitHub API разрешает tree SHA `2279612908135418b2b5448d598274ea6741deaa` и возвращает его дерево. Это подтверждает существование объекта tree, но не подтверждает заявленную связь с R4 commit.
- Следовательно, R4 commit/tree provenance остаётся **PARTIALLY VERIFIED / COMMIT UNRESOLVED**. Нельзя утверждать, что immutable R4 baseline полностью подтверждён, пока не найден достоверный commit или не предоставлен источник происхождения.

### 16.3 Текущая сверка Baseline 1.0 ↔ Baseline 2.0

Синхронизация документа 1.0 выполнена, но полная семантическая reconciliation не завершена. Обязательные дальнейшие действия:
1. Сравнить все 68 разделов текущего паспорта с Baseline 2.0 и зафиксировать отсутствующие, изменённые и противоречивые требования.
2. Построить матрицу требований по MH-01…MH-23 с владельцем, authority, зависимостями, доказательствами и governance-решением.
3. Отдельно разрешить потенциальные конфликты по State Authority, Home Assistant authority, мобильным приложениям, AI/cloud boundaries, storage, OTA, продуктовым редакциям и квалификационным gates.
4. Не объявлять архитектуру production-ready, квалифицированной или разрешённой к выпуску на основании одного только паспорта.

### 16.4 Границы выполненной работы

- Изменён только документ паспорта 1.0 в `main` и данная карта в её отдельной ветке.
- Установки, тесты, квалификация, production-запуски и действия на реальном железе не выполнялись.
- Baseline 2.0 не переписывался; R4 commit не изменялся и не создавался.
- Предыдущий раздел 15 отражает состояние до синхронизации и читается с учётом этого раздела 16; пункты раздела 15 о ещё не сохранённом паспорте и неизменённом `main` superseded настоящей записью.


### 16.5 Финальная фиксация статуса 1.0

После первичной синхронизации в `main` выполнен отдельный commit с явной маркировкой «АКТУАЛЬНЫЙ ПАСПОРТ РЕДАКЦИИ 1.0»:
- commit: `1d45bbccbbbd27309c39cb9e9351bb291cdb47a8`;
- blob SHA: `9df4892ed0734050ac79732603d15bb414717310`;
- повторное чтение с GitHub подтвердило 68 нумерованных заголовков, маркировку актуальной редакции 1.0 и конечный маркер `END OF PASSPORT`.

Итоговый путь остаётся `specification/MEDIAHUB-FUNCTIONAL-BASELINE-1.0.md`. Это актуальный паспорт именно версии 1.0. Семантическое сравнение с Baseline 2.0 всё ещё открыто.


---

## 17. НАВИГАЦИОННЫЙ ПРОТОКОЛ, ПАМЯТЬ ПРОЕКТА И АВТОМАТИЗАЦИЯ — 2026-10-12

### 17.1 Обязательное правило «карта → первичные документы → действие»

Для дальнейшей работы в этом чате и при возобновлении работы в новом чате карта является первым навигационным документом, а не заменой первичных источников.

Перед каждым самостоятельным действием по проекту:
1. Прочитать актуальный `docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md` из ветки `docs/mediahub-chat-tree-map-20261012`; проверить SHA и последние разделы.
2. Найти в карте релевантный домен MH, конфликт, первичный документ, путь, ветку и известный SHA.
3. Прочитать указанные первичные документы из правильной ветки/ref. Не полагаться только на пересказ карты, старую память чата или search snippet.
4. Разделить факты на `CONFIRMED`, `PROPOSED`, `CONFLICT`, `NOT FOUND`, `NOT VERIFIED`; фиксировать точный источник и SHA.
5. Только после этого выполнять действие, разрешённое текущей фазой. Сейчас фаза — архитектурный аудит и документация; без отдельного разрешения не делать установок, реальных hardware-тестов, квалификационных запусков, destructive operations или изменений инфраструктуры.
6. После изменения документа повторно прочитать его из GitHub и подтвердить commit SHA, blob SHA, ключевые маркеры и отсутствие случайной потери содержания.
7. Обновить карту только подтверждёнными результатами, добавив дату, источник, SHA, статус и следующий шаг. Не выдавать намерение за результат.

### 17.2 Карта как внешняя память чата

Карта — индекс и долговременная проектная память, но не буквальная копия всего репозитория и не гарантия, что весь проект автоматически загружен в контекст модели. Для восстановления контекста следует:
- начинать с разделов 1–8 карты для правил, дерева, документов, инвариантов, конфликтов и критерия полноты;
- использовать разделы 9–13 для branch diff, истории доменов, путей и acceptance/evidence;
- использовать разделы 14–16 для паспорта 1.0, Baseline 2.0, provenance и открытой reconciliation;
- использовать текущий раздел 17 как обязательный operating protocol;
- затем читать первичные документы по затрагиваемому домену и сверять актуальные refs/SHA.

Если новый чат не имеет доступа к этой ветке или инструментам GitHub, он должен явно сообщить об ограничении и запросить карту/доступ, а не утверждать, что восстановил полное содержимое проекта.

### 17.3 Паспортная иерархия — текущая формулировка

- `specification/MEDIAHUB-FUNCTIONAL-BASELINE-1.0.md` — **актуальный паспорт редакции 1.0**, 68 разделов, blob SHA `9df4892ed0734050ac79732603d15bb414717310`.
- `docs/checkpoints/mediahub-functional-baseline-2.0.md` — отдельный документ Baseline 2.0 со статусом `ACCEPTED — CANONICAL IMMUTABLE REFERENCE POINT`, blob SHA `1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f`.
- Не сводить эти два утверждения к ложному выводу, что 1.0 уже supersedes 2.0 или что 2.0 автоматически отменяет требование владельца считать паспорт 1.0 актуальным паспортом первой версии.
- Следующий governance-артефакт должен объяснить версионирование, область нормативности и порядок разрешения конфликтов между 1.0 и 2.0; до этого reconciliation остаётся `OPEN`.

### 17.4 Подключённая автоматизация аудита

Создана и включена еженедельная автоматизация ChatGPT:
- Название: `MediaHub Map Audit`
- Automation ID: `6acca178cf1081919c240615580688a6`
- Режим: еженедельно по понедельникам, гибкое время, timezone `Asia/Singapore`.
- Тип: read-only аудит карты и выбранных первичных документов; сверка SHA/статусов, изменений main и ветки карты, конфликтов и ближайшего безопасного шага.
- Запреты: не устанавливать ПО, не запускать тесты/квалификацию, не изменять репозиторий, PR, настройки или инфраструктуру; не объявлять результат без повторного чтения GitHub.
- Автоматизация создана и включена; создание расписания не доказывает, что первый запуск уже выполнен. `next_run_time` при создании не был предоставлен сервисом.

Автоматизация является дополнительным контрольным циклом и не заменяет правило читать карту перед каждым действием в активном чате. Она не делает все документы постоянно загруженными в модель и не гарантирует автономную запись результатов в GitHub.

### 17.5 Следующие приоритеты после подключения навигации

1. Составить карту источников требований и конфликтов Baseline 1.0 ↔ Baseline 2.0 по всем тематическим разделам, а не только по заголовкам.
2. Добавить таблицу трассируемости: требование/номер раздела → первичный источник и SHA → домен MH → контракты/зависимости → acceptance/evidence → конфликт/решение/владелец.
3. Верифицировать назначение каждого MH-01…MH-25 и отличать чат, домен, branch, prompt, implementation и acceptance record.
4. Уточнить ссылки на master prompts, acceptance criteria, dependency maps, evidence registers, checkpoints и component manifests с правильными refs.
5. Отдельно держать реестр неподтверждённых утверждений, включая R4 commit SHA, и не повышать их статус без проверяемых доказательств.

### 17.6 Ограничения выполненного шага

- Перед изменением прочитаны карта и релевантные паспорта/checkpoint-документы с GitHub.
- Создана только автоматизация read-only аудита; её первый запуск не подтверждён.
- Этот раздел добавлен в ветку карты, не в `main`.
- Установка, hardware-тесты, qualification, release и production не выполнялись.
