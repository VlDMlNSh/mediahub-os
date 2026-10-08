"""Deterministic development-intelligence primitives for Astra Gold.

This layer is advisory/compilation logic. It never owns claims, executor identity,
promotion, target-SHA authority, or qualification decisions.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
import hashlib
import re
from typing import Iterable


FAILURE_CLASSES = (
    "state_instruction",
    "production_code",
    "dependency",
    "build_toolchain",
    "environment",
    "platform_device",
    "test_infrastructure",
    "external_service",
    "unknown",
)

KNOWLEDGE_LEVELS = ("Confirmed", "Strong", "Project-only")
KNOWLEDGE_SCOPES = ("Universal", "Platform", "Framework/Tooling", "Project-specific")


@dataclass(frozen=True)
class ProjectProfile:
    project_type: str
    platform: str
    frameworks: tuple[str, ...]
    layers: tuple[str, ...]


@dataclass(frozen=True)
class RoadmapBlock:
    block_id: str
    title: str
    source_heading: str
    dependencies: tuple[str, ...]
    entry_conditions: tuple[str, ...]
    exit_conditions: tuple[str, ...]


def classify_project(specification: str) -> ProjectProfile:
    """Classify common project signals without making execution decisions."""
    text = specification.lower()
    platforms: list[str] = []
    frameworks: list[str] = []
    layers: list[str] = []
    project_type = "software"

    for needle, value in (
        ("flutter", "Flutter"),
        ("swiftui", "SwiftUI"),
        ("ios", "iOS"),
        ("android", "Android"),
        ("react", "React"),
        ("next.js", "Next.js"),
        ("nextjs", "Next.js"),
        ("django", "Django"),
        ("fastapi", "FastAPI"),
        ("desktop", "Desktop"),
        ("web", "Web"),
        ("mobile", "Mobile"),
    ):
        if needle in text:
            if value in {"Flutter", "SwiftUI", "React", "Next.js", "Django", "FastAPI"}:
                if value not in frameworks:
                    frameworks.append(value)
            elif value not in platforms:
                platforms.append(value)

    if any(x in text for x in ("mobile", "ios", "android", "flutter", "swiftui")):
        project_type = "mobile"
    elif any(x in text for x in ("web", "browser", "frontend", "backend")):
        project_type = "web"
    elif "desktop" in text or "macos" in text or "windows" in text or "linux" in text:
        project_type = "desktop"

    for layer, needles in {
        "frontend": ("frontend", "ui", "swiftui", "react", "web"),
        "backend": ("backend", "api", "server", "django", "fastapi"),
        "data": ("database", "postgres", "sqlite", "storage"),
        "testing": ("test", "validation", "regression"),
    }.items():
        if any(n in text for n in needles):
            layers.append(layer)

    return ProjectProfile(project_type, tuple(platforms), tuple(frameworks), tuple(layers))


def compile_roadmap_blocks(specification: str) -> list[RoadmapBlock]:
    """Compile explicit Markdown H1/H2 sections into stable logical blocks.

    This is deliberately conservative: it never invents hidden requirements.
    If no headings exist, one block is returned for the complete specification.
    """
    headings = re.findall(r"(?m)^#{1,2}\s+(.+?)\s*$", specification)
    titles = [h.strip() for h in headings if h.strip()]
    if not titles:
        titles = ["Project Specification"]
    blocks: list[RoadmapBlock] = []
    for index, title in enumerate(titles, 1):
        previous = (f"MD-{index - 1:03d}",) if index > 1 else ()
        blocks.append(
            RoadmapBlock(
                block_id=f"MD-{index:03d}",
                title=title,
                source_heading=title,
                dependencies=previous,
                entry_conditions=("previous block checkpoint satisfied",) if previous else ("specification received",),
                exit_conditions=(f"all units in MD-{index:03d} verified",),
            )
        )
    return blocks


def split_block_into_units(block_text: str, block_id: str) -> list[dict]:
    """Create conservative units from Markdown task/list boundaries."""
    lines = [line.strip() for line in block_text.splitlines() if line.strip()]
    candidates = [line for line in lines if re.match(r"^(?:[-*+] |\d+[.)] |UNIT\s+)", line, re.I)]
    if not candidates:
        candidates = [block_text.strip()] if block_text.strip() else []
    units = []
    for index, item in enumerate(candidates, 1):
        digest = hashlib.sha256(item.encode("utf-8")).hexdigest()[:12]
        units.append({
            "unit_id": f"{block_id}-U{index:03d}",
            "purpose": item.lstrip("-*+ ").strip(),
            "source_fingerprint": digest,
            "entry_conditions": [f"{block_id} checkpoint is available"],
            "validation_required": True,
            "recovery_required": True,
        })
    return units


def universal_first_action() -> tuple[str, ...]:
    return (
        "read authoritative state",
        "resolve latest confirmed project/file/unit checkpoint",
        "verify prerequisites and dependency state",
        "load only applicable confirmed failure knowledge",
        "verify target SHA and claim boundaries",
        "execute the bounded unit",
        "validate before checkpointing",
    )


def classify_failure(symptom: str, context: str = "") -> str:
    text = f"{symptom} {context}".lower()
    rules = (
        ("state_instruction", ("checkpoint", "state", "resume", "instruction", "wrong unit")),
        ("dependency", ("dependency", "package", "module not found", "lockfile")),
        ("build_toolchain", ("gradle", "xcodebuild", "compiler", "toolchain", "build failed")),
        ("platform_device", ("simulator", "device", "ios", "android", "windows", "macos")),
        ("test_infrastructure", ("pytest", "runner", "ci", "github actions", "test infrastructure")),
        ("external_service", ("github api", "network", "service unavailable", "timeout")),
        ("environment", ("permission denied", "environment variable", "path", "credential")),
        ("production_code", ("assertion", "exception", "logic bug", "regression")),
    )
    for category, needles in rules:
        if any(needle in text for needle in needles):
            return category
    return "unknown"


def validate_knowledge_entry(entry: dict) -> tuple[bool, list[str]]:
    required = (
        "ERROR_ID", "CATEGORY", "SYMPTOM", "ROOT_CAUSE", "CONFIRMED_FIX",
        "VALIDATION", "APPLICABILITY", "CONFIDENCE",
    )
    missing = [key for key in required if not str(entry.get(key, "")).strip()]
    if entry.get("CATEGORY") not in KNOWLEDGE_SCOPES:
        missing.append("CATEGORY(valid)")
    if entry.get("CONFIDENCE") not in KNOWLEDGE_LEVELS:
        missing.append("CONFIDENCE(valid)")
    if entry.get("CONFIRMED") is not True:
        missing.append("CONFIRMED=true")
    return (not missing, missing)


def capability_contract(task: dict) -> dict:
    """Normalize task capability metadata without changing Astra authority."""
    capabilities = sorted({str(x).strip() for x in task.get("required_capabilities", []) if str(x).strip()})
    roles = sorted({str(x).strip() for x in task.get("preferred_roles", []) if str(x).strip()})
    return {
        "required_capabilities": capabilities,
        "preferred_roles": roles,
        "verification": list(task.get("verification", [])),
        "evidence_required": bool(task.get("qualification", {}).get("evidence_required", True)),
        "commit_binding": bool(task.get("qualification", {}).get("commit_binding", True)),
    }


def checkpoint_record(level: str, project_sha: str, state: dict) -> dict:
    if level not in {"UNIT", "FILE", "PROJECT"}:
        raise ValueError("invalid_checkpoint_level")
    return {
        "schema": "mediahub.astra.checkpoint.v1",
        "level": level,
        "project_sha": project_sha,
        "state": state,
    }
