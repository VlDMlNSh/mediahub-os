# MH-12 Security Evidence Register

Required record: claim | source | evidence | date | status | confidence | owner | verification method | related ADR | implementation | test.

Current evidence status: architecture claims are derived from the MH-12 baseline and protected P0-03…P0-07 records. Concrete technology, deployment and hardware claims remain REQUIRES VERIFICATION unless separately evidenced.

Never label a system secure, production-ready or qualified without explicit criteria and verification evidence.


- P9.5 credential broker revocation isolation | tests/test_mediahub_credential_broker.py | 7 broker tests; revocation blocks environment materialization and authorize-after-revoke | 2026-09-19 | VERIFIED (local) | high | mh-12 | pytest -q tests/test_mediahub_credential_broker.py tests/security/test_ai_adapter.py tests/security/test_cloud_development_sandbox.py; git diff --check | none | ops/mediahub_credential_broker.py | 20 passed
