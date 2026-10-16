# MediaHub Chat Tree Map — Wave 41 Addendum

- Date: 2026-10-17
- Status: RUSSIA-HOSTED RUNNER / PROVIDER-GEOGRAPHY ADMISSION GATE
- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
- Primary report: [Russia-Hosted Runner Boundary and Provider-Key Enrollment Design, Wave 41](../checkpoints/MEDIAHUB-RUSSIA-HOSTED-RUNNER-AND-PROVIDER-KEY-ENROLLMENT-WAVE-41-2026-10-17.md)

## Navigation decision

Separate human provider account/key enrollment from runtime provider invocation. The Russian-hosted runner must not be expected to open registration or key-management pages. The operator can use a browser from a provider-authorized location and enter the key directly into an approved secret store.

This does not prove that calls from the Russian runner are allowed. Provider-specific geography, actual execution egress, contractual terms, data residency and account eligibility remain admission gates. No proxy, VPN, relay or alternate target may be used to disguise origin or bypass restrictions.
