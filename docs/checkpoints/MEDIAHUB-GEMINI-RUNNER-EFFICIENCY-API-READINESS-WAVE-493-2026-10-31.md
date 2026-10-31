# Wave 493 — Gemini runner efficiency and provider credential readiness (2026-10-31)

## Status

**SOURCE AUDIT COMPLETE / OPTIMIZATION PROPOSAL RECORDED / NO WORKFLOW CHANGE / NO CREDENTIAL OR PROVIDER ACTION.**

## Immutable documentation baseline

- Canonical documentation base: `docs/mediahub-chat-tree-map-20261012` at `bfb2a6d73ba64839e783d6ee30d0d8ae2e3074a4`.
- Main runtime snapshot referenced by the latest adjacent waves: `f0448f28c7cfa61e4450c38529f09afbfdbbc7c7`.
- Gemini controller blob on main: `0a1246f6755020faf8b7e48d07bfff790bbaece3`.
- Agent 1 workflow blob: `155a02159912ca371e6f826c51325ca269857aad`.
- Agent 2 workflow blob: `fff1820a6b97d379b23674f36bd62227b7d4dec2`.
- Agent 3 workflow blob: `781df56e8aa7c75ba453c08378611857862b2e44`.
- Router policy blob: `e249333c1c0ce6c1c586a5f498dbfd3979418f6e`.
- FCC/OpenRouter worker blob: `384eee5209d2ec129ff2d0e92e953d3cad0fa863`.
- Issue [#301](https://github.com/VlDMlNSh/mediahub-os/issues/301) remains OPEN and governs Contour A gates.

## 1. Verified current execution topology

The three Gemini roles are dispatched by `.github/workflows/gemini-batch-dispatch-controller.yml` as three distinct GitHub Actions workflow runs. Each child workflow currently declares `runs-on: ubuntu-latest` for both its authorization job and its model-execution job. The three workflows therefore use GitHub-hosted ephemeral runner instances; they do not consume or target the owner's 20 physical computers.

The current topology is:
- Agent 1: `gemini-autonomous-engineering.yml`; `GEMINI_API_KEY`.
- Agent 2: `gemini-agent-2.yml`; `GEMINI_API_KEY_2`.
- Agent 3: `gemini-agent-3.yml`; `GEMINI_API_KEY_3`.

Each child has an authorization job followed by a separate execution job. These are separate GitHub Actions jobs and therefore separate runner allocations. Controller POST requests are made for the three child workflows; their runs can overlap. The current Agent 2 prompt explicitly says not to claim review of Agent 1 changes created concurrently in the same batch. Thus parallel dispatch currently weakens the value of downstream verification: the reviewer may not have a completed implementation PR to inspect.

The controller uses `ubuntu-latest` for its own admission/dispatch job as well. No workflow inspected in this pass routes these Gemini child jobs to a physical owner-managed runner label.

## 2. Runner efficiency decision

**Recommended next design: preserve three distinct roles and credentials boundaries, but make the orchestration dependency-aware and sequential.**

1. Agent 1 produces one bounded implementation/evidence PR.
2. Agent 2 receives the exact resulting PR number, base SHA and head SHA and performs a read-only contract/test review of that immutable diff.
3. Agent 3 receives the same immutable PR diff and performs a read-only security/provenance audit.
4. The controller records all run/job IDs, terminal states and artifact digests. Missing results remain NOT VERIFIED.

Benefits:
- Verification is performed against a completed, immutable implementation result.
- Peak concurrent runner demand is reduced.
- Independent roles remain distinct.
- The controller can stop subsequent steps when Agent 1 fails or creates no valid PR.

Cost qualification:
- Sequential dispatch reduces peak concurrency, not necessarily total GitHub Actions billed minutes.
- A single job with three sequential model sessions could reduce runner startup/authorization overhead, but would share one runner filesystem/process boundary. It is **not selected** until separate clean workspaces, session isolation, credential minimization, artifact handoff and failure recovery are specified and tested.
- Do not force the three agents onto one persistent physical self-hosted runner merely to reduce concurrency.
- Do not create three duplicate API keys or accounts to multiply provider quota. Provider quota is governed by the provider's account/project/entitlement rules, not the number of MediaHub roles.

Before changing the controller, prepare a source-bound design and negative tests for dispatch ordering, immutable PR binding, duplicate/replay suppression, stop-on-failure, exact run-ID reconciliation, credential scope, cancellation and partial completion. Keep the existing controller gates fail-closed.

## 3. Classification of the 20 computers

The phrase "computer is a GitHub runner" must be distinguished technically:
- GitHub-hosted runner: a temporary GitHub-managed VM selected by labels such as `ubuntu-latest`.
- Self-hosted runner: a physical/virtual machine owned or administered by the project and registered with GitHub Actions.

The current MediaHub Gemini workflows use the first type. If the 20 computers are registered self-hosted runners, they are a separate capacity pool and are not used by the inspected Gemini workflows.

The repository is public. GitHub's security guidance warns that self-hosted runners can be persistently compromised by untrusted workflow code and should almost never be used for public repositories. Therefore, do not route untrusted PR/model-agent work to persistent owner-managed machines. Any future use of the 20 machines requires separate runner groups, strict repository/workflow allowlists, one-job ephemeral/JIT provisioning, clean-state destruction, network/secret isolation and a separately accepted target manifest. Hardware inventory and runner identity are still required before assignment.

## 4. Exact credential references found in source

### Gemini controller and children

- Secrets: `MEDIAHUB_GITHUB_TOKEN`, `MEDIAHUB_DISPATCH_HMAC_KEY`, `GEMINI_API_KEY`, `GEMINI_API_KEY_2`, `GEMINI_API_KEY_3`.
- Variable: `MEDIAHUB_GEMINI_BATCH_ENABLED`.
- Optional model variable: `GEMINI_MODEL` (workflow default is `gemini-3.5-flash-lite`).
- Presence, value, scope and permission metadata for these repository secrets/variables were **NOT VERIFIED**. No secret values were read.

### FCC/OpenRouter Free worker

- Secret: `OPENROUTER_API_KEY`.
- Variable: `MEDIAHUB_ALLOW_FCC_FREE_CLAUDE`.
- The workflow explicitly checks for `OPENROUTER_API_KEY` and requires the enable variable to equal `true` before dispatch. The provider response's actual model ID is checked for the `:free` suffix; the route name does not prove the actual model is Claude.
- No `ANTHROPIC_API_KEY` is required by this worker; its smoke test explicitly requires it to be absent. Do not create an Anthropic direct-provider route for this workflow.

### Classification

- `MEDIAHUB_GITHUB_TOKEN`: GitHub API credential used only by the controller; not an LLM provider key. Its exact fine-grained permissions must be verified before creating/replacing it.
- `MEDIAHUB_DISPATCH_HMAC_KEY`: controller signing secret; not a provider key.
- Gemini secrets: current child workflow references. Do not rename them, create aliases, or populate all three with copied values without a reviewed contract change.
- `OPENROUTER_API_KEY`: provider key for the already admitted FCC/OpenRouter Free workflow.
- `MEDIAHUB_GEMINI_BATCH_ENABLED` and `MEDIAHUB_ALLOW_FCC_FREE_CLAUDE`: repository variables, not secrets.
- No additional provider/gateway key is currently authorized by `.github/ai/model-router.yml`. LiteLLM and Bifrost remain research candidates only.

## 5. Registration and management links

These links are registration/management entry points, not authorization to enable billing or dispatch:

- Google AI Studio / Gemini API keys: https://aistudio.google.com/apikey
- Gemini API key and authentication documentation: https://ai.google.dev/gemini-api/docs/api-key
- Gemini API free/paid tiers and billing controls: https://ai.google.dev/gemini-api/docs/billing
- OpenRouter account/API keys: https://openrouter.ai/settings/keys
- OpenRouter developer onboarding: https://openrouter.ai/developers
- GitHub fine-grained personal access token management: https://github.com/settings/personal-access-tokens
- GitHub Actions repository secrets/variables: https://github.com/VlDMlNSh/mediahub-os/settings/secrets/actions
- GitHub Actions secret handling documentation: https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/use-secrets

Only Gemini and OpenRouter are external model-provider key families in the currently admitted cloud routes. Do not register Anthropic, LiteLLM, Bifrost, Groq, Cerebras or other providers for MediaHub at this stage: they are not admitted by the current router policy. GitHub PAT and HMAC are separate infrastructure credentials, not model API keys.

Google's current documentation states that AI Studio creates a project/key for new users and that paid tiers require billing setup; free-tier availability and limits depend on model/project/account. Do not enable billing, purchase credits or configure a paid fallback as part of this pass. Review account eligibility and provider terms before any account creation. Never paste keys into chat, commits, issue comments, prompts or artifacts.

## 6. Controller gate and execution status

The controller source requires:
- `MEDIAHUB_GEMINI_BATCH_ENABLED=true`;
- `MEDIAHUB_GITHUB_TOKEN` and `MEDIAHUB_DISPATCH_HMAC_KEY`;
- trusted `main` ref and exact immutable target SHA;
- signed child dispatch payloads.

The controller/Bootstrap additionally require exact-main CI, independent security review, effective secret/variable presence and scope, effective branch governance and a successful trusted-main no-secret probe before live agent dispatch. Issue #301 A0/R-06, runner-target, schema and independent-review gates remain controlling.

No controller run, Gemini child run, provider call, secret read, credential creation, billing change, workflow change, self-hosted runner registration, merge, deployment, qualification or acceptance occurred in this pass. Agent dispatch is **NOT RUN**; credentials metadata is **NOT VERIFIED**; Contour A remains **NOT ACCEPTED**.

## 7. Next bounded engineering step

Prepare a documentation-backed controller optimization proposal with:
- sequential Agent 1 → Agent 2 → Agent 3 dispatch;
- exact PR/base/head SHA handoff;
- per-role immutable task envelope and independent evidence;
- stop-on-failure and partial-result reconciliation;
- explicit compute-minute versus peak-concurrency accounting;
- no use of the 20 physical machines until their runner type and trust boundary are accepted.

Then run source-bound tests and independent A3 review. Do not dispatch Gemini until all existing gates pass.

## Sources

- [Gemini controller](https://github.com/VlDMlNSh/mediahub-os/blob/main/.github/workflows/gemini-batch-dispatch-controller.yml)
- [Agent 1 workflow](https://github.com/VlDMlNSh/mediahub-os/blob/main/.github/workflows/gemini-autonomous-engineering.yml)
- [Agent 2 workflow](https://github.com/VlDMlNSh/mediahub-os/blob/main/.github/workflows/gemini-agent-2.yml)
- [Agent 3 workflow](https://github.com/VlDMlNSh/mediahub-os/blob/main/.github/workflows/gemini-agent-3.yml)
- [Router policy](https://github.com/VlDMlNSh/mediahub-os/blob/main/.github/ai/model-router.yml)
- [FCC/OpenRouter worker](https://github.com/VlDMlNSh/mediahub-os/blob/main/.github/workflows/mediahub-fcc-free-claude-worker.yml)
- [Issue #301](https://github.com/VlDMlNSh/mediahub-os/issues/301)
- [Canonical map](https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md)
- [Wave 492 OSS shortlist](https://github.com/VlDMlNSh/mediahub-os/pull/606)
