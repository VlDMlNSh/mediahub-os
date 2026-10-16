# MediaHub OS — Gemini Read-only Workflow Source Review, Wave 09

- Date: 2026-10-16
- Status: **STATIC SOURCE REVIEW / FINDINGS / PATCH PLAN PROPOSED / NOT QUALIFIED**
- Scope: exact workflow files on `main`; source-only review, no execution.
- Parent design: [Autonomous Cloud-Agent Development Fabric Reference Architecture, Wave 08](MEDIAHUB-AUTONOMOUS-CLOUD-AGENT-FABRIC-REFERENCE-ARCHITECTURE-WAVE-08-2026-10-16.md)
- Functional authority: Baseline 2.0 on `main`.
- Restriction: this review does not dispatch workflows, call providers, inspect or use secrets, run tests/scanners, alter workflow source, or change repository settings.

## 1. Exact source revisions

| Workflow | Ref | Blob SHA | Source-level role |
|---|---|---|---|
| `.github/workflows/gemini-readonly-audit.yml` | `main` | `0d10efdda251f2ceca43175981c919102303572b` | Manual read-only advisory audit; contents read; Gemini API request; artifact retention 14 days |
| `.github/workflows/gemini-readonly-audit-retry.yml` | `main` | `96fcc9ed4e45659d0118f0b9f3593a0c736200f0` | Manual read-only advisory audit with bounded retry and sanitized error metadata; contents read; artifact retention 14 days |

These SHA values identify the files retrieved for this source review. No claim is made about execution on those revisions.

## 2. Positive controls confirmed by source

- Both workflows use `workflow_dispatch`, declare `contents: read`, and repeat read permission at job level.
- Checkout sets `persist-credentials: false`.
- API keys are read from Actions secrets and are absent from the artifact content by intended code path; the workflows avoid printing raw HTTP error bodies.
- Context paths reject absolute paths, path strings containing `..`, newline characters, missing files, workflow-directory files, and files larger than 200 KB.
- The task prompt says repository content is untrusted evidence and requests advisory-only findings.
- The retry workflow has a bounded four-attempt policy for selected transient HTTP statuses and sanitizes several common key/bearer patterns in error text.
- Artifact upload is conditional on the expected output file existing and retention is set to 14 days.

These are static source observations, not runtime verification.

## 3. Findings and remediation priority

| ID | Severity | Finding | Consequence | Recommended control |
|---|---|---|---|---|
| GWF-01 | P0 before broader agent admission | `context_ref` is caller-selectable and checkout resolves a mutable ref rather than binding the run to an immutable SHA | A branch/tag can move; report provenance may diverge from the intended source snapshot | Resolve ref to commit once; checkout the exact SHA; record requested ref, resolved SHA and selected file digests in an evidence manifest |
| GWF-02 | P1 | Third-party actions use version tags such as `actions/checkout@v4` and `actions/upload-artifact@v4` | A tag is mutable relative to an immutable full-SHA pin | Verify upstream action revisions and pin full-length commit SHAs; maintain a reviewed update procedure |
| GWF-03 | P1 | Context selection accepts arbitrary repository-relative files rather than a task-specific path allowlist | A caller can provide broad or sensitive text files that pass basic traversal/size checks | Define per-task path allowlists and data classification; enforce file count, aggregate bytes and extension/content policy |
| GWF-04 | P1 | Retry workflow accepts an arbitrary model ID input | Destination/model identity is caller-controlled and may differ from the reviewed provider policy | Use a reviewed model allowlist bound to provider eligibility and task authorization; reject unknown identifiers |
| GWF-05 | P1 | Output is inserted into GitHub step summary as model-generated Markdown | Output may include misleading links, headings or formatting and can confuse evidence readers | Label output as untrusted advisory content; preserve a digest; render with bounded formatting or store the raw report as a quarantined artifact |
| GWF-06 | P1 | No manifest binds workflow run, source SHA, context file digests, action SHAs, model ID, policy revision and output digest | Independent reviewers lack a complete provenance envelope in the artifact | Emit a versioned evidence manifest and verify it independently before promotion |
| GWF-07 | P1 | Runner image uses `ubuntu-latest` | Runtime image changes can alter tools and execution behavior across runs | Record runner image metadata; use a controlled image where supported; qualify image updates separately |
| GWF-08 | P1 | Context ref/task/path inputs lack a comprehensive schema and total input bound | Very large or malformed input can consume resources or produce ambiguous evidence | Add bounded lengths, path count, aggregate context size, normalized ref policy and explicit task schema |
| GWF-09 | P2 | First workflow has no bounded retry; retry workflow is a separate parallel workflow rather than a single versioned shared policy | Behavior differs across entry points and maintenance can drift | Consolidate after governance review into one reviewed workflow implementation with explicit retry policy |
| GWF-10 | P0 for any write-capable extension | Read-only design is a useful boundary, but no accepted task-envelope, A0 issuer, R-06 audit sink or promotion contract is established by these files | These workflows cannot serve as a complete autonomous code-writing/promotion fabric | Keep advisory-only; qualify all additional authority boundaries before any write-capable worker exists |

## 4. Threat and boundary interpretation

1. Current workflow permissions are read-only at source level. No direct repository write token is declared in either workflow.
2. API invocation is an external provider call. This source review did not make such a call and does not establish account eligibility, provider entitlement, current quota, acceptable data policy or service availability.
3. Caller-controlled context and task text are untrusted. The workflow must keep them out of shell-code construction and privileged workflow expressions; current shell use passes values through environment variables and quotes them in the prompt.
4. Model output is advisory and untrusted. A successful HTTP response, non-empty report or uploaded artifact is not a security verdict, verification, qualification or acceptance.
5. Provider age/account/region eligibility is a hard gate. When eligibility is unknown or unmet, provider use remains blocked; this design provides no restriction bypass.
6. Branch protection and required-check settings remain UNKNOWN in the available evidence. Source-level `contents: read` permissions alone do not prove repository governance or an independent promotion path.

## 5. Proposed patch sequence — pending separate authorization

**Patch P0-A — immutable provenance**
- Resolve `context_ref` to one immutable commit SHA before checkout.
- Generate a manifest with workflow/run/job IDs, source SHA, requested ref, normalized input digest, selected path list, per-file digests, action SHAs, model/provider identity, policy revision, output digest and result status.
- Fail closed if resolution or manifest generation fails.

**Patch P0-B — strict input policy**
- Use an explicit allowed-ref policy and task-specific path allowlist.
- Bound task length, path count, aggregate context bytes and model output bytes.
- Pin the retry workflow's model ID to a reviewed allowlist; remove free-form model selection.

**Patch P1-A — action supply chain**
- Pin actions to verified full commit SHAs and record versions in the evidence manifest.
- Review runner-image stability and action update cadence.

**Patch P1-B — output quarantine**
- Store generated output as an untrusted advisory artifact.
- Sanitize or bound step-summary presentation; retain the original output digest.
- Require an independent reviewer before any result becomes an input to an implementation or promotion decision.

**Patch P1-C — shared policy**
- Consolidate duplicated prompt/context/provenance logic only after an approved patch plan and source-level compatibility review.
- Preserve a read-only workflow class separate from patch-producing workers.

## 6. Acceptance criteria for a future authorized implementation

- Inputs normalize deterministically; all bounds and allowlists are enforced.
- Checkout uses an immutable resolved SHA; manifest SHA matches checked-out source and context digests.
- Unknown refs, paths, models, providers, eligibility or policy decisions fail closed.
- Action revisions are full-SHA pinned and independently checked against upstream repositories.
- No secret values appear in logs, prompts, artifacts or summaries.
- Generated output remains advisory and cannot trigger a privileged action.
- Error, retry, timeout, cancellation and artifact-upload outcomes are represented in the manifest.
- Independent review binds findings to the exact workflow and artifact revisions.
- Tests, scanners, provider calls, workflow dispatch, qualification and deployment each require their own explicit authorization and evidence.

## 7. Disposition

The current Gemini workflow pair is a candidate for a **read-only advisory worker only**. Static source review identifies actionable provenance, input-scope, model allowlist, action pinning and output-handling gaps. No workflow was edited, dispatched, tested or qualified in this pass.

Next: prepare the exact P0/P1 patch proposal after A0 issuer/lifecycle, R-06 and target-manifest evidence is reconciled. Keep all implementation and execution gates explicit.

Project map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md


## Addendum — historical execution evidence verified in Wave 10

GitHub run metadata was subsequently retrieved for [run 38952885501](https://github.com/VlDMlNSh/mediahub-os/actions/runs/38952885501). It completed with `conclusion=success`; job `117148417231` shows the step **Call Gemini API with bounded retry** completed successfully, and artifact `12069128185` was uploaded with digest `sha256:a31c7a5036f003e6918c4c6a3ab0ad7f82c8c6c5fb10afde77f8a39d0d8b4d7d`. The run used source commit `b45324009ac3aa65322a702c28069b12190bc4b8`.

This direct run evidence establishes that the Gemini integration worked for that execution. The title and scope of this Wave 09 source review remain accurate: the ten findings concern source provenance, input bounds, action pinning, output handling and governance qualification. Those findings are remediation candidates, not a claim that the integration is nonfunctional. The broader autonomous fabric remains unqualified until its queue, agent registry, A0/R-06 authority, evidence manifest, isolated patch worker and promotion gates are established.

See [Wave 10 — Operational Evidence and Status Correction](MEDIAHUB-CLOUD-AGENT-FABRIC-GEMINI-OPERATIONAL-EVIDENCE-WAVE-10-2026-10-16.md) for the exact run/job/artifact metadata.
