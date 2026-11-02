# Wave 510 — clean Ollama/FCC/Claude runner ECC integration proposal (2026-11-02)

## Status

- Configuration branch: `feat/ollama-runner-ecc-wave-510`
- Immutable base: `af200c4323bd4cb7cfa4c47dab4accc10049d1ec` (main at inspection)
- Branch head at report creation: `fd18d813287a5f4497617907cac6f14452727545`
- Compare: 2 commits ahead, 0 behind; cleanly based on current main.
- Runtime installation: NOT RUN.
- Model download/inference: NOT RUN.
- Exact-head CI: NOT RUN (no PR was created).
- Independent review: NOT VERIFIED.
- Qualification / acceptance: NOT QUALIFIED / NOT ACCEPTED.

## Work performed

Created a clean branch from current main rather than carrying forward PR #610's 92-commit divergent history. Added:
1. `.github/workflows/mediahub-ollama-fcc-claude-runner.yml` — existing bounded owner-gated Ubuntu local inference workflow, extended with a pinned ECC guidance-only profile.
2. `tests/test_mediahub_ollama_fcc_runner_contract.py` — contract coverage extended for ECC source, selected skill blob provenance, and no hooks/MCP/controller installation.

ECC profile is pinned to:
- Repository commit: `c05b2d6614f62f6db0047669aa4eefb223d478f9`
- MIT license blob: `b832b6f642312312367c07688dc7426db40a82ed`
- `verification-loop/SKILL.md`: `d7eb1fa239fd8c0ba8ae2d31a3c34d1f01741ef9`
- `security-review/SKILL.md`: `3f26b0df65661425de4e5c40c295e04edcad7a83`
- `search-first/SKILL.md`: `3d2669e71ba54afba95defb05080253058190600`

The selected ECC files are concatenated into a runner-temp guidance file and supplied to the bounded empty-workspace Claude Code smoke. Metadata records the exact source pins and explicitly records hooks/MCP/controllers as not installed. ECC guidance does not grant execution authority.

## Verification

- Workflow read-back blob SHA: `b64a19e6058090cac389d12f1eecee13c21d548b`
- Test read-back blob SHA: `e89dcc7bb81a067462f1d620205c17c8f374f142`
- Branch head read from Git refs: `fd18d813287a5f4497617907cac6f14452727545`
- Branch compare against main: ahead 2 / behind 0.
- Static source read-back confirms ECC checkout, exact commit and blob checks, guidance profile, and artifact metadata.
- Exact-head CI has zero check runs because a PR was not created.
- Attempt to create a draft PR was blocked by the tool safety layer; no PR number or review request exists.

## Not done / blockers

- No GitHub Actions workflow_dispatch.
- No Ollama install, model pull, or inference.
- No FCC/Claude Code runtime launch.
- No secrets or provider credentials read.
- No Gemini or other agent dispatch.
- No independent review.
- No merge, deployment, qualification, or acceptance.
- PR #610 remains separate and divergent; do not merge it as part of this wave.

## Next

1. Owner/repository maintainer opens a draft PR from `feat/ollama-runner-ecc-wave-510` to `main`.
2. Wait for all required exact-head CI contexts; resolve any failures.
3. Obtain independent security review of workflow permissions, owner/target-SHA gate, source pins, shell quoting, ECC prompt composition, artifact hygiene, and no-paid-fallback behavior.
4. Only after gates are green, owner dispatches the workflow from main with `confirm=true` and exact current main SHA.
5. Treat the run as a bounded smoke only. Runtime qualification requires retained successful artifacts and independent review.

## Canonical references

- [Canonical map](https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md)
- [Issue #301](https://github.com/VlDMlNSh/mediahub-os/issues/301)
- [Prior runner PR #610](https://github.com/VlDMlNSh/mediahub-os/pull/610)
- [FCC source](https://github.com/Alishahryar1/free-claude-code/tree/3d2ae2306752dbdf504714a5489bcfcf69b2d04a)
- [ECC source](https://github.com/affaan-m/ECC/tree/c05b2d6614f62f6db0047669aa4eefb223d478f9)
