package adapters

import "errors"

var (
	ErrIncompleteMetadata = errors.New("oss component metadata is incomplete")
	ErrNotQualified       = errors.New("oss component is not independently qualified")
	ErrForbiddenAuthority = errors.New("oss component cannot become an authority")
)
