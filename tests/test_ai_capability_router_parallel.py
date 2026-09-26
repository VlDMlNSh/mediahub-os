from ops.mediahub_ai_capability_router import AIProvider, routing_lanes


def test_gemini_is_a_specialist_lane_not_a_fallback():
    lanes = routing_lanes(
        "architecture",
        healthy=frozenset({AIProvider.GEMINI, AIProvider.OPENROUTER, AIProvider.FCM, AIProvider.OMNIROUTE, AIProvider.LOCAL_QWEN}),
    )
    assert (AIProvider.GEMINI,) in lanes
    assert len(lanes) == 1


def test_local_development_lane_has_ordered_degradation():
    lanes = routing_lanes(
        "code_generation",
        healthy=frozenset({AIProvider.OPENROUTER, AIProvider.FCM, AIProvider.OMNIROUTE, AIProvider.LOCAL_QWEN}),
    )
    assert lanes == ((AIProvider.OPENROUTER, AIProvider.FCM, AIProvider.OMNIROUTE, AIProvider.LOCAL_QWEN),)


def test_other_cloud_is_separate_lane_when_local_is_unavailable():
    lanes = routing_lanes(
        "code_generation",
        healthy=frozenset({AIProvider.LOCAL_QWEN, AIProvider.OTHER_CLOUD}),
    )
    assert lanes == ((AIProvider.LOCAL_QWEN,),)
