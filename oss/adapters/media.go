package adapters

import "context"

type MediaProcessor interface {
	Component() Component
	Process(ctx context.Context, input []byte, limits ResourceLimits) ([]byte, error)
}

type ResourceLimits struct {
	MaxBytes int64
	TimeoutSeconds int
	MaxConcurrent int
}

func (r ResourceLimits) Valid() bool {
	return r.MaxBytes > 0 && r.TimeoutSeconds > 0 && r.MaxConcurrent > 0
}
