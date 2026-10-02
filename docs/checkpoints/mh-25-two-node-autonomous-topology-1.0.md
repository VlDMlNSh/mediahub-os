# MH-25 — Two-Node Autonomous Runtime Topology 1.0

Status: IMPLEMENTED / RUNTIME QUALIFICATION GATED
Date: 2026-10-02
Repository: VlDMlNSh/mediahub-os

## Purpose

Separate coordination from execution so the lower-memory node does not carry the long-lived controller plus coding workloads.

## Node roles

| Node | RAM | Role | Provider responsibilities |
|---|---:|---|---|
| mh-dev-02 | 16 GiB | A0 Astra GitHub Transport controller | GitHub polling, command admission, claims/leases, result publication, queue coordination |
| mh-dev-01 | 8 GiB | execution node | local FCC/Claude/Codex execution, task workspaces, A2 workers, A3 verification when explicitly assigned |

## Controller placement

mh-dev-02 is the canonical controller host because it has approximately 15 GiB visible memory and currently has the GitHub SSH identity required for `VlDMlNSh/mediahub-os`.

Observed evidence on 2026-10-02:
- hostname: mh-dev-02
- Python: 3.12.3
- available memory: approximately 14 GiB
- GitHub SSH authentication: successful
- main HEAD observed during bootstrap: `c5191f0ce657346d385a175ed12a0cd067da5668`
- GitHub transport health command: PASS
- result branch: `astra-node/mh-dev-02`

## Execution placement

mh-dev-01 remains the local execution node:
- 7.7 GiB RAM
- Free Claude Code installed
- `fcc-server` active on localhost:8092
- `fcc-claude` installed
- `fcc-codex` installed
- native `claude` installed
- native `codex` installed
- FCC exposes an Ollama/Qwen model path

The FCC path is classified as `CLAUDE_LOCAL_FCC` / `CODEX_LOCAL_FCC`, not Anthropic Claude or OpenAI API qualification.

## Transport contract

`mh-dev-02` receives GitHub commands under `control/commands/mh-dev-02.json`, claims execution, executes the allowlisted operation, and publishes evidence under `control/results/mh-dev-02.json` on `astra-node/mh-dev-02`.

Execution nodes remain subordinate to task/claim/target-SHA fencing. No provider is granted authority over MediaHub state.

## Persistence

The node has an existing systemd unit `mediahub-astra-github-bootstrap.service` with the correct `mh-dev-02` identity and GitHub transport configuration. The active session also runs the canonical bootstrap/agent under `/home/mediahub/astra-work`.

A reboot-persistent enablement must be independently verified on the host; absence of such evidence is a deployment gate, not a PASS.

## Qualification gates

1. controller health — PASS
2. GitHub command consume/publish — PASS
3. local Claude/FCC inference — PASS at proxy/API level
4. Claude Code headless executor marker — BLOCKED/PENDING
5. Codex/FCC headless executor marker — BLOCKED/PENDING
6. two disjoint concurrent claims — BLOCKED/PENDING
7. A3 independent verification — BLOCKED/PENDING
8. restart/recovery — BLOCKED/PENDING
9. exact-SHA qualification — BLOCKED/PENDING
10. 24h GOLD soak — BLOCKED until 1–9 PASS

No later gate may inherit PASS from an earlier or historical SHA.
