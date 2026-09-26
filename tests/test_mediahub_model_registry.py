import pytest

from ops.mediahub_model_registry import ModelRecord, ModelRegistry


def test_unknown_model_denied():
    r=ModelRegistry((ModelRecord("openai","qualified-model"),))
    try: r.require("openai","unknown")
    except PermissionError: pass
    else: assert False

def test_disabled_model_denied():
    r=ModelRegistry((ModelRecord("anthropic","retired-model",False),))
    try: r.require("anthropic","retired-model")
    except PermissionError: pass
    else: assert False

def test_qualified_model_allowed():
    r=ModelRegistry((ModelRecord("openai","qualified-model"),))
    assert r.require("openai","qualified-model").model == "qualified-model"

def test_registry_rejects_malformed_record_types():
    for value in ((object(),), (None,), (ModelRecord(1, "model"),), (ModelRecord("openai", 1),)):
        with pytest.raises(ValueError):
            ModelRegistry(value)
