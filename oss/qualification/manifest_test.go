package qualification

import "testing"

func TestManifestValidationRejectsActiveWithoutEvidence(t *testing.T) {
	version := "1.0.0"
	m := Manifest{
		SchemaVersion: 1,
		Policy: "fail-closed",
		Requires: []string{"exact-version-or-immutable-digest", "license-record", "sbom"},
		Components: []Component{{ID: "example", Version: &version, Status: "active", Evidence: map[string]bool{"version": true}}},
	}
	if err := m.Validate(); err == nil { t.Fatal("expected active component without complete evidence to fail") }
}

func TestManifestValidationAllowsGatedPendingComponent(t *testing.T) {
	m := Manifest{
		SchemaVersion: 1,
		Policy: "fail-closed",
		Requires: []string{"exact-version-or-immutable-digest"},
		Components: []Component{{ID: "postgresql", Status: "target-gated", Evidence: map[string]bool{}}},
	}
	if err := m.Validate(); err != nil { t.Fatalf("expected gated component to validate: %v", err) }
}
