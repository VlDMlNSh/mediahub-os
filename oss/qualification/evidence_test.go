package qualification

import "testing"

func completeEvidence() Evidence {
	stages := map[Stage]bool{}
	for _, s := range []Stage{Inventory, Provenance, License, SBOM, Vulnerability, Contract, Functional, Negative, Degraded, Recovery, Performance, Rollback, IndependentReview} { stages[s] = true }
	return Evidence{ComponentID: "example", Version: "1.0.0", Stages: stages}
}

func TestIncompleteEvidenceFailsClosed(t *testing.T) {
	e := completeEvidence(); e.Stages[IndependentReview] = false
	if e.Validate() == nil { t.Fatal("expected incomplete evidence to fail") }
}

func TestCompleteEvidenceQualifies(t *testing.T) {
	if err := completeEvidence().Validate(); err != nil { t.Fatalf("unexpected qualification failure: %v", err) }
}
