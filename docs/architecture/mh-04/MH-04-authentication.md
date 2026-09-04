# MH-04 Authentication

Authentication answers only whether a principal identity has been sufficiently established for the requested trust boundary.

Valid credential != unrestricted access. Authentication success does not imply authorization.

Failures: unknown identity, invalid/expired/revoked credential, ambiguous proof or authentication subsystem error -> DENY; quarantine may apply to suspicious external subjects.

Credential material remains outside canonical runtime state. Concrete authentication framework is CANDIDATE TECHNOLOGY until ADR/evidence review.