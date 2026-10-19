# MediaHub OS Contour A — Gemini workflow supply-chain and dispatch audit (Wave 182)

- Date: 2026-10-19
- Status: source-backed static audit; no Gemini job dispatched, no host command executed, no tests run.
- Canonical map: [MEDIAHUB-CHAT-TREE-MAP.md](../architecture/MEDIAHUB-CHAT-TREE-MAP.md)
- Prior readiness audit: [Wave 181](MEDIAHUB-CONTOUR-A-RUNNER-MANIFEST-AND-GEMINI-POOL-READINESS-WAVE-181-2026-10-19.md)
- Governing issue: [Issue #301](https://github.com/VlDMlNSh/mediahub-os/issues/301)
- Current worker hardening candidate: [PR #375](https://github.com/VlDMlNSh/mediahub-os/pull/375)

## 1. Current verified state

- Issue #301 is open (last observed update 2026-10-19T09:15:45Z).
- PR #375 is open, Draft, not merged; head SHA `59a9d063778ec11b751cc7309c04e7fe27f3a603`, base SHA `c06015e0b1526e0aaa6a522306052b077455aba5`.
- PR #374 is open, Draft, not merged; head SHA `3b1fc96beeedcc6cb38c7beeb5809f0004c6ac8a`, base SHA `e922349c6e7a49657faf70836b36d96d977a948b`.
- Named hosted Actions runs for PR #375 are successful: Astra Verify [run 39223983372](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39223983372) and Astra Cloud Runtime Validation [run 39223983379](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39223983379). The PR #374 schema-validation run [39222111677](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39222111677) is also successful. These results do not qualify the self-hosted worker or Gemini dispatch.
- `docs/qualification/CURRENT-TRUTH.generated.md` remains blob `48d581a8f6a6a5fd380abbb7a7ce938b3b1e6731`: G0–G11 all BLOCKED, overall NOT_PROVEN / BLOCKED.
- Three Gemini workflow definitions exist on main:
  - `.github/workflows/gemini-autonomous-engineering.yml` blob `09523d809530ae5b7bf528eab5fa53bc5deaf92d`
  - `.github/workflows/gemini-agent-2.yml` blob `259c8c82b8d90a39e1c90e65390e469b241b5581`
  - `.github/workflows/gemini-agent-3.yml` blob `91b5397001e088dfae2f450ee77c9c23118b5601`
- SentinelX inventory currently shows zero connected hosts: Mac mini disconnected with reason `connection_lost`; `mh-dev-01` and `mh-dev-02` remain user-disabled. A fresh project snapshot returned `agent_offline`. No host execution occurred.
- Codex Tasks reports no registered remote environments; recent task records contain no turns, so they are not evidence of active autonomous coding.

## 2. Gemini workflow design facts

The three workflow files use a common manual `workflow_dispatch` input contract: required free-form `task`, `base_ref=main`, and `scope=contour-a`. Each uses a distinct secret reference: `GEMINI_API_KEY`, `GEMINI_API_KEY_2`, or `GEMINI_API_KEY_3`. They run on GitHub-hosted `ubuntu-latest`, set checkout `persist-credentials: false`, and configure a restricted GitHub MCP tool list for branch creation, file creation/update, PR creation, and file reads. The workflow prompt says one bounded evidence/documentation pass, dedicated branch and PR, no merge/deploy, no test/qualification or infrastructure work.

These are useful controls but remain source-level intentions until a workflow run and its artifacts prove execution. Manual dispatch does not mean the agent stays running or receives tasks automatically.

## 3. Supply-chain and authority gaps found

1. **Mutable action references:** Gemini workflow invokes `google-github-actions/run-gemini-cli@v0`; checkout uses `actions/checkout@v4`. The worker workflow also uses major-version action tags such as `actions/checkout@v4` and `actions/upload-artifact@v4`. Tags are mutable references; they do not bind the run to a reviewed commit digest. Before qualification, pin external actions to reviewed full commit SHAs and document update policy.
2. **Mutable MCP image tag:** The Gemini workflows run `ghcr.io/github/github-mcp-server:v0.27.0`. This is a version tag, not an image digest. Resolve and record a trusted immutable digest, verify provenance/signature as supported, and update only through reviewed change control.
3. **Job-level write authority:** Workflow top-level permissions are `contents: read`, but the job explicitly expands to `contents: write` and `pull-requests: write`. This appears intentional for creating branches/files/PRs, yet it means a prompt or tool-use failure can produce repository writes within that token's scope. Keep the write scope limited to the expected repository and branch/PR operations, and validate branch naming, changed paths, diff size, and PR base after the run.
4. **Free-form task is untrusted input:** The `task` input is interpolated into a model prompt. The prompt already instructs the model to treat task/repository data as untrusted; this is not a machine-enforced authorization boundary. A structured allowlisted task registry or controller-generated immutable task envelope would reduce prompt-injection and scope-widening risk.
5. **No run was dispatched:** No evidence yet establishes that the three secrets exist, that each key authenticates, that the configured Gemini model is available, or that an agent can produce a valid PR. Do not infer readiness from workflow files alone.
6. **Workflow parity needs validation:** All three definitions appear structurally similar, but Agent 1, Agent 2, and Agent 3 prompts differ by role and key. A future CI check should assert shared hardening invariants across all three workflows to prevent one agent from silently drifting.

## 4. Bounded remediation order

- P0: Preserve manual-only dispatch; do not enable self-hosted execution or automatic scheduling as a workaround for disconnected hosts.
- P1: Pin third-party actions and MCP container to immutable reviewed references; record source/provenance and upgrade path.
- P1: Add static CI checks for workflow invariants: `persist-credentials: false`, exact minimal MCP tools, no deployment/host tools, required timeout, no secret echo, no broad `pull-requests: write` outside the one bounded job.
- P2: Replace free-form authorization claims with a validated task contract (task ID, allowed paths, expected base SHA, output type, expiry) while treating model output as untrusted.
- P2: Add post-run verification for branch base, changed-file allowlist, diff budget, required evidence section, and PR URL; reject or quarantine invalid output.
- P3: Only after the workflow is hardened, manually dispatch Agent 2 and Agent 3 with the Wave 181 read-only tasks. Check run logs/artifacts and resulting PRs before dispatching Agent 1 implementation work.

Do not alter secret values or attempt to verify them by printing. Do not promote a run to qualification evidence until exact run SHA, logs, artifact digest, and independent review are recorded.

## 5. Verification boundary and next step

This was a static source review only. No code/tests were changed or run; no workflow dispatch, Gemini model call, secret read, SentinelX command, merge, deployment, or qualification occurred. The workflow files were read from `main` and their returned blob SHAs are listed above. The PR/issue heads and named successful Actions runs were re-checked during this pass.

Next bounded engineering step: create a separate Draft PR that pins third-party actions and the GitHub MCP container to reviewed immutable references, after obtaining trusted upstream commit/digest evidence; then add a static workflow-parity test. Keep PR #375 Draft/unmerged and all ASTRA GOLD gates BLOCKED until issuer/publisher and independent acceptance evidence are complete.
