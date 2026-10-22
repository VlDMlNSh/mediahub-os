package runtime

import "testing"

func TestCandidateCannotActivate(t *testing.T) {
	if err := Activate(Candidate); err != ErrActivationDenied {
		t.Fatalf("expected activation denial, got %v", err)
	}
}

func TestQualifiedCanActivate(t *testing.T) {
	if err := Activate(Qualified); err != nil {
		t.Fatalf("expected qualified activation, got %v", err)
	}
}
