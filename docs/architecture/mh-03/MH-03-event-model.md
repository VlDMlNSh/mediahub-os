# MH-03 Event Model

`Event = fact that something happened.`

Events are produced after governed canonical mutation or bounded lifecycle facts. They are immutable observations of an occurrence, not authority grants.

Event consumers are observers/processors. An event handler must not infer mutation authority from event receipt.

Required properties: event identity, type, timestamp/ordering metadata as defined by contract, source, correlation context where applicable, and bounded payload.

Telemetry and diagnostics are observations and cannot become implicit commands.
