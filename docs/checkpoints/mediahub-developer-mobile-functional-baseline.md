# MediaHub Developer Mobile — Functional Baseline

Status: **Defined / queued for implementation in MH-25**

## 1. Product role
Developer Mobile is the personal AI Development Operator and developer control plane. It is not a development server and is not a MediaHub state authority.

Primary model: **User → Local Assistant → Coordination Layer + GitHub + Development Infrastructure**

The application orchestrates work while existing domain and security authorities remain authoritative.

## 2. Local Assistant
- Local-first, hardware-adaptive assistant/runtime.
- Assistant/runtime may be selected from suitable available projects and deployed on-device.
- Hardware capability is detected and mapped to an appropriate model/runtime.
- Model/runtime may change with device capability without changing the product architecture.
- Hybrid inference: local model; own inference server; development-cluster inference; external model/API providers.
- Routing is policy-driven and may select an available capable backend.

Conceptual pipeline: Hardware Profile → Capability Matrix → Assistant/Model Selection → Deployment → Verification → Runtime

## 3. Coordination Layer
The coordination layer is provider-agnostic.

Required capabilities: create development chats; read existing history; continue/close chats; transfer context; select relevant chat; create MH-25/MH-26 and later threads; coordinate GitHub and development infrastructure.

A shared URL is not a credential. Authentication, identity, session and capability authorization remain separate concerns.

## 4. GitHub integration
Authorized operations include repositories/mappings, issues, branches, commits, pull requests, project context and GitHub Actions workflows.

GitHub Actions must support authorized build/test/deploy workflows, including build, signing, staging, publishing and rollback workflows where corresponding workflows exist.

Developer Mobile is a control surface; GitHub is not the MediaHub state authority.

## 5. Projects
A Project is an orchestration boundary containing, as applicable: development chats; repositories and mappings; environments; credential references; tasks; development workspaces; terminals; artifacts; AI context; execution state; evidence.

Projects may span multiple repositories and environments.

## 6. Development Workspace
Developer Mobile exposes a higher-level Development Workspace rather than a raw terminal-only product.

Capabilities: terminal/PTY; files; processes; Git; builds; logs; jobs; long-running/background work; remote development sessions.

Terminal access is always subject to authorization and capability boundaries.

## 7. Development infrastructure
Developer Mobile controls authorized development infrastructure through established coordination/infrastructure mechanisms.

Server provisioning is not a new Developer Mobile authority/domain. Existing MediaHub development infrastructure remains responsible for node provisioning and admission.

## 8. Digital Clone
Complete multimodal scope: voice; visual/avatar; text/personality; multimodal source material; processing; training/fine-tuning where explicitly enabled; qualification; publication/revocation.

Storage domain: developer cluster. Current access policy: owner only.

## 9. Trusted Sources / Knowledge
Autonomous knowledge ingestion: Source → Fetch → Validate → Deduplicate → Extract → Classify → Index → Knowledge Update → Evidence.

Autonomous learning means knowledge/RAG ingestion by default. Model training is a separate explicit capability.

## 10. Media Studio
Supplier data remains on supplier websites.

Generation pipeline: Generate → Evaluate → Publish.

Media generation and publication may operate fully automatically according to configured task/instruction and authorization policy.

## 11. Web Studio
Supplier data is obtained from supplier websites.

Managed content: descriptions; categories; SEO; images; translation; prices; attributes; merchandising; instructions.

Publication pipeline: Generated → Review → Approved → Published. Human approval remains required before publication.

## 12. Releases / Updates
Developer Mobile is a release control surface.

Supported operations: build; sign; stage; publish; rollback.

Production release authority belongs to the user.

MediaHub's established update/recovery authority remains authoritative for MediaHub system state.

## 13. Authorization model
LOW — automatic within policy. Examples: read, inspection, logs, status, diagnostics, tests.

MEDIUM — always requires explicit user confirmation. Examples: package installation, controlled restarts, environment modifications and other medium-risk operations.

HIGH — always requires explicit user confirmation. Examples: production deployment, destructive operations, node destruction, credential rotation, production updates, publishing and material-blast-radius rollback.

AI may never silently escalate an operation between authorization levels.

## 14. Credential boundary
Developer Mobile and Local Assistant must not receive raw secret values merely to perform an authorized operation.

Intended model: credential reference + allowed operation + target scope, rather than exposing secret material to the assistant.

Implementation must preserve the invariant that Local Assistant cannot use general context as a secret extraction channel.

## 15. Activity / Evidence
Activity is an evidence system, not only a visual log.

Material operations should record: Action ID → Actor → Assistant → Project → Target → Authorization → Intent/Input → Execution → Result → Artifact → Evidence → Timestamp.

Evidence must allow later reconstruction of what the assistant did and what result was produced.

## 16. Offline / reconnect
Offline support where capability is local/cached: local inference; local project state; cached GitHub metadata; LAN/local development access where available; Digital Clone capture; source management; queued actions.

Remote operations require connectivity.

Reconnect lifecycle: Offline Queue → Revalidate → Authorize → Execute.

Queued actions must not bypass current authorization or execute stale destructive intent without revalidation.

## 17. Authority boundaries
- Developer Mobile UI ≠ authority.
- Local Assistant ≠ authority.
- AI ≠ authority.
- Coordination Chat ≠ authority.
- GitHub ≠ MediaHub state authority.
- Development infrastructure ≠ user-data authority.
- Development cluster ≠ local MediaHub canonical state.
- Remote terminal ≠ unrestricted shell capability.
- Search/knowledge ≠ authorization.

All actions resolve through the appropriate domain/security contracts.

## 18. MH-25 implementation queue
1. Developer Mobile application shell and project model.
2. Local Assistant runtime and hardware capability abstraction.
3. Model/assistant registry and routing policy.
4. Coordination adapter abstraction.
5. GitHub integration and GitHub Actions control.
6. Development Workspace/terminal abstraction.
7. Authorization and confirmation center.
8. Credential/capability boundary.
9. Digital Clone domain.
10. Trusted Source / Knowledge pipeline.
11. Media Studio.
12. Web Studio.
13. Release/update control surface.
14. Activity/Evidence system.
15. Offline queue and reconnect revalidation.
16. Qualification and accessibility tests.

Implementation must not silently alter established MediaHub architecture or authority boundaries.

## 19. State of this document
This document defines the functional contract. It does not claim implementation, qualification or production readiness.

Next phase: **Developer Mobile Visual / UX Baseline**, followed by transition to MH-25 autonomous implementation.
