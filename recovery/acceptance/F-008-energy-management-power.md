# MediaHub — F-008 Energy Management / Power

Date: 2026-09-04
Status: CONFIRMED_ACCEPTED

## Functional requirements

### Energy sources
- Grid power, UPS, solar generation, inverters, batteries, generators and other supported sources are part of the MediaHub energy domain.

### Observation
- Where technically available, MediaHub observes source availability/state, power, consumption, generation, battery charge/discharge, available energy, UPS state, inverter state, generator state and relevant alarms.

### Unified energy model
- Energy equipment is represented through a unified MediaHub model independent of vendor/protocol.
- User-facing model is Source → Storage → Consumer → State → Energy.

### Automation
- Energy state can participate in automation, scheduling, notifications, diagnostics, Local Assistant and other authorized functions.
- Examples include controlled UPS transition, use of available solar generation, limiting non-critical loads at low battery, and changing modes after grid restoration.
- Exact optimization and priority algorithms remain deferred.

### UPS
- UPS state, charge, power source, alarms and relevant transitions can be integrated where equipment supports them.
- UPS state can affect automation and system behavior.

### Solar / inverter / battery
- MediaHub can model relationships among solar generation, inverter, battery, grid and loads where supported by the equipment.

### Generator
- Generator presence, state, availability, alarms and, where technically safe and supported, start/stop and source switching can participate in the energy model.

### Smart Home integration
- Energy integrates with Smart Home devices and automation.

### Cluster
- MediaHub Cluster may account for node energy consumption, node availability and compute workload distribution under power constraints.

### Professional / Engineer
- Energy is part of the engineering model and can be associated with electrical design, distribution panels, cabling, loads, UPS, solar, batteries, inverters, generators and automation.

### Local-first
- Critical local energy reactions should continue without Internet when the required local infrastructure is available.

## Explicitly deferred technical decisions

1. Specific vendors.
2. Protocols.
3. Supported inverter models.
4. UPS models.
5. Battery systems.
6. Generator models.
7. Exact control commands.
8. Source priorities.
9. Optimization algorithms.
10. Tariff handling.
11. Generation/consumption forecasting.
12. V2G/grid-interaction details.
13. Exact safety classes for energy operations.

## Main invariant

MediaHub treats home energy as one integrated system of sources, storage and consumers rather than a collection of unrelated devices.
