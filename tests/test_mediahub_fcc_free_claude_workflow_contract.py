from pathlib import Path


WORKFLOW = Path(".github/workflows/mediahub-fcc-free-claude-worker.yml")


def test_fcc_worker_is_gated_and_github_hosted() -> None:
    source = WORKFLOW.read_text(encoding="utf-8")
    assert "workflow_dispatch:" in source
    assert "default: false" in source
    assert "inputs.confirm" in source
    assert "vars.MEDIAHUB_ALLOW_FCC_FREE_CLAUDE" in source
    assert "runs-on: ubuntu-latest" in source
    assert "self-hosted" not in source
    assert "permissions:" in source and "contents: read" in source


def test_fcc_and_free_model_route_are_immutable_and_explicit() -> None:
    source = WORKFLOW.read_text(encoding="utf-8")
    assert "3d2ae2306752dbdf504714a5489bcfcf69b2d04a" in source
    assert "open_router/openrouter/free" in source
    assert "uv sync --locked --no-dev" in source
    assert "MODEL_FALLBACKS" in source
    assert "unset ANTHROPIC_API_KEY MODEL_FALLBACKS" in source


def test_worker_never_maps_paid_anthropic_credential() -> None:
    source = WORKFLOW.read_text(encoding="utf-8")
    assert "secrets.ANTHROPIC_API_KEY" not in source
    assert "vars.MEDIAHUB_ALLOW_FCC_FREE_CLAUDE" in source
    assert "secrets.OPENROUTER_API_KEY" in source


def test_worker_requires_immutable_target_and_bounded_prompt() -> None:
    source = WORKFLOW.read_text(encoding="utf-8")
    assert '"$TARGET_SHA" =~ ^[0-9a-f]{40}$' in source
    assert 'TASK_PROMPT}" -le 12000' in source
    assert "git diff --check" in source
    assert "persist-credentials: false" in source
    assert "actions/upload-artifact@" in source


def test_first_live_smoke_is_read_only() -> None:
    source = WORKFLOW.read_text(encoding="utf-8")
    assert '--allowed-tools "Read,Glob,Grep"' in source
    assert '--allowed-tools "Read,Glob,Grep,Edit,Write"' not in source
    assert '--permission-mode plan' in source
    assert "Read-only MediaHub smoke worker." in source
