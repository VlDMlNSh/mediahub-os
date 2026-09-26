"""Bounded external-component adapters.

Adapters expose capabilities to MediaHub without granting external projects authority over canonical state.
"""
from collections.abc import Mapping
from dataclasses import dataclass
from enum import Enum


class ComponentTier(str, Enum):
    P0 = "P0"
    P1 = "P1"
    P2 = "P2"


class AuthorityBoundary(str, Enum):
    PROCESSING = "processing"
    OBSERVATION = "observation"
    RECOVERY = "recovery"
    DELIVERY = "delivery"


@dataclass(frozen=True)
class ComponentSpec:
    name: str
    tier: ComponentTier
    boundary: AuthorityBoundary
    canonical_authority: bool = False
    exact_pin_required: bool = True


SELECTED_COMPONENTS: tuple[ComponentSpec, ...] = (
    ComponentSpec("postgresql-pgvector", ComponentTier.P0, AuthorityBoundary.PROCESSING),
    ComponentSpec("s3-object-storage", ComponentTier.P0, AuthorityBoundary.PROCESSING),
    ComponentSpec("ifcopenshell", ComponentTier.P0, AuthorityBoundary.PROCESSING),
    ComponentSpec("paddleocr", ComponentTier.P0, AuthorityBoundary.PROCESSING),
    ComponentSpec("opencv-onnxruntime", ComponentTier.P0, AuthorityBoundary.PROCESSING),
    ComponentSpec("llama-cpp", ComponentTier.P0, AuthorityBoundary.PROCESSING),
    ComponentSpec("temporal", ComponentTier.P0, AuthorityBoundary.RECOVERY),
    ComponentSpec("opentelemetry-prometheus", ComponentTier.P0, AuthorityBoundary.OBSERVATION),
    ComponentSpec("restic", ComponentTier.P0, AuthorityBoundary.RECOVERY),
    ComponentSpec("rauc", ComponentTier.P0, AuthorityBoundary.RECOVERY),
    ComponentSpec("cosign-syft-trivy", ComponentTier.P0, AuthorityBoundary.DELIVERY),
    ComponentSpec("openbao", ComponentTier.P0, AuthorityBoundary.DELIVERY),
    ComponentSpec("web-ifc", ComponentTier.P1, AuthorityBoundary.PROCESSING),
    ComponentSpec("threejs-vtkjs", ComponentTier.P1, AuthorityBoundary.PROCESSING),
    ComponentSpec("opendronemap", ComponentTier.P1, AuthorityBoundary.PROCESSING),
    ComponentSpec("gpu-llm-selected-after-benchmark", ComponentTier.P1, AuthorityBoundary.PROCESSING),
    ComponentSpec("k3s-argo-cd", ComponentTier.P2, AuthorityBoundary.RECOVERY),
)


def component_registry() -> Mapping[str, ComponentSpec]:
    """Return an immutable-by-convention registry keyed by component name."""
    return {item.name: item for item in SELECTED_COMPONENTS}


def validate_external_write(component: ComponentSpec, writes_canonical_state: bool) -> None:
    """Reject any adapter design that turns an external component into an authority."""
    if writes_canonical_state or component.canonical_authority:
        raise ValueError(f"external component cannot be canonical authority: {component.name}")
