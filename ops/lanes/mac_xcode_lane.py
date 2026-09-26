from __future__ import annotations

import json
import platform
import re
import shutil
import subprocess
from dataclasses import dataclass


@dataclass(frozen=True)
class MacXcodeQualification:
    platform: str
    architecture: str
    xcrun: str | None
    xcode_select: str | None
    xcode_version: str | None
    iphoneos_sdk: str | None
    iphonesimulator_sdk: str | None
    simctl: str | None
    booted_simulator: str | None
    qualified: bool
    reason: str


def _version(binary: str, args: list[str]) -> str | None:
    path = shutil.which(binary)
    if not path:
        return None
    try:
        result = subprocess.run(
            [path, *args],
            text=True,
            capture_output=True,
            timeout=10,
            check=False,
        )
    except (OSError, subprocess.SubprocessError):
        return None

    if result.returncode != 0:
        return None

    lines = (result.stdout or result.stderr).strip().splitlines()
    return lines[0][:200] if lines else None


def _xcrun_path(tool: str) -> str | None:
    xcrun = shutil.which("xcrun")
    if not xcrun:
        return None

    try:
        result = subprocess.run(
            [xcrun, "--find", tool],
            text=True,
            capture_output=True,
            timeout=10,
            check=False,
        )
    except (OSError, subprocess.SubprocessError):
        return None

    if result.returncode != 0:
        return None

    path = result.stdout.strip()
    return path or None


def _booted_simulator() -> str | None:
    simctl = _xcrun_path("simctl")
    if not simctl:
        return None

    try:
        result = subprocess.run(
            [simctl, "list", "devices", "booted"],
            text=True,
            capture_output=True,
            timeout=10,
            check=False,
        )
    except (OSError, subprocess.SubprocessError):
        return None

    if result.returncode != 0:
        return None

    for line in result.stdout.splitlines():
        match = re.search(
            r"\(([0-9A-Fa-f-]{36})\)\s+\(Booted\)$",
            line.strip(),
        )
        if match:
            return match.group(1)

    return None


def _sdk_path(sdk: str) -> str | None:
    xcrun = shutil.which("xcrun")
    if not xcrun:
        return None

    try:
        result = subprocess.run(
            [xcrun, "--sdk", sdk, "--show-sdk-path"],
            text=True,
            capture_output=True,
            timeout=10,
            check=False,
        )
    except (OSError, subprocess.SubprocessError):
        return None

    if result.returncode != 0:
        return None

    path = result.stdout.strip()
    return path or None


def qualify() -> MacXcodeQualification:
    system = platform.system()
    arch = platform.machine()
    xcrun = shutil.which("xcrun")
    xselect = shutil.which("xcode-select")
    xcode_version = _version("xcodebuild", ["-version"])
    simctl = _xcrun_path("simctl")
    booted_simulator = _booted_simulator() if simctl else None

    iphoneos_sdk = None
    iphonesimulator_sdk = None

    if system == "Darwin" and xcrun:
        iphoneos_sdk = _sdk_path("iphoneos")
        iphonesimulator_sdk = _sdk_path("iphonesimulator")

    if system != "Darwin":
        return MacXcodeQualification(
            system,
            arch,
            xcrun,
            xselect,
            xcode_version,
            iphoneos_sdk,
            iphonesimulator_sdk,
            simctl,
            booted_simulator,
            False,
            "NOT_MACOS",
        )

    if arch != "arm64":
        return MacXcodeQualification(
            system,
            arch,
            xcrun,
            xselect,
            xcode_version,
            iphoneos_sdk,
            iphonesimulator_sdk,
            simctl,
            booted_simulator,
            False,
            "UNSUPPORTED_ARCHITECTURE",
        )

    if not xcrun or not xselect:
        return MacXcodeQualification(
            system,
            arch,
            xcrun,
            xselect,
            xcode_version,
            iphoneos_sdk,
            iphonesimulator_sdk,
            simctl,
            booted_simulator,
            False,
            "XCODE_TOOLING_MISSING",
        )

    if not xcode_version:
        return MacXcodeQualification(
            system,
            arch,
            xcrun,
            xselect,
            xcode_version,
            iphoneos_sdk,
            iphonesimulator_sdk,
            simctl,
            booted_simulator,
            False,
            "XCODEBUILD_UNHEALTHY",
        )

    if not iphoneos_sdk:
        return MacXcodeQualification(
            system,
            arch,
            xcrun,
            xselect,
            xcode_version,
            iphoneos_sdk,
            iphonesimulator_sdk,
            simctl,
            booted_simulator,
            False,
            "IPHONEOS_SDK_MISSING",
        )

    if not iphonesimulator_sdk:
        return MacXcodeQualification(
            system,
            arch,
            xcrun,
            xselect,
            xcode_version,
            iphoneos_sdk,
            iphonesimulator_sdk,
            simctl,
            booted_simulator,
            False,
            "IPHONESIMULATOR_SDK_MISSING",
        )

    if not simctl:
        return MacXcodeQualification(
            system,
            arch,
            xcrun,
            xselect,
            xcode_version,
            iphoneos_sdk,
            iphonesimulator_sdk,
            simctl,
            booted_simulator,
            False,
            "SIMCTL_MISSING",
        )

    if not booted_simulator:
        return MacXcodeQualification(
            system,
            arch,
            xcrun,
            xselect,
            xcode_version,
            iphoneos_sdk,
            iphonesimulator_sdk,
            simctl,
            booted_simulator,
            False,
            "NO_BOOTED_SIMULATOR",
        )

    return MacXcodeQualification(
        system,
        arch,
        xcrun,
        xselect,
        xcode_version,
        iphoneos_sdk,
        iphonesimulator_sdk,
        simctl,
        booted_simulator,
        True,
        "QUALIFIED",
    )


def manifest() -> dict:
    q = qualify()

    capabilities = (
        [
            "ios_build",
            "ios_test",
            "ios_simulator",
            "macos_build",
            "macos_test",
            "xcodebuild",
            "xctest",
        ]
        if q.qualified
        else []
    )

    return {
        "schema_version": 3,
        "lane": "mac-xcode",
        "platform": q.platform,
        "architecture": q.architecture,
        "qualified": q.qualified,
        "reason": q.reason,
        "xcode_version": q.xcode_version,
        "iphoneos_sdk": q.iphoneos_sdk,
        "iphonesimulator_sdk": q.iphonesimulator_sdk,
        "simctl": q.simctl,
        "booted_simulator": q.booted_simulator,
        "capabilities": capabilities,
    }


if __name__ == "__main__":
    print(json.dumps(manifest(), indent=2, sort_keys=True))
