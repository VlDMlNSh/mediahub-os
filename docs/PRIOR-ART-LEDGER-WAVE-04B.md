# PRIOR-ART LEDGER — WAVE 04B

Status: QUALIFIED FOR IMPLEMENTATION

## Scope

Native provider execution boundary for OpenAI Responses and Anthropic Messages,
without replacing the currently deployed OpenRouter lane.

## Evidence

- OpenAI documents API-key Bearer authentication and Responses API usage.
- Anthropic documents `x-api-key`, `anthropic-version: 2023-06-01`, and Messages API.
- Current MediaHub wrappers were verified to be OpenRouter-bound and therefore are
  not treated as native provider implementations.

## Implemented

- Native adapter request envelopes.
- Provider-neutral execution target and credential reference.
- Provider-specific authentication header construction.
- Fail-closed model registry.
- Protocol/provider/credential/HTTPS qualification tests.
- No secret persistence in adapter or target objects.

## Explicitly not cut over

The installed Codex/Claude systemd lanes remain unchanged. Native wrappers are not
activated until credential presence, model qualification, endpoint reachability and
sandbox integration are independently verified.

## Required next gates

1. Native wrappers with provider-specific base URLs.
2. Streaming event boundary and bounded response parsing.
3. Provider capability matrix integrated into routing.
4. Credential availability checks without secret disclosure.
5. Direct cloud E2E per provider, otherwise classify POLICY_BLOCKED/UNAVAILABLE.
6. Only after all gates pass: controlled non-R4 branch cutover.
