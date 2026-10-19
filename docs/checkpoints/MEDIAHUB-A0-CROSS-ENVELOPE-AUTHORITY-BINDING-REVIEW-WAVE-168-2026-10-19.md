# MediaHub OS — A0 cross-envelope authority-binding review, Wave 168

- Date: 2026-10-19
- Repository: `VlDMlNSh/mediahub-os`
- Source ref: `main` at `c06015e0b1526e0aaa6a522306052b077455aba5`
- Documentation work branch: `docs/contour-a-wave-163-pypi-publisher-provenance-20261019`
- Governing tracker: [Issue #301](https://github.com/VlDMlNSh/mediahub-os/issues/301)
- Status: **SOURCE CROSSWALK COMPLETE FOR REVIEWED ARTIFACTS / ISSUER DECISION OPEN / NO IMPLEMENTATION OR QUALIFICATION**
- Scope: connect the existing local command-HMAC, task-file ingress, worker workflow input and model-execution boundary findings into one non-normative acceptance/test contract. Read-only source and documentary review only.

## 1. Executive finding

The reviewed paths do not establish one authenticated authority decision that is cryptographically and semantically bound from the controller command to the exact worker task that reaches model execution.

The project has three different concepts that must remain distinct:
1. the local A0 control-command envelope and its HMAC/freshness/replay checks;
2. task JSON and task-file ingress fields, including a file-supplied `approval_state`;
3. a worker-dispatch payload and the model process that executes it.

The existence of a valid controller HMAC is not evidence that the task payload is issuer-authorized. Shape/schema validation is not issuer verification. A typed `AuthorizationContext(principal, capability)` and tuple-grant policy do not establish issuer provenance or lifecycle. The current source evidence also identifies a separate credential-isolation exposure path; cross-envelope binding alone would not fix it.

**Disposition:** define the semantic binding and negative-test requirements below as a proposal for review. Do not implement a new token format, wire protocol, issuer, key store, endpoint, or default-deny exception until the WB-05/GOV-CAP and R-06 decisions are recorded by the authorized owner/governance process.

## 2. Source evidence and pins

| Artifact | Ref / blob SHA | Observation and limit |
|---|---|---|
| `ops/control/sign_command.py` | `main`, `fc6943a79cefdf06e59d6e32771d2df551b2f0e9` | Defines `mediahub.astra.control-command.v1`, node-specific HMAC environment names and freshness checks. It is not shown to issue task approval or an `AuthorizationContext`. |
| `tools/sign_astra_command.py` | `main`, `a4222ac51a47cbfe8288f9af34f1e542c0a4b6a8` | Separate `schema: 1` envelope and generic `ASTRA_COMMAND_HMAC_KEY`; interoperability/authoritative caller is not established. |
| `runtime/mediahub_runtime/task_ingress.py` | `main`, `59e1254aa61cc8f55f53bd1e179631e81c441393` | `FileTaskIngress._read` checks shape, schema/version, owner, approval enum and context-ref shape; file-supplied approval state is not an external signed attestation. |
| `runtime/mediahub_runtime/astra_gateway.py` | `main`, `10985e4ad8f682313d08e7492ecc1856a8bce20f` | `AstraTaskRequest` carries task/command/approval/context fields but does not by itself prove issuer provenance or bind the distributed worker grant. |
| `runtime/mediahub_runtime/authorization.py` | `main`, `4d8df5d3c1c26f7f133a8093cd270635b085f4d5` | Local `AuthorizationContext` plus configured tuple-grant policy; no issuer lifecycle proof in this seam. |
| `astra_github_agent.py` | `main`, `dd2f373bf5f3d69dec951c84e3d53b0e9befab0c` | Controller HMAC verification is invoked for its command envelope; that check does not prove worker-side signed-task capability validation. |
| `runtime/mediahub_runtime/autonomous_queue.py` | `main`, `72c4a5ccb367884fb02d247b1b8848ea62c3c6b1` | Dispatch serializes task JSON into workflow input; `github_auth_env` copies process environment and may add `GH_TOKEN`. |
| `.github/workflows/astra-distributed-local-worker.yml` | `main`, `f650f2416c19dc75b4a0eeec037661c0c6169910` | Self-hosted worker path, `contents: write`, checkout `persist-credentials: true`, model-worker launch. |
| `ops/qualification/run_distributed_local_worker.py` | `main`, `42b2d53361bbd26d7fcaed82dfd710d4f09c4e6d` | Reads FCC env file and merges values into the Claude process environment; separate from authority binding. |
| Wave 148 ingress revalidation | docs ref `docs/mediahub-chat-tree-map-20261012`, blob `a0f00dd08e99e913e1f6949843e6943ecb937b15` | Explicitly records three non-equivalent paths and prohibits treating their formats as interchangeable. |
| Wave 134 call-site inventory | docs ref `docs/mediahub-chat-tree-map-20261012`, blob `cd6f6021bc5b617ef0bc581bfe4a6748515ce81e` | Direct constructors in the scanned snapshot were qualification fixtures, not an authoritative production issuer. |
| Wave 149 governance matrix | docs ref `docs/mediahub-chat-tree-map-20261012`, blob `9c1a02dc125b37abea9284f0c0aa5deb571f13e7` | GOV-CAP-01…07 and R-06 remain unresolved; no issuer/token/key-store choice is accepted. |
| MH-12 security architecture | `main`, blob `cf4ebfd5bf471ca676f075c51d3a24906504e490` (as pinned in Wave 149) | Requires capability binding to issuer, principal, operation, resource/target, scope, constraints, provenance, lifetime and revocation; explicit bounded/revocable delegation and fail-closed ambiguity. |

The source pins above are cited from the bounded Wave 148/Wave 167 traces and Wave 149 crosswalk. This pass did not independently rerun a full repository tree scan or execute the worker.

## 3. Proposed semantic binding requirements (not an accepted wire schema)

Before an implementation PR is authorized, the owner/governance decision must define a single accepted issuer/verifier authority and the protocol-level meaning of each field. The eventual verifier contract must establish, without trusting task-controlled claims alone:

- **Authentic issuer and principal:** who issued the authorization and which authenticated caller/principal is represented; no self-grant from task JSON.
- **Exact command-to-task linkage:** a stable command/run identifier, task identifier and payload digest are bound together so a valid command cannot authorize a substituted task.
- **Target and audience:** repository, immutable target commit SHA, workflow/worker identity and intended execution audience are bound; ref/HEAD drift or wrong audience is denied.
- **Operation and scope:** permitted operation, resource/path boundary, constraints and any forbidden surfaces are authorized by policy, not just prompt text.
- **Lifecycle:** issue/not-before/expiry semantics, revocation source/freshness, replay/idempotency handling and explicit bounded delegation are specified.
- **Integrity and evidence:** signature/MAC verification covers the exact canonical payload; audit records correlate decision, denial, expiry, revocation and recovery without leaking secrets.
- **Fail-closed behavior:** missing verifier, unknown issuer, unavailable mandatory audit, malformed binding, stale lease or unresolved authority denies/contains; no permissive fallback.
- **Separation of duties:** successful admission does not grant Product State Authority, publication, merge or deployment rights. Jarvis submits missions; ASTRA A0 coordinates engineering; Product State Authority alone mutates canonical product state.

This list is a semantic acceptance checklist only. It intentionally does not choose field names, serialization/canonicalization, signing algorithm, token format, issuer service, key management, audit product, or an exactly-once guarantee.

## 4. Required negative and positive conformance cases

Once governance accepts the issuer contract, implement source-bound tests against the same verifier used at worker ingress. Minimum cases to include:

| Case | Expected result |
|---|---|
| Valid issuer + matching command/task/target/audience/scope + live grant | Admit only the exact authorized task |
| Missing signature or unknown issuer | Deny |
| Valid command signature but task payload changed after signing | Deny |
| Command ID or task ID mismatch across envelopes | Deny |
| Target SHA/repository/ref/workflow audience mismatch | Deny |
| Operation, resource, path scope or constraint exceeds grant | Deny |
| Task JSON says `approval_state=approved` but no accepted signed authority attestation exists | Deny |
| Expired/not-yet-valid authorization or stale lease | Deny |
| Revoked grant or stale/unavailable revocation authority under accepted policy | Deny/contain |
| Replayed nonce/command or conflicting duplicate task | Reject or return the same idempotent outcome per accepted contract; never execute twice by assumption |
| Mandatory audit sink unavailable | Follow explicitly accepted R-06 decision; default proposal is fail closed |
| Invalid/ambiguous envelope or unsupported schema version | Deny |
| Valid controller envelope paired with a separately substituted worker payload | Deny |

These are **proposed fixtures**, not implemented or executed tests. Any exact expected result for audit availability and idempotent retries remains contingent on the owner decision.

## 5. Remediation order and separate blockers

1. Record WB-05/GOV-CAP-01…07 and R-06 decisions, including who can issue/revoke authority and audit-unavailable behavior.
2. Accept the runner/workspace/network target manifest and the worker ingress contract.
3. Specify one canonical command↔task↔target binding and migration/compatibility rules; explicitly retire or document the two incompatible signing-helper formats.
4. Implement a shared verifier at the actual worker admission boundary, before branch creation or model execution, with revision-bound positive/negative tests.
5. Independently review the verifier, fixtures, revocation/replay semantics and source-bound CI evidence.
6. Separately contain the Wave 167 credential exposure: do not assume a signed task fixes inherited `GH_TOKEN`, persistent checkout credentials or FCC credentials in the model process. Require an approved isolation/broker design and OS-level boundary before any further authorized dispatch on that path.
7. Keep merge, publication and deployment as separate authorization gates.

## 6. Verification and limits

- Reviewed current `main` HEAD: `c06015e0b1526e0aaa6a522306052b077455aba5`.
- Canonical documentation ref: `docs/mediahub-chat-tree-map-20261012`; full map Contents API response was empty, so its pinned blob `5cb5818b827c80875dd95f710a5cc8abb207379f` must be read via blob API.
- Current comparison reports documentation ref diverged from `main`: 2,333 commits ahead / 27 behind, merge base `f0f406feb9f9816b009f4e6e756813541e53b9bc`. No branch integration was attempted.
- PR #373 remains OPEN / DRAFT / UNMERGED at previously observed head `33a42629ebbdb1ab88ce1bfb4ada1adf8defcf40` at the beginning of this pass. Exact-head workflow lookup returned no workflow runs; this is not a CI pass.
- No tests executed, no code/runtime/workflow changes, no secret reads, provider calls, dispatches, host inspection, merge, deployment or qualification.
- This is not proof of exploit, credential access/exfiltration or an online runner.
- Contour A remains **NOT QUALIFIED / NOT DEPLOYED / NOT INDEPENDENTLY ACCEPTED**. Contour B remains gated.

## 7. Next bounded step

Prepare the governance decision packet for the specific issuer/lifecycle questions and obtain an explicit authorized disposition. In parallel, only perform static, read-only checks on independent blockers. Do not implement a guessed issuer or dispatch worker tasks while the trust and credential-isolation gates remain open.
