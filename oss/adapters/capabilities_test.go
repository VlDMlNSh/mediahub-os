package adapters

import "testing"

func TestSmartHomeAuthorityRequiresSmartHomeCapability(t *testing.T) {
	if err := ValidateContract(Contract{Capability: CapabilitySmartHome, Authority: SmartHomeDomain}); err != nil {
		t.Fatalf("expected Smart Home contract: %v", err)
	}
	if err := ValidateContract(Contract{Capability: CapabilityPersistence, Authority: SmartHomeDomain}); err != ErrForbiddenAuthority {
		t.Fatalf("expected invalid authority/capability pair to fail: %v", err)
	}
}

func TestStateMutationRequiresMediaHubAuthority(t *testing.T) {
	if err := ValidateContract(Contract{Capability: CapabilityPersistence, Authority: MediaHubState, MutatesState: true}); err != nil {
		t.Fatalf("expected governed persistence contract: %v", err)
	}
	if err := ValidateContract(Contract{Capability: CapabilityPersistence, Authority: NoAuthority, MutatesState: true}); err != ErrForbiddenAuthority {
		t.Fatalf("expected state mutation without authority to fail: %v", err)
	}
}

func TestProcessingCapabilityIsNonAuthoritative(t *testing.T) {
	if err := ValidateContract(Contract{Capability: CapabilityMediaProcess}); err != nil {
		t.Fatalf("expected non-authoritative media contract: %v", err)
	}
}
