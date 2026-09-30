# MH-4 GAPS / BLUEPRINT — 2026-09-30

## GAPS

### G0 — Qualification evidence
Architecture is reconciled, but implementation/runtime/independent qualification evidence is not yet attached to the MH-4 baseline. This is the primary closure gap.

### G1 — Cross-lane evidence
Security contracts must be verified against downstream consumers, especially Policy, Runtime, Plugins, AI, Observability, Privacy, Persistence, Recovery and Qualification.

### G2 — Platform variance
TPM/Secure Enclave/attestation/secure-boot capabilities differ across Linux, macOS, iPadOS and Raspberry Pi. Qualification must verify capability reduction where a primitive is unavailable.

### G3 — Critical degraded/emergency paths
Any availability-preserving security fallback must prove bounded scope, pre-qualification, fresh policy and audit. No implicit bypass is allowed.

### G4 — Negative-path proof
S-01..S-23 and forbidden paths require fresh negative evidence. Architectural statements are not sufficient.

### G5 — Credential/secret enforcement evidence
Secret storage, rotation, revocation, provider mismatch, malformed credential and admission rejection need exact implementation evidence where applicable.

### G6 — Supply-chain evidence
SBOM, provenance, artifact integrity, vulnerability disposition and reproducibility must be tied to the qualification target.

### G7 — Independent review
MH-4 needs independent review/evidence reconciliation before QUALIFIED.

## BLUEPRINT

OBSERVE
-> RECONCILE exact GitHub revision and architecture dependencies
-> VERIFY artifact integrity/provenance
-> VERIFY identity/trust/authentication
-> VERIFY authorization/capability/policy
-> VERIFY credential/key/secret lifecycle
-> VERIFY device/node admission + quarantine
-> VERIFY segmentation + egress + User/Developer isolation
-> VERIFY AI/Cloud/Plugin non-authority
-> VERIFY API/session/callback/mobile/cluster/runtime boundaries
-> VERIFY bootstrap/integrity/supply-chain/recovery
-> RUN negative invariant matrix S-01..S-23
-> RUN forbidden-path matrix
-> RECONCILE cross-lane contracts
-> INDEPENDENT REVIEW
-> RECORD evidence manifest
-> QUALIFY only if all hard gates PASS

## HIPPODROME EXECUTION WAVES

Wave 0: exact revision + provenance.
Wave 1: identity/trust.
Wave 2: authorization/capability/policy.
Wave 3: credentials/cryptography/secrets.
Wave 4: admission/quarantine/runtime.
Wave 5: segmentation/egress/data isolation.
Wave 6: AI/Cloud/Plugin/Smart Home.
Wave 7: API/mobile/cluster/recovery.
Wave 8: supply chain/integrity.
Wave 9: negative/security invariants.
Wave 10: independent review + final qualification.

## EXIT

QUALIFIED only when fresh evidence proves the security contracts on the exact target revision.

Otherwise:
BLOCKED with exact evidence gap.

No production/release authorization is implied.
