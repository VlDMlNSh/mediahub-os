#!/usr/bin/env python3

import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUILD = ROOT / "build"
ARTIFACT = BUILD / "foundation-manifest.json"

def run(command):
    result = subprocess.run(
        command,
        cwd=ROOT,
        text=True,
        capture_output=True,
    )

    if result.returncode != 0:
        print(result.stdout, end="")
        print(result.stderr, end="", file=sys.stderr)
        raise SystemExit(result.returncode)

    return result.stdout.strip()

def main():
    BUILD.mkdir(exist_ok=True)

    print("=== VALIDATION ===")
    run([sys.executable, "tools/validate_contracts.py"])

    print()
    print("=== UNIT TESTS ===")
    run([
        sys.executable,
        "-m",
        "unittest",
        "discover",
        "-s",
        "tests",
        "-p",
        "test_*.py",
    ])

    revision = run(["git", "rev-parse", "HEAD"])

    contracts = sorted(
        str(path.relative_to(ROOT))
        for path in ROOT.glob("contracts/**/*.json")
    )

    manifest = {
        "artifact_type": "mediahub.foundation.validation",
        "artifact_version": "1.0.0",
        "source_revision": revision,
        "target": {
            "platform": "linux",
            "architecture": run(["uname", "-m"]),
        },
        "toolchain": {
            "python": run([sys.executable, "--version"]),
        },
        "contracts": contracts,
        "validation": {
            "contract_validation": "PASS",
            "unit_tests": "PASS",
        },
        "runtime": "NOT_EXECUTED",
        "qualification": "NOT_QUALIFIED",
        "production": "NOT_GRANTED",
        "generated_at_utc": datetime.now(
            timezone.utc
        ).isoformat(),
    }

    raw = json.dumps(
        manifest,
        indent=2,
        sort_keys=True,
    ) + "\n"

    ARTIFACT.write_text(raw, encoding="utf-8")

    digest = hashlib.sha256(
        ARTIFACT.read_bytes()
    ).hexdigest()

    checksum = BUILD / "foundation-manifest.sha256"
    checksum.write_text(
        f"{digest}  {ARTIFACT.name}\n",
        encoding="utf-8",
    )

    print()
    print("=== BUILD ARTIFACT ===")
    print(f"ARTIFACT={ARTIFACT}")
    print(f"SHA256={digest}")
    print("BUILD_RESULT=PASS")

if __name__ == "__main__":
    main()
