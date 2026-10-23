# MediaHub OS — Agent 3 Security and Provenance Audit

**Date:** 2026-10-23  
**Agent Identity:** `gemini-agent-3` (Contour A — Security and Verification Review)  
**Immutable Target SHA:** `fbbdc9a06ef344cd57aae13b230a042af76bbc60`  
**Status:** DRAFT AUDIT REPORT (No merge, deployment, or qualification performed)

---

## 1. Executive Summary

This audit evaluates the security, trust, authorization, secret separation, transport integrity, HMAC validation, fail-closed behavior, and evidence provenance of the MediaHub OS autonomous dispatch and execution framework (Contour A). 

Based on static inspection and test suite verification against immutable target SHA `fbbdc9a06ef344cd57aae13b230a042af76bbc60`, the security architecture robustly enforces least privilege, fail-closed semantics, cryptographic authentication of dispatches, and strict secret isolation.

---

## 2. Controller & Child Transport Architecture

- **Controller Workflow:** `.github/workflows/gemini-batch-dispatch-controller.yml` (SHA: `5ae0e8db9465ce36bd4020df69b552c659cd6187`)
- **Child Workflows:**
  - `gemini-autonomous-engineering.yml`
  - `gemini-agent-2.yml`
  - `gemini-agent-3.yml`
  - `gemini-fcc-independent-review-wave409.yml`
- **Transport Mechanism:** Dispatches are executed via authenticated GitHub REST API calls (`/actions/workflows/{wf}/dispatches`) utilizing dedicated orchestration token `MEDIAHUB_GITHUB_TOKEN`.
- **Isolation:** `secrets: inherit` is explicitly disabled across all workflows. Child workflows never receive `MEDIAHUB_GITHUB_TOKEN`.

---

## 3. Issuer / Capability & HMAC Integrity

- **HMAC Secret:** `MEDIAHUB_DISPATCH_HMAC_KEY` is shared between controller and child authorizers.
- **Signed Payload Structure:**
  ```json
  {
    "workflow_file": "...",
    "dispatch_id": "...",
    "target_sha": "...",
    "task": "...",
    "base_ref": "...",
    "scope": "..."
  }
  ```
- **Hashing & Comparison:** Computed via `hmac.new(..., hashlib.sha256)` over sorted, compact JSON (`json.dumps(payload, sort_keys=True, separators=(',', ':'))`). Validation uses `hmac.compare_digest` to prevent timing attacks.
- **Validation Ref:** `tests/test_gemini_child_signed_dispatch_runtime_contract.py` (SHA: `e92e1c3f4e52fb2005845e520d1bbe10dcdacfbe`).

---

## 4. Secret Separation & Least Privilege

- **Provider Credentials:** Each child workflow maps a dedicated API key secret (`GEMINI_API_KEY`, `GEMINI_API_KEY_2`, `GEMINI_API_KEY_3`).
- **Permissions:** 
  - Review workflows operate with strict read-only permissions (`contents: read`) and lack PR creation capabilities (`create_pull_request`).
  - Secret scanning and redaction primitives (`runtime/mediahub_runtime/astra_security.py`) ensure secret-like strings are detected and redacted before logging or persistence.

---

## 5. Fail-Closed & Negative Test Coverage

The test suite thoroughly validates fail-closed behavior under malicious or erroneous conditions:
1. **Task Tampering:** Modifying task payload after signing is rejected with `"Invalid controller signature"`.
2. **Cross-Child Replay:** Using a signature generated for one child workflow on another is rejected.
3. **Malformed UUIDv4 & Target SHA:** Non-v4 UUIDs or non-40-char SHAs fail validation with `"Malformed target SHA or dispatch ID"`.
4. **Unallowlisted Scope/Base:** Scopes outside `contour-a` or base refs outside `main` are rejected with `"Input outside allowlist"`.
5. **Unauthorized Triggers:** Dispatches triggered by `pull_request` events, unauthorized repositories, or non-main branch refs are blocked.
6. **Missing HMAC Key:** Missing secrets cause immediate fail-closed behavior (`"Dispatch HMAC secret missing"`).

---

## 6. Evidence Provenance & Reconciliation

- **Auditability:** Every dispatch records execution logs, job IDs, artifact digests, and reconciliation states.
- **Failure Resilience:** The controller captures dispatch and runtime exceptions without crashing the batch loop, marking unknown or failed dispatches explicitly in summary artifacts.

---

## 7. Residual Risks & Recommendations

- **Key Rotation:** Ensure periodic rotation of `MEDIAHUB_DISPATCH_HMAC_KEY` and provider API keys.
- **Workflow Permissions Audit:** Maintain minimal write permissions on engineering agents, ensuring pull request creation is strictly bounded to authorized branches.

---
*Audit completed by Gemini Agent 3 under Contour A.*
