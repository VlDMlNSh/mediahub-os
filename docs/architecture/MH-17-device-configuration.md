# MH-17 — Device Configuration

**Status:** PROPOSED / CANDIDATE

Configuration is separate from device identity and runtime state. Configuration changes require identity, trust, scope, capability compatibility, policy, authorization, validation, audit, and explicit apply semantics.

Configuration MUST NOT silently grant capabilities or permissions. Secrets are referenced through approved secret-management boundaries and are never embedded in device descriptions or ordinary logs.

After configuration, the system distinguishes desired/configured state from device-reported and confirmed state. Failed or ambiguous application remains explicit rather than being assumed successful.
