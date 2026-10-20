# MediaHub OS Contour A — GitHub Transport controller integration and API-secret routing (Wave 217)

Date: 2026-10-20

## Outcome

- Updated the controller to use the repository secret `MEDIAHUB_GITHUB_TOKEN` for GitHub Actions REST API dispatch and run monitoring. Secret values were not read or logged.
- Controller PR #408 was merged after its exact-head checks passed. Merge commit: `27edfd5f04c6704ee7136c6cc73cf46f9731beb7`.
- The first dispatch attempt against `main` was rejected by GitHub with HTTP 422 because the unquoted YAML choice values `yes` and `no` were not accepted as strings. No child agents were launched by that attempt.
- Created fix PR #411 to quote both choice values. Current head: `9053d2115a54f357cccecb02a0e76091a528b662`; source blob SHA: `22f7e1ed844059b65cd5703f130da780ba2aa29b`. Read-back confirms `options: ["no", "yes"]` and `default: "no"`.
- PR #411 CI at last check: `validate` PASS; `verify` pending. Do not merge until the remaining check is complete and the exact head is rechecked.
- The corrected controller has not yet been dispatched; no new child run IDs, artifacts, or PRs are attributable to this wave.

## Evidence links

- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
- Bootstrap: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CONTEXT-BOOTSTRAP-INSTRUCTION.md
- Continuation checkpoint: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/checkpoints/mediahub-next-continuation-checkpoint-2026-10-12-current.md
- Master roadmap: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/checkpoints/MEDIAHUB-MASTER-DEVELOPMENT-ROADMAP-1.0.md
- Governing Issue #301: https://github.com/VlDMlNSh/mediahub-os/issues/301
- Controller PR #408: https://github.com/VlDMlNSh/mediahub-os/pull/408
- Choice-option fix PR #411: https://github.com/VlDMlNSh/mediahub-os/pull/411
- Controller merge commit: https://github.com/VlDMlNSh/mediahub-os/commit/27edfd5f04c6704ee7136c6cc73cf46f9731beb7
- Fix commit: https://github.com/VlDMlNSh/mediahub-os/commit/9053d2115a54f357cccecb02a0e76091a528b662

## Technical notes

The controller uses GitHub-hosted Actions and sends child `workflow_dispatch` requests using `MEDIAHUB_GITHUB_TOKEN`. It snapshots each child workflow's latest run ID before dispatch, filters post-start candidates and fails closed on ambiguity or non-success conclusions. The dispatch token's actual scope/validity is not yet proven; a successful corrected controller run must demonstrate the token can read run metadata and dispatch all three child workflows.

Agent provider keys remain separately bound to `GEMINI_API_KEY`, `GEMINI_API_KEY_2`, and `GEMINI_API_KEY_3`. Never expose secret values. Successful child run status alone is not acceptance: inspect job steps, tool-call evidence, artifacts, and resulting Draft PRs. Do not auto-merge agent output.

## Next bounded step

Wait for PR #411's exact-head CI to finish, reread the file and SHA, integrate only if checks remain green, then dispatch one controlled batch through the GitHub-hosted controller with `confirm=yes`. Record controller run ID, three exact child run IDs, jobs, conclusions, artifacts and Draft PR links. If the token is rejected or the controller fails, fix the GitHub secret scope/permissions or controller and retry only after diagnosing the failure.


## Runtime dispatch — 2026-10-20 08:54 UTC

The corrected controller was manually dispatched on `main` and is running on GitHub-hosted Actions:

- Controller run [39396582084](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39396582084), job [118540718853](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39396582084/job/118540718853). The `Dispatch the three fixed-scope agents` step completed SUCCESS. This proves the controller was able to use `MEDIAHUB_GITHUB_TOKEN` for the API calls needed to dispatch the three workflows; no token value was exposed.
- Agent 1 run [39396593650](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39396593650), job 118540757771: SUCCESS. Draft/working output PR [#413](https://github.com/VlDMlNSh/mediahub-os/pull/413) exists.
- Agent 2 run [39396596067](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39396596067), job 118540763883: IN_PROGRESS at the last read; Gemini CLI step still running.
- Agent 3 run [39396598015](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39396598015), job 118540769364: SUCCESS. Draft PR [#414](https://github.com/VlDMlNSh/mediahub-os/pull/414) exists.
- The controller is still monitoring the child runs. Its final conclusion is not yet available; do not call the batch fully successful until the controller and Agent 2 reach terminal states.
- Prior API rejection was HTTP 422 on the unquoted choice input. The corrective change was merged in PR [#411](https://github.com/VlDMlNSh/mediahub-os/pull/411), merge commit `7d86e852bf5837bc7dcf650327b22c1b27886efa`. The corrected workflow was reread from `main` and showed quoted string values.

The map file remains unreadable through the GitHub Contents wrapper (empty content despite known blob SHA), so it was not overwritten. This report is on the canonical documentation branch.
