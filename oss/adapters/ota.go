package adapters

import "context"

type OTA interface {
	Component() Component
	Install(ctx context.Context, bundle []byte) error
	Verify(ctx context.Context, bundle []byte) error
	Rollback(ctx context.Context) error
}

// RAUC is the only production OTA authority. Mender remains reference-only.
type OTAAuthority struct { ComponentID string }

func (a OTAAuthority) IsProductionAuthority() bool { return a.ComponentID == "rauc" }
