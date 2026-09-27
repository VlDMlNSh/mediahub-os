from ops.astra_generated_ollama_e2e import cycle_marker

def test_cycle_marker():
    assert cycle_marker() == "ASTRA_OLLAMA_E2E"
