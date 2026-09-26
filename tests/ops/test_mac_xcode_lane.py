from __future__ import annotations

import ops.lanes.mac_xcode_lane as lane


def _qualified(**overrides):
    values = {
        "platform": "Darwin",
        "architecture": "arm64",
        "xcrun": "/usr/bin/xcrun",
        "xcode_select": "/usr/bin/xcode-select",
        "xcode_version": "Xcode 16.2",
        "iphoneos_sdk": "/sdk/iPhoneOS.sdk",
        "iphonesimulator_sdk": "/sdk/iPhoneSimulator.sdk",
        "simctl": "/usr/bin/simctl",
        "booted_simulator": "06D1D93E-80A2-4F05-B797-D5D5E60FF7C5",
        "qualified": True,
        "reason": "QUALIFIED",
    }
    values.update(overrides)
    return lane.MacXcodeQualification(**values)


def test_qualify_requires_darwin(monkeypatch):
    monkeypatch.setattr(lane.platform, "system", lambda: "Linux")
    monkeypatch.setattr(lane.platform, "machine", lambda: "x86_64")

    result = lane.qualify()

    assert result.qualified is False
    assert result.reason == "NOT_MACOS"


def test_qualify_requires_apple_toolchain(monkeypatch):
    monkeypatch.setattr(lane.platform, "system", lambda: "Darwin")
    monkeypatch.setattr(lane.platform, "machine", lambda: "arm64")

    def which(binary):
        return {
            "xcrun": "/usr/bin/xcrun",
            "xcode-select": "/usr/bin/xcode-select",
            "xcodebuild": "/usr/bin/xcodebuild",
            "simctl": "/usr/bin/simctl",
        }.get(binary)

    monkeypatch.setattr(lane.shutil, "which", which)
    monkeypatch.setattr(
        lane,
        "_xcrun_path",
        lambda tool: "/Applications/Xcode.app/Contents/Developer/usr/bin/simctl"
        if tool == "simctl"
        else None,
    )
    monkeypatch.setattr(lane, "_booted_simulator", lambda: "06D1D93E-80A2-4F05-B797-D5D5E60FF7C5")
    monkeypatch.setattr(
        lane,
        "_version",
        lambda binary, args: "Xcode 16.2" if binary == "xcodebuild" else None,
    )
    monkeypatch.setattr(
        lane,
        "_sdk_path",
        lambda sdk: f"/sdk/{sdk}.sdk",
    )

    result = lane.qualify()

    assert result.qualified is True
    assert result.reason == "QUALIFIED"
    assert result.iphoneos_sdk == "/sdk/iphoneos.sdk"
    assert result.iphonesimulator_sdk == "/sdk/iphonesimulator.sdk"
    assert result.simctl == "/Applications/Xcode.app/Contents/Developer/usr/bin/simctl"


def test_missing_simulator_sdk_fails_closed(monkeypatch):
    monkeypatch.setattr(lane.platform, "system", lambda: "Darwin")
    monkeypatch.setattr(lane.platform, "machine", lambda: "arm64")

    def which(binary):
        return {
            "xcrun": "/usr/bin/xcrun",
            "xcode-select": "/usr/bin/xcode-select",
            "xcodebuild": "/usr/bin/xcodebuild",
            "simctl": "/usr/bin/simctl",
        }.get(binary)

    monkeypatch.setattr(lane.shutil, "which", which)
    monkeypatch.setattr(
        lane,
        "_version",
        lambda binary, args: "Xcode 16.2" if binary == "xcodebuild" else None,
    )
    monkeypatch.setattr(
        lane,
        "_sdk_path",
        lambda sdk: "/sdk/iphoneos.sdk" if sdk == "iphoneos" else None,
    )

    result = lane.qualify()

    assert result.qualified is False
    assert result.reason == "IPHONESIMULATOR_SDK_MISSING"


def test_manifest_contains_apple_capabilities(monkeypatch):
    monkeypatch.setattr(lane, "qualify", lambda: _qualified())

    manifest = lane.manifest()

    assert manifest["qualified"] is True
    assert set(manifest["capabilities"]) == {
        "ios_build",
        "ios_test",
        "ios_simulator",
        "macos_build",
        "macos_test",
        "xcodebuild",
        "xctest",
    }
    assert manifest["architecture"] == "arm64"
    assert manifest["booted_simulator"] == "06D1D93E-80A2-4F05-B797-D5D5E60FF7C5"
    assert manifest["schema_version"] == 3


def test_booted_simulator_extracts_udid(monkeypatch):
    class Result:
        returncode = 0
        stdout = """== Devices ==
    iPhone 16 Pro (06D1D93E-80A2-4F05-B797-D5D5E60FF7C5) (Booted)
    iPhone 16 (E79A97A3-8B25-4B96-AA48-6293EB8AA1F6) (Shutdown)
"""

    monkeypatch.setattr(lane, "_xcrun_path", lambda tool: "/usr/bin/simctl")
    monkeypatch.setattr(
        lane.subprocess,
        "run",
        lambda *args, **kwargs: Result(),
    )

    assert lane._booted_simulator() == "06D1D93E-80A2-4F05-B797-D5D5E60FF7C5"


def test_booted_simulator_returns_none_when_none_booted(monkeypatch):
    class Result:
        returncode = 0
        stdout = """== Devices ==
    iPhone 16 Pro (06D1D93E-80A2-4F05-B797-D5D5E60FF7C5) (Shutdown)
"""

    monkeypatch.setattr(lane, "_xcrun_path", lambda tool: "/usr/bin/simctl")
    monkeypatch.setattr(
        lane.subprocess,
        "run",
        lambda *args, **kwargs: Result(),
    )

    assert lane._booted_simulator() is None
