# MediaHub OS — OSV-Scanner v2.7.0 Qualification Preflight (Wave 458, 2026-10-29)

- Scope: **STEP 2A ONLY — PINNED CLI/JSON CONTRACT AND EXECUTION-ENVIRONMENT PREFLIGHT**
- Status: **STATIC SOURCE CONTRACT VERIFIED / TOOL INTEGRITY NOT VERIFIED / RUNTIME PROBE NOT RUN / SCA BLOCKED**
- Immutable MediaHub main target: `f0448f28c7cfa61e4450c38529f09afbfdbbc7c7`.
- Canonical documentation branch at preflight: `742e1023aaa55b42b904d50fe045086202197993`.
- Prior input pin report: [Wave 457](MEDIAHUB-DEPENDENCY-AUDIT-INPUT-PINS-WAVE-457-2026-10-29.md), blob `d82ee45893c6d0a2a68a290c2b1475cd93d117a2`.
- Canonical map: [MEDIAHUB-CHAT-TREE-MAP.md](../architecture/MEDIAHUB-CHAT-TREE-MAP.md); [Wave 458 map addendum](../architecture/MEDIAHUB-CHAT-TREE-MAP-ADDENDUM-WAVE-458-2026-10-29.md); [checkpoint](mediahub-next-continuation-checkpoint-2026-10-12-current.md); [Master Roadmap](MEDIAHUB-MASTER-DEVELOPMENT-ROADMAP-1.0.md); governing [Issue #301](https://github.com/VlDMlNSh/mediahub-os/issues/301).

## 1. Pinned scanner source and release evidence

- OSV-Scanner release: [v2.7.0](https://github.com/google/osv-scanner/releases/tag/v2.7.0); release API reports `immutable=false`.
- Tag object `7ef17deffedb9e9b751fe6c6c328a88de29d9cf4` points to source commit `bfe2f84abd2f09fe0b83ba7f6dad40d296762f40`.
- GitHub commit verification for the **source commit** reports `verified=true / reason=valid`; GitHub tag-object verification reports `verified=false / reason=unknown_key`. These are distinct statements: the source commit signature is accepted by GitHub's API, but the tag object signature is not.
- Published release metadata records Linux amd64 asset `sha256:160c6253e2922e9e0a6a9771c5c4c40a4b3c6090b34a3cdd5e80c96cc2e4218b` (57,725,088 bytes), checksum asset `sha256:95d69019bcfe0586eb8f07aad4c56e2f734ee969e8e3e209591f259a1bfde88c`, and attestation bundle `sha256:f76e4c6fe6c5f12cb209978418ac42de3da63251bdbef16417645c7660f10ea8`.
- These are **GitHub release API digest metadata**, not independently recalculated binary/checksum/attestation hashes. The executable, checksum asset contents, and SLSA attestation were not downloaded or independently verified.

## 2. Pinned CLI and JSON output contract

Static source documentation was read at exact commit `bfe2f84abd2f09fe0b83ba7f6dad40d296762f40`:

- `docs/usage.md`, blob `f6d68845d275fe477674e8e738830a5d354d03ad`: describes `osv-scanner scan -L path/to/lockfile --format json` and the pinned-version `--output-file` flag.
- `docs/output.md`, blob `025bc1a3f1cb69a1b901e4b43ccfb2029f23fbae`: documents JSON stdout, non-JSON diagnostic output on stderr, and a single-lockfile example using `-L` with JSON redirected to a file.
- `docs/installation.md`, blob `de0479312f21fcd6fb5d2ca617c7c1ac9629379b`: documents release SLSA provenance and the intended `slsa-verifier verify-artifact` flow.

Disposition: this verifies the **documented source contract only**. No runtime `--version`, `--help`, JSON fixture, or lockfile scan was executed. Documentation does not substitute for a runtime command/output test.

## 3. Controlled-environment preflight

The available container reports Linux x86_64. `sha256sum`, `gpg`, `jq`, and Go are present; `osv-scanner`, `slsa-verifier`, `cosign`, and `gh` are absent. A read-only attempt to retrieve the official release checksum asset via HTTPS failed with `curl: (6) Could not resolve host: github.com`; no binary was installed or executed. The sandbox therefore cannot independently compare the published asset digest/checksum or verify the SLSA bundle in this pass.

- Scanner provenance/qualification: **NOT VERIFIED**.
- Runtime command/output contract: **NOT RUN**.
- All eight source-snapshot scans from Wave 457: **BLOCKED / NOT RUN**.
- Advisory results: **NOT RUN**; do not infer a clean scan from missing output.
- Recovery of the unrelated Trivy quota-limited job and independent gVisor release-artifact verification remain separate tasks.

## 4. Current MediaHub integration gates

- PR [#583](https://github.com/VlDMlNSh/mediahub-os/pull/583): OPEN / DRAFT / UNMERGED at `448bcbe6b941847b993dc2675a74367cce276b3e`. Nine exact-head check-runs observed: seven SUCCESS and two SKIPPED (controller non-launching admission/dispatch path). Combined status: pending with zero contexts; formal reviews: zero.
- PR [#585](https://github.com/VlDMlNSh/mediahub-os/pull/585): OPEN / DRAFT / UNMERGED at `8940c7f0f66c9f50e2d83659a6231aa790817221`. Both observed exact-head checks SUCCESS; combined status pending with zero contexts; formal reviews: zero.
- Ruleset listing returned an empty list; direct branch-protection read returned HTTP 403. Effective required-check/branch policy remains **NOT VERIFIED**.
- Issue #301 remains OPEN (196 comments; last updated 2026-10-23T14:55:53Z).
- Gemini batch/child runs, provider inference, secret access, local executor task, merge, deployment, runtime qualification and component adoption: **NOT RUN**. Contour A **NOT ACCEPTED**; Contour B remains gated.

## 5. Next bounded step

Use a controlled network-enabled, ephemeral verification environment to independently download the exact v2.7.0 Linux amd64 binary, checksum file, and attestation bundle; compare the executable hash against both the published asset digest and checksum manifest; verify SLSA provenance against source URI/tag; and only then run `--version`, `scan --help`, and a harmless pinned fixture to validate JSON/exit-code behavior. Do not start the eight dependency scans until those gates pass. If an approved environment cannot be established, keep the scan **BLOCKED / NOT RUN**.

Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
