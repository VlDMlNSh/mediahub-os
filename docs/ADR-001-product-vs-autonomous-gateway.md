# ADR-001: MediaHub Product vs Autonomous Development Gateway

## Status
Accepted — 2026-09-09.

## Decision
MediaHub Product owns the security boundary and canonical provider gateway.
Third-party gateways are permitted in Autonomous Development only.

## Product invariants
- Localhost-only frontend; no client direct cloud egress.
- Provider selection is capability-aware and fail-closed.
- Credentials arrive through the credential broker / systemd LoadCredential.
- 401/403 policy failures are quarantined; they are not retry storms.
- 429/5xx/timeouts are bounded transient failures.
- Cloud exhaustion falls back to Local Cluster, then Local AI, then SAFE_STOP.
- R4 qualification object remains immutable.
- No provider-specific gateway becomes a product architectural dependency.

## Qualified protocol surface
- OpenAI Responses: only explicitly qualified adapters.
- OpenAI Chat Completions: only explicitly qualified adapters.
- Anthropic Messages: only explicitly qualified adapters.
- Provider adapters own endpoint translation and response normalization.

## Ecosystem use
OmniRoute, Bifrost and LiteLLM are reference implementations for routing,
provider adapters, retries, circuit breakers, protocol conversion and tests.
Their code may be evaluated or selectively reimplemented, but Product must
remain operational if any one of them disappears.

## Consequence
The current native gateway HTTP prototype is not production-installed yet.
Before cutover it must gain packaged install paths, complete protocol adapters,
provider credential availability checks, provenance/audit integration, and
fault-injection coverage.
