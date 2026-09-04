# MH-09 — Localization

**Status:** PROPOSED / REQUIRES VERIFICATION

Localization covers language, locale, timezone, units, date/time formatting, numbers, pluralization and fallback behavior. These are presentation concerns and must not mutate canonical domain semantics.

Critical actions, errors and safety states require localized but semantically equivalent wording. Tests must verify that formatting cannot change identifiers, authorization semantics, capability names or command meaning.
