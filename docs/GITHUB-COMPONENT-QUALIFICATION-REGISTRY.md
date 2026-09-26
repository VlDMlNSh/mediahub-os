# MediaHub GitHub Component Qualification Registry v1.0

Дата: 2026-09-10
Назначение: единый реестр внешних GitHub-компонентов для MediaHub Product и Autonomous Development.

## 1. Неподвижное правило

MediaHub Product не должен иметь обязательной зависимости от конкретного внешнего AI gateway,
AI provider, agent framework или SaaS. Внешние проекты используются по пяти режимам:

- USE-AS-IS — отдельный изолированный инструмент/сервис;
- BORROW — архитектурный паттерн или алгоритм воспроизводится нативно;
- VENDOR — код допускается к включению после license/SBOM/provenance review;
- REFERENCE — только исследование и тестовые oracle;
- REJECT — не проходит security, maintenance, licensing или architectural gates.

R4 SHA 471f709f5633feab7aeb62dd3ea52effad6d2bc4 остаётся immutable.

## 2. Квалифицированное ядро

| Компонент | Роль | Решение | Лучшее свойство |
|---|---|---|---|
| diegosouzapw/OmniRoute | AI routing | BORROW/REFERENCE | provider registry, local-first gateway, routing/fallback |
| maximhq/bifrost | gateway reference | BORROW/REFERENCE | provider adapters, failover, cooldown, protocol conversion |
| BerriAI/litellm | routing oracle | REFERENCE/BORROW | огромная матрица providers/endpoints, retry/fallback tests |
| openai/codex | coding agent | USE-AS-IS через controlled adapter | локальный агент, sandboxed execution model |
| modelcontextprotocol/swift-sdk | iOS MCP | VENDOR/REFERENCE | официальный Swift client/server и transport/auth model |
| modelcontextprotocol/python-sdk | server/agent MCP | VENDOR/REFERENCE | официальный Python MCP implementation |
| open-policy-agent/opa | policy engine | USE-AS-IS/REFERENCE | декларативная authorization policy |
| firecracker-microvm/firecracker | hostile workload isolation | USE-AS-IS/REFERENCE | lightweight microVM boundary |
| open-telemetry/opentelemetry-collector | observability | USE-AS-IS | vendor-neutral telemetry pipeline |
| sigstore/cosign | supply-chain signing | USE-AS-IS | artifact/image signature verification |
| gitleaks/gitleaks | secret scanning | USE-AS-IS | repository/history secret detection |
| semgrep/semgrep | SAST | USE-AS-IS | structural code rules and CI scanning |
| google/oss-fuzz | fuzzing methodology | REFERENCE/USE-AS-IS where applicable | continuous fuzzing infrastructure |
| langchain-ai/langgraph | agent orchestration | REFERENCE | explicit graph/state orchestration |
| pydantic/pydantic-ai | typed agents | REFERENCE/VENDOR | typed tool/model contracts |
| renovatebot/renovate | dependency maintenance | USE-AS-IS | automated dependency update PRs |

## 3. Gateway evidence

OmniRoute release/v3.8.51 is MIT licensed. Its documented architecture includes provider registry,
custom authentication, local audit trail and security controls. These are design inputs, not automatic
security qualification. See repository evidence and source paths in the accompanying qualification notes.

Bifrost is Apache-2.0 and documents 23+ providers, automatic failover, load balancing, MCP, governance,
observability and secrets management. Its circuit-breaker design supports per-model/per-key state and
header-derived cooldown. This is an excellent reference for MediaHub's native resilience layer.

LiteLLM is MIT outside its enterprise directory, with separate licensing for enterprise content.
Its repository contains router strategies, retry policies and reliability coverage registries. We must
not vendor enterprise content without a separate license review.

## 4. Stable qualities to reproduce natively

### Provider Gateway

- canonical internal request model;
- explicit protocol capabilities;
- provider registry with immutable provider identity;
- OpenAI Responses frontend;
- OpenAI Chat Completions frontend;
- Anthropic Messages frontend;
- provider-specific adapters;
- policy-block classification;
- bounded retry/backoff for transient failures;
- Retry-After aware cooldown;
- circuit breaker and quarantine;
- deterministic failover;
- no retry on permanent policy blocks;
- Local Cluster -> Local AI -> SAFE_STOP degradation.

### Security plane

- credentials only through OS credential injection/broker;
- no secrets in logs, configuration, Git or provenance records;
- explicit egress allowlist;
- policy evaluation before network access;
- per-task capability grants;
- sandbox/worktree path boundary;
- process-group termination on timeout;
- signed build/artifact verification;
- SBOM and dependency provenance;
- secret scanning and SAST gates.

### Autonomous Development plane

- multiple independent agents;
- isolated worktrees;
- parallel qualification;
- deterministic test gates;
- fault injection;
- fuzzing;
- security scanning;
- dependency freshness checks;
- benchmark/regression ledger;
- GitHub PR automation;
- evidence ledger with exact SHA/tree.

## 5. Ready-to-reuse source areas

The following source areas are designated as implementation references, subject to exact commit pinning:

- LiteLLM: `litellm/router_strategy/`, `litellm/router.py`, reliability coverage tests;
- Bifrost: provider implementations, transport layer, converter layer, circuit-breaker implementation;
- OmniRoute: provider registry, provider-node model, auth configuration, routing/fallback implementation;
- Codex: local agent execution boundary and sandbox/tooling architecture;
- MCP Swift SDK: client/server, transports, authentication, cancellation and graceful shutdown;
- OPA: policy evaluation and bundle-based policy distribution concepts;
- Firecracker: microVM lifecycle and isolation model;
- OpenTelemetry Collector: receiver/processor/exporter pipeline model;
- Cosign: signature verification and provenance workflow;
- Gitleaks: secret-detection rules and CI integration;
- Semgrep: structural SAST rules and policy packs;
- OSS-Fuzz: fuzz-target lifecycle and continuous fuzzing methodology;
- LangGraph: explicit state graph orchestration;
- PydanticAI: typed model/tool interfaces;
- Renovate: automated dependency PR workflow.

No external source is copied into MediaHub Product merely because it is useful. Every imported code
fragment must retain attribution/license metadata and pass SBOM, provenance, security and maintenance gates.

## 6. Wave 04C prior-art decision — 2026-09-10

For native Codex/Claude execution, the selected approach is controlled USE-AS-IS execution of the
official CLIs through a MediaHub-native launch contract; no OpenRouter wrapper is accepted as a
native implementation.

- `openai/codex`: USE-AS-IS through `mediahub_native_agent_launcher`; reuse the documented `codex exec`
  CLI surface, model selection and sandbox mode, while keeping MediaHub policy/credential authority outside Codex.
- `anthropics/claude-code`: USE-AS-IS through the same launch contract; reuse the documented print-mode,
  model and structured-output CLI surface, while keeping MediaHub policy/credential authority outside Claude Code.
- `anthropics/sandbox-runtime`: REFERENCE/BORROW candidate for Wave 06 process/filesystem/network isolation;
  not installed and not made an authority dependency in Wave 04C.
- Daytona and E2B remain alternative sandbox-runtime candidates; neither is installed in this wave.

The MediaHub implementation retains only the smallest stable launch contract required to bind agent,
qualified provider/model, HTTPS endpoint, broker-owned credential reference and sandboxed process execution.
