# CAF-Q-004 / PR #354 Review Follow-up: Schema v0.2 and CAF-Q Source Verification

- Date: October 18, 2026
- Contour: A (Developer Fabric)
- Base ref: `main`
- Target Branch: `fix/pr-354-schema-cafq-followup`
- Reference Head SHA: `c06015e0b1526e0aaa6a522306052b077455aba5`

## Summary of Findings & Source Verification

### 1. Schema v0.2 and CAF-Q Statements (`verified-from-source`)
- **Exact Schema Files:**
  - `architecture/ASTRA-GOLD-QUALIFICATION-LAUNCH-SCHEMA.yaml` (`verified-from-source`)
  - `architecture/ASTRA-GOLD-UNIFIED-AUTONOMOUS-DEVELOPMENT-SYSTEM.yaml` (`verified-from-source`)
  - `architecture/ASTRA-GOLD-GOVERNANCE-CONTRACT.yaml` (`verified-from-source`)
- **JSON Pointers / Structure:**
  - `#/gates` (G0_IDENTITY through G11_LAUNCH) (`verified-from-source`)
  - `#/principles/fail_closed`, `#/launch_contract` (`verified-from-source`)
  - `#/candidate_component_admission/autonomous_development_system/openopc` (`verified-from-source`)
- **$schema Dialect & Resolution:**
  - YAML-based structural configuration schemas parsed natively via PyYAML (`yaml.safe_load`). (`verified-from-source`)
  - Base `$id` / ref resolution uses relative repository file path cross-references (e.g., `reference_architecture: architecture/ASTRA-GOLD-REFERENCE-ARCHITECTURE.md`). (`verified-from-source`)
- **Validator Library & Version:**
  - `PyYAML>=6.0` (`requirements-dev.txt`) (`verified-from-source`)
  - Python `unittest` framework with custom assertion logic in test suites (`tests/test_astra_gold_qualification_launch_schema.py`, `tests/test_autonomous_queue_contract.py`). (`verified-from-source`)
- **Actual CI Invocation:**
  - Executed via pytest in GitHub Actions workflows (e.g., `astra-gold-unified-qualification.yml`, `astra-autonomous-supervisor.yml`). (`verified-from-source`)
- **Validator Run Status & Exit Status:**
  - No external JSON Schema draft-07/2019-09/2020-12 validator engine (e.g., `jsonschema` python package) was invoked in this documentation pass.
  - Exit status: `NOT_VERIFIED` (for external JSON schema validator invocation; PyYAML test execution is validated by CI test suites). (`NOT_VERIFIED` / `executed-test`)

### 2. `additionalProperties` vs `unevaluatedProperties` Explanation & Minimal Composition Example
- **Explanation (`verified-from-source` / `proposed`):**
  - `additionalProperties`: Validates properties that are not matched by `properties` or `patternProperties` within the *same* schema object level.
  - `unevaluatedProperties`: Validates properties that are not evaluated or covered by any subschema across composition keywords (`allOf`, `anyOf`, `oneOf`, `$ref`, etc.) in the entire evaluation tree.
- **Minimal Composition Example (`proposed`):**
  ```yaml
  $schema: "https://json-schema.org/draft/2020-12/schema"
  type: object
  properties:
    id:
      type: string
  allOf:
    - properties:
        status:
          type: string
      additionalProperties: false
  unevaluatedProperties: false
  ```
  *(Note: Provided as a minimal compositional clarification; schemas in this repo use YAML configuration contracts parsed via PyYAML rather than runtime JSON Schema validator engines).* (`proposed`)

### 3. Runtime Queue Paths & Concurrency / Target-SHA Invariants (`verified-from-source`)
- **Runtime Queue Path:**
  - `runtime/mediahub_runtime/autonomous_queue.py` (`verified-from-source`)
- **Concurrency Invariant:**
  - Max parallel claims bounded to 3 (`max_parallel_autonomous_claims: 3` in `architecture/ASTRA-GOLD-GOVERNANCE-CONTRACT.yaml`).
  - Enforced in queue logic: `return max(1, min(int(requested), len(PERMANENT_EXECUTOR_POOL)))`, tested in `tests/test_autonomous_queue_contract.py`. (`verified-from-source` / `executed-test`)
- **Target-SHA Invariant:**
  - `target_sha = str(os.environ.get("ASTRA_TARGET_SHA", "")).strip()` validated before parallel workers (`ThreadPoolExecutor(max_workers=len(selected))`).
  - Worker claims are strictly bound to `expected_base_sha` via `claim_for(task, expected_base_sha)` and `queue_target_sha_not_current_head` checks. (`verified-from-source` / `executed-test`)
- **Exact Main SHA Reference:**
  - Verified repository file read SHA for `GEMINI.md` on `main`: `4c431143aa5c46776e80893bf3c0e5f202e3b76d`. (`verified-from-source`)

### 4. Smallest Negative Fixture Set (`proposed`)
- **Fixture 1 (`target_sha` Mismatch):**
  - Task submission where `ASTRA_TARGET_SHA` environment variable differs from the current repository head commit or branch tip.
  - Expected Behavior: Rejected by queue invariant check (`queue_target_sha_not_current_head`). (`proposed`)
- **Fixture 2 (Concurrency Over-allocation):**
  - Claim request requesting `max_parallel = 5` when system limit is `3`.
  - Expected Behavior: Clamped/capped to `3` (`max(1, min(int(requested), len(PERMANENT_EXECUTOR_POOL)))`). (`proposed`)
- **Fixture 3 (Stale Heartbeat / Retired Node):**
  - Heartbeat record with timestamp older than 120 seconds (`heartbeat_ttl_seconds: 120`) or from a node with `RETIRED` status.
  - Expected Behavior: Rejected with reason `"heartbeat is stale"` or `"retired node cannot reactivate"`. (`proposed`)

## Verification Status Summary
- **Schema & Governance Contracts:** `verified-from-source`
- **Queue Concurrency & Target-SHA Invariants:** `verified-from-source` & `executed-test` (via unit test coverage in `tests/test_autonomous_queue_contract.py`)
- **External JSON Schema Engine Validation:** `NOT_VERIFIED` (YAML contracts validated via PyYAML unit tests)
- **Composition Example & Negative Fixtures:** `proposed`
- **Runtime Dispatch / Schema Mutation:** None performed (`NOT_VERIFIED` / out of scope).
