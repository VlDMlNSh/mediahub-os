# MediaHub Prior-Art Ledger — Wave 01

Status: QUALIFIED FOR IMPLEMENTATION
Date: 2026-09-09
Rule: ADR-002 GitHub Prior-Art-First Engineering

## Objective

Qualify the design basis for the first native implementation wave: canonical protocol, capability matrix, and provider adapter contract.

## Evidence matrix

| Area | Prior art | Observed pattern | MediaHub decision |
|---|---|---|---|
| Provider abstraction | Bifrost | provider-specific implementations behind a gateway | REIMPLEMENT native contract |
| Routing policy | LiteLLM | explicit routing strategies and deployment selection | REIMPLEMENT deterministic subset |
| Provider management | OmniRoute | normalization, validation, compatibility classification, audit, secret masking | REIMPLEMENT security-relevant subset |
| Protocol boundary | Bifrost/LiteLLM | translation between provider-specific wire formats | REIMPLEMENT canonical model |
| Capability truth | LiteLLM/Bifrost | provider/deployment-specific routing constraints | REIMPLEMENT explicit matrix |
| Secrets | LiteLLM/OmniRoute | centralized/scoped credential access and masking | REIMPLEMENT broker boundary |
| Isolation | Firecracker/Codex | narrow execution boundary | REIMPLEMENT orchestration contract; USE qualified runtime where appropriate |
| Telemetry | OpenTelemetry Collector | stable internal representation and pipeline stages | USE collector; REIMPLEMENT product event schema |

## Rejected design shortcuts

1. Generic HTTP passthrough as the canonical gateway model.
2. Assuming OpenAI Responses compatibility from Chat Completions compatibility.
3. Treating every provider error as retryable.
4. Embedding provider secrets in routing objects or ordinary logs.
5. Making one external gateway the authority for MediaHub Product.
6. Copying a complete third-party router/gateway architecture.

## Required Wave-01 contracts

### Canonical request

Must carry only normalized fields required by the MediaHub execution contract: request id, model identity, protocol, messages/input, generation controls, tool declarations, metadata, timeout/deadline, and policy context. Provider-specific fields remain inside adapter-owned extension data and cannot silently alter authorization.

### Canonical response

Must normalize output, finish state, usage when available, provider identity, model identity, request id, timing, and provenance. Raw provider payloads are retained only under explicit bounded/debug policy.

### Canonical failure

Must contain provider identity, HTTP/status information when available, normalized failure class, retryability, policy-block indication, safe public message, retry-after when valid, and provenance. Credentials and raw sensitive payloads are excluded.

### Capability matrix

A dispatch is valid only when provider + model + protocol + operation are explicitly qualified. Unknown capability is NOT treated as supported.

### Adapter contract

Adapters translate canonical requests to provider wire format and provider responses/errors back to canonical form. They must declare capabilities, authentication requirements, endpoint constraints, timeout semantics, and supported operations. An adapter cannot bypass policy, credential broker, or egress controls.

## Security-derived tests

- unknown capability => dispatch denied;
- provider-specific protocol mismatch => dispatch denied;
- 401/403/security-policy response => POLICY_BLOCKED, no blind retry;
- transient 408/429/5xx => bounded retry/failover only;
- permanent 4xx => no fallback;
- missing credential => fail closed;
- secret never appears in canonical error/log representation;
- adapter cannot select an unqualified endpoint;
- retry budget and deadline are enforced;
- provenance survives provider failover;
- R4 qualification object remains untouched.

## Qualification conclusion

Wave 01 design is sufficiently constrained to begin native implementation. The implementation must remain independent of OmniRoute, Bifrost and LiteLLM at runtime unless a separate dependency decision is approved. Prior-art evidence is a design input, not a runtime dependency.
