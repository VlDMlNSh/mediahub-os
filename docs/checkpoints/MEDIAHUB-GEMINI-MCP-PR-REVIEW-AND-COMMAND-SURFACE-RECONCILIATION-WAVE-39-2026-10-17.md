# MediaHub OS — Gemini MCP PR Review and Command-Surface Reconciliation, Wave 39

- Date: 2026-10-17
- Contour: A — Developer Fabric
- Status: **PR CHECKS PASS / SOURCE FIX PROPOSED / NOT MERGED / PROVIDER RUNTIME ACCEPTANCE PENDING**
- Parent: [Wave 38 Gemini MCP core-allowlist diagnosis](MEDIAHUB-GEMINI-MCP-CORE-ALLOWLIST-DIAGNOSIS-AND-REMEDIATION-WAVE-38-2026-10-17.md)
- Project map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md

## 1. Live repository state

| Item | Current evidence |
|---|---|
| `main` HEAD | `6c2e8dbdee81c798b64e65546e7ded07093f100a` |
| Documentation branch HEAD | `207e5a951081bbe825d13a6b0de18a2853887bcb` |
| Branch comparison | `DIVERGED`; docs branch ahead 1,966 / behind 14; merge base `f0f406feb9f9816b009f4e6e756813541e53b9bc` |
| PR #307 | [Allowlist GitHub MCP tools without enabling core tools](https://github.com/VlDMlNSh/mediahub-os/pull/307) |
| PR head | `5ae969763ff7ccbd22052efbd2661cf7bbdd7fd3` |
| PR base | `main` at `6c2e8dbdee81c798b64e65546e7ded07093f100a` |
| PR state | Open, unmerged, mergeable |
| `validate` check | Success — [run 38977903775](https://github.com/VlDMlNSh/mediahub-os/actions/runs/38977903775/job/117231642998) |
| `verify` check | Success — [run 38977903690](https://github.com/VlDMlNSh/mediahub-os/actions/runs/38977903690/job/117231642369) |
| Main branch protection | GitHub branch endpoint reports `protected: false`; no required-check enforcement was evidenced by that endpoint |

The PR has two successful check runs. This is source/CI evidence only; it does not prove a successful Gemini MCP call or end-to-end task execution. PR #307 remains open. No merge or branch integration was performed.

## 2. Review of the proposed source change

The PR changes one setting in `.github/workflows/gemini-autonomous-engineering.yml`:

- Before: `"tools": { "core": [] }`
- Proposed: `"tools": { "core": ["mcp_github_*"] }`

The exact workflow on the PR branch was fetched and read back. Its server-side `includeTools` allowlist and direct prompt continue to constrain GitHub operations to the named MCP tool set. The proposed setting matches the failure mechanism described by upstream Gemini CLI issue [#28361](https://github.com/google-gemini/gemini-cli/issues/28361) and Google Action issue [#532](https://github.com/google-github-actions/run-gemini-cli/issues/532): an explicitly configured empty core-tool list can cause a wildcard deny that also excludes MCP tools from the active registry.

**Review disposition:** the one-line change is consistent with the documented root cause and has passing PR checks. Runtime acceptance remains pending. Keep the PR unmerged until the authorized reviewer applies the repository's intended integration decision; branch protection is currently reported disabled, so passing checks alone do not establish a required-review gate.

## 3. Separate bundled-command compatibility defect

The exact action revision currently resolved by the mutable `google-github-actions/run-gemini-cli@v0` ref was read as commit `f77273f4c914e4bf38440cf36a0369cb64a37489`.

At that commit, `action.yml` copies bundled command prompts from `.github/commands/*` into the workspace's `.gemini/commands/` directory. Source reads of `gemini-review.toml`, `gemini-plan-execute.toml`, and `gemini-issue-fixer.toml` show references to bare or stale MCP method names such as `get_file_contents`, `create_pull_request`, and method-shaped names that do not match the Gemini CLI's registered `mcp_{server}_{tool}` names. Upstream issue [#510](https://github.com/google-github-actions/run-gemini-cli/issues/510) documents the same class of mismatch.

Scope distinction:

- The current MediaHub workflow uses its own direct prompt with fully qualified `mcp_github_*` tool names. The reviewed failure and PR #307 concern this direct-prompt path.
- Bundled slash-command prompts are a separate defect surface. Avoid invoking those commands for autonomous tasks until their tool names and consolidated GitHub MCP method parameters have a source-pinned compatibility review.
- Do not broaden the core-tool allowlist merely to mask stale command prompts. Add built-in tools such as `activate_skill` only when a specific accepted workflow actually requires them.

The action reference is `@v0`, a mutable tag. The tag resolved during this pass to `f77273f4c914e4bf38440cf36a0369cb64a37489`. For a future hardening patch, pin the action to an audited full commit SHA and preserve a documented update process.

## 4. Portable credential and worker topology

The target architecture remains GitHub-centered and ephemeral-worker-first:

- GitHub-hosted jobs provide disposable execution capacity without requiring a continuously running owner-operated server in the provider request path.
- Provider/account credentials remain separate from any physical host. Inject a narrowly scoped secret at job runtime only where the provider requires a static key; use OIDC only for destinations that support an explicitly configured trust relationship.
- OIDC avoids storing long-lived cloud credentials in GitHub secrets when supported; it does not remove the need for a provider-side trust policy or least-privilege claims. See [GitHub OIDC documentation](https://docs.github.com/en/actions/concepts/security/openid-connect) and [cloud-provider configuration](https://docs.github.com/en/actions/how-tos/secure-your-work/security-harden-deployments/oidc-in-cloud-providers).
- Hosted-runner outbound traffic still has a real network source and provider-specific policy. No fixed egress IP, guaranteed processing region, or location-control bypass is assumed.
- Existing hardware topology remains unchanged: Mac mini 2018/macOS, Mac mini 2011/Linux, and remote video server. Ephemeral hosted runners are an additive Contour A execution lane, not a replacement for the local topology.

## 5. Agent queue and activation state

The current activation queue read-back contains 16 unique items and retains status `DOCUMENTARY_QUEUE_ONLY`. The schemas for task envelope v0.2, registry v0.2, and evidence manifest v0.2 are proposed artifacts. No durable queue consumer, lease/fencing coordinator, isolated patch worker, registered-and-qualified cloud agent, or promotion pipeline is proven by the inspected evidence.

The queue must remain fail-closed until the accepted A0 issuer/ingress/lease/cancellation/recovery contract, MH-12 capability and credential authority, R-06 audit/privacy disposition, target runner/workspace/network manifest, standards-compliant schema validation, and independent review are available. A successful CI run or a provider's authorization page alone must not move an agent to `ACTIVE`.

## 6. Acceptance evidence still required

1. Authorized merge decision for PR #307, with review provenance and exact resulting `main` SHA.
2. Separately authorized provider-runtime acceptance event against that exact source revision.
3. At least one successful read-only MCP call using the expected fully qualified name.
4. Valid structured output, correct artifact provenance, and final validator success.
5. Task outcome consistent with scope; PR evidence only when the task contract requires a PR.
6. Negative-path evidence that unapproved core tools and MCP operations remain unavailable.
7. Separate source-pinned repair/replacement plan for bundled slash-command prompts.
8. Full action SHA pin and documented controlled update procedure.
9. Closure of A0, MH-12, R-06, target manifest and schema validation gates before any durable autonomous queue activation.

## 7. Execution boundary

This wave used GitHub source reads, PR/check metadata and upstream source/issue reads. It did not dispatch a workflow, invoke a model/provider, read credential values, run tests, install software, inspect a host/runtime, change infrastructure, deploy, merge, rebase or cherry-pick. The PR's existing `validate` and `verify` checks passed; no new tests were launched by this wave.

**Next bounded action:** continue the source-bound review of the pinned OpenHands Agent Server route/configuration and workspace/tool enforcement against A0, MH-12 and R-06. Keep live activation blocked until those authority and target gates close.

## 8. Source anchors

- MediaHub PR #307: https://github.com/VlDMlNSh/mediahub-os/pull/307
- MediaHub workflow at current `main`: https://github.com/VlDMlNSh/mediahub-os/blob/main/.github/workflows/gemini-autonomous-engineering.yml
- Gemini CLI issue #28361: https://github.com/google-gemini/gemini-cli/issues/28361
- Google Action issue #532: https://github.com/google-github-actions/run-gemini-cli/issues/532
- Google Action bundled command issue #510: https://github.com/google-github-actions/run-gemini-cli/issues/510
- GitHub OIDC: https://docs.github.com/en/actions/concepts/security/openid-connect
- GitHub OIDC provider setup: https://docs.github.com/en/actions/how-tos/secure-your-work/security-harden-deployments/oidc-in-cloud-providers
- OpenHands source pin retained for the next pass: https://github.com/OpenHands/software-agent-sdk/tree/6530325e9dd0ea1b6b4f1994d7dab52764cfc3f1
