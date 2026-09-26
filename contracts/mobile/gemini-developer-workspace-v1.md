# Gemini Developer Workspace — Mobile Contract v1

## Decision

MediaHub iOS Developer gets a persistent Development attachment action (`+`) that opens a dedicated Gemini Workspace sheet. This is preferable to a hidden on-demand command because file handling is a first-class developer workflow.

## Boundary

MediaHub iOS Developer
→ MediaHub AI Gateway
→ credential broker / authorized egress
→ Gemini Files API / Gemini GenerateContent or Interactions API

The mobile client never stores or receives a long-lived Gemini API secret.

## Isolation from this ChatGPT conversation

File bytes selected in Gemini Workspace are sent directly to the approved Gemini boundary. They are not pasted into the ChatGPT conversation and are not copied into the ChatGPT conversation transcript by default. The Control Plane stores only task/evidence metadata when a user explicitly creates a development task or qualification record.

## UX

Development section:
- Astra
- Gemini Workspace
- Tasks
- Qualifications
- Models
- Hosts
- Runs / Evidence
- Blocked / Recovery
- Diagnostics

Gemini Workspace:
- `+` Add file
- selected-file list with local upload state
- remove/cancel controls
- prompt field
- capability selector: Analyze / Extract / Review / Code / Document / Schematic
- Send
- result/evidence panel

## File lifecycle

SELECT → CLASSIFY → POLICY CHECK → UPLOAD DIRECTLY TO GEMINI → ANALYZE → RETURN RESULT → OPTIONAL DURABLE EVIDENCE REFERENCE

Default policy: uploaded bytes are not persisted in Control Plane task state. Only metadata/evidence references required by an explicit task are persisted.

## Supported use classes

- images
- PDFs/documents
- text/code files
- engineering schematics where supported by the selected Gemini model
- other Gemini-supported multimodal inputs after capability qualification

## Security

- no secret in iOS binary or UI state
- authorization before upload
- data classification before egress
- residency/egress policy enforcement
- audit of upload intent, model, result and evidence reference
- revocation support
- fail closed when Gemini route or policy is unavailable

## Qualification requirement

The workspace is not production-qualified merely because the UI exists. The Gemini route must have current live evidence for the requested capability class. Google documents Gemini 3.5 Flash-Lite as a current API model and documents multimodal/file inputs and structured outputs; MediaHub still requires its own live capability qualification before enabling each production capability.
