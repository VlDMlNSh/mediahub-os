# MH-17 — Device Scope

**Status:** PROPOSED / CANDIDATE

Every integration operation has an explicit scope: device, component, endpoint, capability, operation, and resource context as applicable. Scope is narrower than identity and authorization is evaluated against scope.

No implicit wildcard scope is permitted. Group membership, network reachability, adapter ownership, or possession of an endpoint locator does not create scope authorization.

Cross-device and cross-component operations MUST decompose into independently authorized operations unless a higher-level approved contract explicitly defines atomic semantics.
