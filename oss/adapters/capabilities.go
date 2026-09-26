package adapters

// Capability is intentionally a MediaHub concept, not an upstream product API.
type Capability string

const (
	CapabilitySmartHome      Capability = "smart-home"
	CapabilityPersistence    Capability = "persistence"
	CapabilityVector         Capability = "vector"
	CapabilityOCR            Capability = "ocr"
	CapabilityVision         Capability = "vision"
	CapabilityInference      Capability = "inference"
	CapabilityLocalLLM       Capability = "local-llm"
	CapabilityTelemetry      Capability = "telemetry"
	CapabilityMetrics        Capability = "metrics"
	CapabilityArtifactTrust  Capability = "artifact-trust"
	CapabilitySBOM           Capability = "sbom"
	CapabilityVulnerability  Capability = "vulnerability"
	CapabilityBackup         Capability = "backup"
	CapabilityUpdate         Capability = "update"
	CapabilitySecretConfig   Capability = "secret-config"
	CapabilityContracts      Capability = "contracts"
	CapabilityRPC            Capability = "rpc"
	CapabilityMediaProcess   Capability = "media-process"
	CapabilityBIM            Capability = "bim"
)

// Contract declares the boundary an adapter implements.
type Contract struct {
	Capability Capability
	Authority  AuthorityDomain
	MutatesState bool
	NetworkEgress bool
	Subprocess bool
}

// ValidateContract enforces the architectural invariant that only explicitly
// approved domain authorities can mutate canonical state.
func ValidateContract(c Contract) error {
	if c.MutatesState && c.Authority != MediaHubState {
		return ErrForbiddenAuthority
	}
	if c.Authority == SmartHomeDomain && c.Capability != CapabilitySmartHome {
		return ErrForbiddenAuthority
	}
	return nil
}
