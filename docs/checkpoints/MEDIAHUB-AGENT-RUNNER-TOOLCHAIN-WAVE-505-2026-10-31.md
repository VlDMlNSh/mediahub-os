# MediaHub — Agent Runner Toolchain Extension (Wave 505)

- Date: 2026-10-31
- Status: **IMPLEMENTED IN OPEN PR / PR-SCOPE CI VERIFIED / REQUIRED RULESET CONTEXTS NOT SATISFIED / RUNTIME NOT RUN / NOT QUALIFIED / NOT ACCEPTED**
- Governing issue: [Issue #301](https://github.com/VlDMlNSh/mediahub-os/issues/301)
- Canonical map target: [MEDIAHUB-CHAT-TREE-MAP.md](../architecture/MEDIAHUB-CHAT-TREE-MAP.md)
- Documentation proposal branch: `docs/wave505-agent-runner-toolchain-20261031`
- Documentation base/canonical branch SHA at creation: `d9a289b9113f7567711b641a7017eb814d6c259d`
- Code target main SHA: `f0448f28c7cfa61e4450c38529f09afbfdbbc7c7`
- Code PR: [PR #610](https://github.com/VlDMlNSh/mediahub-os/pull/610)

## 1. Objective and bounded scope

Extend the existing owner-gated Ubuntu Hosted Runner workflow so the same ephemeral runner can provision the requested coding-agent toolchain alongside the Ollama/FCC/Claude Code candidate:

1. Gemini CLI
2. mini-SWE-agent
3. Aider
4. OpenHands SDK
5. Goose

This is a toolchain-provisioning change only. It does not create two persistent virtual machines, register these tools as MediaHub A0 executors, authorize autonomous repository mutation, or perform model/provider calls.

## 2. Exact implementation evidence

PR #610 current HEAD at audit time: `8f59cc25e789796979637aab6edd7e0e98c4f511`.

- Workflow: `.github/workflows/mediahub-alamo-fcc-claude-runner.yml`
  - Blob SHA: `96d9b8a2724fe2b805c357336e20d66b86d56516`
- Contract tests: `tests/test_mediahub_alamo_fcc_runner_contract.py`
  - Blob SHA: `4c504dc99b7130572bb0c3fa38f78f5d580a390a`
- The workflow's toolchain step is gated to `workflow_dispatch`; the existing workflow additionally requires owner confirmation and exact-SHA admission.
- CLI path is exported to subsequent runner steps via `GITHUB_PATH`; the OpenHands SDK interpreter path is exported via `GITHUB_ENV`.
- The OpenHands SDK is installed in a dedicated Python 3.12 virtual environment.
- Aider and mini-SWE-agent are installed through isolated `uv tool` environments.
- Goose Linux x86_64 archive is SHA-256 checked before extraction.
- Tool versions and provider-authentication state are written to the runtime evidence manifest.

## 3. Pinned upstream source evidence

| Component | Pin | Source evidence |
|---|---:|---|
| Gemini CLI | 0.66.0 | [package.json at v0.66.0](https://github.com/google-gemini/gemini-cli/blob/v0.66.0/package.json), blob `f9deabb1b7d7690c391db516a0996577ee184553` |
| mini-SWE-agent | 2.4.6 | [pyproject.toml at v2.4.6](https://github.com/SWE-agent/mini-swe-agent/blob/v2.4.6/pyproject.toml), blob `0bd3e1329252af4399805959d78d5984f2bbf2b0` |
| Aider | 0.86.0 | [pyproject.toml at v0.86.0](https://github.com/Aider-AI/aider/blob/v0.86.0/pyproject.toml), blob `e92d278d46ff944402b2c5dd17edde5c0a6d2d2f` |
| OpenHands SDK | 1.59.0 | [openhands-sdk/pyproject.toml at v1.59.0](https://github.com/OpenHands/software-agent-sdk/blob/v1.59.0/openhands-sdk/pyproject.toml), blob `c05143c255f01f580047e838394069c7f746c580` |
| Goose | 1.57.0 | [release v1.57.0](https://github.com/aaif-goose/goose/releases/tag/v1.57.0); Linux x86_64 archive SHA-256 `10eb96cb6a159b6e1d38eeedbef6ab64cd28168aad91948f1fa5c34eefdf98e3` |

The OpenHands import surface `from openhands.sdk import LLM, Agent, Conversation` is present in the upstream SDK examples. The installer checks the import at runtime, but that runtime check has not yet been executed on the hosted runner.

## 4. Security and authority boundaries

- **Gemini CLI:** installation is inert. Bootstrap policy requires Gemini work to use the approved GitHub Actions controller transport. Direct Gemini CLI provider invocation from the runner is not authorized by this change. No Gemini provider credential is configured or passed.
- **mini-SWE-agent, Aider, OpenHands SDK, Goose:** no provider credentials or model route are configured by this change. They are not registered as A0 executors and have no authority to mutate the repository.
- No `secrets: inherit`, provider-key forwarding, paid fallback, or secret access was performed.
- Existing Ollama/FCC endpoints remain loopback-scoped with the existing run-scoped FCC authentication contract.
- The runner is GitHub-hosted and ephemeral. The workflow does not provision a persistent VM or guarantee service availability after the job ends.
- Shared runner capacity does not imply shared agent identity, capability, quota, or write access. Before agent-mode qualification, each adapter needs an explicit identity/capability contract, model route, quota budget, workspace isolation, audit record, and bounded output policy.

## 5. Exact-head CI and runtime evidence

Latest observed PR #610 workflow run for the prior immutable HEAD:

- [Alamo candidate run 41191982864](https://github.com/VlDMlNSh/mediahub-os/actions/runs/41191982864): `workflow-contract`, `dispatch-gate`, and `alamo-local-fcc-claude` completed SUCCESS. The runtime job executed only the pull-request no-op step; all installation, Ollama, FCC, Claude Code, and agent toolchain steps were SKIPPED.
- [Astra Cloud Runtime Validation run 41191982860](https://github.com/VlDMlNSh/mediahub-os/actions/runs/41191982860): SUCCESS.
- [Astra Verify run 41191982832](https://github.com/VlDMlNSh/mediahub-os/actions/runs/41191982832): SUCCESS.
- The five observed check-run names were `alamo-local-fcc-claude`, `dispatch-gate`, `workflow-contract`, `validate`, and `verify`. They do not match the five exact required contexts in active ruleset `26108066`; exact required-context matches on this PR HEAD are **0/5**.
- No workflow artifacts were produced.
- No live workflow_dispatch, tool installation, Ollama inference, FCC request, Claude Code task, Gemini child dispatch, provider/model call, secret read, merge, deployment, or qualification occurred.

The latest code HEAD subsequently advanced to `8f59cc25e789796979637aab6edd7e0e98c4f511` for the PATH/SDK interpreter export improvement. The PR-scope workflow checks reported SUCCESS on that exact HEAD, but the ruleset exact-context mismatch and independent-review gate remain unresolved. Re-run the exact-head check reconciliation after the required CI alignment reaches main.

## 6. Governance and related PRs

- Active ruleset: [MediaHub-main-autonomous-merge #26108066](https://github.com/VlDMlNSh/mediahub-os/rules/26108066). Required contexts:
  - `Astra Cloud Runtime Validation`
  - `AI Factory verification`
  - `provider contract verification`
  - `Astra Verify`
  - `Gemini workflow contract validation (Wave 284)`
- [PR #613](https://github.com/VlDMlNSh/mediahub-os/pull/613) exact HEAD `237948e03088c3ea43608b0c284327c552d34f4b` produced all five required exact contexts SUCCESS. It remains OPEN/DRAFT/UNMERGED with no independent formal review or inline review threads.
- [PR #617](https://github.com/VlDMlNSh/mediahub-os/pull/617) records Wave 504 but is a separate documentation proposal, not an accepted canonical update.
- [Issue #301](https://github.com/VlDMlNSh/mediahub-os/issues/301) remains open.
- Main remains `f0448f28c7cfa61e4450c38529f09afbfdbbc7c7`; the canonical docs branch remains `d9a289b9113f7567711b641a7017eb814d6c259d`.

## 7. Runner availability

SentinelX reports one active host, `Voktors-Mini.Dlink`, with one active slot on the Free plan; `mh-dev-01` and `mh-dev-02` are disabled. This does not provide two persistent machines. GitHub-hosted Ubuntu runners are separate ephemeral execution environments created by Actions and destroyed after the workflow.

## 8. Home Assistant architecture clarification

Functional Baseline 2.0 explicitly names **Home Assistant Core as the Smart Home operational/device-state authority**. Therefore it is not merely a future agent-pool add-on and must not be confused with a coding agent or the developer runner control plane. Any future integration belongs to the Smart Home domain and remains behind MediaHub policy/security boundaries. No Home Assistant implementation or deployment is part of this wave.

## 9. Disposition and next step

- Toolchain definition and workflow code: **IMPLEMENTED IN OPEN PR**.
- PR-scope contract/CI checks: **SUCCESS** on observed exact head.
- Active ruleset exact contexts: **NOT SATISFIED (0/5 on PR #610)**.
- Independent security review: **NOT VERIFIED**.
- Actual installation and version/import checks on Ubuntu: **NOT RUN**.
- Provider/model invocation: **NOT RUN**.
- Agent identity/capability/quota/workspace qualification: **NOT RUN**.
- Production qualification and acceptance: **NOT ACCEPTED**.

Next bounded sequence:
1. Obtain independent review of PR #613 and integrate it only after all governance and exact-head gates pass.
2. Retarget/rebase PR #610 onto the updated main, then verify all five exact required contexts on its new immutable HEAD.
3. Obtain independent security/contract review of the exact final PR #610 HEAD.
4. Only after those gates, run the owner-gated manual hosted workflow on an immutable main SHA and inspect the artifact digest. Treat the first run as installation and bounded smoke evidence, not agent qualification.
5. Qualify each agent adapter separately. Keep Gemini execution on the approved controller route.

No Master Roadmap priority or Functional Baseline change is proposed in this wave because the runner extension is not merged, qualified, or accepted.
