# MediaHub OS — PR #421 / #426 probe integration boundary (Wave 299)

Date: 2026-10-21  
Disposition: **BLOCKED / NOT_PROVEN**  
Scope: bounded source and governance recheck only. No dispatch, credentials, merge, deployment, or qualification.

## Current refs and review state

- `main`: `80be45a70732b1d568164571d4273a6397792c3b`.
- PR #421: OPEN, DRAFT, UNMERGED; head `185f55b63121b1aece7e60f6c087ecfceab2721e`; base SHA `80be45a70732b1d568164571d4273a6397792c3b`. Metadata reports 11 changed files.
- PR #426: OPEN, DRAFT, UNMERGED; head `6caf55977260e808a055c8c4b9a04d68eb050d8c`; same base SHA; metadata reports 3 changed files.
- Submitted GitHub review records: none visible for #421 or #426.
- PR #428 remains a report-only Draft. Its Gemini `APPROVE` report does not substitute for a formal review of the exact #421 head.

## Source read-back

| Source | Ref | Blob SHA | Evidence |
|---|---|---|---|
| Controller workflow | PR #421 branch | `4cec1aa234fd9ccb0d41533b37248fff079c79c5` | Default `mode=probe`, `confirm=no`; model jobs require `workflow_dispatch`, `mode=agents`, `confirm=yes`; each agent job maps its provider secret explicitly. |
| Reusable context observer | PR #421 branch | `e05759d04f34f52cc7ad1b794b6718585ee2507f` | `workflow_call`, empty permissions, exact event/ref predicate; observer has no checkout, external action, provider secret, or model call. |
| Separate caller sentinel | PR #426 branch | `1bb861788fa586c3bb23c6405c0c65410bac68bc` | Separate reusable `workflow_call` workflow; no model/provider/network action; guarded sentinel should be skipped for unapproved callers. |
| Astra Verify | PR #426 branch | `f8f8de42bd8b454ba6e3b67a0e4740914bd6c0ed` | Calls the sentinel and asserts a non-controller context is denied. |

## Integration boundary

The inspected paths are distinct in these current refs: PR #421's controller calls `.github/workflows/gemini-reusable-context-probe-wave284.yml`; PR #426 adds `.github/workflows/gemini-caller-context-probe.yml` and wires it into `astra-verify.yml`. The earlier concern about same-path probe-role collision is **not demonstrated by these exact file paths**. This is not proof that the PRs are conflict-free as complete changesets, nor does it resolve sequencing, branch protection, or review requirements.

The PR #426 sentinel tests an unapproved caller's negative path. The PR #421 evidence previously recorded for the same head covers pull-request context and model jobs skipped. Neither establishes a successful trusted positive `workflow_dispatch` observer path. The controller's `agents` mode remains capable of mapping provider secrets; do not use it to collect positive-context evidence.

## Governance and checks

- The classic `main` branch-protection endpoint previously returned 403 to the available integration; repository-level rulesets returned an empty list. Effective organization/repository protection and Actions policy remain **unverified**, not absent.
- The combined commit-status endpoint returned an empty status list for the PR #421 head; that endpoint alone is not a complete Actions check-run inventory. Use the linked exact-head Actions runs in Wave 298's report for the already-recorded CI evidence.
- No formal submitted review is visible for either candidate PR.
- No code or workflow was changed in this pass. No positive dispatch, provider/model call, secret-value access, merge, deployment, qualification, or acceptance occurred.

## Decision and next bounded step

Keep #421 and #426 Draft/unmerged. First obtain a substantive independent review tied to exact head `185f55b63121b1aece7e60f6c087ecfceab2721e` and administrator-visible governance evidence. Then re-check the complete PR file sets and exact-head CI, and only after accepted integration consider a no-secret positive-context probe that cannot invoke child agent workflows. Do not dispatch `mode=agents`.

## Direct references

- [PR #421](https://github.com/VlDMlNSh/mediahub-os/pull/421)
- [PR #426](https://github.com/VlDMlNSh/mediahub-os/pull/426)
- [PR #428 report-only review artifact](https://github.com/VlDMlNSh/mediahub-os/pull/428)
- [Issue #301](https://github.com/VlDMlNSh/mediahub-os/issues/301)
- [Wave 298 source trace](MEDIAHUB-GEMINI-REVIEW-SOURCE-TRACE-WAVE-298-2026-10-21.md)
- [Canonical project map](../architecture/MEDIAHUB-CHAT-TREE-MAP.md)
