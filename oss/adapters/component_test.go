package adapters

import "testing"

func TestGuardRejectsIncompleteMetadata(t *testing.T) {
	err := Guard(Component{ID: "postgresql", Version: "18", Status: Qualified})
	if err != ErrIncompleteMetadata {
		t.Fatalf("expected incomplete metadata error, got %v", err)
	}
}

func TestGuardRejectsUnqualifiedComponent(t *testing.T) {
	err := Guard(Component{
		ID:         "postgresql",
		Version:    "18",
		Provenance: "upstream",
		License:    "PostgreSQL",
		Status:     Candidate,
	})
	if err != ErrNotQualified {
		t.Fatalf("expected qualification error, got %v", err)
	}
}

func TestGuardAcceptsQualifiedComponent(t *testing.T) {
	err := Guard(Component{
		ID:         "opentelemetry",
		Version:    "pinned",
		Provenance: "upstream",
		License:    "Apache-2.0",
		Status:     Qualified,
	})
	if err != nil {
		t.Fatalf("expected qualified component, got %v", err)
	}
}
