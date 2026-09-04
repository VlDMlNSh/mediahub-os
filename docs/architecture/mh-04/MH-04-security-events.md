# MH-04 Security Events

Security events are facts, not commands.

Examples: authentication success/failure, authorization denied, credential expiry/revocation, principal/device quarantine, policy violation, command rejection, boundary violation.

Events may support audit and response workflows but event receipt never grants authority and event handlers cannot infer mutation rights.

Security event payloads must be bounded and sanitized; secrets and unnecessary sensitive material are excluded.