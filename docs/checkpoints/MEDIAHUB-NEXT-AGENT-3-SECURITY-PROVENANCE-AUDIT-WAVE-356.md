# MediaHub OS — Agent 3 Independent Security and Provenance Audit (Wave 356)

- **Date:** 2026-10-22
- **Agent Identity:** `gemini-agent-3`
- **Credential Reference:** `GEMINI_API_KEY_3`
- **Authorized Contour:** Contour A (Developer Fabric)
- **Immutable Target SHA:** `b33ab31674bfa9595a8f2ba5a570dbc1eb3686b2`
- **Base Ref:** `main`
- **Branch:** `audit/agent-3-security-provenance-wave356`
- **Task Scope:** Independent security and provenance audit of controller/child transport, issuer/capability, secret separation, least privilege, HMAC, quota/fallback policy, evidence provenance, and fail-closed behavior.

---

## 1. Executive Summary & Audit Scope

This document records the independent security and provenance audit performed by Agent 3 for MediaHub OS Contour A against the immutable target SHA `b33ab31674bfa9595a8f2ba5a570dbc1eb3686b2`. 

All analyses are based on static code inspection of core controller and child workflows, execution security harnesses, and cryptographic verification contracts. **No secret values were read, logged, or exposed.**

---

## 2. Component & Transport Audit

### 2.1 Controller / Child Transport
- **Controller Workflow:** `.github/workflows/gemini-batch-dispatch-controller.yml`
- **Child Workflows:**
  - `.github/workflows/gemini-autonomous-engineering.yml` (Agent 1)
  - `.github/workflows/gemini-agent-2.yml` (Agent 2)
  - `.github/workflows/gemini-agent-3.yml` (Agent 3)
- **Transport Mechanism:** Explicit GitHub REST API calls (`/actions/workflows/{wf}/dispatches`) from the controller to dispatch the three child workflows with a shared immutable target SHA (`TARGET_SHA`), unique UUIDv4 dispatch IDs, signed task strings, and HMAC signatures.
- **Trigger Isolation:** Protected by strict conditional guards requiring `workflow_dispatch` on `refs/heads/main`, explicit user confirmation (`confirm: true`), mode selection (`mode: agents`), and readiness gate compliance (`MEDIAHUB_GEMINI_BATCH_ENABLED=true`).

### 2.2 Issuer / Capability & Secret Separation
- **Secret Isolation:** `secrets: inherit` is strictly absent across all controller and child workflow files.
- **Provider API Keys:** Each child workflow receives a dedicated, role-scoped secret (`GEMINI_API_KEY`, `GEMINI_API_KEY_2`, `GEMINI_API_KEY_3`) and has zero access to `MEDIAHUB_GITHUB_TOKEN`.
- **Controller Token Scope:** The controller utilizes `MEDIAHUB_GITHUB_TOKEN` exclusively for repository workflow dispatch and `MEDIAHUB_DISPATCH_HMAC_KEY` for payload signing.

### 2.3 Least Privilege & Fail-Closed Behavior
- **Workflow Permissions:** Explicitly declared minimal permissions (`permissions: {}`) at workflow and job levels to prevent unintended token permission escalation.
- **HMAC Verification:** Signed fields (`workflow_file`, `dispatch_id`, `target_sha`, `task`, `base_ref`, `scope`) are serialized using strict key sorting (`json.dumps(..., sort_keys=True, separators=(",", ":"))`) and verified via constant-time comparison (`hmac.compare_digest`).
- **Fail-Closed Semantics:** 
  - Tampered tasks, mismatched child workflow identities, malformed UUIDv4 shapes, or invalid SHA lengths trigger immediate failure before execution.
  - Inputs outside allowlisted base refs (`main`) or scopes (`contour-a`) are rejected.
  - Missing HMAC secrets or invalid signatures result in fail-closed termination.

---

## 3. Negative Tests & Contract Verification

The verification test suites (`tests/test_gemini_child_signed_dispatch_runtime_contract.py` and `tests/test_gemini_transport_controller_contract.py`) empirically validate the security contract against negative scenarios:
1. **Valid Canonical Signature:** Successfully verifies across all three child authorizers.
2. **Task Tampering:** Rejected (`Invalid controller signature`).
3. **Cross-Workflow Replay:** A signature generated for child 1 is rejected when presented to child 2/3 (`Invalid controller signature`).
4. **Malformed UUID / SHA:** Rejected (`Malformed target SHA or dispatch ID`).
5. **Base Ref / Scope Violation:** Rejected (`Input outside allowlist`).
6. **Incorrect Event / Repository / Ref:** Rejected (`Child must run from trusted main workflow_dispatch`).
7. **Missing Key / Invalid Signature:** Fails closed.
8. **Output Validation:** Child steps strictly require actionable PR results and successful tool execution logs before success acceptance.

---

## 4. Quota, Fallback & Provenance Policy

- **Quota / Fallback:** Local execution and cloud dispatch maintain strict separation. No paid fallback or unvouched model inference is permitted.
- **Evidence Provenance:** All dispatched tasks require verifiable execution artifacts, signed dispatch tracking, and output validation. Product State Authority retains sole canonical mutation authority.

---

## 5. Residual Risks & Known Gaps

- **Formal Independent Review:** Remains pending formal human/independent sign-off.
- **Live Positive Dispatch:** Production-governed multi-agent batch dispatch under live repository settings remains gated pending full authorization.
- **Scope limitation:** Draft audit only; no merge, deployment, qualification, or nested dispatch performed.

---

## 6. Verification Status

- **Static Contract Verification:** PASS (tested via unit test suites).
- **Transport & HMAC Security:** VERIFIED.
- **Draft Audit Status:** COMPLETE.
- **Action:** Open Pull Request to `main`. **Never merge or deploy.**
