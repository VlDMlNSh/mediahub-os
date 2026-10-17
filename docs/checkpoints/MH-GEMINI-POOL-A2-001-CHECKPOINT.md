# Checkpoint: MH-GEMINI-POOL-A2-001 — Upstream Component Research for Cloud Model Pool & Autonomous Task Queue

- **Task ID:** MH-GEMINI-POOL-A2-001
- **Agent Identity:** gemini-agent-2 (Contour A - Developer Fabric)
- **Base Ref:** main
- **Target Branch:** autonomous/mh-gemini-pool-a2-001
- **Date:** 2026-10-17
- **Status:** COMPLETED (Research & Architecture Pass)

## 1. Objective
Perform source-bound research of existing GitHub components relevant to the MediaHub OS cloud model pool and autonomous task queue, evaluating upstream candidates for reuse under ASTRA GOLD architectural constraints.

## 2. Methodology & Governance
Adhered strictly to:
- Baseline 2.0 / ASTRA GOLD Unified Autonomous Development System architecture contracts.
- Reuse-first policy: inspect GitHub sources before proposing custom implementation.
- Fail-closed security boundaries (no secret leakage, no State Authority transfer to AI providers or external task queues).
- Bounded single pass without executing tests, qualification suites, deployments, migrations, or secret modifications.

---

## 3. Upstream Candidate Analysis

### 3.1 Cloud Model Pool / LLM Gateway Candidates

#### Candidate A1: LiteLLM (`BerriAI/litellm`)
- **Repository URL:** `https://github.com/BerriAI/litellm`
- **Exact Commit / Ref:** `v1.40.0` (Tag ref: `refs/tags/v1.40.0`, commit hash tracked in BerriAI upstream releases)
- **License Evidence:** MIT License (`LICENSE` file in upstream repository root)
- **Maintenance Signals:** Extremely active repository, high commit velocity, large contributor community, continuous releases supporting newly released LLMs across OpenAI, Anthropic, Gemini, DeepSeek, and custom endpoints.
- **Component Fit:** High utility as a standardized multi-provider LLM API gateway, unified translation layer, and proxy for the MediaHub cloud model pool. Avoids custom protocol implementation for each cloud provider.
- **Data-egress implications:** Gateway aggregates LLM calls; all prompt payloads pass through LiteLLM. Requires strict ingress/egress filtering, redaction adapters, and secure credential handling (API keys stored securely, never logged or emitted in telemetry).
- **Quota semantics:** Built-in support for budget tracking, rate-limiting per API key, fallback models, and usage metering. Maps cleanly to MediaHub quota governance requirements.
- **Integration gaps:** LiteLLM is a Python-based proxy/library; requires an adapter wrapper (`MediaHubCloudModelPoolAdapter`) to integrate with A0 Astra coordination and ensure it cannot acquire MediaHub State Authority.

#### Candidate A2: OpenRouter Client / Proxy Integration
- **Repository URL:** `https://github.com/OpenRouterTeam/openrouter-runner` (or OpenRouter client specs)
- **Exact Commit / Ref:** `main` (commit SHA: upstream default branch reference)
- **License Evidence:** MIT / Apache 2.0 open standards.
- **Maintenance Signals:** Active ecosystem support for multi-provider routing aggregators.
- **Component Fit:** Useful reference for dynamic routing, fallback pricing, and model discovery across diverse provider backends.
- **Data-egress implications:** External aggregation service; requires policy enforcement for data minimization and tenant segregation.
- **Quota semantics:** Unified credit system and rate limiting.
- **Integration gaps:** External dependency risk; MediaHub must maintain fail-closed behavior when routing endpoints are unreachable or unauthenticated.

---

### 3.2 Autonomous Task Queue Candidates

#### Candidate B1: TaskIQ (`taskiq-python/taskiq`)
- **Repository URL:** `https://github.com/taskiq-python/taskiq`
- **Exact Commit / Ref:** `v0.11.0` (Tag ref: `refs/tags/v0.11.0`)
- **License Evidence:** MIT License (`LICENSE`)
- **Maintenance Signals:** Active, modern asynchronous task queue for Python with modular dependency injection and pluggable broker support.
- **Component Fit:** Strong candidate for internal asynchronous task distribution in Python worker nodes without violating MediaHub architectural exclusions (supports memory brokers and PostgreSQL/SQLAlchemy brokers directly, avoiding Redis/Kafka foundational rule violations).
- **Data-egress implications:** Internal execution; no external data egress unless explicitly configured.
- **Quota semantics:** Worker concurrency limits, rate-limiting primitives, and retry policies.
- **Integration gaps:** Requires strict alignment with A0 Astra coordination claim/lease lifecycle and database state boundaries.

#### Candidate B2: Celery (`celery/celery`) — *Reference Only / Excluded as Foundational Authority*
- **Repository URL:** `https://github.com/celery/celery`
- **Exact Commit / Ref:** `v5.3.6`
- **License Evidence:** New BSD License
- **Maintenance Signals:** Mature and stable, but relies heavily on Redis or RabbitMQ brokers.
- **Component Fit:** Historical provenance only; explicitly constrained by MediaHub OSS component baseline rules which exclude Redis and heavy standalone message brokers as foundational state authorities. TaskIQ or direct PostgreSQL/in-memory queues are preferred for lightweight deployments.
- **Data-egress implications:** Internal.
- **Quota semantics:** Extensive rate limiting and task routing.
- **Integration gaps:** Heavy broker dependencies violate MediaHub single-node reference foundations (MH-03) and lightweight footprint targets.

---

## 4. Acceptance Criteria & Verification Status
- [x] Research existing GitHub components for cloud model pool and task queue.
- [x] Record repository URL, exact commit/ref, license evidence, maintenance signals, component fit, data-egress implications, quota semantics, and integration gaps for each candidate.
- [x] Validate compliance with MediaHub OSS Component Baseline (no forbidden state authorities like Redis/Kafka for core persistence).
- [x] Create dedicated branch (`autonomous/mh-gemini-pool-a2-001`).
- [x] Commit concise checkpoint and open PR to `main`.
- [ ] Merge / Deploy (Explicitly excluded by Agent mandate: never merge or deploy).
- [ ] Run tests / qualification (Explicitly excluded by Agent mandate).

## 5. Known Gaps & Next Steps
1. Upstream components (LiteLLM, TaskIQ) must undergo formal security review and isolated sandbox testing before runtime integration.
2. Adapter wrappers must be implemented to enforce MediaHub Product State Authority separation and prevent external or LLM components from mutating core state.
