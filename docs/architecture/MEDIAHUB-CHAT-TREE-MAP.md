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
