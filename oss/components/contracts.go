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
	Observability Capability = "observability"
	Persistence Capability = "persistence"
	Backup Capability = "backup"
	SmartHome Capability = "smart-home"
	MediaProcessing Capability = "media-processing"
	OCR Capability = "ocr"
	ComputerVision Capability = "computer-vision"
	LocalInference Capability = "local-inference"
	DigitalTwin Capability = "digital-twin"
)
