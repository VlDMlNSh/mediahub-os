# MediaHub autonomous development status

This repository is the local autonomous engineering workspace on mh-dev-01.

- Base lineage: PR #66 downstream of immutable R4.
- Current branch: `autonomous/os-build`.
- Immutable R4: `471f709f5633feab7aeb62dd3ea52effad6d2bc4`.
- R4 tree: `2279612908135418b2b5448d598274ea6741deaa`.
- Current local control commit: `87044b4e650cdc24588da62652e6de70531155d0`.

## Autonomous loop

`ops/autonomous_os_loop.sh` runs bounded Codex engineering cycles and repeats until STOP is requested or safe progress is blocked.
`ops/autonomous_watchdog.sh` restores the controller if its process disappears, unless `.autonomous/STOP` exists.

## Security gate

The local gate uses compileall, pytest, security pytest, Ruff, mypy, Semgrep, Bandit, pip-audit and git diff checks.
Official Codex Security was requested through the plugin catalog, but its ChatGPT plugin installation state is not yet verified as installed in the local Codex runtime.

## Governance

R4 remains immutable. MH-05 qualification, independent security review, independent system-wide review, MH-06, production authorization and release authorization remain separate gates and are not changed by this automation.

## Working rule

Inspect -> implement -> test -> security scan -> diagnose -> smallest safe fix -> retest -> repeat.
Use exact SHA/TREE provenance. Do not fabricate qualification or independence. Mature GitHub dependencies may be integrated only after license, security, maintenance, compatibility and exact pinning checks.
