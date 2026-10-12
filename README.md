# MediaHub OS

Единая платформа MediaHub OS, автономный контур разработки ASTRA GOLD и пользовательский фасад Jarvis.

## Основная документация

- [MASTER SYSTEM GUIDE](docs/MASTER_SYSTEM_GUIDE.md) — целевая архитектура, подтверждённая аппаратная инвентаризация, распределение задач, модельная маршрутизация, Jarvis, инструменты, безопасность, статус квалификации и план исправлений.
- [ASTRA GOLD reference architecture](architecture/ASTRA-GOLD-REFERENCE-ARCHITECTURE.md)
- [Governance contract](architecture/ASTRA-GOLD-GOVERNANCE-CONTRACT.yaml)
- [Qualification / launch schema](architecture/ASTRA-GOLD-QUALIFICATION-LAUNCH-SCHEMA.yaml)
- [Security / trust / authorization contract](architecture/SECURITY-TRUST-AUTHORIZATION-CONTRACT.md)

## Текущий статус

Аудит от 12 октября 2026 года: **BLOCKED / NOT GOLD_ACTIVE**. В актуальных evidence есть блокеры: disk-full на mh-dev-01, устаревший heartbeat на mh-dev-02, конфликт идентификаторов двух Ollama model labels и неподтверждённый сквозной путь FCC → FreeLLMAPI / Alamo.

Не выполнять очистку, сброс грязных worktrees, удаление моделей или широкие тестовые волны до сохранения evidence и безопасного устранения P0. Документированная целевая архитектура не означает, что runtime квалифицирован.

## Правила изменения

- Канонические governance/qualification contracts имеют приоритет над противоречащими им описательными документами.
- Секреты, приватные prompts и чувствительные payloads не размещаются в репозитории.
- Пропущенное, устаревшее или противоречивое доказательство ведёт к BLOCKED.
- G11 / production launch остаётся HUMAN_ONLY и требует точного SHA, независимого A3, текущего 24-часового soak и плана отката.
