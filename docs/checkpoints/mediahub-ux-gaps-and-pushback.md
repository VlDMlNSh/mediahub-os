# MediaHub UX Gaps and Pushback Register

Date: 2026-09-30
Status: MH-24 reconciliation and gap register

## Closed by MH-24

### UX-G1 — iPad Core vs Remote ambiguity
Resolved: iPad/iPadOS Core is a local Core edition; Remote is a separate remote application family.

### UX-G2 — UI as authority
Resolved: UI is an interaction surface only. Mutations traverse authorization, policy and domain contracts.

### UX-G3 — hidden degraded state
Resolved: system states are first-class, textual and accessible; color is supplemental.

### UX-G4 — developer/user data conflation
Resolved: developer UX does not inherit user-data navigation or visibility.

### UX-G5 — duplicate canonical screens
Resolved: object identity/deep-link contract converges Home, Search, notifications and domain navigation on one canonical object detail contract.

## Remaining implementation decisions

1. Exact SwiftUI/AppKit component tokens and theme values.
2. Exact screen inventory and route identifiers for every domain.
3. Exact entitlement UX and subscription flows.
4. Exact notification taxonomy and priority policy.
5. Exact command palette grammar and shortcut map.
6. Exact persistence/restoration model for navigation state.
7. Exact mobile API session/reconnect UI states.
8. Exact design-token serialization and code-generation strategy.
9. Snapshot/UI test strategy and accessibility automation.
10. Exact qualification evidence format for UX gates.

## Non-negotiable pushback

- Do not expose databases, queues, schedulers or network planes as ordinary user products merely because they exist internally.
- Do not hide critical state to make the interface look simpler.
- Do not let AI UI imply authority it does not have.
- Do not create separate canonical UX architectures per platform.
- Do not use color alone for state.
- Do not make developer interfaces a side door into user data.
- Do not call architecture "implemented" because a screen mockup exists.
- Do not call UI "qualified" without fresh evidence.

## MH-24 review result

The architecture is coherent with the reconciled Functional Baseline 2.0 direction. The largest remaining UX work is screen-level specification, design-token concretization, implementation, testing and qualification—not a change to the authority model.
