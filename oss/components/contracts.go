package components

import "context"

// Contract is a bounded MediaHub-owned interface for mature OSS components.
// Upstream types must not cross this boundary into domain state.
type Contract interface {
	ID() string
	Health(context.Context) error
}

// Capability identifies what a component is permitted to provide.
type Capability string

const (
	CapabilityObservability Capability = "observability"
	CapabilityPersistence Capability = "persistence"
	CapabilityBackup Capability = "backup"
	CapabilitySmartHome Capability = "smart-home"
	CapabilityMediaProcessing Capability = "media-processing"
	CapabilityOCR Capability = "ocr"
	CapabilityComputerVision Capability = "computer-vision"
	CapabilityLocalInference Capability = "local-inference"
	CapabilityDigitalTwin Capability = "digital-twin"
)
