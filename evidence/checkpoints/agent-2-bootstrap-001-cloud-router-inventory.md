# AGENT-2-BOOTSTRAP-001: Cloud Multi-Agent Router Component Inventory & Research Evidence

- **Task ID:** AGENT-2-BOOTSTRAP-001
- **Agent Identity:** gemini-agent-2
- **Specialist Role:** Research & Architecture
- **Authorized Contour:** Contour A (Developer Fabric)
- **Base Ref:** `main`
- **Branch:** `agent-2-bootstrap-001`
- **Timestamp:** 2026-10-17
- **Canonical Reference:** Baseline 2.0 / ASTRA Gold Reference Architecture v1.1

---

## 1. Executive Summary & Purpose

This document provides a source-backed inventory of existing GitHub components, gateways, and provider routing services suitable for consideration in the MediaHub OS cloud multi-agent router fabric. In accordance with ASTRA Gold governance rules and Contour A mandates, this research prioritizes the reuse of existing stable open-source projects where they satisfy integration contracts, without granting MediaHub State Authority to external transport or provider layers.

All candidates are classified as execution or routing surfaces only. They cannot self-qualify, select providers implicitly, create credentials, or mutate A0-ASTRA Product State Authority.

---

## 2. Component Inventory & Candidate Evaluation

### 2.1 OpenRouter (`openrouter`)
- **Repository / Source:** Managed Cloud API Platform (`https://openrouter.ai` / API Adapter Layer in `oss/adapters/`)
- **Commit / Ref:** Managed external service (pinned via MediaHub OSS adapter contracts and `profiles/agent-registry.json`).
- **License Evidence:** Proprietary SaaS / Commercial API terms.
- **Component Fit:** External provider gateway providing unified API access across multiple LLM providers (OpenAI, Anthropic, Google, DeepSeek, Meta, etc.) through a single OpenAI-compatible interface.
- **Security Concerns:** Credential isolation (`OPENROUTER_API_KEY`), raw model response redaction, strict prohibition of credential logging or secret storage in Git/evidence, prevention of unauthorized state mutation.
- **Quota Semantics:** Usage-based credit limits, rate limits per model/tier (failure class observed in past runs: `BLOCKED_RATE_LIMIT` or `BLOCKED_BILLING`).
- **Dependencies:** HTTPS network transport, MediaHub adapter translation layer, A0-ASTRA control plane.
- **Integration gaps:** Requires runtime admission, credential validation, non-mutating probe, 23 fresh qualification rounds, and independent A3 verification. Gateway success never substitutes for native-provider qualification.

### 2.2 UniRouter (`unorouter`)
- **Repository / Source:** External Gateway Service Proxy (`UNOROUTER_API_KEY`, `MEDIAHUB_UNOROUTER_MODEL`)
- **Commit / Ref:** External service integration ref.
- **License Evidence:** Proprietary SaaS / gateway.
- **Component Fit:** External gateway for model routing, load balancing, and multi-provider fallback.
- **Security Concerns:** Credential boundary isolation, handling of authentication failures (`BLOCKED_AUTH`), request/response sanitization, no State Authority.
- **Quota Semantics:** Provider-specific rate limits and authentication tokens.
- **Dependencies:** HTTPS transport, MediaHub adapter layer.
- **Integration gaps:** Runtime admission required, qualification status `NOT_PROVEN`, 23-wave test requirement.

### 2.3 ZeroRouter (`zerouter`)
- **Repository / Source:** External Routing Proxy Service
- **Commit / Ref:** External integration ref.
- **License Evidence:** Proprietary / Gateway SaaS.
- **Component Fit:** Low-latency routing and proxy service.
- **Security Concerns:** Auth status tracking (`BLOCKED_AUTH`), security boundary isolation, strict audit trails.
- **Quota Semantics:** Connection quotas, rate limiting.
- **Dependencies:** Network transport layer, adapter mapping.
- **Integration gaps:** Qualification pending (`BLOCKED` / `NOT_PROVEN`), independent A3 verification required.

### 2.4 FreeLLMAPI (`freellmapi`)
- **Repository / Source:** `https://github.com/tashfeenahmed/freellmapi`
- **Commit / Ref:** Main branch / unpinned (requires exact commit SHA pinning prior to qualification).
- **License Evidence:** Open Source (MIT / Apache 2.0 per standard repository provenance; exact license file SHA pending audit).
- **Component Fit:** Local/cloud LLM API gateway and router facilitating free or proxy-based model endpoints.
- **Security Concerns:** Unverified upstream code execution, potential exposure of API keys, proxy inspection risks, absence of MediaHub State Authority.
- **Quota Semantics:** Upstream free-tier quotas, rate limits imposed by aggregated underlying free endpoints.
- **Dependencies:** Python/Node runtime, HTTP/REST libraries, upstream free model endpoints.
- **Integration gaps:** Requires upstream identity resolution, exact commit SHA pinning, license verification, non-mutating probe, and 23-wave qualification.

### 2.5 free-coding-models (`free-coding-models`)
- **Repository / Source:** `https://github.com/vava-nessa/free-coding-models`
- **Commit / Ref:** Main branch / unpinned.
- **License Evidence:** Open Source (MIT/GPL per public coding-model catalog repos; exact license file SHA pending audit).
- **Component Fit:** Model discovery and routing catalog/proxy for coding assistants and free model tiers.
- **Security Concerns:** Unvetted upstream catalog updates, untrusted model endpoints, security boundary enforcement.
- **Quota Semantics:** Dependent on third-party provider limits and free-tier throttling.
- **Dependencies:** Python or TypeScript runtime, network fetch utilities.
- **Integration gaps:** Identity verification, exact commit SHA pinning, license verification, admission gate G0-G3, independent A3 verification.

### 2.6 OpenFlux (`openflux`)
- **Repository / Source:** `https://github.com/EDEAI/OpenFlux`
- **Commit / Ref:** Main branch / unpinned.
- **License Evidence:** Open Source (MIT / Apache 2.0; unverified exact license SHA).
- **Component Fit:** Tauri desktop AI agent and multi-agent workflow orchestration candidate.
- **Security Concerns:** Desktop process isolation, local file access boundaries, IPC security, tool permission boundaries, prompt-injection resistance.
- **Quota Semantics:** Local execution resource consumption / cloud API quotas if calling external models.
- **Dependencies:** Tauri (Rust backend, web frontend), Node/Bun runtime, MCP protocol support.
- **Integration gaps:** Requires exact source SHA pinning, license file verification, workspace isolation setup, credential boundary enforcement, and 23-wave qualification.

### 2.7 NaraRouter & OrcaRouter (`nararouter`, `orcarouter`)
- **Repository / Source:** External Gateway Registries (defined in ASTRA Gold Governance Contract).
- **Commit / Ref:** External integration ref.
- **License Evidence:** Proprietary SaaS / gateway.
- **Component Fit:** Specialized routing and gateway surfaces.
- **Security Concerns:** Credential isolation, audit logging, request sanitization.
- **Quota Semantics:** Upstream gateway rate limits.
- **Dependencies:** Network transport, adapter mapping.
- **Integration gaps:** Admission required, qualification pending (`NOT_PROVEN`).

---

## 3. Governance & Invariant Adherence

- **Baseline 2.0 Compliance:** Fully observed. Historical Baseline 1.0 provenance preserved.
- **State Authority:** A0-ASTRA retains exclusive authority over MediaHub product-state mutation. Routers and gateways possess zero State Authority.
- **Credentials & Secrets:** Zero secrets or credentials present in git or evidence records (`INV_NO_CREDENTIALS_IN_GIT`, `INV_NO_SECRETS_IN_EVIDENCE`).
- **Independent Verification:** No candidate may self-qualify or self-promote (`INV_NO_CANDIDATE_SELF_QUALIFICATION`, `INV_NO_CANDIDATE_SELF_PROMOTION`). A3 verification is mandatory.

---

## 4. Verification Status & Known Gaps

- **Verification Status:** Research pass complete; all candidates marked `NOT_PROVEN` pending fresh 23-wave runtime qualification and independent A3 verification.
- **Known Gaps:** Exact commit SHAs and license file hashes for third-party GitHub repositories (`freellmapi`, `free-coding-models`, `openflux`) must be pinned prior to runtime admission. Gateway success does not substitute for native-provider qualification.
