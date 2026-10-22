package components

import "context"

type UpdateBundle struct { Version string; Digest string; Signature string }
type UpdateManager interface { Contract; Verify(ctx context.Context, bundle UpdateBundle) error; Stage(ctx context.Context, bundle UpdateBundle) error; Activate(ctx context.Context, bundle UpdateBundle) error; Rollback(ctx context.Context) error }

// RAUC is the target OTA authority. No Mender/second production OTA authority is exposed here.
