package components

import "context"

// HealthAdapter models observational integrations only. It cannot mutate
// MediaHub state or authorize releases.
type HealthAdapter struct { Name string }
func (a HealthAdapter) ID() string { return a.Name }
func (a HealthAdapter) Health(context.Context) error { return nil }

// MetricsSink is intentionally narrow; labels and metric names remain owned by MediaHub.
type MetricsSink interface {
	Observe(name string, value float64, labels map[string]string)
}

// TraceSink accepts already-bounded MediaHub spans; upstream SDK types do not cross the boundary.
type TraceSink interface {
	Record(ctx context.Context, name string, attributes map[string]string) context.Context
}
