# MH-7 — Validation Model

Status: CANDIDATE

Validation gates are distinct:

1. Syntax
2. Schema
3. Semantic validity
4. Policy admissibility
5. Principal authorization
6. Runtime applicability

Passing one gate does not imply passing later gates. Malformed, unsupported, conflicting or unauthorized input fails closed.

Bounds are canonical v1 constraints: document/request/response 256 KiB; depth 8; total value nodes 512; collection elements 128; strings 4096 bytes; identifiers 128 bytes; object keys 128 bytes with at most 64 keys; policy rules 64; namespace/schema identifiers 128 bytes. Non-finite numbers, credentials and unsafe executable content are rejected.
