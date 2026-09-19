# MH-07 — Configuration Lifecycle

Status: CANDIDATE.

Conceptual states: Absent → Candidate → Validated → Authorized → Published → Applied → Superseded; Reset/Delete are explicit authorized operations.

Construction creates Candidate. Validation creates Validated. Authorization is a decision, not publication. Published requires the authorized P0-05/P0-04 path. Applied means runtime accepted the published desired configuration; observed state may still differ.

Reset returns to an explicitly defined safe/default representation. Delete removes the object. Neither is an implicit fallback.

Current P0-07 does not implement this complete lifecycle; status is CANDIDATE/REQUIRES VERIFICATION.
