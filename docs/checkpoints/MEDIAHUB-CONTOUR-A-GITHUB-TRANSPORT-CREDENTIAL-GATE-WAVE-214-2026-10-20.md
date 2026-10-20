# MediaHub OS Contour A — GitHub transport credential and dispatch gate (Wave 214)

Date: 2026-10-20

Status: source re-read and GitHub PR comment recorded; no new Gemini workflow dispatch, merge, deployment, qualification or acceptance performed.

## Canonical navigation

- Canonical project map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
- Bootstrap: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CONTEXT-BOOTSTRAP-INSTRUCTION.md
- Continuation checkpoint: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/checkpoints/mediahub-next-continuation-checkpoint-2026-10-12-current.md
- Master Roadmap: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/checkpoints/MEDIAHUB-MASTER-DEVELOPMENT-ROADMAP-1.0.md
- Governing issue: https://github.com/VlDMlNSh/mediahub-os/issues/301
- Controller PR: https://github.com/VlDMlNSh/mediahub-os/pull/408
- Wave 213 report: https://github.com/VlDMlNSh/mediahub-os/blob/feat/contour-a-gemini-github-dispatch-controller-wave-213-2026-10-20/docs/checkpoints/MEDIAHUB-CONTOUR-A-GEMINI-GITHUB-TRANSPORT-WAVE-213-2026-10-20.md

## Current source read-back

Repository: VlDMlNSh/mediahub-os  
Base ref: `main` at `1324f2f9e558a99c1d3e06eb9d955c0827214fe2`  
Controller branch: `feat/contour-a-gemini-github-dispatch-controller-wave-213-2026-10-20`  
Compare: 4 commits ahead, 0 behind main.

Read-back blob SHAs:
- Controller `.github/workflows/gemini-batch-dispatch-controller.yml`: `d237e6ba7f7f7ff33caa7a47ea156c570e52a658`
- Agent 1 `.github/workflows/gemini-autonomous-engineering.yml` on main: `09523d809530ae5b7bf528eab5fa53bc5deaf92d`
- Agent 2 `.github/workflows/gemini-agent-2.yml` on main: `259c8c82b8d90a39e1c90e65390e469b241b5581`
- Agent 3 `.github/workflows/gemini-agent-3.yml` on main: `91b5397001e088dfae2f450ee77c9c23118b5601`
- Bootstrap on canonical docs branch: `4a101ab3d7ec766ccbd2d3541f84593e9a406a8b`
- Map on canonical docs branch: `ffe4e0b22f899113fe1790618dea87a36d56e959` (Contents wrapper returned empty content; do not infer that the map is empty. Use a raw/blob read before any edit.)
- Continuation checkpoint on canonical docs branch: `8d924c9bdcb6751b883c9094090dc35e18338b08`

## Credential routing

- Agent 1 references `secrets.GEMINI_API_KEY`.
- Agent 2 references `secrets.GEMINI_API_KEY_2`.
- Agent 3 references `secrets.GEMINI_API_KEY_3`.
- The child workflows provide `github.token` to the GitHub MCP server, with the job-level permissions defined in each workflow.
- The batch controller uses a short-lived `github.token` and declares controller-level `contents: read`, `actions: write` to request Actions dispatch. This is preferable to adding a long-lived PAT to the controller when repository policy allows the scoped token to work.
- The user reports adding two GitHub API secrets. Their exact secret names/scopes cannot be enumerated or validated by the available chat connector; no secret values were read, logged, copied or tested. Do not guess secret names. Keep PATs least-privilege and out of source; rotate any credential that was exposed.

## Execution evidence

Historical successful batch (not started by this session and not launched by this controller):
- Agent 1 run [39370191589](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39370191589), job 118456086050, success.
- Agent 2 run [39370202615](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39370202615), job 118456119718, success.
- Agent 3 run [39370217605](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39370217605), job 118456166571, success.

No new run IDs, artifacts or agent Draft PRs were created by Wave 214. The controller is still on a feature branch, so it is not yet available as a default-branch workflow for normal manual dispatch.

## Risk and next step

The controller currently finds runs using workflow path, `workflow_dispatch`, `main`, and creation time after the controller start timestamp. Concurrent direct dispatches could cause incorrect correlation. Before integration, improve run correlation or serialize every dispatch source, run YAML/actionlint checks, then execute a single controlled batch and verify the three exact run IDs, jobs, artifacts, and agent Draft PRs. Keep agent output untrusted and do not auto-merge.

PR #408 has a Wave 214 comment documenting these findings (comment ID 6286674187). No merge/deploy/qualification/acceptance is claimed. Contour A remains NOT_PROVEN / BLOCKED pending the project's required gates.
