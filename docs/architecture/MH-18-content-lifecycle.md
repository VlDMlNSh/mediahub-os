# MH-18 — Content Lifecycle
Status: PROPOSED / NOT ACCEPTED

States: DISCOVERED → INGESTING → VALIDATING → REGISTERED → INDEXED → AVAILABLE → PROCESSING → PUBLISHED → ARCHIVED → DELETED/QUARANTINED.

State transitions are domain events/commands authorized through State Authority. Discovery/processing failures do not silently advance state. Quarantine is fail-closed for unsafe or malformed input. Recovery must resume or restart from an explicit checkpoint without inventing canonical state. ARCHIVED and DELETED semantics remain policy-controlled.