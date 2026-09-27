# P8.4 — Bounded-agent security reconciliation

Status: SECURITY_RECONCILIATION / P8.4 NOT CLOSED

## Scope

This artifact records deterministic repository evidence for bounded-agent security surfaces: subprocess and network-egress controls, sandbox isolation, forbidden capabilities, and State Authority construction boundaries. It distinguishes static and negative-test evidence from runtime qualification and does not claim closure where runtime or external qualification is absent.

## Security classification

- AI adapter and Astra gateway surfaces: inspected for bounded execution and authorization boundaries.
- Cloud Development sandbox: inspected for isolation and forbidden-capability controls.
- Native execution and agent launcher: inspected for bounded subprocess/provider launch constraints.
- MH-05 reachability/bypass tests: inspected as negative security evidence; reachability is not treated as authorization.
- State Authority red-team tests: inspected for construction and mutation-boundary protection.
- Runtime/external-provider qualification: NOT established by this repository-only reconciliation.

## Closure

P8.4 remains OPEN until the required security surfaces have deterministic acceptance coverage including any uncovered runtime, endpoint, credential, persistence, or authority-escalation paths.

## Source evidence


### ops/ai/ai_adapter.py
SHA256: ff3261a2e5386e350d0b0372d46e2c8c5d93d37da0eec2f866631d9e2f021272
### ops/ai/astra_host_execution_gate.py
SHA256: 964ba2e0b8bd02b41f574b756aa5867c3c0312bdd10d7f9924c8bc92a0b096e1
### ops/ai/astra_host_gateway.py
SHA256: 1431fbe54ad012ed5920ee4ffae336d2824f795f8fbd3fa2e991e79331d65b74
### ops/ai/astra_task_gateway.py
SHA256: d6aed36847d7ca3adc34e33f2d01e556f9c575222fd33a2d272c59da88aeae6d
### ops/cloud_development_sandbox.py
SHA256: 45275dbc2732b3efe274491549b27b632dbb6b21e27efda004db568a8d4911ff
### ops/mediahub_native_execution.py
SHA256: db7e67d988bb19a2c0b88bdf29ccda4a7b578df92e08da1f001f346213400a5a
### ops/mediahub_native_agent_launcher.py
SHA256: a14a6d0428c10ca551b4363fa8ed57d04947e77a951985562c05a4ec90ce923f
### tests/security/test_ai_adapter.py
SHA256: 006a86b1f16ecb3a5f24b715ae9be5200369558cf62a14b45a3e59bca1acda30
### tests/security/test_native_agent_launcher.py
SHA256: 5553b0d88a086216df22993527a05f55936e685fa6153520df6cad0e684df35c
### tests/security/test_cloud_development_sandbox.py
SHA256: 6f0bed8a5b265f6a4d21f790e1898ce41552974c497bc7a06804f7eb9437628d
### tests/security/test_mh05_bypass_audit.py
SHA256: 02dda13b842ebfa1190e40a1bc41e94fa74f7e92afb695c453cf239ae402ad78
### tests/security/test_mh05_systemwide_reachability.py
SHA256: 09ae4c2c39621836f1639e34fe8c1ac22c209cf2e2ba27b951adb8ef13786bee
### tests/security/test_mh04_state_authority_redteam.py
SHA256: 01f2254acfb4cadc04b2f9a9ab25288bde86dc48c9405f2fa805a2f0e2646cb9
