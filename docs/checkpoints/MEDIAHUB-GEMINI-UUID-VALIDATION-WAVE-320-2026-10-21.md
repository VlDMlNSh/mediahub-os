# Wave 320 — strict dispatch UUID validation (2026-10-21)

## Result

**SOURCE CHANGE WRITTEN AND READ BACK / EXACT-HEAD CI SUCCESS / NO AGENT DISPATCH.**

On PR #432's existing candidate branch, the three Gemini child workflows now require a canonical lowercase UUIDv4 dispatch correlation ID instead of accepting any 36-character string composed of hex digits and hyphens.

- PR: https://github.com/VlDMlNSh/mediahub-os/pull/432
- Working branch: `fix/gemini-controller-api-dispatch-wave312-final`
- Current PR #432 head after this bounded change: `8a6bc17180ff8027edb5c628f8092a4c527212b5`; base SHA: `f16e5bae202a78584f273132e7f88c6e25d3142e`.
- Workflow blob SHAs after the change:
  - `.github/workflows/gemini-autonomous-engineering.yml`: `155a02159912ca371e6f826c51325ca269857aad`
  - `.github/workflows/gemini-agent-2.yml`: `fff1820a6b97d379b23674f36bd62227b7d4dec2`
  - `.github/workflows/gemini-agent-3.yml`: `781df56e8aa7c75ba453c08378611857862b2e44`
- Test blob SHA: `65bc0c4b9a7eb58a71bb1b8123cf1ff4305f52af`.

## Change

All three child authorization steps now validate:
`[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}`

This is stricter than the previous `[0-9a-f-]{36}`: it checks canonical hyphen positions, UUID version 4 and RFC variant bits. The test module adds valid and invalid fixtures, including wrong version, wrong variant, missing hyphens, invalid characters and all-hyphen input, and checks that each child source includes the strict validator.

## Verification status

- GitHub API read-back confirmed the three workflow blobs have the expected SHAs and contain the strict validator.
- GitHub API read-back confirmed the test blob contains `test_children_enforce_canonical_uuid4_dispatch_ids` and the invalid fixtures.
- Latest workflow-run inventory for the previously inspected SHA `0f291dc77ecdd00798c6900b92f18fce58267cbc` reports success for contract validation, probe, Astra Verify and Cloud Runtime Validation, but these runs predate this UUID-validation test change. They are not exact-head evidence for Wave 320.
- Exact-head CI for `8a6bc17180ff8027edb5c628f8092a4c527212b5`: all five listed runs report success — [Astra Cloud Runtime Validation 39648235456](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39648235456), [non-launching caller-context probe 39648235621](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39648235621), [Gemini controller probe 39648235821](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39648235821), [workflow contract validation 39648235554](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39648235554), [Astra Verify 39648235100](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39648235100). The probe's dispatch job remains non-launching; no Gemini children were run.
- Local tests were not run in this environment. No HMAC key or provider credential was read.
- No controller run, Gemini child run, Claude session or agent-browser session was launched.

## Residual gates

PR #432 remains OPEN / DRAFT / UNMERGED and has no submitted formal review. Source-only inspection is not independent acceptance. The controller candidate is not active on `main`; the current `main` controller blob remains `4cec1aa234fd9ccb0d41533b37248fff079c79c5`.

Remaining requirements include exact-head CI, independent review of the candidate head, non-disclosing verification of secret presence/separation and effective token permissions, governance/branch-protection evidence, Alamo identity/capabilities and non-paid Claude route, and a supported event bridge if each ChatGPT `/next` must trigger GitHub Actions.

## Next step

Add runtime-level secret-free HMAC canonicalization/tamper tests rather than relying only on source-string assertions. Add runtime-level secret-free HMAC canonicalization/tamper tests rather than relying only on source-string assertions. Keep controller dispatch fail-closed until review and governance gates are met.
