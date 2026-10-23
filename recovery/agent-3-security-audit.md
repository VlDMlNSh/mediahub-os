# Agent 3 — Independent Security and Provenance Audit

## Metadata
- **Agent:** Gemini Agent 3 (Security & Verification Review)
- **Contour:** Contour A (Developer Fabric)
- **Base Ref:** `main`
- **Immutable Target SHA:** `fbbdc9a06ef344cd57aae13b230a042af76bbc60`
- **Branch:** `agent-3-security-audit`
- **Date:** October 23, 2026

## Executive Summary
This independent security and provenance audit evaluates the MediaHub OS Contour A controller/child transport architecture, cryptographic verification mechanisms, issuer/capability boundaries, secret separation, least privilege enforcement, and fail-closed runtime semantics. The evaluation is anchored against the immutable target SHA `fbbdc9a06ef344cd57aae13b230a042af76bbc60` and verified via structured test suites (e.g., `tests/test_gemini_child_signed_dispatch_runtime_contract.py`).

## 1. Controller/Child Transport & HMAC Security
- **Mechanism:** The controller workflow (`.github/workflows/gemini-batch-dispatch-controller.yml`) signs dispatch payloads using HMAC-SHA256 (`HMAC_KEY` / `MEDIAHUB_DISPATCH_HMAC_KEY`).
- **Canonicalization:** Payloads are serialized using `json.dumps(payload, sort_keys=True, separators=(",",":")).encode()`, ensuring identical payload representation between issuer and verifier.
- **Verification:** Child workflows verify signatures using Python-based authorizer steps with `hmac.compare_digest` to prevent timing attacks.
- **Signed Fields:** `workflow_file`, `dispatch_id`, `target_sha`, `task`, `base_ref`, `scope`.

## 2. Issuer/Capability & Least Privilege
- **Permissions:** Child workflows (such as `.github/workflows/gemini-fcc-independent-review-wave409.yml` and engineering agents) enforce strict least-privilege permissions (e.g., `contents: read` at the job and workflow level).
- **Tool Restrictions:** Restricted tool sets (e.g., `["read_file", "grep_search", "glob", "list_directory"]`) prevent unauthorized mutations.
- **Strict Input Validation:**
  - `dispatch_id` is validated against RFC 4122 UUIDv4 regex (`^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$`).
  - `target_sha` and ref formats are strictly checked.
  - Non-allowlisted base refs (`main` only) and scopes (`contour-a` only) are explicitly rejected.

## 3. Secret Separation & Safety
- **Isolation:** Secrets (`HMAC_KEY`, `MEDIAHUB_DISPATCH_HMAC_KEY`, API keys) are injected exclusively into controlled environment variables.
- **Non-Disclosure:** In compliance with core mandates, no secret values are read, logged, printed, or emitted in logs, tests, or evidence artifacts. Test suites utilize synthetic test keys (e.g., `unit-test-only-not-a-secret`).

## 4. Quota, Fallback & Fail-Closed Behavior
- **Missing Keys:** Absence of the HMAC secret causes immediate, fail-closed termination (`Dispatch HMAC secret missing`).
- **Tampering & Mismatches:** Task tampering, workflow file spoofing, signature mismatch, or event type mismatches (`workflow_dispatch` required) all trigger fail-closed exits with non-zero return codes.
- **Step Outcome Handling:** Review and execution steps utilize `if: always()` validation coupled with explicit `steps.<id>.outcome` checks to prevent unverified bypasses when upstream steps fail or cancel.

## 5. Evidence Provenance & Test Coverage
- **Primary Source Ref:** `main` at SHA `fbbdc9a06ef344cd57aae13b230a042af76bbc60`.
- **Key Test Suite:** `tests/test_gemini_child_signed_dispatch_runtime_contract.py` (Blob SHA / test coverage confirming 100% negative test pass rates for tampered tasks, mismatched signatures, malformed UUIDs, invalid scopes, and non-dispatch events).

## 6. Residual Risks & Known Gaps
- **GitHub Actions Token Permissions:** As documented in prior recovery artifacts (CAF-Q-003), GitHub Actions built-in GITHUB_TOKEN policies restrict automated PR creation (`403 GitHub Actions is not permitted to create or approve pull requests`), necessitating explicit PAT configuration or manual PR opening for automated pipeline integration.
