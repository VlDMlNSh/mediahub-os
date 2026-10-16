package observability

import "context"

type Metrics interface {
	Counter(name string, value int64)
	Gauge(name string, value float64)
}

type Tracer interface {
	Start(ctx context.Context, name string) (context.Context, func())
}

// Observability is strictly non-authoritative: implementations must not mutate
// MediaHub state or become recovery/state authorities.
type Boundary struct{}
