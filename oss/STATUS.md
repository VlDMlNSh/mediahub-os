# MediaHub OSS implementation status

| Wave | Capability | Code boundary | Production activation |
|---|---|---|---|
| W0 | contracts/observability/supply-chain | implemented | gated |
| W1 | SOPS/age/OpenBao | contract baseline | gated |
| W2 | PostgreSQL/pgvector/restic/object storage | implemented boundaries | gated |
| W3 | Home Assistant Core | Smart Home boundary | gated |
| W4 | FFmpeg/OpenCV/PaddleOCR | bounded processing | gated |
| W5 | ONNX Runtime/llama.cpp | inference/routing boundary | gated |
| W6 | IfcOpenShell/web-ifc | Digital Twin boundary | gated |
| W7 | NATS/JetStream/etcd | transport/coordination boundary | future-gated |
| W8 | RAUC/cluster/cloud | OTA boundary | future/target-gated |

## Qualification rule
No component may transition to active without complete MediaHub-owned qualification evidence and independent review.

## Authority rule
No OSS component may become MediaHub State Authority. Home Assistant Core may be authoritative only inside the Smart Home domain. Observability, backup, transport, AI and engineering components remain non-authoritative.

## Runtime rule
The frozen MH-03 runtime remains unchanged until a separately governed migration establishes persistence, HA and other target capabilities.
