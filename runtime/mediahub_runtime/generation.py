"""Generation identity and compatibility checks."""

from dataclasses import dataclass

from .errors import GenerationMismatch


@dataclass(frozen=True)
class Generation:
    generation_id: str
    binary_version: str
    schema_version: str
    state_version: str
    integrity_reference: str

    def __post_init__(self):
        for name in (
            "generation_id",
            "binary_version",
            "schema_version",
            "state_version",
            "integrity_reference",
        ):
            value = getattr(self, name)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{name} must be a non-empty string")


def validate_generation_compatibility(binary, schema, state):
    """Require an exact version tuple for an authoritative generation."""
    if (
        not isinstance(binary, Generation)
        or not isinstance(schema, Generation)
        or not isinstance(state, Generation)
    ):
        raise TypeError("generation components must be Generation instances")

    tuples = {
        (
            binary.generation_id,
            binary.binary_version,
            binary.schema_version,
            binary.state_version,
        ),
        (
            schema.generation_id,
            schema.binary_version,
            schema.schema_version,
            schema.state_version,
        ),
        (
            state.generation_id,
            state.binary_version,
            state.schema_version,
            state.state_version,
        ),
    }
    if len(tuples) != 1:
        raise GenerationMismatch(
            "binary, schema and state generations are incompatible"
        )

    return True
