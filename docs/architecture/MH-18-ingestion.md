# MH-18 — Ingestion
Status: PROPOSED / NOT ACCEPTED

Sources: local/removable filesystem, network share, device, camera, phone, upload, API, cloud/provider.

All sources are untrusted until validated. Intake must be authenticated where required, capability-authorized, bounded, resumable where supported, integrity checked, observable and privacy-aware. Import creates candidate data; registration is an authorized mutation. No importer owns canonical state or unrestricted storage.