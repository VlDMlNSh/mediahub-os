# MH-06 — IPC Boundary

Status: PROPOSED / TRANSPORT UNKNOWN

Conceptual IPC requirements: authentication, authorization, bounded payloads, request identity, timeout, cancellation, replay handling, explicit failure semantics and audit context.

Transport choices (Unix sockets, local RPC, gRPC, HTTP, message bus) are candidates only. No IPC transport may be treated as trusted merely because it is local. IPC must preserve P0-05 authorization and cannot expose direct P0-04 mutation.
