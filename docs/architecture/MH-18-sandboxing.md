# MH-18 — Sandboxing
Status: PROPOSED / NOT ACCEPTED

Untrusted media processing should use appropriate process isolation/sandboxing with least filesystem access, no unnecessary network, reduced privileges and CPU/memory/time/temp-storage quotas. Candidate mechanisms include OS sandboxing, containers and syscall restrictions; technology selection requires threat model, platform evidence and ADR.