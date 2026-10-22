# MediaHub OS — Agent 3 Independent Security & Provenance Audit

- **Audit Agent:** gemini-agent-3 (Contour A)
- **Immutable Target SHA:** `1c22d82c1750aebe0c5571e088d9c0adc012c42f`
- **Base Ref:** `main`
- **Branch:** `agent3-security-provenance-audit-wave319`
- **Date:** 2026-10-22
- **Status:** DRAFT INDEPENDENT AUDIT (No merge, deployment, qualification, or nested dispatch)

## 1. Executive Summary & Scope
This independent security and provenance audit evaluates the controller/child dispatch transport, HMAC authorization hardening, secret separation boundaries, capability issuers, least-privilege enforcement, fail-closed semantics, and evidence provenance under MediaHub OS Contour A.
All findings are derived from empirical inspection of repository contracts, python security unit tests (`tests/test_astra_security.py`, `tests/test_gemini_child_signed_dispatch_runtime_contract.py`), security-trust-authorization contracts (`architecture/SECURITY-TRUST-AUTHORIZATION-CONTRACT.md`), and transport health evidence (`evidence/transport-health-current.json`).

## 2. Controller & Child Transport Security (HMAC & Validation)
- **Mechanism:** As validated in `tests/test_gemini_child_signed_dispatch_runtime_contract.py` (Blob SHA: `efb573f36861508e440e2e4f5da4d5a76b54005b`), the controller (`.github/workflows/gemini-batch-dispatch-controller.yml`) and child workflows (`gemini-autonomous-engineering.yml`, `gemini-agent-2.yml`, `gemini-agent-3.yml`) enforce strict cryptographic payload binding using HMAC-SHA256 (`HMAC_KEY`).
- **Signed Fields:** `workflow_file`, `dispatch_id`, `target_sha`, `task`, `base_ref`, `scope`.
- **Serialization:** Canonical JSON serialization with sorted keys and compact separators (`json.dumps(payload, sort_keys=True, separators=(",",":")).encode()`).
- **Timing Attack Mitigation:** Constant-time comparison via `hmac.compare_digest`.
- **Fail-Closed Behavior:** Missing keys, empty secrets, invalid HMAC signatures, mismatched workflow filenames, tampered task parameters, or invalid dispatch identifiers trigger immediate failure and exit.

## 3. Issuer & Capability / Least Privilege
- **Access Boundaries:** Contour A (Developer Fabric) remains strictly separated from Contour B product implementation.
- **State Authority:** Product State Authority alone owns canonical product-state mutation. AI agents, cloud workflows, queues, and adapters lack mutation authority.
- **Parameter Validation:** Strict input regex validation enforces UUIDv4 shape for dispatch IDs, 40-character hex strings for target SHAs, allowlisted base refs (`main`), and allowlisted scopes (`contour-a`). Inputs outside allowlists or malformed shapes are rejected before signature evaluation.
- **Event Restrictions:** Child workflows strictly mandate execution from trusted `workflow_dispatch` events originating from the authorized repository (`VlDMlNSh/mediahub-os`) and canonical ref (`refs/heads/main`).

## 4. Secret Separation & Redaction
- **Secret Primitive:** SOPS + age principles. Plaintext secrets are never committed, embedded in source, or emitted into logs/telemetry.
- **Redaction Engine:** Verified via `tests/test_astra_security.py` (Blob SHA: `6761edb5e1e9e035388aabcd1b95d240098c2ec4`), `runtime.mediahub_runtime.astra_security` (`scan_secret`, `redact`, `require_safe`) correctly identifies secret-like patterns (e.g. Bearer tokens, API keys), redacts them to `[REDACTED_SECRET]`, and rejects unverified persistence or source content.
- **Evidence Handling:** Transport health evidence (`evidence/transport-health-current.json`, Blob SHA: `c1d63bb5fa5b4d6be0763eff2893fb157324999a`) explicitly suppresses secret values (`"secret_values": "SUPPRESSED"`). No secret values were read or output during this audit.

## 5. Quota, Fallback, & Fail-Closed Semantics
- **Policy:** Authorization failure never falls back to broader roles. Ambiguous policy results fail closed.
- **Evidence Provenance:** Transport health tracking (`evidence/transport-health-current.json`) indicates mixed status (`BLOCKED` overall status due to legacy schema nodes lacking explicit transport version/SHA fields in node `mh-dev-02`), ensuring downstream verification prevents unvalidated nodes from acquiring silent trust.
- **Output Validation:** Child workflow validators ensure that Gemini execution artifacts are non-empty, valid JSON, and record at least one successful tool call including Pull Request creation (`mcp_github_create_pull_request`).

## 6. Negative Tests & Coverage
The test suite explicitly exercises negative cases:
1. Task tampering after signing -> rejected (`Invalid controller signature`).
2. Signature reuse across different child workflows -> rejected (`Invalid controller signature`).
3. Malformed UUIDv4 shapes or short target SHAs -> rejected (`Malformed target SHA or dispatch ID`).
4. Non-allowlisted base refs or scopes -> rejected (`Input outside allowlist`).
5. Unauthorized event names, external repositories, or non-main ref names -> rejected (`Child must run from trusted main workflow_dispatch`).
6. Missing HMAC key -> rejected (`Dispatch HMAC secret missing`).
7. Malformed or empty Gemini stdout outputs -> rejected by output validator.

## 7. Residual Risks & Recommendations
1. **Legacy Node Compliance:** Node `mh-dev-02` in transport health evidence currently reports `BLOCKED` due to legacy schema usage. Recommendation: enforce transport schema compliance across all mesh nodes prior to qualification.
2. **Secret Rotation Discipline:** Maintain rigorous automated rotation schedules for `HMAC_KEY` and GitHub Actions secrets.
3. **Draft Audit Scope:** This PR contains audit documentation only. No execution, deployment, merging, or qualification has occurred.
