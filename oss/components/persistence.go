package components

import (
	"context"
	"errors"
)

var ErrPersistenceGated = errors.New("persistence component is target-gated and cannot activate in MH-03 foundation")

// Transaction is the MediaHub-owned transaction boundary. Implementations may
// use PostgreSQL, but schema, invariants and authorization remain MediaHub-owned.
type Transaction interface {
	Commit(ctx context.Context) error
	Rollback(ctx context.Context) error
}

type Persistence interface {
	Contract
	Begin(ctx context.Context) (Transaction, error)
	Migrate(ctx context.Context, target string) error
}

type VectorStore interface {
	Contract
	Upsert(ctx context.Context, namespace string, id string, vector []float32) error
	Delete(ctx context.Context, namespace string, id string) error
}

// PersistenceActivation documents the current frozen runtime boundary.
func PersistenceActivation(enabled bool) error {
	if !enabled { return ErrPersistenceGated }
	return nil
}
