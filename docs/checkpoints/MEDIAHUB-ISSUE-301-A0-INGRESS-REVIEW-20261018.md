# MediaHub OS — Task B / Issue 301 Review: A0 Ingress/Issuer Boundary & R-06 Separation

- **Date:** October 18, 2026
- **Task ID:** Issue 301 / Task B
- **Reviewer Identity:** `gemini-agent-3` (Contour A - Security & Verification Review)
- **Base Ref / Commit SHA:** `main` (`c06015e0b1526e0aaa6a522306052b077455aba5`)
- **Status:** COMPLETED_INDEPENDENT_REVIEW (Non-mutating architectural review; no runtime deployment or product-state modification performed)

---

## 1. Executive Summary

This independent review evaluates the proposed **A0 ingress/issuer boundary** and **R-06 separation** within MediaHub OS Contour A. In accordance with the ASTRA GOLD Reference Architecture v1.1, Governance Contract v1.0, and Security/Trust/Authorization Contract, this review verifies that:
1. **Product State Authority** alone owns canonical MediaHub product-state mutation. AI agents, transport mechanisms, cloud workflows, and executors do not acquire state mutation authority.
2. **Jarvis engineering-mission admission routes** remain distinct from **ASTRA A0 executor authority** and canonical state mutation pathways.
3. **Fail-closed behavior** is strictly enforced for unauthenticated requests, invalid signatures, stale timestamps, target SHA mismatches, and unauthorized issuers.
4. **Secret-flow isolation** and evidence sanitization (`SUPPRESSED` credential metadata, redaction of secrets) prevent unauthorized leakage or trust escalation.

---

## 2. Architectural Boundary & Separation Analysis

| Boundary / Route | Authority Level | Permitted Actions | Prohibited Actions |
|---|---|---|---|
| **MediaHub Product State Authority** | Sovereign Domain State Authority | Canonical state mutation, domain ledger commits | Direct execution by AI agents, unvalidated transport payloads |
| **Jarvis Engineering-Mission Admission** | Bounded Engineering Admission | Task scoping, agent dispatch orchestration | Direct state mutation, bypassing A3 verification |
| **ASTRA A0 Coordinator / Executor** | Control & Execution Orchestration | Queue coordination, claim leasing, test capture, evidence publishing | Self-promotion, architecture ownership override, product-state mutation |
| **Transport & Gateways (GitHub / FCC / OmniRoute / Routers)** | Transport / Routing Substrate | Message relay, network transport, format adaptation | Acquiring State Authority, issuing trust tokens, self-qualification |

### R-06 Separation Assessment
R-06 and associated architectural contracts enforce strict boundaries between **ingress ingestion** (how commands enter the agent fabric via signed GitHub/transport artifacts) and **issuer validation** (how commands are authenticated via HMAC, age validation, schema compliance, and target SHA binding).
- **Finding:** The ingress payload (`control/commands/{NODE_ID}.json`) is treated strictly as an untrusted transport artifact. It requires a valid HMAC signature evaluated against node-specific secrets (`COMMAND_HMAC_KEY`), strict schema compliance (`mediahub.astra.control-command.v1`), and an exact Git SHA match against the current repository HEAD (`_current_head()`).
- **Severity:** Informational (Controls are correctly structured and fail-closed).

---

## 3. Threat & Failure Analysis

### 3.1 Fail-Closed Behavior
- **Mechanism:** As implemented in `astra_github_agent.py` and tested in `tests/test_astra_command_auth.py`, any missing signature, failed HMAC comparison, expired timestamp, or malformed command envelope immediately results in rejection (`_command_auth_valid` returns `False`).
- **Evaluation:** Complies with the Security Contract requirement that ambiguous policy results or invalid credentials fail closed.

### 3.2 Stale / Invalid Issuer Handling
- **Mechanism:** `COMMAND_HMAC_MAX_AGE_SECONDS` (default bounded to 900 seconds) rejects commands with timestamps older than the allowed window. Node ID binding (`NODE_ID` validation via `_safe_id`) prevents cross-node command injection.
- **Evaluation:** Effectively mitigates replay attacks and stale issuer impersonation.

### 3.3 Secret-Flow Isolation
- **Mechanism:** Evidence publication explicitly suppresses sensitive credential values (`secret_values: "SUPPRESSED"`). Security scanners (`tests/test_astra_security.py`) enforce regex and content validation to ensure tokens, API keys, and bearer strings never leak into git history or evidence bundles.
- **Evaluation:** Strict adherence to SOPS+age and zero-credential-in-evidence mandates.

### 3.4 Cancellation & Recovery
- **Mechanism:** Claim leases (`AgentClaim`, `ClaimStore`) enforce time-bounded ownership (default max 600s lease TTL, heartbeat TTL 120s). Stale claims are recoverable, and duplicate controllers are rejected.
- **Evaluation:** Prevents zombie worker locks and ensures deterministic recovery to a known state or `BLOCKED`.

---

## 4. Negative-Test Matrix

| Test Case ID | Scenario / Attack Vector | Expected Behavior | Verification Status / Source |
|---|---|---|---|
| **NC-01** | Missing or malformed command HMAC signature | Reject command (`_command_auth_valid` -> `False`) | Verified in `tests/test_astra_command_auth.py` |
| **NC-02** | Stale command issued beyond `COMMAND_HMAC_MAX_AGE_SECONDS` | Reject command (stale timestamp) | Verified in `tests/test_astra_command_auth.py` |
| **NC-03** | Path traversal in command ID or owned paths (`../escape`) | Reject command (`_safe_id` -> `False`) | Verified in `tests/test_astra_command_auth.py` |
| **NC-04** | Target SHA mismatch with current repository HEAD | Reject execution (`BLOCKED` / head mismatch) | Verified in `astra_github_agent.py` |
| **NC-05** | Attempt to inject secret-like strings into evidence/persistence | Raise `ValueError` / block persistence | Verified in `tests/test_astra_security.py` |
| **NC-06** | Transport / Cloud router attempting to claim State Authority | Denied (Transport has no State Authority) | Enforced by ASTRA GOLD Invariants (INV_NO_TRANSPORT_STATE_AUTHORITY) |

---

## 5. Identified Gaps & Recommendations

1. **Runtime Qualification Evidence:** While static contracts, unit tests (`test_astra_command_auth.py`, `test_astra_security.py`), and reference architectures are robust, live 23-wave qualification evidence across all distributed nodes (`mh-dev-01`, `mh-dev-02`, `Voktors-Mac-mini.local`) remains pending execution. No runtime qualification claims are asserted in this review.
2. **Contour A / Contour B Boundary Enforcement:** As Contour B features evolve, strict review gates must ensure product implementations do not bypass Contour A governance or establish unauthorized state mutation paths.

---

## 6. Verification Status

- **Static Analysis & Contract Conformance:** PASS. All governing security, trust, and authorization invariants are backed by unit tests.
- **Runtime Qualification:** PENDING fresh 23-wave evidence collection.
- **Merge/Deployment Authorization:** BLOCKED / PROHIBITED. In accordance with agent mandates, this review is published as a non-mutating PR and will never be merged or deployed autonomously.
