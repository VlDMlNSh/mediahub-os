# MH-04 Recovery Boundary

Security recovery is bounded containment and restoration, not authority escalation.

Allowed architectural classes: revoke/rotate credentials, re-establish identity, quarantine/release after verification, restart/reinitialize security-dependent services, restore readiness, controlled degraded operation.

Forbidden: replacement State Authority, direct state mutation, authorization bypass, capability widening after failure, implicit trust promotion.

Every recovery mutation returns through the governed authority path. Recovery loops are bounded, observable and policy-controlled.