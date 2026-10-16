# MediaHub OS — Cloud-Agent Autonomous Development Fabric, Wave 35

- Date: 2026-10-17
- ID: MH-CLOUD-AGENT-FABRIC-W35
- Contour: A — Developer Fabric
- Status: **REFERENCE DESIGN PROPOSED / EXISTING COMPONENTS REUSED / IMPLEMENTATION AND RUNTIME QUALIFICATION OPEN**
- Repository: `VlDMlNSh/mediahub-os`
- Documentation ref: `docs/mediahub-chat-tree-map-20261012`
- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md

## 1. Decision summary

Use one MediaHub-owned admission policy and one A0/ASTRA-owned engineering queue lifecycle. Treat cloud coding agents, hosted CI workers and model providers as replaceable execution adapters. Enroll each adapter once, then route only tasks whose immutable source revision, data class, path scope, provider/model, destination, permissions, quota and evidence requirements fit its admission record.

Reuse the current Agent Fabric and 23-lane manifest where their contracts apply. Do not create a competing task lifecycle or a second canonical product-state authority. Cloud agents return evidence and candidate patches; an independent verifier and existing governance gates control promotion.

This is a proposal, not an acceptance of the current runtime. The current qualification truth marks G0–G11 BLOCKED and overall status NOT_PROVEN / BLOCKED. The 23-lane manifest still contains extensive UNKNOWN ownership, SHA, lease and worker fields. A passing unit-test file or a successful historical provider run alone does not qualify the distributed queue.

## 2. Live source baseline and reused components

The following source-bound evidence was read during this pass:

| Existing artifact | Ref | Blob SHA | What it establishes |
|---|---|---|---|
| 23-lane execution manifest | `main:ops/agent-fabric/manifest/mediahub-23-lane-execution-manifest.json` | `b948f0beb510f24399d82aaefcb7f95584e99cab` | Existing 23-lane registry format; promotion requires exact base/head/owner/lease/worker/verification evidence; global dependency order remains UNKNOWN. |
| Agent Fabric claim/lease primitives | `main:runtime/mediahub_runtime/agent_fabric.py` | `3c70dda5df8c6caa9411201d754ead6b3bfdf6dd` | File-backed claim records, path overlap checks, local advisory locking, heartbeat, expiry and release. |
| Agent Fabric tests | `main:tests/test_agent_fabric.py` | `ed64595a6e396fc4d58c08b47bf708cd92b1275b` | Existing tests cover collision, expiry, heartbeat, release, concurrent claim acquisition and one distributed-worker contract. These are source evidence only; no tests were run in this pass. |
| Agent Fabric verification workflow | `main:.github/workflows/mediahub-agent-fabric-verify.yml` | `2cec0ba1f02018f7037417363c707a13bc673117` | Existing verifier is path-filtered on `main` plus manual dispatch and currently grants `contents: read`. |
| Current ASTRA qualification truth | `main:docs/qualification/CURRENT-TRUTH.generated.md` | `48d581a8f6a6a5fd380abbb7a7ce938b3b1e6731` | G0–G11 all BLOCKED; overall NOT_PROVEN / BLOCKED; promotion ladder is explicit. |
| Existing cloud-agent enrollment direction | docs Wave 11 | `8467ad1dbe349ea12cb735da3542b73df68b7446` | Credentials belong to provider/account/project scope and authorized secret references, rather than being attached permanently to one of the three servers. |
| Provider secret-flow/egress crosswalk | docs Wave 30 | `28a5152b60b0809a90a0c938b81439b8a19852b7` | Current source review identifies broad qualification environment exposure, configurable endpoints, a Gemini query-string key path, and the absence of a proven task-scoped credential broker / common destination gate. |

The documented implementation already has useful primitives. The gap is a revision-bound, distributed admission and evidence contract across ephemeral workers and cloud agent identities, not a need to rebuild a generic agent framework.

## 3. Reference architecture

```text
Owner / Policy Decision
        |
        v
Provider + Agent Admission Registry ---- Secret reference catalog (values stay outside task data)
        |
        v
A0 / ASTRA queue lifecycle ---- durable claim authority / idempotency / cancellation / audit
        |
        v
Task policy gate: source SHA, data class, provider/model, destination, paths, capabilities, budget
        |
        +---- hosted CI/read-only worker
        +---- authorized SaaS GitHub agent
        +---- authorized cloud coding worker
        +---- approved local worker
        |
        v
Isolated task workspace + topic branch + immutable artifact/evidence manifest
        |
        v
Independent path/diff/schema/test verification
        |
        v
Existing A0 gates / review / release governance
        |
        v
PR candidate; integration/release/deployment remain separate authorized stages
```

The queue, its leases and promotion authority remain within the accepted ASTRA/A0 boundary. The agent/provider registry is an admission catalog, not a second scheduler or policy authority. Provider adapters can change without changing the queue contract. Cloud model output and tool output remain untrusted input.

## 4. Agent admission record

Every agent entry must have these fields before it may claim work:

- `agent_id`: stable project identifier, unique within the registry.
- `integration_kind`: SaaS GitHub App, GitHub-hosted workflow worker, cloud worker API, or local worker.
- `provider_account_ref`, `provider_project_ref`, `credential_ref`: opaque references only; never store credentials in a JSON task, prompt, source control, output artifact or log.
- `auth_mode`: provider OAuth/GitHub App, short-lived federation where supported, or a scoped secret reference; record the actual supported mode rather than assuming universal OIDC.
- `permitted_repositories`, `permitted_refs`, `permitted_paths`, `capabilities` and `output_modes`.
- `allowed_data_classes`, `allowed_provider_models`, `allowed_destinations`, `egress_region_policy` and `data_policy_evidence_ref`.
- `quota_policy`, `max_concurrency`, `budget_ceiling`, `timeout`, `retry_policy` and `fallback_destinations`.
- `admission_state`, `last_auth_evidence`, `last_policy_review`, `expires_at`, `revocation_state` and `reviewer`.
- `verification_profile`, `artifact_manifest_schema` and `independent_verifier_class`.

The canonical state sequence is:

`CANDIDATE → REGISTERED → POLICY_REVIEWED → CREDENTIAL_REFERENCE_CONFIGURED → AUTH_PROBE_PASSED → READ_ONLY_ADMITTED → PATCH_WORKER_ADMITTED → QUALIFIED → ENABLED`

`BLOCKED`, `EXPIRED` and `REVOKED` are terminal admission outcomes until an authorized re-enrollment. A configured secret reference alone does not prove valid authentication. A successful authentication probe alone does not qualify write access. Credential values must remain entirely outside this workflow.

## 5. Enrollment and activation protocol

1. Discover an existing agent or provider integration and map its actual upstream repository/product, supported auth mechanism, license/terms, quota, region/data policy, tool permissions and update path. Reuse a stable existing project component when it covers the need.
2. Add a candidate registry entry using non-secret metadata. Mark all unverified claims UNKNOWN.
3. The owner authorizes the specific account/app/repository and completes authentication in the provider's or GitHub's own UI. The assistant and task workers receive only the named secret reference or integration identity, never the raw credential.
4. Review provider eligibility, region, data retention/training policy, acceptable use, endpoint identity and route-specific data classes. A failed or unknown gate produces BLOCKED.
5. Configure a repository/environment-scoped secret only for integrations that require a static credential. Use separate secrets per provider and job. Prefer short-lived federation only when that exact service supports and has accepted the trust configuration.
6. Run an auth/model-discovery probe only after explicit authorization for that exact provider, account/project, model, data class, destination, cost ceiling and request budget. Redact outputs and do not return secrets.
7. Admit the worker read-only first, using a bounded synthetic or low-sensitivity task. Check revision pinning, artifact integrity, timeout/cancel behavior, audit records and independent verification.
8. Grant patch-producing capability only after the read-only evidence is accepted. Restrict path scope, branch write capability and runner workspace. Never grant the agent direct merge, release, deployment, secret administration or canonical product-state authority.
9. On revocation, provider policy change, unexpected destination, 401/403, eligibility denial or evidence expiry, block new claims and cancel queued tasks that depend on that route. Never rotate accounts or change egress to evade a refusal.

Activation should be event-driven from confirmed admission state. Merely adding a secret, clicking OAuth consent or registering an agent must not silently launch model work.

## 6. Durable queue and task envelope

The task record must bind:

- `task_id`, idempotency key, parent task, dependencies and owner/approver;
- repository, immutable `base_sha`, accepted task branch and current `head_sha`;
- stable `agent_id`, provider/model route, credential reference ID and admission/policy revisions;
- data class, allowed context paths, permitted reads/writes, tool capabilities and forbidden side effects;
- deadline, lease interval, heartbeat, cancellation generation, attempt counter, retry budget, concurrency group and spend ceiling;
- expected outputs, changed-path allowlist, validation commands approved for the task, verifier identity and evidence schema;
- output artifact digest, run identifier, sanitized audit events, result status and review references.

Secret values, reusable auth tokens, raw provider error bodies and unrestricted repository snapshots are excluded from task payloads and artifacts.

Reuse the existing `WAIT / READY / CLAIMED / VERIFY / BLOCKED / CLOSED` lane vocabulary. Task-local execution statuses may become more detailed only through a versioned schema change that preserves existing IDs and maps losslessly to the canonical lane state. Each retry has a bounded attempt count and immutable source identity.

## 7. Distributed-claim correctness is the primary engineering gate

The existing `ClaimStore` uses local files, `fcntl` locking and expiry-based reclamation. This is useful for processes that share the same filesystem, but separate ephemeral cloud runners ordinarily have separate filesystems. It therefore cannot by itself prove atomic distributed claims across independent hosted runners.

Before parallel cloud workers are enabled, A0 must name one durable claim authority and define atomic compare-and-swap/version fencing, lease owner, monotonic claim generation, heartbeat cadence, stale-lease recovery, idempotency, cancellation and crash recovery. An accepted shared persistence or GitHub-backed claim protocol must be selected from the existing component inventory. Do not add Temporal, a new database, or a second scheduler simply to cover an unproven gap. If atomic claim authority is unavailable, permit only one active writer per lane and keep other work read-only.

The 23-lane manifest's UNKNOWN dependency order and lane ownership fields remain hard admission blockers for autonomous multi-lane execution. A task PR or workflow completion may provide evidence, but does not promote an entire domain.

## 8. Server-independent key custody versus network egress

Provider identity, credential custody, execution placement and network egress are separate dimensions:

- **No owned always-on server is required** when the selected hosted agent or GitHub-hosted runner can authenticate directly through its own provider integration or access an approved scoped secret.
- **A credential is not permanently bound to Mac mini 2018, Mac mini 2011 or the remote video server.** Store a secret reference at approved account/project/repository/environment scope and expose it only to the authorized job.
- **Every remote API request still has a network source.** The provider can observe the runner/service egress IP and evaluate region, account configuration, access eligibility and applicable terms. GitHub-hosted runner ranges vary; do not claim fixed source IP, location independence or absence of an egress point.
- Choose a provider-permitted execution region and record the real destination and egress class. Do not spoof location, hide source location or use routing to bypass provider controls.
- For services supporting GitHub OIDC/workload identity, use a narrowly trusted workflow/repository/ref/audience with short-lived credentials. For other services use the provider-supported OAuth/API-key mechanism, with one job-scoped secret, redaction and rotation. OIDC is not a universal replacement for provider API keys.
- Keep `permissions` minimum-scoped per job. A read-only agent has `contents: read`; any write token belongs in a downstream validated output/PR job, never in an untrusted model runtime.

This architecture removes a fixed dependency on an owner-operated server. It does not eliminate the service's network-origin or regional signals.

## 9. Routing, quotas and failover

1. Resolve provider/model only from the task's pre-authorized route list; reject caller-supplied endpoints and arbitrary base-URL overrides.
2. Check the provider admission record, data class, route policy, quota and deadline before transferring repository content.
3. Retry transient 5xx/network failures within a bounded budget. Honor the provider's retry instructions for rate limits.
4. Fail closed on authentication failure, policy denial, unknown endpoint, region/eligibility failure or data-class mismatch.
5. Use an alternate only if the exact provider, model, underlying router target, destination and data class were authorized before the first attempt. Every route attempt gets its own audit event.
6. Enforce an explicit zero-paid-fallback ceiling where free-only operation is required. A free quota label does not by itself prove privacy or eligibility.
7. When authorized routes are exhausted, persist a blocked/waiting task and resume after policy-valid authorization or quota replenishment. Do not loop indefinitely.

## 10. Worker isolation and patch promotion

- Pin the input commit and immutable versions of actions, CLIs, container images and schema assets.
- Place each task in an isolated workspace. Never run untrusted repository code with a repository-administration token or unrelated provider secrets.
- Reject path traversal, symlink escapes, unexpected generated files, binary/oversized output, forbidden workflow edits and changes outside the declared allowlist.
- Validate the patch independently from the agent: source SHA, changed-file set, schema, secret hygiene, dependency/license metadata, test evidence and artifact digest.
- Publish through a topic branch and pull request. Agent output remains a candidate until independent verification and review.
- Keep integration, qualification, release, deployment and product acceptance as separate governance stages.
- No agent may mutate MediaHub Product State Authority, amend Baseline 2.0, alter A0 issuer authority, self-approve a policy change, or promote its own qualification.

## 11. Evidence and observable operating states

Each run emits a sanitized evidence manifest with:

`task_id, agent_id, run_id, source_sha, policy_revision, admission_revision, provider_route_id, model_id, request_status, retry_count, changed_paths, artifact_digest, verification_id, review_ref, start/end time, final_state`.

Never include API keys, access tokens, raw secret-bearing URLs, private prompts outside approved retention, unredacted provider error bodies or credentials in logs.

Readiness states should be distinguishable: `REGISTERED`, `WAITING_AUTH`, `BLOCKED_POLICY`, `WAITING_QUOTA`, `READY`, `CLAIMED`, `RUNNING`, `VERIFY`, `FAILED_RETRYABLE`, `FAILED_FINAL`, `CANCELLED`, `CLOSED`. The external dashboard may project these states, but A0 remains the authoritative engineering queue owner; implement a versioned mapping rather than silently changing the 23-lane manifest schema.

## 12. Deployment-free rollout sequence

| Wave | Work | Exit evidence |
|---|---|---|
| W35 | Source-bound reference design and existing-component crosswalk | This design plus roadmap/matrix/map/checkpoint pointers |
| W36 | Reconcile accepted A0 issuer/ingress, R-06 data policy, MH-12 secrets, provider adapters and canonical target manifest | Exact primary-source crosswalk; authority and destination conflicts resolved |
| W37 | Select the existing durable claim authority; document cross-runner atomicity and lease/cancellation contract | Accepted revision-bound design and failure-state table |
| W38 | Versioned agent registry/task envelope/evidence schemas reusing existing schemas where possible | Collision-checked schemas and offline validation plan |
| W39 | Implement only required adapters/validators on a feature branch based on current `main` after architecture admission | Minimal diff, pinned dependencies/actions, code review |
| W40 | Run authorized offline/schema/unit tests and independent review | Test logs bound to exact commit and environment |
| W41 | Run a read-only hosted-runner workflow with synthetic context and no provider credentials | Run ID, source SHA, least-privilege proof, sanitized manifest, cancellation/recovery evidence |
| W42 | Authorize one specific provider/agent with limited non-sensitive task and explicit spend/data budget | Provider-specific auth/probe evidence plus independent review |
| W43 | Expand worker admission one lane at a time; verify path collision, quota, retry, cancellation and rollback | Lane-by-lane evidence at frozen SHA |
| W44 | Run integrated soak and independent qualification after all prerequisite gates pass | Fresh G0–G11 evidence at one frozen SHA; explicit owner acceptance |

Wave numbering is a planning index; preserve existing historic wave IDs and check collisions before creating future records.

## 13. Known blockers and dispositions

| Blocker | Evidence | Required disposition |
|---|---|---|
| No proven distributed claim authority across ephemeral runners | Current claim primitive is local file-backed; manifest has UNKNOWN lease/owner/dependency fields | BLOCK multi-writer hosted execution until durable atomic claim/fencing contract is accepted |
| Qualification is blocked | `CURRENT-TRUTH.generated.md` reports G0–G11 BLOCKED and overall NOT_PROVEN / BLOCKED | No production-readiness claims; fill gates with fresh revision-bound evidence |
| Provider secret exposure / destination override | Wave 30 source review identifies broad environment injection and configurable endpoint risks | Partition credentials by job/provider and implement allowlisted egress decision before provider execution |
| Queue/provider auth linkage | Wave 11 requires scoped references and owner authorization | Introduce a versioned non-secret registry and auth-evidence contract |
| Main/docs branches diverged | Current compare: 1,944 ahead / 12 behind, merge base `f0f406feb9f9816b009f4e6e756813541e53b9bc` | Keep docs work isolated; feature implementation must be based on current main through a separately reviewed integration path |
| Existing workflows include powerful self-hosted paths | ASTRA supervisor schedule and chat-control permissions are broader than read-only audit; qualification secrets are broadly injected per Wave 30 | Reconcile A0/R-06/MH-12 before reusing these execution paths for cloud agents |

## 14. External primary-source anchors reviewed

- GitHub Actions OpenID Connect: https://docs.github.com/en/actions/concepts/security/openid-connect
- GitHub workflow dispatch endpoint and permission requirements: https://docs.github.com/en/rest/actions/workflows#create-a-workflow-dispatch-event
- GitHub-hosted runner network/IP guidance: https://docs.github.com/en/actions/reference/runners/github-hosted-runners
- GitHub Agentic Workflows guardrails: https://docs.github.com/en/copilot/concepts/agent-capabilities/agent-powered-workflows-and-operations/about-github-agentic-workflows
- Jules GitHub integration and VM task lifecycle as a market reference: https://jules.google/docs/

These sources describe capability patterns; they do not qualify any MediaHub provider/account, authorize a service, establish current quota for a specific project, or prove a runtime is enabled. Revalidate all external service terms, eligibility and API behavior immediately before admitting a specific provider.

## 15. Acceptance boundaries

This wave changes the documented reference architecture and proposed rollout order only.

- No runtime code, workflow, secret, credential, provider route, endpoint or agent configuration was changed.
- No model/provider was invoked and no account credentials were accessed.
- No test or qualification was executed in this pass.
- No host/runtime, infrastructure or deployment was inspected or changed.
- No branch was merged, rebased or cherry-picked.
- Status remains **PROPOSED / NOT IMPLEMENTED BY THIS WAVE / RUNTIME UNVERIFIED / QUALIFICATION BLOCKED**.
