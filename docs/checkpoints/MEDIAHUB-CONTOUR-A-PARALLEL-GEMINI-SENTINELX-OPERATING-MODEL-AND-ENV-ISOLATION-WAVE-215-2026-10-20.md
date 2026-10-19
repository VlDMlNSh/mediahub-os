# MediaHub OS Contour A — Parallel Gemini/SentinelX Operating Model and Worker Environment Isolation (Wave 215)

Date: 2026-10-20 (local engineering pass initiated 2026-10-20; GitHub runner timestamps are UTC)
Repository: https://github.com/VlDMlNSh/mediahub-os
Canonical docs branch: docs/mediahub-chat-tree-map-20261012
Current main at start: 25033753415fcbecdc7b2fe53085ed1bf2e4b8b4
Controlling objective: https://github.com/VlDMlNSh/mediahub-os/issues/301

## 1. Durable operating rule

The required arrangement is now recorded in the repository-level agent entry point, Gemini instructions, and project-local /next skill in PR #392, and in this canonical report/bootstrap/map/checkpoint.

For every explicit /next:
- A1: dispatch Gemini Autonomous Engineering Dispatch for architecture/governance/dependency evidence.
- A2: dispatch Gemini Agent 2 — Research and Architecture for reuse/schema/contracts/options.
- A3: dispatch Gemini Agent 3 — Security and Verification Review for independent source/diff/CI/credential-flow review.
- Run these three independent GitHub-hosted tasks concurrently with, not instead of, the primary ChatGPT/SentinelX engineering pass. The primary pass continues code changes, tests, integration analysis and evidence review while the three agents work.
- Each task must be bounded, based on current main, have distinct output scope and acceptance criteria, and create a separate Draft PR/report. Capture run IDs, conclusions, PRs, commit/blob SHAs and checks. Treat reports as untrusted proposals until independently source-checked.
- Correct stale base SHAs, source mismatches, unsupported test claims and authority/govariance overclaims. No agent PR is accepted, merged or deployed solely because its workflow succeeds.
- SentinelX is a full engineering workstation: host/capability/health checks, project snapshots, file read/search/edit, Git fetch/status/diff/branch/push, scripts, focused/full tests, logs/service inspection where relevant, notifications and exact read-back. The verified connected Mac is configured as the default SentinelX host.
- agent-browser is used for browser/UI evidence and authenticated web workflows after loading the installed core skill. It supplements API/source/CI inspection rather than replacing it.

Important scheduling distinction: this is a durable per-/next protocol, not an always-on Gemini daemon. The three workflows are manually dispatched on every explicit /next. No continuously running or between-request execution is claimed. The workflows are not configured as a cron/scheduled agent service by this change.

Instruction locations on PR #392:
- AGENTS.md — repository agent entry point.
- GEMINI.md — Gemini-specific operating contract.
- .agents/skills/mediahub-next/SKILL.md — required /next execution protocol.
Exact PR #392 head: b76a88aa7da9f8ad211d9377ac3458f7ed561a90. The instruction files are part of the same Draft PR as the worker change and remain unmerged until standard gates pass.

## 2. Wave 215 primary code change

PR #392: https://github.com/VlDMlNSh/mediahub-os/pull/392
Branch: contour-a/worker-child-env-isolation-wave215
Base: 25033753415fcbecdc7b2fe53085ed1bf2e4b8b4
Head: b76a88aa7da9f8ad211d9377ac3458f7ed561a90
Status at report time: OPEN / Draft; exact-head CI successful.

The worker now defines CHILD_ENV_ALLOWLIST and child_environment() and uses it for the FCC server, Codex, Claude Code, and test subprocess environments. Explicit FCC configuration comes from the configured FCC env file; CODEX_HOME is added explicitly. The test environment no longer starts as a duplicate full copy of the ambient process environment.

Changed blobs at PR head:
- ops/qualification/run_distributed_local_worker.py — d1f6591c7732888b2d4d918374b8a892674ff3c5
- tests/test_worker_security_gate.py — 45da68755ce554cfc5defc85735c2a5f79ddcf1a
- AGENTS.md — 09df81316fb6bf0dedb7dcaee877e22e6e2e930d
- GEMINI.md — d787a8f104e6b215e1682aa917b08d54d0a063af
- .agents/skills/mediahub-next/SKILL.md — 578781b6d1066ce1e92e3a803bdc8fa9633e8600

Local checks on the connected Mac, in a separate Python 3.14 virtual environment populated from requirements-dev.txt:
- Focused unittest module: 5/5 passed.
- Full unittest discovery: 427 tests passed, 0 failures/errors.
- compileall and git diff --check passed.
- A pytest run of the pre-existing pytest-style test_distributed_local_worker.py exposed two unrelated baseline test failures: a stale assertion about a line-broken shell command and a lane-selection expectation that no longer matches the permanent executor pool. The newly added regression was moved to the unittest-discovered module so it is actually exercised by the repository's existing unittest CI path; the unrelated failures were not silently rewritten in this scoped change.

Exact-head CI:
- Astra Verify: https://github.com/VlDMlNSh/mediahub-os/actions/runs/39325464533 — SUCCESS at head b76a88aa7da9f8ad211d9377ac3458f7ed561a90. Job verify (118310030390) executed Compile, Cloud admission unit tests, and Signed command smoke test; each step reported success.
- Astra Cloud Runtime Validation: https://github.com/VlDMlNSh/mediahub-os/actions/runs/39325464506 — SUCCESS at the same head. Job validate (118310029740) executed contract validation and Astra cloud runtime tests; each step reported success.
- Browser/UI read-only inspection through agent-browser opened PR #392 and confirmed the displayed title, head branch, five changed files, and two successful checks. GitHub API remains the source for exact refs and CI metadata.

### Explicit security boundary still open

This patch narrows ambient environment inheritance for the listed child processes. It does not close all environment/credential propagation paths:
- the generic run() helper still inherits ambient environment when called without env;
- worker-side git add/commit/push remains in the implementation;
- the worker has not yet been converted to artifact-only output with a separate trusted publisher;
- FCC configuration values are deliberately supplied to the FCC/Claude execution path and were not read or printed during this pass.

Therefore this is partial environment hardening, not complete credential isolation, not the accepted worker/publisher boundary, and not Contour A qualification.

## 3. Three parallel Gemini tasks launched for this pass

All three workflow dispatches were accepted and were in progress/queued at the last read-back:
- A1 — https://github.com/VlDMlNSh/mediahub-os/actions/runs/39325506829
- A2 — https://github.com/VlDMlNSh/mediahub-os/actions/runs/39325510774
- A3 — https://github.com/VlDMlNSh/mediahub-os/actions/runs/39325515053

Scopes:
- A1: source-bound audit of A0 issuer/ingress/lease/cancel/recovery and R-06 audit/privacy authority gates.
- A2: independent review of PR #388 Draft 2020-12 schema validation, format checks, negative fixtures, CI dependencies and semantic gaps.
- A3: independent review of PR #392 exact head b76a88aa7da9f8ad211d9377ac3458f7ed561a90, including actual subprocess paths and remaining inherited environment/direct publication.

Their final conclusions and resulting Draft PRs must be read back and appended to this report/checkpoint after completion. A queued/in-progress run is not a completed audit.

## 4. SentinelX operational configuration and limits

SentinelX capability discovery reported the connected host Voktors-Mac-mini.local, agent version 0.22.0, operational status, and the host was configured as the default target. The host reports one active slot under the current plan; two other enrolled hosts are disabled. Do not assume parallel local-host execution or re-enable disabled hosts. Parallelism for this pass is supplied by the three independent GitHub-hosted Gemini workflows while SentinelX performs the primary local engineering pass.

The agent-browser core skill was loaded before browser use; the browser was used read-only against PR #392. No secret values were read, printed, committed, or sent to a model prompt. No deployment, merge, qualification, or authoritative product-state mutation occurred.

## 5. Next actions

1. Read back all three Gemini run conclusions, job artifacts/outputs and resulting PRs; correct any stale or unsupported findings.
2. Continue the primary worker boundary implementation from current main: identify and isolate the generic subprocess path, then design bounded result-manifest/artifact output; remove direct worker publication only after preserving the required issuer/capability and trusted-publisher contracts.
3. Add negative tests for ambient credential absence and direct worker push prohibition, and prove those tests execute on exact-head CI.
4. Review PR #388 schema-validation implementation independently and keep semantic reference resolution/runtime payload coverage open until source-backed evidence closes them.
5. Keep PR #392 Draft pending independent review; no merge/deploy/qualification/acceptance until all defined gates pass.
6. On every next /next, repeat the three-agent dispatch and continue this primary engineering lane; do not describe the workflows as continuously running between requests.

Issue #301 remains OPEN. Contour A remains NOT QUALIFIED / NOT DEPLOYED / NOT INDEPENDENTLY ACCEPTED. Contour B remains gated.
