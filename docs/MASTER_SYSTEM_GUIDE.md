# MediaHub OS / ASTRA GOLD / Jarvis — единый мастер-гайд

**Версия:** 1.0 · **Аудит:** 12 октября 2026 года  
**Статус:** интегрированная документация по целевой архитектуре и доступным доказательствам. ASTRA GOLD runtime **не квалифицирован**.

> Правило достоверности: «Проверено» означает, что сведения подтверждены чтением исходников/состояния подключённых узлов; «Цель» — согласованная целевая архитектура; «Кандидат» — внешний компонент, не внедрённый до admission и свежих тестов. Документ или health endpoint не доказывает сквозную работоспособность.

## 1. Назначение и итог аудита

MediaHub OS — платформа и доменная система. ASTRA — контроллер автономной разработки и квалификации. Jarvis — пользовательский интерфейс, голос и запуск разрешённых задач. Эти уровни связаны, но не взаимозаменяемы.

Цель — система с голосовым/текстовым входом, памятью, контроллером заданий, инструментами, локальными и разрешёнными облачными моделями, распределённым исполнением, проверяемыми результатами, безопасностью и восстановлением.

**Фактическое состояние на 12.10.2026:** подключены два Linux-узла и Mac mini M2. Mac Pro, MacBook и GPU host не появились среди активных Desktop Commander устройств; их характеристики/доступность неизвестны. Корневой диск mh-dev-01 заполнен на 100%. На mh-dev-02 жив API Ollama, но heartbeat контроллера последний раз менялся 7 октября. Существующие transport/provider evidence датированы концом сентября и содержат BLOCKED/NOT_PASS. На Mac mini прошла валидация 25 контрактных файлов/9 envelope contracts и пять тестов топологии; другие выбранные unittest-модули не импортировались из-за отсутствующего PyYAML, pytest не установлен. Полная qualification не подтверждена.

### Ключевые выводы

1. Сильная сторона — формализованные роли A0/A1/A2/A3, fail-closed gate, обязательные evidence и человеческий запуск.
2. Первоочередной блокер — заполненный диск mh-dev-01. Не запускать там сборки, установку пакетов или широкие тесты и не удалять файлы до read-only анализа и сохранения dirty worktrees.
3. Evidence устарели и не доказывают состояние сегодня.
4. Один компонентный документ говорит о двух параллельных claims, а канонические контракты, reference architecture и тесты — о трёх. Документацию следует согласовать.
5. На mh-dev-02 метки qwen2.5-coder:7b и claude-sonnet-4-6:latest показывали один и тот же Ollama ID. Это конфликт идентичности: не считать их двумя независимыми моделями, пока manifest/digest не проверен.
6. FreeLLMAPI не имеет подтверждённого точного upstream/commit. В сети есть несколько одноимённых проектов; не подключать найденный случайный репозиторий.
7. Jarvis из видео — полезный референс голосового HUD, но его базовая реализация использует Claude Code/Agent SDK и облачную Anthropic модель. Это не готовый Alamo/FCC/local-only маршрут.

## 2. Авторитет и границы ответственности

| Компонент | Роль | Ограничения |
|---|---|---|
| Человек | Финальная архитектурная, безопасностная и production authority | Только человек разрешает запуск G11 |
| A0-ASTRA | Единственная координация и State Authority MediaHub; queue, claims, leases, reconciliation | Не подменяется провайдером, транспортом или моделью |
| A1 | Архитектура и контракты | Не исполняет роль независимого A3 |
| A2 | Ограниченная реализация | Не сертифицирует собственную работу |
| A3 | Независимая проверка на exact SHA | Должен быть независим от исполнителя |
| Jarvis | Голосовой/UI фасад, сбор задачи, отображение состояния | Не является второй State Authority |
| FCC / OmniRoute | Транспорт/интеграция исполнителей | Не владеют состоянием MediaHub |
| FreeLLMAPI / provider gateways | Маршрутизация к моделям после admission | Не гарантируют бесплатную ёмкость и не получают полномочий |
| Alamo / Ollama | Инференс локальных моделей | Не принимают решения о разрешениях |
| Executors | Выполнение ограниченной задачи | Только executor authority |
| GitHub control bus | Код, desired state, журналы/evidence transport | В публичном репозитории запрещены конфиденциальные данные |

Модель предлагает; исполнитель выполняет; State Authority проверяет и фиксирует допустимое изменение; A3 независимо проверяет; человек утверждает запуск. Сетевая доступность или членство в mesh/VPN не означает разрешения менять состояние.

## 3. Целевая топология

Пользователь и клиенты MediaHub iOS/MacBook обращаются через аутентифицированный API к предполагаемому центральному Mac Pro. Целевые компоненты там: API Jarvis, A0 queue/state/evidence, policy router, локальный endpoint Alamo, memory service и observability. Приватные аутентифицированные связи ведут к трём Claude execution lanes, принадлежащему оператору GPU pool A и изолированному user pool B. Европейский VPS — только key registration/management; не proxy для обычного model/data traffic.

Это целевая схема, не утверждение о текущем деплое. Фактически доступны только mh-dev-01, mh-dev-02 и Voktors-Mini.Dlink. Mac Pro, MacBook и GPU host нужно отдельно инвентаризировать, если они существуют и должны участвовать.

### Плоскости системы

- **Authority plane:** человек, A0, A1, A2, A3 и формально разделённые права.
- **Control plane:** приём задания, декомпозиция, зависимости, очередь, claims/leases, heartbeat, fencing, duplicate suppression, отмена, replay и reconciliation.
- **Execution plane:** Claude Code, Codex и другие допущенные executors в изолированных рабочих областях.
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
| Voktors-Mini.Dlink | Mac mini M2, Mac14,3, ARM64, 8 GB RAM; Data volume 228 GiB, около 60 GiB свободно; Python 3.14.8, Node 22.23.3, Ollama | Лёгкая третья lane/локальные пробы. Модели есть, qualification не подтверждена |
| Mac Pro | Целевая роль — central API/router/Alamo | Не найден среди подключённых устройств; характеристики и health неизвестны |
| MacBook | Цель — Claude Desktop/Codex Desktop client | Не найден среди подключённых устройств |
| Owned GPU host | Цель — Pool A GPU compute | GPU/VRAM/RAM/runtime/network неизвестны |
| User pool | Участнические узлы, только opt-in jobs | Недоверенные по умолчанию; доступ к секретам и authority запрещён |
| VPS | Изолированный key registration workflow | Не использовать как inference proxy или для обхода правил провайдеров |

На mh-dev-02 Ollama list показал qwen2.5-coder:1.5b (986 MB), qwen2.5-coder:3b (1.9 GB), qwen2.5-coder:7b (4.7 GB) и alias claude-sonnet-4-6:latest (4.7 GB), причём две последние метки имели один ID. На Mac mini найдены qwen2.5-coder:1.5b, qwen2.5-coder:3b и qwen3:4b. Не считать модельные метки доказательством идентичности; сохранять manifest/digest и исключить сомнительный alias из автоматического выбора до read-only проверки. Не удалять модели автоматически.

Для GPU-host нужны подтверждённые GPU/VRAM, RAM, SSD, driver/runtime, checkpoint, quantization, context length, concurrency, latency/throughput и thermal budget. Между компьютерами RAM/VRAM не складываются автоматически. Большую модель размещать на одном подходящем хосте либо использовать проверенный multi-GPU runtime.

## 5. Распределение задач

| Узел | Базовая роль | Не назначать без qualification |
|---|---|---|
| Mac Pro (цель) | Jarvis API, A0 queue/state/evidence, router, Alamo после hardware/runtime check | Большой inference без benchmark, открытые admin ports |
| mh-dev-01 | Claude lane для bounded coding/test jobs после освобождения диска | Любая запись при нуле свободного места, очистка dirty worktrees |
| mh-dev-02 | Claude lane, health probes, Ollama/API tests | Большой inference, cloud fallback в LOCAL_ONLY, квалификация по одному каталогу |
| Mac mini M2 | Третья Claude lane, диагностика, малые локальные модели | Большие модели с превышением RAM, независимая сертификация своих изменений |
| MacBook | Пользовательская поверхность Claude Desktop/Codex Desktop | Постоянный сервер/тяжёлый inference по умолчанию |
| Pool A GPU | Доверенный worker крупных моделей, vision/embeddings по scoped API | Секреты контроллера или direct access к canonical state |
| Pool B | Non-sensitive opted-in bounded jobs | Секреты, личные данные, приватный контекст, controller rights |
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

Поток: Browser/Native UI → authenticated Jarvis API → task service → A0 queue/policy → permission broker → executor/model adapter → result validator → evidence store → UI. Секреты остаются server-side; модель не управляет своими разрешениями и не получает бессрочные credentials.

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

Постоянные production lanes в canonical reference: Claude на mh-dev-01, mh-dev-02 и Mac mini. Максимум три одновременных claims — по одному на lane. Claims не пересекаются; общие mutable surfaces сериализуются; duplicate controller отклоняется; stale lease требует fencing/recovery; replay идемпотентен.

Пять qualification paths — CODEX_FCC, CLAUDE_FCC, CODEX_OMNIROUTE, CLAUDE_OMNIROUTE и CLAUDE_CODE_DIRECT — это испытательные сочетания executor/transport, не замена трём permanent lanes. Каждый mandatory path должен пройти 23 свежих изолированных успешных раунда.

Evidence: command ID, node, component, executor, provider/model, transport if applicable, source SHA, round, timestamp, exit status, timeout, workspace, verification status, evidence digest. Secrets и authorization tokens запрещены. Историческое evidence не закрывает fresh gate.

- G0 Identity — точные identities/SHA, чистый worktree.
- G1 Boundary — authorization, transport/state/credential boundaries, isolated workspace.
- G2 Control Plane — queue, leases, duplicate suppression, result publication, heartbeat.
- G3 Execution Path — runtime/version, timeout, exit status, schema and marker.
- G4 23-wave — все mandatory rounds свежие, успешные, изолированные.
- G5 Concurrency — три непересекающихся claims и duplicate-controller rejection.
- G6 Recovery — timeout, executor/transport failure, stale claim, restart, replay, publication recovery.
- G7 Integrated A3 — independent code/contracts/regression/security/concurrency/recovery verification.
- G8 Pre-soak — all paths/recovery/A3 PASS, clean worktree, fresh evidence.
- G9 24H soak — 24 часа без unexplained restart, claim corruption, unresolved failure или authority violation.
- G10 Launch-ready — G0–G9, evidence bundle, rollback target.
- G11 Human launch — только человек, approval привязан к exact SHA/release и rollback.

Missing/stale/conflicting evidence означает BLOCKED. Модель/исполнитель не присваивают себе qualification.

## 9. Проверки и пробелы

**Проверено:** GitHub reference architecture, governance contract, qualification schema, unified system YAML, component scheme/registry/decisions и security boundaries прочитаны. На Mac mini contract validator: PASS, 25 contract files, 9 envelope contracts. Пять topology tests прошли: concurrency=3, три Claude lanes, Codex не является permanent lane, capability/single-authority checks. На mh-dev-02 Ollama localhost version endpoint вернул HTTP 200.

**Не пройдено/не запускалось:** pytest отсутствует; PyYAML отсутствует в выбранном Python 3.14 на Mac mini, поэтому governance/repo hygiene/secret hygiene модуль не импортировался. Часть test dependencies отсутствует и на mh-dev-02. Не выполнены сквозной Claude Code→FCC→FreeLLMAPI/Alamo, local-only egress denial, tool-calling, все 23 раунда на mandatory paths, recovery suite, fresh independent A3 и текущий 24H soak. Полный security audit всех runtime/API не заявляется.

Evidence transport/provider от 27.09.2026 показывает BLOCKED/NOT_PASS; qualification JSON от 27.09.2026 содержит BLOCKED_PRE_SOAK. Heartbeat mh-dev-02 старше 24-hour evidence freshness window. Итог ASTRA GOLD runtime: **BLOCKED / NOT GOLD_ACTIVE**.

## 10. Реестр исправлений

| Приоритет | Проблема | Критерий закрытия |
|---|---|---|
| P0 | mh-dev-01 disk 100%, 0 free | Read-only inventory, сохранение dirty/untracked/evidence, согласованный selective cleanup, затем свежие health/runtime checks |
| P1 | Stale mh-dev-02 heartbeat | Один подтверждённый controller per lane, свежие heartbeat/queue evidence по текущему SHA |
| P1 | Один Ollama ID у двух model labels | Сохранить manifest/digest/provenance; quarantine alias до подтверждения |
| P1 | FreeLLMAPI upstream unknown | Exact repo/commit, license/auth/terms, secure bind и adapter tests |
| P1 | Нет Alamo endpoint/e2e FCC route | Identity/schema/auth/health, bounded task, actual provider/model evidence, negative egress test |
| P1 | Mac Pro/MacBook/GPU host не подключены | Проверить фактические hardware, network и runtime, если узлы должны существовать |
| P1 | Jarvis reference defaults to Anthropic cloud | Adapter, local-only hard boundary, MCP allowlist, broker и negative tests |
| P1 | Тестовые зависимости неполны | Pinned isolated venv/lockfile и повтор contract/unit/security suites |
| P2 | Component scheme говорит max 2 claims вместо 3 | Согласовать prose с canonical gate contract и тестами |
| P2 | Корневой README почти пустой | Сослаться на master guide, safe setup/tests/security |

Не выполнялись очистка диска, удаление моделей, restart controller и перезапись dirty worktrees: это может уничтожить данные.

## 11. План реализации

**Фаза A — стабилизация:** остановить writes на mh-dev-01; сохранить изменённые файлы; подтвердить один controller per lane, source SHA/worktree и fresh heartbeat; read-only расследовать модельный ID conflict.

**Фаза B — маршрутизация:** pin версии Claude Code/FCC/FreeLLMAPI/Ollama и Alamo variant; протестировать каждый переход отдельно; non-mutating probe до bounded repo task; проверить LOCAL_ONLY с egress denial; испытать 429/quota, outage, malformed response, timeout, cancellation, idempotency, stale claim и recovery.

**Фаза C — Jarvis:** закрепить MIT upstream commit, review SBOM/dependencies/license/security; authenticated API; explicit MCP allowlist; permission broker, sandbox, approvals для необратимых действий; voice/privacy, task ID, cancel/reconnect; versioned memory с sources, retention и deletion.

**Фаза D — qualification:** exact SHA/worktree, 23 rounds на mandatory paths, concurrency 3, recovery tests, A3, reconciliation, fresh pre-soak, полные 24H и human G11 approval с rollback.

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

## 15. Итоговый статус

DESIGNED — описание существует, runtime не доказан. PREFLIGHT — проверяется идентичность и окружение. ADMITTED — компонент прошёл admission. QUALIFICATION — выполняются свежие испытания. VERIFICATION — независимая проверка A3. SOAK — текущие 24 часа. LAUNCH_READY — G0–G10 пройдены, но требуется human G11. GOLD_ACTIVE/LAUNCHED — только после человеческого запуска exact SHA. BLOCKED — evidence отсутствуют, устарели, конфликтуют или не проходят gate.

**Приоритет:** сначала стабилизировать mh-dev-01, восстановить актуальную heartbeat-доказательность, разрешить конфликт ID модели и pin-нуть FreeLLMAPI. Потом — сквозной model-routing, Jarvis UI/voice/tool broker и полная квалификация. На 12.10.2026 система **BLOCKED / NOT GOLD_ACTIVE**.
