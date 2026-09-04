# MH-18 — Migration
Status: PROPOSED / NOT ACCEPTED

Data migration covers metadata/schema/storage identity/path changes. Content transcoding covers media representation changes. They must remain separate workflows with distinct validation and rollback. Migration preserves content identity where semantics remain equivalent, records provenance, verifies destination integrity and updates canonical references only through authorized mutation.