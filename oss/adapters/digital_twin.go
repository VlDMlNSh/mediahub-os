package adapters

import "context"

type DigitalTwin interface {
	Component() Component
	Import(ctx context.Context, artifact []byte) (TwinArtifact, error)
}

type TwinArtifact struct {
	ID string
	Format string
	SourceDigest string
}

type EngineeringArtifact interface {
	Validate(ctx context.Context, artifact TwinArtifact) error
}
