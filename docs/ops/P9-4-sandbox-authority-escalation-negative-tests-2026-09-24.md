# P9.4 — Sandbox escape / authority-escalation negative tests

Status: SECURITY_RECONCILIATION / P9.4 NOT CLOSED

## Scope

Repository-local execution of the existing sandbox, native-launch and State Authority red-team tests. The evidence is limited to the checked test suite and does not establish production or external-provider security.

## Test result

- Command: `python3 -m pytest -q` against the three P9.4 security test modules.
- Exit code: 0
- Output (sanitized):

```text
................                                                         [100%]
16 passed in 0.08s
```

## Security interpretation

- Sandbox tests cover symlink-parent denial, symlink-worktree denial, marker tamper detection and deterministic teardown.
- Native launcher tests cover unknown agents, missing/unqualified models, non-HTTPS endpoints and credential absence.
- State Authority red-team tests cover missing authorization, remote read-only context, observer isolation, forged checkpoint rejection and unavailable-authority fail-closed behavior.
- P9.4 remains OPEN until all required negative surfaces are covered and any residual sandbox, process-execution, egress or authority-escalation gaps are explicitly classified.

## Source evidence

### ops/cloud_development_sandbox.py
SHA256: 45275dbc2732b3efe274491549b27b632dbb6b21e27efda004db568a8d4911ff

### ops/mediahub_native_execution.py
SHA256: db7e67d988bb19a2c0b88bdf29ccda4a7b578df92e08da1f001f346213400a5a

### ops/mediahub_native_agent_launcher.py
SHA256: a14a6d0428c10ca551b4363fa8ed57d04947e77a951985562c05a4ec90ce923f

### runtime/mediahub_runtime/state_authority.py
SHA256: 0dac69fb3da3ed8ea78f8461be2136e0fdb93f6c803622cc58cb7d44c16e4bdb

### tests/security/test_cloud_development_sandbox.py
SHA256: 6f0bed8a5b265f6a4d21f790e1898ce41552974c497bc7a06804f7eb9437628d

### tests/security/test_native_agent_launcher.py
SHA256: 5553b0d88a086216df22993527a05f55936e685fa6153520df6cad0e684df35c

### tests/security/test_mh04_state_authority_redteam.py
SHA256: 01f2254acfb4cadc04b2f9a9ab25288bde86dc48c9405f2fa805a2f0e2646cb9
