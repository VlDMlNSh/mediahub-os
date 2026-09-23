# MediaHub OS — Claude Code Engineering Contract

## Mission
Work only within the existing MediaHub OS / MediaHub iOS architecture. Do not restart or redesign the project from zero.

## Mandatory engineering rules
- Inspect relevant existing files before proposing or changing code.
- Never invent APIs, files, schemas, commands, or repository state.
- Make the smallest change that fully satisfies the task; no speculative refactors.
- Preserve existing contracts and backwards compatibility unless the task explicitly changes them.
- Never hard-code credentials, tokens, secrets, private keys, or environment-specific passwords.
- Never log secrets or copy secrets into source, tests, artifacts, or documentation.
- Use least privilege for tools and execution.
- Do not use destructive shortcuts (`rm -rf`, force reset, force push, bypass hooks/checks) unless explicitly authorized.
- Do not modify tests merely to make a failing implementation pass. Fix the implementation.
- Add or update tests for behavior changes.
- Run the narrowest relevant formatter, linter, type checker, and tests after changes.
- Before finishing, inspect the diff and verify that only intended files changed.
- If requirements conflict with existing contracts, stop and report the conflict instead of silently rewriting architecture.

## MediaHub architecture
- MediaHub Codex = authority/policy layer.
- Astra = master orchestrator.
- CloudFirstOrchestrator = cloud-first routing component; OpenRouter is the primary cloud route; local providers are extensions.
- Agent Gateway/Router = delegation boundary.
- Ollama = local extension/fallback inference when no suitable credentialed cloud route is available. OpenRouter API credentials remain in GitHub Actions Secrets and are never required on the host.
- Claude = engineering/architecture/review worker when explicitly enabled.
- Cursor = repository-native implementation worker when explicitly enabled.
- Gemini/Nano Banana = multimodal/image worker when explicitly enabled.
- Harness = execution/harness layer, not authority and not the orchestrator.

## Completion contract
A coding task is complete only when implementation, relevant tests, validation, and evidence are present. State what was changed, what was verified, and any remaining blocker.
