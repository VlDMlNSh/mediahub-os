# MediaHub AI OS stack

## Installed baseline
- Ollama 0.34.1
- Local model: qwen2.5-coder:3b
- MediaHub AI contracts and provider registry
- Local-first orchestration policy
- Astra token economy policy
- Agent registry with external providers opt-in

## Agent duties
- Astra: planning, delegation, policy enforcement, evidence aggregation.
- Ollama: default local inference and private tasks.
- Claude: engineering and architecture when explicitly enabled.
- Cursor: repository-native implementation when explicitly enabled.
- Gemini: multimodal/document analysis when explicitly enabled.
- Perplexity: web research and source collection when explicitly enabled.
- Kimi: long-context/reasoning tasks when explicitly enabled.
- DeepSeek: coding, reasoning and batch workers when explicitly enabled.
- ChatGPT: general reasoning/analysis when explicitly enabled.

## Cost rule
The core system must remain functional without paid external AI APIs.
External providers are opt-in and use user-owned credentials.
