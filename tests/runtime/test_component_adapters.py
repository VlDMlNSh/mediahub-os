from runtime.mediahub_runtime.component_adapters import (
    AuthorityBoundary,
    ComponentTier,
    component_registry,
    validate_external_write,
)


def test_registry_contains_only_selected_components():
    registry = component_registry()
    assert registry["postgresql-pgvector"].tier is ComponentTier.P0
    assert registry["opentelemetry-prometheus"].boundary is AuthorityBoundary.OBSERVATION
    assert registry["rauc"].boundary is AuthorityBoundary.RECOVERY


def test_external_components_cannot_become_authority():
    component = component_registry()["ifcopenshell"]
    validate_external_write(component, writes_canonical_state=False)

    try:
        validate_external_write(component, writes_canonical_state=True)
    except ValueError as exc:
        assert "cannot be canonical authority" in str(exc)
    else:
        raise AssertionError("authority escalation was not rejected")
