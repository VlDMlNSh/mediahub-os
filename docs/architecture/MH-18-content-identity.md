# MH-18 — Content Identity
Status: PROPOSED / NOT ACCEPTED

Identity layers:
Content ID = logical domain identity.
Asset ID = acquired representation identity.
Object ID = storage object identity.
Storage locator = physical location, mutable.
External provider ID = provider-scoped identity.
Digest = content-integrity evidence, not domain identity.
Fingerprint = similarity/deduplication evidence, not identity.
Version = schema/content representation version.

Identifiers must be opaque, stable within scope, non-secret and never derived solely from paths or URLs. Identity changes require authorized state mutation.