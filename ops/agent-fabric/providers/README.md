# Local executor providers

This directory defines provider contracts for Astra.

## Providers

- CODEX_LOCAL: local Codex process, selected through MEDIAHUB_CODEX_EXECUTOR.
- CLAUDE_LOCAL: local Claude process, selected through MEDIAHUB_CLAUDE_EXECUTOR.

Astra may dispatch both concurrently only when their claims and workspaces are disjoint.

Provider availability is runtime-qualified. A configured provider is not considered RUNNING or QUALIFIED until an exact-node executable probe and D1-D10 evidence pass.

No credential creation, credential exposure, quota bypass, force-push, rebase, reset, or history rewrite is performed by this provider layer.
