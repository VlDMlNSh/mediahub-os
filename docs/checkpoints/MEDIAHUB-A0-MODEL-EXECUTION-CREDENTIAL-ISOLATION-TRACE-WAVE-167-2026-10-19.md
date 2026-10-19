# MediaHub OS — A0 model-execution credential-isolation trace — Wave 167

- Date: 2026-10-19
- Status: **SOURCE-BOUND EXPOSURE PATH VERIFIED / NO EXPLOITATION OBSERVED / REMEDIATION AND QUALIFICATION OPEN**
- Repository: `VlDMlNSh/mediahub-os`
- Work branch: `docs/contour-a-wave-163-pypi-publisher-provenance-20261019`
- Governing tracker: [Issue #301](https://github.com/VlDMlNSh/mediahub-os/issues/301)
- Canonical map: [MEDIAHUB-CHAT-TREE-MAP.md](../architecture/MEDIAHUB-CHAT-TREE-MAP.md)
- Scope: read-only trace of current `main` from queue dispatch through the self-hosted GitHub Actions worker into model-controlled execution. No runner or workflow was dispatched.

## 1. Exact source evidence

| Component | Ref / blob SHA | Relevant source behavior |
|---|---|---|
| `astra_github_agent.py` | `main`, `dd2f373bf5f3d69dec951c84e3d53b0e9befab0c` | HMAC command verification exists in `_command_auth_valid` and is invoked by `read_command`; this verifies the controller command envelope only. For `autonomous_gold_mission`, `execute` copies the full process environment using `os.environ.copy()` and passes it to the autonomous queue subprocess. |
| `runtime/mediahub_runtime/autonomous_queue.py` | `main`, `72c4a5ccb367884fb02d247b1b8848ea62c3c6b1` | `github_auth_env` copies the process environment and may add the authenticated `gh auth token` as `GH_TOKEN`. Dispatch passes the full serialized task as `task_json` to `.github/workflows/astra-distributed-local-worker.yml`. |
| `.github/workflows/astra-distributed-local-worker.yml` | `main`, `f650f2416c19dc75b4a0eeec037661c0c6169910` | All three jobs use self-hosted runners, workflow-level `permissions: contents: write`, checkout with `persist-credentials: true`, and a model-worker script. Each job points `ASTRA_FCC_ENV_FILE` to a runner-local file. |
| `ops/qualification/run_distributed_local_worker.py` | `main`, `42b2d53361bbd26d7fcaed82dfd710d4f09c4e6d` | `load_env_file` reads the complete FCC env file. `exec_claude` copies `os.environ`, merges those values, puts the FCC token into `ANTHROPIC_AUTH_TOKEN` and `ANTHROPIC_API_KEY`, and launches Claude Code with `Read`, `Edit`, `Bash(git *)` and `Bash(python *)` tools for the non-structured path. |

## 2. Verified exposure path and confidence

### A. FCC token enters the model-client process

The worker reads the runner-local FCC environment file into a Python dictionary. The Claude execution path then merges the file's values into a copy of the inherited environment and sets both `ANTHROPIC_AUTH_TOKEN` and `ANTHROPIC_API_KEY` to the FCC token before starting the Claude Code process.

**Conclusion:** the FCC credential is present in the model-client process environment, not isolated behind a separate credential broker. Because the process is granted shell/Python tools, its execution boundary must be treated as potentially able to inspect inherited process state. This is a source-derived exposure path; this review did not read the runner's actual env file, inspect a live process, or observe token access/exfiltration. The code names the token as FCC authentication; it is not established here to be a commercial provider key.

### B. Git write credential remains configured in the model's checkout

The worker workflow requests `contents: write` and sets `persist-credentials: true` for checkout. The same job subsequently starts the model worker in that checked-out repository, and the model tool allow-list includes Git commands.

**Conclusion:** the checkout's persisted Git authentication is inside the same workspace/process trust boundary as model-controlled Git commands. This is a potential path for a model task to inspect or misuse the job's Git write authority. The exact token value, active permission scope, branch protections and any attempted access were not inspected; no exploitation is claimed.

### C. Task-boundary enforcement is not process isolation

The task prompt describes allowed/forbidden paths and the worker later evaluates changed-path scope. These are useful controls, but they do not themselves establish OS-level read isolation or remove credentials from the model process. The GitHub workflow input is described as a “Full signed task payload”; this review verified the dispatch path but did not establish a verifier for a signed task capability at the worker boundary.

### D. HMAC boundary is not equivalent to capability authorization

The controller's HMAC command check and replay marker protect that local command envelope under their configured assumptions. They do not by themselves prove the worker workflow verifies an issuer-bound grant with principal, audience, operation, resource, scope, expiry and revocation semantics. Wave 149 still records GOV-CAP-01…07 and R-06 as unresolved; no authority option is selected.

## 3. Risk disposition

- **High-priority design finding:** model-controlled execution shares a process/workspace trust boundary with at least an FCC credential and a checkout configured to retain Git write authentication.
- **Not proven:** that any real runner is currently online, that the credential file contains a live/valuable external token, that a token was read or exfiltrated, or that a malicious task was run.
- **Not in scope / not done:** no secret values were read; no host inventory, process inspection, live workflow, queue dispatch, provider call, credential test, or exploitation test was performed.
- Existing worker workflow is on `main`; this is not limited to Draft PR #338. Unlike the setuptools provenance issue, this finding concerns the current source path and should be tracked independently of candidate-only lock generation.

## 4. Remediation sequence — proposals, not implementation

1. **Contain credential reachability before expanding autonomy:** do not dispatch model-controlled work on self-hosted lanes with privileged credentials until an owner-approved isolation change is reviewed. This report does not itself disable any runner or workflow.
2. Split orchestration credentials from model execution. Keep GitHub dispatch/publish credentials in a narrow controller or broker process that never launches model-controlled tools; grant a separate, short-lived, narrowly scoped credential only to a post-verification publisher step.
3. Remove persistent checkout credentials from the model workspace. Use read-only checkout for model execution and perform branch publication in a separate, bounded step after independent diff/scope verification. If publication is required, avoid workflow-wide `contents: write` for the model job.
4. Do not inject the FCC auth token into the general Claude tool process. Prefer a local proxy/broker that owns the token and exposes only a narrow authenticated interface; confirm the token's actual purpose, privilege and lifetime through the authorized secret owner without disclosing its value.
5. Enforce filesystem, network, process and syscall boundaries independently of prompt instructions and post-hoc changed-path checks. Prove negative cases for reading secret files, reading Git credential config, environment enumeration, arbitrary network access, and writes outside the declared worktree.
6. Add worker-ingress verification for task provenance and capability constraints only after GOV-CAP-01…07 and R-06 are explicitly resolved. Preserve the separation between Jarvis coordination, ASTRA A0 workflow state and MediaHub Product State Authority.
7. Require independent security review, fresh exact-head negative tests, auditable run/job/artifact identifiers and digests, and a separate qualification decision before restoring broader dispatch.

## 5. Evidence boundary and project status

This pass inspected source blobs and governance records and created documentation only. It did not change code, workflow permissions, secrets, hosts, runner state, queues, dependencies, branch protection, or deployment. No CI pass, credential isolation, security qualification, or acceptance is claimed.

**Disposition:** current-main source shows a credible credential exposure path at the model-worker boundary; containment/remediation is open and requires owner-authorized engineering plus independent verification. Contour A remains **NOT QUALIFIED / NOT DEPLOYED / NOT INDEPENDENTLY ACCEPTED**. Contour B remains gated.
