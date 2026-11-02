from pathlib import Path


WORKFLOW = Path(".github/workflows/mediahub-ollama-fcc-claude-runner.yml")


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
    assert "ollama_runtime_qualification=NOT_VERIFIED" in source


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


def test_cloud_agent_toolchain_is_not_installed_on_ollama_runner() -> None:
    source = WORKFLOW.read_text(encoding="utf-8")
    forbidden = (
        "gemini-cli",
        "GEMINI_CLI_VERSION",
        "mini-swe-agent",
        "aider-chat",
        "openhands-sdk",
        "goose-linux-x86_64",
        "agent-toolchain/",
    )
    for marker in forbidden:
        assert marker not in source, f"VM 1 must not provision VM 2 tool: {marker}"


def test_old_runtime_alias_is_not_reintroduced() -> None:
    """Keep Ollama as the sole runtime name; host and model identities stay separate."""
    source = WORKFLOW.read_text(encoding="utf-8").lower()
    legacy_alias = "ala" + "mo"
    assert legacy_alias not in source
    assert "ollama-local-fcc-claude:" in source
    assert "mediahub-ollama-fcc-claude-" in source



def test_selective_ecc_profile_is_pinned_and_guidance_only() -> None:
    source = WORKFLOW.read_text(encoding="utf-8")
    assert "repository: affaan-m/ECC" in source
    assert "c05b2d6614f62f6db0047669aa4eefb223d478f9" in source
    assert "b832b6f642312312367c07688dc7426db40a82ed" in source
    assert "d7eb1fa239fd8c0ba8ae2d31a3c34d1f01741ef9" in source
    assert "3f26b0df65661425de4e5c40c295e04edcad7a83" in source
    assert "3d2669e71ba54afba95defb05080253058190600" in source
    assert 'cat ecc/skills/verification-loop/SKILL.md ecc/skills/security-review/SKILL.md ecc/skills/search-first/SKILL.md' in source
    assert "ecc-profile-metadata.txt" in source
    assert "hooks_installed=false" in source
    assert "mcps_installed=false" in source
    assert "controller_installed=false" in source
    assert "ECC is guidance only and grants no authority." in source


def test_fcc_env_file_uses_a_real_line_terminator() -> None:
    source = WORKFLOW.read_text(encoding="utf-8")
    expected = r"""printf 'ANTHROPIC_AUTH_TOKEN=%s\n' "$ANTHROPIC_AUTH_TOKEN" > "$FCC_ENV_FILE"""
    escaped_newline = r"""printf 'ANTHROPIC_AUTH_TOKEN=%s\\n'"""
    assert expected in source
    assert escaped_newline not in source


def test_fcc_runtime_token_file_is_ephemeral_and_private() -> None:
    source = WORKFLOW.read_text(encoding="utf-8")
    assert 'export FCC_ENV_FILE="$RUNNER_TEMP/fcc-runtime.env"' in source
    assert "umask 077" in source
    assert 'chmod 600 "$FCC_ENV_FILE"' in source
    assert "unset OPENROUTER_API_KEY ANTHROPIC_API_KEY MODEL_FALLBACKS" in source
