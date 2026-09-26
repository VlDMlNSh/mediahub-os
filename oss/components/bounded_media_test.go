package components

import "testing"

func TestValidateMediaJob(t *testing.T) {
	if ValidateMediaJob(MediaJob{} ) == nil { t.Fatal("expected bounded execution rejection") }
	if err := ValidateMediaJob(MediaJob{Input:"in", Output:"out", TimeoutSeconds:30, MaxBytes:1024}); err != nil { t.Fatal(err) }
}
