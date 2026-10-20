# MediaHub Contour A — Gemini caller-context probe startup-failure triage (Wave 284)

**Date:** 2026-10-20  
**Execution class:** GitHub source/status inspection and documentation; no runtime/provider operation.

## Objective and bounded task decomposition

This `/next` is divided into five small tasks:

1. **Triage exact-head non-launching caller-context probe failure.** Completed in Wave 284.
2. Design a no-provider, no-secret probe that tests the exact controller-only caller predicate without creating a permissions escalation or workflow-path collision.
3. Implement the smallest isolated workflow/test correction on a dedicated candidate branch or PR; do not overwrite either PR's file semantics in place.
4. Recheck actionlint, static positive/negative contracts, and exact-head GitHub Actions results. The runtime probe must not invoke Gemini or any provider.
5. Obtain a genuine independent review and verify repository-protection evidence; only then decide on governance-approved integration. Agent dispatch, merge and deployment remain separately gated.

Only task 1 was performed in this pass.

## Current refs and gates

- Canonical documentation branch `docs/mediahub-chat-tree-map-20261012`: HEAD `a5d6e13f4c573fcd8aaa09ef8d7bb6e956c7631f` before the Wave 284 documentation commits.
- `main`: HEAD `80be45a70732b1d568164571d4273a6397792c3b`.
- [Issue #301](https://github.com/VlDMlNSh/mediahub-os/issues/301): OPEN; observed update timestamp 2026-10-20T16:40:40Z.
- [PR #421](https://github.com/VlDMlNSh/mediahub-os/pull/421): OPEN / DRAFT / UNMERGED; candidate head `abcfce3f70c4cc56335bf353a51a268d998f41b0`; base `main` at `80be45a70732b1d568164571d4273a6397792c3b`. No submitted independent review was returned.
- [PR #426](https://github.com/VlDMlNSh/mediahub-os/pull/426): OPEN / DRAFT / UNMERGED; head `6caf55977260e808a055c8c4b9a04d68eb050d8c`; base `main` at `80be45a70732b1d568164571d4273a6397792c3b`. No submitted independent review was returned.
- Repository branch-protection read returned HTTP 403 for the connected integration; protection requirements remain unverified, not absent.

## Exact-head evidence and source diagnosis

For PR #421 head `abcfce3f70c4cc56335bf353a51a268d998f41b0`:

- [Astra Verify #39459833610](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39459833610): SUCCESS.
- [Astra Cloud Runtime Validation #39459833967](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39459833967): SUCCESS.
- [Non-launching caller-context probe #39459834572](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39459834572): `startup_failure`.
- The probe run metadata reports zero jobs. The connected GitHub API returned HTTP 404 for its logs endpoint. Therefore there is no runner-step log and no directly observed runtime caller context to cite.

Read-back of the candidate source provides a strong structural explanation, but not a definitive server-side error message:

1. PR #421's caller workflow `.github/workflows/gemini-caller-context-probe.yml`, blob `e23694317ce7892e646e4750af46476a1f90ca2e`, calls `.github/workflows/gemini-agent-2.yml` with `probe_only: true`, an empty secret map, and caller job permissions limited to `contents: read` and `issues: read`.
2. Its called workflow `.github/workflows/gemini-agent-2.yml`, blob `9fced7999c0ab5a5a8b9666fd92791726b64fc66`, declares an `engineer` job that requests `contents: write`, `pull-requests: write`, and `issues: read`. The probe input makes that job ineligible at runtime, but the reusable-workflow graph still contains the broader permission declaration.
3. GitHub's [reusable workflow documentation](https://docs.github.com/en/actions/reference/workflows-and-actions/reusing-workflow-configurations) states that `GITHUB_TOKEN` permissions can only be maintained or reduced in a called workflow; they cannot be elevated. Combined with a startup failure and zero jobs, the permission mismatch is the leading static hypothesis. It has **not** been confirmed by a readable startup log.
4. PR #426 supplies a different reusable sentinel under the same path `.github/workflows/gemini-caller-context-probe.yml`, blob `1bb861788fa586c3bb23c6405c0c65410bac68bc`. PR #421 uses that path as a `pull_request` caller workflow instead. This is a concrete path/semantic collision across two unmerged candidates. They must not be merged together unchanged or treated as one qualified probe.

PR #426 exact-head checks returned SUCCESS: [Astra Verify #39456720322](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39456720322) and [Astra Cloud Runtime Validation #39456720748](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39456720748). Those checks do not fix or qualify PR #421's distinct caller workflow.

## Disposition

- **Triage outcome:** high-confidence source-level permission mismatch plus independently verified workflow-path collision; exact startup cause remains **probable, not conclusively proven** because the startup logs were inaccessible and zero jobs were created.
- Next work should separate the harmless caller-context sentinel from the write-capable Gemini child. Use a distinct workflow filename and a permission-compatible probe-only contract; test that the exact guard expression remains attached to each real child `engineer.if` with static contract tests. Do not compensate by giving the PR probe write-capable permissions merely to make startup proceed.
- Re-read PR #421/#426 file diffs before edits to keep their bases and meanings isolated. Preserve the single controller ingress, explicit confirmation gate, per-child secret isolation, exact trusted ref, and A3 review requirement.
- No provider/model invocation, secret-value access, agent dispatch, manual workflow dispatch, test execution in this pass, merge, deployment, route qualification, or acceptance occurred. Contour A remains **NOT_PROVEN / BLOCKED**. Contour B remains gated pending Contour A deployment and independent acceptance.

## Primary project links

- [Canonical project map](../architecture/MEDIAHUB-CHAT-TREE-MAP.md)
- [Current continuation checkpoint](mediahub-next-continuation-checkpoint-2026-10-12-current.md)
- [Master Development Roadmap](MEDIAHUB-MASTER-DEVELOPMENT-ROADMAP-1.0.md)
- [Context bootstrap](../architecture/MEDIAHUB-CONTEXT-BOOTSTRAP-INSTRUCTION.md)
- [Governance Issue #301](https://github.com/VlDMlNSh/mediahub-os/issues/301)
