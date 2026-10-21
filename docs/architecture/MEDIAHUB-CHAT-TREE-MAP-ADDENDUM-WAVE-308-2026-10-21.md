# MediaHub Chat Tree Map — Wave 308 addendum

Date: 2026-10-21  
Status: provisional documentation on working branch; not canonical until accepted/integrated.

## New binding per-/next orchestration contract

- [Wave 308 report](../checkpoints/MEDIAHUB-NEXT-MULTI-AGENT-ALAMO-CLAUDE-AND-BROWSER-ORCHESTRATION-WAVE-308-2026-10-21.md)
- [Updated Bootstrap §1D](MEDIAHUB-CONTEXT-BOOTSTRAP-INSTRUCTION.md)
- [Continuation checkpoint](../checkpoints/mediahub-next-continuation-checkpoint-2026-10-12-current.md)
- [Canonical map branch/file](https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md)
- [Controller governance PR #421](https://github.com/VlDMlNSh/mediahub-os/pull/421)
- [Documentation working PR #430](https://github.com/VlDMlNSh/mediahub-os/pull/430)
- [Governing Issue #301](https://github.com/VlDMlNSh/mediahub-os/issues/301)

For every `/next`, the lead must prepare a shared immutable task packet and attempt the three distinct Gemini lanes, a local-only Claude Code task on Alamo/server 3 through a verified non-paid route, and SentinelX + agent-browser inspection when browser UI evidence is needed. The exact requirements, status semantics, report schema, fail-closed behavior and secret hygiene are in Bootstrap §1D and Wave 308.

## Operational constraints

- This is not a live scheduler and does not itself start agents.
- PR #421 remains open/draft/unmerged; the controller route is not to be treated as active before independent review, exact-head checks, caller-context/secret-boundary tests and governed integration.
- Current SentinelX inventory in Wave 308 showed only one operational host and two disabled hosts; designated Alamo/server 3 was not positively identified as operational.
- Do not claim browser inspection, Claude execution, or Gemini launch without actual run/session/job IDs and evidence.
- Canonical map remains unchanged until this addendum is accepted through the documentation workflow.
