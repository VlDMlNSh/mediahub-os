package components

import "context"

type InferenceRequest struct { Model string; Input []byte; MaxTokens int; TimeoutSeconds int }
type InferenceResult struct { Output []byte; Model string }
type LocalInference interface { Contract; Infer(context.Context, InferenceRequest) (InferenceResult, error) }

// AI routing is owned by MediaHub. An inference runtime never decides escalation.
type AIRouter interface {
	Local(context.Context, InferenceRequest) (InferenceResult, error)
	CanEscalate() bool
}
