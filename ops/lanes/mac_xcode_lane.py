from __future__ import annotations
import json, platform, shutil, subprocess
from dataclasses import dataclass

@dataclass(frozen=True)
class MacXcodeQualification:
    platform: str
    architecture: str
    xcrun: str | None
    xcode_select: str | None
    xcode_version: str | None
    qualified: bool
    reason: str

def _version(binary: str, args: list[str]) -> str | None:
    path=shutil.which(binary)
    if not path: return None
    try:
        result=subprocess.run([path,*args],text=True,capture_output=True,timeout=10,check=False)
    except (OSError, subprocess.SubprocessError): return None
    if result.returncode != 0: return None
    lines=(result.stdout or result.stderr).strip().splitlines()
    return lines[0][:200] if lines else None

def qualify() -> MacXcodeQualification:
    system=platform.system(); arch=platform.machine(); xcrun=shutil.which("xcrun"); xselect=shutil.which("xcode-select"); version=_version("xcodebuild",["-version"])
    if system != "Darwin": return MacXcodeQualification(system,arch,xcrun,xselect,version,False,"NOT_MACOS")
    if not xcrun or not xselect: return MacXcodeQualification(system,arch,xcrun,xselect,version,False,"XCODE_TOOLING_MISSING")
    if not version: return MacXcodeQualification(system,arch,xcrun,xselect,version,False,"XCODEBUILD_UNHEALTHY")
    return MacXcodeQualification(system,arch,xcrun,xselect,version,True,"QUALIFIED")

def manifest() -> dict:
    q=qualify()
    return {"schema_version":1,"lane":"mac-xcode","platform":q.platform,"architecture":q.architecture,"qualified":q.qualified,"reason":q.reason,"capabilities":["ios_build","ios_test","macos_build","macos_test"] if q.qualified else []}

if __name__ == "__main__": print(json.dumps(manifest(),indent=2,sort_keys=True))
