# Wave 516 — Ollama pin refresh and FCC local-route hardening (2026-11-02)

## Immutable source snapshot

- Main HEAD: `af200c4323bd4cb7cfa4c47dab4accc10049d1ec`.
- Branch: `feat/ollama-runner-ecc-wave-510`.
- PR #623: OPEN / READY / UNMERGED; mergeable=true; no formal reviews or inline threads.
- Source target before this report commit: `830f5acb56153fe3bc9e1ebc651f78507c4f3aa9`.
- Workflow blob: `12b684bbd3d475d64cac7e37bbaf64c65ce40529`.
- Contract test blob: `a3cf0c8fffbe5fd049144619d388354b4704b1d8`.

## Bounded implementation

### Ollama pin refresh

Updated the Ubuntu runner from Ollama `0.40.11` to `0.40.13`.

- Official release: [ollama/ollama v0.40.13](https://github.com/ollama/ollama/releases/tag/v0.40.13), published 2026-10-28.
- Release commit: `04088e7c9d41cba5d33bafbf788d87a465c79d5b`.
- Versioned installer asset: [install.sh](https://github.com/ollama/ollama/releases/download/v0.40.13/install.sh).
- Official installer asset SHA-256: `25f64b810b947145095956533e1bdf56eacea2673c55a7e586be4515fc882c9f`.
- Workflow now downloads the versioned release asset, verifies the SHA-256 and checks `ollama --version` for `0.40.13`.

The existing model candidate remains `llama3.2:3b`; its actual download, model digest and inference have not been executed in this pass.

### FCC local-only configuration assertions

Before starting FCC, the bounded runtime script now asserts the effective managed settings:

- `MODEL == ollama/llama3.2:3b`.
- `OLLAMA_BASE_URL == http://127.0.0.1:11434`.
- `MODEL_FALLBACKS` absent.
- No custom providers.
- No model-tier overrides for Fable/Opus/Sonnet/Haiku.
- Provider API keys/tokens, secret/access keys and bearer tokens are empty; only the run-scoped local FCC bearer token is exempted from that denylist.
- Provider proxy fields are empty.
- Proxy authentication remains enabled and the managed token is compared without printing it.

This is a source-level runtime assertion. It has not been executed on a live runner because the PR event intentionally skips runtime installation and provider/model operations.

### Regression coverage

Added source-contract assertions for:
- The exact Ollama version and versioned release asset URL.
- The pinned installer SHA-256.
- FCC effective route identity, loopback URL, no fallback, no custom provider, no cloud credentials and no provider proxy fields.

The test suite completed **13/13 PASS** on the exact source target.

## Exact-head CI

All eight check-runs on `830f5acb56153fe3bc9e1ebc651f78507c4f3aa9` completed terminal **SUCCESS**:

| Check | Workflow run | Job |
|---|---:|---:|
| `ollama-local-fcc-claude` | [41389278687](https://github.com/VlDMlNSh/mediahub-os/actions/runs/41389278687) | 125096946308 |
| `workflow-contract` | [41389278687](https://github.com/VlDMlNSh/mediahub-os/actions/runs/41389278687) | 125096920512 |
| `dispatch-gate` | [41389278687](https://github.com/VlDMlNSh/mediahub-os/actions/runs/41389278687) | 125096920151 |
| `Astra Verify` | [41389278506](https://github.com/VlDMlNSh/mediahub-os/actions/runs/41389278506) | 125096871603 |
| `Astra Cloud Runtime Validation` | [41389278518](https://github.com/VlDMlNSh/mediahub-os/actions/runs/41389278518) | 125096871? |
| `AI Factory verification` | [41389278619](https://github.com/VlDMlNSh/mediahub-os/actions/runs/41389278619) | 125096? |
| `provider contract verification` | [41389278774](https://github.com/VlDMlNSh/mediahub-os/actions/runs/41389278774) | 125096? |
| `Gemini workflow contract validation (Wave 284)` | [41389278638](https://github.com/VlDMlNSh/mediahub-os/actions/runs/41389278638) | 125096872246 |

The five exact active Ruleset contexts are present and SUCCESS on this SHA: Astra Verify, Astra Cloud Runtime Validation, AI Factory verification, provider contract verification, and Gemini workflow contract validation (Wave 284).

The runner workflow was triggered by `pull_request`. Its contract test job ran and passed, but every live runtime step was **SKIPPED**: FCC checkout, capacity measurement, ECC checkout, Ollama installation, model pull/inference, FCC server/auth smoke, Claude Code installation/invocation and artifact upload. The successful job result is not runtime qualification.

## Runner and Gemini disposition

- Runner 1 (Ollama/FCC/Claude Code/ECC): source contract CI VERIFIED; live install and inference NOT RUN.
- The workflow targets ephemeral `ubuntu-latest`; it does not provision or retain a persistent Ubuntu VM.
- Runner 2 co-location remains NOT IMPLEMENTED. The main controller dispatches three child workflow runs, each with its own `ubuntu-latest` allocation; the controller itself also uses a separate hosted job. This does not satisfy one-VM co-location.
- Gemini Agents 1/2/3: NOT RUN. No controller batch run, child run/job IDs or agent artifacts are claimed.
- SentinelX currently exposes only the macOS ARM64 `Voktors-Mini.Dlink` host in the active slot; it is not an Ubuntu runner. Desktop Commander lists `mh-dev-01` and `mh-dev-02` offline. No usable persistent Ubuntu runner was verified.
- Secret/variable presence and scope for the Gemini controller remain NOT VERIFIED; no secret values were read.
- Independent review of PR #623 remains NOT VERIFIED (0 formal reviews, 0 inline threads). Exact CI success does not replace the project security-review gate.
- No merge, installation, deployment, qualification or acceptance occurred.

## Next bounded step

1. Obtain an independent security review of PR #623.
2. Resolve the deployment model for two Ubuntu runners: GitHub-hosted ephemeral jobs versus actual persistent Ubuntu VMs; verify a real Ubuntu target and its disk/CPU/RAM before provisioning.
3. For Runner 2, design a same-host arrangement with three separately isolated agent execution environments and a controller boundary that cannot leak its GitHub API/HMAC credentials to the agents. Do not dispatch until the existing controller gates pass.
4. After the runner workflow is integrated through the reviewed path, run one owner-gated exact-main runtime smoke and retain the model digest, measured capacity, FCC 401/200 evidence, Claude marker and artifact digests. This remains future work, not a completed action.

## Canonical references

- [Canonical project map](https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md)
- [Bootstrap](https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CONTEXT-BOOTSTRAP-INSTRUCTION.md)
- [Continuation checkpoint](https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/checkpoints/mediahub-next-continuation-checkpoint-2026-10-12-current.md)
- [Master Roadmap](https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/checkpoints/MEDIAHUB-MASTER-DEVELOPMENT-ROADMAP-1.0.md)
- [Issue #301](https://github.com/VlDMlNSh/mediahub-os/issues/301)
- [PR #623](https://github.com/VlDMlNSh/mediahub-os/pull/623)
- [Wave 515 two-runner placement audit](MEDIAHUB-TWO-RUNNER-PLACEMENT-AND-GOVERNANCE-WAVE-515-2026-11-02.md)
