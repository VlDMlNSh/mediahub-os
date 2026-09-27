import os
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LAUNCHER = ROOT / "ops" / "ai" / "godmode_openrouter_codex.sh"


def test_godmode_launcher_requires_openrouter_credential():
    env = os.environ.copy()
    env.pop("OPENROUTER_API_KEY", None)
    result = subprocess.run(
        [str(LAUNCHER)],
        cwd=ROOT,
        env=env,
        text=True,
        capture_output=True,
        timeout=5,
        check=False,
    )
    assert result.returncode != 0
    assert "OPENROUTER_API_KEY is required" in result.stderr
    assert "OPENROUTER_API_KEY=" not in result.stderr
    assert "OPENAI_API_KEY=" not in result.stderr


def test_godmode_launcher_pins_openrouter_endpoint():
    text = LAUNCHER.read_text(encoding="utf-8")
    assert 'OPENAI_BASE_URL="https://openrouter.ai/api/v1"' in text
    assert 'export OPENAI_API_KEY="$OPENROUTER_API_KEY"' in text
    assert 'exec codex "$@"' in text
