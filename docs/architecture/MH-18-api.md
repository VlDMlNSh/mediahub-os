# MH-18 — Media API
Status: PROPOSED / NOT ACCEPTED

Operations are distinct: browse, search, metadata read, playback request, upload/import, transcode request, export, delete, metadata modification. Each declares principal, capability, scope, input limits and audit requirements. Read APIs expose read models; mutations delegate through authorized State Authority path. Bulk operations require explicit policy and bounded batches.