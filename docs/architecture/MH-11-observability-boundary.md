# MH-11 Observability Boundary

Status: PROPOSED

```text
Runtime / Services
      ↓
Observability Adapter
      ↓
Logs / Metrics / Traces / Events / Audit / Telemetry
      ↓
Bounded Collector
      ↓
Authorized Storage / Viewer
```

Observability adapters are passive where possible, bounded and failure-contained. They may read explicitly exposed data and publish diagnostic information. They must not directly mutate canonical runtime state.

Diagnostic clients access read models through an authorized consumer/diagnostic boundary. Any requested mutation follows the ordinary authorization and State Authority path.
