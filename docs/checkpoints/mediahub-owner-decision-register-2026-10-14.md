# MediaHub — единый реестр архитектурных вопросов владельца

- Дата: 2026-10-14
- Ref: docs/mediahub-chat-tree-map-20261012
- Статус: ЧАСТИЧНО РАЗРЕШЁН — D-03 ПРИНЯТ ВЛАДЕЛЬЦЕМ 2026-10-14; D-01/D-04…D-10 остаются PROPOSED/OPEN; нормативные контракты не меняются автоматически
- Назначение: свести к одному понятному списку только решения, которые действительно требуют выбора владельца. Технические детали, протоколы, форматы evidence и способы проверки остаются на стороне инженерной работы, если не меняют продуктовые цели, границы доверия или расходы/риски.
- Ограничение: это крупный проход по сводным документам, а не заявление о полном построчном аудите всех файлов и всех веток GitHub.

## Рекомендуемая позиция по умолчанию

Сохранять действующие ограничения: Baseline 2.0 — единственный текущий функциональный эталон; Product State Authority — единственный владелец канонических изменений состояния продукта; Home Assistant Core — authority в Smart Home в утверждённых границах; Jarvis и ASTRA координируют инженерную работу, но не становятся authority продукта; local-first, явная политика передачи данных и запрет тихого cloud fallback; Contour A должен пройти развёртывание и независимую приёмку до начала продуктовой разработки в Contour B. Это рекомендация продолжать действующие контракты, а не новое решение.

## A. Решения владельца — действительно архитектурные

### D-01. Что строим первым?
**Простыми словами:** сначала доводим до готовности инженерную среду, которая помогает разрабатывать и проверять проект, или одновременно начинаем создавать конечную систему?
- **Рекомендуемый вариант: A — сначала Contour A**, пройти независимые readiness gates и приёмку, затем Contour B.
- Почему: это действующая последовательность мастер-плана и снижает риск смешать инструменты разработки с продуктом.
- Другой вариант потребует явного изменения мастер-плана и границ допуска.

### D-02. Кто имеет право менять подтверждённое состояние MediaHub OS?
**Рекомендуемый вариант:** сохранить Product State Authority как единственную точку канонических изменений. Jarvis, ASTRA, AI, плагины, UI, устройства, облако и workflow только запрашивают действия через разрешённые контракты.
- Это существующий инвариант, а не новый вопрос для повторного голосования, если владелец не хочет менять фундамент.

### D-03. Модель работы Jarvis — ПРИНЯТО ВЛАДЕЛЬЦЕМ 2026-10-14
**Решение владельца:** Jarvis — верхний координационный слой распределённой гибридной автономной разработки; впоследствии он должен управлять облачной системой разработки и иметь непосредственную интеграцию с GitHub для управления репозиторием через разрешённый интерфейс.
- Jarvis координирует задачи, выбирает способ выполнения и применяет явную политику маршрутизации по задаче и классу данных.
- Claude Code — инженерный клиент/agent surface Jarvis. Само использование Claude Code не доказывает, что запрос исполняется hosted-моделью Anthropic: фактический исполнитель определяется разрешённым маршрутом.
- Для Claude Code предусмотрен путь через FCC как обязательный integration/control layer; целевая маршрутизация может направлять запросы к локальному Alamo/Ollama либо к облачным моделям через FreeLLMAPI, в зависимости от задачи, класса данных, egress-политики и разрешённой конфигурации.
- FreeLLMAPI — облачный provider path, а не MediaHub authority и не гарантия постоянной бесплатной доступности. Ollama — отдельный локальный runtime для совместимых моделей. Локальный режим не должен незаметно переключаться на Anthropic или другого внешнего провайдера.
- Архитектура architecture/MEDIAHUB-DISTRIBUTED-AI-INFRASTRUCTURE.md на main (blob e549692f207fbc91d9b9b9b92b8e665404f07290) описывает эту топологию как логическую; она не является доказательством установленной/работающей интеграции.
- ASTRA обеспечивает автономную инженерную координацию только в предоставленных полномочиях.
- Product State Authority сохраняет исключительное право на канонические изменения состояния продукта. Jarvis и GitHub-интеграция не получают полномочий Product State Authority.
- Прямое управление GitHub означает capability-scoped операции через адаптер, аудит, проверку diff и действующие разрешения. Это не разрешение на обход review/branch protection, самовольный merge, выпуск, deployment или изменение production.
- Любая передача данных внешнему провайдеру через FreeLLMAPI/Anthropic или иной cloud route допускается только после классификации и разрешения политики; local-only задача не переключается в облако незаметно. Ошибка/недоступность выбранного исполнителя не даёт права на автоматический внешний fallback.
- Техническая реализация, API/адаптеры, журналирование, ограничение полномочий и верификация остаются инженерной задачей в рамках принятых контрактов.
- Статус: OWNER-ACCEPTED D-03 / ARCHITECTURE DIRECTION; реализация, квалификация и допуск к эксплуатации не подтверждены.

### D-04. Какие данные можно отправлять во внешние сервисы?
- **Рекомендуемый вариант:** только по классификации данных и явной политике для каждого назначения; не отправлять секреты и локально ограниченные данные без разрешения. Никакого незаметного переключения с локальной модели на облачную.
- От владельца нужны только исключения для конкретных классов данных; enforcement — инженерная задача.

### D-05. Какую роль получает Mac mini Server 2011?
- **Рекомендуемый вариант:** необязательный legacy-узел для лёгких вспомогательных задач, только если отдельно подтверждены ОС, безопасность, ресурсы и восстановление. Не считать его заранее пригодным для современных локальных моделей.
- Уточнение от владельца требуется, только если этот узел должен быть обязательным.

### D-06. Нужен ли удалённый GPU-сервер на первом этапе?
- **Рекомендуемый вариант:** не делать его обязательной зависимостью Contour A; предусмотреть подключение позже через изолированный и проверяемый интерфейс.
- От владельца нужны бюджет и ограничения на размещение только если сервер должен стать обязательным.

### D-07. Какую автономность разрешаем?
**Простыми словами:** что система делает сама, а где ждёт человека?
- **Рекомендуемый вариант:** автоматизировать заранее разрешённые, ограниченные и обратимые инженерные действия. Изменение архитектурных контрактов, секретов, инфраструктуры, production, разрушительные операции и продвижение qualification/release требуют отдельного разрешения и доказательств.
- От владельца нужны только бизнес-исключения; лимиты, аудит, отмену, изоляцию и проверку результата проектирует инженер.

### D-08. Что означает «система готова»?
- **Рекомендуемый вариант:** раздельные gates: реализация → тестирование → проверка → квалификация → выпуск → развёртывание → наблюдение → приёмка. Один этап не доказывает следующий.
- Production остаётся NO-GO без требуемых evidence и разрешений.

### D-09. Объединяем ли все машины и данные в одну доверенную сеть?
- **Рекомендуемый вариант: нет.** Раздельные trust domains, минимальные права, отдельная авторизация приложения, отзыв доступа и аудит. Клиентская среда и contributed compute не получают доступ к developer secrets или очередям только из-за сетевого подключения.
- Владелец нужен только если хочет изменить сами границы доверия; сетевые детали — инженерная ответственность.

### D-10. Можно ли использовать требования Baseline 1.0 как текущие без отдельного согласования?
- **Рекомендуемый вариант: нет.** Baseline 2.0 остаётся текущим принятым эталоном; Baseline 1.0 — исторический источник. Возвращение дополнительного требования из B1 требует явного решения и change control.
- Это уже зафиксированный инвариант; повторное подтверждение не требуется, если владелец не инициирует change request.

## B. Что не нужно перекладывать на владельца

Инженер самостоятельно готовит и документирует:
- форматы task envelope, idempotency, lease/heartbeat, retry/cancellation и recovery;
- аудит, provenance, evidence и трассировку «утверждение → источник → версия → проверка»;
- поиск дублей и расхождений, таблицы трассируемости и проверку исторических ID;
- адаптеры, API-контракты, тайм-ауты, health/readiness, метрики и журналы;
- размещение служб после получения подтверждённых аппаратных характеристик и ограничений безопасности/ресурсов;
- лицензии, происхождение артефактов, совместимость версий и сравнение технических кандидатов;
- sandbox, ограничения инструментов, секретов и worktree, проверку вывода моделей как недоверенных данных;
- acceptance criteria и evidence checklist.

Установка, вызов провайдера, использование credentials, запуск тестов/квалификации, исследование runtime/host, изменение инфраструктуры, deployment или merge по-прежнему требуют отдельного разрешения.

## C. Подтверждённые группы противоречий и пробелов

1. **Статусы доменов:** карта содержит частично закрытые домены и прямо говорит, что полная приёмка не доказана. Более поздние отчёты могут фиксировать более позднюю стадию; сохранять даты и provenance.
2. **Ветки и канонические версии:** специализированные ветки могут быть diverged от main. Наличие файлов не делает их каноническими; нужны актуальные HEAD, ancestry и содержательное сравнение.
3. **MH-18:** несколько handoff/sync веток; канонический вариант нельзя выбирать только по имени.
4. **MH-23:** имя ветки architecture/mh-23-long-term-evolution не совпадает напрямую с названием домена Migration; проверить происхождение и scope, не переименовывать автоматически.
5. **State Authority:** старые blueprint-формулировки, назначающие A0-ASTRA State Authority, конфликтуют с действующим разделением ролей. До governance-решения сохранять Product State Authority как каноническую власть.
6. **HA/распределённое состояние:** предложения PostgreSQL/etcd/NATS не являются автоматически частью принятой single-node/in-memory foundation.
7. **P0-07:** authorization/publication/API gap остаётся блокером для продвижения canonical mutations и связанных автоматизированных стадий.
8. **MH-14/15/16/21/22:** физическая persistence, OS/appliance acceptance, lifecycle implementation, hybrid-cloud implementation и production qualification нельзя считать разрешёнными или готовыми по одному проектному документу.
9. **ASTRA/Jarvis:** доказательства очереди, выполнения задач, изоляции исполнителей и квалификации должны быть актуальными и привязанными к точному revision; старые branch-specific evidence не подтверждают текущий runtime.
10. **Аппаратная неопределённость:** точные спецификации Mac Pro, Mac mini, будущего GPU-сервера и тестовых хостов не подтверждены этим документальным проходом; не выбирать модели/нагрузки на догадках.
11. **Claude/Ollama/Jarvis:** D-03 принят владельцем 2026-10-14: Jarvis — верхний координационный слой, политика маршрутизации выбирает разрешённого исполнителя на задачу, Claude остаётся внешним исполнителем, Ollama — отдельным локальным runtime. GitHub управляется через ограниченный и аудируемый адаптер. Реализация и квалификация не подтверждены.
12. **Карта неполна:** карта сама обозначает инвентаризацию как неполную приёмку. Этот документ не превращает аудит в полный.

## D. Как отвечать

D-03 явно принят владельцем 2026-10-14 и больше не считается открытым вопросом о выборе между Claude-оператором и маршрутизатором на каждую задачу. Принятие фиксирует архитектурное направление, но не доказывает реализацию и не снимает действующие gates. D-01, D-04…D-10 остаются открытыми, пока владелец отдельно их не разрешит. Молчание по остальным пунктам не означает принятия.

## E. Проверки и ограничения прохода

- Прочитаны Bootstrap, Project Map, Current Continuation Checkpoint и Master Development Roadmap с документационной ветки.
- GitHub branch search вернул множество ASTRA и архитектурных веток, но полное сравнение branch trees не выполнялось.
- Поиск GitHub по тексту реестров в этом вызове не дал пригодных результатов; конфликты собраны из доступных сводных документов, а не объявлены результатом полного поиска всех документов.
- Не выполнялись тесты, квалификация, установка, вызов провайдеров, использование credentials, исследование runtime/host, изменение инфраструктуры, deployment, merge, rebase или cherry-pick.


## Contour A D-ING ingress decision register cross-reference (2026-10-16)

- Related decision-path analysis: [WB-14W A0 Ingress Decision-Register Ownership and Acceptance Paths](MEDIAHUB-CONTOUR-A-WB-14W-A0-INGRESS-DECISION-REGISTER-OWNERSHIP-AND-ACCEPTANCE-PATHS-2026-10-16.md).
- D-ING-01…04 and D-ING-05a, D-ING-05b, D-ING-06 remain OPEN. These are cross-referenced here for visibility; this entry does not accept any option or alter the normative contracts.
- The reviewed sources do not name accountable individuals or establish a formal approval workflow for these decisions. WB-14W proposes role-level owners for explicit confirmation only. Recommendations, silence, or an architecture document are not owner acceptance.
- MH-06 ADR-001 remains ACCEPTED / GOVERNANCE ACCEPTED for its stated Core Runtime Services scope; implementation authorization remains NO. The generic domain-health mapping, A0 probe contract and A0 lifecycle transition table are separate unresolved decisions.
- No implementation, schema registration, tests, qualification, deployment or runtime action is authorized by this cross-reference.

## Contour A route-boundary clarification — WB-14Y (2026-10-16)

- See [WB-14Y ASTRA A0 Ingress vs Product-Mutation Boundary Correction](MEDIAHUB-CONTOUR-A-WB-14Y-A0-INGRESS-VS-PRODUCT-MUTATION-BOUNDARY-CORRECTION-2026-10-16.md).
- Do not conflate owner-register D-03, project DEC-DEV-02, or ingress D-ING-03. DEC-DEV-02 Option C is owner-approved in the owner decision packet §8; the stale §6.1 summary was corrected without changing primary normative sources.
- Jarvis → ASTRA A0 engineering ingress and P0-07 → P0-05 → P0-04 product mutation are distinct routes. The latter's caller/header issues do not automatically decide the former's API or block all engineering submissions; product mutations remain blocked by their own gates.
- Existing D-ING-01…04, D-ING-05a/05b and D-ING-06 remain OPEN; no new option, issuer, protocol, schema, or implementation status was accepted.

## Contour A A0 ingress source-contract census — WB-14Z (2026-10-16)

- Report: [WB-14Z ASTRA A0 Ingress Source-Contract Census](MEDIAHUB-CONTOUR-A-WB-14Z-A0-INGRESS-SOURCE-CONTRACT-CENSUS-2026-10-16.md).
- WB-14Z source-pinned the Jarvis adapter draft, WB-14B caller trace, Wave 07 A0/MH-12 trace, executor capability matrix, ASTRA GOLD internal design and governance contract. Existing sources establish internal A0 lifecycle policy but do not establish an accepted Jarvis→A0 API/issuer/idempotency/status/result contract.
- The local file task ingress and signed operational-command path remain separate and are not evidence of a connected authenticated Jarvis producer. Internal lease/retry values are not external TTL/idempotency policy.
- Product mutation remains a separate P0-07→P0-05→P0-04 route. No A0 ingress permission bypasses it. All D-ING decisions remain OPEN where previously recorded.
- Next: prepare a transport-neutral, clearly PROPOSED A0 ingress contract candidate from the source-backed requirements; do not register schema IDs or implement before explicit owner/governance acceptance.

## Contour A A0 ingress contract candidate — WB-14AA (2026-10-16)

- Proposal: [WB-14AA ASTRA A0 Ingress Contract Candidate](MEDIAHUB-CONTOUR-A-WB-14AA-ASTRA-A0-INGRESS-CONTRACT-CANDIDATE-2026-10-16.md), status PROPOSED / NOT ACCEPTED / NOT FROZEN / NOT IMPLEMENTED.
- Provides a transport-neutral logical operation inventory, minimum request envelope, durable admission/idempotency requirements, lifecycle/fencing/cancellation/result semantics, trust-boundary requirements, failure matrix and nine local proposal decisions.
- Does not select transport, endpoint, schema ID, issuer, crypto profile, storage or numeric TTLs. Proposal decision IDs are not canonical registry IDs; collision-check before promotion.
- No implementation, tests, qualification or runtime activity. All A0 ingress-specific owner/governance questions remain OPEN.

## Contour A A0 ingress ID and decision-owner crosswalk — WB-14AB (2026-10-16)

- Report: [WB-14AB A0 Ingress Proposal-ID Collision Audit and Decision-Owner Crosswalk](MEDIAHUB-CONTOUR-A-WB-14AB-A0-INGRESS-ID-COLLISION-AND-DECISION-OWNER-CROSSWALK-2026-10-16.md).
- Bounded scan found no exact `A0-ING-01…09` hits in the reviewed map, checkpoint, roadmap, owner records, MH-12 and ASTRA governance/source files. This is not an all-branch absence proof; retain these labels as proposal-local, not canonical decision IDs.
- Crosswalk maps A0-ING-02 to D-ING-01/02, A0-ING-04 to D-ING-03, A0-ING-06 to D-ING-04, A0-ING-07 to D-ING-05b, A0-ING-05 to D-ING-06; A0-ING-01/03/08/09 retain cross-cutting acceptance dependencies. Keep D-ING-05a and D-ING-05b separate.
- WB-14W's role-level acceptance paths remain proposals; accountable individuals/delegated authority and formal approval workflow are NOT ESTABLISHED. No options selected; WB-14AA remains PROPOSED / NOT ACCEPTED / NOT FROZEN.

## A0 ingress evidence and qualification boundary — WB-14AC (2026-10-16)

- Report: [WB-14AC A0 Ingress Evidence and Qualification-Boundary Crosswalk](MEDIAHUB-CONTOUR-A-WB-14AC-A0-INGRESS-EVIDENCE-AND-QUALIFICATION-BOUNDARY-CROSSWALK-2026-10-16.md).
- ASTRA GOLD qualification schema/reference architecture/governance contract establish internal evidence integrity, exact-SHA binding, freshness in qualification scope, independent A3 verification and fail-closed handling. They do not supply the accepted Jarvis-facing A0 API/issuer/admission/result contract or named acceptance authority.
- Executor matrix docs/main wording drift is documented, not integrated. No owner option was selected; WB-14AA remains PROPOSED / NOT ACCEPTED / NOT FROZEN / NOT IMPLEMENTED.


## WB-14AD — A0 ingress governance request (2026-10-16)

- Request: [WB-14AD ASTRA A0 Ingress Governance Request](MEDIAHUB-CONTOUR-A-WB-14AD-A0-INGRESS-GOVERNANCE-REQUEST-2026-10-16.md).
- This is a prepared request, not an owner decision or named assignment. It asks for accountable contract/security/lifecycle owners and confirmation of the approval workflow; no technical option is selected.
- D-ING-01…04, D-ING-05a/05b and D-ING-06 remain OPEN. Keep A0-ING-01…09 proposal-local. DEC-DEV-02 Option C remains OWNER-APPROVED; not reopened.
