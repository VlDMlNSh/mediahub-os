# MediaHub — инструкция загрузки контекста и обязательного анализа перед действием

- Статус: рабочая инструкция проекта; не заменяет нормативные Baseline и governance-решения.
- Карта проекта: [MEDIAHUB-CHAT-TREE-MAP.md](MEDIAHUB-CHAT-TREE-MAP.md)
- Исторический источник требований и provenance редакции 1.0: `specification/MEDIAHUB-FUNCTIONAL-BASELINE-1.0.md` в `main`; он не является текущим каноническим функциональным эталоном.
- Baseline 2.0: `docs/checkpoints/mediahub-functional-baseline-2.0.md` в `main`.
- Назначение: восстановление релевантного контекста по первичным документам и предотвращение действий без проверки зависимостей.

## 1. Обязательный протокол перед КАЖДЫМ действием

Перед любым чтением с последствиями, изменением файла, Git-операцией, созданием PR, запуском команды, установкой, тестом, квалификацией, деплоем или изменением инфраструктуры:

1. **Открыть карту** `docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md` в актуальной ветке карты. Проверить ветку, дату инвентаризации, Blob SHA и статус. Если карта недоступна или устарела — остановиться на безопасном чтении, восстановить индекс и не делать необратимых действий.
2. **Определить домен и маршрут**: найти соответствующий MH-01…MH-25, раздел карты, связанные документы, контракты, acceptance criteria, evidence registers, checkpoints, ветки и открытые противоречия. Не искать весь репозиторий вслепую, если карта уже указывает путь.
3. **Открыть первичные документы** из указанных путей/веток; сверить SHA, commit/ref, статус и происхождение. Для решений, затрагивающих несколько доменов, прочитать документы всех затронутых доменов и их зависимости.
4. **Сверить источники истины**: Functional Baseline 2.0 (`docs/checkpoints/mediahub-functional-baseline-2.0.md` на `main`) — текущий принятый канонический функциональный эталон; сам документ прямо supersedes Baseline 1.0 как current functional reference. Baseline 1.0 — сохранённый исторический источник/provenance, а не параллельная текущая нормативная точка. Не смешивать baseline и не импортировать дополнительные требования B1 в B2 молча; любое изменение B2 или восстановление/применение дополнительного требования B1 требует явного решения владельца и change control. Более ранняя формулировка этой инструкции, по которой B1 назван актуальным паспортом текущих требований и «ни один baseline не отменяет другой», устарела и заменена принятым статусом B2 и текущей инструкцией владельца.
5. **Проверить полномочия и ограничения**: определить, разрешено ли действие; проверить состояние ветки, diff, незакоммиченные изменения, provenance, зависимости, риски, безопасность и возможность отката. Не перезаписывать чужие/локальные изменения; не выполнять merge в `main` без отдельного разрешения.
6. **Сформулировать проверяемый план**: ожидаемый результат, точные файлы/ресурсы, критерий успеха, риски и способ проверки. Если не хватает данных или требуется решение владельца продукта — остановиться и запросить решение, а не угадывать.
7. **Выполнить только разрешённый объём**. Не расширять задачу автоматически на соседние изменения. Не выдавать наличие документа за принятие, реализацию, тестирование, квалификацию или production-допуск.
8. **Проверить результат**: после изменения повторно прочитать затронутые файлы/ресурсы, проверить SHA и diff, ссылки, критерии и побочные эффекты. Записывать в карту только подтверждённые факты с путями, refs, SHA, датой и статусом.
9. **Обновить память проекта**: если обнаружены новые документы, ветки, решения, расхождения или изменившиеся статусы, обновить карту в отдельной документальной ветке, затем сделать read-back. Не переписывать исторические свидетельства и не объявлять полную сверку, пока не пройдены все строки матрицы.
10. **Отчитаться точно**: разделять подтверждённое, предполагаемое, частично проверенное и неизвестное. Указать выполненное действие, файлы/refs/SHA, проверку, оставшиеся риски и следующий безопасный шаг.

## 2. Постоянные архитектурные инварианты

- Product State Authority — единственный источник изменения canonical product state. A0-ASTRA — инженерная координация/очередь/evidence/qualification, а не Product State Authority.
- Home Assistant Core — единственный authority в домене Smart Home в пределах утверждённых границ.
- AI, cloud, workflow engine, plugins, adapters, knowledge graph, persistence и observability не становятся State Authority.
- Cloud/AI остаются вне канонической власти продукта; сохранять local-first поведение и fail-closed на неопределённости.
- Отделять reported/observed/desired/policy-allowed/commanded/committed/applied/confirmed/predicted state.
- Не считать кандидатов (например, Temporal, LangGraph, LiteLLM), черновики, branch-only файлы или найденные репозитории утверждёнными/установленными без evidence.
- Не путать стадии IDEA → DESIGN → IMPLEMENTED → TESTED → VERIFIED → QUALIFICATION CANDIDATE → QUALIFIED → RELEASED → DEPLOYED → OBSERVED → PRODUCTION ACCEPTED.
- Независимая квалификация не может быть заменена self-review; release и production требуют отдельных разрешений и evidence.
- Роли — наборы capability, а не обязательные постоянно работающие отдельные боты.
- Не запускать установку, тесты, квалификацию, очистку дисков, перезапись данных или production-действия без явного разрешения пользователя на соответствующий этап. Учитывать известное ограничение: `mh-dev-01` ранее имел заполненный на 100% root disk; никаких записей или очистки на этом хосте без отдельного разрешения и предварительной диагностики.
- Не заявлять, что автономный контроллер, очередь, тест, soak или qualification реально выполняются, пока это не подтверждено свежими журналами/статусами и evidence.

## 3. Правила карты и памяти

- Карта — навигационный индекс и журнал подтверждённых результатов, не хранилище всех файлов целиком.
- Перед задачей читать карту; затем извлекать только необходимые первичные источники, указанные в карте. Для широкого аудита читать несколько связанных документов и обновлять матрицу трассируемости.
- Для каждого важного утверждения сохранять: `claim → source path → ref/branch → commit SHA → blob SHA → status → verification date`.
- Отсутствие документа в одном пути не доказывает его отсутствия в проекте: проверить варианты путей, ветки, историю и checkpoints.
- Не переписывать историю, не подменять старые артефакты новыми и не повышать статус без явного acceptance evidence.
- Если GitHub/API/инструмент недоступен, прямо указать, что именно не удалось проверить; не подставлять выдуманные данные.
- Если сессия новая, начать с раздела карты «правила интерпретации», дерева доменов, последних результатов и открытых конфликтов; после этого читать актуальные источники задачи.

## 4. Короткий bootstrap-промпт для начала нового чата

> Работай над MediaHub OS строго по инструкции `docs/architecture/MEDIAHUB-CONTEXT-BOOTSTRAP-INSTRUCTION.md`. Перед каждым действием сначала открой актуальную `docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md`, пройди по её навигации к нужным MH-доменам и прочитай все необходимые первичные документы, проверив refs, SHA, статусы, зависимости и ограничения. Используй карту как внешнюю проектную память, но не считай её заменой первичным источникам. Baseline 2.0 — текущий принятый канонический функциональный эталон; Baseline 1.0 — исторический provenance. Не смешивай версии; изменение или дополнительная реабилитация требования B1 требует явного решения владельца и change control. Ничего не устанавливай, не запускай тесты/квалификацию и не меняй инфраструктуру без отдельного разрешения. Не перезаписывай локальные изменения и не делай merge в main без разрешения. После каждого изменения выполни read-back, проверь результат и зафиксируй подтверждённые факты в карте с путями/SHA. Отчитывайся только по проверенным данным, явно отмечай пробелы и следующий безопасный шаг. Начни с чтения карты и последнего checkpoint, затем выполняй мою текущую задачу.

## 5. Границы гарантии

Эта инструкция заставляет агента следовать retrieval-протоколу в пределах доступных инструментов и контекста, но сама по себе не загружает весь репозиторий в окно контекста модели и не гарантирует, что другой агент/платформа соблюдёт её автоматически. Для устойчивого поведения её следует подключить к системным/project instructions используемого агента, а карту и первичные документы держать доступными в GitHub.


## 6. Живые refs, SHA и автоматическое обновление ссылок

Перед КАЖДЫМ запросом `/next` заново проверь GitHub, а не доверяй URL или SHA, сохранённым в этой инструкции, карте, checkpoint или истории чата:

1. Найди фактические refs для документационной ветки и `main`; зафиксируй текущие HEAD SHA и результат compare (ahead/behind/diverged/merge base), если инструмент это предоставляет.
2. По фактической документационной ветке перечитай Bootstrap, карту, current checkpoint и Master Development Roadmap. Проверь пути, blob SHA, доступность файлов, актуальность содержания и внутренние ссылки. Для источников в `main` читай именно `main`, а не одноимённый файл документационной ветки.
3. Различай обычное изменение blob SHA после редактирования и реальное изменение маршрута. Само по себе изменение SHA не требует замены URL. Повод для обновления — переименование/удаление ветки, перенос/переименование файла, неработающая или ведущая не к актуальному содержимому ссылка, либо переход на новую каноническую контрольную точку.
4. Если изменились ветка или путь любой ссылки, используемой в Project Instructions, не оставляй это только в истории чата: в том же проходе обнови ссылочную запись в GitHub, если это разрешено; затем в финальном отчёте обязательно выдай отдельное задание «ЗАМЕНИТЬ ИНСТРУКЦИЮ ПРОЕКТА CHATGPT» с готовым текстом замены и новыми прямыми URL. Если замена в GitHub требует полномочий/решения, не делай её молча — выдай задание и объясни блокер.
5. После каждого документального изменения повторно прочитай изменённые файлы и проверь blob SHA/содержание. Обнови карту и current checkpoint. В финале укажи фактическую ветку/HEAD, SHA файлов и прямую ссылку на актуальную карту.
6. Если проверить refs или содержание не удалось, пометь контрольную точку как НЕ ПРОВЕРЕНА; не объявляй ссылки актуальными и не продолжай к действиям с последствиями.

`/next` — это рабочий цикл: live GitHub state → следующий незакрытый шаг единого Master Development Roadmap → ограниченный разрешённый проход → read-back и проверка доказательств → запись результата в GitHub, карту и checkpoint → точный отчёт и, при drift ссылок, готовое задание на замену Project Instructions.


## 0. Каноническая инструкция проекта и ссылка на неё

**Полная каноническая инструкция проекта размещена в GitHub и должна перечитываться перед каждым `/next`:**

- Прямая ссылка на эту инструкцию: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CONTEXT-BOOTSTRAP-INSTRUCTION.md
- Актуальная карта проекта: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
- Актуальный continuation checkpoint: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/checkpoints/mediahub-next-continuation-checkpoint-2026-10-12-current.md
- Единый мастер-план разработки: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/checkpoints/MEDIAHUB-MASTER-DEVELOPMENT-ROADMAP-1.0.md

Эти URL — текущие указатели, а не доказательство актуальности refs. На каждом `/next` сначала проверь фактическую ветку и HEAD, доступность всех файлов, пути и blob SHA. Если ветка или путь изменились, найди действующие ссылки, обнови затронутые проектные документы в пределах разрешённых прав и выдай пользователю готовое задание на замену инструкции ChatGPT Project Instructions. Не считай, что пользовательские настройки ChatGPT обновлены автоматически.


## 7. Принцип крупных связных проходов и запрет повторной инвентаризации

Цель `/next` — максимальный проверяемый прогресс к архитектуре, контрактам и независимой приёмке, а не максимальное число мелких коммитов. После обязательного live-read выбери самый крупный связный объём, который одновременно разрешён текущими полномочиями, опирается на первичные источники и может быть полностью проверен за проход.

1. **Не повторяй уже закрытый deliverable.** Ищи его в текущей ветке и по релевантным refs/веткам до создания нового файла. Если артефакт уже существует, проверь его свежесть и качество, затем двигайся к следующему зависимому незакрытому результату.
2. **Работай пакетом зависимых документов.** Когда одна доказанная находка меняет маршрут/статус/трассировку, за один проход согласованно обнови первичный рабочий артефакт, master roadmap при изменении очередности, карту, checkpoint и затронутые crosswalk/passport sections. Не размножай одну и ту же полную информацию: держи подробности в одном канонически индексируемом рабочем артефакте, а в остальных — краткую ссылку и подтверждённый статус.
3. **Разделяй документальную автономность и решения владельца.** Выполняй все независимые чтения, сверки, структурирование доказательств, обнаружение противоречий и подготовку вариантов без ожидания владельца. Останавливай только конкретный шаг, требующий owner decision/authorization; продолжай независимые ветви работы.
4. **Не называй проход широким без проверяемого результата.** Для каждого крупного прохода нужны source/ref/blob SHA, точный результат, критерий проверки, read-back и следующий зависимый шаг. Масштаб оценивается числом закрытых доказательных зависимостей, а не количеством изменённых файлов.
5. **Не перепрыгивай gates.** Быстрый прогресс не означает установки, тестов, qualification, provider/model calls, credentials, host/runtime inspection, инфраструктурных изменений, deployment, merge/rebase/cherry-pick или решения владельца без отдельного разрешения.
6. **Когда найден следующий артефакт уже созданным позднее:** не создавать дубль. Прочитать его, обновить только доказанные ошибки/статусы и сразу продолжить по его handoff.

Текущий пример применения: source-anchored node/service placement matrix уже существует в `docs/checkpoints/MEDIAHUB-NODE-SERVICE-PLACEMENT-AND-DECISION-REGISTER-01.md`; следующий проход не должен повторять инвентаризацию. Используй его для точной crosswalk-сверки и подготовки owner-decision packet `docs/checkpoints/MEDIAHUB-OWNER-DECISION-PACKET-01.md`, сохраняя DEC-DEV-01…08 и не принимая решения за владельца.


## 8. Owner direction: engineering autonomy and decision escalation

Owner direction recorded on 2026-10-14: **bring the project to one coherent, verifiable architecture without turning every technical detail into a separate owner approval.**

Operational interpretation:
1. Resolve technical design details independently when they are within existing accepted contracts, roadmap sequencing, permissions, and safety constraints. Prefer the simplest verifiable design that preserves current invariants.
2. Do not ask the owner to choose routine implementation mechanics, protocols, data structures, evidence formats, source-comparison methods, or ordinary engineering trade-offs. Research, compare, recommend, document, and verify those independently.
3. Escalate only decisions that materially change product intent, accepted architecture, trust boundaries, data-egress policy, budget/hardware commitments, irreversible actions, authority boundaries, or explicit owner/governance gates.
4. For each escalation, state the question in plain language, recommend one option, explain the consequence of alternatives, and distinguish facts from assumptions and proposals. Do not treat silence or a recommendation as acceptance.
5. If an action is blocked by missing authorization, do independent read-only/documentation work that does not cross the blocked boundary.
6. This direction does not grant permission for software installation, tests/qualification, provider/model calls, credentials, host/runtime inspection, infrastructure changes, deployment, migration, merge, rebase, or cherry-pick. Existing prohibitions and gates remain in force.
7. Each /next must select the next unfinished step in the live Master Development Roadmap, perform one bounded verifiable pass, read back changed artifacts, and update the map/checkpoint when relevant. Avoid duplicating existing deliverables.
8. The owner decision register is a navigation/support artifact, not a normative contract: ../checkpoints/mediahub-owner-decision-register-2026-10-14.md.

This instruction records a working method and does not itself accept any proposed architecture or change Functional Baseline 2.0.

## Clean-slate target rule — new hardware

Owner direction (2026-10-15): MediaHub OS is to be rebuilt as a new system for new hardware. Unsuccessful attempts to install/deploy on retired servers are not a source of target configuration, installed-component assumptions, host identity, runtime state, or acceptance evidence.

For every legacy artifact, distinguish RETIRE (confirmed old-target-only active artifact), HISTORY (preserve provenance, never treat as target state), REUSE-CANDIDATE (generic component requiring fresh admission), and UNKNOWN (insufficient evidence). Do not erase audit history or delete shared components based only on names. Before deleting a candidate, inspect its references and dependent contracts; record exact paths and resulting blob/commit SHAs. New hardware details remain UNKNOWN until supplied or accepted explicitly. Keep Contour A setup/qualification/acceptance separate from Contour B product implementation.
