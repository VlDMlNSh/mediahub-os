# MEDIAHUB OS / MEDIAHUB iOS — MASTER CONTINUATION PROMPT
# Checkpoint: 2026-09-23
# Purpose: перенос текущей инженерной истории в новый чат без перезапуска архитектуры.

ПРОДОЛЖАЙ СУЩЕСТВУЮЩИЙ ПРОЕКТ MediaHub OS / MediaHub iOS.
Это НЕ новый проект, НЕ новая архитектура и НЕ новый Control Plane.
Сохраняй все ранее принятые архитектурные решения и контрольные точки.

## 1. МИССИЯ

Продолжать автономную инженерную работу по циклу:

АНАЛИЗ → ИЗМЕНЕНИЕ → ТЕСТ → ИСПРАВЛЕНИЕ → РЕГРЕССИЯ → GITHUB CI → ПОВТОРНЫЙ АНАЛИЗ → QUALIFICATION.

Цель — довести существующую систему до квалификационной точки без известных блокирующих дефектов, не создавая второй оркестратор и не ломая существующие контракты.

## 2. КАНОНИЧЕСКАЯ АРХИТЕКТУРА

USER / ChatGPT
→ ASTRA
→ MEDIAHUB CODEX / POLICY
→ AGENT GATEWAY
→ CLOUD-FIRST ORCHESTRATOR
→ CLOUD PROVIDERS / LOCAL EXTENSIONS
→ MEDIAHUB HARNESS
→ MEDIAHUB OS HOST
→ ARTIFACTS + EVIDENCE + VALIDATION
→ ASTRA
→ ChatGPT / USER

Роли:
- MediaHub Codex — authority / policy.
- Astra — master orchestrator.
- Agent Gateway — delegation boundary.
- CloudFirstOrchestrator — routing/control component.
- Harness — bounded execution layer.
- Ollama — local extension / fallback.
- OpenRouter — primary cloud route.
- GitHub Actions runner — credential execution boundary for cloud relay.
- ChatGPT — operator/client Astra.
- Experiential CLI — optional gateway/local extension, НЕ второй orchestrator.
- unlazy — development/completion-discipline layer, НЕ Control Plane.
- OmniRoute — Claude MCP integration/gateway, НЕ MediaHub Control Plane.
- Claude Code — engineering client/toolchain, НЕ MediaHub orchestrator.
- ClaudeMem — local memory layer for Claude.
- Headroom — context/status layer.
- Task Observer — task-observation skill.

НЕЛЬЗЯ:
- создавать второй Control Plane / orchestrator;
- автоматически создавать или раскрывать API keys;
- хранить API keys в repo, source, .env, task JSON, prompt, argv, logs, artifacts/evidence;
- менять provider/model молча;
- делать production deployment без authorization;
- делать destructive actions;
- делать force-push/reset --hard;
- использовать VPN для обхода региональных ограничений.

Sensitive actions requiring approval:
host_install, credential_change, production_deploy, destructive_action.

## 3. REPOSITORY / GIT

Repository:
github.com/VlDMlNSh/mediahub-os

Branch:
implementation/p0-06-core-runtime-services

Последняя известная опубликованная ветка:
1e027944e9f526a1c8caac946ca084b12c9186bf
security(runtime): harden public webhook targets

Локальный HEAD:
2806bc85c737c5caf8d8d785afa6185414738b16

Локальная ветка ahead 2 относительно origin:
39e6dee security(runtime): harden public webhook targets
2806bc8 security(cloud): finalize relay boundary hardening

НЕ делать destructive reset.
Перед публикацией провести diff/review и CI qualification.

SSH git ls-remote ранее не работает (publickey).
HTTPS GitHub с dev работает без VPN.
Это не блокирует текущий GitHub Actions/HTTPS workflow.

Текущий рабочий tree имеет незакоммиченные untracked компоненты:
.agents/
.claude/skills/
agent/
skills-lock.json
Оценить их принадлежность MediaHub прежде чем коммитить. Не публиковать автоматически.

## 4. КВАЛИФИКАЦИЯ P0-06

Последняя полная опубликованная qualification:
- contract validation PASS
- connector boundary PASS
- host registration PASS
- identity separation PASS
- runtime tests: 93 passed
- compileall PASS
- git diff --check PASS
- bash -n deploy/*.sh PASS
- secret scan PASS
- final wave PASS

Local runtime:
93 tests passed в последней волне.

Без credentials cloud relay с пустым inbox возвращает exit 0 — это НЕ E2E доказательство OpenRouter.

## 5. SECURITY HARDENING

Cloud task envelope:
- MAX_TASK_BYTES = 131072
- strict allowed fields
- model override из task schema удалён
- OpenRouter model выбирается только через MEDIAHUB_OPENROUTER_MODEL runtime env.

Cloud relay filesystem:
- O_NOFOLLOW для result target, где доступно;
- symlink DONE/inbox/task files отвергаются;
- task_id regex [A-Za-z0-9._-]{1,128};
- security regression tests присутствуют.

TinyFish webhook:
- public URL validation;
- запрещены localhost/.local/private/loopback/link-local/multicast/reserved/unspecified;
- webhook требует HTTPS;
- credentials в payload не должны утекать.

Harness:
- PROJECT_ROOT определяется от runtime расположения;
- нет hardcoded /home/mediahub/mediahub-os.

CI:
- GitHub Actions permissions contents: read;
- checkout persist-credentials=false;
- pytest==7.4.4;
- contract/connector/compileall/runtime tests;
- cloud relay без automatic git commit/push;
- evidence scan перед artifact upload.

## 6. OPENROUTER

Canonical configuration:
provider_id=openrouter
priority=5
credential=OPENROUTER_API_KEY
model=MEDIAHUB_OPENROUTER_MODEL
endpoint=https://openrouter.ai/api/v1/chat/completions

OpenRouter — primary cloud route.
Ollama — local extension/fallback.

Пользователь сообщил, что OPENROUTER_API_KEY уже существует в GitHub Actions.
Не раскрывать значение.
Инструментальная GITHUB_SECRET_CONFIRMED ранее не установлена.
GITHUB_RELAY_VERIFIED и E2E_VERIFIED не установлены.
PRODUCTION_READY не установлено.
Не запускать metered OpenRouter без отдельной авторизации/условий workflow.

## 7. OLLAMA / LOCAL ASTRA

Ollama binary установлен:
~/.local/bin/ollama

Ранее подтверждён реальный local runtime:
STATUS=completed
PROVIDER=ollama
OUTPUT_PRESENT=True
EVENTS=9
ERROR=None

Но systemd host stack сейчас НЕ установлен/не запущен.

## 8. HOST mh-dev-01

Device:
mh-dev-01
id=ce4e0915-3e19-4fb8-a73a-88b3c33c12ac
repo=/home/mediahub/mediahub-os

Последняя проверка:
ollama.service = inactive
sentinelx-cloud-core.service = inactive
mediahub-astra.service = inactive
/opt/mediahub/astra = absent
/etc/sentinelx/config.yaml = absent

Preflight PASS.
Install script прошёл статический аудит, но запуск с sudo был заблокирован policy Remote Desktop Commander.

Подготовленная команда установки:
cd /home/mediahub/mediahub-os && bash deploy/preflight-mediahub-astra.sh && bash deploy/install-mediahub-astra.sh

Команда требует sudo/system privilege.
Пытались:
sudo -n bash deploy/install-mediahub-astra.sh
но execution policy Remote Desktop Commander отклонила команду.

НЕ обходить это через su/nested shell/privilege bypass.
Если доступного легитимного privileged execution interface нет, выдать пользователю точную команду для однократного запуска на mh-dev-01. Approval host_install уже был дан пользователем и повторно спрашивать его не нужно.

## 9. CODEX CONFIG

Файл:
~/.codex/config.toml

Уже содержит:

[features.context_management]
experimental_mode = true

Также:
[features]
multi_agent = true

agents.max_threads = 6
agents.max_depth = 1

Codex model provider:
continuum
и profiles opus/kimi/continuum уже настроены.
Не удалять существующие настройки.

## 10. CLAUDE CODE

Claude Code:
2.1.263

Установлен и работает.

OmniRoute:
3.8.50
MCP configured as stdio:
claude mcp add --scope user omniroute -- omniroute --mcp

Последняя проверка:
omniroute: omniroute --mcp - Connected

НЕ использовать OmniRoute как второй MediaHub orchestrator.

ClaudeMem:
13.25.3
local provider mode
cloud sync OFF
worker:
PID 2464056
port 37700
running

Headroom:
0.3.0
binary:
~/.claude/bin/headroom
wired into ~/.claude/settings.json statusLine.
Backup:
~/.claude/settings.json.headroom-backup

Task Observer:
global skill:
~/.claude/skills/task-observer/SKILL.md
PASS

Global Claude instructions:
~/.claude/CLAUDE.md
require task-observer at start of task-oriented sessions.

Claude automation setup:
claude-automation-recommender installed globally.

unlazy:
installed via:
npx skills add Leonxlnx/unlazy --all
installed across detected agents.
Do not execute arbitrary CHECK: commands without explicit review/approval.
unlazy is discipline layer only.

## 11. FREELLMAPI

Official repository:
tashfeenahmed/freellmapi

Local installation:
~/.local/share/freellmapi

HEAD:
b5d8333177cb7521488b6fa7ed89294058c0c029

Build:
npm install PASS
npm run build PASS

npm reported 13 vulnerabilities (1 low, 6 moderate, 6 high).
Do NOT blindly run npm audit fix --force.
Review dependency graph before hardening.

Server:
localhost:3001
PID 2466631
HTTP root = 200
/v1/models without auth = 401, proving endpoint is live and protected.

Encryption key:
~/.config/freellmapi/server.env
permissions 600
directory 700
This is application encryption material, not a provider API key.

UNFINISHED:
- FreeLLMAPI unified API key has NOT been created.
- No provider keys have been added.
- Claude is NOT yet bound to FreeLLMAPI.
Reason: project policy forbids automatic creation of API keys.

Next legitimate step:
user explicitly provides/creates the FreeLLMAPI unified key, then use documented setup:
npx freellmapi setup-claude --url http://localhost:3001 --api-key <UNIFIED_KEY>
Never place the key in repository or prompt.

## 12. EXPERIENTIAL CLI / RUFLO / CADDY / AUTHELIA / NAABU

Previously installed/prepared binaries include:
~/.local/bin/caddy
~/.local/bin/authelia
~/.local/bin/naabu
~/.nvm/.../claude
~/.nvm/.../ruflo
Experiential CLI 0.7.109 installed/prepared.
Treat all as optional supporting tools, not orchestration authority.
Verify current binary health before relying on them.

## 13. CONNECTOR PROFILES

chatgpt-astra:
operator=ChatGPT
transport=github_task_contract
gateway=AstraGatewayRuntime
policy_authority=MediaHub Codex
orchestrator=CloudFirstOrchestrator
local_extension=ollama
cloud_boundary=github-cloud-boundary
secret_handling=never_in_chat_never_in_repository
provider_selection=server_side_only
fail_closed=true

github-cloud-boundary:
execution_location=github-hosted-runner
local_host_credentials=false
task_transport=git_repository
allowed operations:
tinyfish.web.run
openrouter.infer
fail_closed=true

## 14. REQUIRED DEVELOPMENT RULES

Before any substantial task:
1. Invoke Task Observer skill in Claude task-oriented sessions.
2. Inspect relevant current files and git diff.
3. Preserve architecture.
4. Search official documentation for changing third-party APIs.
5. Run focused tests.
6. Run full qualification/regression.
7. Review security implications.
8. Only then publish intended changes.
9. Never expose secrets.
10. Never claim a component is installed/ready without direct verification.

For OpenAI/Codex API-related questions, verify current official OpenAI documentation before making substantive claims.

## 15. CURRENT CHECKPOINT

As of 2026-09-23:

PASS:
- MediaHub contracts
- connector boundary
- runtime tests
- security regression suite
- published-tree qualification
- Ollama local runtime
- Codex context_management experimental_mode
- Claude Code 2.1.263
- OmniRoute 3.8.50 MCP
- ClaudeMem 13.25.3 worker
- Headroom 0.3.0
- Task Observer
- Claude automation recommender
- unlazy
- FreeLLMAPI build and local HTTP service

PARTIAL / PENDING:
- MediaHub host systemd installation
- SentinelX enrollment/config
- MediaHub Astra system service
- FreeLLMAPI unified key
- FreeLLMAPI provider configuration
- Claude → FreeLLMAPI binding
- OpenRouter GitHub secret instrumentally verified
- OpenRouter cloud relay E2E
- production readiness/authorization
- final reconciliation/publication of two local Git commits

BLOCKERS:
1. Host privileged installation is blocked by Remote Desktop Commander command policy; do not bypass.
2. FreeLLMAPI credential setup requires a user-created/provided unified key; do not auto-generate.
3. OpenRouter metered E2E requires appropriate authorization/configuration.

## 16. NEXT AUTONOMOUS WORK ORDER

Continue in this order:

A. Re-run full local qualification and inspect git diff.
B. Review the two local commits against origin; publish only intended security fixes after qualification.
C. Inspect untracked agent/skill files and decide whether they belong in MediaHub repo; do not commit blindly.
D. Verify Claude MCP, Task Observer, ClaudeMem, Headroom and Codex config.
E. Harden/review FreeLLMAPI dependencies without force-upgrading.
F. Prepare exact one-command privileged host installation handoff if tool policy still blocks sudo.
G. Once unified FreeLLMAPI key exists, bind Claude using documented setup and verify end-to-end without leaking key.
H. Once GitHub secret/authorization conditions permit, verify OpenRouter relay E2E.
I. Re-run final qualification and create a new checkpoint.
J. Update this master continuation document with every material state transition.

## 17. CONTINUATION COMMAND

В новом чате считать этот документ канонической контрольной точкой проекта.
Не начинать проект заново.
Не создавать новый Control Plane.
Сначала восстановить состояние по разделам 3, 8, 10, 11 и 15, затем продолжить NEXT AUTONOMOUS WORK ORDER.

## 18. AUTONOMOUS CONTINUATION UPDATE — 2026-09-23 15:32 +03:00

- Local qualification rerun: 192 tests passed.
- Contract validation: PASS (14 contract files; identity separation PASS).
- Connector boundary validation: PASS.
- Runtime compileall: PASS.
- git diff --check: PASS.
- Found CI defect: boundary-guard workflow invoked pytest without PYTHONPATH=runtime, although runtime package is intentionally rooted under runtime/.
- Corrective change applied: `.github/workflows/mediahub-boundary-guard.yml` now runs `PYTHONPATH=runtime python3 -m pytest -q tests/runtime`.
- Untracked `.agents/`, `agent/`, and `.claude/skills/` remain uncommitted pending provenance/ownership review; no blind commit.
- No credentials created, read, or written.
- Next: commit only the reviewed CI correction plus this checkpoint, publish non-destructively, then verify GitHub Actions qualification.

## 19. AUTONOMOUS CONTINUATION UPDATE — 2026-09-23

- Canonical stack qualification completed on mh-dev-01: `deploy/qualify-mediahub-reference-stack.sh` PASS.
- Qualification result: 192 runtime tests passed; 5/5 stability iterations passed; contracts, connector boundary and host registration all PASS.
- Ollama is operational with required `qwen2.5-coder:3b` model verified by preflight.
- Claude Code 2.1.263 verified; Ruflo v3.42.5 MCP connected; ECC Chrome DevTools MCP connected; OmniRoute MCP connected; Experiential CLI present.
- Codex `features.context_management.experimental_mode=true` verified.
- No credentials were created or exposed. Paid cloud remains disabled. Production authorization, SentinelX enrollment, Experiential live gateway and metered OpenRouter E2E remain explicitly unverified.
- Repository secret scan over tracked files found no matching GitHub/OpenAI-style credential patterns.
- Untracked unlazy copies and `skills-lock.json` remain pending provenance review; they were not blindly added to the repository.
- Host installation remains gated by privileged-operation policy. `deploy/preflight-mediahub-astra.sh` is PASS and the repository contains the prepared installation/qualification scripts for dev handoff.
- GitHub publication remains blocked by unavailable repository authentication on the dev shell; no credential workaround was attempted.
- Next: resolve legitimate GitHub write authorization, review unlazy provenance, then prepare/execute privileged dev installation when authorized and available; after installation rerun full qualification and create the next checkpoint.

## 20. AUTONOMOUS CONTINUATION UPDATE — 2026-09-23 15:43 +03:00

- `deploy/install-mediahub-ultimate.sh` executed successfully on mh-dev-01 in user-local mode; no privileged escalation was used.
- Security edge refresh completed: Naabu 2.6.1, Caddy 2.11.4 and Authelia 4.39.28 verified.
- Canonical architecture validation remains PASS: 14 contracts, identity separation, connector boundary and host registration all PASS.
- Native MediaHub Harness PASS.
- Full qualification PASS: 192 runtime tests and 5/5 stability loops.
- Truth-state remains explicit: credentials not created; paid cloud disabled; production authorization, SentinelX enrollment, Experiential live gateway and metered OpenRouter E2E not verified.
- Unlazy provenance remains unresolved: `.agents/skills/unlazy/SKILL.md` and `agent/skills/unlazy/SKILL.md` differ and must not be merged blindly; `.claude/skills/unlazy` points to `.agents/skills/unlazy`.
- Git working tree still has only the previously known untracked unlazy/skills-lock artifacts; no new tracked changes were introduced by the installer.
- Next: resolve legitimate GitHub write authorization; finish unlazy provenance decision; only then publish reviewed changes and perform any remaining credential-dependent E2E checks.

## 21. AUTONOMOUS FULL-WAVE AUDIT — 2026-09-23

- Full preflight + qualification rerun after ultimate installation: `PREFLIGHT=PASS`, `QUALIFICATION=PASS`.
- Runtime remains 192/192 PASS; stability remains 5/5 PASS.
- Local tooling audit: Headroom 0.3.0 present; Task Observer, ClaudeMem and the broader Claude skill suite are installed as skills; Claude settings have ECC and claude-mem enabled; Headroom command is present.
- FreeLLMAPI local runtime is active on localhost port 3001; no credential values were inspected or exposed.
- Ollama remains active on localhost:11434.
- The remaining NOT_VERIFIED states are authorization-dependent rather than local build failures: production authorization, SentinelX enrollment, Experiential live gateway, and metered OpenRouter E2E. GitHub write authorization is also still unavailable from the dev shell.
- No destructive operations, force-pushes, credential generation, or secret disclosure performed.
