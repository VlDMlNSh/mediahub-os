# MediaHub OS — Contour A: Agent 3 Security and Provenance Audit

- **Audit Date:** 2026-11-15
- **Agent Identity:** `gemini-agent-3`
- **Authorized Contour:** Contour A (Developer Fabric)
- **Immutable Target SHA:** `41c13e1c2b17ac48dc51c9963a9cda140f79ddb0`
- **Baseline Reference:** Functional Baseline 2.0 / ASTRA-GOLD Governance Contract (v1.0)
- **Status:** DRAFT INDEPENDENT AUDIT (NO MERGE / NO DEPLOYMENT / NO QUALIFICATION)

---

## 1. Executive Summary

This independent security and provenance audit was conducted by Gemini Agent 3 under Contour A of MediaHub OS. The evaluation targets the immutable commit SHA `41c13e1c2b17ac48dc51c9963a9cda140f79ddb0` across key architectural domains: controller/child transport protocols, issuer/capability boundaries, secret separation, least privilege enforcement, HMAC command authentication, quota/fallback policies, and evidence provenance.

All evaluations adhere strictly to the governance mandates established in `GEMINI.md`, `architecture/SECURITY-TRUST-AUTHORIZATION-CONTRACT.md`, and `architecture/ASTRA-GOLD-GOVERNANCE-CONTRACT.yaml`. No secrets were accessed, emitted, or exposed during this review.

---

## 2. Detailed Audit Findings

### 2.1 Controller / Child Transport
- **Architecture:** Communication between controllers and child workloads relies on explicit message serialization, cryptographic signing, and strict command envelope validation.
- **Verification (`tests/test_astra_command_auth.py`):** Verified that command payloads require all mandatory authority fields (`schema_version`, `command_id`, `node_id`, `operation`, `target_sha`, `workflow_only`, `owned_paths`, `title`, `description`, `exclusive_actions`, `issued_at`).
- **Path Safety:** Strict validation rules (`_safe_id`) reject directory traversal attempts (`../escape`, `cmd/escape`, empty IDs) and ensure command IDs conform to safe alphanumeric/hyphen patterns.
- **Target SHA Validation:** Git SHAs are strictly validated (`_valid_target_sha`) for 40- or 64-character hexadecimal shapes, preventing command injection via malicious ref strings.

### 2.2 Issuer / Capability & Least Privilege
- **Product State Authority Boundary:** Product State Authority alone owns canonical MediaHub product-state mutation. AI agents, cloud workflows, queues, and adapters lack mutation authority (`INV_NO_PROVIDER_STATE_AUTHORITY`, `INV_NO_TRANSPORT_STATE_AUTHORITY`).
- **Authorization Invariants:** Default deny, least privilege, and explicit capability scoping are enforced prior to any operation (`architecture/SECURITY-TRUST-AUTHORIZATION-CONTRACT.md`).
- **Isolation:** Executor authority is strictly bounded (`EXECUTOR_ONLY`). Cloud executors and auxiliary tooling cannot create credentials or self-promote (`INV_NO_CANDIDATE_SELF_PROMOTION`, `INV_NO_CREDENTIAL_CREATION_BY_AUXILIARY`).

### 2.3 HMAC Command Authentication & Freshness
- **Mechanism:** Commands are authenticated using HMAC-SHA256 over canonicalized JSON bodies (`sort_keys=True`, separators).
- **Replay Protection:** Commands exceeding max age thresholds (`COMMAND_HMAC_MAX_AGE_SECONDS`, e.g., 900 seconds default) or attempting execution of unauthorized operations (e.g., `reconcile_controller_processes` when unauthorized) are rejected.
- **Idempotency:** Executed command markers prevent duplicate execution (`_command_already_executed`, `_mark_command_executed`).

### 2.4 Secret Separation & Data Egress
- **Secret Hygiene (`tests/test_astra_security.py`):** Verified that secret-like values (API keys, Bearer tokens) are actively detected and redacted (`scan_secret`, `redact`, `require_safe`).
- **Storage Policy:** SOPS + age remain the mandatory secret-protection primitives. Plaintext secrets are strictly prohibited from Git (`INV_NO_CREDENTIALS_IN_GIT`) and evidence bundles (`INV_NO_SECRETS_IN_EVIDENCE`).
- **Observability:** Telemetry and audit records suppress secret values and tokens while preserving trace context.

### 2.5 Quota, Fallback, and Fail-Closed Behavior
- **Fail-Closed Principle:** Ambiguous policy results, missing evidence, or credential/transport failures result in strict fail-closed rejection (`INV_MISSING_EVIDENCE_BLOCKS`, authorization failure never falls back to broader roles).
- **Resource Bounds:** Heartbeat TTL (120s), lease TTL (600s), executor timeout (900s), and evidence freshness windows (86400s) enforce strict operational bounds.

### 2.6 Evidence Provenance
- **Metadata Completeness:** Evidence bundles must include `command_id`, `node_id`, `component_id`, `executor_id`, `provider_or_model_id`, `source_sha`, `round`, `timestamp`, `exit_status`, `timeout`, `workspace`, `verification_status`, and `evidence_digest`.
- **Historical Evidence Ban:** Qualification from historical unverified evidence is strictly prohibited (`INV_NO_QUALIFICATION_FROM_HISTORICAL_EVIDENCE`).

---

## 3. Negative Tests and Verification Status

| Test Suite / Scope | Target File / Rule | Status |
|---|---|---|
| Secret Redaction & Persistence Gate | `tests/test_astra_security.py` | Verified (Pass) |
| HMAC Signature & Expiry Validation | `tests/test_astra_command_auth.py` | Verified (Pass) |
| Path & SHA Sanity Checks | `tests/test_astra_command_auth.py` | Verified (Pass) |
| Governance Invariants & Gates | `architecture/ASTRA-GOLD-GOVERNANCE-CONTRACT.yaml` | Verified (Pass) |

---

## 4. Residual Risks & Recommendations

1. **External Gateway Adoption:** Candidate cloud gateways (e.g., OpenRouter, Unorouter) must complete all 23 qualification rounds and independent A3 review before promotion to mandatory paths.
2. **Key Rotation Lifecycle:** Enforce automated rotation of HMAC shared secrets within the 90-day maximum credential age window.
3. **Strict Isolation:** Ensure zero shared state between Contour A (Developer Fabric) and Contour B product runtimes.
