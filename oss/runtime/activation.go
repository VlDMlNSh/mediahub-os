package runtime

import "errors"

type Status string

const (
	Disabled  Status = "disabled"
	Candidate Status = "candidate"
	Qualified Status = "qualified"
	Active    Status = "active"
)

var ErrActivationDenied = errors.New("OSS runtime activation denied: qualification required")

// Activate performs the final local gate. Release authorization remains
// outside this package and is never delegated to an OSS component.
func Activate(status Status) error {
	if status != Qualified && status != Active {
		return ErrActivationDenied
	}
	return nil
}
