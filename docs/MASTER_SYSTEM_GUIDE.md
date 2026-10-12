# MediaHub OS — единый мастер-гайд распределённой мультиагентной системы

**Версия:** 1.1 · **Аудит и пересмотр архитектуры:** 12 октября 2026 года  
**Статус:** мастер-архитектура системы целиком; набор выбранных open-source компонентов требует поэтапной qualification. Текущая реализация Astra Gold и межузловой runtime **не квалифицированы**.

> Правило достоверности: «Проверено» означает, что сведения подтверждены чтением исходников/состояния подключённых узлов; «Цель» — согласованная целевая архитектура; «Кандидат» — внешний компонент, не внедрённый до admission и свежих тестов. Документ или health endpoint не доказывает сквозную работоспособность.

## Архитектура системы целиком: два раздельных контура

Главное решение: проектируется **вся мультиагентная система MediaHub OS**, а не расширение текущей Astra. Astra Gold — подсистема автономной инженерной разработки и квалификации. Jarvis — один из пользовательских фасадов. Ни Astra, ни Jarvis не должны сами становиться универсальной властью над продуктом, клиентскими данными и правами.

| Контур | Железо | Функция | Граница |
|---|---|---|---|
| **MediaHub Product / Edge Runtime** | Первый продуктовый прототип — существующий Mac mini M2 8 GB на объекте заказчика | Пользовательские функции MediaHub, UI, Jarvis/voice, локальные действия, устройства и медиа-интеграции | После передачи заказчику не является development server. Не содержит developer credentials и не входит в постоянную очередь dev workers |
| **Multi-Agent Development Plane** | Покупаемый Mac Pro — dev host №1; Mac mini 2011/Linux/целевые 16 GB — dev host №2 | Исследование GitHub, планирование, архитектура, изолированные implementation workers, тестирование, security review, сборки, документация, evidence и release preparation | Ветки, sandbox и секреты dev-контура изолированы от клиентской среды. Начальный физический лимит — два development hosts |
| **Будущий GPU/Video Compute Pool** | Отдельный видеосервер с мощным GPU | Большие модели, vision, batch inference, видеоаналитика/transcoding | Дополнительный worker pool, не обязательный для первой версии; не владеет product state и не является центральным контроллером |
| **Текущая test lab** | mh-dev-01, mh-dev-02 и M2 в текущем лабораторном контексте | Совместимость, PoC, регрессии и сбор evidence до покупки целевых серверов | Временная конфигурация, не production topology. mh-dev-01 сейчас заполнен на 100%; M2 должен быть выведен из dev pool после передачи клиенту |
| **Общие контракты** | Versioned schemas, API, component registry, model/tool adapters | Стабильные интерфейсы, task/result schemas, capabilities, identity и evidence metadata | Код и протоколы могут быть общими; credentials, customer data и authority не общие |

### Целевая логическая схема

    PRODUCT / CUSTOMER SITE
    MediaHub UI / iOS / Jarvis voice + HUD
                  |
          authenticated API
                  |
    MediaHub Product Core
      - authentication and authorization
      - Product Domain State Authority
      - policy and capability enforcement
      - local deterministic/degraded operation
      - product workflows and integrations
                  |
       approved workflow/tool requests
                  |
    Agent Runtime + model/tool adapters
      - dynamic planner and specialist workers
      - local inference when allowed and capable
      - approved cloud routes under explicit policy
      - MCP tools behind permission broker
      - output validation, audit and human approvals

    ENGINEERING SITE
    task intake -> repo scout -> architecture/plan
                      |
               component admission
                      |
         isolated workers: Mac Pro + Linux Mac mini
                      |
           test / security / independent review
                      |
          exact-SHA evidence -> human release gate

    FUTURE GPU / VIDEO POOL
    scoped workload -> isolated compute worker -> validated artifacts

### Обязательное разделение полномочий

В текущих ASTRA-документах A0-ASTRA описан одновременно как координатор инженерной разработки и как MediaHub State Authority. Это конфликт целевой архитектуры: пользовательский продукт и инженерный контроллер должны иметь разные state/credential/authorization boundaries. Мастер-гайд фиксирует целевое решение, но сам по себе не мигрирует код и канонические контракты.

- **MediaHub Product State Authority** — единственная authority для canonical domain mutations продукта. Все изменения проходят authentication, policy/capability checks и command/consumer contract.
- **A0-ASTRA Development Coordinator** — только инженерные задачи, workspaces, leases, evidence reconciliation и квалификация кода.
- **Workflow engine** — lifecycle, timer/retry/resume и worker dispatch; workflow history не является product-domain truth.
- **Agent/model/executor/provider/tool/transport** — не получают State Authority по факту регистрации или успешного вызова.
- **Человек** — окончательное решение по архитектуре, безопасности, хранению данных и production launch.

Нужно оформить ADR и согласованно обновить governance contract, schemas, tests, queue/workflow manifests и component registry. Текущий MH-03 помечает физическую persistence как неразрешённую. Поэтому нельзя молча ввести PostgreSQL/pgvector как canonical product store или объявить внутреннюю БД workflow engine источником product state. Сначала отдельно утвердить политику хранения product data, engineering task metadata, agent memory и evidence.

### Роли — это capabilities, а не 26 постоянных ботов

Каталог ролей может быть широким, но процессы запускаются динамически под конкретную задачу. Количество логических ролей не равно количеству постоянно работающих агентов и не задаёт concurrency.

| Роль | Работа | Ограничение |
|---|---|---|
| Intake / Dispatcher | Task ID, scope, priority, deadline, privacy/risk tier, idempotency key | Не расширяет запрос сам |
| Planner / Coordinator | Декомпозиция, зависимости, acceptance criteria, ownership файлов | Не исполняет скрытые side effects |
| Repository Scout | GitHub search, official docs, releases, licenses, CI, tests, issues, advisories | Не принимает README или stars за доказательство надёжности |
| System / Domain Architect | Контракты, ADR, state/authority and data boundaries | Архитектурное предложение требует review |
| Component Integrator | Переиспользование зрелых блоков и тонкие adapters | Не переписывает существующую библиотеку без причины |
| Specialist Implementer | API, UI/iOS, tools/MCP, models, voice, media, infra | Только bounded scope, sandbox и минимум прав |
| QA / Evaluation | Unit/contract/integration/e2e, performance, model/tool evaluations | Не сертифицирует собственную реализацию как независимый A3 |
| Security / Supply Chain | Threat model, permissions, secrets, dependency/SBOM/provenance, prompt-injection/tool abuse | Не меняет и не подменяет evidence |
| Independent Reviewer | Независимый diff/test/security review на exact SHA | Не совпадает с исполнителем того же изменения |
| Memory / Knowledge Curator | Verified facts, sources, version/time, privacy/retention, deduplication | Не является product State Authority и не хранит secrets |
| Integration / Release Engineer | Reconciliation, reproducible artifact, SBOM/signature/scan, rollback | Protected writes/release только по human gate |
| Documentation / UX | Master guide, onboarding, interface contracts, user errors, accessibility | Не выдаёт target design за подтверждённый runtime |

Роль не закрепляется за одной моделью: executor выбирается из admitted capability registry. Skills — библиотека процедур, не полномочия и не отдельные постоянно запущенные агенты.

## Repository-first политика: сначала найденное, потом написанное

Перед каждой значимой разработкой обязательна проверка: существует ли зрелый SDK, repo, reference implementation, schema или tool, который закрывает задачу. Требование относится и к пользовательскому продукту, и к developer plane. Не начинать самостоятельную реализацию лишь потому, что так проще расширить текущую Astra.

### Admission-процесс

1. Описать capability contract, API/input-output schemas, acceptance tests, data/privacy constraints и integration boundary.
2. Провести GitHub search и поиск официальной документации; обычно собрать минимум три кандидата, если рынок содержит альтернативы. Если кандидатов меньше — зафиксировать поисковые запросы и причину.
3. Проверить не только README: upstream owner, exact release/commit, license и embedded licenses, release cadence, CI/tests, open issues/advisories, lockfiles, supported OS/architecture, dependencies, auth/data flow, offline behavior, resource profile и failure/recovery model.
4. Применить hard gates: подтверждённая upstream identity, совместимая лицензия, приемлемая security posture, управляемые зависимости, изоляция и timeout/cancel для side effects, совместимость с целевым железом.
5. Pin source commit/release, packages/checksums, configuration, SBOM, license obligations, review date, owner, rollback и test evidence.
6. Выполнить изолированный PoC без клиентских данных и production secrets; сохранить команды, точную версию/SHA, результаты и замер ресурсов.
7. Если годится — интегрировать узкий adapter или часть компонента; не импортировать лишние подсистемы и не форкать весь проект без необходимости.
8. Если готового подходящего блока нет — показать кандидатов и причины отказа, только после этого создавать минимальный replacement с contract tests.
9. На major update, критическом advisory или смене целевого железа повторять admission.

### Оценка кандидата из 100 баллов

- соответствие capability/контракту — 25;
- зрелость, release cadence, поддержка maintainers — 20;
- тесты, CI, воспроизводимость, recovery — 15;
- security, provenance, dependency hygiene — 15;
- совместимость macOS/Apple Silicon и Linux x86_64/старого CPU — 10;
- license and commercial redistribution — 10;
- runtime footprint, latency, resource observability — 5.

80–100 — допуск к PoC/admission; 65–79 — ограниченный эксперимент; ниже 65 — обычно reject. Score не отменяет hard gates. Stars/install counts — вторичный сигнал, не доказательство production stability.

### GitHub shortlist по функциям (кандидаты, не auto-install)

| Функция | Репозитории | Решение |
|---|---|---|
| Stateful agent graph | [LangGraph](https://github.com/langchain-ai/langgraph) | Ведущий Python-first PoC: MIT, stateful graph, checkpoints, human-in-the-loop. Допустить после теста provider compatibility and persistence adapter |
| Альтернатива agent framework | [Microsoft Agent Framework](https://github.com/microsoft/agent-framework) | MIT, Python/.NET, graph workflows и checkpointing. Рассматривать при фактической потребности в .NET/Microsoft integration; не использовать параллельно с LangGraph для одной и той же оркестрации |
| Durable cross-node workflow | [Temporal](https://github.com/temporalio/temporal) | Ведущий PoC для retries, timers, resume и worker task queues. Это lifecycle workflow, не LLM reasoning graph и не Product State Authority |
| Messaging/pub-sub | [NATS Server/JetStream](https://github.com/nats-io/nats-server) | Отложить, пока нет доказанной потребности в fan-out/pub-sub/replay сверх durable workflow queues |
| Tools protocol | [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk) | MIT, стандартизирует tools/resources/prompts. Permission broker и authorization policy всё равно отдельные |
| Browser | [Playwright](https://github.com/microsoft/playwright) + [Playwright MCP](https://github.com/microsoft/playwright-mcp) | PoC для e2e/browser tools; изолированный browser profile/domain allowlist. Playwright MCP сам по себе не security boundary |
| Multi-provider gateway | [LiteLLM](https://github.com/BerriAI/litellm) | Сравнить с существующими provider schemas и native adapters; зафиксировать версию/лицензию/footprint. Выбрать максимум один shared gateway |
| Local inference | [Ollama](https://github.com/ollama/ollama) | Уже используется в test lab; не считать общим production runtime без exact model identity/capability tests |
| Alternative inference | [llama.cpp](https://github.com/ggml-org/llama.cpp) | MIT, Apple Silicon/x86/multiple backends; вводить только если benchmark выявил конкретный gap |
| Coding executors | [OpenHands](https://github.com/All-Hands-AI/OpenHands), [SWE-agent](https://github.com/SWE-agent/SWE-agent), [Aider](https://github.com/Aider-AI/aider) | Только кандидатные execution surfaces; сравнить sandbox, license, tests, task success and resource use. Не являются system-wide orchestrators |
| Memory layer | [Mem0](https://github.com/mem0ai/mem0) | Optional PoC после privacy/persistence ADR; memory не является canonical domain state |
| Vector retrieval | [PostgreSQL](https://github.com/postgres/postgres) + [pgvector](https://github.com/pgvector/pgvector) | Target-gated: persistence needs explicit architecture approval under current MH-03 constraint |
| Offline STT | [whisper.cpp](https://github.com/ggml-org/whisper.cpp), [sherpa-onnx](https://github.com/k2-fsa/sherpa-onnx) | MIT/Apache-2.0 candidates; compare accuracy, latency, RAM and offline quality on M2 and target CPU |
| TTS | [Piper upstream](https://github.com/OHF-Voice/piper1-gpl) | Not default: GPL-3.0-or-later and upstream alpha status require licensing and packaging review |
| Media processing | [FFmpeg](https://github.com/FFmpeg/FFmpeg) | Reuse existing toolbox; pin build/features and review codecs/licenses actually distributed |
| Observability | [OpenTelemetry](https://opentelemetry.io/docs/), Prometheus, Grafana if needed | Keep standard telemetry stack; traces/metrics never mutate state or authorize |
| Supply chain/secrets | [SOPS](https://github.com/getsops/sops) + [age](https://github.com/FiloSottile/age), [Syft](https://github.com/anchore/syft), [Cosign](https://github.com/sigstore/cosign), [Trivy](https://github.com/aquasecurity/trivy) | Keep selected foundation with explicit policy and CI gates |

Microsoft marks [AutoGen](https://github.com/microsoft/autogen) as maintenance-mode and recommends new users start with Microsoft Agent Framework. Thus AutoGen should not be picked for a new core just because older tutorial material is popular.

### Рекомендуемая схема оркестрации

- MediaHub API + policy + Product State Authority отвечает за разрешённые продуктовые mutations.
- **Один** durable workflow engine (Temporal — ведущий PoC) может отвечать за длительные cross-node tasks, retries/timers/resume/worker dispatch.
- **Один** graph framework (LangGraph — ведущий Python-first PoC) может отвечать за сложный reasoning/agent delegation внутри bounded workflow activity. Простой шаг должен остаться обычной typed function.
- Model gateway — один выбранный adapter за существующими provider/inference contracts. LiteLLM сравнить с native adapters; FreeLLMAPI не допущен, пока не определены конкретный upstream repository, commit, license and routing behavior.
- MCP предоставляет интерфейс tools, но не принимает authorization decisions.
- OpenTelemetry/Prometheus показывают traces, model/tool timings, errors and resource metrics.

Это preferred architecture PoC, а не утверждение, что Temporal/LangGraph/LiteLLM уже установлены. До переписывания текущего queue нужно сравнить existing implementation и кандидатов по одинаковому acceptance suite. Если существующий компонент проходит reliability/security/maintenance gates — повторно использовать; если нет — менять только конкретно провалившийся слой.

## 1. Назначение и итог аудита

MediaHub OS — вся продуктовая и системная платформа. Мультиагентная система — универсальный слой планирования, исполнения, проверки и координации разных типов задач. Jarvis — один из пользовательских фасадов (голос, диалог, память, HUD), а ASTRA — подсистема автономной разработки/квалификации кода. Ни Jarvis, ни ASTRA не должны подменять доменную State Authority продукта.

Цель — целостная распределённая мультиагентная система: единый защищённый API, workflow/task control plane, динамические роли и worker capabilities, реестр компонентов и моделей, локальные/облачные model adapters, память с источниками и политикой хранения, MCP/инструменты за permission broker, продуктовые интеграции, voice/UI, observability, аудит, отказоустойчивость и управляемое развёртывание на разных аппаратных профилях.

**Фактическое состояние на 12.10.2026:** подключены два Linux-узла и Mac mini M2. Mac Pro, MacBook и GPU host не появились среди активных Desktop Commander устройств; их характеристики/доступность неизвестны. Корневой диск mh-dev-01 заполнен на 100% (0 свободных блоков, inode usage 57%); read-only scan нашёл около 2.8 GiB в /var/log и 2.5 GiB systemd journal, но очистка не выполнялась, чтобы не потерять доказательства. На mh-dev-02 жив API Ollama, но heartbeat контроллера последний раз менялся 7 октября. Существующие transport/provider evidence датированы концом сентября и содержат BLOCKED/NOT_PASS. На Mac mini прошла валидация 25 контрактных файлов/9 envelope contracts и пять тестов топологии; другие выбранные unittest-модули не импортировались из-за отсутствующего PyYAML, pytest не установлен. Полная qualification не подтверждена.

### Целевая аппаратная конфигурация — решение пользователя от 12.10.2026

Это архитектура **под будущее железо**, а не утверждение о наличии всех устройств сегодня. Рабочая система планируется к развёртыванию ближе к концу октября 2026 года, после покупки и фактической инвентаризации целевого компьютера.

| Целевой узел | Роль в итоговой схеме | Этап и ограничения |
|---|---|---|
| **Покупаемый Mac Pro** | Основной целевой сервер MediaHub и один из двух серверов разработки ASTRA; центральная control/API-поверхность, координация Jarvis, состояние задач, маршрутизация и evidence после квалификации компонентов | До покупки неизвестны точная модель/поколение, CPU, RAM, GPU, SSD, ОС и сеть. Выбор моделей и worker capacity окончательно фиксировать только после проверки конфигурации. Не считать Alamo или контроллер развёрнутыми заранее |
| **Mac mini 2011, Linux, целевые 16 GB RAM** | Второй сервер разработки / Linux executor, тестовая совместимость и ограниченные фоновые задачи | 16 GB — целевая конфигурация пользователя. Apple официально указывает заводские комплектации до 8 GB, но OWC сообщала о верифицированной установке 16 GB (2×8 GB); фактический объём и стабильность нужно проверить на конкретном экземпляре до ввода в эксплуатацию. Первый запуск Linux выполнять по Ethernet, проверить firmware/network/SSD, стабильность памяти и автоматическое восстановление после перезагрузки |
| **Mac mini M2 Виктора, 8 GB** | Первый работающий прототип продукта MediaHub; среда функциональной проверки, staging/demo и проверки UX | Не включать в постоянный парк серверов разработки и не считать постоянной Astra Gold executor lane после перехода к целевому железу. На этапе разработки разрешены временные тесты, но продуктовый прототип должен быть отделён от очереди и полномочий дев-серверов |
| **Будущий видеосервер с мощным GPU** | Дополнительный compute/inference pool для крупных моделей, обработки видео/изображений и иных GPU-задач | Будущее расширение, не prerequisite для базового старта. Его GPU/VRAM/RAM/storage/driver/network/API/модель нужно квалифицировать отдельно. По умолчанию это compute worker, не сервер разработки и не State Authority |
| MacBook / другие UI-клиенты | Клиентская поверхность при необходимости | Не являются обязательными центральными серверными узлами |

**Разделение фаз:** (1) текущие машины — test lab; (2) Mac mini M2 — первый прототип MediaHub; (3) после закупки — основной целевой узел Mac Pro + отдельный Linux Mac mini 2011 для разработки; (4) позднее — GPU/video server. Текущая реализация Astra queue пока содержит старое сопоставление трёх тестовых lane, включая M2. Перед целевым запуском оно должно быть перепривязано к конечным узлам и подтверждено тестами. Начальная плановая ёмкость — два физических development hosts; concurrency нельзя оставлять равным трём только потому, что тестовый контроллер так сконфигурирован. Третья одновременная задача допускается лишь после отдельного обоснования изолированных логических worker lanes и capacity-тестов Mac Pro или явно квалифицированного дополнительного executor.

### Ключевые выводы

1. Сильная сторона — формализованные роли A0/A1/A2/A3, fail-closed gate, обязательные evidence и человеческий запуск.
2. Первоочередной блокер — заполненный диск mh-dev-01. Не запускать там сборки, установку пакетов или широкие тесты и не удалять файлы до read-only анализа и сохранения dirty worktrees.
3. Evidence устарели и не доказывают состояние сегодня.
4. Один компонентный документ говорит о двух параллельных claims, а канонические контракты, reference architecture и тесты — о трёх. Документацию следует согласовать.
5. Read-only ollama show на mh-dev-02 подтвердил, что qwen2.5-coder:7b и claude-sonnet-4-6:latest указывают на один blob sha256:60e05f2100071479f596b964f89f510f057ce397ea22f2833a0cfe029bfc2463 с архитектурой qwen2, 7.6B и Q4_K_M. Следовательно, метка claude-sonnet-4-6:latest здесь alias той же Qwen2 модели, а не отдельной Claude Sonnet. Alias следует исключить из автоматической маршрутизации до отдельного исправления registry; модель не удалять.
6. FreeLLMAPI не имеет подтверждённого точного upstream/commit. В сети есть несколько одноимённых проектов; не подключать найденный случайный репозиторий.
7. Jarvis из видео — полезный референс голосового HUD, но его базовая реализация использует Claude Code/Agent SDK и облачную Anthropic модель. Это не готовый Alamo/FCC/local-only маршрут.

## 2. Авторитет и границы ответственности

| Компонент | Роль | Ограничения |
|---|---|---|
| Человек | Финальная архитектурная, безопасностная и production authority | Только человек разрешает запуск G11 |
| A0-ASTRA (developer plane) | Координация инженерных задач, queue/claims/leases, evidence reconciliation и qualification | Не является State Authority клиентского MediaHub продукта и не подменяет product-domain authority |
| A1 | Архитектура и контракты | Не исполняет роль независимого A3 |
| A2 | Ограниченная реализация | Не сертифицирует собственную работу |
| A3 | Независимая проверка на exact SHA | Должен быть независим от исполнителя |
| MediaHub Product State Authority | Единственная authority для canonical domain mutations продукта | Принимает команды только после authentication, policy, capability и consumer-contract validation; persistence требует отдельного ADR |
| Jarvis | Один пользовательский фасад: голос, HUD, память/контекст и сбор задачи | Не является orchestration authority, permission broker или State Authority |
| FCC / OmniRoute | Транспорт/интеграция исполнителей | Не владеют состоянием MediaHub |
| FreeLLMAPI / provider gateways | Маршрутизация к моделям после admission | Не гарантируют бесплатную ёмкость и не получают полномочий |
| Alamo / Ollama | Инференс локальных моделей | Не принимают решения о разрешениях |
| Executors | Выполнение ограниченной задачи | Только executor authority |
| GitHub control bus | Код, desired state, журналы/evidence transport | В публичном репозитории запрещены конфиденциальные данные |

Модель предлагает; исполнитель выполняет; State Authority проверяет и фиксирует допустимое изменение; A3 независимо проверяет; человек утверждает запуск. Сетевая доступность или членство в mesh/VPN не означает разрешения менять состояние.

## 3. Целевая топология

Топология делится на зоны. (1) Development plane: покупаемый Mac Pro и Mac mini 2011/Linux — два dev hosts; на Mac Pro после commissioning можно разместить central engineering API/workflow runtime. (2) Product/edge plane: существующий M2 работает у заказчика как первый отдельный продуктовый прототип и по умолчанию не зависит от developer control plane. (3) Future compute plane: GPU/video server как capability worker. Product API, domain State Authority и developer ASTRA API имеют отдельные identities, credentials и data boundaries. Европейский VPS — только key registration/management; не proxy для обычного model/data traffic.

Это целевая схема, не утверждение о текущем деплое. Фактически доступны только mh-dev-01, mh-dev-02 и Voktors-Mini.Dlink. Mac Pro и отдельный Mac mini 2011/Linux ещё предстоит купить/ввести в целевую эксплуатацию. M2 после ввода продукта на объекте выводится из dev worker pool. GPU host — позднее расширение.

### Плоскости системы

- **Product authority plane:** user/device/service identity → authentication → policy/capability → MediaHub Product State Authority.
- **Engineering authority plane:** человек, A0-ASTRA, A1/A2/A3; права действуют только в dev/qualification scope.
- **Workflow/control plane:** приём задания, декомпозиция, зависимости, durable lifecycle, queue/claims/leases, heartbeat, fencing, duplicate suppression, отмена, replay и reconciliation. Один durable scheduler выбирается после PoC; не поддерживать две competing queues как равноправных источника правды.
- **Execution plane:** product agent workers и отдельные developer executors (Claude Code, Codex и другие допущенные инструменты) в изолированных рабочих областях и credential scopes.
- **Model/provider plane:** Alamo/Ollama и разрешённые облачные модели через адаптеры.
- **Transport plane:** GitHub Transport, FCC, OmniRoute и частная сеть; transport не авторитетен для состояния MediaHub.
- **Evidence plane:** неизменяемые результаты с source SHA, provider/executor identity, round, exit status, timestamp, timeout, workspace и digest.
- **Integration/tool plane:** MCP, browser automation, почта, календарь и внешние API только через permission broker.
- **Observability plane:** OpenTelemetry/Prometheus; telemetry не меняет доменное состояние и не даёт прав.

## 4. Фактическая аппаратная инвентаризация

| Узел | Подтверждённые характеристики | Вывод |
|---|---|---|
| mh-dev-01 | Ubuntu x86_64; Intel Core i7-2635QM 2.00 GHz, 8 CPU, около 7.7 GiB RAM; root disk 109 GiB | **P0:** root filesystem 100%, 0 free. Не писать, не устанавливать и не очищать без плана сохранения данных |
| mh-dev-02 | Ubuntu x86_64; показан тот же класс CPU/8 CPU, около 15 GiB RAM; disk 61 GiB, 14 GiB свободно; Python 3.12.3, Node 22.23.3, Ollama 0.34.4 | Лёгкое исполнение, координация и пробы локального API; не доказанный GPU worker |
| Voktors-Mini.Dlink | Mac mini M2, Mac14,3, ARM64, 8 GB RAM; Data volume 228 GiB, около 60 GiB свободно; Python 3.14.8, Node 22.23.3, Ollama | Первый прототип MediaHub; на этапе разработки также используется для тестов. Не оставлять постоянной dev/Astra lane после перехода на целевое оборудование |
| Mac Pro (планируемый к покупке) | Основной целевой MediaHub server и development host №1; после закупки будет центральной API/control-поверхностью | Пока отсутствует в текущем test lab. Модель/конфигурация/health не известны; проверить при покупке и до выбора модели/нагрузки |
| Mac mini 2011 / Linux / 16 GB (планируемый development host №2) | Linux executor для разработки и совместимости | Целевой объём RAM дан пользователем; проверить фактическое обнаружение 16 GB на конкретном экземпляре. Apple заявляла штатную конфигурацию до 8 GB, сторонний OWC тестировал 16 GB для Mid-2011. Сначала Ethernet и базовая Linux/firmware qualification |
| MacBook / UI clients | Клиентская поверхность при необходимости | Не является обязательным сервером целевой топологии |
| Будущий GPU/video server | Дополнительный compute pool для крупных моделей, vision/video processing | Будущее расширение; не нужен для первого запуска базовой архитектуры. Не давать ему State Authority |
| VPS | Изолированный key registration workflow | Не использовать как inference proxy или для обхода правил провайдеров |

На mh-dev-02 Ollama list показал qwen2.5-coder:1.5b (986 MB), qwen2.5-coder:3b (1.9 GB), qwen2.5-coder:7b (4.7 GB) и alias claude-sonnet-4-6:latest (4.7 GB), причём две последние метки имели один ID. На Mac mini M2-прототипе найдены qwen2.5-coder:1.5b, qwen2.5-coder:3b и qwen3:4b. Не считать модельные метки доказательством идентичности; сохранять manifest/digest и исключить сомнительный alias из автоматического выбора до read-only проверки. Не удалять модели автоматически.

Для GPU-host нужны подтверждённые GPU/VRAM, RAM, SSD, driver/runtime, checkpoint, quantization, context length, concurrency, latency/throughput и thermal budget. Между компьютерами RAM/VRAM не складываются автоматически. Большую модель размещать на одном подходящем хосте либо использовать проверенный multi-GPU runtime. Mac mini 2011 с целевыми 16 GB RAM — executor/compatibility Linux host, не крупный LLM/GPU сервер.

## 5. Распределение задач

| Узел | Базовая роль | Не назначать без qualification |
|---|---|---|
| Mac Pro (планируемый) | Development host №1; central engineering API/workflow runtime, repo research, build/test/evidence. Может предоставлять dev-model services после commissioning, но не является обязательной онлайн-зависимостью customer M2 prototype | Нагрузка и число процессов/claims только после покупки, профилирования и изоляционных тестов; не выдавать права developer executor автоматически всем system services |
| mh-dev-01 | Claude lane для bounded coding/test jobs после освобождения диска | Любая запись при нуле свободного места, очистка dirty worktrees |
| mh-dev-02 | Claude lane, health probes, Ollama/API tests | Большой inference, cloud fallback в LOCAL_ONLY, квалификация по одному каталогу |
| Mac mini 2011 / Linux / 16 GB (план) | Development host №2: Linux executor, compatibility tests, bounded background jobs | Не использовать как GPU inference host; 16 GB и Linux drivers проверяются на реальном экземпляре |
| Mac mini M2 | Первый MediaHub product prototype на объекте заказчика: product/edge runtime, UX и acceptance feedback | После передачи заказчику не входит в постоянную очередь dev servers; клиентские данные/credentials не смешиваются с dev state |
| Будущий GPU/video server | Отдельный GPU worker pool для крупных моделей и медиаобработки | Не включать в обязательный путь базовых команд до развёртывания; секреты контроллера и direct canonical-state writes запрещены |
| MacBook / other client | UI/approval surface при необходимости | Не считать developer lane или server без отдельного решения |
| VPS | Управление регистрацией/отзывом ключей | Model proxy, traffic relay, quota bypass |

Планировщик учитывает privacy tier, capability fit, ресурсы, deadline, latency/cost/quota, isolation и lease. Результат фиксирует фактические provider/model IDs и причину выбора. Скрытая смена провайдера запрещена.

## 6. Jarvis: референс и целевой функционал

Три видеозаписи показывают идеи аппаратного «тела», UI/обвязки, инструментов, памяти, голоса, интеграций и старта одной задачи. Полная аудиорасшифровка не выполнена; неразборчивые шаги не восстанавливаются по догадке. Один ролик относится к настройке **Claude Code**, а не доказывает интеграцию Claude Desktop с Alamo.

Видеореференс: https://github.com/adewaskar/jarvis (MIT). Это браузерный HUD на React/Vite/Three.js и Node WebSocket bridge. Bridge запускает Claude Agent SDK/Claude Code headless, читает MCP servers из локальной конфигурации Claude Code и использует существующий Claude login. README указывает, что модель выполняется в инфраструктуре Anthropic. Репозиторий подходит как UI/voice reference, но не как готовая local-only реализация. До форка: pinned commit, dependency/SBOM/license/security review и отдельный adapter.

### Целевой функционал (требует реализации и тестов)

- Голос и текст: push-to-talk, опциональный wake word после privacy review, VAD/STT/TTS, прерывание/отмена.
- HUD: task ID, этап, executor/provider/model, permissions, прогресс, результат, ошибки и ссылки на diff/evidence.
- Планирование: decomposed task, dependencies, queue, timeout, cancel, bounded retry, idempotency.
- Инструменты: search/browser/GitHub/file workspace; почта, календарь, телефон и внешние API только отдельными scoped connectors.
- Память: профиль и настройки, проектные факты с источником/датой, session summaries, task history/evidence, privacy class, retention и deletion. Свободный state.md не является авторитетным runtime state без schema/validation.
- Безопасность: default-deny; tool allowlist; permission broker; sandbox; human approval для отправки сообщений, deploy, заказов и других необратимых действий.
- Статусы по evidence: SUCCEEDED, FAILED, BLOCKED, CANCELLED, NEEDS_APPROVAL.

Поток продукта: Browser/Native UI → authenticated MediaHub API → product policy/domain command path → workflow engine for long-running jobs → agent/tool/model adapters → result validator → approved product command → Product State Authority → audit/evidence/UI. Engineering flow отдельный: issue/task → A0 coordinator → isolated worker → test/review/security → evidence и human release gate. Секреты server-side; модель не управляет своими разрешениями и не получает бессрочные credentials.

## 7. Модельный контур

- **Alamo:** целевое обозначение local endpoint; точный model ID, runtime, API, auth, tool calls, streaming и context limits пока не подтверждены.
- **Ollama:** обнаружен на Linux и Mac mini; mh-dev-02 версия 0.34.4, localhost version endpoint отвечает HTTP 200. Это health, не qualification inference.
- **FCC:** обязателен в целевом Claude Code пути; точная версия/конфигурация и e2e совместимость этим аудитом не подтверждены.
- **FreeLLMAPI:** candidate gateway с неустановленной exact upstream identity. Сначала закрепить owner/repo/commit/license/auth/schema/terms/quota, не выбирать одноимённый проект наугад.
- **Codex:** отдельный поддерживаемый auth path; не смешивать с Claude Code/FCC/Alamo.
- **Другие облачные модели:** admission отдельно для каждой provider/model identity.

### Режимы маршрутизатора

| Режим | Политика |
|---|---|
| LOCAL_ONLY | Только проверенный локальный endpoint. При недоступности — fail-closed; облачный fallback запрещён |
| APPROVED_CLOUD | Только явно допущенные providers; fallback только по policy/privacy/terms/quota и видимый в evidence |
| MANUAL | Пользователь задаёт точный provider/model; смена без уведомления запрещена |
| POLICY | Allowlist + capabilities + privacy tier + resources + cost/latency + quota + circuit breaker + reason log |

Для LOCAL_ONLY нужны положительный локальный inference test и отрицательный egress test, доказывающий отсутствие облачных запросов при отказе локального endpoint. OpenAI-compatible API не гарантирует одинаковое tool-calling, streaming, JSON schema или multimodal support. Каждый adapter публикует health/identity/capabilities/infer/timeout/cancel/error mapping/usage/evidence metadata.

Если FreeLLMAPI допускает запуск без auth key, production должен fail-start без аутентификации; bind только loopback/private, authenticated caller, allowlisted upstreams, изолированные credentials, bounded retries, timeout/circuit breaker, redacted logs и реальный upstream provider/model. Бесплатная квота не означает unlimited capacity или SLA.

## 8. Очередь Astra Gold и qualification

В текущем тестовом коде `runtime/mediahub_runtime/autonomous_queue.py` жёстко прописаны три lane: `mh-dev-01`, `mh-dev-02` и `Voktors-Mac-mini.local`, а максимальная параллельность равна трём. Это **текущая тестовая конфигурация**, а не конечная аппаратная схема. По целевому плану два development hosts — покупаемый Mac Pro и Mac mini 2011/Linux; Mac mini M2 является прототипом продукта, а не постоянным dev worker. До развёртывания нужно изменить pool registry, G5 concurrency contract, topology tests, task node IDs и workflow routing на конечные логические ID. Начальная целевая параллельность — не более двух физических hosts; повышать её можно только после отдельного доказательства нескольких независимых sandbox lanes и ресурсного профиля Mac Pro. Будущий GPU/video server относится к AI/медиа compute pool и не становится dev lane автоматически. Claims должны не пересекаться; shared mutable surfaces сериализуются; duplicate controller отклоняется; stale lease требует fencing/recovery; replay идемпотентен.

Пять qualification paths — CODEX_FCC, CLAUDE_FCC, CODEX_OMNIROUTE, CLAUDE_OMNIROUTE и CLAUDE_CODE_DIRECT — это испытательные сочетания executor/transport, не замена трём permanent lanes. Каждый mandatory path должен пройти 23 свежих изолированных успешных раунда.

Evidence: command ID, node, component, executor, provider/model, transport if applicable, source SHA, round, timestamp, exit status, timeout, workspace, verification status, evidence digest. Secrets и authorization tokens запрещены. Историческое evidence не закрывает fresh gate.

- G0 Identity — точные identities/SHA, чистый worktree.
- G1 Boundary — authorization, transport/state/credential boundaries, isolated workspace.
- G2 Control Plane — queue, leases, duplicate suppression, result publication, heartbeat.
- G3 Execution Path — runtime/version, timeout, exit status, schema and marker.
- G4 23-wave — все mandatory rounds свежие, успешные, изолированные.
- G5 Concurrency — на тестовой конфигурации действует старый лимит 3; перед целевым запуском контракт и тесты должны быть переведены на 2 физические development lanes (или на отдельно доказанную модель нескольких изолированных worker lanes), с duplicate-controller rejection.
- G6 Recovery — timeout, executor/transport failure, stale claim, restart, replay, publication recovery.
- G7 Integrated A3 — independent code/contracts/regression/security/concurrency/recovery verification.
- G8 Pre-soak — all paths/recovery/A3 PASS, clean worktree, fresh evidence.
- G9 24H soak — 24 часа без unexplained restart, claim corruption, unresolved failure или authority violation.
- G10 Launch-ready — G0–G9, evidence bundle, rollback target.
- G11 Human launch — только человек, approval привязан к exact SHA/release и rollback.

Missing/stale/conflicting evidence означает BLOCKED. Модель/исполнитель не присваивают себе qualification.

## 9. Проверки и пробелы

**Проверено:** GitHub reference architecture, governance contract, qualification schema, unified system YAML, component scheme/registry/decisions и security boundaries прочитаны. На Mac mini contract validator: PASS, 25 contract files, 9 envelope contracts. Пять topology tests прошли для старой тестовой конфигурации: concurrency=3, три Claude lanes и отсутствие Codex в permanent lanes. Это не подтверждает целевую конфигурацию Mac Pro + Linux Mac mini с M2 как отдельным product prototype; tests нужно обновить после фиксации architecture ADRs. На mh-dev-02 Ollama localhost version endpoint вернул HTTP 200.

**Не пройдено/не запускалось:** pytest отсутствует; PyYAML отсутствует в выбранном Python 3.14 на Mac mini, поэтому governance/repo hygiene/secret hygiene модуль не импортировался. Часть test dependencies отсутствует и на mh-dev-02. Не выполнены сквозной Claude Code→FCC→FreeLLMAPI/Alamo, local-only egress denial, tool-calling, все 23 раунда на mandatory paths, recovery suite, fresh independent A3 и текущий 24H soak. Полный security audit всех runtime/API не заявляется.

Evidence transport/provider от 27.09.2026 показывает BLOCKED/NOT_PASS; qualification JSON от 27.09.2026 содержит BLOCKED_PRE_SOAK. Heartbeat mh-dev-02 старше 24-hour evidence freshness window. Итог текущего engineering controller: **BLOCKED / NOT QUALIFIED**; целевая продуктовая multi-agent architecture описана, но candidate components ещё не прошли PoC/admission.

## 10. Реестр исправлений

| Приоритет | Проблема | Критерий закрытия |
|---|---|---|
| P0 | mh-dev-01 disk 100%, 0 free | Read-only inventory, сохранение dirty/untracked/evidence, согласованный selective cleanup, затем свежие health/runtime checks |
| P1 | Stale mh-dev-02 heartbeat | Один подтверждённый controller per lane, свежие heartbeat/queue evidence по текущему SHA |
| P1 | Один Ollama ID у двух model labels | Сохранить manifest/digest/provenance; quarantine alias до подтверждения |
| P1 | FreeLLMAPI upstream unknown | Exact repo/commit, license/auth/terms, secure bind и adapter tests |
| P1 | Нет Alamo endpoint/e2e FCC route | Identity/schema/auth/health, bounded task, actual provider/model evidence, negative egress test |
| P1 | Целевые Mac Pro и Mac mini 2011 ещё не введены; текущий queue всё ещё назначает третью lane на M2 | До целевого развёртывания привязать роли к закупленным узлам, проверить Linux/RAM/network и обновить registry/schema/G5/tests/tasks; M2 оставить prototype-only |
| P1 | Jarvis reference defaults to Anthropic cloud | Adapter, local-only hard boundary, MCP allowlist, broker и negative tests |
| P1 | Тестовые зависимости неполны | Pinned isolated venv/lockfile и повтор contract/unit/security suites |
| P2 | Документы и тестовый код описывают три постоянные dev lanes, включая M2, а целевая конфигурация — два development hosts и отдельный M2 prototype | До commissioning сделать controlled migration и reconciliation; не выдавать тестовые hosts за целевые |
| P2 | Корневой README почти пустой | Сослаться на master guide, safe setup/tests/security |

Не выполнялись очистка диска, удаление моделей, restart controller и перезапись dirty worktrees: это может уничтожить данные.

## 11. План реализации

**Фаза A — стабилизация:** остановить writes на mh-dev-01; сохранить изменённые файлы; подтвердить один controller per lane, source SHA/worktree и fresh heartbeat; read-only расследовать модельный ID conflict.

**Фаза B — маршрутизация:** pin версии Claude Code/FCC/FreeLLMAPI/Ollama и Alamo variant; протестировать каждый переход отдельно; non-mutating probe до bounded repo task; проверить LOCAL_ONLY с egress denial; испытать 429/quota, outage, malformed response, timeout, cancellation, idempotency, stale claim и recovery.

**Фаза C — Jarvis:** закрепить MIT upstream commit, review SBOM/dependencies/license/security; authenticated API; explicit MCP allowlist; permission broker, sandbox, approvals для необратимых действий; voice/privacy, task ID, cancel/reconnect; versioned memory с sources, retention и deletion.

**Фаза D — qualification:** после закупки оборудования зафиксировать exact hardware/runtime/SHA, 23 rounds на mandatory paths, target lane registry, initial concurrency ≤2 (или утверждённые и измеренные extra logical lanes), recovery tests, независимый A3, reconciliation, свежий pre-soak, полные 24H и human G11 approval с rollback.

## 12. Статусы компонентов

- **Selected/current foundation:** Protobuf/gRPC, OpenTelemetry/Prometheus, SOPS+age, Syft/Cosign/Trivy, FFmpeg в определённых границах.
- **Target-gated:** PostgreSQL/pgvector, Home Assistant Core, IfcOpenShell/web-ifc, PaddleOCR/OpenCV, ONNX Runtime/llama.cpp, restic, RAUC — включать только после capability/security/performance/recovery gate.
- **Future-gated/reference:** NATS/JetStream, etcd, OpenBao, Kubernetes, Temporal, Caddy, Jellyfin, SeaweedFS, n8n и другие — при доказанном функциональном разрыве.
- **Candidate/not proven:** FreeLLMAPI, free-coding-models, OpenOPC, OpenFlux, browser/coding tools и model variants — admission нужен конкретному проекту/version/adapter.

MediaHub сохраняет domain model, State Authority, permission policy, lifecycle, recovery и release authority. Сторонний компонент не становится вторым центром управления.

## 13. Безопасность и диагностика

Секреты не включать в Git, prompts, unrestricted logs, screenshots или evidence; поддерживать rotation/revocation и least privilege. Не публиковать Ollama/FCC/Jarvis/control endpoints в Internet без service authentication, TLS/ACL и negative tests. Сайты, письма, issues и MCP результаты — недоверенный ввод; prompt injection не расширяет permissions. Browser sessions изолированы; cookies/tokens исключены из evidence. User nodes получают только минимальные non-sensitive opted-in jobs в sandbox, с quotas, timeout, result verification, quarantine/revocation. Публичный репозиторий — только код и очищенные evidence.

Безопасные диагностические команды для Linux:

~~~bash
hostname
uname -a
lscpu | grep -E 'Model name|CPU\\(s\\):|Architecture:' | head
free -h
df -h /
git -C /path/to/mediahub-os status --short --branch
git -C /path/to/mediahub-os rev-parse HEAD
ollama --version
ollama list
curl --fail --silent --show-error --max-time 2 http://127.0.0.1:11434/api/version
~~~

Тесты запускаются в pinned isolated environment и controlled worktree. Не выводить .env, .claude.json, keychain или runner secrets. На disk-full host не устанавливать dependencies. Jarvis quick-start — только в isolated prototype, Node >=20, pinned commit, write-tools off и local-only bridge; не публиковать bridge в LAN/Internet без security design.

## 14. Источники

Внешние проекты меняются; перед внедрением нужно pin exact commit/release.

1. MediaHub distributed architecture: https://github.com/VlDMlNSh/mediahub-os/blob/main/architecture/MEDIAHUB-DISTRIBUTED-AI-INFRASTRUCTURE.md
2. ASTRA GOLD reference: https://github.com/VlDMlNSh/mediahub-os/blob/main/architecture/ASTRA-GOLD-REFERENCE-ARCHITECTURE.md
3. Governance contract: https://github.com/VlDMlNSh/mediahub-os/blob/main/architecture/ASTRA-GOLD-GOVERNANCE-CONTRACT.yaml
4. Qualification schema: https://github.com/VlDMlNSh/mediahub-os/blob/main/architecture/ASTRA-GOLD-QUALIFICATION-LAUNCH-SCHEMA.yaml
5. Unified system: https://github.com/VlDMlNSh/mediahub-os/blob/main/architecture/ASTRA-GOLD-UNIFIED-AUTONOMOUS-DEVELOPMENT-SYSTEM.yaml
6. Component scheme/registry/decisions: https://github.com/VlDMlNSh/mediahub-os/blob/main/architecture/ASTRA-GOLD-COMPLETE-COMPONENT-SCHEME.md · https://github.com/VlDMlNSh/mediahub-os/blob/main/components/COMPONENT-REGISTRY.yaml · https://github.com/VlDMlNSh/mediahub-os/blob/main/architecture/COMPONENT-ARCHITECTURE-DECISIONS.md
7. Security contract: https://github.com/VlDMlNSh/mediahub-os/blob/main/architecture/SECURITY-TRUST-AUTHORIZATION-CONTRACT.md
8. Jarvis reference: https://github.com/adewaskar/jarvis · https://github.com/adewaskar/jarvis/blob/main/bridge/server.mjs
9. Claude Code CLI permissions: https://docs.anthropic.com/en/docs/claude-code/cli-usage
10. Claude Code SDK: https://docs.anthropic.com/ru/docs/claude-code/sdk
11. Ollama API: https://github.com/ollama/ollama/blob/main/docs/api/introduction.mdx · https://github.com/ollama/ollama/blob/main/docs/api/openai-compatibility.mdx
12. OpenTelemetry: https://opentelemetry.io/docs/
13. MCP authorization: https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/docs/specification/2025-11-25/basic/authorization.mdx
14. Apple, Mac mini Mid-2011 memory specifications (official factory options): https://support.apple.com/en-us/103344
15. Apple, Mac mini Mid-2011 technical specifications (factory memory options up to 8 GB): https://support.apple.com/en-sa/112007
16. OWC, independent testing of 16 GB (2×8 GB) upgrade on Mid-2011 Mac mini: https://www.owc.com/news/owc-announces-industrys-first-16gb-ram-upgrade-for-latest-apple-mac-mini-models

## 15. Итоговый статус

DESIGNED — описание существует, runtime не доказан. PREFLIGHT — проверяется идентичность и окружение. ADMITTED — компонент прошёл admission. QUALIFICATION — выполняются свежие испытания. VERIFICATION — независимая проверка A3. SOAK — текущие 24 часа. LAUNCH_READY — G0–G10 пройдены, но требуется human G11. GOLD_ACTIVE/LAUNCHED — только после человеческого запуска exact SHA. BLOCKED — evidence отсутствуют, устарели, конфликтуют или не проходят gate.

**Приоритет:** (1) безопасно решить disk-full на временном mh-dev-01 и сохранить dirty worktrees/evidence; (2) закрепить целевые dev hosts и отдельный product M2; (3) оформить authority/persistence/worker-topology ADRs; (4) выполнить GitHub-first component admission и PoC для workflow/agent/router/voice alternatives; (5) интегрировать product tool broker и модельные adapters; (6) добавить GPU/video pool только после workload benchmark; (7) проводить qualification по exact SHA. На 12.10.2026 ни product multi-agent runtime целиком, ни engineering controller не следует объявлять qualified.
