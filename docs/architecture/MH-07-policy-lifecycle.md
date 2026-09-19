# MH-07 — Policy Lifecycle

Status: CANDIDATE.

Conceptual lifecycle: Absent → Candidate → Validated → Authorized → Published → Active, with Superseded, Reset/Deleted and Quarantined recovery paths.

Modes proposed for architecture: disabled, dry-run, recommendation, supervised, active, emergency-disabled, quarantined. Mode transitions require explicit authorization and audit. Emergency-disabled cannot weaken hard safety constraints.

No mode is executable authority. Current P0-07 has no complete lifecycle/mode state machine; this remains CANDIDATE/REQUIRES VERIFICATION.
