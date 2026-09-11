package adapters

import "context"

type Persistence interface {
	Component() Component
	Ping(ctx context.Context) error
	Begin(ctx context.Context) (Transaction, error)
}

type Transaction interface {
	Commit(ctx context.Context) error
	Rollback(ctx context.Context) error
}

type Backup interface {
	Component() Component
	Create(ctx context.Context, destination string) error
	Verify(ctx context.Context, snapshot string) error
	Restore(ctx context.Context, snapshot string) error
}
