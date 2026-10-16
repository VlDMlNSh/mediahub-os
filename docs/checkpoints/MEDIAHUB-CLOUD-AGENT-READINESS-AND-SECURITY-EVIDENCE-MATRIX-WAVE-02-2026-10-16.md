# MediaHub OS — Cloud Agent Readiness and Security Evidence Matrix, Wave 02
Date: 2026-10-16
Repository: https://github.com/VlDMlNSh/mediahub-os
Documentation ref: `docs/mediahub-chat-tree-map-20261012`
Status: DOCUMENTED DESIGN / PROPOSED / RUNTIME UNVERIFIED

## 1. Objective and boundary

This pass converts the Wave 01 runbook and Wave 02 static security review into one reviewable admission matrix for free/low-cost agents and one evidence ledger for safe enablement. This is documentation work only. No credentials, external providers, workflows, tests, scanners, installations, infrastructure or deployments were invoked.

The controlling architecture remains local-first and fail-closed: agents provide advisory analysis and evidence; they do not become Product State Authority, authorize canonical state mutation, or bypass Policy → Authorization → Consumer Boundary → State Authority.

## 2. Agent admission matrix

Status vocabulary:
- `SOURCE-CONFIRMED`: a repository artifact exists at a recorded ref/SHA.
- `CANDIDATE`: a possible route requiring current provider terms/quota verification.
- `BLOCKED`: a required capability or permission is unavailable in the current connector.
- `RUNTIME-UNVERIFIED`: no revision-bound successful execution evidence exists.

| Agent path | Intended use | Current evidence | Cost assumption | Admission decision | Required proof |
|---|---|---|---|---|---|
| Gemini through GitHub Actions | Read-only architecture review, bounded security triage | Two existing manual workflows on `main`; blobs `0d10efdda251f2ceca43175981c919102303572b` and `96fcc9ed4e45659d0118f0b9f3593a0c736200f0` | Provider quota and billing state must be checked in the Google AI account | FIRST CANDIDATE; RUNTIME-UNVERIFIED | Actions secret metadata, current model availability, one successful run, resolved SHA, artifact digest, redaction check |
| GitHub Actions deterministic jobs | Tree inventory, metadata checks, static policy checks and evidence formatting | Existing Actions infrastructure; main tree report recorded 32 workflows | Subject to repository plan and runner-minute limits | ADMIT ONLY PER JOB | Effective token permissions, action provenance, runner class, retention and run evidence |
| Local model adapter (for example, Ollama) | Local-only summarization or bounded code review | Architecture candidate only; no runtime qualification in this pass | No per-token hosted inference charge; host resource, power and model-license costs remain | CANDIDATE | Explicit install/runtime authorization, model digest/license, hardware capacity, network isolation and local evidence |
| Additional hosted model APIs | Optional second-provider fallback | No successful provider-specific integration evidence captured in this pass | Free quotas and model availability change by provider/account/region | DEFER | Official current terms, model ID, quota, retention/data-use policy, key scope, rate limits and outage behavior |
| Multi-provider router | Policy-based selection/fallback among qualified providers | No accepted router contract or provider matrix found in this pass | Could route to a paid model unless enforced | BLOCKED UNTIL COST GATE EXISTS | Explicit free-only allowlist, hard spend cap, provider denylist, no silent paid fallback, deterministic fallback tests and audit log |

Provider selection rule: prefer the already-present Gemini path for the first bounded live proof. Admit another provider only after current official terms, free-tier quota, model availability, data handling and authentication scope are documented. Do not treat a “free model” label as a guaranteed zero-cost contract.

## 3. Gemini workflow source review

### Positive controls confirmed by reading source

- Manual `workflow_dispatch` trigger.
- Job and workflow `contents: read` permission.
- Checkout uses `persist-credentials: false`.
- Context size cap, traversal-pattern rejection and workflow-file exclusion.
- API error bodies are suppressed from output.
- Retry workflow bounds attempts to four and uses retryable HTTP status classification.
- Uploaded result artifact has a 14-day retention period.

### Hardening requirements before treating output as trusted evidence

| ID | Gap / risk | Required design control | Verification evidence |
|---|---|---|---|
| AGENT-SEC-01 | Caller-supplied ref can select arbitrary repository history | Allowlist permitted refs or dispatch only against an immutable approved SHA | Input rejection cases and resolved commit recorded in summary |
| AGENT-SEC-02 | Caller-supplied context paths are only pattern-checked | Enforce a positive path allowlist; canonicalize paths; reject symlink escapes and duplicate paths | Negative-path matrix, canonical path manifest and file digests |
| AGENT-SEC-03 | Caller-supplied task is model prompt input | Bound task length; state output is untrusted; prohibit tool instructions, credential requests and mutation proposals as executable actions | Input-bound tests and prompt-policy review |
| AGENT-SEC-04 | `actions/checkout@v4` and `actions/upload-artifact@v4` use mutable major tags | Pin third-party actions to reviewed full commit SHAs with provenance records | Workflow source SHA and approved action-SHA register |
| AGENT-SEC-05 | Artifact currently contains model output without a declared integrity manifest | Record repository, workflow ref, resolved commit SHA, selected paths and SHA-256 digests, model ID, run ID, UTC time, HTTP status and redaction outcome | Artifact manifest and independently recomputed digest |
| AGENT-SEC-06 | Model output may contain incorrect or adversarial claims | Treat output as advisory; require source-linked reviewer verification before use in a decision | Review record with claim-to-source mapping |
| AGENT-SEC-07 | Secret availability/validity is unknown from this connector | Inspect secret metadata in GitHub UI; never reveal value; use one bounded dispatch | Run ID, status and redacted summary |
| AGENT-SEC-08 | Retryable service errors may consume quota repeatedly | Preserve bounded attempts; respect Retry-After where safe; avoid logging response bodies; add an explicit request/attempt budget | Sanitized run evidence and provider quota record |

These are design findings from source review, not claims that the workflow is exploitable. Implementation requires a separately authorized code-change pass.

## 4. Unified security evidence ledger

Use one row per control. Store references and hashes, never credential values.

| Control ID | Required evidence | Current status | Owner action |
|---|---|---|---|
| SEC-MAT-001 — repository secrets | Scanner/version/config, scanned refs/range, findings, suppression rationale and artifact digest | UNKNOWN; scanner execution absent | Obtain an authorized scanner path and preserve redacted output |
| SEC-MAT-002 — SAST | Tool/ruleset/version, scope, SARIF, triage and fixed commit | UNKNOWN | Choose CodeQL or Semgrep after workflow design review |
| SEC-MAT-003 — SCA/SBOM | Complete manifest inventory, lock resolution, SBOM and vulnerability snapshot | UNKNOWN | Inventory actual runtime/build manifests, then select compatible tooling |
| SEC-MAT-004 — workflow least privilege | Trigger graph, per-job permissions, action SHA pins, credential persistence and write destinations | PARTIAL STATIC REVIEW | Prioritize Astra comment controller and autonomous supervisor |
| SEC-MAT-005 — branch governance | Required reviews/checks, bypasses, force-push and deletion rules | UNKNOWN; connector returned 403 for branch-protection query | Capture owner-visible GitHub settings evidence |
| SEC-MAT-006 — secret alerts/push protection | Alert export, coverage state, push-protection evidence and dismissal rationale | UNKNOWN; alert endpoint inaccessible | Review GitHub Security settings |
| SEC-MAT-007 — controller integrity | Principal, command signature, expiry, nonce/idempotency, target binding and replay-negative evidence | STATIC REVIEW REQUIRED | Review issue-comment controller and supervisor as a pair |
| SEC-MAT-008 — target topology | Approved registry ref/SHA, target lifecycle, runner mapping and legacy-ID ledger | OPEN | Keep old node identifiers historical until approved inventory is established |
| SEC-MAT-009 — evidence provenance | Commit/blob SHA, run ID, tool/version, timestamp, scope, redaction and verifier | PARTIAL | Require a manifest for each future agent artifact |
| SEC-MAT-010 — independent acceptance | Independent verifier, reproducible evidence and acceptance authority | OPEN | Keep Contour A acceptance separate from Contour B product implementation |

## 5. Security priority and sequencing

1. Owner-visible evidence for branch governance and Security-tab alert coverage.
2. Static review of `astra-chat-control.yml` and `astra-autonomous-supervisor.yml` before any mutation path is enabled.
3. First bounded Gemini run through the existing retry workflow; capture source SHA and artifact digest.
4. Authorized implementation of scanner workflows with least-privilege permissions and full-SHA action pins.
5. Independent verification of secret hygiene, SAST, SCA/SBOM and applicable IaC/container coverage.
6. Only then evaluate a second hosted provider or a provider router with a strict free-only allowlist and a hard cost gate.

## 6. Current pass results

- Read the current bootstrap, map, Wave 01 runbook, Wave 02 security report and both Gemini workflow files.
- Recorded the candidate topology, source-backed Gemini controls, hardening gaps and security evidence ledger.
- No API keys or secret values accessed; no external model call; no workflow dispatch; no tests or scanners executed; no runtime or infrastructure action.
- Runtime success, security alert counts, secret inventory and provider quota remain UNKNOWN.
- This document is a design and traceability artifact, not implementation, qualification or acceptance.

## 7. Next bounded action

Use the GitHub UI to inspect secret metadata and security alerts, then run one read-only Gemini audit. After collecting its revision-bound evidence, perform the first authorized implementation pass for deterministic scanner workflows and Gemini evidence provenance. Keep the Astra mutation workflows gated pending their dedicated review.

Project map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
