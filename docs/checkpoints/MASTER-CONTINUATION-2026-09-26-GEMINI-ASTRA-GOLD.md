# MediaHub — Master Continuation Checkpoint 2026-09-26

## Purpose

This checkpoint is the authoritative continuation handoff for the MediaHub OS / MediaHub iOS development thread. Continue from repository state and evidence, not from conversational assumptions.

## Immutable architectural principles

- MediaHub State Authority is the canonical platform-state authority.
- Home Assistant Core is the Smart Home domain authority.
- AI is advisory/proposal-producing and controlled; it is never release or production authority.
- Cloud Development AI is non-authoritative and crosses controlled gateway boundaries.
- Local-first operation remains mandatory.
- Git provenance, persistent Control Plane state, audit and evidence are mandatory.
- Ambiguity fails closed.
- External side effects require idempotency/reconciliation semantics.
- Untrusted model output never becomes unrestricted shell execution.
- RELEASE and PRODUCTION remain LOCKED until independent qualification gates pass.

## Required autonomous lifecycle

DISCOVER -> PLAN -> READY -> SELECT -> CLAIM -> EXECUTE -> VERIFY -> RECORD -> COMMIT -> PUSH -> QUALIFY -> CLOSE -> GENERATE_NEXT

A task is not DONE without machine-verifiable implementation, verification, tests, required qualification, evidence and durable record.

## Current repository

Repository: VlDMlNSh/mediahub-os
Branch: engineering/mh21-sandbox-lifecycle-20260910
Latest known commit before this checkpoint: 8c19af0
Previous key commits include 3eb9793, 48960c4, 6dda143, 5637ba4.

## Current evidence

- Control Plane focused local autonomous tests: 102 passed.
- Recent full project regression previously recorded: 897 passed.
- Independent fresh checkout verification previously recorded: 232 passed.
- SQLite backup/recovery qualification exists and was previously regression-tested.
- Exactly-once resolved-operation deduplication is implemented and tested.
- Ambiguous transport defaults to fail-closed unless explicitly authorized.
- Duplicate command bus ownership is fenced.
- Astra supervisor/heartbeat/STOP semantics are implemented.
- DF3 Apple development lane is qualified at the recorded scope.
- DF3 Ollama 0.34.4 is installed and serving qwen2.5-coder:1.5b.
- DF3 Qwen model digest: d7372fd828518a4d38b1eb196c673c31a85f2ed302b3d1e406c4c2d1b64a0668.
- DF3 Qwen exact-marker generation succeeded: MEDIAHUB_PING_OK / coding marker.
- The local autonomous coding E2E still requires an admissible patch + verify + commit + push pass before GOLD.

## Gemini 3.5 Flash-Lite

Official Google documentation currently lists gemini-3.5-flash-lite as an available Gemini API model and documents multimodal inputs, structured JSON output, image/file/document inputs and the Files API.

Project routing already contains gemini-3.5-flash-lite as the preferred cloud development route when a legitimate GEMINI_API_KEY is injected through the approved credential boundary.

Recorded prior live provider evidence: Gemini 3.5 Flash-Lite route returned HTTP 200 and the exact live marker in GitHub Actions run 36240130439. This is text/smoke evidence only, not full multimodal qualification.

Current DF3 environment has GEMINI_API_KEY ABSENT. Do not invent, print or request the secret value. A new live qualification must run only through the trusted credential boundary.

Full Gemini qualification still OPEN:
- text exact marker;
- structured JSON schema;
- image input;
- file upload/input;
- PDF/document/schematic input;
- coding/diff generation;
- failure classification;
- latency/resource evidence;
- digest/version/model identity;
- sanitized evidence record.

The existing GitHub live-provider workflow can perform text smoke qualification but must be extended/used through a trusted dispatch path that actually supports the target ref before claiming new evidence.

## DF3 local model qualification issue found in this wave

ops/mediahub_model_qualification.py originally targeted /api/chat, while the qualified DF3 Ollama lane reliably responds through /api/generate. The qualification utility was corrected to use /api/generate for deterministic completion and coding qualification. This correction itself must be regression-tested and committed; it does NOT by itself qualify the model.

## Mobile Gemini file UX decision

Do NOT attempt to alter the ChatGPT application's own UI from this repository. The product implementation belongs in MediaHub iOS Developer.

Chosen product pattern: persistent Developer-section attachment action (plus/add-files button), opening a dedicated Gemini Workspace sheet. The selected files are uploaded directly from the MediaHub app to the Gemini Files API / approved Gemini gateway, rather than being copied into the ChatGPT conversation. The chat should receive only a small metadata/evidence reference when policy allows; file bytes must not be embedded into the ChatGPT conversation history.

Required boundary:
MediaHub iOS Developer -> MediaHub AI Gateway -> Gemini file upload / inference

Never put GEMINI_API_KEY in the mobile client. Use the approved credential broker/gateway. File uploads must be isolated from the Control Plane task transcript unless an explicit task creates a durable evidence reference.

Proposed Developer section:
- Development / Astra
- Gemini Workspace
- Tasks
- Qualifications
- Models
- Hosts
- Runs / Evidence
- Blocked / Recovery
- Logs / Diagnostics

## GOLD gates still open

1. DF3 local model coding patch E2E.
2. Mid-task worker/agent crash recovery.
3. DF1 cold boot and recovery qualification.
4. DF2 cold boot and recovery qualification.
5. DF3 physical cold boot and recovery qualification.
6. DF1 <-> DF2 <-> DF3 distributed E2E.
7. Network partition/fencing test.
8. Automatic task generation and dependency-aware scheduling proof.
9. Automatic qualification scheduler proof.
10. Gemini full multimodal qualification.
11. Zhipu/GLM live qualification with legitimate credential.
12. Claude Code -> OmniRoute context-safe E2E.
13. Independent security sweep (Strix or equivalent).
14. 24h soak completion.
15. 72h soak completion.
16. Final disaster-recovery matrix.
17. GOLD acceptance matrix and independent verification.

## Passport 1.0

The full MEDIAHUB OS 11.x LTS / MEDIAHUB iOS FUNCTIONAL BASELINE 1.0 supplied in the conversation is the product functional baseline. Do not silently narrow it. Preserve its core requirements: State Authority, Home Assistant authority, unified UI, Smart Home, Media, Documents, Digital Twin, Engineering, Network, Local AI, Local Cluster AI, Cloud Development AI, Trusted Sources Intelligence, authorized AI Human Clone, two-app Mobile Access Layer, local-first operation, controlled cloud escalation, security/provenance, observability, PostgreSQL/pgvector/object storage target architecture, mature OSS adoption gates, RAUC update authority, backup/recovery, release gates, and autonomous-development governance.

## Next autonomous sequence

OBSERVE -> RECONCILE -> SELECT highest admissible open gate -> CLAIM -> EXECUTE -> VERIFY -> RECORD -> COMMIT -> PUSH -> QUALIFY -> GENERATE_NEXT.

Never mark a blocked gate as passed. Physical reboot gates require an actual reboot event. Live provider gates require fresh live evidence. Independent security gates require independent evidence.
