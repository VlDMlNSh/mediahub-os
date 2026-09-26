package adapters

import "context"

// PersistenceAdapter isolates PostgreSQL/pgvector behind MediaHub persistence
// semantics. The adapter never owns domain invariants.
type PersistenceAdapter interface {
	Adapter
	Ping(ctx context.Context) error
	Begin(ctx context.Context) (Transaction, error)
}

type Transaction interface {
	Commit(ctx context.Context) error
	Rollback(ctx context.Context) error
}

// SmartHomeAdapter isolates Home Assistant Core. MediaHub remains the platform
// authority; HA is authoritative only inside the Smart Home domain.
type SmartHomeAdapter interface {
	Adapter
	Discover(ctx context.Context) ([]DeviceDescriptor, error)
	Execute(ctx context.Context, command SmartHomeCommand) error
}

type DeviceDescriptor struct {
	ID           string
	Manufacturer string
	Model        string
	Protocol     string
}

type SmartHomeCommand struct {
	DeviceID string
	Action   string
	Payload  []byte
}

// MediaProcessor isolates FFmpeg/OpenCV/PaddleOCR-style processing engines.
// Processing results are proposals/facts and never direct State Authority
// mutations.
type MediaProcessor interface {
	Adapter
	Process(ctx context.Context, request ProcessingRequest) (ProcessingResult, error)
}

type ProcessingRequest struct {
	InputURI string
	Profile  string
}

type ProcessingResult struct {
	OutputURI string
	Metadata  map[string]string
}
