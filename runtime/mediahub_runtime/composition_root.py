"""MH-05 production composition root for the governed runtime prototype."""

from .consumer_boundary import ConsumerBoundary
from .state_authority import StateAuthority


class CompositionError(RuntimeError):
    """Raised when the canonical runtime graph cannot be constructed safely."""


def build_runtime(initial_state=None, policy=None):
    """Construct the only supported runtime graph.

    The StateAuthority instance created here is the sole canonical mutation
    authority. Consumers receive only the governed ConsumerBoundary and never
    receive a second state/event/persistence authority.
    """
    authority = StateAuthority(initial_state=initial_state, policy=policy)
    boundary = ConsumerBoundary(authority)

    graph = {
        "state_authority": authority,
        "consumer_boundary": boundary,
    }
    if graph["state_authority"] is not authority:
        raise CompositionError("canonical authority construction failed")
    if graph["consumer_boundary"]._authority is not authority:
        raise CompositionError("boundary is not bound to canonical authority")
    return graph


def canonical_authority(graph):
    """Return the canonical StateAuthority from a validated composition graph."""
    authority = graph.get("state_authority") if isinstance(graph, dict) else None
    if not isinstance(authority, StateAuthority):
        raise CompositionError("invalid composition graph")
    return authority
