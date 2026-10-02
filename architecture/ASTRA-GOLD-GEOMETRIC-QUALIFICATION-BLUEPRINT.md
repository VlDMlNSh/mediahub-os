# ASTRA GOLD — GEOMETRIC QUALIFICATION BLUEPRINT

## Цель

Минимизировать активное инженерное время до разрешённого тестового старта за счёт геометрического уменьшения повторной работы после каждого запроса, не сокращая обязательные доказательства, физические испытания или человеческую авторизацию.

## Инварианты

- G4: 5 mandatory paths × 23 fresh rounds = 115 observations.
- G5: максимум 2 параллельных claims; shared surfaces serial.
- G6: все 8 recovery scenarios.
- G7/A3: независимая проверка; self-verification запрещена.
- G8: только при полном свежем bundle.
- G9: непрерывные 24 часа; планировщик не сокращает duration.
- G10: только после G0–G9.
- G11: только HUMAN_AUTHORIZED.
- Historical evidence reuse=false.
- Fail-closed=true.

## Геометрический принцип

B(n) = max(Bmin, B0 × 2^(-(n-1))).

B0 = 8 часов; Bmin = 0.25 часа. Это плановый бюджет, а не обещание длительности и не право пропустить gate.

## Алгоритм каждого запроса

1. Считать актуальный gate/evidence state.
2. Найти самый ранний незакрытый gate.
3. Проверить наличие свежего evidence.
4. Не повторять уже доказанную работу без нового input.
5. Если evidence отсутствует — создать минимальный verifier/test surface.
6. Немедленно проверить созданный surface.
7. Интегрировать только необходимые изменения.
8. Пересчитать blocker и wall-clock.
9. Зафиксировать commit SHA.
10. Перейти к следующему запросу с уменьшенным активным бюджетом.

## Wave packing

Разрешено параллелить только независимые read-only/isolated операции.

### Pre-G4

Пять mandatory smoke probes независимы и используют отдельные временные workspaces. Они выполняются одним bounded batch с максимумом 5 параллельных probes. Это уменьшает wall-clock верхней границы с примерно 5 × probe_timeout до примерно 1 × probe_timeout плюс подготовка, без изменения числа путей, fresh evidence, source SHA, marker validation и timeout semantics. Реализовано в ops/qualification/pre_g4_auth_tree.py.

### G4

115 observations остаются обязательными. Параллелизм допустим только при полной изоляции evidence. Параллельность не сокращает число observations.

### G5

Максимум 2 claims; параллельная работа только для disjoint boundaries. Shared surfaces serial.

### G6

Независимые recovery scenarios могут подготавливаться параллельно, но результат публикуется через одну coordination authority. Replay/idempotency и publication recovery сохраняются отдельными доказательствами.

### G7

A3 остаётся отдельной verification authority. Executor и verifier не объединяются.

### G8

После G4–G7 формируется один immutable bundle. Любой отсутствующий prerequisite блокирует admission.

## Критерий прогресса

Каждый запрос обязан сделать минимум одно из:

- закрыть реальный blocker свежим evidence;
- уменьшить число отсутствующих prerequisites;
- устранить путь обхода gate;
- повысить наблюдаемость следующего gate;
- подготовить физический запуск, который раньше был невозможен;
- уменьшить wall-clock подготовки безопасной независимой параллельностью.

Если запрос не уменьшает blockers или доказуемую wall-clock latency, косметическая работа запрещена.

## Экспоненциальное сокращение повторной работы

Запрещено повторять уже подтверждённые статические проверки, deterministic tests, одинаковый audit без нового input и исторические qualification results как замену fresh evidence. Приоритет — delta verification.

## Physical boundary

GitHub Transport может подготовить код, contracts, verifiers и evidence surfaces. Физическая квалификация executors, shared-node coordination, recovery и 115 реальных rounds требует реального executor environment и не считается выполненной по исходному коду.

## Разрешённый тестовый старт

G8 PASS → G9 24H PASS → G10 PASS → G11 HUMAN_AUTHORIZED.

G11 остаётся человеческим решением.

## Метрика

Найденно → Исправлено [SHA] → Новые blockers → Сокращение активного бюджета → Следующий gate → наблюдаемая оценка wall-clock.

Время оценивается только по реально наблюдаемым этапам; отсутствие runner не превращается в выдуманный countdown.

## Stop condition

Если следующий шаг требует отсутствующего физического ресурса, результат не имитируется. Фиксируется BLOCKED и выполняется следующий доказуемый подготовительный шаг.
