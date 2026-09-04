# MH-12 Failure Domains

Required isolation: UI ↛ State Authority; AI ↛ authorization; plugin ↛ runtime authority; device adapter ↛ core authority; cloud ↛ local authority; observability ↛ state authority; diagnostics ↛ mutation authority; update service ↛ runtime authority; recovery ↛ unlimited authority.

A compromise in one domain must not automatically compromise another. Cross-domain effects require explicit authorization and boundary enforcement.
