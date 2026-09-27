from ops.astra_generated_e2e_cycle_1 import cycle_marker


def test_cycle_marker():
    assert cycle_marker() == "ASTRA_E2E_CYCLE_1"
