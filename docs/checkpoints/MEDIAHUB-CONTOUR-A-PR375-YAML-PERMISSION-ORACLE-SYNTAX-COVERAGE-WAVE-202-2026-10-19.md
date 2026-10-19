# MediaHub OS Contour A — PR #375 YAML permission-oracle syntax coverage (Wave 202)

- Date: 2026-10-19
- Canonical documentation branch: `docs/mediahub-chat-tree-map-20261012`
- Canonical map: [MEDIAHUB-CHAT-TREE-MAP.md](../architecture/MEDIAHUB-CHAT-TREE-MAP.md)
- Previous continuation checkpoint: [Wave 201](MEDIAHUB-NEXT-CONTINUATION-CHECKPOINT-WAVE-201-2026-10-19.md)
- Candidate PR: [#375](https://github.com/VlDMlNSh/mediahub-os/pull/375)
- Governing issue: [#301](https://github.com/VlDMlNSh/mediahub-os/issues/301)

## Objective

Continue the isolated credential-policy regression work without promoting or merging the draft. Review whether the static test oracle rejects valid YAML spellings of a job-level `contents: write` permission.

## Finding

The previous oracle searched for an unquoted block-style line matching `contents: write`. That can miss other YAML representations, including a quoted scalar (`contents: 'write'` / `contents: "write"`) and a flow-style mapping (`permissions: { contents: write }`). This is a test-oracle coverage gap; it is not evidence that the currently checked-in worker workflow contains one of these forms or that a runtime exploit occurred.

## Bounded candidate change

Updated only `ops/qualification/test_worker_workflow_credential_policy.py` on the existing PR #375 branch:

- Extended the static matcher to detect block-style unquoted/single-quoted/double-quoted `contents: write` and same-line flow-style `permissions` mappings.
- Added negative fixtures for a job-level flow-style write permission and a job-level single-quoted write permission.
- Did not change the worker workflow, credential policy, dispatch path, or runtime configuration.

Evidence:
- Previous test blob: `1d003b1d33fa31ec44d4cc8220747e3c4982b8b6`.
- Candidate commit: [`5ed32d0cc1375aa2cd524d1963183497cc0ff6eb`](https://github.com/VlDMlNSh/mediahub-os/commit/5ed32d0cc1375aa2cd524d1963183497cc0ff6eb).
- Final read-back test blob: `1046b59acf4a97390b64162dcbbb81e458ec26c2`.
- Isolated matcher matrix checked six write variants (block/flow and unquoted/single-/double-quoted); all were detected, while `contents: read` was not classified as write. This was a narrow regex sanity check, not a YAML-parser conformance proof; the later exact-head CI below also ran the repository regression test successfully.

## Current candidate state and verification

- PR #375 was re-read after the change: OPEN / Draft / unmerged; base `main` at `c06015e0b1526e0aaa6a522306052b077455aba5`; exact head `5ed32d0cc1375aa2cd524d1963183497cc0ff6eb`.
- A later exact-commit workflow-run query returned PR-triggered CI for this head: [Astra Verify run 39290847516](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39290847516), job `verify` / `118190778964`, SUCCESS; the **Worker workflow credential policy regression tests** step passed, along with cloud admission tests and signed-command smoke test. [Astra Cloud Runtime Validation run 39290847553](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39290847553), job `validate` / `118190779017`, SUCCESS. The earlier query returned no runs before these became visible; this is now exact-head CI evidence, not inherited parent-commit evidence.
- No submitted PR review was returned for PR #375.
- Issue #301 remains OPEN with 42 comments; the latest retrieved governance comment is Wave 192 (comment ID `6265270600`). No later governance disposition was found in the reviewed history.
- `docs/qualification/CURRENT-TRUTH.generated.md@main` remains blob `48d581a8f6a6a5fd380abbb7a7ce938b3b1e6731`; G0–G11 remain BLOCKED in the retrieved generated truth.

## Limits and safety boundary

This is a static regression-test candidate only. Regex-based source inspection does not replace parsing the workflow with a YAML implementation, and neither approach is server-side authorization. It does not close the worker's trusted publisher/output-publication path, FCC token propagation, OS/network isolation, issuer/capability governance, branch-protection evidence, or independent security review.

No worker/Gemini dispatch, provider call, secret access, host command, merge, deployment, qualification, or Contour B work occurred. PR #375 remains Draft and unmerged.

## Next action

Exact-head CI is now recorded above. Next obtain independent security review and settle a trusted publisher/output-publication design before any integration; do not treat passing CI as security acceptance.

**Contour A remains NOT QUALIFIED / NOT DEPLOYED / NOT INDEPENDENTLY ACCEPTED. Contour B remains gated.**
