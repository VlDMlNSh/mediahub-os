# Wave 351 — recovered Claude/FCC/Ollama historical evidence

- Date: 2026-10-22
- Status: **HISTORICAL COMPONENT/TRANSPORT EVIDENCE RECOVERED / HISTORICAL END-TO-END RUN ID NOT YET LOCATED / CURRENT RUNTIME NOT QUALIFIED**
- Canonical map: [MEDIAHUB-CHAT-TREE-MAP.md](../architecture/MEDIAHUB-CHAT-TREE-MAP.md)
- Related live work: [Issue #301](https://github.com/VlDMlNSh/mediahub-os/issues/301), [PR #437](https://github.com/VlDMlNSh/mediahub-os/pull/437), [PR #443](https://github.com/VlDMlNSh/mediahub-os/pull/443)
- Previous effort reconciliation: [Wave 349](MEDIAHUB-NEXT-RECONCILED-EFFORT-AND-TRIGGER-COVERAGE-WAVE-349-2026-10-22.md)

## Owner correction and treatment

Owner reports that the Claude-fcc-Ollama lane and agent-browser previously ran successfully and passed checks. This pass searched the repository's indexed files and recovered concrete historical evidence below. Do not rebuild the route or repeat completed browser work merely because a later bounded PATH inventory did not find a command. A historical pass remains historical; it is not silently promoted to current exact-SHA qualification.

## Recovered evidence

### 1. Host inventory on 2026-10-02

[Hybrid component reconciliation](https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/checkpoints/2026-10-02-astra-gold-hybrid-component-reconciliation.md), blob SHA `567ea108f5faee9d9176cb475ac8534ef19eb25d`, records for `Voktors-Mini.Dlink`:

- macOS Darwin 23.6 / arm64;
- Claude Code 2.1.282 discovered;
- OmniRoute 3.8.50 discovered and a running OmniRoute process observed;
- Ollama 0.34.4 discovered and a running Ollama server observed;
- Node.js 22.23.3 discovered.

The same report explicitly classifies this as read-only discovery, not qualification. It is strong evidence that a later scan finding no reachable Ollama server represents a change in runtime state, not proof that the route never worked.

### 2. GitHub transport identity/health

[2026-09-27 refresh checkpoint](https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/evidence/checkpoints/2026-09-27T2145Z-mediahub-refresh.md), blob SHA `18ca4708d67456fc6be8953cfe411fff8c007d67`, records a fresh transport health command `health-verify-20260928T0018Z`:

- `Voktors-Mini.Dlink`: **PASS**, transport `self-reexec-v1`, canonical worker SHA `cd7a83c6b6b8d6065a157274e79e315e2aa5012c0f8ee9466de92980570b9e1a`, worktree `/Users/voktor/astra-work`;
- result commit recorded as `3a369037e99058d51e37eee3d26fb3941a6506f` in the checkpoint.
  
This is a historical transport PASS, not evidence of today's connected session or current Ollama inference.

### 3. Existing three-Claude qualification workflow

[Workflow source](https://github.com/VlDMlNSh/mediahub-os/blob/main/.github/workflows/mh25-three-claude-23wave.yml), blob SHA `3a7327135ea73c7a886c1c8b6dbbf7080aff421c`, already implements a real three-lane 23-round qualification pipeline. The Mac lane:

- admits only `Voktors-Mini.Dlink` or `Voktors-Mac-mini`, user `voktor`;
- requires `claude`, `ollama`, the installed `free-claude-code/fcc-server` binary and `ollama show qwen2.5-coder:1.5b`;
- executes `ops/qualification/run_claude_23wave.py` against `qwen2.5-coder:1.5b`;
- uploads `astra-claude-mac-23wave-${{ github.sha }}` artifact.
  
The aggregate job downloads the three node artifacts, calls `verify_three_claude_23wave.py` bound to `GITHUB_SHA`, and emits `THREE_CLAUDE_23WAVE=PASS` only if the verifier succeeds. The workflow file is implementation evidence, not itself proof that a particular run passed.

### 4. Existing local-worker implementation

[Distributed local worker](https://github.com/VlDMlNSh/mediahub-os/blob/main/ops/qualification/run_distributed_local_worker.py), blob SHA `dfa6bdfc5b2bd728f51ded9bd21b4de9db127cd1`, already contains a bounded local Claude/FCC/Ollama executor. It binds `Voktors-Mini.Dlink` and `Voktors-Mac-mini.local` to `qwen2.5-coder:1.5b` and the FCC env path. It checks that `MODEL=ollama/<model>`, probes FCC health, starts FCC if needed, and validates a real execution result. This implementation is reused; it is not being rewritten.

### 5. Qualification boundary

The repository's [authorized execution schemes](https://github.com/VlDMlNSh/mediahub-os/blob/main/docs/operations/ASTRA-AUTHORIZED-EXECUTION-SCHEMES.md), blob SHA `db12a7559de0ed5d2bcebf623133f22509ecf5d7`, still labels the three-Claude distributed-local scheme **AUTHORIZED / QUALIFICATION PENDING**. Its PASS rule requires fresh exact-SHA evidence from all three lanes, independent verification, aggregate qualification and a fresh soak. Separately, [local qualification result 2026-10-02](https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/qualification/ASTRA-GOLD-LOCAL-QUALIFICATION-RESULT-2026-10-02.md), blob SHA `3b284dd211414da816af8fc4ac8addbc810a928d`, documents repository-local tests passing (197 unittest, 228 pytest, 25 schemas/9 envelope contracts) while correctly keeping live-node/provider qualification blocked because it ran on a different node without live credentials. This is not a failed Claude run; it is a separate local-only gate.

## What was and was not recovered

- **Recovered:** prior host/runtime discovery, historical GitHub transport PASS and exact worker SHA, existing Claude/FCC/Ollama execution implementation and three-lane 23-wave qualification contract.
- **Not yet recovered in this pass:** an exact historical successful workflow run ID and its aggregate `THREE_CLAUDE_23WAVE=PASS` artifact/digest. Repository code search does not index GitHub Actions run history. The owner reports successful historical execution; record as owner-reported until run/artifact metadata is found.
- **Current runtime:** the latest Wave 347 bounded check found Ollama client 0.34.4 but could not connect to a running Ollama server; a later reconnect attempt was interrupted by a SentinelX session issue. Do not overwrite the older positive inventory; classify it as historical state with a current availability gap.
- **Browser:** prior successful agent-browser work is owner-reported and will not be repeated. The old successful task/run artifact has not been found in this repository search. A recent PATH check is not evidence that no earlier browser execution happened.

## Current next step

1. Reuse the existing workflow/worker; do not rebuild.
2. Resolve PR #437 exact-head evidence: current combined status, workflow-run wrapper and formal review endpoints still return empty arrays for head `e7e99c2fe5f090df3a731b0b1a7f3fcb5335bd14`. Status is **NOT VERIFIED**, not PASS.
3. Once the source gate is satisfied, run the controller-owned Gemini batch via the approved GitHub controller only. The Mac local lane remains separate; if current Claude qualification is required, recover its runtime and retrieve fresh evidence through its existing qualified workflow, without using the Mac to launch/transport Gemini.
4. Find historical Claude/browser workflow run IDs/artifact metadata using Actions history when that interface is available; do not fabricate IDs.

No secret values were read, no provider was called, no local service was started, no workflow dispatched and no owner trigger posted in this pass.
