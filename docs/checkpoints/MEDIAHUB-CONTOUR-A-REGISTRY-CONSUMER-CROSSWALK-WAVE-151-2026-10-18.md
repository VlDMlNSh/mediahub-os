# Contour A registry consumer crosswalk — Wave 151 — 2026-10-18

## Purpose
Advance Wave 150 by inspecting the current main-branch consumers of existing provider registry artifacts. This is a source-only pass; no registry was changed.

## Source snapshot
- `main`: `c06015e0b1526e0aaa6a522306052b077455aba5`.
- `ops/qualification/qualify_execution_backends.py`, blob `acf092d5dd9d67ab187f1b67ab691ca730028306`.
- `ops/qualification/provider_model_registry.json`, blob `62328126fd2cd8879a73bb6812adcacd3e2abe84`.
- `profiles/agent-registry.json`, blob `993cbbe1b2b2a88da7d8884a897b404f055981a8`.
- `schemas/ai/ai-provider-registry.schema.json`, blob `9537a64bc948b1bea3e2a640670f48e107760a50`.
- `schemas/ai/ai-provider.schema.json`, blob `364a1aed7a8ff14b382aad0eab4ec0b5d5a55347`.
- `schemas/ai/ai-provider-adapter.schema.json`, blob `e0dab7002222451579e649a7d1d29985393d9a42`.
- `tests/ai/test_ai_provider_registry.py`, blob `5b064c47e54c541f70cc9c314cbec14f64141015`.
- `tests/ai/test_ai_provider.py`, blob `e9389284c326c7fbc6309ecfe45858901816d765`.
- `tests/ai/test_ai_provider_adapter.py`, blob `bbffbff01460453943742eaa254d401403a5c7da`.
- `tests/test_provider_qualification_classification.py`, blob `6ce80170180a8741f83109c04d1484f289753114`.
- `main:.github/workflows/astra-provider-qualification.yml`, blob `d3160088fbef4fce152ed7335f0acaa3bb440378`.

## Field-level initial crosswalk

| Artifact | Observed consumer / purpose | Data it can govern | It does not prove |
|---|---|---|---|
| `ops/qualification/provider_model_registry.json` | Read directly by `ops/qualification/qualify_execution_backends.py`; invoked by provider-qualification workflow | Candidate providers, models, endpoint and credential environment-variable names used by bounded live qualification | Current quota entitlement, accepted A0 issuer authority, permission to dispatch arbitrary tasks, or route safety |
| `schemas/ai/ai-provider-registry.schema.json` | `tests/ai/test_ai_provider_registry.py` asserts schema metadata and fields | Structural contract for provider-selection records: provider ID, enabled flag, priority and selection policy | Authorization envelope, egress policy, provider account entitlement or registry instance data |
| `schemas/ai/ai-provider.schema.json` | `tests/ai/test_ai_provider.py` checks schema contract | Provider/model declaration, capabilities, authentication mode and availability state | Successful runtime connectivity or qualification; schema field `available` is not live proof |
| `schemas/ai/ai-provider-adapter.schema.json` | `tests/ai/test_ai_provider_adapter.py` checks adapter contract | Adapter/provider identity, operations, capabilities and lifecycle/availability states | Provider authorization, model quota or trusted worker identity |
| `profiles/agent-registry.json` | Source inventory identifies agent catalog v1.2.0; consumer mapping is not yet fully proven by source search | Declared agent IDs, capability labels, activation hints and non-secret credential env names | Active runtime, authenticated session, route entitlement or qualification; `enabled: true` is not sufficient |
| Proposed cloud-agent registry v0.2 on docs branch | Source-only candidate contract; its own comment says status values are descriptive and requires accepted A0/MH-12/R-06 validation | Intended per-agent identity, model/provider route, scope, lifecycle and evidence references | Runtime authorization until governance, verifier and policy integration are accepted |

## Findings
1. The qualification workflow injects many provider credentials as runtime environment variables, checks out the caller-supplied target SHA and executes the provider qualification script on a self-hosted `mediahub-provider` runner. This workflow is not equivalent to GitHub-hosted ephemeral worker qualification and must not be conflated with the preferred target architecture.
2. The qualification script reads `ops/qualification/provider_model_registry.json` as its direct selection input. Therefore provider labels in that file can affect which live endpoints are probed; stale `cost_class`/ `persistence_class` values are operationally consequential and must be re-verified before enabling fallback.
3. The three `schemas/ai` test files inspect schema structure and metadata. The inspected tests do not establish that a runtime provider registry instance conforms to these schemas or that a provider is authorized.
4. GitHub code-search returned no indexed matches for registry references; that search result is inconclusive. This pass verified direct use in the qualification script and test files only; a complete writer/reader inventory still requires a local clone or full source traversal.
5. Do not merge `profiles/agent-registry.json`, qualification routing, provider-selection schema and proposed cloud-agent authorization records into one registry. Keep authorization, runtime availability, provider quota and model preference as separate data domains with explicit source-of-truth ownership.

## Next executable step
1. Inspect the full qualification script for candidate selection, status semantics, fallback behavior, endpoint requests, and output sanitization; inspect workflow trigger/caller boundaries and permissions.
2. Build a writer/reader inventory for `profiles/agent-registry.json` and the `schemas/ai` contracts using full repository traversal rather than relying on code-search indexing.
3. Compare actual schema validation in CI against Draft 2020-12 meta-validation, format assertions and positive/negative fixtures. If missing, prepare a dedicated test-only PR; do not modify provider entries yet.
4. Keep all provider routes BLOCKED until official current documentation, account/project entitlement, data policy, budget, retry/circuit-breaker behavior and negative tests are evidenced.

## Safety boundary
No credential values were read; no provider API/model was called; no worker dispatch, merge, deployment or qualification occurred. Contour A remains NOT QUALIFIED / NOT DEPLOYED / NOT INDEPENDENTLY ACCEPTED. Contour B remains blocked.
