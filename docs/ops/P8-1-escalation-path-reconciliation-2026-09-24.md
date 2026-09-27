# P8.1 — AI escalation path reconciliation

Status: DISCOVERY_RECONCILIATION / P8.1 NOT CLOSED

## Scope

This artifact records deterministic repository evidence for the existing escalation path Mobile Access Layer → Local AI → Local Cluster AI → Cloud Development AI. It does not invent routing semantics, add a Mobile AI tier, execute providers, acquire credentials, mutate State Authority, or claim end-to-end closure.

## Deterministic classification

- Mobile Access Layer boundary: inspected from existing repository sources; it remains an access layer, not an AI compute tier.
- Local AI: inspected as an existing repository-local AI surface only.
- Local Cluster AI: absence of an explicit current hop is reported rather than inferred.
- Cloud Development AI: inspected through existing policy/orchestration surfaces without activating a provider.
- End-to-end escalation: NOT ESTABLISHED by this reconciliation alone.

## Source evidence
### specification/MEDIAHUB-FUNCTIONAL-BASELINE-1.0.md
SHA256: 9cab7f0518208ecaeae8f605785a9e25eb9ed1ae9db420b19898fe83059dc18a
- 27: Философия: **Local First → Unified State → Unified UI → AI Assisted → Controlled Cloud Escalation**.
- 31: → Mobile Access Layer / Cloud Development AI → controlled development infrastructure.
- 39: State Authority работает fail-closed. Её отказ не создаёт fallback authority.
- 105: Network: wired/wireless/mesh/VLAN/routing/monitoring/diagnostics/discovery/controlled remote access,
- 114: Mobile Access Layer — не AI tier. Каноническая цепочка:
- 115: **Mobile Access Layer → Local AI → Local Cluster AI → Cloud Development AI**.
- 117: Local AI: local inference, natural language, analysis, assistance, automation assistance,
- 119: Local AI advisory/proposal only и не является State Authority.
- 121: Local Cluster AI — trusted MediaHub Cluster: heavy inference, batch, CV, media, generation,
- 124: Cloud Development AI — корпоративная облачная вычислительная среда MediaHub. Обычные пользователи
- 134: Trusted Sources Intelligence Engine — first-class Cloud Development AI subsystem:
- 143: AI Human Clone — отдельная Cloud Development AI subsystem для авторизованного media content:
### specification/MEDIAHUB-FUNCTIONAL-BASELINE-GOVERNANCE.yaml
SHA256: 0160f24d3364d44b33aadc330be1519b99b61af4a3941400563caaf4d9576b4b
- 24: cloud_development: Cloud Development AI
- 33: - Mobile Access Layer
- 34: - Local AI
- 35: - Local Cluster AI
- 36: - Cloud Development AI
### docs/ops/P5-5-mobile-access-not-ai-compute-gap-reconciliation-2026-09-22.md
SHA256: 6d90524ad1f4d07a550194a95077471d6224ab1b831db91c74fb6fdf233add26
- 1: # P5.5 Mobile Access Layer / AI Compute Boundary Reconciliation
- 7: `P5.5 Validate that Mobile Access Layer is not an AI compute tier.`
- 11: - `contracts/mobile/mobile-api-compatibility.schema.json` — assigns ownership to `MediaHub Mobile Access Layer` and distinguishes `core` and `remote` client roles; no AI compute role is defined.
- 12: - `ops/ai/ai_gateway.py` — describes compute-tier selection and explicitly separates gateway routing from provider execution.
- 13: - `recovery/acceptance/F-009-remote-access-mobile-and-cloud-escalation.md` — defines mobile access/escalation requirements rather than a mobile AI compute tier.
- 15: - `ops/verify_functional_baseline.sh` — checks the canonical escalation sequence `Mobile Access Layer → Local AI → Local Cluster AI → Cloud Development AI`.
- 19: - Mobile Access Layer as separate AI compute tier: ABSENT by contract/baseline.
- 20: - Canonical escalation separation: IMPLEMENTED at repository architecture/baseline level.
- 21: - Direct mobile AI/provider execution authority: ABSENT in inspected surfaces.
### docs/ops/P7-4-ordinary-user-cloud-development-access-gap-reconciliation-2026-09-22.md
SHA256: 72b1b1603c43d3282df4511f8b316ec5380241aa2837daab0f78b70a202cc60d
- 1: # P7.4 — Ordinary-user Cloud Development AI access boundary
- 7: This artifact records deterministic repository evidence for the existing requirement that ordinary users have no direct corporate Cloud Development AI access. It distinguishes repository policy declarations from executable enforcement evidence. It does not invent authentication, UI, provider, or production-authorization semantics.
- 11: - Policy/declaration evidence: PRESENT where the source excerpts below explicitly describe Cloud Development AI, ordinary-user access, or controlled escalation.
- 19: - 31: → Mobile Access Layer / Cloud Development AI → controlled development infrastructure.
- 20: - 115: **Mobile Access Layer → Local AI → Local Cluster AI → Cloud Development AI**.
- 21: - 124: Cloud Development AI — корпоративная облачная вычислительная среда MediaHub. Обычные пользователи
- 23: - 134: Trusted Sources Intelligence Engine — first-class Cloud Development AI subsystem:
- 24: - 143: AI Human Clone — отдельная Cloud Development AI subsystem для авторизованного media content:
- 31: - 24: cloud_development: Cloud Development AI
- 32: - 36: - Cloud Development AI
- 40: - 28: - INV-025: Internal storage/processing/routing topology is hidden from ordinary users
- 42: - 49: - INV-045: AI escalation order is Mobile Access Layer → Local AI → Local Cluster AI → Cloud Development AI
### ops/mediahub_provider_gateway.py
SHA256: 9c10717bc8e2940c548cbb574a0130b5798dd8532ced391cbf857fd670c26ea4
- 1: """MediaHub-native multi-provider gateway primitives.
- 3: LiteLLM is used only as a reference implementation. Production routing here
- 21: class Provider:
- 36: provider: str | None
- 42: class ProviderGateway:
- 43: """Deterministic provider selection with bounded circuit state."""
- 45: def __init__(self, providers: tuple[Provider, ...], *, threshold: int = 2,
- 49: self.providers = tuple(sorted(providers, key=lambda p: p.priority))
- 52: self.circuits = {p.name: Circuit() for p in self.providers}
- 68: def available(self, provider: str, now: float | None = None) -> bool:
- 69: circuit = self.circuits[provider]
- 75: def record(self, provider: str, failure: FailureClass, now: float | None = None) -> None:
### ops/cloud_development_adapter.py
SHA256: 2ef2e8d4843d36ac219f19acfbf6de811f5183354cbfe9d97ae9c35dafb7dad2
- 1: """Provider-neutral, fail-closed bridge for isolated development harnesses."""
- 20: PROVIDERS = frozenset({"codex", "claude"})
- 29: class ProviderProtocolError(RuntimeError):
- 30: """Raised when a provider violates the neutral response contract."""
- 34: class ProviderRequest:
- 36: provider: str
- 55: class ProviderResult:
- 56: provider: str
- 66: """Policy gate plus provider-neutral subprocess execution boundary.
- 68: The adapter never receives provider credentials. Harness CLIs are invoked
- 77: allowed_providers: frozenset[str] = PROVIDERS
- 92: def admit(self, request: ProviderRequest) -> None:
