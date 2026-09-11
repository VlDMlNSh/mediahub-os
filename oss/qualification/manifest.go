package qualification

import (
	"encoding/json"
	"fmt"
	"os"
)

type Manifest struct {
	SchemaVersion int         `json:"schema_version"`
	Policy        string      `json:"policy"`
	Requires      []string    `json:"activation_requires"`
	Components    []Component `json:"components"`
}

type Component struct {
	ID         string          `json:"id"`
	Version    *string         `json:"version"`
	Status     string          `json:"status"`
	Authority  string          `json:"authority,omitempty"`
	Provenance string          `json:"provenance,omitempty"`
	Evidence   map[string]bool `json:"evidence"`
}

func LoadManifest(path string) (Manifest, error) {
	data, err := os.ReadFile(path)
	if err != nil { return Manifest{}, err }
	var m Manifest
	if err := json.Unmarshal(data, &m); err != nil { return Manifest{}, err }
	if err := m.Validate(); err != nil { return Manifest{}, err }
	return m, nil
}

func (m Manifest) Validate() error {
	if m.SchemaVersion != 1 { return fmt.Errorf("unsupported schema_version: %d", m.SchemaVersion) }
	if m.Policy != "fail-closed" { return fmt.Errorf("policy must be fail-closed") }
	if len(m.Components) == 0 { return fmt.Errorf("manifest has no components") }
	seen := make(map[string]bool, len(m.Components))
	for _, c := range m.Components {
		if c.ID == "" { return fmt.Errorf("component id is required") }
		if seen[c.ID] { return fmt.Errorf("duplicate component: %s", c.ID) }
		seen[c.ID] = true
		if c.Status == "active" {
			if c.Version == nil || *c.Version == "" { return fmt.Errorf("active component %s has no exact version", c.ID) }
			if !c.Evidence["version"] { return fmt.Errorf("active component %s missing version evidence", c.ID) }
			for _, req := range m.Requires {
				key := req
				switch req {
				case "exact-version-or-immutable-digest": key = "version"
				case "mediahub-adapter": key = "adapter"
				case "vulnerability-report": key = "vulnerability"
				case "degraded-recovery-tests": key = "degraded"
				}
				if !c.Evidence[key] { return fmt.Errorf("active component %s missing evidence: %s", c.ID, req) }
			}
		}
	}
	return nil
}
