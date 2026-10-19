# MediaHub OS Contour A — Gemini workflow token-authority review (Wave 188)

- Date: 2026-10-19
- Scope: independent blocker review while exact MCP OCI digest remains unresolved.
- Canonical map: [MEDIAHUB-CHAT-TREE-MAP.md](../architecture/MEDIAHUB-CHAT-TREE-MAP.md)
- Prior checkpoint: [Wave 187](MEDIAHUB-NEXT-CONTINUATION-CHECKPOINT-WAVE-187-2026-10-19.md)
- Governing issue: [#301](https://github.com/VlDMlNSh/mediahub-os/issues/301)

## Frozen refs and evidence

- `main` HEAD: `c06015e0b1526e0aaa6a522306052b077455aba5`.
- Canonical documentation branch before this wave: `35693d49cd071a0d1bffe8b07cfd790619007e3a`.
- Workflow blobs on `main`:
  - `.github/workflows/gemini-autonomous-engineering.yml`: `09523d809530ae5b7bf528eab5fa53bc5deaf92d`
  - `.github/workflows/gemini-agent-2.yml`: `259c8c82b8d90a39e1c90e65390e469b241b5581`
  - `.github/workflows/gemini-agent-3.yml`: `91b5397001e088dfae2f450ee77c9c23118b5601`
- Each workflow has a manual free-form `task`, checks out only `main`, runs on `ubuntu-latest` with a 30-minute timeout, and prompts the model to make one bounded documentation/evidence pass and open a PR without merging or deploying.
- Each job grants `contents: write`, `pull-requests: write`, and `issues: read`; the workflow-level permission is `contents: read`.
- The MCP `includeTools` list names four tools: create branch, create/update file, create PR, and get file contents. The token permissions themselves do not restrict writes to a dedicated branch, allowed file paths, or documentation-only changes. The configured tool is prompted to use a dedicated branch, but this is an instruction, not an enforced capability boundary.
- The task text is explicitly treated as untrusted in the prompt. Nevertheless, a model holding a repository-write token and a general file-write tool could attempt writes to a different ref or paths outside the intended documentation scope if the tool accepts those arguments. The PR/no-merge instruction is also prompt-level; branch protection and server-side authorization are separate controls.
- Post-run validation checks that the output artifact exists and parses as JSON, response is non-empty, at least one tool call succeeded, and a create-PR tool call succeeded. It does not validate PR base/head relationship, changed paths, absence of workflow or policy changes, or whether a direct write touched a protected ref.

## Assessment

This is a **design-level authority gap**, not evidence of an observed exploit. No workflow was dispatched in this pass. Do not infer that branch protection is absent; its current rules were not inspected in this bounded pass.

The four-tool allowlist reduces available operations but does not itself establish path/ref restrictions. Broad repository write authority is larger than the documented documentation-only task. Mutable action refs and the unresolved MCP image digest remain separate supply-chain blockers.

## Recommended control design (proposal; not yet approved or implemented)

1. Use a read-only model token for repository discovery and draft generation where feasible.
2. Put branch creation, file writes, and PR creation behind a constrained broker/action that enforces a fixed base ref, dedicated branch namespace, path allowlist, and denied workflow/security-sensitive paths.
3. Validate the resulting PR server-side: exact base, branch prefix, allowed changed paths, no direct writes to protected refs, and no unexpected permission/workflow changes. Fail closed if any check cannot be evaluated.
4. Keep write authority limited to a short-lived token scoped to the minimum repository permissions and revoke/expire it after the operation.
5. Before any Gemini dispatch, resolve the exact MCP OCI digest and verify upstream provenance; pin action commits and re-run parity tests.

These are proposals for governance/change control, not accepted contracts. No permission contract or approval was inferred.

## State and non-actions

- Issue #301 remains open.
- PRs #374, #375, and #376 remain open Draft/unmerged.
- PR #376 head remains `1b6643d4dc3cbb27646e9dbfd27a6a763340cfbd`; previously observed Astra Verify and Astra Cloud Runtime Validation runs passed on that exact head.
- SentinelX: zero connected hosts; Mac mini offline; `mh-dev-01` and `mh-dev-02` user-disabled. Codex Tasks has no registered environments.
- No Gemini dispatch, secret access, host command, manual test, workflow modification, merge, deployment, or qualification occurred.

## Next action

Review the proposed brokered-write contract against the existing issuer/capability and governance requirements, then create a separate testable design/implementation PR only after required approval. In parallel, obtain authorized registry access for the exact MCP image digest. Do not dispatch Gemini while these controls remain unresolved.

Contour A remains **NOT QUALIFIED / NOT DEPLOYED / NOT INDEPENDENTLY ACCEPTED**.
