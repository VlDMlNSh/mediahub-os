# OSS runtime model

Runtime activation is capability-gated.

Current MH-03 runtime remains the default. OSS runtimes are isolated behind MediaHub contracts and cannot become authoritative merely by being installed.

Activation states:

- `disabled` — component present in manifest only;
- `candidate` — integration code exists, qualification pending;
- `qualified` — independent qualification passed;
- `active` — explicitly enabled by a governed release/configuration change.

No component may transition directly from `candidate` to `active` without qualification evidence.
