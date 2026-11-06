# MediaHub OS — Agent 3 Independent Security & Provenance Audit

- **Agent ID:** `gemini-agent-3`
- **Contour:** `contour-a` (Developer Fabric)
- **Date:** 2026-10-23
- **Immutable Target SHA:** `f0448f28c7cfa61e4450c38529f09afbfdbbc7c7`
- **Base Ref:** `main`
- **Status:** DRAFT AUDIT COMPLETE (No merge, deployment, or qualification execution)

---

## 1. Audited Artifacts & Blob SHAs

| File Path | Blob SHA (Ref: `main`) | Description |
|---|---|---|
| `GEMINI.md` | `4c431143aa5c46776e80893bf3c0e5f202e3b76d` | Gemini Agent Rules & Authority Scope |
| `architecture/SECURITY-TRUST-AUTHORIZATION-CONTRACT.md` | `8d831c2a8fa333977dd86524099568bae2a8db0e` | Security, Trust & Authorization Governing Specification |
| `runtime/mediahub_runtime/astra_security.py` | `ff4ba9b581cf30e0f2d6bbed70c5290d93bfa27d` | Security Boundary for Durable Memory & Redaction |
| `tests/test_astra_security.py` | `6761edb5e1e9e035388aabcd1b95d240098c2ec4` | Unit Tests for Secret Detection & Redaction Gates |
| `tests/test_astra_command_auth.py` | `8df49fc55e660c13ad54aca9b9dc78132c335dd1` | Unit Tests for Command HMAC Auth & Path Safety |
| `tests/test_astra_context_redaction.py` | `d0ff000e39a0466fa41b9c2e555b5c521d147c7e` | Unit Tests for Context Assembly Redaction |
| `astra_github_agent.py` | `dd2f373bf5f3d69dec951c84e3d53b0e9befab0c` | Astra GitHub Transport Worker & Execution Dispatch |

---

## 2. Controller & Child Transport Security

- **Transport Model:** GitHub-backed polling transport (`astra_github_agent.py`) syncing via bounded Git fetch/reset (`git_network` with exponential retry up to 4 attempts).
- **Branch Protection & Isolation:** Node results are committed to isolated remote branches (`astra-node/{NODE_ID}`) and pushed with fail-closed concurrency rejection (`git push origin HEAD:astra-node/{NODE_ID}`). Unstaged/dirty worktrees are restored via `git restore` or `git clean` restricted strictly to the command path (`control/commands/{NODE_ID}.json`), ensuring zero collateral impact on user changes.
- **Self-Reexecution Integrity:** The transport worker computes `RUNNING_AGENT_SHA` on startup from its own file content and re-executes (`os.execv`) if updated in the worktree, ensuring runtime consistency with the fetched repository revision.

---

## 3. Issuer, Capability & Claim Enforcement

- **Claim Store Integration:** Every command dispatch enforces an exclusive agent claim (`AgentClaim` & `ClaimStore` in `mediahub_runtime.agent_fabric`) bound to `task_id`, `paths`, `exclusive_actions`, and lease duration (`CLAIM_LEASE_SECONDS`).
- **State Authority Boundary:** Product State Authority alone owns canonical product-state mutation. Agent claims and worker transport records are tracked as auditable facts/evidence and do not confer State Authority.

---

## 4. Secret Separation, Redaction & Zero-Leakage

- **Pre-Persistence Gates:** `require_safe` in `astra_security.py` scans inputs against robust regex patterns covering API keys (`sk-[A-Za-z0-9_-]{16,}``), GitHub tokens (`ghp_`, `github_pat_`), Bearer authorization headers, and assignment patterns (`api_key=`, `access_token=`, `secret`, `password`). Any match raises `ValueError` before persistence.
- **Defense-in-Depth Redaction:** `redact()` substitutes all detected secret-like fragments with `[REDACTED_SECRET]`. In `astra_github_agent.py`, all result publication payloads explicitly enforce `"secret_values": "SUPPRESSED"`.
- **Secret Handling Rule:** Never read or output secret values. All tests (`test_astra_security.py`, `test_astra_context_redaction.py`) verify that secret-like strings are successfully intercepted, rejected, and redacted.

---

## 5. Least Privilege & Command Envelope Invariants

- **Mandatory Fields:** Commands require all fields in `REQUIRED_COMMAND_FIELDS` (`schema_version`, `command_id`, `node_id`, `operation`, `target_sha`, `workflow_only`, `owned_paths`, `title`, `description`, `exclusive_actions`, `issued_at`).
- **Path Safety:** `_safe_id` and owned path validation reject traversal attempts (`..`, absolute paths, empty IDs, shell metacharacters).
- **Target SHA Validation:** `_valid_target_sha` enforces strict Git SHA shape (`^[0-9a-fA-F]{40,64}$`). Commands executing against non-matching heads are rejected.

---

## 6. HMAC Authentication & Replay Protection

- **HMAC Verification:** `_command_auth_valid` computes HMAC-SHA256 over the canonical serialized command body (excluding the `signature` field) using node-specific secrets (`COMMAND_HMAC_KEY`) and constant-time comparison (`hmac.compare_digest`).
- **Freshness Window:** Commands outside `COMMAND_HMAC_MAX_AGE_SECONDS` (default 900s) are rejected.
- **Replay Protection:** Executed command IDs are marked durably (`_mark_command_executed` creating `{command_id}.done` marker files in `STATE/executed_command_ids`), preventing duplicate execution of replayed command payloads.

---

## 7. Quota, Fallback & Fail-Closed Behavior

- **Network Resilience:** `git_network` employs bounded exponential backoff (base delay 2.0s up to 15.0s, 4 attempts). If network recovery fails, the transport fails closed rather than proceeding blindly.
- **Policy Ambiguity & Fail Closed:** Any missing evidence digest, schema mismatch, node identity mismatch, or stale distributed verification timestamp (>900s) forces a blocked status (`BLOCKED`).
- **No Insecure Fallback:** Authorization or capability outages never fall back to broader roles or wildcard permissions.

---

## 8. Negative Testing Coverage

Verified through test suites (`test_astra_command_auth.py`, `test_astra_security.py`, `test_astra_context_redaction.py`):
1. **Invalid/Missing HMAC Signature:** Rejected.
2. **Stale Issued Timestamp (>900s):** Rejected.
3. **Path Traversal in Command ID or Owned Paths (`../escape`, `cmd/escape`):** Rejected.
4. **Invalid Target SHA Shape (`../main`):** Rejected.
5. **Secret-Bearing Memory/Content Persistence:** Intercepted and rejected by `require_safe`.
6. **Secret-Bearing Prompt Assembly:** Redacted to `[REDACTED_SECRET]`.

---

## 9. Residual Risks & Governance Boundaries

- **Key Management:** HMAC node secrets rely on environment variables (`ASTRA_NODE_HMAC_KEY_*`). Operational security depends on secure out-of-band provisioning of these secrets.
- **Contour Separation:** Contour A remains strictly bounded to Developer Fabric. No Contour B product code mutation occurs without Master Development Roadmap gating.

---

## 10. Acceptance Criteria & Verification Status

- [x] Controller/child transport verified (`astra_github_agent.py`)
- [x] Issuer/capability & claim enforcement verified (`agent_fabric.py`)
- [x] Secret separation & redaction verified (`astra_security.py`)
- [x] Least privilege & path safety verified (`_safe_id`, `owned_paths`)
- [x] HMAC signature & replay protection verified (`_command_auth_valid`)
- [x] Fail-closed behavior on policy/evidence ambiguity verified
- [x] Zero secret values read, logged, or emitted
- [x] Draft audit checkpoint published successfully

**Verification Status:** Audit findings confirmed against immutable target SHA `f0448f28c7cfa61e4450c38529f09afbfdbbc7c7`. Ready for Pull Request.
