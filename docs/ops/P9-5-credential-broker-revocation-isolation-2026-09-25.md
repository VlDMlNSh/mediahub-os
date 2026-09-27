# P9.5 — Credential broker revocation / isolation evidence

Status: SECURITY_RECONCILIATION / P9.5 NOT CLOSED

Scope: repository-local evidence only. Do not read or emit credential values, invoke providers, create credentials, or grant production authorization.

Verification command: `pytest -q tests/test_mediahub_credential_broker.py tests/security/test_native_agent_launcher.py`

Review boundary: credential broker, native execution admission and native launcher negative tests. This record does not claim external secret-store, cloud-provider, rotation-service or production revocation qualification.

Source evidence: `ops/mediahub_credential_broker.py`, `tests/test_mediahub_credential_broker.py`, `ops/mediahub_native_execution.py`, `tests/security/test_native_agent_launcher.py`.
