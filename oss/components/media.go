package components

import "context"

type MediaJob struct { Input string; Output string; TimeoutSeconds int; MaxBytes int64 }
type MediaProcessor interface { Contract; Process(context.Context, MediaJob) error }

type OCRDocument struct { ID string; Text string; Confidence float32 }
type OCR interface { Contract; Extract(context.Context, string) (OCRDocument, error) }

type Image struct { ID string; Width int; Height int; Format string }
type ComputerVision interface { Contract; Analyze(context.Context, Image) (map[string]string, error) }
