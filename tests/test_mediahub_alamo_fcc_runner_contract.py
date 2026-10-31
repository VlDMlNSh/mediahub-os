from pathlib import Path


WORKFLOW = Path(".github/workflows/mediahub-alamo-fcc-claude-runner.yml")


def test_runner_is_owner_gated_and_target_sha_bound() -> None:
    source = WORKFLOW.read_text(encoding="utf-8")
    assert "workflow_dispatch:" in source
    assert "default: false" in source
    assert 'SOURCE_REF" == "refs/heads/main"' in source
    assert 'TRIGGER_ACTOR" == "$REPO_OWNER"' in source
    assert 'TARGET_SHA" == "$CURRENT_SHA"' in source
    assert "runs-on: ubuntu-latest" in source
    assert "permissions: {}" in source


def test_local_model_runtime_is_pinned_and_loopback_only() -> None:
    source = WORKFLOW.read_text(encoding="utf-8")
    assert "OLLAMA_VERSION=0.40.11" in source
    assert "25f64b810b947145095956533e1bdf56eacea2673c55a7e586be4515fc882c9f" in source
    assert "OLLAMA_HOST=127.0.0.1:11434" in source
    assert "llama3.2:3b" in source
    assert "OLLAMA_BASE_URL: http://127.0.0.1:11434" in source
    assert "alamo_equivalence=NOT_VERIFIED" in source


def test_fcc_and_claude_are_pinned_and_no_cloud_credentials_used() -> None:
    source = WORKFLOW.read_text(encoding="utf-8")
    assert "3d2ae2306752dbdf504714a5489bcfcf69b2d04a" in source
    assert "@anthropic-ai/claude-code@2.1.282" in source
    assert "unset OPENROUTER_API_KEY ANTHROPIC_API_KEY MODEL_FALLBACKS" in source
    assert "secrets.OPENROUTER_API_KEY" not in source
    assert "secrets.ANTHROPIC_API_KEY" not in source
    assert "paid_fallback=false" in source


def test_fcc_auth_is_required_and_negative_case_checked() -> None:
    source = WORKFLOW.read_text(encoding="utf-8")
    assert "PROXY_AUTH_ENABLED=true" in source
    assert "ANTHROPIC_AUTH_TOKEN=" in source
    assert 'unauth_status" == "401"' in source
    assert 'Authorization: Bearer ${ANTHROPIC_AUTH_TOKEN}' in source


def test_claude_code_smoke_is_bounded_and_evidence_is_uploaded() -> None:
    source = WORKFLOW.read_text(encoding="utf-8")
    assert "fcc-claude" in source
    assert "--permission-mode plan" in source
    assert '--allowed-tools "Read,Glob,Grep"' in source
    assert '--disallowed-tools "Bash,WebFetch,WebSearch,NotebookEdit"' in source
    assert "fcc-empty-workspace" in source
    assert "actions/upload-artifact@" in source
    assert "target_sha=$GITHUB_SHA" in source


def test_pr_checks_are_green_without_running_live_install_or_model_calls() -> None:
    source = WORKFLOW.read_text(encoding="utf-8")
    assert "  dispatch-gate:\n    if:" not in source
    assert "github.event_name == 'pull_request' || (github.event_name == 'workflow_dispatch'" in source
    assert "PR validation only; live runner dispatch is not authorized" in source
    assert "Record that live execution is intentionally not run on pull requests" in source
    assert source.count("if: github.event_name == 'workflow_dispatch'") >= 7
    assert "if: always() && github.event_name == 'workflow_dispatch'" in source


def test_pinned_agent_toolchain_is_installed_without_provider_credentials() -> None:
    source = WORKFLOW.read_text(encoding="utf-8")
    assert "Install pinned agent toolchain (no provider authentication)" in source
    assert 'GEMINI_CLI_VERSION: "0.66.0"' in source
    assert 'MINI_SWE_AGENT_VERSION: "2.4.6"' in source
    assert 'AIDER_VERSION: "0.86.0"' in source
    assert 'OPENHANDS_SDK_VERSION: "1.59.0"' in source
    assert 'GOOSE_VERSION: "1.57.0"' in source
    assert "openhands-sdk==${OPENHANDS_SDK_VERSION}" in source
    assert "from openhands.sdk import Agent, Conversation, LLM" in source
    assert "goose-x86_64-unknown-linux-gnu.tar.gz" in source
    assert "10eb96cb6a159b6e1d38eeedbef6ab64cd28168aad91948f1fa5c34eefdf98e3" in source
    assert "provider_authentication=NOT_CONFIGURED" in source
    assert "agent_model_invocations=NOT_RUN" in source
    assert "agent-toolchain/" in source
    assert "GEMINI_API_KEY" not in source
    assert "ANTHROPIC_API_KEY" not in source
