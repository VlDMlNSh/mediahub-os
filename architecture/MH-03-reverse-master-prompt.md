# MH-03 Reverse Master Prompt

Проверь реализацию MediaHub против MH-3 и верни только архитектурный compliance report.

Проверить:
1. Нет ли второго canonical mutation path.
2. State Authority остаётся единственной mutation authority.
3. Нет ли shadow state store или persistence-as-authority.
4. Все mutations проходят Command → Validation → Authorization/Policy → Consumer Contract → State Authority.
5. Event/Telemetry/AI/UI/Plugin/Device/Cloud не мутируют state напрямую.
6. Runtime lifecycle соответствует ABSENT → INITIALIZING → STARTING → READY ↔ DEGRADED/RECOVERING → STOPPING → STOPPED.
7. State Authority failure не создаёт fallback authority.
8. Cloud/AI loss допускает deterministic local operation где возможно.
9. Unknown/malformed/ambiguous/unauthorized inputs обрабатываются reject/deny/fail-closed/quarantine согласно MH-3.
10. Runtime service boundaries не создают implicit authority.
11. Observability остаётся non-mutating.
12. Technology choices не объявлены canonical без соответствующего decision/evidence process.

Формат результата: VERIFIED / FAILED / UNKNOWN / REQUIRES VERIFICATION + evidence paths. Не исправляй архитектуру самостоятельно. Архитектурное противоречие оформляй как CONTRADICTION / GOVERNANCE CHANGE REQUIRED.
