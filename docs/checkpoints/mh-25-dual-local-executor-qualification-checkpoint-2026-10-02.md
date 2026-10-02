# MH-25 — Dual Local Executor / GitHub Transport Qualification Checkpoint 2026-10-02

Status: QUALIFICATION IN PROGRESS / FAIL-CLOSED
Checkpoint commit: 4f2f1f9604dae6d4a4f6914056f348afe2766d04
Repository: VlDMlNSh/mediahub-os

## Continuation contract

New chat continuation command: `продолжай`

On continuation, resume from this checkpoint. Do not restart architecture work or reuse historical PASS evidence. Reconcile the exact current `main` SHA first.

## Objective

Qualify two independent local coding executors:

1. Codex Code CLI
2. Claude Code CLI

Provider paths under test:

- FCC / Free Claude Code
- OmniRoute
- native provider path only where independently authenticated and executable

ECC is treated as an auxiliary local-assistant component. ECC may provide local orchestration/assistant capability, but it is not granted MediaHub authority and is not allowed to manufacture provider credentials or bypass provider policy.

## Canonical topology

- mh-dev-02: A0 Astra GitHub Transport controller, approximately 16 GiB RAM.
- mh-dev-01: execution node, approximately 8 GiB RAM.
- Control transport: GitHub command files under `control/commands/<node>.json`.
- Evidence transport: `control/results/<node>.json` on `astra-node/<node>`.
- Execution chain: TASK -> CLAIM -> DISPATCH -> WORKER -> RESULT -> VERIFY -> EVIDENCE -> COMMIT.
- Maximum local executor concurrency: 2.
- Concurrent claims must be disjoint and task workspaces isolated.
- No provider receives MediaHub authority.
- No credentials are stored in GitHub.

## Fresh evidence

### mh-dev-02

GitHub Transport health command:
- command commit: `c5191f0ce657346d385a175ed12a0cd067da5668`
- result branch: `astra-node/mh-dev-02`
- status: PASS
- hostname: mh-dev-02
- Python: 3.12.3
- Linux: 6.8.0-142-generic x86_64

The controller process was observed running from `/home/mediahub/astra-work`.

Reboot persistence is not yet independently proven.

### mh-dev-01

A controller-process reconciliation result exists:
- command: `MH25-RECOVER-DUPLICATE-CONTROLLER-20261002-01`
- execution head: `1f9c05ee1911dbcc689570b76a140fba08ae7ffd`
- status: PASS
- remaining duplicate Astra GitHub controller processes: none at reconciliation time

This does not prove current controller polling or reboot persistence.

### Provider inventory evidence

The execution-node service account exposed to the GitHub Actions runner currently resolves:

- codex: `/usr/local/bin/codex`
- fcc-codex: NOT_FOUND in runner PATH
- fcc-claude: NOT_FOUND in runner PATH
- omniroute: NOT_FOUND in runner PATH
- claude: NOT_FOUND in runner PATH
- ecc / ecc-cli: NOT_FOUND in runner PATH

This is a runtime identity/environment boundary, not proof that the user-level mediahub installation is absent. The known FCC installation is under the mediahub user's home and is not readable by the mediahub-runner account.

FCC proxy/API was previously proven responsive on the mediahub user path. That evidence is not promoted to current runner qualification.

## 23-wave qualification implementation

GitHub Actions workflow added:

`.github/workflows/mh25-dual-local-executor-23wave.yml`

Workflow commit:
`4f2f1f9604dae6d4a4f6914056f348afe2766d04`

The workflow is designed to execute the existing `dual_local_executor_23wave` Astra qualification operation for 23 rounds, record per-round status/latency, inventory ECC, compare FCC and OmniRoute paths, and publish an artifact.

The GitHub Actions API exposed in this session did not return a run for the push-triggered workflow, so no workflow PASS is claimed.

## Existing local 23-wave operation

`astra_github_agent.py` contains `dual_local_executor_23wave`.

It performs 23 rounds across:

- FCC Codex
- FCC Claude
- OmniRoute Claude
- OmniRoute Codex

It records:

- exact execution HEAD
- inventory
- proxy probes
- marker presence
- return code
- timeout
- latency
- per-provider pass count
- pass rate
- median latency
- selection order

Promotion condition in the current implementation requires both FCC Codex and FCC Claude to achieve 23/23. This condition must be reviewed before final provider selection because it is intentionally conservative and does not yet represent an independent quality model.

## Current qualification gates

| Gate | Status |
|---|---|
| D1 provider identity | PASS |
| D2 executable/provider availability | BLOCKED/PARTIAL |
| D3 isolated execution | BLOCKED |
| D4 concurrent disjoint execution | BLOCKED |
| D5 timeout/failure | IMPLEMENTED |
| D6 result contract | IMPLEMENTED |
| D7 independent A3 verification | BLOCKED |
| D8 evidence chain | IMPLEMENTED |
| D9 restart/recovery | BLOCKED |
| D10 exact-SHA qualification | BLOCKED |
| 24h GOLD | BLOCKED |

## Required next waves

### Wave 1 — runner/runtime boundary
1. Reconcile mh-dev-01 controller polling state.
2. Reconcile mediahub vs mediahub-runner executor identities.
3. Make the intended executor user explicit.
4. Ensure FCC and OmniRoute launchers are available to the executor identity without exposing credentials.
5. Ensure ECC is inventory-only and cannot become authority.

### Wave 2 — provider qualification
Run at least 23 rounds per candidate path:
- FCC Claude
- FCC Codex
- OmniRoute Claude
- OmniRoute Codex

Each round must use stdin=/dev/null, non-mutating prompts, exact marker, timeout, and result contract.

### Wave 3 — concurrency
Run two disjoint claims concurrently with two isolated workspaces. Capture overlapping timestamps and distinct claim IDs.

### Wave 4 — A3
A3 independently verifies both result contracts and exact target SHA. Worker self-report is not sufficient.

### Wave 5 — negative/recovery
Exercise:
- timeout
- non-zero exit
- provider unavailable
- malformed result
- interrupted process
- controller restart
- claim expiry
- result replay/idempotency

### Wave 6 — exact-SHA
Freeze one exact source SHA. Re-run D1-D9 against that SHA. Do not inherit historical evidence.

### Wave 7 — 24h GOLD
Only after D1-D10 PASS:
- enable the bounded autonomous controller
- 24h soak on the exact qualified SHA
- preserve artifacts
- independent final verification

## 24/7 controller rule

The intended controller is mh-dev-02. A live process is not equivalent to reboot-persistent 24/7 qualification.

Required proof:
- service installed
- service enabled
- active after boot
- GitHub poll/consume/publish loop healthy
- duplicate-controller fencing
- restart recovery
- exact result branch evidence

Until these are observed, controller status remains IMPLEMENTED / RUNTIME QUALIFICATION GATED.

## Hard stops

Never:
- label Qwen/Ollama traffic as Anthropic Claude;
- treat FCC/OmniRoute gateway success as native Anthropic/OpenAI provider qualification;
- expose or create credentials;
- bypass quota/security policy;
- force-push or rewrite history;
- promote historical GOLD to a newer SHA;
- close qualification gaps from implementation text alone.

## Exact continuation point

Start from current `main` and this checkpoint. First action in the next chat:

1. fetch current `main` SHA;
2. inspect this checkpoint and current gap register;
3. inspect latest `control/results/mh-dev-01.json` and `control/results/mh-dev-02.json`;
4. determine whether the 23-wave workflow has produced a run;
5. if no run, repair the GitHub Actions/controller execution path before changing provider policy;
6. continue until fresh machine-verifiable qualification evidence exists.

No false closure.
