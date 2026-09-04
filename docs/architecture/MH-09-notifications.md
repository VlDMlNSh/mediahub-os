# MH-09 — Notifications

**Status:** PROPOSED / REQUIRES VERIFICATION

Events and notifications are observer-oriented data, not commands. Notification content is bounded, privacy-aware and authorization-filtered.

A notification action is only a user intent and must re-enter authentication/authorization/capability checks and the Consumer Boundary. Push delivery, notification visibility or action identifiers cannot directly mutate canonical state.
