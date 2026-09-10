# W04C — OpenRouter elimination checkpoint

Date: 2026-09-10

## Objective

Remove OpenRouter from MediaHub native/runtime execution and Codex default routing without bypassing provider regional policy.

## Implemented

- Native provider gateway now contains only Opper and Continuum.
- OpenRouter credential loading was removed from the repository systemd gateway unit.
- Gateway upstream routing no longer contains an OpenRouter branch.
- Historical gateway tests were converted to exercise the remaining qualified providers while preserving failure/failover coverage.
- Native adapter comment no longer names a third-party gateway as a runtime dependency.
- `/home/mediahub/.codex/config.toml` default provider is now `continuum` with `gpt-5.6-luna`.
- A sanitized MediaHub-specific Codex home was created at `/home/mediahub/.mediahub-codex`.
- The previous Codex configuration was retained as a non-runtime backup.

## Verification

- Targeted gateway/native tests: 23 passed; final gateway set: 13 passed.
- Full pytest: 300 passed.
- Ruff: all checks passed.
- Local security scan: exit code 0.
- pip-audit: no known vulnerabilities.
- Runtime OpenRouter scan under `ops/`: PASS.
- argv credential pattern scan: no matches.

## Remaining gates

- System OpenRouter gateway remains active because `systemctl stop` requires interactive authorization for the current user. No destructive system change was performed.
- Codex legacy backup/ECC cache may contain historical OpenRouter text; these are not native runtime authorities.
- Mypy currently fails on repository/module-resolution configuration and missing test/runtime imports; no PASS asserted.
- Semgrep reports four blocking findings, including local loopback HTTP and HTTPSConnection rules; no suppression was added.
- Bandit reports seven low-severity findings in existing local autonomous/security code; no false PASS asserted.

## Immutable authority

R4 remains unchanged and no production merge/cutover was performed.
