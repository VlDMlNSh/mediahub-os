# MediaHub OS — Three-Server and Cloud-Agent Key Enrollment / Chat Continuity, Wave 11

- Date: 2026-10-16
- Status: OWNER DIRECTION RECORDED / DESIGN PROPOSED / DOCUMENTATION COMMITTED / RUNTIME UNVERIFIED
- Contour: A — autonomous development fabric
- Repository: `VlDMlNSh/mediahub-os`
- Documentation ref: `docs/mediahub-chat-tree-map-20261012`
- Parent: [Cloud-Agent Fabric Reference Architecture — Wave 08](MEDIAHUB-AUTONOMOUS-CLOUD-AGENT-FABRIC-REFERENCE-ARCHITECTURE-WAVE-08-2026-10-16.md)
- Operational evidence: [Gemini Run Evidence — Wave 10](MEDIAHUB-CLOUD-AGENT-FABRIC-GEMINI-OPERATIONAL-EVIDENCE-WAVE-10-2026-10-16.md)

## 1. Owner direction captured from the current chat

The owner confirms the existing three-server design remains in force and requests a cloud-agent development fabric alongside it. The current chat's project-relevant direction is consolidated here for cross-chat continuity:

1. Keep the selected three-server topology: **Mac mini 2018 running macOS; Mac mini 2011 running Linux; remote video server**.
2. Add cloud agents as a complementary execution lane; preserve the three-server design and existing authority boundaries.
3. Provider API-key enrollment should be managed as provider/account/project credentials and authorized secret references, rather than a credential permanently attached to one of the three hosts.
4. As agents become authorized, admit them through a governed registry and place eligible work into a durable, auditable development queue.
5. Keep the unified architecture, unified verifiable contract, and unified traceability matrix as parallel workstreams.
6. Preserve Gemini's proven historical workflow execution evidence from run `38952885501`; do not characterize the integration as wholly unverified.
7. The owner states that their Google account and age eligibility are already established. This statement is recorded as owner-provided context; the historical run is separate direct evidence that the workflow's Gemini API step succeeded.
8. No credentials, secret values, account identifiers, personal data, or private key material are recorded in this document.

This is a project-relevant continuity summary, not a verbatim export of every chat message.

## 2. Topology invariant

The cloud-agent fabric extends the existing topology; it does not replace it.

| Execution lane | Intended role | Binding rule | Status |
|---|---|---|---|
| Mac mini 2018 / macOS | Existing local development/control role, subject to its accepted host contract | Exact workloads and authority follow the existing target manifest and A0 contracts | Existing selected topology; current runtime status requires target evidence |
| Mac mini 2011 / Linux | Existing legacy/Linux server role | Preserve compatibility and workload boundaries; admit tasks only after capability and security qualification | Existing selected topology; workload eligibility remains target-gated |
| Remote video server | Existing remote media/video role | Keep media workload and network authority separate from developer-agent credentials | Existing selected topology; exact endpoint and current qualification remain target-gated |
| GitHub-hosted ephemeral runners | Cloud CI / bounded read-only agent execution where the workflow permits | Short-lived jobs, least privilege, immutable source identity, minimal context, bounded artifacts | Candidate execution lane; workflow-specific controls apply |
| Additional cloud agents | Read-only analysis first; patch-producing agents only after separate qualification | Explicit identity, task envelope, capability scope, evidence output, isolated branch/PR and revocation | Proposed; agent-specific authorization required |

No host role, network route, deployment topology or canonical product-state authority is changed by this document.

## 3. Provider key enrollment is distinct from request egress

The desired design separates four concepts:

- **Provider identity:** account/project and model/service entitlement held with the provider.
- **Credential custody:** secret reference held by an approved secret store, such as a repository/environment secret for a bounded GitHub Actions workflow, or an approved secret manager for a server-side workload.
- **Execution placement:** the runner or host that performs a request for a particular task.
- **Network egress and provider eligibility:** the actual request origin, IP/region signals, account/project settings and provider policy that the provider evaluates.

The credential should be selected by a policy-controlled secret reference, not hard-wired to one of the three servers. A cloud runner can use a repository/environment-scoped secret without routing the key through a user-owned always-on server. A local/server workload can use its own approved secret delivery mechanism when that workload is authorized.

**Important technical boundary:** this removes an architectural dependency on one particular server; it does not make provider requests location-blind. The provider can evaluate the actual request's network origin, account region, project configuration, eligibility and applicable terms. Do not spoof or conceal location signals or use routing to bypass provider restrictions. Select a permitted execution location, and record the chosen provider/route in the task authorization and evidence manifest.

For Gemini, the successful historical run proves the API step worked in that run. It does not by itself prove current quota, repeatability, every execution location, or eligibility of a different account/project. No new provider call was made in this pass.

## 4. Credential handling contract

1. Store credential values only in an approved secret store; documents, prompts, task payloads, artifacts and logs contain references or redacted metadata only.
2. Scope each secret to one provider/project and the smallest applicable repository, environment, workflow or service principal.
3. Grant a worker access only for the authorized job; prefer short-lived federation where the provider and workflow support it.
4. Separate read-only audit credentials from patch-worker credentials. A read-only agent must have no write token.
5. Resolve provider and model identity from an allowlist. A task may select only routes already authorized by policy.
6. Treat quota fallback as a new provider destination requiring prior task authorization; fallback never silently expands egress or spending.
7. Record secret reference ID, version/fingerprint where safe, provider, model, task, run ID and policy revision; never record the secret value or reusable token.
8. Rotate and revoke through the owning provider/secret store. Revocation invalidates future admission and cancels queued tasks that require the revoked credential.
9. A worker with an unavailable credential enters `BLOCKED_AUTH`; it waits for owner-controlled authorization rather than requesting or fabricating a credential.
10. Credential registration itself does not authorize a provider call, a data class, a repository write, a merge or a deployment.

## 5. Agent admission and autonomous queue

Each agent registration record should contain:

- Stable `agent_id`, implementation/version, owner and authorization record.
- Provider/service identity and permitted model IDs, if applicable.
- Capability set: `read_audit`, `propose_patch`, `create_branch`, `open_pr`, `run_approved_checks`, and other separately granted capabilities.
- Allowed repositories, refs, paths, data classifications, egress destinations and secret references.
- Maximum concurrency, time budget, token/cost ceiling where available, retry ceiling and cancellation behavior.
- Output contract: changed-file list, source SHA, diff, evidence manifest, check results, known limitations and disposition.
- Admission status: `PENDING_AUTH`, `AUTHORIZED`, `ACTIVE`, `SUSPENDED`, `REVOKED`, `BLOCKED_POLICY`.
- Revision-bound qualification and last independent review.

Queue state is separate from agent state. Recommended task lifecycle:

`DRAFT → READY → CLAIMED → RUNNING → EVIDENCE_PENDING → REVIEW_REQUIRED → ACCEPTED`

Terminal or exceptional states:

`BLOCKED_AUTH`, `BLOCKED_POLICY`, `CANCELLED`, `FAILED_RETRYABLE`, `FAILED_FINAL`, `EXPIRED`, `REJECTED`.

Every task carries a stable task ID, idempotency key, target repository/ref/commit SHA, scope and exclusions, task/data classification, authorized agent class, provider route if any, deadline, cancellation token, expected evidence and promotion policy. Queue claims require lease/fencing semantics to prevent duplicate workers from committing conflicting results. Model output alone never transitions a task to accepted.

## 6. Initial queue — planning records only

| Queue ID | Priority | Work item | Eligible worker class | Exit evidence |
|---|---|---|---|---|
| CAF-Q-001 | P0 | Reconcile ASTRA A0 issuer, admission, lease, cancellation and recovery | Read-only source auditor | Source-bound authority/lifecycle crosswalk; open decisions explicit |
| CAF-Q-002 | P0 | Close R-06 audit/privacy authority, retention and outage behavior | Read-only policy auditor | Accepted policy and audit evidence contract |
| CAF-Q-003 | P0 | Prepare exact patch plan for Gemini workflow provenance, path allowlist, action pinning and output quarantine | Read-only workflow auditor | File/line/SHA-bound proposed diff and acceptance criteria |
| CAF-Q-004 | P0 | Define task-envelope and agent-registry schemas with historical-ID collision check | Contract/schema analyst | Versioned candidate schema and collision evidence |
| CAF-Q-005 | P1 | Define provenance manifest for run, commit, input digests, model/provider, policy and artifact | Evidence-contract analyst | Manifest schema and integrity rules |
| CAF-Q-006 | P1 | Define provider credential references and egress authorization matrix | Security/privacy analyst | Provider × data class × route × execution lane decision table |
| CAF-Q-007 | P1 | Locate authoritative target manifest for all three servers and hosted runners | Read-only inventory auditor | Exact source paths/SHAs and capability gaps |
| CAF-Q-008 | P1 | Define PR-first promotion, review and repository protection evidence | Governance auditor | Source-backed promotion contract |
| CAF-Q-009 | P1 | Build free/cloud-agent capability and terms inventory | Component researcher | Official-source comparison; eligibility, privacy and quota facts |
| CAF-Q-010 | P2 | Create onboarding packet and operator runbook for future agent authorization | Documentation agent | Reviewed runbook with secret-free setup and revocation paths |

These rows are a documented backlog, not live queued jobs or dispatched agents. The queue becomes operational only when its accepted A0/queue implementation and authorized execution path exist.

## 7. Promotion ladder

- **L0 — Inventory:** public documentation and repository source reading; no credentials or external model calls.
- **L1 — Read-only audit:** bounded context, contents-read permission, immutable source SHA, sanitized output, provenance manifest.
- **L2 — Patch proposal:** isolated worktree/branch, explicit path allowlist, no direct default-branch writes; output is a proposed diff.
- **L3 — PR worker:** open a pull request only under an explicitly authorized GitHub identity and policy.
- **L4 — Approved checks:** execute only the checks explicitly authorized for that task and target.
- **L5 — Human/governance acceptance:** independent source/evidence review and required approvals.
- **L6 — Release/deployment:** separate authorization and target qualification; never implied by L0–L5.

Promotion between levels requires evidence and explicit capability grants. Successful provider connectivity only qualifies the relevant call path, not the entire worker.

## 8. Privacy, security and failure controls

- Default-deny egress; minimize context to the task's allowlisted files and data classification.
- Avoid secrets, personal data, private media and production state in prompts unless an approved policy explicitly permits a specific transfer.
- Use immutable source SHA, path/file digests, action full-SHA pins and output digest in each evidence manifest.
- Treat repository text and model output as untrusted; prevent prompt-injection text from changing tool permissions or task scope.
- Enforce per-agent least privilege, isolated execution, bounded concurrency, timeouts, cancellation and revocation.
- Keep provider outages and quota exhaustion visible. Retry only bounded transient failures; use only pre-authorized fallback routes.
- Preserve the MediaHub Product State Authority and ASTRA A0 boundaries; agents remain engineering actors, not canonical product-state authorities.
- Retain audit evidence according to accepted R-06 policy; when the audit sink is unavailable, fail closed for privileged work.

## 9. Current evidence and limits

- Historical Gemini run: [38952885501](https://github.com/VlDMlNSh/mediahub-os/actions/runs/38952885501), source commit `b45324009ac3aa65322a702c28069b12190bc4b8`, job `117148417231`, artifact `12069128185`, digest `sha256:a31c7a5036f003e6918c4c6a3ab0ad7f82c8c6c5fb10afde77f8a39d0d8b4d7d`.
- Gemini is operationally proven for at least that historical read-only workflow run.
- The general-purpose durable queue, agent registry, scheduler, isolated patch worker, task manifest, A0 integration, R-06 audit sink and promotion pipeline remain unqualified until direct evidence is available.
- This wave records design and owner direction only. No credentials were read, added or transmitted; no new provider call or workflow dispatch occurred; no tests, scanners, installations, host/runtime inspection, infrastructure change, deployment or branch integration occurred.

## 10. Next step

1. Reconcile this wave with the current A0 issuer/lifecycle and R-06 primary artifacts.
2. Convert CAF-Q-003 and CAF-Q-004 into exact source-bound patch/schema proposals.
3. Resolve the canonical target manifest for the three existing servers and hosted runners.
4. Establish a secret-free agent onboarding record and authorization lifecycle.
5. Implement and test only after separate explicit authorization; keep test, qualification, deployment and acceptance evidence distinct.

Project map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
