# MediaHub OS — Unified Security Control Matrix and Verifiable Workflow Contract, Wave 05

- Date: 2026-10-16
- Repository: `VlDMlNSh/mediahub-os`
- Documentation ref: `docs/mediahub-chat-tree-map-20261012`
- Source review ref: `main`
- Status: **PROPOSED / SOURCE-ANCHORED / NOT ACCEPTED / NOT FROZEN**
- Scope: GitHub-driven ASTRA control plane, privileged workflow execution, provider-secret transfer, HMAC authority, evidence provenance, and change/verification gates.
- Parent references:
  - [Astra Workflow Authority Review — Wave 04](MEDIAHUB-ASTRA-WORKFLOW-AUTHORITY-REVIEW-WAVE-04-2026-10-16.md)
  - [Unified System Traceability Matrix v0.1](mediahub-unified-system-traceability-matrix-v0.1.md)
  - [Unified Architecture and Deployment Contract v0.1](mediahub-unified-architecture-and-deployment-contract-v0.1.md)
  - [Canonical Source Registry and Security Evidence Ledger — Wave 03](MEDIAHUB-CANONICAL-SOURCE-REGISTRY-AND-SECURITY-EVIDENCE-LEDGER-WAVE-03-2026-10-16.md)
  - [Project map](../architecture/MEDIAHUB-CHAT-TREE-MAP.md)
- Authority boundary: this document composes a proposed, checkable control contract. It does not amend accepted Functional Baseline 2.0, appoint a security authority, grant workflow permissions, authorize source edits, or constitute implementation, test, qualification, release, deployment, or production acceptance.

## 1. Decision summary

Wave 04 established ten source-level findings across the ASTRA control and qualification workflow family. Wave 05 turns those findings into one traceable matrix and a verification contract with explicit preconditions, observable evidence, pass/fail semantics, and closure ownership.

Recommended remediation order:

1. **P0 — approved-ref fence:** bind workflow definition, executable source, and target SHA to one approved immutable default-branch commit before privileged jobs or secrets.
2. **P0 — actor/capability authorization:** replace broad association-only control with explicit actor, operation, target, freshness, and replay/idempotency checks.
3. **P0 — provider secret minimization:** replace `secrets: inherit` with an explicit allowlist and separate provider credentials by job/environment.
4. **P1 — least privilege and credential lifetime:** scope token permissions per job, justify every write capability, and remove persisted checkout credentials where feasible.
5. **P1 — HMAC isolation:** keep node-specific signing keys inside the smallest possible execution step and avoid passing signing keys to aggregate jobs.
6. **P1 — target/executor consistency:** validate the accepted target registry once and preserve the same canonical values from request parsing through dispatch and execution.
7. **P2 — immutable action provenance and schedule guardrails:** pin third-party actions to full commit SHAs and document schedule authority, cost ceilings, and stop conditions.

The severity labels in Wave 04 are review priorities based on static source structure. They are not a finding of exploitation or a confirmed vulnerability in the live environment. Dispatch-ref behavior, repository permissions, branch protection, and runner isolation require separate authoritative evidence.

## 2. Normative boundary and status vocabulary

This contract is a candidate for governance review. Until explicit acceptance, it is a review checklist rather than an active policy.

| Status | Meaning |
|---|---|
| SOURCE-CONFIRMED | A property is visible in a retrieved, SHA-identified source file. |
| PROPOSED CONTROL | A recommended future control; implementation is unverified. |
| EVIDENCE PENDING | A required authoritative artifact has not been supplied or retrieved. |
| PASS | A defined check ran against the exact revision and target, and its result artifact is linked. |
| FAIL | A required invariant was violated by the tested revision or evidence. |
| BLOCKED | A precondition or authorization gate is missing; no pass inference is allowed. |
| ACCEPTED | An authorized governance decision identifies the accepted revision and scope. |

A PASS applies only to its named gate, commit, workflow, target profile, and evidence set. It never automatically promotes another gate or the complete system.

## 3. Source register and revision anchors

The following are the source blobs reviewed by Wave 04 on `main`; these hashes identify file contents, not a claim that the docs branch and main are integrated.

| Source ID | Path on `main` | Blob SHA | Contract relevance |
|---|---|---|---|
| SRC-01 | `.github/workflows/astra-chat-control.yml` | `51b17ec2410032772f9baa1de4afedb6b000f3c4` | Comment ingress, issuer check, token permissions, target/executor parser |
| SRC-02 | `.github/workflows/astra-autonomous-supervisor.yml` | `a0209a2d01122354d19e95d2f362a6ecfa3d6186` | Trigger/ref policy, HMAC signing, reusable-workflow dispatch, privileged supervisor |
| SRC-03 | `.github/workflows/astra-distributed-verification.yml` | `648f56badd2b919b822b4fe4b61f285cca99ed93` | Node jobs and aggregate key distribution |
| SRC-04 | `.github/workflows/astra-provider-qualification.yml` | `d3160088fbef4fce152ed7335f0acaa3bb440378` | Provider credential environment and checkout credential handling |
| SRC-05 | `.github/workflows/astra-local-claude-qualification.yml` | `7f7dc2d65481e2cc80a1db94b41a1e60ed117ffd` | Reusable local-qualification boundary |
| SRC-06 | `astra_github_agent.py` | `dd2f373bf5f3d69dec951c84e3d53b0e9befab0c` | HMAC verification, freshness checks, Git fetch/publication paths |
| SRC-07 | `ops/control/sign_command.py` | `fc6943a79cefdf06e59d6e32771d2df551b2f0e9` | Node-specific command signing |
| SRC-08 | `docs/checkpoints/MEDIAHUB-ASTRA-WORKFLOW-AUTHORITY-REVIEW-WAVE-04-2026-10-16.md` on docs ref | `2d3ad89a6cd485f74463c9d87edf234758a4997c` | Findings, line anchors, confidence boundaries |

Live source anchors from Wave 04:
- Chat-control trigger and permission context: [lines 7–31](https://github.com/VlDMlNSh/mediahub-os/blob/main/.github/workflows/astra-chat-control.yml#L7-L31)
- Chat-control parsing and execution: [lines 33–48](https://github.com/VlDMlNSh/mediahub-os/blob/main/.github/workflows/astra-chat-control.yml#L33-L48), [lines 60–123](https://github.com/VlDMlNSh/mediahub-os/blob/main/.github/workflows/astra-chat-control.yml#L60-L123)
- Supervisor triggers and permissions: [lines 5–37](https://github.com/VlDMlNSh/mediahub-os/blob/main/.github/workflows/astra-autonomous-supervisor.yml#L5-L37)
- Supervisor signing and dispatch: [lines 39–119](https://github.com/VlDMlNSh/mediahub-os/blob/main/.github/workflows/astra-autonomous-supervisor.yml#L39-L119)
- Supervisor privileged job and credential persistence: [lines 121–222](https://github.com/VlDMlNSh/mediahub-os/blob/main/.github/workflows/astra-autonomous-supervisor.yml#L121-L222)
- Provider credential mapping: [lines 30–76](https://github.com/VlDMlNSh/mediahub-os/blob/main/.github/workflows/astra-provider-qualification.yml#L30-L76)

## 4. Unified requirement-to-control-to-evidence matrix

| Requirement ID | Risk / source finding | Required control contract | Minimum verification evidence | Closure rule / priority |
|---|---|---|---|---|
| SEC-WF-01 | Ref substitution before privileged execution; ASTRA-04-01, -10; SRC-02 | Every privileged job must fail closed unless workflow ref is the approved default branch. Resolve one immutable approved commit SHA; verify workflow definition and executable source use that SHA before secrets, signing keys, or self-hosted runners are reached. Manual dispatch must be disabled or explicitly fenced. | Commit-bound workflow diff; dispatch-ref policy evidence; exact run ID and event ref; resolved SHA; proof each privileged job uses the same SHA; negative cases for non-approved refs. | **P0.** PASS only when both static contract and authorized runtime evidence agree. |
| SEC-WF-02 | Coarse issuer check; ASTRA-04-02; SRC-01 | Authorization must bind authenticated actor ID, allowed capability, operation, target, request digest, issuance time, expiry, unique request/nonce, and approval requirement for high-impact operations. Association labels alone are insufficient. | Policy/allowlist revision; test vectors for permitted and denied actors/operations; expired, replayed, altered-target and duplicate-request rejection records. | **P0.** Any missing actor/capability binding or replay defense = FAIL. |
| SEC-WF-03 | Workflow-wide write scope; ASTRA-04-03; SRC-01/SRC-02 | Declare `permissions: {}` at workflow scope where supported; grant only explicitly required permissions at job scope. Each write permission must map to a named API operation and requirement. Remove unused scopes. | Permission-to-operation table; source diff; GitHub permission semantics review; run evidence demonstrating unrelated write APIs are unavailable. | **P0/P1.** Each permission needs documented necessity; unsupported necessity = BLOCKED pending reduction. |
| SEC-WF-04 | Broad provider secret inheritance; ASTRA-04-04; SRC-02/SRC-04 | Replace `secrets: inherit` with explicit per-secret mapping. Partition credentials by provider and job/environment; expose each secret only to the step that needs it where practical. No secret-bearing job may run from an unapproved ref. | Allowlist inventory; caller/callee mapping; secret-to-step matrix; source review; authorized negative test showing unrelated provider secrets are absent. Secret values must never appear in evidence. | **P0.** Any unlisted inherited secret = FAIL. |
| SEC-WF-05 | Node HMAC key concentration; ASTRA-04-05; SRC-02/SRC-03 | A node signing key may be available only to the authorized signing step. Node jobs receive only their own key. Aggregate jobs should receive public verification material or signed result evidence, not all node signing keys, unless a documented cryptographic need is accepted. | Key-flow diagram; workflow expression/secret map; per-job secret inventory; tests for cross-node key absence; rotation/revocation procedure. | **P1.** Cross-node signing authority without accepted justification = FAIL. |
| SEC-WF-06 | Persisted checkout credential; ASTRA-04-06; SRC-02/SRC-04/SRC-05 | Use `persist-credentials: false` unless a specific later step requires authenticated Git. If required, use a short-lived, narrowly scoped credential and remove it after use. | Checkout configuration; operation inventory; credential lifetime evidence; log scan with values redacted; negative check for unintended push/API authority. | **P1.** Unjustified persistence = FAIL. |
| SEC-WF-07 | Parser/executor target mismatch; ASTRA-04-07; SRC-01 | Parse into a typed canonical request. Validate node and executor against an accepted target/capability registry. Dispatch and execution must consume the same validated values; reject unknown aliases before any side effect. | Accepted registry revision; parser schema; mapping table; valid/invalid combination test results; exact requested vs executed target evidence. | **P1.** Any silent remapping or accepted-but-unexecutable combination = FAIL. |
| SEC-WF-08 | Recurring side-effect/cost surface; ASTRA-04-08; SRC-02 | Every schedule must have a documented purpose, maximum frequency, concurrency policy, budget/side-effect ceiling, cancellation path, and stop condition. Prefer read-only work on recurring triggers; privileged actions require explicit policy gates. | Trigger inventory; schedule owner/purpose; concurrency/cancellation config; cost and side-effect limits; run history reviewed by an authorized owner. | **P2.** Unknown owner, cost ceiling, or stop control = BLOCKED for autonomous privileged use. |
| SEC-WF-09 | Mutable third-party action tags; ASTRA-04-09; SRC-01/SRC-02 | Pin each third-party action to a full commit SHA. Record upstream version, SHA, source/release provenance, update owner, and review procedure. | Action inventory; exact full SHAs; upstream release mapping; diff and review evidence for each update. | **P2.** Major tag alone = FAIL for the accepted hardened profile. |
| SEC-WF-10 | Target SHA checks do not establish actor/ref provenance; ASTRA-04-10; SRC-01/SRC-02/SRC-06/SRC-07 | Treat actor authorization, event/ref authorization, command integrity, target immutability, and target admission as separate predicates. All must pass before execution. A matching SHA alone cannot grant authority. | Decision table for all predicates; signed request record; source SHA; target registry version; denial evidence when any predicate fails. | **P0.** Missing any independent predicate = FAIL. |
| SEC-WF-11 | Evidence can be detached from exact source; Wave 03 EVD-011/EVD-012/EVD-015 | Every security result must identify source commit SHA, workflow file SHA, run ID, event/ref, target profile, artifact digest, tool/config version, timestamp, and verifier. Mark caller-provided context as untrusted and advisory until validated. | Machine-readable evidence record; artifact digest verification; run URL; reviewer identity/role; freshness window; source-to-artifact linkage. | **P1.** Missing revision/run/digest linkage = EVIDENCE PENDING. |
| SEC-WF-12 | Unknown branch protection/security-alert state; Wave 03 EVD-001/EVD-015 | Repository governance state must be evidenced from an authoritative settings/API view. Unknown is preserved as UNKNOWN; no clean-security claim is permitted from absent API data. | Dated branch protection/ruleset export for each relevant branch; required-check list; Security-tab/alert evidence or explicit API capability limitation. | **P0 gate before trusted automation;** otherwise BLOCKED. |
| SEC-WF-13 | Source findings may be over-read as confirmed exploitability | Separate static source observation, exploitability analysis, authorized runtime validation, and accepted risk disposition. No claim of exploitation without direct evidence. | Finding record with source anchors, assumptions, confidence, environment evidence, risk owner and disposition. | Mandatory evidence quality rule across all findings. |
| SEC-WF-14 | Rollback or partial remediation can leave inconsistent authority paths | Remediate in small isolated commits; keep a rollback patch or exact revert instructions; verify caller/callee compatibility and preserve audit artifacts. Do not merge divergent branches as part of remediation. | Before/after source hashes; change inventory; rollback diff/instructions; dependency review; independent read-back. | Mandatory change-control gate for each source-edit slice. |

## 5. Verifiable contract

### 5.1 Preconditions

Before a privileged workflow is eligible to run, all conditions below must hold:

1. **Revision:** the workflow definition and executable inputs are bound to an immutable commit approved for the intended branch.
2. **Identity:** the triggering actor is authenticated and explicitly authorized for the requested capability.
3. **Request:** the command is schema-valid, fresh, uniquely identified, replay-resistant, and bound to the intended operation and target.
4. **Target:** target identity and executor are present in the accepted registry and match the validated request end to end.
5. **Policy:** all required policy checks and independent approvals have passed.
6. **Permissions:** the job token and credentials expose only capabilities required for that job.
7. **Secrets:** secret mapping is explicit, provider-scoped, ref-fenced, and absent from jobs that do not require it.
8. **Evidence:** the run can emit revision-bound evidence without revealing secret values.
9. **Stop controls:** cancellation, timeout, concurrency, and failure behavior are specified before side effects.
10. **Governance:** the remediation revision has the required review/acceptance and separate execution authorization.

If any precondition is missing or unresolved, the expected behavior is **BLOCKED / FAIL CLOSED** before side effects.

### 5.2 Execution invariants

- One request maps to one canonical request ID and one immutable target SHA.
- Authorization checks happen before dispatch, secret exposure, signing, or self-hosted execution.
- Each privileged job independently enforces approved-ref and target constraints; a caller check alone is insufficient.
- Provider jobs receive an explicit secret allowlist, never an implicit inherited secret set.
- Node signing authority is isolated by node and step; verification authority is separated from signing authority.
- A denied, expired, duplicate, replayed, altered, or unrecognized request produces a denial record and no privileged side effect.
- Missing evidence is represented as UNKNOWN / EVIDENCE PENDING, never as PASS.
- A successful child workflow does not imply system-wide qualification or production acceptance.

### 5.3 Required evidence envelope

Each gate result must contain the following fields, with secret values excluded:

| Field | Required semantics |
|---|---|
| `contract_id` / `contract_revision` | Exact contract revision under evaluation |
| `requirement_id` / `gate_id` | Stable requirement and verification gate |
| `source_commit_sha` | Immutable source revision |
| `workflow_path` / `workflow_blob_sha` | Exact workflow identity |
| `event_name` / `event_ref` / `actor_id` | Trigger provenance |
| `request_id` / `request_digest` | Unique command identity and content binding |
| `target_id` / `target_sha` / `executor_id` | Canonical execution target |
| `permission_profile` / `secret_profile_id` | Names/versions of capability profiles; no values |
| `run_id` / `run_url` | Authoritative workflow execution reference |
| `artifact_digest` / `artifact_uri` | Evidence integrity and retrieval pointer |
| `tool_versions` / `policy_revision` | Verification environment and rules |
| `started_at` / `completed_at` | Time bounds and freshness assessment |
| `result` / `failure_codes` | PASS, FAIL, BLOCKED, or EVIDENCE PENDING with reason |
| `reviewer_id` / `review_role` | Independent review identity and authority |
| `limitations` | Explicit coverage gaps and assumptions |

### 5.4 Acceptance gates

| Gate | Acceptance criterion | Evidence required | Current status |
|---|---|---|---|
| GATE-WF-01 Ref and immutable target | All privileged paths fail closed outside the approved ref and use the same resolved SHA | Source diff, dispatch policy, authorized negative/positive run records | BLOCKED — proposed only |
| GATE-WF-02 Actor/capability/replay | Explicit actor-capability matrix and replay/expiry rejection verified | Policy revision and commit-bound test artifacts | BLOCKED — proposed only |
| GATE-WF-03 Secret minimization | Explicit provider allowlist and per-job exposure verified | Caller/callee mapping, source diff, redacted verification artifact | BLOCKED — proposed only |
| GATE-WF-04 Least privilege | Every permission maps to an operation; unused writes removed | Permission matrix and revision-bound review | EVIDENCE PENDING |
| GATE-WF-05 HMAC isolation | No node signing key is exposed outside its required scope | Key-flow review and negative test artifacts | EVIDENCE PENDING |
| GATE-WF-06 Target consistency | Request, dispatch, execution, and evidence use the same admitted target/executor | Registry, test vectors, run records | EVIDENCE PENDING |
| GATE-WF-07 Provenance | Every result is bound to commit, run, target and artifact digest | Evidence-envelope samples and digest validation | EVIDENCE PENDING |
| GATE-WF-08 Governance settings | Branch rules, required checks, and security-alert state are evidenced | Authoritative settings export or explicit access limitation | UNKNOWN |
| GATE-WF-09 Rollback readiness | Each change has a reviewed revert path and compatibility assessment | Patch/revert record and read-back | BLOCKED until a patch exists |
| GATE-WF-10 Independent acceptance | Authorized reviewer accepts exact contract/source revision and limitations | Signed/recorded decision referencing SHAs and open risks | NOT STARTED |

### 5.5 Failure semantics

- **FAIL CLOSED:** any missing identity, authorization, ref, target, policy, or secret-scope predicate prevents privileged execution.
- **BLOCKED:** required authorization, evidence, or governance decision is absent; the next action is to acquire that gate, not to infer approval.
- **UNKNOWN:** authoritative evidence is unavailable. This status cannot satisfy a required gate.
- **PASS:** only for the exact gate and revision with retained evidence.
- **ROLLBACK:** stop further privileged runs, restore the last accepted source revision through an authorized change, preserve run/artifact evidence, and repeat the applicable verification gates. Rollback itself requires separate authorization where it changes repository state.

## 6. Implementation and verification sequence

| Step | Work package | Allowed scope in this pass | Exit artifact |
|---|---|---|---|
| W5-A | Contract/matrix composition | Documentation and source-backed traceability | This document |
| W5-B | P0 patch design | Proposed diff descriptions and threat/control mapping only | Separate patch plan with exact line targets and rollback notes |
| W5-C | Source edits | Requires explicit authorization under project rules | Revision-bound source diff |
| W5-D | Static validation and test design | Define checks and expected outcomes; execution requires separate authorization | Verification plan and test vectors |
| W5-E | Authorized execution | Only after explicit permission for workflow dispatch/tests/credentials as applicable | Run IDs, exact SHAs, artifacts and logs |
| W5-F | Independent acceptance | Reviewer distinct from implementer where required | Recorded acceptance decision |

Recommended patch order for a future authorized pass: (1) approved-ref fence, (2) explicit provider-secret allowlist, (3) job-level permissions, (4) actor/capability/replay binding, (5) target/executor consistency, (6) HMAC isolation, (7) credential persistence, (8) action SHA pins and schedule guardrails.

## 7. Change control and rollback

Every source-edit slice must identify:
- exact files and source blob SHAs;
- threat/finding IDs addressed;
- expected permission and data-flow changes;
- compatibility impact on caller/reusable workflows;
- positive and negative verification cases;
- rollback commit or exact revert instructions;
- evidence retention and secret-redaction rules;
- reviewer and authorization reference.

Apply one bounded remediation slice per change set. Read back all changed files from GitHub and verify the resulting blob SHAs. If any downstream caller/callee contract changes, review all callers before acceptance. Preserve the current workflow files and divergent branches until separately authorized source edits and branch disposition are approved. Do not merge, rebase, cherry-pick, dispatch workflows, invoke providers, access secrets, or inspect runners as part of this documentation-only pass.

## 8. Known evidence gaps and limitations

1. Branch protection/ruleset and security-alert state remain UNKNOWN where authoritative integration evidence is unavailable.
2. Manual-dispatch exploitability depends on actual repository permissions and GitHub dispatch-ref policy; source review alone does not establish exploitability.
3. Self-hosted runner isolation, filesystem/credential persistence, provider account scopes, and runtime behavior were outside this pass.
4. No YAML parser, tests, scanners, workflow dispatch, provider/model calls, credentials, runner/host inspection, or infrastructure actions were performed.
5. No workflow source was changed. No security qualification, deployment readiness, or production acceptance is claimed.
6. This contract is PROPOSED. It becomes normative only after an explicit governance decision references its exact blob SHA and scope.

## 9. Wave 05 conclusion

A single source-anchored control matrix and verifiable contract now connect the ten Wave 04 findings plus four cross-cutting evidence/change-control requirements to specific controls, revision-bound evidence, gate outcomes, and remediation ordering. This is a documentation deliverable and proposed review contract, not a completed remediation.

**Next step:** prepare the exact P0 source patch plan and rollback map, retaining the explicit execution authorization boundary.

Project map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
