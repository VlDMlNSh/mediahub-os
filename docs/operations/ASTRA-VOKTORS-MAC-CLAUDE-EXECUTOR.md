# ASTRA-VOKTORS-MAC-CLAUDE-EXECUTOR.md
Node identity: Voktors-Mac-mini.local
Executor identity: claude
Local model: qwen2.5-coder:1.5b
Verifier identity: claude, running as an independent verifier process.
Authority boundary: executor-only; no controller authority or production infrastructure changes.
The worker is bound to the exact target-SHA and uses an isolated branch.
Promotion is fail-closed.
The worker never writes directly to main.
No credentials or secrets are included.
