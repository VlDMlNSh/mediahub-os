# MH-GEMINI-POOL-A3-001 — Independent Security and Verification Review

## Metadata
- **Task ID:** MH-GEMINI-POOL-A3-001
- **Agent Identity:** Gemini Agent 3 (Security & Verification Review)
- **Authorized Contour:** Contour A (Developer Fabric)
- **Base Ref:** `main`
- **Review Branch:** `mh-gemini-pool-a3-001-security-review`
- **Date:** October 17, 2026

---

## 1. Executive Summary

This independent security and verification review evaluates the Agent 1 and Agent 2 evidence, governance specifications (`architecture/ASTRA-GOLD-GOVERNANCE-CONTRACT.yaml`, `architecture/ASTRA-GOLD-UNIFIED-AUTONOMOUS-DEVELOPMENT-SYSTEM.yaml`), agent profiles (`profiles/agent-registry.json`), and transport execution worker (`astra_github_agent.py`). 

The analysis confirms that the Astra Gold control plane and transport daemon implement rigorous fail-closed invariants, secret suppression (`SUPPRESSED`), path traversal prevention, HMAC command authentication, bounded network retries, and idempotent execution tracking. However, certain operational friction points and GitHub platform permission boundaries (such as Actions token PR creation restrictions) require explicit documentation.

---

## 2. Review of Agent 1 & Agent 2 Evidence

### 2.1 Transport Health (`evidence/transport-health-current.json`)
- **Status:** `BLOCKED`
- **Observations:** Node `mh-dev-01` and `Voktors-Mini.Dlink` successfully report `self-reexec-v1` transport health with exact SHA bindings. Node `mh-dev-02` reports `BLOCKED` due to legacy schema reporting and missing transport version fields (`ModuleNotFoundError('mediahub_runtime')` during prior runtime activation passes).
- **Security Assessment:** Complies with fail-closed requirements. Unverified or legacy node evidence does not contaminate canonical state.

### 2.2 Execution Backends (`evidence/execution-backends.json`)
- **Status:** `BLOCKED` (`RUNTIME_EVIDENCE_REQUIRED`)
- **Observations:** `codex` and `cursor` executors on `mh-dev-01` are marked `UNVERIFIED` with `NOT EXECUTED` checks and secret suppression enabled.
- **Security Assessment:** Proper adherence to the hybrid admission ladder (`REGISTERED → CREDENTIAL_PRESENT → AUTH_SUCCESS → MODEL_DISCOVERY_PASS → PROBE_PASS → EXECUTION_PASS → A3_VERIFIED`). Unproven execution backends cannot masquerade as qualified production executors.

---

## 3. Detailed Security & Architecture Findings

### 3.1 Secret References & Exposure (`astra_github_agent.py`, `profiles/agent-registry.json`)
- **Finding Status:** **LOW / PASS** (Secure by Design)
- **File Reference:** `astra_github_agent.py` (lines 145, 608, 655, 680)
- **Analysis:** All credential values are explicitly suppressed in published results (`publish_result.setdefault("secret_values", "SUPPRESSED")`). HMAC keys are mapped exclusively from environment variables matching node identities (`COMMAND_HMAC_ENV`). No hardcoded secrets or plaintext API keys exist in the codebase.

### 3.2 Effective GitHub Permissions & Token Constraints
- **Finding Status:** **HIGH** (Platform Limitation)
- **File Reference:** GitHub Actions token runtime policy
- **Analysis:** GitHub Actions workflow tokens operating under default job permissions encounter `403 GitHub Actions is not permitted to create or approve pull requests` when attempting programmatic PR creation without an elevated personal access token (PAT) or explicit `contents: write` / `pull-requests: write` permissions.
- **Mitigation:** The agent fabric and workflow architecture correctly treat PR creation failure as a platform access boundary, maintaining local branch separation and recording findings in versioned evidence checkpoints.

### 3.3 Untrusted Task-Input Handling (`astra_github_agent.py`)
- **Finding Status:** **PASS** (Fail-Closed & Validated)
- **File Reference:** `astra_github_agent.py` (`read_command()`, lines 94–119)
- **Analysis:** 
  - Command JSON is validated against `REQUIRED_COMMAND_FIELDS`.
  - Node identity and command IDs are strictly checked against `SAFE_ID_RE` (`^[A-Za-z0-9._:-]{1,128}$`).
  - Target SHAs are validated against `SHA_RE` (`^[0-9a-fA-F]{40,64}$`).
  - `owned_paths` are verified to be relative paths without path traversal components (`".." not in Path(p).parts`).

### 3.4 HMAC Command Authentication & Replay Protection
- **Finding Status:** **PASS**
- **File Reference:** `astra_github_agent.py` (`_command_auth_valid()`, lines 73–82)
- **Analysis:** Commands require a valid HMAC SHA-256 signature calculated over the canonical JSON body (`_canonical_command_body`). Maximum age of commands is strictly capped (`COMMAND_HMAC_MAX_AGE_SECONDS = 900`), preventing stale command injection or replay attacks.

### 3.5 Idempotency & Retry Bounds (`astra_github_agent.py`)
- **Finding Status:** **PASS**
- **File Reference:** `astra_github_agent.py` (`_command_already_executed()`, `_mark_command_executed()`, lines 84–92; `git_network()`, lines 45–55)
- **Analysis:**
  - Executed command IDs are recorded as sentinel `.done` files in `EXECUTED_COMMANDS`. Duplicate execution of the same `command_id` is rejected immediately.
  - Git network operations implement bounded exponential retry (`attempts=4`, `base_delay=2.0`, max delay 15.0s), failing closed upon exhaustion rather than infinite blocking.

### 3.6 Data-Egress Policy & Fail-Closed Behavior
- **Finding Status:** **PASS**
- **File Reference:** `astra_github_agent.py` (lines 142–156, 595–610)
- **Analysis:** If any invariant fails (signature mismatch, target SHA divergence, missing evidence, or lease expiration), the agent aborts execution, releases claims with status `REJECTED`, and publishes a structured failure record without leaking local environment variables or credentials.

---

## 4. Acceptance Criteria Status & Verification

- **Task ID:** `MH-GEMINI-POOL-A3-001`
- **Independent Review Completed:** Yes, Agent 1 and Agent 2 evidence, agent registry, governance contracts, and `astra_github_agent.py` transport worker reviewed.
- **Security Checkpoints Checked:** Secret exposure, GitHub permissions, untrusted input handling, quota/retry semantics, idempotency, data egress, and fail-closed behavior verified.
- **Branch Created:** `mh-gemini-pool-a3-001-security-review` (from `main`, commit SHA: `4712c30c3e0296cf1d792c4c69e49cdb798d99fe`).
- **Checkpoint File Created:** `evidence/security-review-mh-gemini-pool-a3-001.md`.
- **Merge/Deployment Restrictions Respected:** Yes, no merge or deployment attempted.
