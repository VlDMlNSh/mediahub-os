package qualification

import "testing"

func TestCommittedQualificationManifestIsValid(t *testing.T) {
	m, err := LoadManifest("../manifests/qualification.json")
	if err != nil {
		t.Fatalf("committed qualification manifest must validate: %v", err)
	}
	if len(m.Components) < 2 {
		t.Fatalf("expected mature component inventory, got %d components", len(m.Components))
	}
	for _, c := range m.Components {
		if c.Status == "active" {
			t.Fatalf("committed manifest must not activate component %s without full evidence", c.ID)
		}
	}
}
