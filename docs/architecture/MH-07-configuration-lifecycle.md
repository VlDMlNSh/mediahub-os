# MH-7 — Configuration Lifecycle

Status: CANDIDATE

Canonical lifecycle:

Absent → Candidate → Validated → Authorized → Published → Applied → Superseded.

Reset and Delete are explicit domain operations with distinct semantics.

A Candidate is not authoritative. Validation does not imply authorization. Authorization does not imply publication. Publication does not imply runtime application. Applied requires runtime evidence.

Every transition is explicit, bounded and fail-closed on invalid, stale or unauthorized input.
