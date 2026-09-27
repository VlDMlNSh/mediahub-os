# P7.4 — Ordinary-user Cloud Development AI access boundary

Status: DISCOVERY_RECONCILIATION / P7.4 NOT CLOSED

## Scope

This artifact records deterministic repository evidence for the existing requirement that ordinary users have no direct corporate Cloud Development AI access. It distinguishes repository policy declarations from executable enforcement evidence. It does not invent authentication, UI, provider, or production-authorization semantics.

## Deterministic classification

- Policy/declaration evidence: PRESENT where the source excerpts below explicitly describe Cloud Development AI, ordinary-user access, or controlled escalation.
- Executable ordinary-user access enforcement: NOT ESTABLISHED by this reconciliation alone; the inspected adapter/test surfaces are generic Cloud Development controls and are not treated as proof of an ordinary-user-specific access gate.
- Overall P7.4 status: PARTIAL — policy boundary is documented, while ordinary-user-specific executable acceptance is not demonstrated by the inspected evidence.

## Source evidence

### specification/MEDIAHUB-FUNCTIONAL-BASELINE-1.0.md
SHA256: 9cab7f0518208ecaeae8f605785a9e25eb9ed1ae9db420b19898fe83059dc18a
- 31: → Mobile Access Layer / Cloud Development AI → controlled development infrastructure.
- 115: **Mobile Access Layer → Local AI → Local Cluster AI → Cloud Development AI**.
- 124: Cloud Development AI — корпоративная облачная вычислительная среда MediaHub. Обычные пользователи
- 126: local resources и при policy, privacy, authorization, residency и egress controls.
- 134: Trusted Sources Intelligence Engine — first-class Cloud Development AI subsystem:
- 143: AI Human Clone — отдельная Cloud Development AI subsystem для авторизованного media content:
- 146: Обязательны consent, authorization, identity provenance, rights-holder authorization, scope,
- 147: voice/appearance authorization, model/asset provenance, audit, revocation и separation

### specification/MEDIAHUB-FUNCTIONAL-BASELINE-GOVERNANCE.yaml
SHA256: 0160f24d3364d44b33aadc330be1519b99b61af4a3941400563caaf4d9576b4b
- 15: - production_requires_explicit_authorization
- 24: cloud_development: Cloud Development AI
- 36: - Cloud Development AI

### specification/invariant-registry.yaml
SHA256: a73fc89921980839622d586f19c5b5499a03c14036fcb670daff015b102ac4fc
- 8: - INV-005: Authentication does not equal Authorization
- 9: - INV-006: Remote access does not increase authorization
- 23: - INV-020: Physical connection does not grant authorization
- 27: - INV-024: Health, Readiness, Liveness, Trust and Authorization remain distinct
- 28: - INV-025: Internal storage/processing/routing topology is hidden from ordinary users
- 46: - INV-042: Production remains unauthorized until explicit production authorization
- 49: - INV-045: AI escalation order is Mobile Access Layer → Local AI → Local Cluster AI → Cloud Development AI

### recovery/acceptance/F-009-remote-access-mobile-and-cloud-escalation.md
SHA256: ae5861d74451dff765063c5bd4693351e5bf9eb05aa81b93daf715ef1dc6ee05
- 15: - Subject to authorization, MediaHub User may access Smart Home, devices, rooms/zones, automations, scenes, schedules, notifications, history, surveillance, local MediaHub Cluster functions, Personal Media Library, permitted multimedia functions, energy functions and permitted diagnostics/other user functions.
- 16: - The exact function surface remains subject to the user's authorization scope.
- 35: - The cloud execution mechanism, routing and distribution remain internal system behavior and are hidden from ordinary users.
- 59: - Remote access does not increase user authorization.

### ops/cloud_development_adapter.py
SHA256: 2ef2e8d4843d36ac219f19acfbf6de811f5183354cbfe9d97ae9c35dafb7dad2
- 15: from ops.mediahub_credential_broker import CredentialBroker
- 68: The adapter never receives provider credentials. Harness CLIs are invoked
- 134: broker_credential_env=frozenset())
- 138: broker_credential_env: frozenset[str] = frozenset()) -> ProviderResult:
- 152: if ("KEY" in key or "TOKEN" in key or "SECRET" in key or "PASSWORD" in key) and key not in broker_credential_env:
- 153: raise AdapterDenied("provider credentials must remain outside the adapter")
- 260: broker: CredentialBroker, registry: ModelRegistry,
- 270: credential_env = broker.environment(spec.provider, spec.credential_env)

### tests/ops/test_cloud_development_adapter.py
SHA256: 1d0313c410dc43fb34da64171525bfe93f766e9764ad57465985834109596cef
- 57: for data_class in ("credential", "production", "pii", "internal", "unknown"):
- 215: from ops.mediahub_credential_broker import CredentialBroker
- 218: credential_dir = tmp_path / "credentials"
- 219: credential_dir.mkdir()
- 220: credential = credential_dir / "mediahub-openai"
- 221: credential.write_text("synthetic-secret", encoding="utf-8")
- 222: credential.chmod(0o600)
- 223: broker = CredentialBroker(credential_dir, frozenset({"openai"}))
