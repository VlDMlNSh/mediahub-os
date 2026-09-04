# MH-21 — Reverse Master Prompt

## Purpose
Development chat uses this artifact to report architecture-impacting implementation evidence back to MH-21.

## Required report
1. Repository HEAD/branch/clean-state evidence.
2. Files/components implementing MH-21 contracts.
3. Tests and exact verification evidence.
4. Actual provider/model/network/credential configuration evidence.
5. Data-flow traces, especially cloud→agent→tool→device and cloud→State Authority.
6. Egress, classification, privacy, authorization and capability enforcement evidence.
7. Failure/degradation and chaos-test evidence.
8. Observability/audit evidence.
9. Supply-chain/SBOM/provenance evidence.
10. Contradictions and unknowns.
11. Proposed ADRs and architecture changes.

## Status discipline
Use UNKNOWN / REQUIRES VERIFICATION when proof is absent; IMPLEMENTED / NOT VERIFIED when code exists without verification; ACCEPTED / NOT IMPLEMENTED when architecture is accepted but implementation is absent. Never report VERIFIED, ACCEPTED, FROZEN, QUALIFIED or PRODUCTION READY without evidence.

## Prohibition
A development result is evidence for review, not an automatic architecture decision. Only MH-21 governance may accept architecture changes.