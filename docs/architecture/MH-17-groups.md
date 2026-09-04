# MH-17 — Device Groups

**Status:** PROPOSED / CANDIDATE

Groups are organizational and orchestration constructs. Group membership MUST NOT itself grant authorization.

A group may aggregate devices, components, capabilities, or scopes for discovery, UI, automation, or policy evaluation. Every resulting command remains individually subject to identity, capability, authorization, policy, safety, and State Authority rules.

Membership changes are auditable and MUST be treated as policy-relevant configuration when they influence automation or access decisions.
