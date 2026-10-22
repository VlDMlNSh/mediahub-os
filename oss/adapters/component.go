package adapters

import "context"

// Status is intentionally independent from upstream component lifecycle.
type Status string

const (
	Disabled   Status = "disabled"
	Candidate  Status = "candidate"
	Qualified  Status = "qualified"
	Active     Status = "active"
)

// Component identifies a bounded upstream dependency without exposing its
// internal data model to MediaHub domains.
type Component struct {
	ID         string
	Version    string
	Provenance string
	License    string
	Status     Status
}

// Adapter is the minimum MediaHub-owned boundary for an OSS runtime.
type Adapter interface {
	Component() Component
	Health(ctx context.Context) error
	Start(ctx context.Context) error
	Stop(ctx context.Context) error
}

// Guard prevents unqualified components from being activated.
func Guard(c Component) error {
	if c.ID == "" || c.Version == "" || c.Provenance == "" || c.License == "" {
		return ErrIncompleteMetadata
	}
	if c.Status != Qualified && c.Status != Active {
		return ErrNotQualified
	}
	return nil
}
