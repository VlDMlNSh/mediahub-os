# MH-10 AI Authority Boundary

AI MAY: read authorized data; transform; classify; infer; predict; summarize; explain; rank; recommend; create inert proposals; detect anomalies; plan within bounded scope.

AI MUST NOT: modify canonical state directly; authorize itself; grant/revoke capabilities; alter policy silently; bypass Consumer Boundary; access raw State Authority; create unrestricted credentials; use unrestricted filesystem/shell/network; execute critical operations solely on model output; treat confidence as authorization.

Authorization chain:
`Proposal → Policy Evaluation → Authorization → Command → Consumer Boundary → State Authority`.

A model, agent, plugin, tool, orchestrator, RAG result or cloud provider does not inherit authority merely by being reachable or callable.
