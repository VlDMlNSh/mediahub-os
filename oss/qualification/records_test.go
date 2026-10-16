package qualification

import "testing"

func TestCommittedQualificationRecordsAreFailClosed(t *testing.T) {
	r, err := LoadRecordsFile("qualification-records.yaml")
	if err != nil {
		t.Fatalf("qualification records must load: %v", err)
	}
	if err := r.ValidateAuthorityInvariants(); err != nil {
		t.Fatalf("qualification authority invariants must hold: %v", err)
	}
}

func TestQualificationRecordsRejectAlternateStateAuthority(t *testing.T) {
	r := RecordsFile{SchemaVersion: 1, Policy: "fail-closed", Raw: "schema_version: 1\npolicy: fail-closed\nrecords:\n  - id: bad\n    authority: alternate-state-authority\n"}
	if err := r.ValidateAuthorityInvariants(); err == nil {
		t.Fatal("expected alternate State Authority to be rejected")
	}
}
