# Wave 263 — Provider registry consumer census and cloud-only compatibility gap (2026-10-20)

## Scope
A bounded read-only census following Wave 262. Preserve the owner-confirmed boundary: Contour A orchestration, workers, coordination, evidence and recovery run only on GitHub-hosted cloud components; local hardware/servers are reserved for later Jarvis/local compute. External model APIs are endpoints only, not an orchestration plane.

## Current refs and evidence
- Canonical map branch: `docs/mediahub-chat-tree-map-20261012`. The canonical map Contents API response returned an empty body despite reporting blob SHA `cae684678cfbe31a88d01d65614420b70dbc7394`; no inference about its content was made and no map overwrite attempted. Wave 262 addendum remains readable and records the boundary.
- Provider/model registry on `main`: `ops/qualification/provider_model_registry.json`, blob `62328126fd2cd8879a73bb6812adcacd3e2abe84`. It has 25 provider entries, including `ollama-local-1` with a localhost endpoint and static bearer value; therefore it is a mixed-scope registry, not a cloud-pool allowlist. Do not consume it directly for cloud dispatch without an explicit eligibility policy and secret/endpoint validation.
- Separate agent catalog on `main`: `profiles/agent-registry.json`, blob `993cbbe1b2b2a88da7d8884a897b404f055981a8`. It contains external, local, local-gateway and local-tooling tiers; it is not interchangeable with the provider/model registry and must not be treated as proof of credentials, availability or qualification.
- Existing provider contract schema: `schemas/ai/ai-provider-registry.schema.json`, blob `9537a64bc948b1bea3e2a640670f48e107760a50`; adapter schema `schemas/ai/ai-provider-adapter.schema.json`, blob `e0dab7002222451579e649a7d1d29985393d9a42`. They describe a separate `mediahub.ai.ai-provider-registry` / `mediahub.ai.ai-provider-adapter` contract, not the `mediahub.provider-model-registry.v1` JSON currently in ops.
- Existing schema tests: `tests/ai/test_ai_provider_registry.py`, blob `5b064c47e54c541f70cc9c314cbec14f64141015`; `tests/ai/test_ai_provider_adapter.py`, blob `bbffbff01460453943742eaa254d401403a5c7da`. These inspect schema shape but do not prove the ops registry validates against those schemas or is consumed by the cloud controller.
- `docs/architecture/MH-21-provider-adapter.md`, blob `d8b61d65435b13202530946687f8c074617f8c67`, remains PROPOSED.
- Issue #301 remains OPEN (last read update `2026-10-20T11:44:18Z]); Draft 2020-12 validation and negative fixtures for task envelope/agent registry/evidence manifest remain open.
- PR #421 remains OPEN/Draft (last read update `2026-10-20T13:07:15Z`). This census does not authorize dispatch or merge.

## Findings
1. There are at least three distinct provider/agent representations with different identifiers, fields and purposes. No evidence from this pass establishes a canonical, validated adapter from the 25-entry ops registry into the AI provider schema or from either catalog into controller dispatch.
2. The ops registry contains a localhost Ollama endpoint and an inline static bearer value. That entry is categorically ineligible for the GitHub-cloud-only pool. Treat this as a configuration hygiene and boundary finding; the value was not used or sent to any endpoint.
3. `cost_class`, `persistence_class`, model lists and credential environment names are declarations, not current quota, credential-access, policy/terms or qualification evidence. Provider calls and secrets were not accessed.
4. Repository tree inventory found the two AI schema tests and the two catalogs named above. Code-search requests returned no indexed results, so this is a file/path-level census, not a complete proof that no other consumers exist. A full consumer census requires targeted source scans in CI or a checked-out repository.
5. No code change is justified until ownership and mapping among these representations is decided. Do not silently merge registries or add an external queue/router/database.

## Recommended next implementation slice
- Add a CI-only contract test that loads the ops registry as data, asserts no cloud-eligible record uses localhost/private endpoints or inline static bearer credentials, and validates its actual schema separately from the existing AI provider registry schema.
- Define explicit `cloud_eligible` / `execution_scope` policy only through the appropriate architecture/governance contract; default unknown/local records to denied.
- Run Draft 2020-12 meta-validation with format assertions and positive/negative fixtures for the Issue #301 task envelope, agent registry and evidence manifest; use mock providers only.
- Inventory actual consumers via reproducible repository-wide source scan and record file paths, not just code-search results.
- Keep GitHub-hosted Actions/runners as the only Contour A execution plane. If GitHub-native state cannot meet a proven lease/queue requirement, record the exact gap and request governance approval before proposing any external service.

## Verification limits
Read-only source review only. No provider API calls, secret access, workflow dispatch, code execution, package installation, server access, merge, deployment, qualification or acceptance occurred. No test result is claimed for this wave.

## Navigation
- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
- Wave 262 boundary report: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/checkpoints/MEDIAHUB-GITHUB-CLOUD-ONLY-POOL-AND-LOCAL-JARVIS-BOUNDARY-WAVE-262-2026-10-20.md
- Issue #301: https://github.com/VlDMlNSh/mediahub-os/issues/301
- PR #421: https://github.com/VlDMlNSh/mediahub-os/pull/421
