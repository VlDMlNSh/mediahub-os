# MH-03 Health Model

**Status:** PROPOSED

Health dimensions:
- liveness — service/process is responsive;
- readiness — required dependencies and contracts are usable;
- dependency health — required/optional dependencies classified;
- authority health — State Authority availability;
- lifecycle health — runtime state transition is valid;
- degraded status — explicitly reported when reduced capability is active.

Health is observational/control metadata, not canonical domain state. Health signals cannot directly mutate canonical state.
