# MediaHub OS — per-/next three-agent orchestration contract (Wave 307)

- Date: 2026-10-21
- Status: DOCUMENTED TARGET / LIVE DISPATCH STILL BLOCKED
- Canonical instruction reviewed: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CONTEXT-BOOTSTRAP-INSTRUCTION.md, blob SHA e21423ac619fdc9ef4381cca40b0e3675277c42c.
- Governance tracker: https://github.com/VlDMlNSh/mediahub-os/issues/301.
- Controller-only integration gate: https://github.com/VlDMlNSh/mediahub-os/pull/421.
- Working evidence PR: https://github.com/VlDMlNSh/mediahub-os/pull/430.
- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md.

## Finding

The canonical Bootstrap already contains a per-/next parallel-work rule in §1A and the binding launch transport in §§1B–1C. It names .github/workflows/gemini-batch-dispatch-controller.yml as the only authorized entry point, states that the legacy REST-dispatch route is ON HOLD, and requires PR #421's controller-only workflow_call architecture to pass security/CI/governance gates before use. The gap is not absence of an instruction to use three agents; it is ambiguity across historical wording about when live dispatch becomes authorized and absence of a crisp, non-overlapping standing task matrix.

Issue #301 says the queue is documentary, not a live scheduler. PR #421 is still an OPEN/DRAFT implementation proposal and its description says it does not authorize agent dispatch, merge, deployment or qualification. This pass does not dispatch any Gemini workflow and does not change authority.

## Required /next orchestration after controller gate is accepted

At the beginning of each /next, after live refs/HEAD and governing contracts are read, the lead ChatGPT session creates three bounded, independent work packets from the same exact target HEAD and current roadmap step. Agents return evidence and recommendations to the lead; they do not independently choose competing project-wide goals.

1. Gemini Agent 1 — implementation/research slice. Inspect the highest-priority open roadmap item and existing stable components. Return one narrowly scoped implementation or source-backed design proposal; include exact paths/refs/blob SHAs, proposed diff or patch on an isolated branch when permitted, tests, dependencies and rollback. Do not merge or change protected/canonical refs.
2. Gemini Agent 2 — independent contract/test verification. Independently derive acceptance criteria from primary contracts; inspect Agent 1's proposal and relevant existing implementation. Run only authorized, bounded tests. Return reproducible commands, exact tested HEAD, CI/run/job/artifact IDs, failures and a pass/fail matrix. Do not merely restate Agent 1's conclusions.
3. Gemini Agent 3 — security/governance review. Review the same target and proposed change for issuer/capability, caller context, least privilege, secret boundaries, provenance, data/provider route, quotas, branch protections, failure/recovery and authority separation (Jarvis, ASTRA A0, Product State Authority). Return findings ranked by severity with file/line/blob evidence and explicit BLOCK/ALLOW recommendation. A review artifact is not formal GitHub approval unless recorded through the authorized review process.

## Shared packet and result protocol

- All three tasks name the same immutable source commit SHA, task ID, roadmap item, acceptance criteria, allowed paths/actions, prohibited actions, deadline/budget, expected evidence schema and fail-closed conditions.
- Give each agent a separate task/branch/workspace where the controller supports it. Do not allow overlapping writes; Agent 2 and Agent 3 default to read-only.
- Missing, timed-out, refused or malformed results are NOT RUN / INCOMPLETE, never success. Continue independent lead work where safe.
- The lead reconciles disagreement, reads every proposed changed file back, verifies exact commit/blob SHA and exact-head CI, and chooses integration only after applicable gates. Agents do not grant each other authority and cannot self-approve merges/deployments.
- Each /next report records controller run ID; all three child job/run IDs and terminal conclusions; task packet hashes; artifacts/PRs; source and result SHAs; test evidence; unresolved findings; and next roadmap step. If dispatch is blocked, report the exact gate and continue non-agent work.
- Never use alternate dispatch routes, direct local/server Gemini CLI, ad-hoc scripts, secrets: inherit, or expose MEDIAHUB_GITHUB_TOKEN. No paid fallback without separately authorized budget/provider route.

## Live gate snapshot and disposition

- PR #421: OPEN/DRAFT. Its stated requirements include independent review, exact-head CI, caller guard/secret-boundary review and a controlled negative caller-context test without launching Gemini. This pass has not established that all gates are satisfied or that the PR is integrated.
- Issue #301: OPEN. It explicitly states the CAF-Q queue is documentary rather than a live scheduler.
- Therefore, desired behavior is three bounded Gemini tasks per /next, but live launches remain BLOCKED until PR #421 and all governing runtime/authority gates are verified complete. Do not claim agents ran from this documentation change.

## Project Instructions versus GitHub documentation

The repository Bootstrap is the detailed source of truth and already requires it to be read on every /next. A project-level instruction should only point to that canonical Bootstrap and say: “For every /next, follow Bootstrap §1A and the Wave 307 three-agent task matrix; launch only through the accepted controller after all gates pass; if blocked, continue independently and report NOT RUN.” Editing this repository does not automatically modify the user's ChatGPT Project Instructions.

## Next step

Recheck PR #421's exact live HEAD, required CI, independent review and safe negative caller-context probe. Do not launch the Gemini controller until the documented gates are satisfied and integrated. Then run one controlled controller-only validation and capture all three child outcomes before describing the per-/next orchestration as operational.