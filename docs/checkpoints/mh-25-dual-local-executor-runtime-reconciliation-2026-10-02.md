# MH-25 — Dual Local Executor Runtime Reconciliation — 2026-10-02

Status: PARTIAL / FAIL-CLOSED

## Target node

- Node: mh-dev-01
- Codex CLI: present, version 0.151.0
- Claude Code CLI: present, version 2.1.280
- Astra/local autonomous processes: present on node

## Fresh runtime evidence

### Codex

The local Codex executable is present and starts as a native local process. A bounded read-only probe was launched from the isolated dual-executor worktree.

The first probe inherited stdin and remained waiting for input; that process was explicitly terminated. This does not establish successful model execution. A second probe must use stdin=/dev/null and produce the required marker before D2/D3 can pass.

### Claude

The local Claude Code executable is present and launches. A bounded non-mutating print probe completed with:

- model resolution: `~anthropic/claude-opus-latest[1m]`
- authentication failed
- HTTP 403
- provider message: access denied by security policy

Therefore Claude local runtime is installed but not currently qualified for execution.

## Current gates

- D1 provider identity: PASS (CLI identities present)
- D2 local runtime availability: PARTIAL — Codex process launchable; Claude authentication blocked
- D3 isolated workspace execution: BLOCKED
- D4 concurrent disjoint-task execution: BLOCKED
- D5 timeout/failure handling: DESIGNED
- D6 result contract: DESIGNED
- D7 independent A3 verification: BLOCKED
- D8 evidence chain: DESIGNED
- D9 restart/recovery: BLOCKED
- D10 exact-SHA qualification: BLOCKED

## Controller state

Existing Astra/autonomous controller processes are running on mh-dev-01. This evidence does NOT establish that the existing controller is wired to both CODEX_LOCAL and CLAUDE_LOCAL. The dual-provider contract remains fail-closed until provider dispatch is directly evidenced.

## Safety

No credential creation, credential extraction, quota bypass, force-push, rebase, reset, or history rewrite was performed.
