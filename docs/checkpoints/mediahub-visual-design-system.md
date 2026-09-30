# MediaHub Visual Design System

Date: 2026-09-30
Status: MH-24 visual architecture baseline

## 1. Design intent

MediaHub should feel calm, precise and system-native without becoming a copy of macOS or iOS. Visual hierarchy should make system state, user intent and action consequences obvious.

Principle: **quiet chrome, strong semantic hierarchy, explicit state**.

## 2. Visual foundations

Typography: platform-native system typography with a stable MediaHub type scale and semantic roles rather than hard-coded font sizes.

Spacing: 4-point base rhythm with larger structural increments for sections and panels.

Grid: responsive layout based on content density, display size and split-view availability.

Shape: restrained corner radius and elevation; avoid decorative containers when hierarchy can be expressed through spacing.

Iconography: consistent semantic icon set. Icons never carry critical state without text/semantic label.

## 3. Components

Canonical reusable components:
- navigation sidebar;
- navigation bar;
- tab/segmented control;
- list and collection rows;
- object cards;
- detail header;
- inspector;
- sheet;
- dialog;
- confirmation gate;
- alert;
- status badge;
- state banner;
- progress/recovery stepper;
- empty state;
- loading/skeleton state;
- error state;
- dashboard metric;
- chart;
- command/result surface.

Components must encode semantic states rather than visual-only variants.

## 4. State visualization

All system states use at least:
- semantic icon;
- textual label;
- explanatory text where needed;
- accessibility announcement/semantics.

Color is never the sole discriminator.

## 5. Interaction patterns

Destructive or security-sensitive actions require explicit confirmation appropriate to risk.

Long-running actions expose progress, cancellation where safe, current phase and final evidence/result.

Unavailable capabilities are explained as unavailable/locked/unqualified rather than silently omitted when their absence matters to user expectations.

## 6. Edition and entitlement presentation

Professional functions may appear as LOCKED / UNLICENSED where discovery is useful. The UI must not imply that a visible capability is executable until entitlement and policy permit it.

## 7. Desktop

Use persistent sidebar, resizable split views, inspectors, multi-window and keyboard shortcuts. Avoid modal-only workflows for routine administration.

## 8. iPad

Prefer two-column or three-column navigation where width allows. Preserve touch-first controls and large content targets. Keep system status persistent without consuming excessive space.

## 9. iPhone

Prioritize one-handed readability, compact navigation, stacked detail, task-focused flows and clear connection/session state for Remote.

## 10. Developer surfaces

Developer UI may be information-dense and technical, but remains visually consistent with MediaHub. It must visibly distinguish infrastructure/workload/evidence objects from user content.

## 11. Accessibility and localization

Every component must have semantic labels, dynamic type behavior, focus order, keyboard behavior where applicable, reduced-motion behavior and localization-safe layouts.

## 12. Visual qualification

The design system is defined only at architecture level in MH-24. Concrete SwiftUI/AppKit implementation, snapshot testing and accessibility audits are downstream work and must not be inferred from this document.
