# P9.3 — Egress and endpoint allowlist audit

Status: NETWORK_SECURITY_RECONCILIATION / P9.3 NOT CLOSED

## Scope

Deterministic repository audit of existing egress gates, endpoint validation and allowlist evidence. No live network requests are performed. Reachability is not treated as authorization.

## Findings

- Architecture documents define controlled outbound egress and default-deny/allowlist expectations.
- Repository implementation contains egress admission and endpoint validation surfaces that are reviewed below.
- Static evidence does not prove every runtime destination is constrained, nor does it establish external endpoint availability or certificate behavior.
- P9.3 remains OPEN until all production-relevant egress paths have explicit allowlist acceptance evidence and uncovered paths are classified.

## Source evidence

### docs/architecture/MH-21-network-boundary.md
SHA256: 5cab151b01adf189641e2dee36419764118dad35a59358623ec9f53540a57330
- L5: Conceptual topology: MediaHub Core Network → Controlled Egress → External Compute Network → Provider Network → Internet. Prefer controlled outbound communication and minimize inbound exposure. Network reachability never grants business authorization.

### docs/architecture/MH-21-data-egress.md
SHA256: d6a2e980a0237748475f8aa5506b6d19530aa7eb4f5b292fd775e7a56c9fea2e
- L1: # MH-21 Data Egress Gate
- L7: Default: deny arbitrary egress. AI output, plugin configuration, retrieved documents and external events cannot select arbitrary destinations. Sensitive/private data requires explicit eligibility and authorization. Secrets are prohibited unless a separate narrowly scoped contract explicitly permits them.

### ops/mediahub_egress_controller.py
SHA256: 89d9d3dc73b974ee0ba2bdd66840c81d3f3e8304cb74d25c8b8dd5e83aef9c27
- L1: """Explicit destination allowlist for MediaHub autonomous development."""
- L8: class EgressDenied(PermissionError):
- L13: class EgressPolicy:
- L19: raise EgressDenied("malformed egress destinations")
- L21: raise EgressDenied("invalid egress destination limit")
- L24: class EgressController:
- L25: policy: EgressPolicy
- L31: raise EgressDenied("egress controller is revoked")
- L33: raise EgressDenied("egress policy is too broad")
- L42: def admit(self, destination: str) -> None:
- L44: raise EgressDenied("egress is not authorized")
- L47: raise EgressDenied("destination is not allowlisted")
- L53: raise EgressDenied("only HTTPS destinations with a hostname are allowed")
- L55: raise EgressDenied("userinfo in destination is forbidden")
- L57: raise EgressDenied("query and fragment are forbidden in policy destinations")

### ops/hybrid_cloud_api_egress_adapter.py
SHA256: d2c33a6f473a27f71256006efcac74d3ce7794b86071473be4c62e76ee055229
- L1: """Fail-closed Cloud API egress over an externally managed VPN tunnel.
- L5: interface before cloud traffic is admitted. All other traffic remains direct.
- L14: from ops.mediahub_egress_controller import EgressController
- L18: """Raised when the required VPN-backed egress is unavailable."""
- L35: class HybridCloudAPIEgressAdapter:
- L36: egress: EgressController
- L58: self.egress.authorize()
- L64: raise CloudAPIUnavailable("malformed hybrid egress request")
- L66: raise CloudAPIUnavailable("malformed hybrid egress request")
- L68: raise CloudAPIUnavailable("malformed hybrid egress request")
- L70: raise CloudAPIUnavailable("malformed hybrid egress request")
- L71: self.egress.admit(url)
- L77: with urlopen(request, timeout=self.timeout_seconds) as response:  # nosec B310 — HTTPS-only URL admitted by EgressController

### ops/hybrid_cloud_egress.py
SHA256: 957eb9228e8ca055c9786741e2091b4a8c31e1f2edebe35101c30f9c3cc3640b
- L1: """Fail-closed egress selector for the hybrid development system."""
- L12: from ops.hybrid_cloud_api_egress_adapter import CloudAPIUnavailable
- L31: class HybridCloudEgressAdapter:
- L52: raise CloudAPIUnavailable("health endpoint must be HTTPS")

### ops/hybrid_cloud_egress_chain.py
SHA256: 069f42cf613f652859c1a409940c5991210969c571cf3337672522daf053ba7d
- L1: """Deterministic, sticky fail-closed selection of approved cloud egress paths."""
- L7: from ops.hybrid_cloud_api_egress_adapter import CloudAPIUnavailable, TunnelStatus
- L11: class EgressPath:
- L18: class HybridCloudAPIEgressChain:
- L19: paths: tuple[EgressPath, ...]
- L35: raise CloudAPIUnavailable("all approved cloud egress paths are unhealthy")
- L38: def active(self) -> EgressPath | None:

### tests/test_mediahub_egress_controller.py
SHA256: 79c668785a557224d54141991750cfa058db7f37566ef5025569e3d174674a46
- L3: from ops.mediahub_egress_controller import EgressController, EgressDenied, EgressPolicy
- L6: def test_egress_is_fail_closed():
- L7: controller = EgressController(EgressPolicy(frozenset({"https://api.example.com"})))
- L8: with pytest.raises(EgressDenied):
- L9: controller.admit("https://api.example.com")
- L12: def test_allowlisted_destination_is_admitted():
- L13: controller = EgressController(EgressPolicy(frozenset({"https://api.example.com"})))
- L15: controller.admit("https://api.example.com")
- L19: controller = EgressController(EgressPolicy(frozenset({"https://api.example.com"})))
- L21: for destination in ("https://other.example.com", "http://api.example.com"):
- L22: with pytest.raises(EgressDenied):
- L23: controller.admit(destination)
- L28: "https://user:pass@example.com",
- L29: "https://example.com/?token=secret",
- L30: "https://example.com/#fragment",
- L32: controller = EgressController(EgressPolicy(frozenset({destination})))
- L33: with pytest.raises(EgressDenied):
- L38: destinations = frozenset(f"https://{i}.example.com" for i in range(17))
- L39: controller = EgressController(EgressPolicy(destinations))
- L40: with pytest.raises(EgressDenied):
- L45: controller = EgressController(EgressPolicy(frozenset({"https://api.example.com"})))
- L47: with pytest.raises(EgressDenied):
- L50: def test_egress_policy_rejects_malformed_types():
- L51: with pytest.raises(EgressDenied):
- L52: EgressPolicy({"https://example.test"})
- L53: with pytest.raises(EgressDenied):
- L54: EgressPolicy(frozenset({1}))
- L55: with pytest.raises(EgressDenied):
- L56: EgressPolicy(frozenset(), True)

### tests/test_hybrid_cloud_api_egress_adapter.py
SHA256: 322574f41acaa772a3529592f8917e6802241259dd316eb2fea4e666e828e07f
- L7: from ops.hybrid_cloud_api_egress_adapter import (
- L9: HybridCloudAPIEgressAdapter,
- L11: from ops.mediahub_egress_controller import EgressController, EgressDenied, EgressPolicy
- L13: API = "https://api.example.test"
- L16: def adapter(*, interface: str = "tun-vpm") -> HybridCloudAPIEgressAdapter:
- L17: controller = EgressController(EgressPolicy(frozenset({API})))
- L18: return HybridCloudAPIEgressAdapter(controller, tunnel_interface=interface)
- L27: def test_destination_not_allowlisted_is_denied() -> None:
- L29: with patch.object(client, "check_tunnel", return_value=client.check_tunnel()), pytest.raises(EgressDenied):
- L30: client.request("https://not-allowed.example.test")
- L36: with patch.object(client, "check_tunnel", return_value=healthy), patch("ops.hybrid_cloud_api_egress_adapter.urlopen") as open_url:
- L48: with patch.object(client, "check_tunnel", return_value=healthy), patch("ops.hybrid_cloud_api_egress_adapter.urlopen", side_effect=OSError("down")):
