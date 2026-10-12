# MediaHub OS

Единая платформа MediaHub OS, автономный контур разработки ASTRA GOLD и пользовательский фасад Jarvis.

**Целевое железо:** покупаемый в конце октября Mac Pro — основной целевой сервер MediaHub и development host №1; Mac mini 2011 с Linux и целевыми 16 GB RAM — development host №2; Mac mini M2 — первый прототип продукта MediaHub, не постоянный developer server; мощный GPU/video server — будущее расширение. Имеющиеся узлы — test lab, а не окончательная конфигурация.

## Основная документация

- [MASTER SYSTEM GUIDE](docs/MASTER_SYSTEM_GUIDE.md) — целевая архитектура, подтверждённая аппаратная инвентаризация, распределение задач, модельная маршрутизация, Jarvis, инструменты, безопасность, статус квалификации и план исправлений.
- [ASTRA GOLD reference architecture](architecture/ASTRA-GOLD-REFERENCE-ARCHITECTURE.md)
- [Governance contract](architecture/ASTRA-GOLD-GOVERNANCE-CONTRACT.yaml)
- [Qualification / launch schema](architecture/ASTRA-GOLD-QUALIFICATION-LAUNCH-SCHEMA.yaml)
- [Security / trust / authorization contract](architecture/SECURITY-TRUST-AUTHORIZATION-CONTRACT.md)

## Текущий статус

Аудит от 12 октября 2026 года: runtime **BLOCKED / NOT GOLD_ACTIVE**. Физическое развёртывание целевой схемы планируется после покупки Mac Pro в конце месяца; точная комплектация должна быть зафиксирована после приобретения. В актуальных evidence есть блокеры: disk-full на mh-dev-01, устаревший heartbeat на mh-dev-02, конфликт идентификаторов двух Ollama model labels и неподтверждённый сквозной путь FCC → FreeLLMAPI / Alamo.

Не выполнять очистку, сброс грязных worktrees, удаление моделей или широкие тестовые волны до сохранения evidence и безопасного устранения P0. Документированная целевая архитектура не означает, что runtime квалифицирован.

## Правила изменения

- Канонические governance/qualification contracts имеют приоритет над противоречащими им описательными документами.
- Секреты, приватные prompts и чувствительные payloads не размещаются в репозитории.
- Пропущенное, устаревшее или противоречивое доказательство ведёт к BLOCKED.
- G11 / production launch остаётся HUMAN_ONLY и требует точного SHA, независимого A3, текущего 24-часового soak и плана отката.
