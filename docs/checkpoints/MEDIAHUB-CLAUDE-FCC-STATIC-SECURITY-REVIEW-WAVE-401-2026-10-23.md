# MediaHub GitHub-hosted FCC Claude static security review — Wave 401

Date: 2026-10-23

## Scope and target

Review target: [Draft PR #502](https://github.com/VlDMlNSh/mediahub-os/pull/502), head `0a4ccf0e95efb5cc134eedb62dd2f9c175a24e20`.

- Workflow: `.github/workflows/mediahub-fcc-free-claude-worker.yml`
- Workflow blob SHA: `4135c78643e66c6998acb44ec1ae17750bcf0d63`
- Contract test blob SHA: `e24a339ecd846afab8cc700eba97a22307161716`
- FCC source commit: `3d2ae2306752dbdf504714a5489bcfcf69b2d04a`
- Review discussion: [PR #502 Wave 401 findings](https://github.com/VlDMlNSh/mediahub-os/pull/502#issuecomment-6354339535)

This was a bounded static source/config review. It is not a formal independent approval, live provider test, merge authorization, or Contour A qualification.

## Verified evidence

1. PR #502 is OPEN / DRAFT / UNMERGED. Base SHA: `3b054cc8fac38d2fbd58305e9d185d307c6a18bf`; head SHA: `0a4ccf0e95efb5cc134eedb62dd2f9c175a24e20`.
2. Exact-head FCC install smoke run [39876277682](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39876277682), job [120162541784](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39876277682/job/120162541784), completed SUCCESS. It pinned FCC source, installed locked dependencies and checked the CLI entry points. No provider/model request was made.
3. Exact-head related runs [Astra Verify 39876277673](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39876277673) and [Astra Cloud Runtime Validation 39876277731](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39876277731) completed SUCCESS. These results do not substitute for a live inference test or a formal independent review.
4. Formal review submissions for PR #502 are empty.
5. FCC's pinned `pyproject.toml` declares `fcc-server` and `fcc-claude` entry points. The pinned README documents `open_router/openrouter/free` as an example. The router selects from available free models; it does not guarantee a stable model ID or guarantee Qwen.
6. The workflow does not map `ANTHROPIC_API_KEY`, unsets `ANTHROPIC_API_KEY` and `MODEL_FALLBACKS`, pins the FCC source, disables checkout credential persistence and grants the worker `contents: read`.

## Blocking findings

### F1 — Model provenance is incomplete

The workflow uploads response text and a repository patch but does not record the actual upstream model/provider selected by `openrouter/free`, response usage or a provider request identifier. Therefore it cannot prove which model answered. A Qwen-specific acceptance criterion cannot be met by the dynamic router alone.

### F2 — Repository data scope is broad

Claude Code has `Read`, `Glob`, and `Grep` tools over the checked-out repository without an explicit sensitive-path denylist or task-path allowlist. A credential or restricted-data file committed to the repository could be sent to the external model provider as context.

### F3 — Artifact scanning is incomplete

The workflow scans the text result for credential-like patterns but does not scan the generated patch artifact. Both outputs must be scanned and the artifact set rejected if either fails.

### F4 — Effective no-fallback configuration is not proven

The worker unsets `MODEL_FALLBACKS`, but the workflow does not record an effective FCC configuration assertion or a negative test proving that an alternate configuration source cannot restore fallbacks. The runtime should clear alternate config-path overrides and fail closed if a fallback list is effective.

### F5 — Live dispatch is not authorized or available on this draft

The workflow is not on the default branch, the PR remains draft/unmerged, and no formal review is recorded. Do not merge merely to unlock `workflow_dispatch`. Resolve the findings, obtain independent review, and recheck exact-head CI before considering a live request.

## Disposition

- FCC install smoke: **SUCCEEDED**
- Static source/config review: **PARTIAL**
- Model inference: **NOT RUN**
- Actual model provenance: **NOT VERIFIED**
- No-paid-fallback qualification: **NOT VERIFIED**
- Formal independent review: **NOT VERIFIED**
- Live dispatch: **BLOCKED**
- Contour A: **NOT ACCEPTED**

No secret values were read. No provider inference, paid route, merge, deployment or production action occurred.

## Next step

Fix F1–F4 on the PR branch, add negative tests, run exact-head CI, then request an independent security review. Only after those gates pass should the owner authorize one bounded free-route inference test. The first live test should be a no-write prompt against an exact approved repository SHA; do not treat a successful install smoke as inference evidence.

Canonical map: [MEDIAHUB-CHAT-TREE-MAP.md](../architecture/MEDIAHUB-CHAT-TREE-MAP.md)
