package adapters

import "testing"

func TestHomeAssistantAuthorityIsDomainBound(t *testing.T) {
	if err := ValidateAuthority("home-assistant-core", SmartHomeDomain); err != nil {
		t.Fatalf("expected Smart Home authority to be accepted: %v", err)
	}
	if err := ValidateAuthority("home-assistant-core", MediaHubState); err != ErrForbiddenAuthority {
		t.Fatalf("expected State Authority escalation to be rejected: %v", err)
	}
}

func TestOtherComponentsHaveNoAuthority(t *testing.T) {
	if err := ValidateAuthority("postgresql", NoAuthority); err != nil {
		t.Fatalf("expected no authority to be accepted: %v", err)
	}
	if err := ValidateAuthority("postgresql", MediaHubState); err != ErrForbiddenAuthority {
		t.Fatalf("expected persistence authority escalation to be rejected: %v", err)
	}
}
