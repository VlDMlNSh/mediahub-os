# MediaHub OS — распределённая мультиагентная платформа

MediaHub OS проектируется как цельная продуктовая и инженерная система с двумя отдельными контурами: **MediaHub Product / Edge Runtime** и **Multi-Agent Development Plane**. ASTRA — инженерная подсистема разработки и квалификации; Jarvis — один из пользовательских фасадов.

**Целевая аппаратная схема:** покупаемый Mac Pro — development host №1 и будущий инженерный workflow/control узел после commissioning; Mac mini 2011 с Linux и целевыми 16 GB RAM — development host №2; существующий Mac mini M2 8 GB — первый рабочий прототип MediaHub на объекте заказчика, не постоянный сервер разработки; мощный GPU/video server — будущее расширение. Текущие узлы являются test lab, а не конечной топологией. Фактический deployment не считать готовым до закупки и qualification оборудования.

## Основной документ

- [MASTER SYSTEM GUIDE](docs/MASTER_SYSTEM_GUIDE.md) — архитектура мультиагентной системы целиком, роли/capabilities, hardware topology, repository-first policy, GitHub component shortlist, installed skills, модели/инструменты, память, безопасность, аудит и план развёртывания.
- [ASTRA GOLD reference architecture](architecture/ASTRA-GOLD-REFERENCE-ARCHITECTURE.md)
- [Governance contract](architecture/ASTRA-GOLD-GOVERNANCE-CONTRACT.yaml)
- [Qualification / launch schema](architecture/ASTRA-GOLD-QUALIFICATION-LAUNCH-SCHEMA.yaml)
- [Security / trust / authorization contract](architecture/SECURITY-TRUST-AUTHORIZATION-CONTRACT.md)

## Правила разработки

1. Перед созданием компонента сначала исследовать зрелые GitHub repositories, SDKs, standards and official docs; применять component-admission gate, exact version/SHA and isolated PoC.
2. Использовать готовые стабильные блоки и тонкие адаптеры вместо переписывания существующих систем.
3. Отделять product State Authority от developer/Astra coordinator, model providers, transports and workflow engine.
4. Секреты, личные данные, prompts и конфиденциальные task payloads не размещаются в публичном репозитории.
5. Недостающие, устаревшие или противоречивые доказательства означают BLOCKED.
6. Production launch требует exact SHA, independent A3, current 24-hour soak, rollback plan и human approval.

## Текущий статус

Аудит от 12 октября 2026 года: multi-agent target architecture описана, но component selection remains at candidate/PoC stage. Engineering controller runtime remains **BLOCKED / NOT QUALIFIED**. Обнаружены P0/P1 проблемы: disk-full на mh-dev-01; устаревший heartbeat на mh-dev-02; alias модели claude-sonnet-4-6:latest указывает на Qwen2 weights, а не на отдельный Claude Sonnet; route FCC → FreeLLMAPI / Alamo не прошёл e2e qualification; authority model product/developer требует ADR. Не чистить disk, не удалять модели и не сбрасывать dirty worktrees до сохранения evidence.
