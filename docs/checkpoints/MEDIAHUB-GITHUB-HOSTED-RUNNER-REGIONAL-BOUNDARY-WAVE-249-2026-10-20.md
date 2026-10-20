# Wave 249 — GitHub-hosted workflow regional boundary review

- Date: 2026-10-20
- Status: **REGIONAL EXECUTION PATH CLARIFIED; PROVIDER ACCESS NOT QUALIFIED; CONTOUR A NOT PROVEN / BLOCKED**
- Repository: https://github.com/VlDMlNSh/mediahub-os
- Canonical documentation branch: `docs/mediahub-chat-tree-map-20261012`
- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
- Checkpoint: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/checkpoints/mediahub-next-continuation-checkpoint-2026-10-12-current.md
- Master Roadmap: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/checkpoints/MEDIAHUB-MASTER-DEVELOPMENT-ROADMAP-1.0.md
- Issue #301: https://github.com/VlDMlNSh/mediahub-os/issues/301

## 1. Current refs and source snapshot

- `main`: `1324f2f9e558a99c1d3e06eb9d955c0827214fe2`.
- Canonical docs branch before this report: `743db51e7e50f7e8f752c26ac01c385499da2e32`.
- Canonical map blob before this update: `f8acca1b811f44d2d322833f55a51e3d192faadd` (1,157,410 bytes; full blob retrieved because Contents wrapper returned an empty body).
- Checkpoint blob before this update: `65d860e6cbaa6f4d544deedc6cad3393dababcd9` (867,863 bytes).
- Master Roadmap blob: `beef785c787702dc174cf9a5515bac8c9f4b292f`.
- No branch merge/rebase, deployment, secret read, or new Gemini dispatch was performed.
- The latest observed workflow run in the recent Actions list was Astra chat control run `39386506274`, event `issue_comment`, conclusion `skipped`; this is not a Gemini run and not a successful dispatch.
- A1/A2/A3 workflow source SHAs remain `09523d809530ae5b7bf528eab5fa53bc5deaf92d`, `259c8c82b8d90a39e1c90e65390e469b241b5581`, and `91b5397001e088dfae2f450ee77c9c23118b5601`. Each uses `runs-on: ubuntu-latest`, separate Gemini API secret names, and the workflow job's `github.token` for the limited GitHub MCP tool server.

## 2. Answer: did GitHub App remove the geographic launch point?

**No. It moved the control-plane entry point, not every network request.**

The architecture has at least three distinct network locations:

1. **Dispatch caller → GitHub API.** If a GitHub App/connector sends `workflow_dispatch`, the HTTPS request originates from the App integration's service or the host running its client. It is no longer necessarily the Russian server. GitHub records the event, repository, actor and run; the API call's source network is a separate concern.
2. **GitHub Actions runner → model provider.** The A1/A2/A3 workflows currently specify `runs-on: ubuntu-latest`. Therefore the model CLI executes on a GitHub-hosted runner, not on the Russian server. The Gemini API request originates from the runner's network egress. With a standard hosted-runner label, the workflow source does not pin a specific country/region or a fixed egress IP. The actual runner/egress location for a given run was not measured in this pass.
3. **Runner → other services.** Git clone, package downloads, artifact storage, and any external APIs have their own endpoints, network routes, and access controls. They do not inherit one universal “GitHub location.”

GitHub's documentation distinguishes the trigger mechanism from the runner: a workflow must declare `workflow_dispatch` and can be started through the Actions UI, GitHub CLI or REST API; the job machine is separately selected through `jobs.<job_id>.runs-on`. Standard GitHub-hosted runner labels select a class of fresh VM, not a guaranteed geographic egress location. Larger-runner options and static-IP features are separate plan/configuration features; they should not be assumed available or configured in this repository.

## 3. Regional restrictions are not erased

The Google AI Studio / Gemini API availability documentation lists supported countries and territories, and its Additional Terms restrict use to available regions. Lithuania is listed in the published availability list; Russia is not listed. That makes moving the API caller from a Russia-hosted machine to a GitHub-hosted runner a plausible reason a previous network-region failure may no longer occur, but it is **not** proof that the particular Gemini API account, key, model, billing setup, or run is accepted. Account eligibility, provider terms, API quotas, identity/age requirements, service policies, and actual request path can still block access.

Do not treat this as a mechanism to evade provider restrictions. Use only an actually supported execution region and account arrangement, and qualify it with a real successful provider request plus source/run evidence. No VPN, proxy, fabricated region, or location-masking configuration was introduced.

## 4. What is proven versus unknown

**Proven from repository source:**
- A1/A2/A3 use GitHub-hosted `ubuntu-latest` runners.
- The workflows invoke the Gemini CLI action and provide separate `GEMINI_API_KEY`, `GEMINI_API_KEY_2`, and `GEMINI_API_KEY_3` secret references.
- The workflows pass the job-scoped `github.token` to an allowlisted GitHub MCP server; `persist-credentials: false` on checkout does not remove that explicit token path.
- `workflow_dispatch` is the intended event for these workflows, but this pass did not dispatch them.

**Not proven:**
- The physical region or public egress IP of any particular runner.
- The validity/eligibility of any Gemini secret or account, or whether a real Gemini request would succeed.
- Successful A1/A2/A3 execution, completed agent tasks, resulting PR quality, or qualification of the full Contour A.
- A GitHub App installation being the actual caller of the previous successful temporary PAT smoke dispatch. The recorded smoke test proves the classic PAT request returned HTTP 204 and the temporary target run succeeded; it does not by itself prove that a GitHub App initiated it.

## 5. Recommended qualification test

For one bounded, authorized run, record the workflow/run ID, `github.event_name`, runner type, `RUNNER_ENVIRONMENT`, runner OS/architecture, and a successful minimal Gemini API response status without logging the key or sensitive payload. Record only coarse region evidence needed for compliance; do not publish secret material or unnecessary precise network data. Confirm the provider's account/region terms before using the route. Repeat independently for A1/A2/A3 only after the first test and governance gate pass.

Keep the security workstream separate: worker-side Git publication and missing issuer/capability/expiry/revocation/replay validation remain unresolved. The GitHub App is an identity/authorization mechanism, not proof of a trusted issuer, isolated runner, or independent artifact publisher.

## 6. Next action and disposition

1. Confirm the actual dispatch actor/path and use an authorized supported dispatch method.
2. Run one minimal provider connectivity qualification on GitHub-hosted infrastructure, collecting only non-secret evidence.
3. If successful and permitted, run A1/A2/A3 with distinct bounded tasks, capture exact run IDs, review PR diffs and exact-head checks, and leave PRs Draft until governance gates pass.
4. Continue issuer/capability and artifact-only worker/publisher work independently.

**Contour A remains NOT PROVEN / BLOCKED. Contour B remains gated on Contour A deployment and independent acceptance.**
