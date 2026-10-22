"""Structural/binding checks for a proposed source-change bundle.

This module deliberately does NOT verify signatures, issuer authenticity, capability
policy, revocation, replay, patch contents, or publication authority. It is not a
trusted publisher admission function. Callers must fail closed unless a separate,
accepted authority component supplies the expected context after authenticating the
signed command and evaluating capability/policy.
"""
from __future__ import annotations

import re
from typing import Any

SCHEMA_VERSION = "mediahub.astra.source-change-bundle.v1"
_HEX_SHA = re.compile(r"^(?:[0-9a-fA-F]{40}|[0-9a-fA-F]{64})$")
_HEX_SHA256 = re.compile(r"^[0-9a-fA-F]{64}$")
_SAFE_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$")


class BundleValidationError(ValueError):
    """Stable fail-closed error for a structurally invalid or unbound bundle."""


def _require(condition: bool, reason: str) -> None:
    if not condition:
        raise BundleValidationError(reason)


def _safe_repo_path(value: Any) -> bool:
    if not isinstance(value, str) or not value or len(value) > 1024:
        return False
    if value.startswith(("/", "\\")) or "\\" in value or "\x00" in value or ":" in value:
        return False
    parts = value.split("/")
    if any(part in ("", ".", "..") or part.lower() == ".git" for part in parts):
        return False
    return True


def validate_bundle_binding(
    bundle: dict[str, Any], *, expected: dict[str, Any], owned_paths: list[str]
) -> None:
    """Validate bundle shape and bind it to caller-supplied expected values.

    `expected` and `owned_paths` must come from a separately authenticated and
    authorized context. Passing model-controlled or environment-only values here
    does not establish trust. A successful return means *structurally bound only*.
    """
    _require(isinstance(bundle, dict), "bundle_not_object")
    allowed_fields = {"schema_version", "bundle_id", "task_id", "command_id", "node_id", "base_sha", "target_sha", "patch_sha256", "patch_size", "changed_paths", "authorization_context", "created_at", "state"}
    _require(set(bundle).issubset(allowed_fields), "unexpected_bundle_fields")
    _require(bundle.get("schema_version") == SCHEMA_VERSION, "schema_version_mismatch")
    _require(isinstance(bundle.get("bundle_id"), str) and bool(_SAFE_ID.fullmatch(bundle["bundle_id"])), "invalid_bundle_id")
    for field in ("task_id", "command_id", "node_id"):
        _require(isinstance(bundle.get(field), str) and bool(bundle[field]) and len(bundle[field]) <= 128, f"invalid_{field}")
        _require(bundle[field] == expected.get(field), f"{field}_mismatch")
    for field in ("base_sha", "target_sha"):
        _require(isinstance(bundle.get(field), str) and bool(_HEX_SHA.fullmatch(bundle[field])), f"invalid_{field}")
    _require(bundle["base_sha"] == expected.get("base_sha"), "base_sha_mismatch")
    _require(bundle["target_sha"] == expected.get("target_sha"), "target_sha_mismatch")
    _require(isinstance(bundle.get("patch_sha256"), str) and bool(_HEX_SHA256.fullmatch(bundle["patch_sha256"])), "invalid_patch_sha256")
    _require(type(bundle.get("patch_size")) is int and bundle["patch_size"] >= 0, "invalid_patch_size")
    _require(type(bundle.get("created_at")) is int and bundle["created_at"] >= 0, "invalid_created_at")
    _require(bundle.get("state") == "PROPOSED_UNVERIFIED", "bundle_must_remain_unverified")

    paths = bundle.get("changed_paths")
    _require(isinstance(paths, list) and bool(paths), "changed_paths_required")
    _require(all(_safe_repo_path(path) for path in paths), "unsafe_changed_path")
    _require(len(paths) == len(set(paths)), "duplicate_changed_path")
    _require(isinstance(owned_paths, list) and all(_safe_repo_path(path) for path in owned_paths), "invalid_authorized_path_context")
    _require(set(paths).issubset(set(owned_paths)), "changed_path_outside_owned_paths")

    auth = bundle.get("authorization_context")
    _require(isinstance(auth, dict), "authorization_context_required")
    auth_fields = {"issuer_id", "capability_id", "policy_sha256", "signed_command_sha256"}
    _require(set(auth) == auth_fields, "authorization_context_fields_mismatch")
    for field in ("issuer_id", "capability_id"):
        _require(isinstance(auth.get(field), str) and bool(auth[field]) and len(auth[field]) <= 128, f"invalid_authorization_{field}")
        _require(auth[field] == expected.get(field), f"authorization_{field}_mismatch")
    for field in ("policy_sha256", "signed_command_sha256"):
        _require(isinstance(auth.get(field), str) and bool(_HEX_SHA256.fullmatch(auth[field])), f"invalid_authorization_{field}")
        _require(auth[field] == expected.get(field), f"authorization_{field}_mismatch")
