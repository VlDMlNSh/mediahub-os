# MH-04 Credential Boundaries

Credentials are authentication material, not canonical runtime state and not authorization itself.

Boundary: credential source/storage -> authentication verifier -> principal identity -> authorization/capability decision.

Credential material must not be exposed through logs, telemetry, events or ordinary application state. Compromise/revocation must fail closed and invalidate dependent authorization as defined by policy.

Concrete secret store/keychain/identity framework is CANDIDATE TECHNOLOGY until evidence and ADR.