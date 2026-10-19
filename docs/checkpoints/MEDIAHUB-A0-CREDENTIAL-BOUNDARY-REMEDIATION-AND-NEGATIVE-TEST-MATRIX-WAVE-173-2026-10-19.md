# MediaHub OS — A0 credential-boundary remediation and negative-test matrix — Wave 173

- Date: 2026-10-19
- Status: **DESIGN / SOURCE REVIEW ONLY — NO REMEDIATION IMPLEMENTED OR QUALIFIED**
- Repository: `VlDMlNSh/mediahub-os`
- Work branch: `docs/contour-a-wave-163-pypi-publisher-provenance-20261019`
- Governing tracker: [Issue #301](https://github.com/VlDMlNSh/mediahub-os/issues/301)
- Prior source trace: [Wave 167 credential-isolation trace](MEDIAHUB-A0-MODEL-EXECUTION-CREDENTIAL-ISOLATION-TRACE-WAVE-167-2026-10-19.md)
- Canonical project map: [MEDIAHUB-CHAT-TREE-MAP.md](../architecture/MEDIAHUB-CHAT-TREE-MAP.md)

## 1. Purpose and decision boundary

Wave 167 identified a source-bound credential exposure path across queue dispatch, a self-hosted Actions worker, FCC environment loading, and model-controlled execution. This wave converts that finding into a bounded remediation architecture and testable acceptance matrix. It does **not** claim a live exploit, credential theft, or that every credential in the environment is exploitable. No credentials were read, no worker was dispatched, and no code, host, workflow, secret, or runtime state was changed.

Recommended interim posture: treat the affected autonomous execution route as **not qualified for further model-controlled dispatch until an owner-authorized containment decision and credential-boundary review are recorded**. This is a recommendation, not a claim that a runner was disabled or that a governance decision was made.

## 2. Source pins rechecked on `main`

| Component | Blob SHA | Source-bound observation |
|---|---|---|
| `astra_github_agent.py` | `dd2f373bf5f3d69dec951c84e3d53b0e9befab0c` | HMAC validation applies to the controller command envelope; it is not by itself a scoped, issuer-bound worker capability. |
| `runtime/mediahub_runtime/autonomous_queue.py` | `72c4a5ccb367884fb02d247b1b8848ea62c3c6b1` | `github_auth_env()` copies `os.environ` and may place an authenticated `gh auth token` in `GH_TOKEN` before remote workflow dispatch. |
| `.github/workflows/astra-distributed-local-worker.yml` | `f650f2416c19dc75b4a0eeec037661c0c6169910` | Self-hosted jobs request `contents: write`, use checkout with `persist-credentials: true`, and run the worker in the checkout. |
| `ops/qualification/run_distributed_local_worker.py` | `42b2d53361bbd26d7fcaed82dfd710d4f09c4e6d` | FCC env-file values are loaded; values are merged into the Claude process environment, including `ANTHROPIC_AUTH_TOKEN` and `ANTHROPIC_API_KEY`. The non-structured execution path grants Read/Edit and `Bash(git *)` / `Bash(python *)`. |

The source establishes an exposure path, not proof of access or exfiltration. The FCC token's upstream privilege, audience, expiry, and ability to reach any external service were not independently established in this pass. A task prompt, path allowlist, or post-hoc diff check is not an operating-system security boundary.

## 3. Target boundary architecture

Separate the system into three trust domains. Do not pass publisher/dispatcher credentials into a process that executes model-generated instructions.

1. **Controller / dispatcher domain**
   - Owns GitHub dispatch identity and the ability to publish accepted evidence.
   - Produces a signed, short-lived task capability bound to issuer identity, task ID, node/worker identity, immutable source SHA, allowed paths/actions, audience, issued-at/expiry, nonce, and revocation/lease state.
   - Does not forward its ambient process environment or GitHub token to the model worker.
   - Uses an explicit, minimal environment allowlist for each subprocess; never inherit the complete controller environment by default.

2. **Model execution domain**
   - Runs under a distinct OS identity or isolated ephemeral workspace with no controller credential files, no publisher token, no authenticated Git checkout, and no access to the controller's home/config directories.
   - Receives only non-secret task inputs and a narrowly scoped capability that is verified before execution. Prefer broker-mediated operations over direct tokens.
   - Has deny-by-default network egress; permit only endpoints required for the selected model route and explicitly approved tools. Local FCC endpoints must not become a general network pivot.
   - Produces an untrusted patch/result bundle and evidence; it cannot publish, dispatch follow-up work, merge, or alter canonical product state.

3. **Evidence / publisher domain**
   - Independently validates task identity, capability, source SHA, path scope, patch format, test evidence, run/job/attempt/artifact identity, and digests.
   - Publishes only after policy gates pass, using a separate publisher identity and a clean, credential-minimized checkout.
   - Treats model output and worker-generated metadata as untrusted input; the publisher derives provenance from GitHub/controller records rather than trusting claims inside the artifact.

These domains are a proposed design, not an accepted architecture change. Governance and owner approvals remain required before implementation or host containment actions.

## 4. Remediation sequence and gates

| Order | Work item | Required evidence / exit condition |
|---|---|---|
| R1 | Record owner-authorized interim dispatch posture and named authority | Decision is linked to Issue #301; scope and expiry/revisit condition are explicit. No implicit authority inferred from this report. |
| R2 | Inventory credential classes and capabilities without revealing values | Names/locations, issuer, audience, scope, TTL/rotation, consumer processes, and revocation procedure; redact values. Distinguish GitHub checkout credential, `GH_TOKEN`, FCC token, provider keys, and OS credentials. |
| R3 | Define task capability and issuer contract | Schema and verifier bind issuer, audience, task, worker, immutable SHA, allowed actions/paths, expiry, nonce/idempotency, lease/cancel/revocation, and evidence correlation. Invalid or ambiguous inputs fail closed. |
| R4 | Remove ambient credential inheritance | Explicit environment allowlists; model process receives no dispatcher token, inherited `GITHUB_TOKEN`/`GH_TOKEN`, provider key, or credential-file path. Add static regression tests. |
| R5 | Separate checkout and publishing | Model workspace has no persisted checkout credentials and cannot push/dispatch. Publisher uses a separate clean workspace and short-lived least-privilege credential after independent verification. |
| R6 | Enforce OS and network isolation | Distinct identity/workspace, no read access to controller home/secrets, no shared writable credential/config directories, egress allowlist, bounded process and filesystem access. Document platform-specific implementation and threat assumptions. |
| R7 | Add negative tests and prove no secret propagation | Tests below pass with sentinel values; assert they are absent from child environments, prompt, logs, artifacts, result metadata, and workspace. |
| R8 | Independent review and controlled qualification | Independent reviewer verifies exact source SHA, test run IDs, artifact digests, isolation configuration, and rollback/revocation behavior. Only then request a separately authorized controlled dispatch. |

## 5. Required negative-test matrix

Tests must use synthetic sentinel strings only. Never use a live credential as a test fixture. Test harnesses should capture child environment key names and synthetic values only in memory, then assert expected absence; reports must not print values.

| ID | Adversarial fixture | Expected fail-closed result |
|---|---|---|
| CB-01 | Controller environment contains synthetic `GH_TOKEN` and `GITHUB_TOKEN` | Model child receives neither variable; dispatch client and model runner use separate environment builders. |
| CB-02 | `gh auth token` returns a synthetic token | Token is held only by the dispatch/publisher client and is not serialized into task JSON, prompt, logs, worker environment, or artifact. |
| CB-03 | FCC env file contains synthetic auth value plus unexpected keys | Parser enforces an exact key allowlist; unknown keys reject or are explicitly ignored with safe diagnostics. No FCC auth value is copied to the model process unless a documented broker design proves it is unavoidable and non-authoritative. |
| CB-04 | Checkout credential persistence is enabled in workflow fixture | Workflow policy test fails; model workspace must not contain a credential-bearing Git config or usable remote auth. |
| CB-05 | Task asks model to read controller home, secret files, environment, or Git credentials | OS-level access denied; negative test confirms no readable path or credential-bearing process environment. Prompt refusal alone is not a pass. |
| CB-06 | Model tries `git push`, workflow dispatch, merge, or publisher API | Operation is unavailable/denied by identity and network policy; no remote state changes. |
| CB-07 | Capability has missing issuer/audience/task/worker/SHA/expiry/nonce fields | Reject before task claim or process start; emit stable reason code without secret material. |
| CB-08 | Capability is signed by untrusted issuer, altered, expired, replayed, or revoked | Reject; replay is idempotently blocked; expiry and revocation are checked against authoritative state. |
| CB-09 | Task source SHA differs from checked-out SHA or evidence run SHA | Reject; no fallback to mutable branch names or title-only correlation. |
| CB-10 | Task boundary is empty, malformed, absolute, traversal-based, or conflicts with forbidden paths | Reject at schema and runtime layers; do not treat prompt instructions as enforcement. |
| CB-11 | Child process inherits proxy, cloud, SSH, package, or provider credential variables unexpectedly | Child environment allowlist test fails; only explicitly approved non-secret variables remain. |
| CB-12 | Model writes a forged success verdict or artifact metadata | Independent verifier recomputes changed paths, test status, run/job/attempt identity, and digest; worker assertion alone cannot authorize publication. |
| CB-13 | Cancellation/revocation occurs during a running task | Broker blocks subsequent privileged operations, lease expires, worker is terminated or quarantined according to the approved contract, and evidence records the terminal state. |
| CB-14 | Logs/errors contain synthetic sentinel strings | Redaction/secret-scan test fails the run if any sentinel reaches logs, prompts, artifacts, or persisted result files. |

## 6. Acceptance criteria

The remediation is not complete until all are true:

- No model-controlled process receives publisher/dispatcher credentials or can read their source files.
- Git checkout used by the model contains no persisted credential and has no write/push capability.
- Capability verification is issuer-bound and covers scope, immutable source SHA, audience, expiry, replay, cancellation, and revocation.
- OS and network boundaries independently enforce the intended limits; tests do not rely on model compliance.
- Every negative test has a reproducible test name, tool/version, exact commit SHA, result, and artifact digest.
- A reviewer independent of the implementer signs off on the exact candidate SHA and evidence.
- Owner/governance authorization is separately recorded before any controlled dispatch, merge, or deployment.

## 7. Evidence limits and next step

- This was a read-only source review of the pinned `main` blobs listed above.
- No tests were run; no runner state, secret values, provider account, or live workflow was accessed.
- No code or workflow remediation was implemented. This report is not a security qualification, acceptance, deployment, or evidence of credential misuse.
- Next: obtain/record the authorized containment decision, then implement the smallest isolated change on a dedicated code branch with synthetic negative tests. Keep PR promotion, merge, deployment, and Contour A acceptance as separate gates.

Contour A remains **NOT QUALIFIED / NOT DEPLOYED / NOT INDEPENDENTLY ACCEPTED**. Contour B remains blocked.
