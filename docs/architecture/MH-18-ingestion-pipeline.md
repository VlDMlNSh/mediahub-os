# MH-18 — Ingestion Pipeline
Status: PROPOSED / NOT ACCEPTED

Pipeline: Source → Discovery → Intake → Identity → Integrity → Malware/Safety Analysis → Metadata Extraction → Normalization → Classification → Policy Check → Registration → Indexing → Availability.

Each stage has explicit input/output, bounded resources, idempotency key where applicable, timeout, retry policy, cancellation and failure category. Failure is retained as observable evidence; no silent corruption or implicit retry forever. Registration alone can affect canonical state, and only through authorized State Authority path.