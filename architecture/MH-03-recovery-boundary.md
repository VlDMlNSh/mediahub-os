# MH-03 Recovery Boundary

**Status:** PROPOSED

Recovery responsibilities: detect failure, isolate affected service/capability, apply bounded restart/reinitialization, re-check dependencies/health, and restore lifecycle state when invariants hold.

Recovery is not a new authority. It cannot:
- mutate canonical state outside State Authority;
- promote cache/persistence/cloud to authority;
- weaken authorization;
- grant wildcard capabilities;
- bypass Consumer / Integration Boundary.

If State Authority cannot be recovered, runtime stops or remains in a non-mutating degraded state rather than creating a shadow authority.
