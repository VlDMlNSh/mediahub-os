# MH-17 — Device Replacement

**Status:** PROPOSED / CANDIDATE

Replacement separates physical continuity from logical identity. A replacement device MUST NOT inherit authorization merely because it occupies the same endpoint or has the same human label.

Flow: `Detect replacement → Preserve old identity/history → Verify new identity → Evaluate compatibility/capabilities → Enroll → Authorize scope → Rebind approved relationships → Validate state → Resume`.

Historical identity, physical identity, endpoint identity, and MediaHub logical identity remain distinguishable. Rebinding requires explicit policy and audit evidence; destructive automatic substitution is forbidden.
