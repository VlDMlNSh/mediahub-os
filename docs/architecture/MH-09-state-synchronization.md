# MH-09 — State Synchronization

**Status:** PROPOSED

The UI observes canonical state through bounded read models. Each model should carry revision/generation and freshness metadata where the source contract supports it.

On stale/conflicting mutation attempts, the UI presents the authoritative rejection and requests refresh; it does not rebase, merge, or apply hidden last-writer-wins behavior.

Optimistic presentation follows:

```text
Intent → Pending → Authorization → Command → Commit → Confirmed
```

Unknown outcomes remain unknown until authoritative evidence resolves them. Reconnect refreshes observation; it does not infer that a pending mutation committed.
