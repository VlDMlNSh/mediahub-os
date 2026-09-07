#!/usr/bin/env python3

import json
import sys
from json import JSONDecodeError
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT_ROOT = ROOT / "contracts"

def fail(message: str) -> None:
    print(f"FAIL: {message}")
    raise SystemExit(1)

def validate_json(path: Path) -> dict:
    try:
        with path.open(encoding="utf-8") as handle:
            data = json.load(handle)
    except (JSONDecodeError, OSError, UnicodeDecodeError) as exc:
        fail(f"{path}: invalid JSON: {exc}")

    if not isinstance(data, dict):
        fail(f"{path}: top-level document is not an object")

    return data

def validate_common_metadata(path: Path, data: dict) -> None:
    required = {
        "schema_id",
        "schema_version",
        "owner",
    }

    properties = data.get("properties", {})

    if not required.issubset(properties):
        missing = sorted(required - set(properties))
        fail(f"{path}: missing metadata properties: {missing}")

    schema_version = properties["schema_version"]

    if schema_version.get("type") != "string":
        fail(f"{path}: schema_version must be a string")

    if "const" in schema_version:
        version = schema_version["const"]
        parts = version.split(".")
        if len(parts) != 3 or not all(part.isdigit() for part in parts):
            fail(f"{path}: invalid schema version: {version}")

def validate_contract(path: Path) -> None:
    data = validate_json(path)

    if data.get("$schema") != (
        "https://json-schema.org/draft/2020-12/schema"
    ):
        fail(f"{path}: unsupported or invalid $schema")

    if not data.get("$id"):
        fail(f"{path}: missing $id")

    validate_common_metadata(path, data)

    print(f"PASS {path}")

def validate_identity_boundary() -> None:
    path = (
        CONTRACT_ROOT
        / "identity"
        / "identity-boundary.schema.json"
    )

    if not path.exists():
        fail("identity boundary contract is missing")

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
    files = sorted(CONTRACT_ROOT.glob("**/*.json"))

    if not files:
        fail("no contract schemas found")

    for path in files:
        validate_contract(path)

    validate_identity_boundary()

    print(f"CONTRACT_FILES={len(files)}")
    print("CONTRACT_VALIDATION=PASS")

    return 0

if __name__ == "__main__":
    sys.exit(main())
