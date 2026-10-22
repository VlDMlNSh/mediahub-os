package components

import (
	"context"
	"errors"
)

var ErrUnboundedExecution = errors.New("unbounded OSS execution is forbidden")

// ValidateMediaJob enforces process isolation inputs before FFmpeg or similar
// workers are invoked. Resource enforcement remains an outer runtime concern.
func ValidateMediaJob(job MediaJob) error {
	if job.Input == "" || job.Output == "" || job.TimeoutSeconds <= 0 || job.MaxBytes <= 0 {
		return ErrUnboundedExecution
	}
	return nil
}

func ProcessBounded(ctx context.Context, p MediaProcessor, job MediaJob) error {
	if err := ValidateMediaJob(job); err != nil { return err }
	return p.Process(ctx, job)
}
