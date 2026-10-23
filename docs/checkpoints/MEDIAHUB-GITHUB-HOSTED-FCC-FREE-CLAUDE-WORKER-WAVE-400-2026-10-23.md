# MediaHub OS — Wave 400: GitHub-hosted FCC free-route worker implementation

Date: 2026-10-23

## Decision and disposition

**DRAFT PR CREATED / FCC INSTALL SMOKE SUCCEEDED / ALL RETURNED EXACT-HEAD CI SUCCEEDED / INDEPENDENT REVIEW NOT VERIFIED / LIVE DISPATCH NOT RUN**

A separate implementation proposal is now available in [PR #502](https://github.com/VlDMlNSh/mediahub-os/pull/502). It adds a GitHub-hosted ephemeral worker using Free Claude Code (FCC) and the OpenRouter Free Models Router, without a direct paid Anthropic credential or FCC model fallback list.

This is an implementation candidate, not an accepted or deployed route. The worker is disabled by default: live execution requires an explicit workflow input `confirm=true`, repository variable `MEDIAHUB_ALLOW_FCC_FREE_CLAUDE=true`, and repository secret `OPENROUTER_API_KEY`. The owner approval in [Issue #301 comment 6354035391](https://github.com/VlDMlNSh/mediahub-os/issues/301#issuecomment-6354035391) authorizes design/implementation only; it does not authorize dispatch, merge, deployment, or Contour A acceptance.

## Immutable target and changed files

- `main` base SHA: `3b054cc8fac38d2fbd58305e9d185d307c6a18bf`.
- Implementation branch: `contour-a/github-hosted-fcc-openrouter-free-wave400`.
- PR head SHA: `0a4ccf0e95efb5cc134eedb62dd2f9c175a24e20`.
- PR #502: OPEN / DRAFT / UNMERGED; currently mergeable according to GitHub metadata.
- `.github/workflows/mediahub-fcc-free-claude-worker.yml`, blob SHA `4135c78643e66c6998acb44ec1ae17750bcf0d63`.
- `tests/test_mediahub_fcc_free_claude_workflow_contract.py`, blob SHA `e24a339ecd846afab8cc700eba97a22307161716`.

The workflow checks out FCC at immutable upstream commit `3d2ae2306752dbdf504714a5489bcfcf69b2d04a`, uses Python `3.14.7`, installs via the pinned `uv==0.12.13` and the FCC `uv.lock`, and sets `HOST=127.0.0.1` for the ephemeral proxy. It uses GitHub-hosted `ubuntu-latest`, read-only repository permissions, a full target commit SHA, bounded prompt validation, and sanitized result/patch artifacts. It does not push or commit worker changes.

## Route evidence and limits

- Candidate FCC model identifier: `open_router/openrouter/free`.
- FCC source states the project is AGPL-3.0-only and requires Python `==3.14.7`.
- OpenRouter's official [Free Models Router documentation](https://openrouter.ai/docs/guides/routing/routers/free-router) describes `openrouter/free` as selecting among available free models and states requests routed to free models are free. The downstream model is selected dynamically and availability changes; this is not a guarantee that any specific model remains available or that its capabilities are stable.
- FCC's `MODEL_FALLBACKS` setting is explicitly unset for the live worker. The direct `ANTHROPIC_API_KEY` is explicitly unset and is never mapped from repository secrets.
- The worker requires `OPENROUTER_API_KEY`; its value was not inspected or used in this pass.
- Provider/model dispatch was not performed. Free-tier terms, account entitlement, quota state, data handling and real request behavior were not live-tested. Any quota exhaustion or provider error must remain a hard failure, not trigger a paid route.

## Exact-head verification

- GitHub-hosted FCC install smoke: [run 39876277682](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39876277682) — job `install-smoke` completed **SUCCESS**. This installed FCC from the pinned source and lockfile, checked the `fcc-server` entry point and `fcc-claude` entry point metadata, and made no provider/model call.
- Astra Cloud Runtime Validation: [run 39876277731](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39876277731) — **SUCCESS** at exact PR head.
- Astra Verify: [run 39876277673](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39876277673) — **SUCCESS** at exact PR head.
- Formal independent PR reviews: none returned at time of report.
- Live worker workflow: dispatch-gate and bounded-worker were **SKIPPED** on the pull-request run; no provider/model call, no credential value inspection, no local/self-hosted host use, no merge and no deployment.

## Status

- PR implementation: **DRAFT / OPEN**.
- FCC installation smoke: **SUCCEEDED**.
- Astra Cloud Runtime Validation: **SUCCEEDED**.
- Astra Verify: **SUCCEEDED**.
- Independent security review: **NOT VERIFIED**.
- Live Claude dispatch: **NOT RUN**.
- Route qualification: **NOT VERIFIED**.
- Contour A: **NOT ACCEPTED**.

## Next bounded step

All three returned exact-head runs are now terminal SUCCESS. Re-read both changed files and blob SHAs and obtain independent security review. Repair any findings in the same draft PR. Only after CI/review and route/data-governance admission pass should a separately authorized, bounded manual run be considered. Do not set `MEDIAHUB_ALLOW_FCC_FREE_CLAUDE=true` or dispatch the worker before those gates pass.

Canonical map: [MEDIAHUB-CHAT-TREE-MAP.md](../architecture/MEDIAHUB-CHAT-TREE-MAP.md)
