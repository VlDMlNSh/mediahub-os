# MH-04 Trust Model

Trust tiers inherited: T0 Trusted Core; T1 Authorized Local Services; T2 Presentation; T3 Integrations; T4 Intelligence; T5 External Network.

Trust tier is not an authorization grant. Reachability != identity != authentication != authorization.

A principal must be evaluated in context before receiving capabilities. Lower trust must never obtain implicit elevation through network reachability, VPN, locality, events, telemetry, AI output or cloud access.

Security boundaries are reviewed as: boundary -> threat/failure -> identity -> authorization -> policy -> runtime control -> State Authority -> verification -> governance.