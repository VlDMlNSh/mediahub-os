# MH-04 Identity Model

Security Principal is the canonical subject abstraction.

Principal types: human, service, device, integration, AI, cloud, system.

Minimum lifecycle: UNKNOWN -> DISCOVERED -> IDENTIFIED -> AUTHENTICATED -> AUTHORIZED -> ACTIVE. Exceptional states include INVALID, EXPIRED, REVOKED, DENIED and QUARANTINED.

Identity is distinct from credential, authentication state, capability and policy grant.

Identity establishment never grants mutation authority. Every mutation request must carry an auditable principal identity and re-enter the governed authority path.