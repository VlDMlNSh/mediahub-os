# MH-07 — Privacy Boundary

Status: CANDIDATE.

Configuration and policy metadata may be sensitive. Apply minimization, access control, disclosure boundaries and redaction. Do not transmit configuration/policy to external cloud or AI services automatically.

External transfer is an explicit bounded operation subject to authorization. Secrets are rejected from P0-07 values and audit/diagnostic output must avoid sensitive payload disclosure.
