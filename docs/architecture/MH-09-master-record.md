# MH-09 — Presentation / UI Architecture — Master Record

**Project:** MediaHub OS 11.x LTS / MediaHub iOS  
**Architecture chat:** MH-9  
**Status:** PROPOSED / REQUIRES VERIFICATION  
**Implementation authorization:** NOT GRANTED  
**Governance acceptance:** NOT GRANTED  
**Freeze:** NOT GRANTED

## 1. Continuity rule

MH-09 is an architecture keeper, not a development workspace. No feature implementation, debugging session, implementation branch merge, production qualification, or prolonged implementation discussion belongs in this architecture record.

Normative lifecycle:

`Evidence → Canonical State → Decision → Architecture → Implementation → Verification → Governance Acceptance → Freeze`

This repository record is the durable source for the MH-09 architectural state; ChatGPT conversation history is not treated as the sole long-term source of truth.

## 2. Authority invariant

Presentation is a consumer and presentation layer, never an authority.

`UI ≠ State Authority ≠ Policy Authority ≠ Authorization Authority ≠ Runtime Authority ≠ Persistence Authority ≠ Security Authority ≠ AI Authority`

P0-04 State Authority remains the sole canonical mutation authority. UI mutations must use the approved Consumer Boundary and authorization path. UI visibility, disabled controls, hidden routes, deep links, cached credentials, recommendations, and plugin rendering never constitute authorization.

## 3. Canonical interaction

```text
Human
  ↓
Presentation / UI
  ↓
Presentation Model / Read Model / Interaction Model
  ↓
Consumer Boundary
  ↓
Capability / Authorization / Policy
  ↓
Command or inert Proposal
  ↓
State Authority / controlled subsystem
  ↓
Canonical Runtime State
  ↓
Event / Authorized Read Model
  ↓
Presentation
```

## 4. Read model

The UI receives bounded, immutable/value-semantic, authorization-filtered, privacy-aware presentation data. Read models must expose freshness semantics where applicable: current, stale, cached, unavailable, estimated, predicted, recommended. Raw mutable runtime state, raw transactions, persistence handles and authority-bearing internals are forbidden.

## 5. Command / proposal

A UI action is user intent, not authorization. Commands require explicit operation-specific capability and authorization and must traverse the Consumer Boundary. Proposals are inert, bounded, non-executable data. AI recommendations, notification actions and plugin UI actions cannot bypass this path.

## 6. Synchronization / optimistic UI

UI must distinguish pending, accepted, committed, failed, rejected, cancelled and unknown outcomes. Optimistic presentation never constitutes commit. Stale reads and generation conflicts fail safely. UI must not introduce hidden merge, rebase, LWW or infinite retry semantics.

## 7. Sessions / navigation / lifecycle

UI session, authentication context and authorization context are distinct. Deep links and navigation are not security boundaries. Privileged screens remain backend-authorized. UI lifecycle is independent from runtime lifecycle and includes degraded/offline/reconnecting/recovery states.

## 8. Offline / local-first

Preferred dependency order: `Local Core > External Service > Cloud Intelligence`. Cached data must be explicitly identified as cached/stale. Offline operation cannot create unauthorized canonical persistence or mutation authority.

## 9. Security / privacy

UI has no direct State Authority internals, raw transaction access, canonical persistence authority, unrestricted filesystem, unrestricted network, shell, plugin execution authority, or secret access. Sensitive information follows least-disclosure and authorization-aware redaction. Security failures fail closed. UI telemetry is not canonical audit authority.

## 10. AI / plugins / notifications

AI is intelligence, not authority. Recommendation/proposal is not command. Plugin UI is capability-scoped and authorization-bound. Event and notification are observer-oriented; notification actions re-enter normal authorization flow. Detailed AI architecture is deferred to MH-10.

## 11. Platform model

MediaHub OS/appliance and MediaHub iOS share domain semantics, contracts, capabilities, authorization and error semantics, but do not share an assumed identical presentation implementation. Platform-specific lifecycle, connectivity, accessibility and recovery requirements are explicit.

## 12. Accessibility / localization / privacy

Accessibility is architectural: VoiceOver/assistive technologies, Dynamic Type, semantic labels, focus/keyboard behavior, reduced motion, contrast, non-color-only state indication and error announcements. Locale, timezone, units and formatting are presentation concerns and do not change canonical domain semantics.

## 13. Emergency / diagnostic / admin

Emergency UX is explicit, visible, auditable, fail-safe and minimally dependent on AI/cloud. Diagnostic and admin screens are privileged presentation surfaces, not authorities; mutations still require the canonical authorization and Consumer Boundary path.

## 14. Forbidden shortcuts

- UI → database
- UI → canonical filesystem
- UI → State Authority internals
- UI → raw transaction
- UI → direct device control
- UI → arbitrary shell
- UI → unrestricted network
- UI → plugin execution
- AI → UI → automatic critical mutation
- hidden retry / hidden merge / hidden LWW / hidden authorization
- implicit persistence or cloud authority

## 15. Evidence baseline

Repository: `VlDMlNSh/mediahub-os`  
MH-09 architecture branch: `architecture/mh-09-presentation-ui`

Current MH-09 branch head at time of record creation: `2b61e5faf00fcdfb909b5a408fa433f2921c79db`.

The repository also contains current workflow evidence that supersedes older forensic claims: `.github/workflows/mediahub-bridge.yml` now targets a fixed P0-06 verification commit, and a P0-07 verification workflow exists. Older claims must not be carried forward without current verification.

P0-03…P0-06 remain frozen foundations according to the supplied architecture baseline. P0-07 remains implementation-in-progress and not accepted/frozen.

## 16. Contradiction / unknown policy

Any conflict between MH-09 and frozen P0-03…P0-06 is STOP → DOCUMENT → CONTRADICTION REGISTER → GOVERNANCE DECISION. MH-09 must not modify frozen foundations for UI convenience.

Unknowns remain `UNKNOWN` or `REQUIRES VERIFICATION`; no historical relationship is reconstructed by assumption.

## 17. Acceptance gate

MH-09 cannot become ACCEPTED/FROZEN until its UI boundary, read model, command/proposal model, authorization interaction, session/navigation/lifecycle model, synchronization/offline semantics, security/privacy, accessibility, AI/plugin/admin/diagnostic/emergency boundaries, testing/threat model, traceability, contradiction register, unknown register and evidence register are reviewed and separately accepted by governance.

## 18. Development separation

Implementation must occur in a separate development chat/workspace and implementation branch. This architecture chat and this master record are normative/reference artifacts only. The development workspace may consume MH-09 through the master prompt and return implementation evidence through the reverse master prompt; it must not silently rewrite MH-09 architectural decisions.

## 19. Next architecture

After MH-09 governance completion, the next architecture keeper is:

`MH-10 — AI / INTELLIGENCE ARCHITECTURE`

Invariant: **AI is intelligence, not authority.**
