package supplychain

import "errors"

var ErrEvidenceRequired = errors.New("supply-chain evidence required")

type Evidence struct {
	ComponentID string
	Version string
	SourceDigest string
	SBOMDigest string
	LicenseDigest string
	VulnerabilityReportDigest string
	SignatureVerified bool
}

func (e Evidence) Valid() bool {
	return e.ComponentID != "" && e.Version != "" && e.SourceDigest != "" && e.SBOMDigest != "" && e.LicenseDigest != "" && e.VulnerabilityReportDigest != "" && e.SignatureVerified
}

func (e Evidence) Validate() error { if !e.Valid() { return ErrEvidenceRequired }; return nil }
