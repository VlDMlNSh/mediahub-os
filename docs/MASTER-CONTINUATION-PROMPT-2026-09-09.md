# MEDIAHUB OS 11.x LTS / MEDIAHUB iOS
# MASTER AUTONOMOUS DEVELOPMENT CONTINUATION PROMPT
## Контрольная точка: 2026-09-09

Продолжай разработку MediaHub OS 11.x LTS / MediaHub iOS с полным сохранением истории решений, контрольных точек, invariants, provenance и governance. Не начинай проект заново и не возвращайся к forensic recovery.

## Нормативная архитектура

Единый нормативный источник: `specification/MEDIAHUB-FUNCTIONAL-BASELINE-1.0.md`. Functional Baseline 1.0 immutable; silent architectural drift запрещён.

Философия: Local First → Unified State → Unified UI → AI Assisted → Controlled Cloud Escalation.

MediaHub State Authority — единственный canonical platform state authority. Home Assistant Core — authority только Smart Home domain. Cloud, AI, mobile и reference products не становятся authority. Fail closed.

Mobile Access Layer содержит ровно два приложения: MediaHub Core for iOS/iPadOS и отдельное Remote Mobile Application. Mobile не является AI tier.

AI chain: Mobile Access Layer → Local AI → Local Cluster AI → Cloud Development AI. Local AI advisory/proposal only. Cloud Development AI — корпоративный development contour.

Trusted Sources Intelligence Engine и AI Human Clone — отдельные Cloud Development AI subsystems. Human Clone требует consent, authorization, provenance, rights, audit и revocation.

Update target: RAUC; не создавать две production OTA authorities. OSS adoption: capability gap → mature component → license → security → provenance → adapter → benchmark → adoption.

## Git / provenance

Repository: `VlDMlNSh/mediahub-os`.
Local development branch: `autonomous/os-build`.
Immutable R4 anchor: `471f709f5633feab7aeb62dd3ea52effad6d2bc4`.
R4 tree: `2279612908135418b2b5448d598274ea6741deaa`.

Последняя известная локальная контрольная точка: HEAD `057cb0acd9cd24c39dfe5fa17874c1227dcc9ffb`, clean tree. Не выполнять rebase, amend, reset, force-push или изменение R4 anchor.

## Автономная разработка

Authorized host: `mh-dev-01`.

Watchdog и `ops/autonomous_os_loop.sh` уже запущены; не запускать дубликат. Перед продолжением проверить процессы, `.autonomous` и последний log.

Local AI: Qwen2.5-Coder 1.5B Instruct Q4_K_M через `llama-cli`. Codex CLI ранее получил provider 403 и не является обязательной зависимостью. Не обходить региональные/provider restrictions через VPN/proxy/IP masking.

Autonomous loop: fail-closed, малые verified increments, R4 ancestry, diff/security checks, rollback при невалидном изменении. После значимого цикла выполнять pytest, security scan и functional baseline verification.

## Облачная волна

Приоритет: provider-neutral Cloud Development Adapter + isolated Cloud Development Sandbox, затем approved cloud AI providers только через этот boundary.

Adapter: classification, capability declaration, authorization, minimization, egress, residency/policy, timeout/retry, provenance, audit, metering, revocation, fail-closed.

Sandbox: separate identity, filesystem/worktree, network egress boundary, credential broker boundary, resource limits, DLP/secret hooks, quarantine, deterministic teardown.

Запрещены direct provider integrations в core, direct State Authority/HA/production access и unrestricted egress.

## Reg.cloud financial gate

Free Tier Reg.cloud официально существует, но account-specific entitlement и эффективная стоимость 0 ₽ должны быть подтверждены отдельно. Публичные официальные инструкции указывают на идентификацию и положительный баланс; не считать сам факт Free Tier разрешением на billable provisioning.

GitHub Issue #70: `cloud: request zero-cost Reg.cloud Free Tier confirmation before provisioning`.

До provisioning требуется account/API evidence, что выбранная VM и требуемые network/storage resources имеют effective cost `0 ₽` на весь применимый период; также проверить expiry behavior и отсутствие платной активации.

Ранее: API auth работает; reglets отсутствуют; balance `0 ₽`; inventory цен не показал zero-priced reglet. Перед provisioning повторить свежую проверку.

Target: Reg.cloud, предпочтительно `openstack-sam1`, Ubuntu 26.04 `ubuntu-26-04-amd64`, минимальный профиль. IPv4/network/storage включить в финансовую проверку.

При отсутствии явного account-level `0 ₽` confirmation сервер НЕ создавать. Не считать автоматическую остановку защитой от начислений.

API secret: `/etc/mediahub/credentials/regcloud_api_key`; никогда не выводить/логировать/копировать/запрашивать. Не обходить security gate Desktop Commander.

## Provisioning после gate

1. Проверить autonomous loop и git state.
2. Получить свежие Reg.cloud account/pricing/eligibility данные без раскрытия secret.
3. При exact effective cost = 0 ₽ для VM + network + storage создать один минимальный reglet.
4. Зафиксировать resource ID, region, image, network, pricing evidence и provenance.
5. Подключить сервер только через Cloud Development Adapter/Sandbox.
6. Проверить deny cases: State Authority, HA authority, production, local secrets, unrestricted filesystem и egress.
7. Выполнить connectivity, authentication, isolation, DLP/secret, timeout/retry, revocation и teardown tests.
8. При любом financial/security mismatch — fail closed и teardown.
9. Release locked; production NOT AUTHORIZED.

## Qualification

Implementation → unit/integration/negative tests → security → regression → provenance → independent review → MH-05 → T5 → F-03 → release qualification → production authorization.

AI/autonomous agent не может объявить independent qualification, release или production authorization.

## Правило нового чата

При команде `Продолжай` сначала восстанови состояние по этому prompt и repository, проверь HEAD/worktree/processes/logs и не повторяй завершённые проходы. Выполняй все безопасные доступные волны последовательно, не пересекая financial/security/release gates.

Текущая задача: продолжить автономную разработку, квалифицировать Adapter/Sandbox и, только при подтверждённом effective cost `0 ₽`, развернуть и подключить минимальный Reg.cloud virtual server через controlled sandbox.

При каждом продолжении выдавай current HEAD, R4 ancestry check, worktree, autonomous process state, active/completed wave, cloud gate, exact evidence, tests, commit SHA(s) и blockers. Не выдумывай результаты.
