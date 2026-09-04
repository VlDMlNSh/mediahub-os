# MH-06 — Configuration / Policy Interaction

Status: PROPOSED; P0-07 dependency BLOCKED where mutation publication requires the unresolved governance/API decision.

Flow: Configuration/Policy -> Validation -> Authorization -> Runtime Application -> Service Lifecycle.

Runtime must consume policy; it must not invent policy, silently mutate configuration, inherit undocumented critical defaults, or bypass State Authority where canonical state is involved.

MH-6 must not modify P0-03 through P0-06 to work around P0-07.
