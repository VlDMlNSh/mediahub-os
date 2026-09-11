package adapters

// ResourceLimits are MediaHub-owned execution limits for FFmpeg/OpenCV/PaddleOCR
// style workers. The concrete processor contract is defined in adapters/contracts.go.
type ResourceLimits struct {
	MaxBytes int64
	TimeoutSeconds int
	MaxConcurrent int
}

func (r ResourceLimits) Valid() bool {
	return r.MaxBytes > 0 && r.TimeoutSeconds > 0 && r.MaxConcurrent > 0
}
