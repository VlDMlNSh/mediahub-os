# MH-CONTOUR-A-GEMINI-20261019-A1 — Security and Evidence Pass for Issue #301 and Wave 210

## Task Metadata
- **Queue ID:** MH-CONTOUR-A-GEMINI-20261019-A1
- **Contour:** Contour A (Developer Fabric)
- **Base Ref:** main
- **Branch:** mh-contour-a-gemini-20261019-a1
- **Date:** October 19, 2026
- **Target Issue:** Issue #301 / Wave 210

## Objective
Perform one bounded, source-grounded security and evidence pass inspecting the current main worker implementation (`astra_github_agent.py`) and associated contract tests (`tests/test_astra_github_agent_contract.py`). Focus specifically on subprocess environment inheritance, direct worker git publication, artifact-only worker/publisher boundary, exact-base and path validation, and missing negative-test evidence.

---

## 1. Source-Grounded Technical Inspection

### A. Subprocess Environment Inheritance & Isolation
- **Source Artifact:** `astra_github_agent.py`
- **Observations:** 
  - Subprocess execution uses explicit environment dictionaries (e.g., `isolated_env`, `fcc_env`, `direct_claude_env`, `codex_env`) derived from `os.environ.copy()`.
  - Transport collision keys (`HOST`, `PORT`, `MODEL`, `OLLAMA_BASE_URL`, `PROXY_AUTH_ENABLED`, `ANTHROPIC_AUTH_TOKEN`, `FCC_ENV_FILE`) are explicitly popped or isolated during dual executor runs (`dual_local_executor_23wave`) to prevent cross-contamination between proxy endpoints and local models.
  - Thinking and reasoning flags (e.g., `ENABLE_MODEL_THINKING`, `CLAUDE_CODE_DISABLE_THINKING`, `MAX_THINKING_TOKENS`) are explicitly normalized to avoid incompatibilities with third-party local model gateways (such as Qwen2.5-Coder on llama.cpp).

### B. Direct Worker Git Publication
- **Source Artifact:** `_prepare_publish_branch()` and `publish()` in `astra_github_agent.py`
- **Observations:**
  - Before switching to the node result branch (`astra-node/{NODE_ID}`), the worker restores the signed command path (`git restore --source=HEAD -- control/commands/{NODE_ID}.json`) or cleans untracked states to prevent worktree pollution.
  - Commits results locally (`astra: result {NODE_ID}`) and pushes with bounded retry (`git push origin HEAD:astra-node/{NODE_ID}`).
  - Fails closed on remote divergence to prevent remote history rewriting.

### C. Artifact-Only Worker / Publisher Boundary
- **Source Artifact:** `read_command()`, `_command_auth_valid()`, and `execute()` in `astra_github_agent.py`
- **Observations:**
  - Commands must be signed JSON artifacts located at `control/commands/{NODE_ID}.json` adhering to `mediahub.astra.control-command.v1`.
  - HMAC verification (`_command_auth_valid()`) uses node-specific secrets from environment mappings (`COMMAND_HMAC_ENV`) with strict maximum age checks (`COMMAND_HMAC_MAX_AGE_SECONDS`).
  - Claim leasing (`AgentClaim`, `ClaimStore` in `mediahub_runtime.agent_fabric`) enforces strict task lifecycle boundaries.
  - Product State Authority alone owns canonical MediaHub product-state mutation; workers operate strictly within transport and qualification fabric bounds.

### D. Exact-Base and Path Validation
- **Source Artifact:** `read_command()` in `astra_github_agent.py`
- **Observations:**
  - Validates `schema_version`, safe command IDs (`SAFE_ID_RE`), node ID match, operation whitelist (`OPERATIONS`), and exact target SHA validity (`SHA_RE`).
  - Owned paths are strictly validated: must be relative paths (`not Path(p).is_absolute()`) and prohibit path traversal (`".." not in Path(p).parts`).
  - Autonomous gold missions enforce exact target SHA matching (`target_sha_not_exact_current_head` and `target_sha_changed_during_retry`).

### E. Missing Negative-Test Evidence
- **Source Artifact:** `tests/test_astra_github_agent_contract.py`
- **Observations:**
  - Comprehensive positive contract tests verify G4 model routing, git retry bounded loops, signature validation, and recovery marking.
  - **Gaps / Recommendations:** Explicit negative-test assertions covering invalid environment injection attempts, malformed HMAC signature tampering under concurrent load, and path traversal rejection in owned paths should be added to further harden test coverage against adversarial command inputs.

---

## 2. Evidence Versus Inference
- **Empirical Evidence:** Direct code inspection of `astra_github_agent.py` (SHA: `dd2f373bf5f3d69dec951c84e3d53b0e9befab0c`) and `tests/test_astra_github_agent_contract.py` (SHA: `7dc0b70c9b5c3e0ef664749d5527b71740cb1656`).
- **Inference:** The runtime environment and transport protocol maintain strict isolation and fail-closed security properties as specified in Baseline 2.0 governance contracts.

---

## 3. Acceptance Criteria Status
- [x] Source-grounded security/evidence pass completed for Issue #301 and Wave 210.
- [x] Focus areas analyzed: subprocess environment inheritance, direct worker git publication, artifact-only worker/publisher boundary, exact-base and path validation, and missing negative-test evidence.
- [x] Dedicated branch created (`mh-contour-a-gemini-20261019-a1`).
- [x] Checkpoint artifact created and committed (`recovery/mh-contour-a-gemini-20261019-a1.md`).

---

## 4. Blockers & Known Limitations
- GitHub Actions token security policies restrict automated pull request creation (`403` error when opening PRs via GITHUB_TOKEN in restricted workflows). PR creation will be attempted via `mcp_github_create_pull_request`.

---

## 5. Next Step
- Submit review and checkpoint for maintainer evaluation under Contour A governance guidelines.
