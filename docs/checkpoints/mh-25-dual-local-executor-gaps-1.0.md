# MH-25 — Dual Local Executor GAP Register 1.0

Status: LIVE / FAIL-CLOSED

| ID | Gap | State | Required evidence |
|---|---|---|---|
| G1 | Claude provider authentication/policy | BLOCKED | Direct Ollama Anthropic endpoint responds, but Claude CLI rejects the local model identity; real Claude/Anthropic auth remains unavailable |
| G2 | Codex non-interactive probe | BLOCKED | stdin=/dev/null marker PASS; local Ollama launch starts but marker PASS not yet observed |
| G3 | Astra provider dispatch wiring | BLOCKED | task->claim->provider->process evidence |
| G4 | isolated worktrees | BLOCKED | two task-scoped worktrees |
| G5 | concurrent disjoint execution | BLOCKED | overlapping timestamps + distinct claims |
| G6 | independent result contracts | BLOCKED | two valid result manifests |
| G7 | A3 verification | BLOCKED | independent verifier PASS for both |
| G8 | failure/timeout | BLOCKED | deterministic negative tests |
| G9 | restart/recovery | BLOCKED | controller/provider restart reconciliation |
| G10 | exact-SHA qualification | BLOCKED | exact source SHA and complete D1-D9 evidence |
| G11 | multi-node | BLOCKED | mh-dev-01 + mh-dev-02 qualification |
| G12 | GOLD soak | BLOCKED | exact qualified SHA 24h soak + G9 |

## Known facts

- Four GitHub agent profiles exist: A0/A1/A2/A3.
- CODEX_LOCAL and CLAUDE_LOCAL provider contracts exist.
- GitHub Transport control blueprint exists.
- mh-dev-01 has Codex CLI 0.151.0 and Claude Code 2.1.280.
- Claude first-party login remains unauthenticated; local compatibility endpoint responds, but Claude CLI model validation blocks the qwen model mapping.
- Codex fresh successful model marker has not yet been proven.
- No credential or quota bypass is permitted.

## Exit condition

No gap is closed by design text alone. Each gap requires fresh machine-verifiable evidence tied to the exact execution SHA.
