# ASTRA GOLD — Что следует усилить

Status: АНАЛИТИЧЕСКИЙ ОТЧЁТ / НИ ОДИН ГЕЙТ НЕ ПРОДВИГАЕТ
Date: 2026-10-02
Scope: текущее состояние репозитория + архитектурные документы (schema, governance contract, unified model, reference architecture), проверенные hydras и test-gate статусы (compiler, lint-style parse, gate tests, governance validator, drift/pin/hygiene/cross-contract)
Language: русский

Примечание: отчёт не создаёт live-доказательств и не продвигает ни один гейт. Работа в analytic-only режиме на основе того, что уже в репозитории.

---

## 1. Цель этого блока

Ранее добавлен governance contract, current-truth генератор, cloud-executor extension и анти-дрифт тесты. Это сильно улучшило состояние. Сейчас нужен взгляд на то, где схема всё ещё может быть уязвима или незрелой, чтобы выбрать следующие шаги.

Ниже — структурное описание зон для усиления: security, reliability, processes, evidence, operational robustness, extension моделей, governance, учёт покрытия тестов.

---

## 2. По категориям

### 2.1 Живые доказательства, еще не существующие

Сейчас контрактные и тестовые gмеханизмы в репозитории зеленые, но все живые gate-проверки все еще в состоянии ожидания:
- G0–G10 — BLOCKED / NOT_PROVEN
- G4 — 0 из 115 раундов
- A3 — вне репозиторных evidence
- 24h soak — не запущен

Это главный резерв. Уже сделано: контракты, категории, пути, манифест генерации, fail-close логика, pre-soak и governance артефакты. Не сделано: real integrated evidence production в разрешенной среде (kredentials, раннеры, canonical node и т.д.). Это есть самый главное усиление, но это оперативная/инфраструктурная задача, не только схема.

### 2.2 Gateway и cloud-executor идентификация

Good: cloud executors добавлены как extension with no authority, и обязательные 5 путей untouched. Но в current текущем state имеется mix из видимых маршрутов: direct cloud и gateway (например, OpenRouter и т.п.). Неясно до конца:
- каким образом производится целостность provider identity
- как именно это будет проверяться at admission event в runtime
- как именно gateway success не продвинет native provider qualification

Усиление: добавить явный путь и явные критерии в runtime (заимствование не реально, но провешивание identity trace для каждого executor) и отдельные failure-modes (e.g. что если gateway без native querieties перепустит результат). Это образуется как обогащение requirement и test harness.

### 2.3 Credential lifecycle —ограмма в текст, но без исполнения

Good: в governance есть rotation_required, revocation_supported, audit_required, per_provider_isolation, aux creation disallowed, max_credential_age_days=90. Но пока это YAML-свойство. Нет obligation harness через который бы автоматически отвечало:
- bypass вручную нарушение возраста
- устаревание учеток
- автоматический обзор
- автоматическая or controlled возможность удалить и залогирует

Усиление: хоть один интеграционный тест/проверка, где expiry критерий встречает обновлённый/expired credential, что е microseconds утвердите его — credible policy enforcement, not only a comment. Не обязательный но рекомендуемый, failure-gated.

### 2.4 Human approval record — есть форма, но пропущено исполнение

Good: decision_authority = HUMAN_ONLY, unsigned rejected, approval_expires_with_sha_change true, required_fields comprehensive. Но есть только контрактная модель, не runtime check, не пример файла, не процедура как harness проверки.

Усиление:
- Reproducible операция/сценарий: как procedure выполнить signed approval, как stored, как проверить её подпись, как отказать устаревшую.
- Не требуется сейчас как live часть, но задаёт и безопасности и audit процедуре.

### 2.5 Двойное слияние категорий / много повторов категорий

Good автоматизация категорий создана: local_model / gateway, browser, coding_harness, security_tool, unresolved_identity.
Но:
- someкатегории “identity verification required” без runnable resolution step как часть automation
- unresolved identity (например, код ссылки github.com лишь) — не удельна механизм автоматической блокировки в-harness в коде а не только соглашение текста

Усиление: добавить и зафиксировать для каждой категории что есть acceptance gate (и возможно test scenario), и упростить все multi-provider/candidate формы к единому шаблону, содержащему:
- issuer/source
- version/name/release
- dependency fingerprint
- non-mutating probe
- sandbox/boundary
- result validation
- recovery
- A3 binding

### 2.6 Обработка edge при расширении путей

Good: расширение через `` --paths `` allowed but означит, что applicant может делать bigger matrix, но без явного понятия impact на overload/case совпадения/concurrency. В архитектурно-схеме есть concurrency cap = 2, но модель windfall палок для дополнительных paths не выписана (не conflict с cap а качественно: например из каких областей/квот/framework где это будет замедлять или допускать overlap).

Усиление:
- уточнить расширение путей в área конкурентности: если добавить другие путей, как контролируются overlapping distributions? Может добавить отдельный простой guard (например «экран concurrent addition» only after previous gate pass).
- добавить явной материнской проверки: при добавлении cloud executor, какое authority иточку gate неэффективно иные qualification gaps а другие не.

### 2.7 Gate enforcement и visibility в реальном времени

Good: gate 설계를 fail-close 등으로 잘 관리했지만, **실시간 가시성**은 부족했다. 다음 장:
- 현재 run-time 상태(원활/차단/준비 등) — 실시간 수집·시각화
• 어떤 게이트가 넘어가고 어떤 게 아직 블록인지 보기 쉽게 — dashboard/evidence reader

방법:
- separate observability pipeline or artifact for gate states to read
- failure를 catalog/write 시 게이트 레벨에서 (현 상태는) 현재 시스템 동작에 대한 확장된 가시화 추가됨

### 2.8 Edge cases в recovery

Good: 시나리오 목록 큼 — timeout, executor failure,timeout, stale claim, worker restart, duplicate controller, replay, result publication, partial integration, etc.

Но нас:
- каждый scenario отдельное классифицировано как требование, но нет явного "results матрицы — каждый требует отдельно PASS" в current
- в реальном runtime, recovery отвечен — partial/the full

Усиление:
- explicit matrix where each scenario results in PASS/BLOCKED и независимо, не только “required”
- isolation критериев для multi-node, multi-actor replay, partial integration edge case

### 2.9 Replay и idempotency

Good: replay/idempotency требование есть. Lax, но не:
- 어떤 데이터에서도 재계산 이력을 유지해야 하는지 / обновлений
- какое replay event считается invalid
- как записать idempotency в evidence

Усиление:
- формулировка replay event recording и idempotency evidence criteria (что такое duplicate event)
- добавить test/harness-level check where replay case номер event ≠ first, result should fail- blocked 자.

### 2.10 Audit·의료 trail для контроля

Good: secrets suppression, evidence metadata, immutable evidence, linked correction. Но:
- audit required в credential lifecycle пока как YAML
- кому‑как чьи экшены в системе проверяются? (who modified gates, 누구-added executor 경로, 누구‑digited approval 등)
- absence of audit trail для governance change

Усиление:
- governance changes 가 audit trail에 대해 명시적인 field 포함해 e.g. ``changed_by``, ``changed_at``, ``reason``, ``approval_record_ref`` — 요 호소한다; future changes made through approved gate; drift 시 fail constraint at audit layer too

### 2.11 Artifact integrity и 영구 보존성

Good: evidence immutability и linked corrections.

Но:
- как обеспечивается long-term availability/archive (evidence decade-retention, replay на новых машинах)
- artifact linking и хранение длительности в 클라우드/локальной средероме
- regeneration 에서 발생한다 가능한지 (artifact 해시/check, checksum storage?)

Усиление:
- возможность artifact 아카이브/체크섬 저장, verification over time функций при 재생을 통해
- retention policy а nut заявлён в policy как 시간 정책 (현재 정책 명시적 아님)
- cross-check method to verify artifact integrity over long period

### 2.12 Overlap между 여러 YAML 정의

Good: канонизация 1 source. Повтор:
- есть unified-모델, governance contract и qualification schema — некоторые вещи duplicated но согласованы.
- двойной способ описания может привести к slow 조정 если изменить какую-либо плоскость в одном месте

Усиление:
- явный mapping priority и 가능하면 validation что вся необходимая информация для gate 정의에 permited only in single place и остальные yaml 참조하는 형식; 현행 validator가 이미 하나인데, 아직 canonical source priority가 중복되어 있으면。즉, 몇 가지 모델 겹침은 기술적으로는 괜찮지만, 장기적으로 drift 도입 위험 잔존

-----

## 3. Фокус для next steps (без продвижения гейтов)

1. Операционная часть: live evidence (G0–G11, soak) — это biggest strengthenings, но они зависят от окружения/secret/раннеры/канонический узел, а не только от репозитория
2. Если оперативная основа есть — следующий can be защита схемы через harness проверки каждого гейта, а не только через static YAML проверки
3. credential lifecycle и human approval record лучше сделать с runnable примерами и, желательно, минимальными integration проверкими
4. Усиление на расширении путей: добавление новых provider/executor 경로 확대 방지 메커니즘으로 concurrency guard 연결

---

## 4. Итог

현재 구조는 상당히 강하지만, live evidence 부족 및 governance/credential/approval 실행 부족이 main 강화 대상이다. оперативен에 의존하지 않는 범위에서는 다음 강화 포인트:

- категории acceptance gate 러너의 Live/исполнение 메커니즘
- ramp-up при добавление новых путей/provider들과 concurrency guard
- replay/idempotency 명시화
- runtime visibility / telemetry для gates
- audit trail для governance changes
- credential expiration enforcement объектно тест/harness и human approval 실행 시나리오

Это аналитический отчёт и не продвигается гейт.
