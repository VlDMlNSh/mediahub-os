package components

import "context"

type TwinObject struct { ID string; IFCType string; Properties map[string]string }
type DigitalTwin interface { Contract; Load(context.Context, []byte) ([]TwinObject, error) }

type EngineeringArtifact struct { ID string; Kind string; Digest string }
type EngineeringStore interface { Contract; Put(context.Context, EngineeringArtifact, []byte) error; Get(context.Context, string) ([]byte, error) }
