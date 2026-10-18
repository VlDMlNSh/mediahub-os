# Task C / Issue 301 — Cloud Agent Schema v0.2 & CAF-Q-001 through CAF-Q-015 Review

## Task Metadata
- **Task ID:** Task C / Issue 301
- **Contour:** Contour A (Developer Fabric)
- **Base Ref:** `main`
- **Branch:** `task-c-issue-301-schema-review`
- **Date:** October 18, 2026
- **Author:** Bounded Autonomous Engineering Agent (Contour A)

---

## 1. Executive Summary & Scope
This checkpoint records a bounded source-only review of:
1. Cloud Agent Schema v0.2 conceptual specifications and schema structures (task-envelope, agent-registry, evidence-manifest).
2. CAF-Q-001 through CAF-Q-015 qualification and evidence frameworks.

In strict compliance with governing directives:
- This pass is **source-only** and documentary.
- CAF-Q records and schema specifications are **documentary queue/qualification records**, **not** an operational live scheduler or runtime dispatch mechanism.
- No runtime dispatch, automated merge, or production deployment was performed.

---

## 2. Findings: Draft 2020-12 Semantic Validation Issues
Reviewing schema definitions and JSON Schema Draft 2020-12 alignment across the codebase (`architecture/ASTRA-GOLD-QUALIFICATION-LAUNCH-SCHEMA.yaml`, `architecture/ASTRA-GOLD-GOVERNANCE-CONTRACT.yaml`, and associated contracts) reveals the following unresolved semantic issues:

1. **`$schema` Identifier Alignment:**
   - Some component specifications mix Draft-07 and Draft 2020-12 keywords (e.g., `definitions` vs `$defs`, `items` behavior in arrays). Ensuring uniform `https://json-schema.org/draft/2020-12/schema` compliance requires explicit use of `$defs` and `$ref` resolution paths.
2. **`additionalProperties` vs `unevaluatedProperties`:**
   - In composite schemas (`allOf`, `anyOf`) representing task envelopes and evidence manifests, using `additionalProperties: false` without `unevaluatedProperties: false` allows unvalidated properties inside sub-schemas.
3. **Format Assertions as Annotations:**
   - Draft 2020-12 treats validation assertions for formats (`date-time`, `uri`, `uuid`, cryptographic hash `sha256`) as annotations by default unless validator engines are explicitly configured with `unevaluatedProperties` or format assertions enabled. Schemas must explicitly require pattern matching (e.g., `^[a-f0-9]{40}$` or `^[a-f0-9]{64}$`) for SHA-1/SHA-256 evidence hashes.
4. **Relative Reference Ambiguity:**
   - Cross-references between task-envelope, agent-registry, and evidence-manifest schemas can be ambiguous when evaluated outside a root base URI context.

---

## 3. Findings: CAF-Q-001 through CAF-Q-015 & Queue Distinction
- **Documentary vs Operational:** CAF-Q-001 through CAF-Q-015 are documentary evidence, contract reconciliation, and qualification gates (e.g., transport gates, tool evaluations, and agent qualification records). They **do not** constitute an active operational queue or live scheduler.
- **Runtime Execution Boundary:** Actual queue processing and autonomous claims are governed strictly by deterministic Python runtime modules (e.g., `runtime/mediahub_runtime/autonomous_queue.py` and `ops/agent-fabric/`), which enforce hard bounding invariants (e.g., max 3 concurrent claims, target SHA pinning, workspace isolation, and fail-closed validation).

---

## 4. Smallest Correction & Negative-Fixture Set
To achieve trustworthy validation for Cloud Agent schemas:
1. **Schema Corrections:**
   - Migrate all schema definitions explicitly to Draft 2020-12 with root `$id` definitions and `$defs`.
   - Replace or supplement standard `format` assertions with explicit regex patterns (`pattern`) for strict hash validation (`sha256`, `sha1`).
   - Enforce `unevaluatedProperties: false` on evidence manifests and task envelopes.
2. **Negative-Fixture Test Set:**
   - **Fixture 1 (`neg-task-envelope-missing-id.json`):** Task envelope omitting mandatory `command_id` or `base_sha`. Expected validation result: **Reject**.
   - **Fixture 2 (`neg-agent-registry-unauthorized-auth.json`):** Agent registry entry claiming unauthorized MediaHub State Authority. Expected validation result: **Reject**.
   - **Fixture 3 (`neg-evidence-manifest-secret.json`):** Evidence manifest containing unredacted credentials or secret environment values (`GEMINI_API_KEY`). Expected validation result: **Reject**.

---

## 5. Architectural Invariants & Governance Compliance
- **Product State Authority:** Product State Authority alone owns canonical MediaHub product-state mutation. Cloud schemas, evidence manifests, and CAF-Q records have zero mutation authority.
- **Fail-Closed:** Any schema validation failure, missing evidence, or cryptographic hash mismatch results in an immediate `BLOCKED` status.

---

## 6. Inspected Sources & Reference SHAs
- `GEMINI.md`: SHA `4c431143aa5c46776e80893bf3c0e5f202e3b76d` (ref: `main`)
- `architecture/ASTRA-GOLD-COMPLETE-COMPONENT-SCHEME.md`: SHA `54ba34ce53d1d7ecd97eef459be7d055b4fd19b1` (ref: `main`)
- `architecture/ASTRA-GOLD-QUALIFICATION-LAUNCH-SCHEMA.yaml`: SHA `aef6229477ed8ec45e45170f98ea87f7ba75ca29` (ref: `main`)
- `architecture/ASTRA-GOLD-GOVERNANCE-CONTRACT.yaml`: SHA `1d3ac25e7817f365807ad85d0d7c9007bd48bebf` (ref: `main`)
- `architecture/ASTRA-GOLD-UNIFIED-AUTONOMOUS-DEVELOPMENT-SYSTEM.yaml`: SHA `adc852009c3a79d0e64265a3af8a4910a1388057` (ref: `main`)
- `recovery/caf-q-003-gemini-mcp-recovery.md`: SHA `be908ceaa978c654d3b78f87afe90d083dea285b` (ref: `main`)
- `recovery/caf-q-003-wave40-mcp-adapter-remediation.md`: SHA `19212339c6be01ee076024ea28211c1dc4bc4df1` (ref: `main`)

---

## 7. Verification Status
- Static review completed successfully.
- Evidence checkpoint published on dedicated branch `task-c-issue-301-schema-review`.
- No runtime modifications, test executions, merges, or deployments performed.
