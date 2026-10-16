package adapters

import "context"

type SmartHome interface {
	Component() Component
	Health(ctx context.Context) error
	Execute(ctx context.Context, command []byte) ([]byte, error)
}

// State Authority remains MediaHub-owned. This adapter is deliberately scoped
// to the Smart Home domain and cannot expose platform state mutation.
type SmartHomeBoundary struct { ComponentID string }

func (b SmartHomeBoundary) AuthorityDomain() AuthorityDomain { return SmartHomeDomain }
