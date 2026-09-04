# MH-11 — Tracing

Status: PROPOSED

Tracing correlates execution with trace ID, span ID, parent/child relationships, timestamps, latency, status and bounded attributes. The intended chain is intent → consumer → authorization → command → State Authority → runtime → result. A trace is never a command or authority.
