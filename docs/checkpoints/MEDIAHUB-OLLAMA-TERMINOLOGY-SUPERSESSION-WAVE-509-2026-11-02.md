# MediaHub OS — Ollama terminology supersession and runner consolidation (Wave 509)

Date: 2026-11-02
Status: **TERMINOLOGY CORRECTION DOCUMENTED / RUNNER REFACTOR PROPOSED IN PR #610 / CI NOT VERIFIED / NOT ACCEPTED**

## 1. Authoritative owner direction

The owner clarification in [Issue #301, Wave 338](https://github.com/VlDMlNSh/mediahub-os/issues/301#issuecomment-6326925941) explicitly says that prior mentions of “Alamo” mean the local Ollama executor, not a separate host-name requirement. The owner reaffirmed this direction in the current task on 2026-11-02. The correction is also recorded in [a new Issue #301 comment](https://github.com/VlDMlNSh/mediahub-os/issues/301#issuecomment-6568555691).

Canonical meaning:
- **Ollama** — local inference runtime/API server.
- **Model tag** — the model selected and served by Ollama, e.g. llama3.2:3b.
- **Physical host** — e.g. Voktors-Mini.Dlink, identified as Mac mini 2018. The physical host is not the runtime name.
- **Client / integration** — Claude Code via FCC/ECC, subject to route qualification.
- **Cloud-agent pool** — separate GitHub Actions/controller route. The local Ollama host is never Gemini transport.

There is no separate Alamo/Allamo service, endpoint, hostname, host, or executor identity. Wave 364/365 statements that “Alamo” was a distinct host/server are superseded. Historical reports and filenames remain in Git history and are annotated rather than erased.

## 2. Search scope and findings

Repository code search on main at f0448f28c7cfa61e4450c38529f09afbfdbbc7c7:
- Alamo / case variants: 8 matching source/document files.
- Allamo: 0 code-search matches.
- Ollama: 60 matching files, including valid runtime IDs, environment names, tests, docs and workflows.

The 8 current-main Alamo result paths:
1. docs/checkpoints/MEDIAHUB-NEXT-FOUR-EXECUTOR-EXECUTION-AND-ALAMO-IDENTITY-WAVE-364-2026-10-22.md
2. architecture/MEDIAHUB-DISTRIBUTED-AI-INFRASTRUCTURE.md
3. docs/architecture/MEDIAHUB-CHAT-TREE-MAP-ADDENDUM-WAVE-365-2026-10-22.md
4. docs/checkpoints/MEDIAHUB-NEXT-CONTINUATION-CHECKPOINT-WAVE-365-2026-10-22.md
5. docs/checkpoints/MEDIAHUB-MERGE-AND-ROUTING-GOVERNANCE-AUDIT-WAVE-369-2026-10-22.md
6. docs/checkpoints/MEDIAHUB-JARVIS-CORPORATION-ARCHITECTURE-PROPOSAL-CROSSWALK-WAVE-01-2026-10-15.md
7. docs/checkpoints/MEDIAHUB-NEXT-MAC-MINI-2018-IDENTITY-AND-FOUR-EXECUTOR-BLOCKERS-WAVE-365-2026-10-22.md
8. docs/checkpoints/MEDIAHUB-CONTOUR-A-WB-14-JARVIS-A0-AND-DIRECT-LOCAL-ROUTE-SOURCE-RECONCILIATION-2026-10-15.md

Large canonical sources contain additional historical mentions:
- Canonical map blob 75f62685459ec99ebf8be478f4e9096cdb842b1d: 92 case-insensitive legacy matches before the Wave 509 prepend.
- Continuation checkpoint pre-Wave509 blob b6070d3330c4083999f6ddb02dc6a7e11ade8a99: 167 legacy matches.
- Master Roadmap blob ea7e94e921045253f3e6494438e197c4bafae3a0: 200 legacy matches.
- Bootstrap blob 75f30750183efe8c6877368e9f0ada48f8e81ea7: 21 legacy matches.

The large-map/checkpoint/roadmap hits are a mixture of historical reports, active requirements, path names and audit trails. They are not all current component definitions. The current governing note is now prepended to each index source; old records must be read with the supersession notice.

## 3. Corrections made

### Active runner implementation proposal — PR #610 branch

Branch: contour-a/alamo-fcc-claude-hosted-runner-20261031 (legacy branch slug retained as a historical Git ref; not a component identity).

- Renamed workflow: removed .github/workflows/mediahub-alamo-fcc-claude-runner.yml; added .github/workflows/mediahub-ollama-fcc-claude-runner.yml.
- Renamed contract test: removed tests/test_mediahub_alamo_fcc_runner_contract.py; added tests/test_mediahub_ollama_fcc_runner_contract.py.
- Renamed job identity to ollama-local-fcc-claude.
- Normalized workflow artifact/temp names and result marker to Ollama terminology.
- Replaced the misleading equivalence field with ollama_runtime_qualification=NOT_VERIFIED.
- Added a regression test that rejects the legacy alias in the runner workflow source.
- Updated PR #610 title/body and scope to describe Ollama runtime, model and physical host as separate identities.
- Updated the PR's Wave 496/497/498/500 addenda and renamed three PR-scoped report files to Ollama names.
- Annotated Wave364/365/369 and related historical architecture/reconciliation reports with an explicit Wave509 supersession note. Their historical claims have not been erased.

Latest observed test update commit: 961ad2018ed6b702f501c03511596e519742d9e4. Re-read the branch and re-check exact-head CI before treating this implementation proposal as verified. Workflow source readback had no legacy alias and contained the new Ollama job name. The renamed test also had no legacy alias before the final regression guard was appended.

### Governing docs — PR #620 branch

Branch: docs/wave508-pr-review-and-governance-revalidation-2026-11-02, targeting canonical docs branch docs/mediahub-chat-tree-map-20261012.

- Prepended the authoritative Wave509 correction to the canonical map.
- Updated Bootstrap's active local executor sections: no more “Alamo/server 3” entity; local Ollama route and actual host ID/capability verification are separate.
- Prepended the correction to the continuation checkpoint and Master Roadmap.
- Added Wave509 map addendum and this dated report.
- Added a self-contained master continuation prompt for a new chat.
- These documentation changes remain a draft proposal until PR #620 CI/review and canonical integration pass.

## 4. Architecture after correction

Runner 1 target: Ollama local inference runtime + FCC/ECC + Claude Code, isolated from cloud-agent tools. A GitHub-hosted Ubuntu workflow is ephemeral; it is not a persistent VM. If execution happens on the physical Mac mini, verify Voktors-Mini.Dlink host ID and its allowlist separately.

Runner 2 target: three Gemini agent roles plus other approved cloud development agents. Gemini agents must be dispatched only by the approved controller workflow and must never be transported by SentinelX/local Ollama.

Local request path candidate: Claude Code → FCC/ECC → Ollama endpoint → exact model tag. This path remains conditional on evidence of actual upstream identity, auth/cost class, terms, network egress, no Anthropic API or paid fallback, and exact task execution. Running Claude Code on a host alone does not prove inference is local.

## 5. Current governance and execution state

- main: f0448f28c7cfa61e4450c38529f09afbfdbbc7c7.
- Canonical documentation branch at audit start: d9a289b9113f7567711b641a7017eb814d6c259d.
- Issue #296 title/body updated to Ollama terminology; remains OPEN.
- Issue #301 received the Wave509 clarification comment; remains OPEN.
- PR #610 remains OPEN; corrected runner changes are proposed and must pass exact-head CI and independent review. Earlier PR #610 checks ran only PR no-op/contract behavior; they do not prove live Ollama/FCC/Claude execution.
- PR #613 had five required exact-head contexts SUCCESS on 237948e03088c3ea43608b0c284327c552d34f4b, but formal independent review was zero at the last Wave508 check.
- PR #614, #615, #618 are documentation PRs; their bodies/titles have been corrected to Ollama language. Check latest exact-head CI and reviews.
- PR #620 contains Wave508 and Wave509 docs; OPEN/DRAFT until exact-head checks and review are independently verified.
- Active ruleset MediaHub-main-autonomous-merge, ID 26108066, enforcement ACTIVE; five required contexts: Astra Cloud Runtime Validation, Astra Verify, AI Factory verification, provider contract verification, Gemini workflow contract validation (Wave 284).
- SentinelX: one operational host Voktors-Mini.Dlink, ID host_5f7264034bdf0b51; Free plan, one active host / zero available slots. mh-dev-01 and mh-dev-02 are disabled. No independent third server was confirmed.
- Gemini controller batch: NOT RUN. No controller/child run IDs.
- Local Ollama/FCC/Claude task in this Wave: NOT RUN. No model/provider call, live install, merge or deployment.
- Secret values were not read; secret presence/scope was not verified.

## 6. Verification required before acceptance

1. Re-fetch branch heads, PR #610/#620 metadata and exact-head Check Runs.
2. Run the Ollama runner contract test and all five active required CI contexts on the final PR610 SHA.
3. Review source to verify no old alias in active workflow/test IDs, no cloud-agent installation on Runner1, no Anthropic API/paid fallback, owner-only exact-SHA gate, loopback binding, token isolation, cleanup and artifact redaction.
4. Independently review exact final PR head; a copied “APPROVED” comment does not count as formal GitHub review.
5. Only after CI/review/governance, consider a separate owner-authorized workflow_dispatch on exact main SHA. PR CI is a non-launching no-op; it is not runtime evidence.
6. Record runtime/model/host/FCC/Claude versions, run/job IDs, artifacts/digests and terminal statuses. Keep model inference, FCC compatibility, Claude Code task execution, qualification and acceptance distinct.
7. Do not dispatch Gemini until controller admission, secrets/variables metadata, HMAC separation, exact-main CI, required review, effective governance and trusted-main no-secret probe pass.
8. Update canonical map/checkpoint/roadmap and close these PRs only with verified evidence.

## 7. Disposition

- Terminology correction: DOCUMENTED / OWNER-CONFIRMED.
- Runner code refactor: IMPLEMENTED IN PR BRANCH / CI NOT VERIFIED / NOT ACCEPTED.
- Historical record supersession: ANNOTATED IN PR BRANCH / CANONICAL MERGE PENDING.
- Ollama live runtime, model inference and Claude/FCC task: NOT RUN / NOT QUALIFIED.
- Gemini batch: NOT RUN.
- Contour A: NOT ACCEPTED.
- Contour B: GATED.

## Navigation

- [Canonical project map](https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md)
- [Continuation checkpoint](https://github.com/VlDMlNSh/mediahub-os/blob/docs/wave508-pr-review-and-governance-revalidation-2026-11-02/docs/checkpoints/mediahub-next-continuation-checkpoint-2026-10-12-current.md)
- [Master Roadmap](https://github.com/VlDMlNSh/mediahub-os/blob/docs/wave508-pr-review-and-governance-revalidation-2026-11-02/docs/checkpoints/MEDIAHUB-MASTER-DEVELOPMENT-ROADMAP-1.0.md)
- [Bootstrap instruction](https://github.com/VlDMlNSh/mediahub-os/blob/docs/wave508-pr-review-and-governance-revalidation-2026-11-02/docs/architecture/MEDIAHUB-CONTEXT-BOOTSTRAP-INSTRUCTION.md)
- [Issue #296](https://github.com/VlDMlNSh/mediahub-os/issues/296)
- [Issue #301](https://github.com/VlDMlNSh/mediahub-os/issues/301)
- [PR #610](https://github.com/VlDMlNSh/mediahub-os/pull/610)
- [PR #620](https://github.com/VlDMlNSh/mediahub-os/pull/620)
