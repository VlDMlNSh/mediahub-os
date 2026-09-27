# Free/Public Model Provider Compatibility — 2026-09

## Control decision

Do not implement a GitHub Models inference adapter. GitHub documentation states that GitHub Models was fully retired on 2026-07-30, including its playground, model catalog, inference API and BYOK. The MediaHub orchestration layer therefore remains provider-neutral.

## Supported integration contract

A provider adapter may be added outside the qualification authority layer when it satisfies all of the following:

- callable from the configured GitHub Actions runner;
- uses only runner environment/secret-store credentials when credentials are required;
- never writes credentials to repository files, issues, artifacts or logs;
- returns model identity, adapter version, task ID and exact source SHA;
- records failures explicitly rather than fabricating output;
- cannot merge, qualify, authorize production or modify the immutable forensic target;
- can be disabled without affecting MediaHub runtime correctness.

## Free does not mean guaranteed

Provider pricing, quotas, model availability and terms may change. The workflow must therefore treat `configured-free-model` as an adapter label, not as a promise that inference is free or continuously available.

## Current fallback

If no adapter is configured, the workflow performs deterministic orchestration-policy validation and emits a `NO_ADAPTER`-equivalent planning state. It must not pretend that a model was executed.
