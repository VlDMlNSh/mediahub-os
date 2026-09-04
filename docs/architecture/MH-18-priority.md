# MH-18 — Priority
Status: PROPOSED / NOT ACCEPTED

Priority order candidate: safety/system media → active playback → explicit user request → scheduled processing → indexing → AI enrichment → cache rebuild. Priority is subject to platform resource policy. No background queue may starve Core Runtime or bypass quotas/authorization. Preemption/cancellation semantics require implementation evidence.