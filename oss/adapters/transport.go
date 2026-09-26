package adapters

import "context"

type Transport interface {
	Component() Component
	Publish(ctx context.Context, subject string, payload []byte) error
	Subscribe(ctx context.Context, subject string, handler func([]byte) error) (Subscription, error)
}

type Subscription interface { Close() error }

type Coordination interface {
	Component() Component
	Lease(ctx context.Context, key string, ttlSeconds int) (Lease, error)
}

type Lease interface { Release(ctx context.Context) error }
