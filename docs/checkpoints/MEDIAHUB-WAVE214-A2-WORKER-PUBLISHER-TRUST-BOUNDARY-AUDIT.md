# MediaHub OS — Contour A: Source-Bound Worker / Publisher Trust-Boundary Audit

- **Task ID:** `MH-CONTOUR-A-GEMINI-WAVE214-A2`
- **Agent Identity:** `gemini-agent-2` (Research & Architecture)
- **Authorized Contour:** Contour A (Developer Fabric)
- **Base Ref / Target SHA:** `main` (`25033753415fcbecdc7b2fe53085ed1bf2e4b8b4`)
- **Associated Issue:** Issue #301
- **Status:** Completed (Documentation-Only Source-Bound Audit)

---

## 1. Inspected Files & Provenance SHAs

| File Path | SHA-256 Blob / Content Reference | Primary Role in Trust Boundary |
|---|---|---|
| `astra_github_agent.py` | `dd2f373bf5f3d69dec951c84e3d53b0e9befab0c` | Astra GitHub Transport Worker & Execution Loop |
| `ops/astra_orchestrator.py` | `7e22a283ddbbdfeceeea9aa1bd01c33fdbf7cfb8` | Resident Astra Development Coordinator & Liveness Reconciler |
| `architecture/SECURITY-TRUST-AUTHORIZATION-CONTRACT.md` | `8d831c2a8fa333977dd86524099568bae2a8db0e` | Security, Trust, and Authorization Architectural Baseline |
| `tests/test_astra_security.py` | `6761edb5e1e9e035388aabcd1b95d240098c2ec4` | Security Redaction & Persistence Gate Tests |
| `tests/test_astra_github_agent_contract.py` | `7dc0b70c9b5c3e0ef664749d5527b71740cb1656` | Transport Contract, Git Retry, Signer & Execution Tests |

---

## 2. Trust Boundary Architecture & Trace Analysis

### A. Subprocess Environment Inheritance & Isolation
- **Invocation & Shell Safety:** Subprocesses are invoked via explicit argument lists (`subprocess.run(argv, ...)` with `check=False` or `check=True`) without shell expansion (`shell=True` is avoided across all core agent and worker logic).
- **Environment Bounding:**
  - Specialized execution paths (e.g., `dual_local_executor_23wave`, `codex_provider_diagnostic`, `codex_gateway_diagnostic`) explicitly construct isolated environment dictionaries (e.g., `isolated_env`, `fcc_env`, `direct_claude_env`) rather than blindly inheriting unverified process environment variables.
  - Transport collision keys (such as `HOST`, `PORT`, `MODEL`, `OLLAMA_BASE_URL`, `PROXY_AUTH_ENABLED`, `ANTHROPIC_AUTH_TOKEN`, `FCC_ENV_FILE`) are explicitly popped or overridden.
  - Thinking and reasoning flags are explicitly disabled (`ENABLE_MODEL_THINKING = "false"`, `CLAUDE_CODE_DISABLE_THINKING = "1"`, `MAX_THINKING_TOKENS = "0"`) when interacting with local or compatibility gateways.
- **Credential Suppression:** Serialized results and diagnostics explicitly enforce secret suppression (`"secret_values": "SUPPRESSED"`), ensuring that raw tokens, API keys, or private material are never leaked into execution payloads or published result logs.

### B. Worker Git Add / Commit / Push Behavior
- **Consumed Command Cleanup:** Before switching branches or publishing results, `_prepare_publish_branch()` restores the consumed command file (`control/commands/{NODE_ID}.json`) via `git restore --source=HEAD -- control/commands/{NODE_ID}.json` (with fallback to `git clean -f -- control/commands/{NODE_ID}.json` if untracked). This guarantees that consumed transport commands do not remain as dirty worktree modifications when switching branches.
- **Git Author Identity:** Configured locally to non-privileged worker identities (`user.name "Astra Node Agent"`, `user.email "astra-node@localhost"`).
- **Branch and Push Isolation:**
  - Results are written to `control/results/{NODE_ID}.json`.
  - Staged locally under `STATE/publish-{NODE_ID}.json` before writing to the worktree path.
  - Committed with message `astra: result {NODE_ID}`.
  - Pushed exclusively to the node-specific remote branch (`origin/astra-node/{NODE_ID}`).
  - Fails closed on concurrent or stale publish conflicts; never rewrites main or shared release branches.
  - Immediately detaches back to `origin/main` after push completion.

### C. Artifacts & Output Paths
- **Control & Command Inputs:** Read exclusively from `control/commands/{NODE_ID}.json`.
- **Result & State Outputs:** Written to `control/results/{NODE_ID}.json`, cached locally in `STATE/last_command_id`, `STATE/claims`, and `STATE/mission-journal.json`.
- **Execution Evidence:** Captured in structured JSON schemas (e.g., `mediahub.provider-model-qualification.v1`, `mediahub.astra.distributed-verification.v1`, `mediahub.astra-gold.g4-round.v1`).

### D. Publisher Credential Boundary & Security Invariants
- **Command Authentication:** Signed commands must include a valid HMAC-SHA256 signature (`_command_auth_valid`) computed against the canonical command JSON body using node-specific secrets (`COMMAND_HMAC_ENV`, mapped per node ID such as `ASTRA_NODE_HMAC_KEY_MH_DEV_01`).
- **Age Validation:** Commands exceeding `COMMAND_HMAC_MAX_AGE_SECONDS` (default 900s) are rejected.
- **Replay Protection:** Executed command IDs are recorded in `EXECUTED_COMMANDS/{command_id}.done` to prevent replay attacks.
- **Target SHA Binding:** Execution requires exact current HEAD match (`_current_head().lower() == cmd["target_sha"].lower()`).
- **Product State Separation:** AI agents, transport workers, and queues operate strictly within Contour A (Developer Fabric) and possess zero product-state mutation authority; Product State Authority alone owns canonical product-state changes.

---

## 3. Negative Tests & Contract Dependencies

The test suite (`tests/test_astra_github_agent_contract.py` and `tests/test_astra_security.py`) enforces strict negative tests and contract boundaries:
1. **Schema Validation:** Rejects payloads with incorrect schema versions (`mediahub.astra.control-command.v1` required).
2. **Key Isolation:** Verifies node-specific HMAC key resolution and rejects wildcard or unmapped fallback keys.
3. **Exact Head Binding:** Autonomous mission execution fails immediately if target SHA does not match current exact HEAD.
4. **Command Cleanup:** Verifies that `_prepare_publish_branch()` restores the command file before branch operations.
5. **Secret Redaction & Persistence Gates:** `tests/test_astra_security.py` confirms that secret-like patterns are detected and redacted, and persistence gates (`require_safe`) raise `ValueError` on unredacted secret content.
6. **Network Resilience:** Git network operations use bounded exponential backoffs with strict failure-closed retry termination.

---

## 4. Known Gaps & Observations (Non-Mutating)

1. **Environment Secret Hygiene:** While transport layers suppress secret values in published results, host environments must ensure that secret environment variables are restricted to authorized service users and not exposed in process listings (`/proc/*/cmdline`).
2. **Remote Branch Evolution:** The worker relies on explicit remote branch fetching (`git fetch origin +astra-node/{NODE_ID}:refs/remotes/origin/astra-node/{NODE_ID}`) to detect state drift before publishing results.
3. **Scope Enforcement:** Contour A developer fabric tooling remains fully isolated from product state changes, preserving architectural layering.

---
*End of Audit Report.*
