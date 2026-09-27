# MediaHub Native Component Architecture

Status: DESIGN-QUALIFIED / IMPLEMENTATION-WAVE-01
Date: 2026-09-09

This document applies ADR-002: prior art MUST be inspected before implementing a new component.

## 1. Native component map

| Component | Native responsibility | Prior art inspected | Decision |
|---|---|---|---|
| provider_registry | provider identity, lifecycle, metadata | OmniRoute, LiteLLM, Bifrost | REIMPLEMENT |
| canonical_protocol | internal request/response/error model | Bifrost, LiteLLM, OpenAI/Anthropic patterns | REIMPLEMENT |
| provider_adapter | protocol translation per provider | Bifrost, LiteLLM, OmniRoute | REIMPLEMENT |
| capability_matrix | protocol/model/provider capability truth | LiteLLM, Bifrost, OmniRoute | REIMPLEMENT |
| routing_engine | deterministic provider selection | LiteLLM, Bifrost, OmniRoute | REIMPLEMENT |
| retry_engine | bounded retry/failover semantics | LiteLLM, Bifrost | REIMPLEMENT |
| circuit_breaker | provider health/cooldown | Bifrost, LiteLLM | REIMPLEMENT |
| policy_engine | authorization and fail-closed policy | OPA | USE/REFERENCE |
| credential_broker | scoped credential injection | LiteLLM, OmniRoute | REIMPLEMENT |
| egress_controller | destination allowlist and network boundary | Firecracker, gateway patterns | REIMPLEMENT |
| provenance_ledger | source/request/result provenance | Cosign, OpenTelemetry patterns | REIMPLEMENT |
| audit_ledger | security and operational audit events | OmniRoute, OpenTelemetry | REIMPLEMENT |
| sandbox | process/filesystem isolation | Firecracker, Codex | REIMPLEMENT/USE |
| agent_orchestrator | deterministic agent lifecycle | LangGraph, PydanticAI, Codex | REIMPLEMENT |
| mcp_boundary | tool/protocol boundary | MCP SDKs | REFERENCE/VENDOR |
| observability | traces, metrics, logs | OpenTelemetry Collector | USE |
| artifact_trust | artifact signature/provenance verification | Cosign | USE |
| secret_scanning | repository credential detection | Gitleaks | USE |
| static_security | SAST/security rules | Semgrep | USE |
| fuzzing | continuous robustness testing | OSS-Fuzz | REFERENCE/USE |
| dependency_maintenance | controlled dependency updates | Renovate | USE |

## 2. Prior-art findings

### Bifrost

The inspected project presents a single gateway over many providers and explicitly combines provider abstraction with automatic failover and load balancing. Its source ecosystem also contains provider-specific implementations, protocol conversion, and cooldown behavior. The useful lesson is to keep provider-specific behavior behind explicit adapters and make resilience provider-aware rather than treating every upstream as identical. MediaHub will reproduce the contract, not the Bifrost architecture.

### LiteLLM

The inspected router implementation centralizes routing strategies, credential access, timeout resolution, sensitive-data masking and multiple routing policies. The useful lesson is that routing, credential handling, timeout policy and observability must be explicit concerns rather than incidental HTTP forwarding. MediaHub will use a much smaller native contract and preserve fail-closed policy boundaries.

### OmniRoute

The inspected provider-management route demonstrates provider registries, provider-specific normalization, compatibility classification, validation, management authorization, audit context, secret masking, model discovery and defensive handling of internal synchronization. The useful lesson is that provider management needs lifecycle validation, secret minimization and auditability. MediaHub will avoid coupling product authority to a UI/API implementation.

### Firecracker

The inspected VMM source demonstrates a deliberately narrow lightweight microVM boundary and explicit resource/rate-limiting concerns. MediaHub will use the isolation principle where stronger execution isolation is required instead of copying its VMM implementation.

### OpenTelemetry Collector

The inspected receiver contract separates ingestion, translation into an internal representation, processing and exporting through explicit pipelines. MediaHub adopts this architectural lesson for observability: collect -> normalize -> process -> export, with stable internal contracts.

### Cosign

The inspected project treats artifact signatures and verification as infrastructure rather than an application afterthought. MediaHub adopts signature/provenance verification as a first-class supply-chain gate.

### Gitleaks

The inspected project provides repository/file/stdin secret detection and documents security-maintenance status. MediaHub uses secret scanning as an external gate and does not embed its detection engine into Product without a separate qualification decision.

## 3. MediaHub invariants

Every native component MUST preserve:

- fail-closed behavior on ambiguous authorization;
- least-privilege credential access;
- no secrets in ordinary logs;
- deterministic routing decisions;
- explicit capability checks before dispatch;
- provider independence;
- bounded retries and timeouts;
- provenance for externally influenced results;
- immutable R4 qualification objects;
- testable contracts independent of concrete providers.

## 4. Implementation order

Wave 1: canonical protocol + capability matrix + provider adapter contract.

Wave 2: provider registry + routing + retry + circuit breaker.

Wave 3: policy + credential broker + egress + provenance/audit.

Wave 4: sandbox + agent orchestration + MCP boundary.

Wave 5: observability + artifact trust + security/fuzzing/maintenance gates.

No production gateway cutover is authorized by this document. Each wave requires its own tests and qualification evidence.

## 5. Mandatory evidence ledger

For every component implementation, record: repositories inspected; exact revisions/files where relevant; license; strengths; weaknesses; extracted patterns; rejected patterns; MediaHub-specific design; security assumptions; tests derived from prior art; and final implementation decision.
