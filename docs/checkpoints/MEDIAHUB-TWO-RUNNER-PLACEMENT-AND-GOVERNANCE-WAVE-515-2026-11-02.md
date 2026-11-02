# Wave 515 — two-runner placement, runtime state and architecture reconciliation (2026-11-02)

## Immutable snapshot

- Main HEAD: `af200c4323bd4cb7cfa4c47dab4accc10049d1ec`.
- Runner-1 implementation branch: `feat/ollama-runner-ecc-wave-510`.
- PR #623: OPEN, READY (not draft), UNMERGED, mergeable=true.
- PR #623 exact HEAD: `f3e4d5cd1bd05796be9ffd1aed769b76ec0a00d4`.
- PR base SHA: `af200c4323bd4cb7cfa4c47dab4accc10049d1ec`.
- Active main ruleset: `MediaHub-main-autonomous-merge`, ID `26108066`.

## Runner 1 — Ollama / FCC / Claude Code / ECC

The candidate workflow is `.github/workflows/mediahub-ollama-fcc-claude-runner.yml`, blob `c4e3290f2d74523c5bcf6f340fabb8603d82ed46`; contract tests blob `f7053d2355cc5a2210ebddb8512272c953fda1d5`.

The workflow currently targets `ubuntu-latest`, which is a fresh ephemeral GitHub-hosted VM per job. It does not provision a persistent named Ubuntu runner and it does not retain an installed Ollama daemon or model after the job exits.

Exact-head PR CI run: [41388155027](https://github.com/VlDMlNSh/mediahub-os/actions/runs/41388155027), target `f3e4d5cd1bd05796be9ffd1aed769b76ec0a00d4).

- Workflow contract job 125093475472: SUCCESS; pytest contract suite completed.
- Dispatch gate job 125093475293: SUCCESS; PR event correctly admitted no live execution.
- Runtime job 125093495247: SUCCESS as a job, but the following steps were SKIPPED: FCC checkout, capacity check, ECC checkout/verification, Python/uv setup, Ollama/FCC installation, Node/Claude CLI installation, Ollama model pull/inference, FCC auth smoke, Claude invocation and evidence upload.
- Thus exact-head CI is VERIFIED (8/8 checks, including all five active ruleset contexts), but runtime installation/inference/authentication is NOT RUN.
- No Ollama version, model inventory, CPU/RAM/disk measurement or runtime artifact was produced by this PR run.
- No credentials or secret values were accessed.

## Runner 2 — Gemini controller and three agents

The main-branch controller is `.github/workflows/gemini-batch-dispatch-controller.yml`, blob `0a1246f6755020faf8b7e48d07bfff790bbaece3`.

Current controller behavior does not co-locate all three agents on one runner host. It performs three GitHub Actions workflow-dispatch API calls to:
- `gemini-autonomous-engineering.yml`, blob `155a02159912ca371e6f826c51325ca269857aad`;
- `gemini-agent-2.yml`, blob `fff1820a6b97d379b23674f36bd62227b7d4dec2`;
- `gemini-agent-3.yml`, blob `781df56e8aa7c75ba453c08378611857862b2e44`.

Each child currently declares its own `runs-on: ubuntu-latest` jobs. The controller itself also runs on a separate `ubuntu-latest` job. Therefore the existing implementation is four independent ephemeral runner allocations, not one shared second runner.

To meet the requested co-location requirement, the second-runner design needs a separately reviewed implementation: one controller job/host, with three isolated agent execution containers or equivalent sandboxes on that host. The controller transport/HMAC credentials must remain exclusively in the controller boundary and must not be inherited by agent processes/containers. Each agent must have separately scoped provider credentials, filesystem/workspace, network policy, quota and evidence output. Preserve the controller's immutable target SHA, signed task envelopes, replay protection and exact run/job/artifact provenance. Do not replace the current workflow-dispatch route with ad-hoc local scripts or bypass the controller.

Gemini Agents 1/2/3: NOT RUN. No controller run, child run/job IDs, provider calls or agent artifacts are claimed.

## Architecture conflict requiring explicit resolution

The current canonical Bootstrap still contains a hard constraint that Claude Code is a local-executor-only route on Alamo/server 3, and explicitly says not to substitute a GitHub-hosted runner for Alamo. It also requires a permitted non-paid authentication route, verified provider terms/billing, no Anthropic API/paid route and no paid fallback.

The new requested topology places Claude Code on the Ubuntu runner. The candidate PR workflow does exactly that in its planned runtime path, but no invocation occurred. This is a direct conflict with the current canonical hard requirement. Before executing the Claude Code step or accepting this topology, amend the relevant canonical route contract and Wave 272 requirements through a reviewed documentation/architecture change, or retain Claude Code on the qualified Alamo executor. Do not silently treat an owner direction as proof that the security/egress/billing contract has been revised.

Ollama + FCC + ECC static setup can be qualified independently, but the live runner workflow is currently bundled with the Claude Code invocation. A safe next implementation should separate the Ollama/FCC local inference/auth smoke from the Claude Code execution gate until the architecture conflict is resolved.

## Governance

Active repository ruleset `26108066` targets the default branch and requires exactly these five contexts:
1. Astra Cloud Runtime Validation
2. AI Factory verification
3. provider contract verification
4. Astra Verify
5. Gemini workflow contract validation (Wave 284)

All five contexts are SUCCESS on PR #623 exact HEAD `f3e4d5cd1bd05796be9ffd1aed769b76ec0a00d4`. The three additional PR checks also completed SUCCESS (8/8 total).

PR #623 has zero formal reviews and zero inline review threads. The ruleset requires zero approving reviews, but project Bootstrap still requires a genuine independent security review before controller dispatch. That project gate is NOT VERIFIED. Classic branch-protection API remains inaccessible (403). Actions secret/variable metadata listing is unavailable through the connected GitHub interface; presence/scope for `MEDIAHUB_GITHUB_TOKEN`, `MEDIAHUB_DISPATCH_HMAC_KEY` and `MEDIAHUB_GEMINI_BATCH_ENABLED` is NOT VERIFIED. Secret values were not read.

No trusted-main no-secret controller probe was verified in this pass. The controller's probe must remain non-launching; batch dispatch remains BLOCKED / NOT RUN.

## Available execution hosts

- Desktop Commander: `Voktors-Mini.Dlink` is online; `mh-dev-01` and `mh-dev-02` are offline.
- SentinelX: only operational host is `host_5f7264034bdf0b51` (`Voktors-Mini.Dlink`, macOS ARM64); Free plan has 1/1 active slots. This is not an Ubuntu runner and must not be substituted for one.
- No confirmed persistent Ubuntu host/runner is currently available through the connected execution inventory.
- The GitHub-hosted `ubuntu-latest` environment is available for ephemeral jobs only; actual capacity has not yet been measured because runtime steps were skipped.

## Status summary

- Runner 1 source and contract CI: VERIFIED.
- Runner 1 live install / Ollama inference / FCC auth / Claude invocation: NOT RUN.
- Runner 1 persistent installation: NOT PROVIDED by current workflow.
- Runner 2 single-host co-location: NOT IMPLEMENTED.
- Gemini controller dispatch gates: BLOCKED / NOT VERIFIED.
- Gemini Agents 1/2/3: NOT RUN.
- Merge, deployment, qualification and acceptance: NOT performed.
- Contour A: NOT ACCEPTED. Contour B: GATED.

## Next bounded steps

1. Resolve the canonical Alamo-only Claude Code constraint versus the requested Ubuntu placement. Until then, keep Claude invocation disabled.
2. Split Runner 1 into a local Ollama/FCC/ECC smoke that can run without Claude Code, with a distinct gated Claude executor path.
3. Design Runner 2 as one controller runner host with three isolated agent containers; add negative tests proving controller secrets are absent from agent environments and workspaces.
4. Obtain independent security review and verify controller secret/variable presence/scope metadata plus trusted-main no-secret probe.
5. Only after all gates pass, run a bounded main-SHA runtime test and record run/job/container IDs, capacity metrics, model digest, FCC 401/200 evidence and artifact digests.

## Canonical references

- [Canonical project map](https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md)
- [Bootstrap](https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CONTEXT-BOOTSTRAP-INSTRUCTION.md)
- [Continuation checkpoint](https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/checkpoints/mediahub-next-continuation-checkpoint-2026-10-12-current.md)
- [Master Roadmap](https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/checkpoints/MEDIAHUB-MASTER-DEVELOPMENT-ROADMAP-1.0.md)
- [Issue #301](https://github.com/VlDMlNSh/mediahub-os/issues/301)
- [PR #623](https://github.com/VlDMlNSh/mediahub-os/pull/623)
- [Active main ruleset](https://github.com/VlDMlNSh/mediahub-os/rules/26108066)
