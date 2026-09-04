# MH-09 — Presentation / UI Architecture v1.0

**Status:** PROPOSED — GOVERNANCE ACCEPTANCE REQUIRED

## Purpose

Define the canonical Presentation / UI layer for MediaHub OS / MediaHub iOS without introducing a new authority. The presentation layer expresses human intent and renders authorized state; it never owns canonical mutation authority.

## Normative authority

P0-04 State Authority remains the sole canonical mutation authority. P0-05 Consumer Boundary remains the mandatory consumer/integration boundary. P0-06 services remain coordinators, not a second state authority. P0-07 remains implementation-in-progress and is not assumed accepted/frozen. P0-08/plugin interaction remains capability-scoped and does not grant UI authority.

## Canonical flow

```text
Human
  ↓
Presentation / UI
  ↓
View Model / Read Model / Interaction Model
  ↓
Consumer Boundary
  ↓
Capability / Authorization / Policy
  ↓
Command or inert Proposal
  ↓
State Authority / controlled subsystem
  ↓
Canonical runtime state
  ↓
Event / authorized Read Model
  ↓
Presentation
```

UI state is separate from canonical runtime state. A local draft, optimistic value, cache, navigation state, or animation is never evidence of commit.

## Read model

UI receives bounded, immutable/value-semantic, authorization-filtered and privacy-aware read models containing source, revision/generation where applicable, timestamp/freshness and explicit current/stale/cached/unavailable/estimated/predicted/recommended semantics. Internal mutable state, raw transaction handles and persistence handles are never exposed.

## Commands and proposals

A UI action is user intent, not authorization. Mutation requires explicit operation-specific authorization and the normal Consumer Boundary path. Proposals are inert bounded data. AI output, notification actions and plugin UI actions do not bypass this path.

## State synchronization

The UI must represent pending, accepted, committed, failed, rejected, cancelled and unknown outcomes distinctly. Stale reads and generation conflicts fail safely; the UI performs no hidden merge, rebasing or last-writer-wins behavior. Optimistic presentation is allowed only when its non-canonical status is visible.

## Sessions and navigation

UI session, authentication context and authorization context are separate concepts. Deep links, hidden routes and disabled controls are never security boundaries. Privileged screens are guarded but still rely on backend authorization. UI lifecycle is independent from runtime lifecycle.

## Offline and degraded operation

Local-first behavior is preferred. Cached state is explicitly marked as cached/stale and must not be presented as live canonical state. Loss of cloud, AI, optional plugins, external devices or network produces honest degraded/unavailable states. No offline mechanism creates unauthorized canonical persistence or mutation authority.

## Security and privacy

UI has no direct State Authority, database, canonical filesystem, unrestricted network, shell, plugin execution or secret access. Visibility is not authorization. Sensitive information is least-disclosure and authorization filtered. Security failures fail closed. UI telemetry is not canonical audit authority.

## AI / plugin / notification boundary

AI is intelligence, not authority. Recommendation is not command. Plugin UI is an extension surface under declared capability and authorization. Events and notifications are observer-oriented; notification actions re-enter the normal command authorization path.

## Platform model

Appliance/operator, diagnostic, administration and recovery interfaces and MediaHub iOS share domain semantics, contracts, capabilities, authorization and error semantics, but are not treated as the same presentation implementation. Platform-specific lifecycle, accessibility and connectivity constraints are modeled explicitly.

## Accessibility and localization

Accessibility is an architectural requirement: semantic labels, VoiceOver/assistive technology support, Dynamic Type, contrast, keyboard/focus behavior, reduced motion, localization and non-color-only state indication are part of the presentation contract. Locale, timezone, units and formatting remain presentation concerns and never alter canonical domain semantics.

## Error/failure UX

Canonical error categories include validation, authentication required, authorization denied, policy denied, stale/conflict, unavailable, timeout, cancellation, dependency failure, degraded mode, quarantine, recovery required and unknown result. The UI never displays success without authoritative confirmation.

## Testing

Testing is layered: unit tests for presentation models and transformations; contract tests for read/command/proposal and Consumer Boundary integration; security tests for forbidden direct capabilities; integration tests for UI→Consumer Boundary→authorization→State Authority; failure/offline/concurrency tests; accessibility tests.

## Technology neutrality

SwiftUI, UIKit, web, declarative schemas, sandboxed UI, native modules and other technologies remain candidates. No implementation technology is canonicalized by this document. Selection requires an ADR and evidence covering security, lifecycle, performance, accessibility, offline behavior, maintainability, compatibility and deployment constraints.

## Acceptance gate

MH-09 remains PROPOSED until repository evidence, contract review, threat-model review, contradiction review and governance acceptance establish that all required boundaries and artifacts are satisfied. No implementation authorization is granted by this document.
