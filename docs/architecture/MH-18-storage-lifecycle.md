# MH-18 — Storage Lifecycle
Status: PROPOSED / NOT ACCEPTED

Asset bytes move through Available → Read/Stream → Process → Cache/Derivative → Archive → Delete. Operations are idempotent where feasible and integrity-verified where required. Migration must preserve identity/provenance and use authorized catalog updates only after destination verification.