# Agent 3 Security and Provenance Audit Report

- **Audit Date:** November 15, 2026
- **Agent Identity:** `gemini-agent-3` (Security & Verification Review)
- **Authorized Contour:** Contour A (Developer Fabric)
- **Immutable Target SHA:** `1694cde38c7b7d69baf9676b4908c1bb6e197fbe`
- **Audit Status:** COMPLETED (Draft Audit, No Merge / No Deployment / No Qualification)

---

## 1. Executive Summary

This independent security and provenance audit evaluates the MediaHub OS control/child transport mechanics, issuer and capability boundaries, secret separation, least privilege enforcement, HMAC authentication, quota/fallback policies, and fail-closed behaviors against canonical reference Baseline 2.0 and the Astra Gold Governance Contract (`architecture/ASTRA-GOLD-GOVERNANCE-CONTRACT.yaml`).

The codebase exhibits rigorous defense-in-depth design across transport validation, secret hygiene, command signature verification, and immutable governance gates. All checks conform to the requirement that AI agents, transport channels, and cloud adapters hold zero Product State Authority.

---

## 2. Detailed Audit Findings

### A. Controller / Child Transport & HMAC Authentication
- **Mechanism:** Command verification uses cryptographic HMAC-SHA256 (`_command_auth_valid`) over canonicalized JSON payloads (`sort_keys=True`, separators `(",", ":")`).
- **Freshness & Time Window:** Enforces `COMMAND_HMAC_MAX_AGE_SECONDS` (default 900s) to prevent replay attacks. Stale timestamps are rejected (`test_stale_command_is_rejected`).
- **Idempotency & Replay Protection:** Executed commands are tracked via `_mark_command_executed` and `_command_already_executed`, preventing duplicate execution of command IDs.
- **Target SHA Strictness:** Enforces strict regex validation (`_valid_target_sha`) ensuring target SHAs conform to cryptographic commit hash shapes (40-64 hex chars), rejecting relative path escapes (`../main`).
- **Path Traversal Defense:** Command IDs are validated via `_safe_id` to block directory traversal attempts (`../escape`, `cmd/escape`, empty IDs).

### B. Issuer, Capability, & Least Privilege Boundaries
- **Product State Authority:** AI agents, cloud workflows, queues, and transport adapters do not possess State Authority. State mutation requires canonical validation paths as defined in `architecture/SECURITY-TRUST-AUTHORIZATION-CONTRACT.md`.
- **Command Envelope:** Required envelope fields (`schema_version`, `command_id`, `node_id`, `operation`, `target_sha`, `workflow_only`, `owned_paths`, `title`, `description`, `exclusive_actions`, `issued_at`) are strictly enforced.
- **Execution Scope:** Contour A is strictly bounded to developer fabric. Contour B product implementation remains gated.

### C. Secret Separation & Hygiene
- **Storage & Primitives:** SOPS + age encryption primitives are mandated for secret management. Production plaintext secrets are strictly excluded from Git and evidence.
- **Redaction & Scanning:** `runtime/mediahub_runtime/astra_security.py` provides automated scanning (`scan_secret`), redaction (`redact`), and persistence gating (`require_safe`), ensuring API keys and bearer tokens are automatically caught and replaced with `[REDACTED_SECRET]` before output or logging.
- **Verification:** Enforced by `tests/test_repo_secret_hygiene.py` and `tests/test_astra_security.py`.

### D. Quota, Fallback, & Fail-Closed Behavior
- **Policy Ambiguity:** Ambiguous policy evaluation results fail closed.
- **Authentication Failures:** Unknown principals, invalid or revoked credentials, and unknown devices result in immediate denial or quarantine.
- **Missing Evidence:** Under Astra Gold governance, missing required evidence defaults to `BLOCKED`.
- **Cloud Executors:** Cloud adapters operate under `EXECUTOR_ONLY` authority with mandatory admission gates, independent A3 verification, and per-provider credential isolation. No cloud executor holds native architecture authority.

---

## 3. Negative Test Coverage & Evidence

The audit verified the existence and execution of regression and negative test suites:
1. **`tests/test_astra_command_auth.py` (SHA: `8df49fc55e660c13ad54aca9b9dc78132c335dd1`):**
   - Validates signature verification and rejects tampered operations.
   - Rejects stale commands exceeding max age.
   - Enforces strict `target_sha` shape validation (rejects `../main`, short strings).
   - Enforces command ID path safety (`_safe_id`).
   - Verifies command idempotency via `EXECUTED_COMMANDS`.
2. **`tests/test_astra_security.py` (SHA: `6761edb5e1e9e035388aabcd1b95d240098c2ec4`):**
   - Detects and redacts secret-like token patterns.
   - Preserves standard non-secret text.
   - Rejects unverified content persistence in gates.
3. **`architecture/ASTRA-GOLD-GOVERNANCE-CONTRACT.yaml` (SHA: `1d3ac25e7817f365807ad85d0d7c9007bd48bebf`):**
   - Invariant registry and gate registry binding all invariants to automated test fixtures.

---

## 4. Residual Risks & Governance Notice

- **Draft Audit Status:** This report constitutes an independent security audit pass for Contour A. No merge, promotion, qualification execution, or deployment is authorized by this artifact.
- **Credential Integrity:** No secret values or live tokens were accessed, stored, or emitted during this audit.
