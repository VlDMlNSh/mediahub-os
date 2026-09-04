# MH-23 API Compatibility

Compatibility requires request/response/error/command/event and authorization-context analysis. Unknown fields may be accepted only where safely ignored without changing security or authority semantics. Unsupported security-sensitive or authority-sensitive inputs are rejected or quarantined.