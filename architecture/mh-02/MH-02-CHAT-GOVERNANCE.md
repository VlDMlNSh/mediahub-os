# MH-02 — Chat Governance / Architecture-Only Rule

## Role of architecture chats
MH-01…MH-23 are canonical architecture/governance custodians in ChatGPT. They are not implementation workspaces.

## Development chat
Implementation is performed in a separate development chat. The development chat may consult architecture chats through a Master Prompt / Reverse Master Prompt exchange.

## Forbidden in architecture chats
- implementation work;
- production coding sessions;
- prolonged implementation discussion;
- debugging implementation details;
- technology commitment without architecture decision;
- silent modification of frozen contracts;
- contamination of canonical architecture with development chatter.

## Allowed
- architecture decisions;
- reconciliation;
- evidence review;
- contradiction registration;
- acceptance/freeze decisions;
- master prompts to development chat;
- reverse master prompts from development chat;
- concise implementation constraints needed to preserve architecture.

## Source-of-truth rule
For long-term architecture, the ChatGPT architecture chats are the canonical custodians as explicitly designated by project governance. GitHub is a synchronized archival/versioned mirror and engineering repository, not an authority that can silently override architecture chats.

## Sync rule
GitHub changes representing architecture must be traceable to an accepted/proposed architecture-chat decision. Implementation branches/PRs must not redefine MH-01…MH-23.
