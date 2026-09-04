# MediaHub Architecture Chat Governance

## Purpose

MH-1…MH-23 are architecture guardian chats. They preserve the reference architecture and its decisions. They are not development workspaces.

The GitHub repository is the durable external record so that architecture does not depend solely on ChatGPT conversation history.

## Separation of concerns

### Architecture chats

Allowed:

- architecture decisions;
- invariants;
- contracts;
- boundaries;
- dependency/traceability analysis;
- evidence review;
- contradiction and unknown registers;
- ADR decisions;
- acceptance gates;
- master prompts and reverse master prompts.

Not allowed:

- production implementation;
- prolonged debugging;
- feature development;
- ad-hoc code iteration;
- turning the architecture chat into the development workspace.

### Development chat

Owns implementation, debugging, code iteration and ordinary engineering work.

It consumes architecture through the master prompts and reports architecture-impacting findings through reverse master prompts.

It must not silently alter architecture authority.

## Change flow

```text
Architecture Chat
   -> GitHub architecture record
   -> Master Prompt
   -> Development Chat
   -> Implementation / Tests
   -> Reverse Master Prompt
   -> Architecture Review
   -> ADR / Governance Decision
   -> GitHub architecture update
```

## Source-of-record policy

Chat context is useful for reasoning but is not the only durable record. Material architecture decisions must be synchronized to GitHub.

When chat and GitHub disagree, do not silently choose one. Mark the discrepancy as a contradiction and resolve it through explicit architecture governance.

## Implementation prohibition

An architecture document may define an implementation gate, but the architecture chat itself does not authorize implementation merely by discussing it. Physical implementation requires the explicit gate defined by the relevant architecture.

## MH-14 special rule

For MH-14:

- State Authority remains sole canonical mutation authority.
- Persistence is storage, not authority.
- Physical persistence implementation is NOT AUTHORIZED until separate governance authorization.
- Database/filesystem code is not architecture approval.
- Hardware, OS, filesystem and durability claims require evidence.
