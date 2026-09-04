# MH-18 — Integrity
Status: PROPOSED / NOT ACCEPTED

Integrity evidence includes byte size, digest (candidate SHA-256 or equivalent), MIME/type, container, stream structure and relevant codec parameters. Digest algorithm is not canonical until requirements/security review and ADR. Integrity verifies bytes; it does not establish domain identity, ownership, rights or trustworthiness. Revalidation is required after transport/storage migration where policy demands it.