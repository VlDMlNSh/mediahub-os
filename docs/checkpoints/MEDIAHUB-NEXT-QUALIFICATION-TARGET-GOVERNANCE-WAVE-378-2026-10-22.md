# MediaHub OS — Wave 378: qualification target/governance reconciliation

- Date: 2026-10-22
- Scope: cloud-only, read-only contract and workflow evidence reconciliation. No server command was executed in this wave.
- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
- Canonical documentation branch: `docs/mediahub-chat-tree-map-20261012`
- Main SHA last confirmed by source-bound search and PR #458 merge evidence: `11d04d2f2687e9ba9215e4b67af2e450516960bb`
- Governing issue: https://github.com/VlDMlNSh/mediahub-os/issues/301
- User operational boundary from master context: work only with third server `Voktors-Mini.Dlink`; do not require owner actions on `mh-dev-01`; do not route Gemini through server 3.

## 1. Rechecked controller and Gemini execution evidence

Controller run [39794516227](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39794516227) jobs were re-read:
- admission job 119885145866 — `completed / success`
- `dispatch_and_monitor` job 119885198704 — `completed / success`
- probe/assert jobs were skipped in that agents-mode run.

All three child task/preflight jobs were re-read:
- [Agent 1 run 39796606536](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39796606536): HMAC job 119885265759 and task job 119885322228 both `completed / success`.
- [Agent 2 run 39796609924](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39796609924): HMAC job 119885277345 and task job 119885337195 both `completed / success`.
- [Agent 3 run 39796613574](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39796613574): HMAC job 119885301867 and task job 119885352702 both `completed / success`.

Artifact endpoints were re-read. Three `gemini-output` artifacts remain unexpired:
- Artifact 12434585216, digest `sha256:96a1bdfce9bff0becb5f5687dd49a56198ea98e34bd45b5a62653f65ccf32010`.
- Artifact 12433742517, digest `sha256:067a30ce8519cd076da4c2ddeb75c33fbedd82637ed15d77c609eb799076dbc2`.
- Artifact 12432709691, digest `sha256:145b28b740200b551dab039a9a069dab1f06d2663e85fdba38e3104c9489a6d9`.

These runs target historical SHA `b33ab31674bfa9595a8f2ba5a570dbc1eb3686b2`, not current main. This is execution/artifact evidence only; no new Gemini dispatch occurred and semantic verification/acceptance remains open.

## 2. FreeLLMAPI qualification — exact contract

Current main workflow `.github/workflows/freellmapi-qualification.yml`, blob SHA `708ddeffc4664fd03f5ca6475a117348cf3666dc`, specifies:
- `runs-on: [self-hosted, linux, x64, mediahub-control]`.
- Runtime assertions: `hostname == mh-dev-01` and `id -un == mediahub-runner`.
- Requires configured key-file existence, runs adapter tests, queries `/models`, and performs bounded live inference with exact marker `MEDIAHUB_FREELLMAPI_LIVE_OK`.

Canonical runner contract `control/qualification/canonical-runner-contract.json`, blob SHA `32ec7bbe371b1cfd3f2f46019ee1d2671980aa26`, specifies node `mh-dev-01`, Linux/x64, user `mediahub-runner`, and mandatory hostname/user checks.

Distributed runner contract `control/qualification/distributed-runner-contract.json`, blob SHA `993f51f07c7937165ffb3bfbe59cd0801ea71ec0`, identifies the third server as non-authoritative macOS/ARM64 with label `astra-control`; it is not a canonical replacement for `mh-dev-01`.

Fresh query of FreeLLMAPI run [39797189239](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39797189239) again returned empty jobs and empty artifacts. Status remains `PENDING / NOT VERIFIED`; this does not prove failure or identify the runner as the sole cause.

## 3. User scope versus canonical target: explicit governance conflict

The operational boundary says work only with `Voktors-Mini.Dlink`. The accepted qualification contract requires `mh-dev-01` with Linux/x64 identity, and the third server's own runner is macOS/ARM64/`astra-control`. These cannot be reconciled by relabeling, editing host assertions, running the qualification on the third server, or treating its runner as equivalent.

A contract change would alter target identity and possibly authority/security boundaries. This evidence pass does **not** authorize that change. Required disposition: preserve the current fail-closed contract and treat FreeLLMAPI qualification as `BLOCKED / NOT VERIFIED` until a formally approved contract/governance decision establishes an allowed execution target and its runtime identity. No owner action on `mh-dev-01` is requested.

## 4. Autonomous supervisor and current PR evidence

- [Astra autonomous queue supervisor run 39806527991](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39806527991) was rechecked. Its only returned job, 119921113939 (`Prepare and sign authoritative Astra command`), is still `queued`. No job logs or artifacts were available. This is not a successful supervisor qualification.
- [PR #458](https://github.com/VlDMlNSh/mediahub-os/pull/458) is merged. Astra Verify run [39797189267](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39797189267), job 119887360499, was re-read as `completed / success`, including compile, cloud admission unit tests and signed-command smoke test. This is not proof of full Contour A acceptance.
- [PR #474](https://github.com/VlDMlNSh/mediahub-os/pull/474), [#475](https://github.com/VlDMlNSh/mediahub-os/pull/475), and [#473](https://github.com/VlDMlNSh/mediahub-os/pull/473) remain reported open by the current PR connector. Formal review lists for #474/#475 and combined status for #475 returned empty arrays; exact-head CI/review are `NOT VERIFIED`, not PASS.
- Candidate PRs #467–#469 and report PRs #470–#473 are not merged based on the evidence gathered here; no PR was merged in this wave.
- Bootstrap, canonical map, canonical checkpoint, Master Roadmap, Issue #301 and controller source were queried. The map endpoint returned its blob SHA `ba5731256321251b6a92b35d51f5bd0f2c1d4e86` but no body in that response; do not infer the full map contents from an empty response.

## 5. Disposition and next step

- Gemini controller/child execution: `SUCCEEDED` at workflow/job level; artifacts exist; semantic verification `NOT VERIFIED`.
- FreeLLMAPI live qualification: `BLOCKED / NOT VERIFIED` due to no jobs/artifacts and a target-contract/operational-scope conflict.
- Astra supervisor run 39806527991: `RUNNING/QUEUED` at job level; qualification outcome `NOT VERIFIED`.
- PR #473–#475 exact-head CI/review: `NOT VERIFIED`.
- Contour A: `NOT QUALIFIED / NOT ACCEPTED`; Contour B remains gated.

Next bounded action: inspect the queued supervisor job's status again and read its exact job logs only after it leaves queued; in parallel, continue source-only analysis of how a governed qualification target decision can be represented without weakening existing runtime identity assertions. Do not start Gemini, reroute through server 3, change labels, operate another host, read secrets, merge PRs, deploy, or claim qualification in the absence of explicit contract approval and evidence.
