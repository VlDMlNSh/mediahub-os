# Wave 490 — Microsoft developer tooling integration assessment

- Date: 2026-10-31
- Status: **RESEARCH COMPLETE / IMPLEMENTATION NOT STARTED / NOT ACCEPTED**
- Workstream: Contour A developer experience; supporting only, not a new execution authority
- Immutable documentation parent: canonical docs branch commit `bfb2a6d73ba64839e783d6ee30d0d8ae2e3074a4`
- Runtime source snapshot: `main` commit `f0448f28c7cfa61e4450c38529f09afbfdbbc7c7`

## 1. Executive decision

Adopt **Visual Studio Code as the preferred cross-platform engineering workbench** for MediaHub OS. Evaluate **Dev Containers first** as a reproducible local development environment. Treat **GitHub Codespaces as an optional cloud development workspace**, not as a replacement for GitHub Actions hosted runners, the MediaHub AI Router, or the Gemini/Claude admission controllers.

Do not introduce Visual Studio IDE, Azure, Codespaces prebuilds, Copilot subscriptions, or any other paid service as a project dependency in this wave. No account settings, billing, secrets, repository code, workflows, or runtime configuration were changed.

## 2. Repository baseline inspected

Source snapshot: `main` at `f0448f28c7cfa61e4450c38529f09afbfdbbc7c7`.

- `.github/copilot-instructions.md` exists (blob `c1e5bea77bcfc38cbb62398d050d792ef62cd69b`). It already defines the project as the authoritative engineering source and requires preservation of State Authority, regression tests, secret hygiene, independent verification and security review for permissions/network/process/persistence/secrets/plugins/deployment.
- `.github/agents/` already contains MediaHub agent profiles; repository AI Factory verification requires a fixed set of architect, implementer, verifier, security and release roles.
- `.github/workflows/mediahub-ai-factory-verification.yml` exists (blob `ccad424e0d225d6f92e1e0589d3fc38ba1a37589`) and runs `scripts/verify_ai_factory.py` on matching pull requests and manual dispatch.
- `scripts/verify_ai_factory.py` exists (blob `e8a4a62dc480b23b5db452fe4a47527e3f44137a`) and checks the required agent files, AI Router policy, approved controller workflows and forbidden direct-provider routes.
- `.devcontainer/devcontainer.json` lookup returned NOT_FOUND. GitHub code search found no `devcontainer.json`, `.vscode/settings.json`, or Codespaces configuration on the default branch.
- `README.md` is currently only a minimal foundation statement; it does not describe a developer environment.

The existing agent and AI Factory controls should be reused. Do not create a second role registry, a competing instruction hierarchy, or an IDE-specific route around the approved controllers.

## 3. Microsoft/GitHub tool assessment

| Component | Project value | Disposition |
|---|---|---|
| Visual Studio Code | Cross-platform editor, Git, debugging, extensions and agent customization | **RECOMMENDED** |
| VS Code Dev Containers | Reproducible, isolated toolchain declared in `devcontainer.json` | **FIRST IMPLEMENTATION CANDIDATE** |
| GitHub Codespaces | Cloud-hosted development workspace usable in browser or VS Code | **OPTIONAL / COST-GATED** |
| GitHub Copilot in VS Code | Inline assistance and agent harness using repository instructions/agent profiles | **OPTIONAL / POLICY-GATED** |
| Visual Studio Community IDE | Useful mainly for Windows .NET/C++/WinUI/WPF workloads | **NOT A BASELINE DEPENDENCY** |
| Visual Studio Professional/Enterprise | Paid IDE/subscription capabilities | **OUT OF SCOPE** |
| Microsoft Foundry/Azure AI | Potential future provider/service integration | **NOT SELECTED; NO PAID ROUTE** |

### Why VS Code

It runs on macOS, Windows and Linux, matches the current repository stack (Python, TypeScript/YAML/JSON, GitHub Actions), and supports Dev Containers and Codespaces. Visual Studio IDE is not the same product as VS Code; the full IDE is primarily a Windows development environment. Visual Studio for Mac was retired in 2024, so it is not a suitable Mac-first baseline.

Visual Studio Community is free for individual developers and qualifying open-source/education use, but organization use is subject to license eligibility and limits. The project should not assume that Community is universally free for every organization or contractor.

### Why Dev Containers first

A checked-in `devcontainer.json` can describe a reproducible developer toolchain. VS Code runs the development tools and extensions inside the container and can attach to the same environment on a developer machine. This supports repeatable lint/test/build tooling without turning the container into a production runner or authority.

Security implication: code running inside the container, lifecycle scripts and installed extensions can access the mounted workspace and container environment. Therefore:
- no production or provider secrets in the dev container;
- no unreviewed lifecycle scripts or floating third-party features;
- pin images/features/extensions where practical;
- use non-root execution and least privilege where compatible;
- keep host mounts narrow;
- treat opened repositories and extensions as executable/untrusted input;
- never let local IDE agent mode bypass the approved task envelope, issuer/capability checks, model route, quota or review gates.

### Why Codespaces is optional

Codespaces offers a cloud-hosted development environment, but it is a separately metered product with plan, machine, storage and usage constraints. Prebuilds consume storage; repository/organization secrets configured for prebuilds can be available to users creating Codespaces from that repository. Thus prebuilds must not receive provider or production credentials. No free capacity, included quota, account entitlement or budget is assumed in this assessment.

Codespaces is a developer workspace, not evidence of an ephemeral GitHub Actions job, a qualified Runner Pool member, or a persistent GUI worker. Keep these identities and lifecycle contracts separate.

## 4. AI agent customization and governance

VS Code supports project customizations such as instructions, custom agents, prompt files, skills, tools and MCP integrations. The repository already has `.github/copilot-instructions.md` and `.github/agents/`; these are the starting point.

Proposed rules:
1. Preserve `.github/copilot-instructions.md` as the authoritative project-wide Copilot instruction file unless an explicit reviewed migration says otherwise.
2. Reuse the existing `.github/agents/` role definitions; do not duplicate Jarvis/Astra, Gemini, Claude, reviewer or security roles in a second registry.
3. If VS Code-specific targeted instructions are later justified, add small `.github/instructions/*.instructions.md` files only after checking for conflicting rules and adding them to the existing AI Factory verification contract.
4. Treat IDE instructions and agent tool restrictions as guidance, not as a security boundary. Enforcement remains in GitHub permissions, reviewed workflows, issuer/capability policy, secret isolation, branch protection, independent review and evidence checks.
5. Do not enable unrestricted terminal, MCP or local-agent capabilities for project work without explicit capability and host qualification.

## 5. Recommended staged adoption

### Stage 0 — documentation and compatibility (this wave)
- Record the tool decision and security boundaries.
- No code, billing, account or workflow changes.

### Stage 1 — minimal Dev Container proposal
Prepare a separate PR with:
- `.devcontainer/devcontainer.json` using a pinned, maintained base image;
- only required runtimes and deterministic tools for current Python/YAML/JSON validation;
- no `postCreateCommand` or lifecycle shell script unless strictly necessary and reviewed;
- no credentials, Docker socket mount, privileged mode, broad host mounts or network listener;
- a documented local command set matching existing CI;
- a deterministic check that the configuration parses and referenced assets exist.

Do not implement Stage 1 until the actual build/test command inventory is read from repository workflows and tool manifests. Do not add a large general-purpose image or speculative language stacks.

### Stage 2 — optional Codespaces evaluation
Only after Stage 1 and explicit budget/account entitlement verification:
- evaluate one short-lived, non-secret development workspace;
- record machine class, startup latency, runtime, storage and actual cost/quota consumption;
- disable or avoid prebuilds until storage cost and secret exposure are accepted;
- verify deletion/retention behavior;
- do not run production or provider-connected agent jobs there.

### Stage 3 — Copilot/VS Code agent workflow
- Verify that the current `.github/agents/` profiles and project instructions are discovered by the intended harness.
- Run a small, non-secret, read-only task and inspect the actual references/tool activity.
- Ensure the IDE does not create alternate dispatch, provider, credential or deployment routes.
- Any persistent agent role or MCP integration must be separately reviewed and mapped to existing Agent Registry, Runner Registry and AI Router contracts.

## 6. Acceptance criteria for a future implementation PR

- Immutable base SHA and exact changed-file list.
- No new provider, secret, paid service or runner authority.
- Dev Container uses pinned inputs and least privilege.
- Reproducible configuration validation and existing project tests pass.
- No conflicting instructions or duplicated agent registry.
- Security review covers container mounts, lifecycle commands, extensions, terminal access, MCP and secrets.
- Exact-head CI and independent review are verified.
- Codespaces remains disabled/not required unless separate budget and account evidence is approved.

## 7. Current PR and execution status

- PR #603 Wave 489 remains OPEN/DRAFT/UNMERGED; exact-head check API returned no statuses and no PR workflow runs; formal reviews: 0. It is unrelated to this research and is not treated as accepted.
- No Gemini/Claude agent dispatch, provider call, secret read, local host operation, Codespaces creation, billing change, workflow dispatch, merge, deployment or qualification was performed.
- This Wave 490 report is a documentation-only proposal on a branch based on the canonical docs commit. It is not yet part of the canonical map.

## 8. Official references

- VS Code documentation: https://code.visualstudio.com/docs
- Dev Containers: https://code.visualstudio.com/docs/devcontainers/containers
- GitHub Codespaces in VS Code: https://code.visualstudio.com/docs/remote/codespaces
- GitHub Codespaces documentation: https://docs.github.com/en/codespaces
- Codespaces prebuild security/secret configuration: https://docs.github.com/en/codespaces/prebuilding-your-codespaces/configuring-prebuilds
- VS Code custom instructions: https://code.visualstudio.com/docs/agent-customization/custom-instructions
- VS Code custom agents: https://code.visualstudio.com/docs/agent-customization/custom-agents
- Visual Studio Community: https://visualstudio.microsoft.com/vs/community/
- Visual Studio licensing: https://www.microsoft.com/licensing/guidance/Visual-Studio

## 9. Next

The next bounded step is Stage 1 preparation: inventory the exact CI toolchain and commands, then draft a minimal Dev Container proposal on a separate branch. Do not create Codespaces, enable prebuilds, add secrets or introduce Copilot as a required dependency.

Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
