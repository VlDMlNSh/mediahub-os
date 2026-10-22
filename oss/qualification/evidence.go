package qualification

import "errors"

type Stage string

const (
	Inventory Stage = "inventory"
	Provenance Stage = "provenance"
	License Stage = "license"
	SBOM Stage = "sbom"
	Vulnerability Stage = "vulnerability"
	Contract Stage = "contract"
	Functional Stage = "functional"
	Negative Stage = "negative"
	Degraded Stage = "degraded"
	Recovery Stage = "recovery"
	Performance Stage = "performance"
	Rollback Stage = "rollback"
	IndependentReview Stage = "independent-review"
)

var ErrIncompleteEvidence = errors.New("qualification evidence incomplete")

// Evidence is MediaHub-owned qualification state. An upstream project cannot
// mark itself qualified.
type Evidence struct {
	ComponentID string
	Version string
	Stages map[Stage]bool
}

func (e Evidence) Qualified() bool {
	if e.ComponentID == "" || e.Version == "" { return false }
	for _, s := range []Stage{Inventory, Provenance, License, SBOM, Vulnerability, Contract, Functional, Negative, Degraded, Recovery, Performance, Rollback, IndependentReview} {
		if !e.Stages[s] { return false }
	}
	return true
}

func (e Evidence) Validate() error {
	if !e.Qualified() { return ErrIncompleteEvidence }
	return nil
}
