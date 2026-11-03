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
    assert '"model":"openrouter/free"' in source
    assert 'export MODEL="open_router/${MODEL_ID}"' in source
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
    assert "persist-credentials: false" in source
    assert "  ecc-profile-preflight:" in source
    assert "ref: c05b2d6614f62f6db0047669aa4eefb223d478f9" in source
    assert "Pinned ECC commit, MIT license blob, and three selected skill blobs verified." in source
    assert "actions/upload-artifact@" in source


def test_provider_probe_is_a_sibling_workflow_step() -> None:
    lines = WORKFLOW.read_text(encoding="utf-8").splitlines()
    probe = "      - name: Probe OpenRouter free router and record selected model"
    assert lines.count(probe) == 1
    assert "            - name: Probe OpenRouter free router and record selected model" not in "\n".join(lines)


def test_first_live_smoke_is_read_only() -> None:
    source = WORKFLOW.read_text(encoding="utf-8")
    assert '--allowed-tools "Read,Glob,Grep"' in source
    assert '--permission-mode plan' in source
    assert 'cd "$RUNNER_TEMP/fcc-empty-workspace"' in source
    assert 'export HOME="$RUNNER_TEMP/fcc-home"' in source
    assert 'export XDG_CONFIG_HOME="$RUNNER_TEMP/fcc-xdg-config"' in source
    assert 'https://openrouter.ai/api/v1/chat/completions' in source
    assert 'endswith(":free")' in source
    assert 'request_id=%s' in source
    assert 'mediahub-claude.patch' not in source
    assert 'git diff --binary' not in source



def test_proxy_token_is_seeded_into_fcc_managed_config_and_auth_failure_is_clear() -> None:
    source = WORKFLOW.read_text(encoding="utf-8")
    assert 'export FCC_ENV_FILE="$RUNNER_TEMP/fcc-runtime.env"' in source
    assert "printf 'ANTHROPIC_AUTH_TOKEN=%s\\n' \"$ANTHROPIC_AUTH_TOKEN\" > \"$FCC_ENV_FILE\"" in source
    assert 'chmod 600 "$FCC_ENV_FILE"' in source
    assert "managed-config loader intentionally does not apply this" in source
    assert "rejected the run-scoped bearer token (HTTP 401)" in source
    assert 'final HTTP status ${status}; server logs withheld.' in source


def test_managed_config_preflight_checks_effective_token_without_provider_access() -> None:
    source = WORKFLOW.read_text(encoding="utf-8")
    assert "  managed-config-preflight:" in source
    assert "FCC managed auth config preflight" in source
    assert "uv run --locked python - <<" in source
    assert "settings.proxy_auth_enabled is True" in source
    assert 'settings.proxy_auth_token, os.environ["ANTHROPIC_AUTH_TOKEN"]' in source
    assert 'stat.S_IMODE(managed.stat().st_mode) == 0o600' in source
    assert "FCC managed bearer-token preflight passed; token values withheld." in source
    assert "openrouter.ai/api/v1/chat/completions" in source


def test_fcc_admission_controller_is_owner_gated_and_target_sha_bound() -> None:
    source = WORKFLOW.read_text(encoding="utf-8")
    assert "      target_sha:" in source
    assert "TARGET_SHA: ${{ inputs.target_sha }}" in source
    assert 'SOURCE_REF" == "refs/heads/main"' in source
    assert 'TRIGGER_ACTOR" == "$REPO_OWNER"' in source
    assert 'TARGET_SHA" == "$CURRENT_SHA"' in source
    assert "@anthropic-ai/claude-code@2.1.282" in source
    assert "target_sha=%s" in source


def test_ai_router_admits_only_explicit_cloud_controllers_and_keeps_no_paid_fallback() -> None:
    router = Path(".github/ai/model-router.yml").read_text(encoding="utf-8")
    assert "direct_provider_api_calls: false" in router
    assert "permitted_cloud_agent_transports:" in router
    assert "  - .github/workflows/gemini-batch-dispatch-controller.yml" in router
    assert "  - .github/workflows/mediahub-fcc-free-claude-worker.yml" in router
    assert "paid_fallback: false" in router
    assert "unknown_route_behavior: fail_closed" in router

def test_cloud_fcc_uses_pinned_selective_ecc_guidance_without_hooks_or_mcp() -> None:
    source = WORKFLOW.read_text(encoding="utf-8")
    assert "repository: affaan-m/ECC" in source
    assert "ref: c05b2d6614f62f6db0047669aa4eefb223d478f9" in source
    assert "git -C ecc rev-parse HEAD:LICENSE" in source
    assert "git -C ecc rev-parse HEAD:skills/verification-loop/SKILL.md" in source
    assert "git -C ecc rev-parse HEAD:skills/security-review/SKILL.md" in source
    assert "git -C ecc rev-parse HEAD:skills/search-first/SKILL.md" in source
    assert "hooks_enabled=false" in source
    assert "mcp_servers_enabled=false" in source
    assert "independent_controller=false" in source
    assert 'ECC_GUIDANCE="$(cat "$RUNNER_TEMP/ecc-profile/guidance.md")"' in source
    assert "ecc-profile-metadata.txt" in source
    assert "persist-credentials: false" in source


def test_router_separates_cloud_free_claude_and_local_ollama_llama() -> None:
    router = Path(".github/ai/model-router.yml").read_text(encoding="utf-8")
    assert "cloud_claude_runtime: fcc_openrouter_free" in router
    assert "cloud_claude_free_only: true" in router
    assert "local_claude_runtime: fcc_ollama" in router
    assert "local_claude_model: llama3.2:3b" in router
    assert "local_claude_host: Voktors-Mini.Dlink" in router
    assert "local_claude_only: true" in router
    assert "permitted_cloud_agent_transport_allowlist_only: true" in router

def test_cloud_claude_task_profiles_are_fixed_and_ruflo_is_pinned_read_only() -> None:
    source = WORKFLOW.read_text(encoding="utf-8")
    for required in (
        "task_profile:",
        "options: [connectivity_smoke, ruflo_static_review]",
        "TASK_PROFILE: ${{ inputs.task_profile }}",
        '[[ "$TASK_PROFILE" == "connectivity_smoke" || "$TASK_PROFILE" == "ruflo_static_review" ]]',
        "arbitrary task input",
        "repository: ruvnet/ruflo",
        "ref: f6c6a32432e74e36c17b91b96e51ba218783e122",
        'git -C ruflo-source rev-parse HEAD:LICENSE',
        'git -C ruflo-source rev-parse HEAD:package.json',
        'git -C ruflo-source rev-parse HEAD:SECURITY.md',
        "chmod -R a-w ruflo-source",
        '--allowed-tools "Read,Glob,Grep"',
        '--disallowed-tools "Bash,WebFetch,WebSearch,NotebookEdit"',
        "Do not install or execute Ruflo",
        "RUNTIME_EXECUTION: NOT RUN",
        "review profile not selected",
        "ruflo-review-result.txt",
    ):
        assert required in source, f"Missing bounded Ruflo task contract: {required}"


def test_ruflo_review_profile_remains_source_only_and_does_not_install_hooks_or_mcp() -> None:
    source = WORKFLOW.read_text(encoding="utf-8")
    assert "persist-credentials: false" in source
    assert "execution=source-only-read-only-no-install-no-hooks-no-mcp" in source
    assert "hooks_enabled=false" in source
    assert "mcp_servers_enabled=false" in source
    assert "independent_controller=false" in source
    assert "Astra remains the sole control plane" in source
