# MH-7 — Plugin Interaction

Status: CANDIDATE

Plugins are bounded proposal sources at the MH-7 boundary. They may recommend or analyze candidates but cannot self-authorize, grant capabilities, publish, directly mutate State Authority, execute arbitrary policy/configuration content, or create hidden persistence/network behavior.

Plugin proposals use the same validation, policy, authorization and controlled-ingress path as all other candidates.
