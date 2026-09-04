# MH-09 — Read Model

**Status:** PROPOSED

A presentation read model is bounded, immutable/value-semantic from the UI perspective, authorization-filtered, privacy-aware and presentation-oriented. It is not an alias of internal runtime state and is not a mutation primitive.

Required metadata where applicable: source, revision/generation, timestamp, freshness and explicit availability state.

Canonical freshness vocabulary: current, stale, cached, unavailable, estimated, predicted, recommended. Silent stale presentation is forbidden.

The model must not expose raw State Authority objects, mutable references, transaction handles, persistence handles, secrets or unrestricted diagnostic internals.

Read models may be reconstructed after reconnect/restart without implying mutation. Cache state remains non-canonical.
