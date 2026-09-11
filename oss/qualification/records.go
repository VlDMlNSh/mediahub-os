package qualification

import (
	"fmt"
	"os"
	"strings"
)

// RecordsFile is the minimal structural model of qualification-records.yaml.
// YAML parsing is intentionally not implemented here: the repository keeps
// this file human-readable, while qualification decisions are enforced by the
// canonical JSON manifest and this invariant checker.
type RecordsFile struct {
	SchemaVersion int
	Policy        string
	Raw           string
}

func LoadRecordsFile(path string) (RecordsFile, error) {
	data, err := os.ReadFile(path)
	if err != nil {
		return RecordsFile{}, err
	}
	r := RecordsFile{Raw: string(data)}
	for _, line := range strings.Split(r.Raw, "\n") {
		line = strings.TrimSpace(line)
		switch {
		case strings.HasPrefix(line, "schema_version:"):
			if _, err := fmt.Sscanf(line, "schema_version: %d", &r.SchemaVersion); err != nil {
				return RecordsFile{}, fmt.Errorf("invalid schema_version: %w", err)
			}
		case strings.HasPrefix(line, "policy:"):
			r.Policy = strings.TrimSpace(strings.TrimPrefix(line, "policy:"))
		}
	}
	if r.SchemaVersion != 1 {
		return RecordsFile{}, fmt.Errorf("unsupported qualification records schema_version: %d", r.SchemaVersion)
	}
	if r.Policy != "fail-closed" {
		return RecordsFile{}, fmt.Errorf("qualification records policy must be fail-closed")
	}
	if !strings.Contains(r.Raw, "records:") {
		return RecordsFile{}, fmt.Errorf("qualification records section is missing")
	}
	return r, nil
}

func (r RecordsFile) ValidateAuthorityInvariants() error {
	if strings.Contains(r.Raw, "authority: second-state-authority") || strings.Contains(r.Raw, "authority: alternate-state-authority") {
		return fmt.Errorf("alternate State Authority is forbidden")
	}
	if strings.Contains(r.Raw, "authority: production-ota") {
		lines := strings.Split(r.Raw, "\n")
		for i, line := range lines {
			if strings.TrimSpace(line) == "authority: production-ota" && i > 0 {
				id := ""
				for j := i - 1; j >= 0 && j >= i-5; j-- {
					if strings.HasPrefix(strings.TrimSpace(lines[j]), "id: ") {
						id = strings.TrimSpace(strings.TrimPrefix(strings.TrimSpace(lines[j]), "id: "))
						break
					}
				}
				if id != "rauc" {
					return fmt.Errorf("production OTA authority must be rauc, got %s", id)
				}
			}
		}
	}
	return nil
}
