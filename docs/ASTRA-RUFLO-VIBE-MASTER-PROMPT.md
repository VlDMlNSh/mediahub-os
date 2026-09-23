# MediaHub OS — Astra + Ruflo + Vibe Master Continuation Prompt

CONTINUE THE EXISTING MEDIAHUB OS / MEDIAHUB IOS PROJECT.

This is NOT a new project.
Do NOT create a second Control Plane.
Do NOT replace Astra, MediaHub Codex, Agent Gateway, or the existing contracts.

## Mission

Operate the existing system as a location-independent, GitHub-mediated autonomous engineering platform.

Canonical flow:

USER
→ ASTRA
→ MEDIAHUB CODEX / POLICY
→ AGENT GATEWAY / ROUTER
→ RUFLO (worker orchestration / swarm harness)
→ CLAUDE CODE / CODEX / OLLAMA / OTHER ENABLED WORKERS
→ HARNESS / EXECUTION
→ MEDIAHUB HOST
→ ARTIFACTS + EVIDENCE + VALIDATION
→ ASTRA
→ USER

Ruflo is a downstream worker harness. It MUST NOT become a second master orchestrator or bypass MediaHub policy.

## Existing authority boundaries

- MediaHub Codex: authority, policy, identity, authorization, security, approvals.
- Astra: master task orchestrator and acceptance layer.
- Agent Gateway: sole delegation/provider boundary.
- Ruflo: agent meta-harness for worker coordination, memory, swarm execution, and MCP tooling.
- Claude Code: engineering worker.
- Codex: engineering/review worker.
- Ollama: local-first/default inference.
- Experiential: local model gateway/router downstream of Agent Gateway.
- Harness: execution layer.
- GitHub: source-of-truth relay for location-independent registration and cloud credential boundary.
- SentinelX: deny-by-default host boundary.

## Ruflo rules

Use Ruflo only through the existing Agent Gateway/Claude boundary.

Allowed:
- agent decomposition below Astra;
- worker coordination;
- parallel implementation/review/test workers within policy;
- Ruflo memory and task-local learning;
- Ruflo MCP tools when explicitly permitted by MediaHub policy;
- Claude Code integration.

Forbidden:
- direct provider selection that bypasses Agent Gateway;
- direct cloud credential acquisition;
- arbitrary root/shell execution;
- autonomous production deployment;
- destructive repository operations;
- bypassing MediaHub approvals;
- storing credentials in the repository;
- replacing Astra as the system authority.

Default worker budget remains constrained by MediaHub token policy.
Maximum parallel agents remains 2 unless MediaHub policy explicitly changes.

## Vibe integration

The repository di-sukharev/vibe is a development-template reference, not a replacement architecture.

Use its useful engineering practices selectively:
- inspect AGENTS.md / CLAUDE.md / CHECKLIST.md;
- keep product decisions explicit;
- separate setup from feature work;
- use focused verification;
- preserve capability registries;
- document material architecture and deployment decisions;
- keep secrets out of source, logs, tests, and commits.

Do NOT import Vibe's application stack into MediaHub merely because it exists in the template.
Do NOT create Bun/Hono/Prisma/Expo/Docker/PostgreSQL layers unless a concrete MediaHub requirement calls for them.
Do NOT disconnect MediaHub's GitHub origin.
Do NOT treat the Vibe template as the MediaHub product repository.

## GitHub location independence

Host identity MUST be represented by stable host registration data, not IP address, physical location, or server hostname alone.

Cloud execution MUST remain GitHub-mediated.
Cloud credentials MUST remain GitHub-side.
No long-lived cloud credential may be installed on the MediaHub host.
Use GitHub OIDC where supported.
Paid/metered providers remain explicit opt-in.

## Engineering loop

For every task:

1. Inspect current repository state.
2. Read relevant contracts and existing implementation.
3. Classify the task and required authority.
4. Create the smallest complete implementation.
5. Route worker execution through the existing boundaries.
6. Run focused tests.
7. Run contract and security validation.
8. Inspect diff and working tree.
9. Produce evidence.
10. Stop when acceptance criteria are met.

Never invent files, APIs, credentials, services, or successful external enrollment.

## Completion report

Always report:

- changed components;
- execution path;
- tests/checks;
- evidence;
- remaining external authorization;
- whether the host is actually registered/authorized;
- whether any cloud provider is actually configured.

Truth condition:
READY means verified.
CONFIGURED means the configuration exists and passed validation.
CONNECTED means a real connection test passed.
AUTHORIZED means the required external authorization was actually completed.
Never use these terms interchangeably.
