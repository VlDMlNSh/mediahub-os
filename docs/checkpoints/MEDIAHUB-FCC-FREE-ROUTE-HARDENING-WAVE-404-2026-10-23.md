# Wave 404 — FCC free-route hardening and live-test gate recheck (2026-10-23)

## Executive disposition

- Provider selection: OpenRouter `openrouter/free` remains the first candidate for a bounded smoke because the existing catalog-auth probe succeeded and the router is documented as selecting only free variants. It is a dynamic model router, not Anthropic Claude, and does not guarantee Qwen or any fixed model.
- Account-specific free quota and remaining allowance: **NOT CHECKED**. Secret names and their creation timestamps do not expose quota balances.
- Workflow implementation: **HARDENED IN PR #502**, but still **OPEN/DRAFT/UNMERGED**.
- Exact-head worker CI: **RUNNING** at review time; Astra Verify and Astra Cloud Runtime Validation succeeded. Overall exact-head CI: **NOT VERIFIED** until the worker workflow run terminates.
- Live inference / provider calls in this wave: **NOT RUN**. No secret values read. No paid provider route used. Contour A remains **NOT ACCEPTED**.

## Source and provenance

- `main` HEAD observed: `3b054cc8fac38d2fbd58305e9d185d307c6a18bf`.
- Canonical docs branch HEAD observed: `4d8c15f3f608b982f429cc8965358b623057255a`.
- FCC worker PR: https://github.com/VlDMlNSh/mediahub-os/pull/502
- PR head: `61c266f565c3ef2fbf49e91217cc1e4650f1bdb8`.
- Workflow blob SHA: `64a5f154d86884bb8b0356d8999cbb9ce4b1db95`.
- Contract-test blob SHA: `32fa070a9d7ac9727ff1f71b3ad07d93d61e230e`.
- FCC upstream pinned commit: `3d2ae2306752dbdf504714a5489bcfcf69b2d04a`.
- FCC `pyproject.toml` blob at pinned commit: `6b252ac571681a37f635f1f3e9c36fb72dacc5ba`; confirms `fcc-server` and `fcc-claude` entry points.
- Existing OpenRouter catalog authentication probe: https://github.com/VlDMlNSh/mediahub-os/actions/runs/39847014875 — HTTP 200 for catalog GET only, not inference or quota telemetry.

## Changes in this pass

- Changed the CLI's allowed tool list from `Read,Glob,Grep,Edit,Write` to `Read,Glob,Grep`.
- Changed Claude Code permission mode from `acceptEdits` to `plan`.
- Narrowed the system prompt to a read-only smoke summary and added a regression assertion in `tests/test_mediahub_fcc_free_claude_workflow_contract.py`.
- Re-read both changed files from GitHub and verified their current blob SHAs above.

These changes reduce write capability, but **do not fully close the sensitive-file-scope finding**: the target repository is still checked out and readable by the model. The worker also still emits a patch artifact and scans the result text but not the patch. Those remain blockers for live dispatch.

## Exact-head CI

- FCC worker run: https://github.com/VlDMlNSh/mediahub-os/actions/runs/39878880575 — **IN_PROGRESS** at the last check.
- Astra Verify: https://github.com/VlDMlNSh/mediahub-os/actions/runs/39878880582 — **SUCCEEDED**.
- Astra Cloud Runtime Validation: https://github.com/VlDMlNSh/mediahub-os/actions/runs/39878880584 — **SUCCEEDED**.
- Combined status endpoint returned no status rows; empty results are not a PASS.
- Since the FCC worker run had not completed, exact-head CI remains **NOT VERIFIED**.

## Remaining security blockers before live inference

1. **Actual model provenance:** capture the actual upstream model/provider and a request identifier or equivalent evidence. `openrouter/free` is dynamic; do not claim the selected model is Qwen or Anthropic Claude without evidence.
2. **Data scope:** run the initial connectivity smoke in an empty temporary workspace or a strict allowlisted snapshot, not with read access to the full repository.
3. **Artifact handling:** omit unnecessary patch artifacts for a read-only smoke, or scan every artifact before upload; reject evidence on any credential-like match.
4. **Effective no-fallback:** isolate FCC config under a fresh temporary home, explicitly unset fallback configuration, and add a negative contract test showing no fallback list is loaded.
5. **Default-branch gate:** GitHub's `workflow_dispatch` requires the workflow to exist on the default branch. Do not merge solely to unlock dispatch; obtain independent review and green exact-head CI first.

## Free-quota assessment

Published provider policies are ceilings/baselines, not proof of this account's remaining quota:

- **OpenRouter** — free router and free-model pool; published free-account limits are 20 requests/minute and 50 requests/day. Dynamic model availability; not a production SLA.
- **Groq** — free-plan limits vary by model and organization; inspect the account's Limits page and response headers before admission.
- **Cloudflare Workers AI** — Free allocation published as 10,000 Neurons/day, reset at 00:00 UTC; some models require paid entitlement.
- **Gemini API** — eligible models have free-tier quotas, but limits are model/project-specific. Multiple keys may share a project quota.
- **Mistral** — Free mode exists with low evaluation limits.
- **Hugging Face Inference Providers** — published Free user credit is $0.10/month, subject to change; unsuitable as a durable coding-agent pool.
- **SambaNova** — current plan page describes a Free onboarding path that requires a payment method and credits for requests; do not assume no-spend inference.
- **DeepSeek, Kimi, Novita, Z.ai, SiliconFlow, LLM7, Nara, Orca, MiMo and UnoRouter** — the names of configured secrets do not prove persistent free inference or no-paid-fallback behavior; keep unqualified until provider-specific terms and bounded probes establish it.

Official references:
- https://openrouter.ai/pricing
- https://openrouter.ai/openrouter/free
- https://console.groq.com/docs/rate-limits
- https://ai.google.dev/gemini-api/docs/rate-limits
- https://developers.cloudflare.com/workers-ai/platform/pricing/
- https://docs.mistral.ai/getting-started/quickstarts/studio/activate-and-generate-api-key
- https://huggingface.co/docs/inference-providers/pricing
- https://cloud.sambanova.ai/plans

## Next action

Finish F1–F4 on PR #502, wait for exact-head CI to finish, and obtain an independent security review. Only then may the bounded live smoke be run through the default-branch workflow with `confirm=true`, `MEDIAHUB_ALLOW_FCC_FREE_CLAUDE=true`, and the already configured `OPENROUTER_API_KEY` secret. Do not read or expose the secret value. No automatic provider fallback is authorized.

Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
