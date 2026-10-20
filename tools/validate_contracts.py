#!/usr/bin/env python3
"""Validate the canonical MediaHub OS schema tree.

Audit defect D2 resolved the `contracts/` vs `schemas/` duplication in favour
of a single canonical source: ``schemas/``. This validator therefore walks
``schemas/`` (not ``contracts/``) and enforces:

- every schema passes the official JSON Schema Draft 2020-12 meta-schema and
  declares a non-empty ``$id``;
- schema format names are recognized and the shared instance validator applies
  format assertions (for example, RFC 3339 date-time and URI checks);
- the common metadata envelope (``schema_id``/``schema_version``/``owner``) is
  all-or-nothing: a schema either opts out entirely or declares all three, and
  ``schema_version`` must be a string carrying an ``X.Y.Z`` value when
  constrained;
- the identity boundary preserves canonical identity separation.

Exit code is 0 on success and 1 on the first failure (fail-closed).
"""

import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker
from jsonschema.exceptions import SchemaError

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_ROOT = ROOT / "schemas"
IDENTITY_BOUNDARY = (
    SCHEMA_ROOT / "identity" / "identity-boundary.schema.json"
)

DRAFT_2020_12 = "https://json-schema.org/draft/2020-12/schema"

METADATA_KEYS = ("schema_id", "schema_version", "owner")
FORMAT_CHECKER = FormatChecker()


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    raise SystemExit(1)


def validate_json(path: Path) -> dict:
    try:
        with path.open(encoding="utf-8") as handle:
            data = json.load(handle)
    except Exception as exc:
        fail(f"{path}: invalid JSON: {exc}")

    if not isinstance(data, dict):
        fail(f"{path}: top-level document is not an object")

    return data


def validate_common_metadata(path: Path, data: dict) -> bool:
    """Validate the optional common metadata envelope.

    Returns True when the schema carries the envelope, False when it opts out.
    """
    properties = data.get("properties", {})

    present = [key for key in METADATA_KEYS if key in properties]

    if not present:
        return False

    if len(present) != len(METADATA_KEYS):
        missing = sorted(set(METADATA_KEYS) - set(present))
        fail(f"{path}: incomplete metadata envelope, missing {missing}")

    schema_version = properties["schema_version"]

    # JSON Schema permits boolean subschemas. The metadata envelope, however,
    # must explicitly constrain schema_version to a string or string constant.
    if not isinstance(schema_version, dict):
        fail(f"{path}: schema_version must be an object schema")

    version_type = schema_version.get("type")
    version_const = schema_version.get("const")

    if "const" in schema_version and not isinstance(version_const, str):
        fail(f"{path}: schema_version const must be a string")

    if version_type != "string" and not isinstance(version_const, str):
        fail(f"{path}: schema_version must be a string")

    if isinstance(version_const, str):
        parts = version_const.split(".")
        if len(parts) != 3 or not all(part.isdigit() for part in parts):
            fail(f"{path}: invalid schema version: {version_const}")

    return True


def validate_format_names(path: str, schema: object) -> None:
    """Reject unknown format names in schema nodes, not arbitrary example data."""
    if not isinstance(schema, dict):
        return

    format_name = schema.get("format")
    if format_name is not None and format_name not in FORMAT_CHECKER.checkers:
        fail(f"{path}: unsupported JSON Schema format: {format_name}")

    mapping_keywords = (
        "$defs",
        "definitions",
        "properties",
        "patternProperties",
        "dependentSchemas",
    )
    single_keywords = (
        "additionalProperties",
        "unevaluatedProperties",
        "propertyNames",
        "items",
        "contains",
        "unevaluatedItems",
        "not",
        "if",
        "then",
        "else",
        "contentSchema",
    )
    array_keywords = ("allOf", "anyOf", "oneOf", "prefixItems")

    for keyword in mapping_keywords:
        children = schema.get(keyword)
        if isinstance(children, dict):
            for child in children.values():
                validate_format_names(path, child)

    for keyword in single_keywords:
        child = schema.get(keyword)
        if isinstance(child, dict):
            validate_format_names(path, child)

    for keyword in array_keywords:
        children = schema.get(keyword)
        if isinstance(children, list):
            for child in children:
                validate_format_names(path, child)


def build_validator(schema: dict, source: str = "<schema>") -> Draft202012Validator:
    """Build a standards-based Draft 2020-12 validator with format assertions."""
    try:
        Draft202012Validator.check_schema(schema)
    except SchemaError as exc:
        fail(f"{source}: invalid JSON Schema Draft 2020-12: {exc.message}")
    validate_format_names(source, schema)
    return Draft202012Validator(schema, format_checker=FORMAT_CHECKER)


def validate_schema(path: Path) -> bool:
    data = validate_json(path)

    if data.get("$schema") != DRAFT_2020_12:
        fail(f"{path}: unsupported or invalid $schema")

    if not data.get("$id"):
        fail(f"{path}: missing $id")

    build_validator(data, str(path))
    has_envelope = validate_common_metadata(path, data)

    print(f"PASS {path}")

    return has_envelope


def validate_identity_boundary() -> None:
    path = IDENTITY_BOUNDARY

    if not path.exists():
        fail("identity boundary schema is missing")

    data = validate_json(path)

    identities = (
        data.get("properties", {})
        .get("identities", {})
        .get("properties", {})
    )

    expected = {
        "device_id",
        "binding_id",
        "adapter_id",
        "adapter_instance_id",
        "capability_id",
        "event_id",
        "command_id",
        "execution_id",
        "request_id",
        "correlation_id",
        "causation_id",
        "recovery_id",
    }

    actual = set(identities)

    if actual != expected:
        fail(
            "identity boundary mismatch: "
            f"expected={sorted(expected)} actual={sorted(actual)}"
        )

    if "universal_id" in actual:
        fail("forbidden universal_id detected")

    print("PASS identity separation")


def main() -> int:
    files = sorted(SCHEMA_ROOT.glob("**/*.json"))

    if not files:
        fail("no schemas found under schemas/")

    envelope_contracts = 0

    for path in files:
        if validate_schema(path):
            envelope_contracts += 1

    if envelope_contracts == 0:
        fail("no metadata-envelope contracts found under schemas/")

    validate_identity_boundary()

    print(f"CONTRACT_FILES={len(files)}")
    print(f"ENVELOPE_CONTRACTS={envelope_contracts}")
    print("CONTRACT_VALIDATION=PASS")

    return 0


if __name__ == "__main__":
    sys.exit(main())
