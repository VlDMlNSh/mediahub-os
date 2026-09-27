# P1.7 — Native Codex / Claude Launch Specification Verification — 2026-09-21

## Scope

Qualify the repository-native Codex and Claude launch specifications without bypassing the existing Cloud Development Adapter, Sandbox, egress gate, credential broker, model registry, provenance and authorization boundaries.

## Deterministic local acceptance

Verified the existing launch and adapter contract surfaces with:

`pytest -q tests/security/test_native_agent_launcher.py tests/ops/test_cloud_development_adapter.py tests/ai/test_hybrid_dispatcher.py tests/ai/test_godmode_openrouter_launcher.py`

Result: **41 passed in 1.30s**.

The verified surfaces cover native Codex/Claude command construction, provider/model qualification, credential separation, endpoint validation, adapter admission/execution boundaries, dispatcher policy/provenance, and launcher behavior.

## Credential / live-execution boundary

No provider credential was acquired or materialized for this qualification. No live Codex or Claude execution was performed. Existing repository evidence records native E2E as credential-gated; deterministic local qualification does not convert that gate into live-provider authorization.

## Authority boundary

Codex and Claude remain execution peers behind the MediaHub adapter boundary. They do not receive State Authority, release authority, production authorization, or implicit repository mutation authority.

## Disposition

`P1.7 = QUALIFICATION-CANDIDATE / DETERMINISTIC LOCAL ACCEPTANCE PASS`

Live provider qualification remains blocked until legitimate provider credentials/authentication and explicit operational authorization exist.

No release, production, R4 mutation, merge, or force-push was performed.
