# Astra Persistence Contract — 2026-09-25

## Purpose

This contract fixes the MediaHub autonomous development combination as a host-recovered resident stack rather than a chat-session-only process.

## Authoritative startup chain

`cron @reboot / 2-minute watchdog -> autonomous_watchdog.sh -> Astra Coordinator -> hybrid controller + command bus + autonomous loop`

The watchdog is the host-level recovery anchor. Astra remains the resident coordinator and owns the bounded child processes through its repository-owned lock/PID/heartbeat protocol.

## Fixed components

- `ops/astra_orchestrator.py` — resident coordinator and child supervisor.
- `ops/astra_command_bus.py` — bounded GitHub command ingress.
- `ops/astra_node_agent.py` — bounded node worker protocol.
- `ops/hybrid_orchestrator.py` — hybrid controller.
- `ops/autonomous_os_loop.sh` — bounded autonomous development loop.
- `ops/autonomous_watchdog.sh` — host reboot/crash recovery anchor.

## Safety properties

- No arbitrary external text is converted into shell commands.
- Process ownership is checked with PID start-time and command identity.
- Duplicate Astra instances are prevented by the Astra lock.
- `STOP` suppresses replacement until `RESUME`/`CONTINUE` removes the marker.
- Runtime state under `.autonomous/` is telemetry/control state, not authoritative durable Control Plane persistence.
- GitHub remains command ingress/audit surface, not runtime source of truth.

## Reboot behavior

The host crontab contains both an immediate `@reboot` watchdog entry and a periodic watchdog entry. The periodic entry is the continuing recovery mechanism; the lock prevents duplicate watchdog instances.

## Qualification boundary

This establishes host-level resident recovery. It does **not** qualify Control Plane persistence, crash-consistent durable task storage, or production readiness. Persistence qualification remains explicitly BLOCKED until the documented source-of-truth, migration, transaction/crash-consistency, and recovery requirements are accepted and tested.
