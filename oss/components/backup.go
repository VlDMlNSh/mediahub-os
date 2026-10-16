package components

import "context"

type BackupManifest struct {
	Repository string
	SnapshotID string
	ContentDigest string
	CreatedAt string
}

type Backup interface {
	Contract
	Create(ctx context.Context, manifest BackupManifest) error
	Verify(ctx context.Context, snapshotID string) error
	Restore(ctx context.Context, snapshotID string) error
}

// BackupPolicy keeps backup mechanics subordinate to MediaHub recovery policy.
type BackupPolicy struct {
	Retention string
	RequireVerification bool
}
