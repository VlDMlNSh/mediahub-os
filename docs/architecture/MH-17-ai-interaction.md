# MH-17 — AI / Device Interaction

**Status:** CANDIDATE

AI may analyze telemetry, detect anomalies, predict failure, recommend actions and generate proposals. AI output remains inert data until an ordinary authorization path accepts it.

Forbidden paths:
`AI → Device direct`, `AI → self-authorize`, `AI → grant capability`, `AI → bypass policy`.

Candidate path:
`AI proposal → Policy evaluation → Authorization → Consumer Boundary → State Authority → Adapter → Device`.

Confidence is an input to decision support, never an authority primitive. AI-generated state remains explicitly attributed and cannot silently overwrite device-reported or confirmed state.