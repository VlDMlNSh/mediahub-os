# MH-03 Event Model

**Status:** PROPOSED

`Command = request to change`  
`Event = fact that something happened`

Events are emitted after canonical state mutation or other explicitly defined facts. Event delivery is observational/coordination-oriented and does not grant mutation authority.

Forbidden implicit conversions:
- Event → Command
- Telemetry → Mutation
- Recommendation → Mutation
- Observer → Mutation

If an event-driven reaction requires a state change, it must create a governed command and pass the normal authorization and State Authority path.
