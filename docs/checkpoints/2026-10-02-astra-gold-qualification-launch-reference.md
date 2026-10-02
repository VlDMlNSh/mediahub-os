# ASTRA GOLD — Эталонная схема TEST → QUALIFICATION → LAUNCH

Статус: CANONICAL REFERENCE
Дата: 2026-10-02

## 1. Назначение

Единый эталонный конвейер допуска ASTRA GOLD разделяет технический тест, квалификацию, независимую проверку A3, 24-часовой soak и фактический запуск.

Успешный тест не равен квалификации. Квалификация не равна разрешению на запуск.

## 2. Эталонный конвейер

DISCOVER → PREFLIGHT → ADMIT → QUALIFY → EXECUTE → VERIFY → INTEGRATE → RECONCILE → PRE_SOAK → SOAK_24H → LAUNCH_READY → HUMAN LAUNCH → LAUNCHED

При обязательном сбое:

BLOCKED → DIAGNOSE → REPAIR → PREFLIGHT

После деградации уже запущенного контура:

LAUNCHED → ROLLBACK → REQUALIFY

## 3. Gates

G0 Identity — node/executor/provider/model/repository/SHA/worktree.

G1 Boundary — authority/transport/state/credential/workspace boundaries.

G2 Control Plane — command/claim/lease/queue/heartbeat/result/replay.

G3 Execution Path — identity, timeout, nonzero handling, malformed-result rejection, marker, schema validation.

G4 23-wave — 23 свежих успешных раунда для каждого mandatory executor path.

G5 Concurrency — максимум 2 параллельных autonomous claims; shared surfaces сериализованы.

G6 Recovery — timeout, executor failure, transport interruption, stale claim, worker restart, duplicate controller, replay/idempotency, result publication recovery.

G7 Integrated A3 — независимая проверка кода, контрактов, архитектуры, security, concurrency, failure и recovery.

G8 Pre-soak — полный свежий evidence bundle и все обязательные проверки PASS.

G9 24h soak — полный непрерывный период без неконтролируемой деградации.

G10 Launch Ready — только при свежем PASS всех G0–G9.

G11 Launch — отдельное решение Human с release SHA и rollback target.

## 4. Evidence

Минимальный набор: command_id, node_id, component_id, executor_id, provider/model_id, source_sha, round, timestamp, exit_status, timeout, workspace, verification_status, evidence_digest.

Секреты, токены и необработанные чувствительные ответы не записываются.

## 5. Gemma 4

Gemma 4 размещается только в LOCAL_MODEL_FABRIC.

Последовательность:
MODEL_IDENTITY → EXACT_VARIANT → WEIGHT_PROVENANCE → RUNTIME_IDENTITY → RESOURCE_PROFILE → NON_MUTATING_PROBE → CAPABILITY_PROBES → LATENCY/MEMORY → FAILURE/RECOVERY → ISOLATED_TASK → RESULT_VALIDATION → A3

Каждый вариант квалифицируется отдельно. Результат одного варианта не переносится на другой.

До свежих runtime-доказательств статус: NOT_PROVEN.

## 6. OpenFlux

OpenFlux остаётся CANDIDATE_EXECUTION_SURFACE.

Последовательность:
IDENTITY → VERSION → SANDBOX → NON_MUTATING_PROBE → ISOLATED_WORKSPACE → RESULT_VALIDATION → RECOVERY → A3

OpenFlux не получает A0/A1/A2/A3 authority и не может самостоятельно продвигать себя, модель или provider.

## 7. Launch contract

Перед запуском должны существовать:
1. approved source SHA;
2. свежий evidence bundle;
3. независимый A3 record;
4. 24h soak record;
5. rollback target;
6. явная Human authorization.

Отсутствие любого пункта блокирует запуск.

ASTRA_GOLD_ELIGIBLE означает соответствие квалификационным критериям, а не автоматический production launch.

LAUNCH_READY означает готовность к решению Human.

LAUNCHED означает только фактически выполненный запуск с записанным evidence.

## 8. Текущий truth status

Architecture: READY
Qualification schema: CANONICAL
Local executor qualification: NOT_PROVEN
Cloud provider qualification: NOT_PROVEN
A3 integrated qualification: NOT_PROVEN
24h soak: NOT_PROVEN
Launch: BLOCKED
