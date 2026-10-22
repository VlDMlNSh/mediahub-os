# MediaHub OS — Wave 376 runner and Gemini evidence recheck

- Date: 2026-10-22
- Scope: one bounded, read-only evidence reconciliation; this report is documentation only.
- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
- Canonical docs branch: `docs/mediahub-chat-tree-map-20261012`
- Working branch: `docs/next-wave-376-runner-and-agent-evidence-20261022`
- Last main HEAD evidenced by Wave 375: `11d04d2f2687e9ba9215e4b67af2e450516960bb`
- Governing issue: https://github.com/VlDMlNSh/mediahub-os/issues/301

## Freshly rechecked workflow evidence

### Gemini controller-owned batch

The recorded immutable target/workflow-definition SHA is `b33ab31674bfa9595a8f2ba5a570dbc1eb3686b2`, distinct from the later main SHA above.

- Parent controller run [39794516227](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39794516227): jobs `Require explicit batch admission flag` (119885145866) and `dispatch_and_monitor` (119885198704) are `completed / success`.
- Agent 1 run [39796606536](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39796606536): HMAC preflight job 119885265759 and task job 119885322228 are `completed / success`; artifact 12434585216, digest `sha256:96a1bdfce9bff0becb5f5687dd49a56198ea98e34bd45b5a62653f65ccf32010`.
- Agent 2 run [39796609924](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39796609924): HMAC preflight job 119885277345 and task job 119885337195 are `completed / success`; artifact 12433742517, digest `sha256:067a30ce8519cd076da4c2ddeb75c33fbedd82637ed15d77c609eb799076dbc2`.
- Agent 3 run [39796613574](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39796613574): HMAC preflight job 119885301867 and task job 119885352702 are `completed / success`; artifact 12432709691, digest `sha256:145b28b740200b551dab039a9a069dab1f06d2663e85fdba38e3104c9489a6d9`.
- Artifact metadata currently reports all three artifacts unexpired. These facts prove workflow/job execution and artifact presence, not semantic correctness or acceptance.
- Parent controller run has both probe jobs skipped; the two successful parent jobs above are the actual dispatch/monitor path. No new batch was dispatched in this pass.

### FreeLLMAPI Live Qualification

- Run [39797189239](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39797189239), target `11d04d2f2687e9ba9215e4b67af2e450516960bb`.
- Fresh jobs query returned an empty list; artifact query returned an empty list. No qualification step or live inference is evidenced. Status remains `PENDING / NOT VERIFIED`, not PASS and not confirmed failure.
- The Wave 375 report records required runner labels `[self-hosted, linux, x64, mediahub-control]` and runtime assertions `hostname == mh-dev-01`, `id -un == mediahub-runner`, and configured key-file existence.
- The likely runner-matching explanation is not proven: this pass had no authorized runner-inventory result. Do not change labels, relax host assertions, move the job to hosted runners, or retrieve/print provider credentials as a workaround.

## PR integration gates

Fresh connector queries returned empty combined-status arrays and zero formal reviews for:
- [PR #470](https://github.com/VlDMlNSh/mediahub-os/pull/470), head `3837d2b63ec2d79eb026f7c7220caad7d97757d8`
- [PR #471](https://github.com/VlDMlNSh/mediahub-os/pull/471), head `8b8dc798c179ea0d10503d1e1ae62b75a0a14866`
- [PR #472](https://github.com/VlDMlNSh/mediahub-os/pull/472), head `c34725d8c3e23981f4ab48993624ecbb6cda7ed6`

These limited connector results mean exact-head CI/review are `NOT VERIFIED`; they do not establish that GitHub has no checks. Do not merge these documentation PRs on this evidence alone. PR #467–#469 remain separate open agent candidate PRs whose exact-head CI, semantic review, and independent approval are unresolved.

## Disposition and next bounded action

- PR #458: merged; Wave 375 records Astra Verify run [39797189267](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39797189267) as `completed / success`. The combined-status connector itself returned an empty array in this pass, so this report relies on the recorded run evidence rather than claiming the empty status query is a pass.
- Gemini parent and all three children: `SUCCEEDED` at workflow/job level; artifacts present; semantic correctness `NOT VERIFIED`.
- FreeLLMAPI live qualification: `PENDING / NOT VERIFIED`.
- PR CI/reviews #470–#472: `NOT VERIFIED`.
- Claude/Ollama and agent-browser: `NOT RUN` in this cloud-only pass.
- Contour A: `NOT QUALIFIED / NOT ACCEPTED`; Contour B remains gated.

Next: obtain authoritative Actions runner inventory/availability for `mediahub-control` and confirm the intended `mh-dev-01` identity without changing policy; then rerun the existing approved FreeLLMAPI qualification path only when the intended runner is available. Separately review the three Gemini artifacts against immutable source/test evidence and resolve exact-head CI/reviews before integrating agent PRs.

No secrets were read or emitted. No controller dispatch, provider call, local-host command, merge, deployment, or qualification was performed in this pass.
