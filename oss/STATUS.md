# OSS implementation status

This wave implements MediaHub-owned contracts and safety gates; it does not claim upstream runtimes are production-qualified.

| Wave | Component family | Code boundary | Activation |
|---|---|---|---|
| W0 | Protobuf/gRPC | contract layer | foundation |
| W0 | OpenTelemetry/Prometheus | observation interfaces | foundation |
| W0 | Cosign/Syft/Trivy | evidence policy | foundation |
| W1 | SOPS/age/OpenBao | secret/config boundary | SOPS/age foundation; OpenBao gated |
| W2 | PostgreSQL/pgvector | persistence/vector contracts | target-gated |
| W2 | restic/object storage | backup contracts | restic target-gated; object storage future-gated |
| W3 | Home Assistant Core | Smart Home authority adapter | target-gated |
| W4 | FFmpeg/OpenCV/PaddleOCR | bounded media/OCR/CV | FFmpeg foundation; OCR/CV gated |
| W5 | ONNX Runtime/llama.cpp | local inference contract | target-gated |
| W6 | IfcOpenShell/web-ifc | digital-twin contract | target-gated |
| W7 | NATS/JetStream/etcd | transport/coordination | future-gated |
| W8 | RAUC/cluster/cloud | update/deployment | RAUC target-gated; cluster/cloud reference/future |

## Hard invariants

- No OSS component is a second State Authority.
- Home Assistant Core is authoritative only for Smart Home domain.
- AI runtimes provide inference only; MediaHub owns routing and escalation.
- Persistence is not activated by this package and does not replace the MH-03 in-memory authority.
- Backup implementations never define recovery policy.
- Observability is non-authoritative.
- Unbounded media execution is rejected.
- Qualification and independent review remain release gates.
