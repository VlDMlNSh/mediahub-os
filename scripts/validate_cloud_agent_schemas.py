#!/usr/bin/env python3
"""Deterministic Draft 2020-12 validation for the proposed cloud-agent v0.2 schemas.

All inputs are synthetic fixtures. This validates schema structure and JSON instances;
it does not admit an agent, authorize a provider call, or qualify a runtime.
"""
from __future__ import annotations

import copy
import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from importlib.metadata import version as package_version
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_DIR = ROOT / "docs" / "checkpoints"
FIXTURE_DIR = ROOT / "tests" / "fixtures" / "cloud-agent-schemas"
REPORT_PATH = ROOT / "artifacts" / "cloud-agent-schema-validation-report.json"

SCHEMAS = {
    "task-envelope": {
        "path": SCHEMA_DIR / "MEDIAHUB-CLOUD-AGENT-TASK-ENVELOPE-SCHEMA-V0.2-WAVE-16-2026-10-16.json",
        "fixture": "valid/task-envelope-v0.2.json",
        "blob_sha1": "6f3cd3d40b2c5fe3f21bb6085536769fbef8322a",
    },
    "agent-registry": {
        "path": SCHEMA_DIR / "MEDIAHUB-CLOUD-AGENT-REGISTRY-SCHEMA-V0.2-WAVE-16-2026-10-16.json",
        "fixture": "valid/agent-registry-v0.2.json",
        "blob_sha1": "b49b89b8fbdfc180862e3dc78f8198f35e486035",
    },
    "evidence-manifest": {
        "path": SCHEMA_DIR / "MEDIAHUB-CLOUD-AGENT-EVIDENCE-MANIFEST-SCHEMA-V0.2-WAVE-16-2026-10-16.json",
        "fixture": "valid/evidence-manifest-v0.2.json",
        "blob_sha1": "40c402432fd0f3899d45fde0fa0a8af4d34c593a",
    },
}


def git_blob_sha1(data: bytes) -> str:
    """Return the Git object SHA-1 for a blob, including Git's header."""
    header = b"blob " + str(len(data)).encode("ascii") + b"\0"
    return hashlib.sha1(header + data).hexdigest()


def current_commit() -> str | None:
    try:
        value = subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True, stderr=subprocess.DEVNULL
        ).strip()
        return value if len(value) == 40 else None
    except (OSError, subprocess.CalledProcessError):
        return None


def read_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def mutate(instance: Any, operation: dict[str, Any]) -> Any:
    """Apply a small, declarative mutation to a deep-copied JSON fixture."""
    result = copy.deepcopy(instance)
    path = operation["path"]
    if not path:
        raise ValueError(f"Negative case {operation.get('id')} has an empty path.")
    parent = result
    for part in path[:-1]:
        if isinstance(parent, dict) and part in parent:
            parent = parent[part]
        elif isinstance(parent, list) and isinstance(part, int) and 0 <= part < len(parent):
            parent = parent[part]
        else:
            raise KeyError(f"Path {path!r} does not exist in fixture.")
    key = path[-1]
    op = operation["op"]
    if op == "remove":
        if isinstance(parent, dict) and key in parent:
            del parent[key]
        elif isinstance(parent, list) and isinstance(key, int) and 0 <= key < len(parent):
            del parent[key]
        else:
            raise KeyError(f"Cannot remove absent path {path!r}.")
    elif op == "set":
        if isinstance(parent, dict):
            parent[key] = operation["value"]
        elif isinstance(parent, list) and isinstance(key, int) and 0 <= key < len(parent):
            parent[key] = operation["value"]
        else:
            raise TypeError(f"Parent of path {path!r} cannot accept the requested key.")
    else:
        raise ValueError(f"Unsupported mutation operation: {op}")
    return result


def nested_required_paths(schema: Any, instance: Any, prefix: tuple[Any, ...] = ()) -> list[tuple[Any, ...]]:
    """Enumerate required-property paths in concrete objects, including array items."""
    paths: list[tuple[Any, ...]] = []
    if isinstance(instance, list):
        item_schema = schema.get("items", {}) if isinstance(schema, dict) else {}
        for index, item in enumerate(instance):
            paths.extend(nested_required_paths(item_schema, item, prefix + (index,)))
        return paths
    if not isinstance(instance, dict) or not isinstance(schema, dict):
        return paths
    properties = schema.get("properties", {})
    for key in schema.get("required", []):
        if key in instance:
            paths.append(prefix + (key,))
    for key, child in properties.items():
        if key in instance and isinstance(child, dict):
            paths.extend(nested_required_paths(child, instance[key], prefix + (key,)))
    return paths


def error_summaries(errors: list[Any], limit: int = 3) -> list[dict[str, str]]:
    return [
        {
            "path": str(error.json_path),
            "message": str(error.message)[:400],
        }
        for error in errors[:limit]
    ]


def main() -> int:
    started = datetime.now(timezone.utc).isoformat()
    report: dict[str, Any] = {
        "report_schema": "mediahub.cloud-agent-schema-validation-report.v1",
        "status": "RUNNING",
        "started_at": started,
        "finished_at": None,
        "source": {
            "repository": "VlDMlNSh/mediahub-os",
            "commit_sha": current_commit(),
            "workflow_run_id": __import__("os").environ.get("GITHUB_RUN_ID"),
            "workflow_run_attempt": __import__("os").environ.get("GITHUB_RUN_ATTEMPT"),
            "schema_pins": {},
        },
        "validator": {},
        "counts": {
            "schemas_expected": len(SCHEMAS),
            "schemas_meta_validated": 0,
            "positive_fixtures_expected": len(SCHEMAS),
            "positive_fixtures_passed": 0,
            "negative_cases_expected": 0,
            "negative_cases_rejected": 0,
            "failures": 0,
        },
        "checks": [],
        "failures": [],
        "limitations": [
            "This validates JSON Schema Draft 2020-12 meta-schemas and synthetic instance fixtures only.",
            "It does not resolve issuer/grant/policy references, test runtime admission, call a provider, or qualify Contour A.",
            "The schema blobs are explicitly pinned; intentional schema changes require reviewed pin updates.",
        ],
    }

    try:
        import jsonschema
        report["validator"] = {
            "implementation": "python-jsonschema",
            "version": package_version("jsonschema"),
            "draft": "2020-12",
            "format_assertions": "FormatChecker enabled",
        }
        format_checker = FormatChecker()
        validators: dict[str, Draft202012Validator] = {}
        fixtures: dict[str, Any] = {}

        for name, spec in SCHEMAS.items():
            raw = spec["path"].read_bytes()
            observed_blob = git_blob_sha1(raw)
            raw_sha256 = hashlib.sha256(raw).hexdigest()
            pin_result = observed_blob == spec["blob_sha1"]
            report["source"]["schema_pins"][name] = {
                "path": str(spec["path"].relative_to(ROOT)),
                "expected_git_blob_sha1": spec["blob_sha1"],
                "observed_git_blob_sha1": observed_blob,
                "raw_file_sha256": f"sha256:{raw_sha256}",
                "pin_match": pin_result,
            }
            if not pin_result:
                report["failures"].append(
                    f"{name}: schema Git blob SHA differs from the reviewed v0.2 pin."
                )
            schema = json.loads(raw)
            if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
                report["failures"].append(f"{name}: $schema is not Draft 2020-12.")
            Draft202012Validator.check_schema(schema)
            report["counts"]["schemas_meta_validated"] += 1
            validators[name] = Draft202012Validator(schema, format_checker=format_checker)
            fixtures[name] = read_json(FIXTURE_DIR / spec["fixture"])
            positive_errors = sorted(
                validators[name].iter_errors(fixtures[name]),
                key=lambda error: (str(error.json_path), error.message),
            )
            check = {
                "kind": "positive_fixture",
                "id": spec["fixture"],
                "schema": name,
                "result": "PASS" if not positive_errors and pin_result else "FAIL",
                "errors": error_summaries(positive_errors),
            }
            report["checks"].append(check)
            if not positive_errors and pin_result:
                report["counts"]["positive_fixtures_passed"] += 1
            elif positive_errors:
                report["failures"].append(
                    f"{name}: positive fixture is invalid: {error_summaries(positive_errors)}"
                )

        negative_cases = read_json(FIXTURE_DIR / "negative-cases.json")
        if not isinstance(negative_cases, list) or not negative_cases:
            raise ValueError("negative-cases.json must be a non-empty array.")
        report["counts"]["negative_cases_expected"] = len(negative_cases)
        seen_ids: set[str] = set()
        for case in negative_cases:
            case_id = str(case.get("id", ""))
            schema_name = case.get("schema")
            fixture_name = case.get("fixture")
            if not case_id or case_id in seen_ids:
                report["failures"].append(f"Negative case has missing/duplicate id: {case_id!r}")
                continue
            seen_ids.add(case_id)
            if schema_name not in validators:
                report["failures"].append(f"{case_id}: unknown schema.")
                continue
            expected_fixture_name = Path(SCHEMAS[schema_name]["fixture"]).name
            if fixture_name != expected_fixture_name:
                report["failures"].append(f"{case_id}: mismatched base fixture; expected {expected_fixture_name}.")
                continue
            candidate = mutate(fixtures[schema_name], case)
            errors = sorted(
                validators[schema_name].iter_errors(candidate),
                key=lambda error: (str(error.json_path), error.message),
            )
            rejected = bool(errors)
            report["checks"].append({
                "kind": "negative_fixture_mutation",
                "id": case_id,
                "schema": schema_name,
                "result": "PASS" if rejected else "FAIL",
                "mutation": {"op": case["op"], "path": case["path"]},
                "errors": error_summaries(errors),
            })
            if rejected:
                report["counts"]["negative_cases_rejected"] += 1
            else:
                report["failures"].append(
                    f"{case_id}: intentionally invalid instance unexpectedly passed validation."
                )

        # Independently synthesize a missing-required negative for every required
        # property present in the fixture. This traversal includes object-valued
        # array items and records concrete numeric indices in mutation paths.
        generated_count = 0
        for schema_name, spec in SCHEMAS.items():
            schema = read_json(spec["path"])
            fixture = fixtures[schema_name]
            for path in nested_required_paths(schema, fixture):
                generated_count += 1
                generated_id = f"generated-required-{schema_name}-{generated_count:04d}"
                candidate = mutate(fixture, {"id": generated_id, "op": "remove", "path": list(path)})
                errors = sorted(
                    validators[schema_name].iter_errors(candidate),
                    key=lambda error: (str(error.json_path), error.message),
                )
                rejected = bool(errors)
                report["checks"].append({
                    "kind": "generated_nested_required_negative",
                    "id": generated_id,
                    "schema": schema_name,
                    "result": "PASS" if rejected else "FAIL",
                    "mutation": {"op": "remove", "path": list(path)},
                    "errors": error_summaries(errors),
                })
                if rejected:
                    report["counts"]["negative_cases_rejected"] += 1
                else:
                    report["failures"].append(
                        f"{generated_id}: missing-required mutation unexpectedly passed validation."
                    )
        report["counts"]["generated_required_cases"] = generated_count
        report["counts"]["negative_cases_expected"] += generated_count

    except Exception as exc:  # preserve report evidence for parse/meta-validation/runtime errors
        report["failures"].append(f"validator_exception: {type(exc).__name__}: {str(exc)[:1000]}")

    report["counts"]["failures"] = len(report["failures"])
    report["status"] = "PASS" if not report["failures"] else "FAIL"
    report["finished_at"] = datetime.now(timezone.utc).isoformat()
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
