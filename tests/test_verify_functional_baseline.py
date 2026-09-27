import os
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "ops" / "verify_functional_baseline.sh"


def run_verifier(ref: str | None = None, head_ref: str | None = None) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env.pop("GITHUB_HEAD_REF", None)
    if ref is not None:
        env["GITHUB_SHA"] = ref
    if head_ref:
        env["GITHUB_HEAD_REF"] = head_ref
    return subprocess.run(
        ["bash", str(SCRIPT)],
        cwd=ROOT,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )


def git(*args: str, env=None, input_text: str | None = None) -> str:
    return subprocess.check_output(
        ["git", *args], cwd=ROOT, text=True, env=env, input=input_text
    ).strip()


def test_valid_descendant_passes() -> None:
    head_ref = os.environ.get("GITHUB_HEAD_REF")
    result = run_verifier(head_ref=head_ref) if head_ref else run_verifier(ref=git("rev-parse", "HEAD"))
    assert result.returncode == 0, result.stderr + result.stdout
    assert "FUNCTIONAL_BASELINE=PASS" in result.stdout


def test_non_ancestor_is_rejected() -> None:
    env = {
        **os.environ,
        "GIT_AUTHOR_NAME": "Astra Test",
        "GIT_AUTHOR_EMAIL": "astra-test@example.invalid",
        "GIT_COMMITTER_NAME": "Astra Test",
        "GIT_COMMITTER_EMAIL": "astra-test@example.invalid",
    }
    tree = git("mktree", env=env, input_text="")
    orphan = subprocess.check_output(
        ["git", "commit-tree", tree, "-m", "astra test orphan"],
        cwd=ROOT, text=True, env=env,
    ).strip()
    result = run_verifier(ref=orphan)
    assert result.returncode != 0


def test_missing_normative_invariant_is_rejected() -> None:
    index = ROOT / ".git" / "astra-test-index"
    env = {
        **os.environ,
        "GIT_INDEX_FILE": str(index),
        "GIT_AUTHOR_NAME": "Astra Test",
        "GIT_AUTHOR_EMAIL": "astra-test@example.invalid",
        "GIT_COMMITTER_NAME": "Astra Test",
        "GIT_COMMITTER_EMAIL": "astra-test@example.invalid",
    }
    try:
        subprocess.run(["git", "read-tree", "HEAD"], cwd=ROOT, env=env, check=True)
        original = subprocess.check_output(
            ["git", "show", "HEAD:specification/invariant-registry.yaml"],
            cwd=ROOT, text=True,
        )
        modified = "\n".join(
            line for line in original.splitlines()
            if "INV-036:" not in line
        ) + "\n"
        blob = subprocess.check_output(
            ["git", "hash-object", "-w", "--stdin"],
            cwd=ROOT, input=modified, text=True,
        ).strip()
        subprocess.run(
            [
                "git", "update-index", "--add", "--cacheinfo",
                f"100644,{blob},specification/invariant-registry.yaml",
            ],
            cwd=ROOT, env=env, check=True,
        )
        tree = git("write-tree", env=env)
        commit = subprocess.check_output(
            ["git", "commit-tree", tree, "-p", "HEAD", "-m", "astra test missing invariant"],
            cwd=ROOT, text=True, env=env,
        ).strip()
        result = run_verifier(ref=commit)
        assert result.returncode != 0
    finally:
        index.unlink(missing_ok=True)
