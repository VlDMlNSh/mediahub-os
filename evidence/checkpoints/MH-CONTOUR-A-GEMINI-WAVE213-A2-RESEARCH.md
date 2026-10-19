# MH-CONTOUR-A-GEMINI-WAVE213-A2 — Runner Target Manifest & Schema Validation Research

**Task ID:** `MH-CONTOUR-A-GEMINI-WAVE213-A2`  
**Agent Identity:** `gemini-agent-2`  
**Credential Reference:** `GEMINI_API_KEY_2`  
**Authorized Contour:** `Contour A (Developer Fabric)`  
**Base Ref:** `main` (SHA: `1363c03f0168c6371332095d38a410974a875815`)  
**Date:** 2026-10-19  
**Status:** RESEARCH_COMPLETE / DOCUMENTATION_ONLY  

---

## 1. Executive Summary & Scope

This research document records the findings for **MH-CONTOUR-A-GEMINI-WAVE213-A2** (Runner target manifest and schema validation research). In accordance with Gemini Agent 2 mandates, this pass is strictly limited to research, architecture analysis, and evidence documentation. No functional production code, schemas, or workflow definitions have been modified.

---

## 2. Authoritative Schema & Manifest Inventory

Through direct inspection of the canonical repository structure on `main`, the following authoritative components were identified:

1. **Canonical Schema Tree (`schemas/`)**:
   - Sole canonical source established following audit defect **D2** resolution (removing legacy duplication in `contracts/`).
   - Validated via `tools/validate_contracts.py`, which enforces JSON Schema Draft 2020-12 (`https://json-schema.org/draft/2020-12/schema`), `$id` presence, and common metadata envelopes (`schema_id`, `schema_version`, `owner`).
   - Strict identity boundary separation enforced (`schemas/identity/identity-boundary.schema.json`), verifying canonical IDs (`device_id`, `binding_id`, `adapter_id`, `adapter_instance_id`, `capability_id`, `event_id`, `command_id`, `execution_id`, `request_id`, `correlation_id`, `causation_id`, `recovery_id`) and explicitly prohibiting `universal_id`.

2. **Agent Registry (`profiles/agent-registry.json`)**:
   - `schema_id`: `mediahub.ai.agent-registry`
   - `schema_version`: `1.2.0`
   - Defines registered AI models, external gateways (`unorouter`, `openrouter`, `claude`, `gemini`, `perplexity`, `kimi`, `deepseek`, `chatgpt`), local tooling (`codex`, `cursor`, `claude-code`, `deepseek-harness`, `stagewise`), auxiliary support (`ecc`, `delx-memory-bun`), and review/qualification candidates (`openopc`, `openflux`, `sol-pi`, `colibri`, `webtool-deepseek`, `minicpm-v-4.5-8b-1mk`, `free-coding-models`, `freellmapi`, `unlazy`, `naabu`, `codex-chatgpt-web`).
   - Enforces the invariant: **Registration or credential reference never implies successful authorization or execution authority.**

3. **Qualification & Launch Gates (`architecture/ASTRA-GOLD-QUALIFICATION-LAUNCH-SCHEMA.yaml`)**:
   - Defines G0 through G11 gates (G0 Identity, G1 Boundary, G2 Control Plane, G3 Execution Path, G4 23-Wave Qualification, G5 Concurrency, G6 Recovery, G7 Integrated A3, G8 Pre-Soak, G9 24h Soak, G10 Launch Ready, G11 Launch).
   - Enforces fail-closed behavior, fresh evidence requirements, and A3 verification independence.

4. **Evidence & Verification Frameworks (`ops/qualification/`)**:
   - `verify_execution_backends.py`: Validates `mediahub.execution-backends.v1` evidence payloads, ensuring node binding, `VERIFIED` state across required backends (`codex`, `cursor`), repository revision matching, and secret value suppression.
   - `verify_pre_soak_bundle.py`: Validates pre-soak bundles (`mediahub.pre-soak-evidence.v1`) against freshness windows (900s TTL), target SHA matching, and node ID binding.
   - `verify_g4_115.py` / `tests/test_astra_gold_evidence_contracts.py`: Validates 115-round G4 qualification matrices (23 fresh rounds across 5 mandatory paths: `CODEX_FCC`, `CLAUDE_FCC`, `CODEX_OMNIROUTE`, `CLAUDE_OMNIROUTE`, `CLAUDE_CODE_DIRECT`).

---

## 3. Validation Infrastructure & Test Coverage

- **JSON Schema Draft 2020-12 Validation**: `tools/validate_contracts.py` acts as the canonical contract linter.
- **Negative Fixtures & Boundary Tests**:
  - `tests/test_astra_gold_evidence_contracts.py`: Tests missing rounds, transport mismatches, and A3 dependencies.
  - `tests/test_pre_soak_evidence_contract.py`: Tests stale bundles, incorrect target SHAs, and node ID mismatches.
  - `tests/test_verify_execution_backends.py`: Tests revision mismatches, missing backends, unverified states, non-PASS status rejection, and secret leak detection (`SUPPRESSED` enforcement).
  - `tests/test_astra_gold_governance_contract.py`: Locks governance contracts, numeric thresholds, invariant registries, and generated current truth (`CURRENT-TRUTH.generated.md`).

---

## 4. Issue #301 Dependencies & Smallest Implementation Sequence

1. **Dependency Analysis**: Issue #301 / Defect D2 established that all schema definitions reside strictly under `schemas/` and are validated by `tools/validate_contracts.py`. Any target manifest or task envelope extensions must build upon the existing Draft 2020-12 infrastructure and metadata envelope contract.
2. **Smallest Implementation Sequence**:
   - **Step 1 (Schema Definition)**: Define/extend target manifest or task envelope schemas under `schemas/core/` adhering to Draft 2020-12 and including the required metadata envelope (`schema_id`, `schema_version`, `owner`).
   - **Step 2 (Contract Validation Integration)**: Ensure `tools/validate_contracts.py` automatically picks up and validates the new schema files.
   - **Step 3 (Verification & Negative Testing)**: Implement dedicated unit tests under `tests/` verifying schema compliance, negative fixtures (malformed payloads, missing required fields, invalid versions), and fail-closed behaviors.
   - **Step 4 (Evidence Generation)**: Generate cryptographically bound execution and qualification evidence records matching the schema requirements.

---

## 5. Acceptance Criteria & Verification Status

| Acceptance Criterion | Status | Verification Reference |
|---|---|---|
| Locate authoritative schemas & manifests | **PASS** | `schemas/`, `profiles/agent-registry.json`, `architecture/` |
| Check Draft 2020-12 validator & negative fixtures | **PASS** | `tools/validate_contracts.py`, `tests/test_*.py` |
| Propose smallest implementation sequence | **PASS** | Documented in Section 4 |
| Dedicated branch & Draft PR | **PASS** | Branch `gemini-agent-2/mh-contour-a-wave213-a2-research` |
| Documentation / evidence only (no code mutation) | **PASS** | Strictly adhered to (no production code changed) |

---

## 6. Known Gaps & Constraints

- Live execution runners on `mh-dev-01` require explicit local environment preparation and credential provisioning outside Contour A scope.
- Automated qualification runs in CI require fresh evidence bundles (`fresh_evidence_required: true`); historical evidence reuse is strictly prohibited.
