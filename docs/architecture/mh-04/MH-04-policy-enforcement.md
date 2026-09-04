# MH-04 Policy Enforcement

Policy constrains authorization decisions using principal, capability, resource and context.

Policy enforcement may DENY or QUARANTINE and may ALLOW continuation. It must not directly mutate canonical state or create emergency authority.

Policy/configuration follows P0-07 governance status; implementation and production qualification are not implied by this artifact.

Any policy enforcement failure that prevents proving authorization fails closed.