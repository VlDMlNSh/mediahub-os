# MH-18 — Resource Governance
Status: PROPOSED / NOT ACCEPTED

Explicit quotas are required for file/upload size, metadata, thumbnails, temporary storage, index size, concurrent streams, processing jobs, CPU/GPU, memory and bandwidth. Limits are per operation/principal/provider where appropriate. Exhaustion fails boundedly and observably; background work cannot starve Core Runtime.