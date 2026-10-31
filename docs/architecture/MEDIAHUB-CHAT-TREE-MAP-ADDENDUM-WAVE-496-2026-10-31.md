# MediaHub Chat Tree Map Addendum — Wave 496

- Date: 2026-10-31
- Status: **WORKING-BRANCH PROPOSAL / NOT ACCEPTED**
- Implementation branch: `contour-a/alamo-fcc-claude-hosted-runner-20261031`
- Base target SHA: `f0448f28c7cfa61e4450c38529f09afbfdbbc7c7`
- Report: [Wave 496 Alamo/FCC/Claude Ubuntu Runner](../checkpoints/MEDIAHUB-ALAMO-FCC-CLAUDE-UBUNTU-RUNNER-WAVE-496-2026-10-31.md)
- Canonical map remains on [docs/mediahub-chat-tree-map-20261012](https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md).

## New working artifact

- `.github/workflows/mediahub-alamo-fcc-claude-runner.yml`: owner-gated, exact-SHA-bound Ubuntu Hosted Runner workflow for a local-only FCC/Claude Code smoke using pinned Ollama as a candidate backend.
- `tests/test_mediahub_alamo_fcc_runner_contract.py`: static contract tests for owner gate, pinned components, local-only routing, FCC auth and evidence.
- `docs/checkpoints/MEDIAHUB-ALAMO-FCC-CLAUDE-UBUNTU-RUNNER-WAVE-496-2026-10-31.md`: implementation scope, evidence requirements and blockers.

## Architecture boundary

The requested placement is an ephemeral GitHub-hosted Ubuntu runner, not a physical server. The workflow starts a loopback-only Ollama process and routes Claude Code through pinned FCC to `ollama/llama3.2:3b`. It has no OpenRouter or Anthropic credentials and no paid fallback.

This is an **Alamo-role local inference candidate**, not proof that Ollama is the Alamo implementation. The accepted architecture still requires Alamo runtime/API identity and compatibility evidence. The workflow records `alamo_equivalence=NOT_VERIFIED` and does not promote the candidate.

## Lifecycle

All processes and model files are scoped to one Actions job and disappear with the ephemeral runner. This does not create a persistent Alamo service. A successful bounded smoke would qualify only the runner-local FCC/Ollama/Claude Code path for further review, not production deployment or Contour A acceptance.

## Status

The working branch is non-canonical. CI, live dispatch, runtime smoke, independent review, qualification and acceptance remain pending.
