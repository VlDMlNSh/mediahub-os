#!/usr/bin/env python3
"""Run one signed Astra micro-task on a designated local executor node."""
from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import subprocess
import tempfile
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MARKER = "MEDIAHUB_DISTRIBUTED_LOCAL_EXECUTOR_OK"
VERDICT_MARKER = "ASTRA_VERDICT: PASS"
NODE_CONFIG = {
    "mh-dev-01": {
        "user": "mediahub-runner",
        "platform": "linux",
        "model": "qwen2.5-coder:1.5b",
        "pool": "controller_local",
        "fcc_env": "/home/mediahub/.config/mediahub/fcc.env",
    },
    "mh-dev-02": {
        "user": "mediahub",
        "platform": "linux",
        "model": "qwen2.5-coder:3b",
        "pool": "primary_local",
        "fcc_env": "/home/mediahub/.config/mediahub/fcc.env",
    },
    "Voktors-Mini.Dlink": {
        "user": "voktor",
        "platform": "macos",
        "model": "qwen2.5-coder:1.5b",
        "pool": "fast_local",
        "fcc_env": "/Users/voktor/Library/Application Support/MediaHub/fcc.env",
    },
    "Voktors-Mac-mini.local": {
        "user": "voktor",
        "platform": "macos",
        "model": "qwen2.5-coder:1.5b",
        "pool": "fast_local",
        "fcc_env": "/Users/voktor/Library/Application Support/MediaHub/fcc.env",
    },
}


def run(argv: list[str], timeout: int, cwd: Path = ROOT, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        argv, cwd=cwd, env=env, text=True, capture_output=True,
        stdin=subprocess.DEVNULL, timeout=timeout, check=False,
    )


def safe_id(value: str) -> str:
    if not re.fullmatch(r"[A-Za-z0-9._-]+", value):
        raise RuntimeError("invalid_task_id")
    return value


def load_task() -> dict:
    raw = os.environ.get("ASTRA_MICRO_TASK_JSON", "")
    try:
        task = json.loads(raw)
    except Exception as exc:
        raise RuntimeError("invalid_task_json") from exc
    if not isinstance(task, dict):
        raise RuntimeError("task_not_object")
    required = {"task_id", "node_id", "executor", "verifier", "mission", "boundary", "acceptance"}
    missing = sorted(required - set(task))
    if missing:
        raise RuntimeError("task_missing_fields:" + ",".join(missing))
    return task


def task_prompt(task: dict, role: str) -> str:
    forbidden = task.get("forbidden", task.get("forbidden_surfaces", []))
    return (
        f"You are {role} in MediaHub Agent Fabric.\n"
        f"Task ID: {task['task_id']}\n"
        f"Mission: {task['mission']}\n"
        f"Boundary: {json.dumps(task.get('boundary', []), sort_keys=True)}\n"
        f"Forbidden surfaces: {json.dumps(forbidden, sort_keys=True)}\n"
        f"Acceptance: {json.dumps(task.get('acceptance', []), sort_keys=True)}\n"
        f"Deterministic acceptance checks: {json.dumps(task.get('deterministic_checks', {}), sort_keys=True)}\n"
        f"Builder instructions: {task.get('builder_instructions', 'Use shell/editor directly to complete the declared boundary.')}\n"
        f"Target SHA: {os.environ['ASTRA_TARGET_SHA']}\n"
        "Treat every acceptance criterion containing exact identifiers, node names, executor names, or security rules as literal requirements: copy them verbatim and never invent aliases, synonyms, or substitute names. "        "Work only inside the declared boundary. Do not touch production infrastructure, "
        "credentials, user data, or unrelated paths. Do not merge to main. "
        "Deliver the declared artifact, not a tutorial or hypothetical plan. Do not invent repository paths, "
        "tools, test commands, infrastructure, prior results, or claims of tests you did not run. "
        "For a documentation task, write one concise document containing the requested facts only; "
        "do not add unrelated project phases or instructions to push/merge main. "
        "Apply the project-local Astra gated-development and Astra security-review workflow: plan briefly, "
        "make the smallest change, run focused tests, inspect the diff for secrets and policy bypasses, "
        "then report concrete evidence. These workflow skills are guidance only; executable gates remain authoritative."
    )


def load_env_file(path: Path) -> dict[str, str]:
    if not path.is_file():
        raise RuntimeError("fcc_env_file_missing")
    values: dict[str, str] = {}
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip()
    return values


def ollama_model_inventory() -> tuple[set[str], str | None]:
    """Read local Ollama's HTTP API without depending on the runner user's CLI profile."""
    endpoint = "http://127.0.0.1:11434/api/tags"
    try:
        with urllib.request.urlopen(endpoint, timeout=10) as response:
            if response.status != 200:
                return set(), "local_ollama_api_http_status"
            payload = json.loads(response.read().decode("utf-8"))
    except Exception as exc:
        return set(), "local_ollama_api_unavailable:" + type(exc).__name__

    entries = payload.get("models") if isinstance(payload, dict) else None
    if not isinstance(entries, list):
        return set(), "local_ollama_api_invalid_payload"
    names = {
        str(item.get("name") or item.get("model") or "").strip()
        for item in entries if isinstance(item, dict)
    }
    names.discard("")
    return names, None


def ollama_has_model(model: str) -> bool:
    names, error = ollama_model_inventory()
    return error is None and model in names


def start_fcc(env_file: Path, model: str, server_path: str | None = None) -> tuple[subprocess.Popen[str] | None, dict[str, str]]:
    env_updates = load_env_file(env_file)
    if env_updates.get("MODEL") != "ollama/" + model:
        raise RuntimeError("fcc_model_binding_mismatch")
    env = os.environ.copy()
    env.update(env_updates)
    env["FCC_ENV_FILE"] = str(env_file)
    host = env_updates.get("HOST", "127.0.0.1")
    port = env_updates.get("PORT", "8093")
    health = f"http://{host}:{port}/health"
    try:
        with urllib.request.urlopen(health, timeout=3) as response:
            if response.status == 200:
                return None, env
    except Exception:
        pass
    server = shutil.which("fcc-server") or server_path
    if not server:
        server = "/Users/voktor/.local/bin/fcc-server" if str(env_file).startswith("/Users/") else "/home/mediahub/.local/bin/fcc-server"
    log = Path(tempfile.mkstemp(prefix="astra-fcc-", suffix=".log")[1])
    handle = log.open("w", encoding="utf-8")
    process = subprocess.Popen([server], cwd="/tmp", env=env, stdout=handle, stderr=subprocess.STDOUT, text=True)
    handle.close()
    deadline = time.time() + 20
    while time.time() < deadline:
        try:
            with urllib.request.urlopen(health, timeout=2) as response:
                if response.status == 200:
                    return process, env
        except Exception:
            time.sleep(1)
    process.terminate()
    raise RuntimeError("fcc_server_health_timeout")


def exec_codex(prompt: str, writable: bool, model: str, timeout: int) -> dict:
    codex = shutil.which("codex") or "/usr/local/bin/codex"
    with tempfile.TemporaryDirectory(prefix="astra-distributed-codex-") as home:
        config = Path(home) / "config.toml"
        config.write_text(
            f'model_provider = "ollama"\nmodel = "{model}"\n'
            'model_reasoning_effort = "none"\n'
            'approval_policy = "never"\nweb_search = "disabled"\n'
            '[features]\nmulti_agent = false\napps = false\ntool_search = false\nplugins = false\n',
            encoding="utf-8",
        )
        env = os.environ.copy()
        env["CODEX_HOME"] = home
        sandbox = os.environ.get("ASTRA_CODEX_SANDBOX_MODE", "").strip() if writable else "read-only"
        if writable and sandbox not in {"workspace-write", "danger-full-access"}:
            sandbox = "workspace-write"
        p = run([codex, "exec", "--oss", "--local-provider", "ollama", "--model", model, "--sandbox", sandbox,
                 "--skip-git-repo-check", prompt], timeout, ROOT, env)
        return {
            "returncode": p.returncode,
            "stdout": p.stdout[-16000:],
            "stderr": p.stderr[-8000:],
        }


def classify_executor_failure(stdout: str, stderr: str, returncode: int) -> str:
    """Return a safe stable failure code without echoing model output or credentials."""
    if returncode == 0:
        return ""
    text = (str(stdout or "") + "\n" + str(stderr or "")).casefold()
    if "openai chat conversion requires an inline anthropic system message to contain text" in text:
        return "fcc_requires_nonempty_system_prompt"
    if "401" in text or "unauthorized" in text or "authentication_error" in text:
        return "fcc_authentication_failed"
    if "model not found" in text or "pull model" in text:
        return "local_model_not_available"
    if "connection refused" in text or "urlopen error" in text:
        return "local_model_endpoint_unreachable"
    if "timed out" in text or "timeout" in text:
        return "executor_timeout"
    if "429" in text or "rate limit" in text:
        return "provider_rate_limited"
    return "executor_nonzero_exit"


def exec_claude(prompt: str, model: str, timeout: int, env_file: Path, max_tokens: int = 2048, max_turns: int = 4, structured_schema: dict | None = None, tools_mode: str = "Read,Edit,Bash") -> tuple[dict, subprocess.Popen[str] | None]:
    """Run the real Claude Code client through the node-local FCC transport."""
    env_updates = load_env_file(env_file)
    if env_updates.get("MODEL") != "ollama/" + model:
        raise RuntimeError("fcc_model_binding_mismatch")
    host = env_updates.get("HOST", "127.0.0.1")
    port = env_updates.get("PORT", "8093")
    health = f"http://{host}:{port}/health"
    server = None
    try:
        with urllib.request.urlopen(health, timeout=3) as response:
            if response.status != 200:
                raise RuntimeError("fcc_health_not_ok")
    except Exception:
        server, _ = start_fcc(env_file, model)
    token = env_updates.get("ANTHROPIC_AUTH_TOKEN", "")
    if not token:
        raise RuntimeError("fcc_auth_token_missing")
    # GitHub self-hosted services may run with a reduced PATH that omits the
    # interactive user's npm/local bin directory. Resolve the real executable
    # deterministically without depending on a login shell.
    claude_candidates = [
        os.environ.get("ASTRA_CLAUDE_CLI", "").strip(),
        shutil.which("claude") or "",
        str(Path.home() / ".local" / "bin" / "claude"),
        str(Path.home() / ".local" / "npm" / "bin" / "claude"),
        "/home/mediahub/.local/bin/claude",
        "/home/mediahub-runner/.local/bin/claude",
        "/Users/voktor/.local/npm/bin/claude",
        "/Users/voktor/.local/bin/claude",
    ]
    claude = next((candidate for candidate in claude_candidates
                   if candidate and Path(candidate).is_file() and os.access(candidate, os.X_OK)), None)
    if not claude:
        raise RuntimeError("claude_cli_missing:checked_configured_and_standard_paths")
    env = os.environ.copy()
    env.update(env_updates)
    env["ANTHROPIC_BASE_URL"] = f"http://{host}:{port}"
    env["ANTHROPIC_AUTH_TOKEN"] = token
    env["ANTHROPIC_API_KEY"] = token
    env["ASTRA_FCC_TRANSPORT"] = "fcc"
    env["ASTRA_FCC_MODEL"] = "ollama/" + model
    env["CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC"] = "1"
    # qwen2.5-coder local lanes are non-thinking backends; keep Claude Code and FCC aligned.
    env["REASONING_POLICY"] = "off"
    env["ENABLE_MODEL_THINKING"] = "false"
    env["ENABLE_OPUS_THINKING"] = "false"
    env["ENABLE_SONNET_THINKING"] = "false"
    env["ENABLE_HAIKU_THINKING"] = "false"
    env["CLAUDE_CODE_DISABLE_THINKING"] = "1"
    env["MAX_THINKING_TOKENS"] = "0"
    isolated_config = tempfile.mkdtemp(prefix="astra-claude-config-")
    env["CLAUDE_CONFIG_DIR"] = isolated_config
    try:
        command = [claude, "-p", prompt, "--max-turns", str(max_turns)]
        if structured_schema is not None:
            command.extend([
                "--output-format", "json",
                "--json-schema", json.dumps(structured_schema, separators=(",", ":")),
                "--tools", tools_mode,
            ])
        else:
            command.extend(["--output-format", "text"])
            if tools_mode.strip():
                command.extend([
                    "--permission-mode", "acceptEdits",
                    "--tools", tools_mode,
                    "--allowedTools", "Read", "Edit", "Bash(git *)", "Bash(python *)",
                ])
            else:
                # Do not use Claude Code's --bare mode here. The node-local FCC adapter
                # converts Anthropic requests to OpenAI chat and requires a non-empty inline
                # Anthropic system message; --bare removes that message and produces HTTP 400.
                # The temporary cwd and CLAUDE_CONFIG_DIR isolate repo instructions and hooks
                # without breaking the adapter's required system-message contract.
                command.extend(["--tools", ""])
        # No-tool generation runs in an isolated cwd/config directory to avoid project context.
        execution_cwd = ROOT if tools_mode.strip() else Path(isolated_config)
        p = run(command, timeout, execution_cwd, env)
    finally:
        shutil.rmtree(isolated_config, ignore_errors=True)
    result = {"returncode": p.returncode, "stdout": p.stdout[-16000:], "stderr": p.stderr[-8000:]}
    failure_code = classify_executor_failure(p.stdout, p.stderr, p.returncode)
    if failure_code:
        result["failure_code"] = failure_code
    return result, server

def scope_paths(task: dict, changed: set[str]) -> list[str]:
    boundary = tuple(str(x) for x in task.get("boundary", []))
    forbidden = tuple(str(x) for x in task.get("forbidden", task.get("forbidden_surfaces", [])))
    bad = []
    for path in sorted(changed):
        normalized = path.lstrip("./")
        if any(normalized == f or normalized.startswith(f.rstrip("/") + "/") for f in forbidden):
            bad.append(normalized)
        elif boundary and not any(
            normalized == b.rstrip("/") or normalized.startswith(b.rstrip("/") + "/")
            for b in boundary
        ):
            bad.append(normalized)
    return bad


def _extract_structured_markdown(output: str) -> str | None:
    """Extract Markdown from Claude CLI JSON, including nested StructuredOutput results."""
    seen: set[str] = set()

    def visit(value: object, depth: int = 0) -> str | None:
        if depth > 4:
            return None
        if isinstance(value, str):
            raw = value.strip()
            if not raw or raw in seen:
                return None
            seen.add(raw)
            try:
                parsed = json.loads(raw)
            except json.JSONDecodeError:
                return None
            return visit(parsed, depth + 1)

        if isinstance(value, dict):
            structured = value.get("structured_output")
            if isinstance(structured, dict) and isinstance(structured.get("markdown"), str):
                return structured["markdown"].strip()
            arguments = value.get("arguments")
            if (
                str(value.get("name", "")).casefold() == "structuredoutput"
                and isinstance(arguments, dict)
                and isinstance(arguments.get("markdown"), str)
            ):
                return arguments["markdown"].strip()
            if isinstance(value.get("markdown"), str):
                return value["markdown"].strip()
            for key in ("result", "output", "content", "structured_output", "arguments"):
                if key in value:
                    extracted = visit(value[key], depth + 1)
                    if extracted:
                        return extracted
            return None

        if isinstance(value, list):
            for item in value:
                extracted = visit(item, depth + 1)
                if extracted:
                    return extracted
        return None

    return visit(output)


def _materialize_bounded_claude_tool_output(output: str, boundary: str) -> str | None:
    """Materialize only an exact-boundary Write/Edit emitted by the real Claude client."""
    candidates: list[dict] = []
    for block in re.findall(r"(?s)```json\s*(\{.*?\})\s*```", output):
        try:
            value = json.loads(block)
        except json.JSONDecodeError:
            continue
        if isinstance(value, dict):
            candidates.append(value)
    for line in output.splitlines():
        line = line.strip()
        if line.startswith("{") and line.endswith("}"):
            try:
                value = json.loads(line)
            except json.JSONDecodeError:
                continue
            if isinstance(value, dict):
                candidates.append(value)

    boundary_path = (ROOT / boundary).resolve()
    for candidate in candidates:
        name = str(candidate.get("name") or "").strip().lower()
        args = candidate.get("arguments")
        if not isinstance(args, dict) or name not in {"write", "edit"}:
            continue
        raw_path = str(args.get("file_path") or args.get("path") or "").strip()
        if not raw_path:
            continue
        target = Path(raw_path)
        if not target.is_absolute():
            target = ROOT / target
        try:
            target = target.resolve()
        except OSError:
            continue
        if target != boundary_path:
            continue
        if name == "write":
            content = args.get("content")
            if not isinstance(content, str):
                continue
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding="utf-8")
            return boundary
        old = args.get("old_string")
        new = args.get("new_string")
        if not isinstance(old, str) or not isinstance(new, str) or not target.is_file():
            continue
        current = target.read_text(encoding="utf-8")
        if old not in current:
            continue
        replace_all = bool(args.get("replace_all", False))
        target.write_text(current.replace(old, new) if replace_all else current.replace(old, new, 1), encoding="utf-8")
        return boundary
    return None


def _materialize_bounded_markdown_output(output: str, boundary: str, required_tokens: list[str]) -> str | None:
    """Materialize real model-produced Markdown only at its declared in-repository .md boundary.

    Some client responses contain a fenced document rather than a Write/Edit tool call. This
    transport fallback is intentionally limited to one declared Markdown path; scope/security
    checks, tests, and an independent verifier still gate publication.
    """
    if not boundary.endswith(".md") or Path(boundary).is_absolute():
        return None
    target = (ROOT / boundary).resolve()
    try:
        target.relative_to(ROOT.resolve())
    except ValueError:
        return None
    blocks = re.findall(r"(?s)```(?:markdown|md|plaintext|text)?[ \t]*\n(.*?)\n```", output, re.IGNORECASE)
    # Small local models often return a complete Markdown document without fences.
    # Accept only heading-led document-shaped output and keep the same token/scope gates;
    # conversational prose and arbitrary code blocks are not materialized.
    stripped_output = output.strip()
    if not blocks and re.match(r"(?m)^#{1,6}\s+", stripped_output):
        blocks = [stripped_output]
    for block in sorted(blocks, key=len, reverse=True):
        content = block.strip()
        if not content or not all(token.lower() in content.lower() for token in required_tokens):
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content + "\n", encoding="utf-8")
        return boundary
    return None


def changed_paths(target_sha: str) -> set[str]:
    changed: set[str] = set()
    for argv in [
        ["git", "diff", "--name-only", target_sha],
        ["git", "diff", "--name-only", target_sha, "HEAD"],
        ["git", "diff", "--cached", "--name-only", target_sha],
    ]:
        p = run(argv, 30)
        if p.returncode != 0:
            raise RuntimeError("diff_listing_failed")
        changed.update(x.strip() for x in p.stdout.splitlines() if x.strip())
    p = run(["git", "status", "--porcelain", "--untracked-files=all"], 30)
    if p.returncode != 0:
        raise RuntimeError("status_listing_failed")
    for line in p.stdout.splitlines():
        if line:
            value = line[3:].strip() if len(line) >= 3 else line.strip()
            if " -> " in value:
                value = value.split(" -> ", 1)[1]
            if value:
                changed.add(value)
    return changed


def diff_for_verifier(target_sha: str, changed: set[str]) -> str:
    """Build verifier evidence from tracked diffs plus newly-created bounded files.

    `git diff <sha> HEAD` compares commits only and silently omits the worker's
    uncommitted/untracked deliverable. That made the verifier assess an empty diff
    even after the builder had created the requested document.
    """
    tracked = run(["git", "diff", "--no-ext-diff", target_sha], 60)
    if tracked.returncode != 0:
        raise RuntimeError("verifier_diff_failed")
    parts = [tracked.stdout] if tracked.stdout.strip() else []
    for path in sorted(changed):
        normalized = path.lstrip("./")
        target = ROOT / normalized
        if not target.is_file():
            continue
        tracked_check = run(["git", "ls-files", "--error-unmatch", "--", normalized], 15)
        if tracked_check.returncode == 0:
            continue
        try:
            content = target.read_text(encoding="utf-8")
        except (OSError, UnicodeError):
            continue
        if len(content) > 12000:
            content = content[:12000] + "\n[TRUNCATED: verifier evidence limit]\n"
        lines = content.splitlines() or [""]
        parts.append(
            f"diff --git a/{normalized} b/{normalized}\n"
            "new file mode 100644\n--- /dev/null\n"
            f"+++ b/{normalized}\n"
            "@@ -0,0 +1," + str(len(lines)) + " @@\n"
            + "".join("+" + line + "\n" for line in lines)
        )
    return "\n".join(parts)


def deterministic_acceptance(task: dict) -> dict:
    """Validate objective deliverable requirements without delegating truth to an LLM."""
    checks = task.get("deterministic_checks")
    if not isinstance(checks, dict):
        return {"status": "NOT_CONFIGURED", "failures": ["deterministic_checks_missing"]}

    boundaries = [str(x) for x in task.get("boundary", [])]
    deliverable = str(task.get("deliverable") or (boundaries[0] if len(boundaries) == 1 else ""))
    if not deliverable or deliverable not in boundaries:
        return {"status": "BLOCKED", "failures": ["deliverable_not_inside_declared_boundary"]}
    target = ROOT / deliverable
    if not target.is_file():
        return {"status": "BLOCKED", "failures": ["deliverable_missing:" + deliverable]}
    try:
        content = target.read_text(encoding="utf-8")
    except (OSError, UnicodeError):
        return {"status": "BLOCKED", "failures": ["deliverable_unreadable:" + deliverable]}

    failures: list[str] = []
    lowered = content.casefold()
    for token in checks.get("required_text", []):
        token = str(token)
        if token.casefold() not in lowered:
            failures.append("missing_required_text:" + token)
    for pattern in checks.get("required_patterns", []):
        pattern = str(pattern)
        try:
            matched = re.search(pattern, content, re.IGNORECASE | re.MULTILINE) is not None
        except re.error:
            failures.append("invalid_required_pattern:" + pattern)
            continue
        if not matched:
            failures.append("missing_required_pattern:" + pattern)
    for pattern in checks.get("forbidden_patterns", []):
        pattern = str(pattern)
        try:
            matched = re.search(pattern, content, re.IGNORECASE | re.MULTILINE) is not None
        except re.error:
            failures.append("invalid_forbidden_pattern:" + pattern)
            continue
        if matched:
            failures.append("forbidden_pattern_present:" + pattern)
    document_lines = task.get("document_lines")
    if isinstance(document_lines, list) and document_lines:
        expected_lines = ["# " + Path(deliverable).name] + [str(line).strip() for line in document_lines]
        actual_lines = [line.strip() for line in content.splitlines() if line.strip()]
        if actual_lines != expected_lines:
            failures.append("document_lines_not_exact_or_unexpected_content")

    return {
        "status": "PASS" if not failures else "BLOCKED",
        "deliverable": deliverable,
        "checks_run": len(checks.get("required_text", []))
            + len(checks.get("required_patterns", []))
            + len(checks.get("forbidden_patterns", []))
            + (1 if isinstance(document_lines, list) and document_lines else 0),
        "failures": failures,
    }


def plain_markdown_prompt(
    task: dict,
    node_id: str,
    executor: str,
    model: str,
    target_sha: str,
    previous_failures: list[str] | None = None,
) -> str:
    """Build a compact prompt for bounded Markdown-only worker tasks."""
    boundary = str(task.get("deliverable") or task.get("boundary", [""])[0])
    filename = Path(boundary).name
    document_lines = task.get("document_lines")
    if not isinstance(document_lines, list) or not document_lines:
        raise RuntimeError("plain_markdown_document_lines_missing")
    required_body = "\n".join(str(line) for line in document_lines)
    repair = ""
    if previous_failures:
        repair = (
            "\nThe previous draft failed deterministic validation. Fix only these failures: "
            + json.dumps(previous_failures, sort_keys=True)
            + ". The required output below remains the entire document."
        )
    # Put all instructions before the canonical body so small local models are less likely
    # to copy instruction text into the deliverable.
    return (
        "You are the A2 Builder. Generate one Markdown file.\n"
        "Output only the file content, with no tool calls, status reports, examples, descriptions, or commentary.\n"
        "Copy the required heading and every body line verbatim, in order. Do not add headings to body lines.\n"
        f"File path: {boundary}; node: {node_id}; executor: {executor}; model: {model}; "
        f"independent verifier: {task.get('verifier')}; target SHA: {target_sha}.\n"
        + repair
        + "\nThe entire document is exactly the text that follows. Do not output anything else.\n\n"
        f"# {filename}\n{required_body}"
    )

def strip_known_cli_metadata(output: str) -> str:
    """Normalize one outer Markdown fence and remove only a standalone CLI date footer."""
    lines = (output or "").strip().splitlines()
    fence = chr(96) * 3
    if (
        len(lines) >= 3
        and re.fullmatch(r"\s*" + re.escape(fence) + r"(?:markdown|md)?\s*", lines[0], re.IGNORECASE)
        and lines[-1].strip() == fence
    ):
        lines = lines[1:-1]
    if lines and re.fullmatch(r"Today's date is \d{4}-\d{2}-\d{2}\.", lines[-1].strip(), re.IGNORECASE):
        lines.pop()
    return "\n".join(lines).strip()


def parse_verifier_verdict(output: str) -> str | None:
    """Accept a canonical standalone verdict on the first non-empty output line."""
    first = next((line.strip() for line in (output or "").splitlines() if line.strip()), "")
    match = re.fullmatch(
        r"(?:\*\*)?ASTRA_VERDICT:\s*(PASS|BLOCKED)(?:\*\*)?",
        first,
        flags=re.IGNORECASE,
    )
    return match.group(1).upper() if match else None


def verify_executor(task: dict, diff_text: str, test_text: str, model: str) -> dict:
    prompt = (
        "You are an independent A3 Verifier. Review the completed micro-task against every "
        "acceptance criterion below.\n"
        f"Task ID: {task['task_id']}\n"
        f"Acceptance: {json.dumps(task.get('acceptance', []), sort_keys=True)}\n"
        f"Boundary: {json.dumps(task.get('boundary', []), sort_keys=True)}\n"
        "Decide only from the supplied evidence. Output exactly one line and nothing else.\n"
        "--- DIFF ---\n" + diff_text[-6000:] +
        "\n--- TESTS ---\n" + test_text[-2500:] +
        "\nReturn exactly: ASTRA_VERDICT: PASS or ASTRA_VERDICT: BLOCKED."
    )
    verifier = task["verifier"]
    if verifier == "codex":
        return exec_codex(prompt, False, model, 240)
    if verifier == "claude":
        env_file = Path(os.environ["ASTRA_FCC_ENV_FILE"])
        # The verifier must judge only the supplied evidence; disable all tools and
        # project-context auto-discovery so it cannot alter files or act on ambient instructions.
        return exec_claude(prompt, model, 240, env_file, 128, max_turns=2, tools_mode="")[0]
    raise RuntimeError("unsupported_verifier")


def security_gate(changed: set[str], task: dict) -> list[str]:
    """Bounded pre-verifier security gate inspired by ECC security-review patterns."""
    forbidden = tuple(str(x) for x in task.get("forbidden", task.get("forbidden_surfaces", [])))
    findings: list[str] = []
    secret_patterns = [
        re.compile(r"(?i)(?:api[_-]?key|access[_-]?token|secret|private[_-]?key|bearer)\s*[:=]\s*['\"][^'\"]{12,}"),
        re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    ]
    for path in sorted(changed):
        normalized = path.lstrip("./")
        if any(normalized == root or normalized.startswith(root.rstrip("/") + "/") for root in forbidden):
            findings.append("forbidden_surface:" + normalized)
            continue
        target = ROOT / normalized
        if not target.is_file() or target.stat().st_size > 2 * 1024 * 1024:
            continue
        try:
            text = target.read_text(encoding="utf-8", errors="replace")
        except OSError:
            findings.append("unreadable_changed_file:" + normalized)
            continue
        for pattern in secret_patterns:
            if pattern.search(text):
                findings.append("possible_secret:" + normalized)
                break
        if normalized in {".env", ".env.local", ".env.production"} or normalized.endswith(".pem"):
            findings.append("sensitive_file:" + normalized)
    return sorted(set(findings))


def main() -> int:
    task = load_task()
    target_sha = os.environ.get("ASTRA_TARGET_SHA", "")
    command_id = os.environ.get("ASTRA_COMMAND_ID", "")
    node_id = os.environ.get("ASTRA_NODE_ID", "")
    executor = task["executor"]
    cfg = NODE_CONFIG.get(node_id)
    if not cfg:
        raise RuntimeError("unsupported_node")
    if task["node_id"] != node_id:
        raise RuntimeError("task_node_binding_mismatch")
    if executor not in {"codex", "claude"}:
        raise RuntimeError("unsupported_executor")
    if not re.fullmatch(r"[0-9a-f]{40}", target_sha or ""):
        raise RuntimeError("invalid_target_sha")
    current = run(["git", "rev-parse", "HEAD"], 30).stdout.strip()
    if current != target_sha:
        raise RuntimeError("target_sha_not_current_head")
    if run(["git", "status", "--porcelain", "--untracked-files=all"], 30).stdout.strip():
        raise RuntimeError("dirty_worker_workspace")
    if cfg["model"] not in {"qwen2.5-coder:3b", "qwen2.5-coder:1.5b"}:
        raise RuntimeError("unsupported_local_model")
    if not ollama_has_model(cfg["model"]):
        raise RuntimeError("required_local_model_missing")

    task_id = safe_id(str(task["task_id"]))
    branch = f"astra/auto/{task_id}-{target_sha[:12]}-distributed-{int(time.time())}"
    checkout = run(["git", "switch", "-c", branch], 60)
    if checkout.returncode != 0:
        raise RuntimeError("worker_branch_create_failed")

    started = int(time.time())
    record = {
        "schema": "mediahub.astra.distributed-local-worker.v1",
        "status": "BLOCKED",
        "command_id": command_id,
        "target_sha": target_sha,
        "node_id": node_id,
        "pool": cfg["pool"],
        "task_id": task_id,
        "executor_identity": executor,
        "model": cfg["model"],
        "verifier_identity": task["verifier"],
        "branch": branch,
        "started_at": started,
    }
    server = None
    try:
        builder_prompt_text = task_prompt(task, "A2 Builder")
        builder_timeout = int(task.get("timeout_seconds", 1800))
        builder_attempts = max(1, min(int(task.get("builder_attempts", 2)), 3))
        build = {"returncode": 1, "stdout": "", "stderr": "builder_not_run"}
        attempt_records = []

        if task.get("builder_mode") == "plain_markdown":
            boundaries = [str(value) for value in task.get("boundary", [])]
            if (
                executor != "claude"
                or len(boundaries) != 1
                or not boundaries[0].endswith(".md")
                or not isinstance(task.get("deterministic_checks"), dict)
            ):
                raise RuntimeError("plain_markdown_mode_requires_bounded_deterministic_markdown_task")

            boundary = boundaries[0]
            plain_attempts = max(1, min(builder_attempts, 2))
            plain_timeout = min(
                builder_timeout,
                max(30, int(task.get("plain_artifact_timeout_seconds", 300))),
            )
            previous_failures: list[str] = []
            for plain_attempt in range(1, plain_attempts + 1):
                prompt = plain_markdown_prompt(
                    task, node_id, executor, cfg["model"], target_sha, previous_failures
                )
                plain_result, server = exec_claude(
                    prompt,
                    cfg["model"],
                    plain_timeout,
                    Path(os.environ["ASTRA_FCC_ENV_FILE"]),
                    max_turns=1,
                    tools_mode="",
                )
                attempt_records.append({
                    "attempt": plain_attempt,
                    "mode": "plain_markdown_builder",
                    "returncode": plain_result.get("returncode"),
                    "failure_code": plain_result.get("failure_code", ""),
                    "stdout": plain_result.get("stdout", "")[-4000:],
                    "stderr": plain_result.get("stderr", "")[-3000:],
                })

                if plain_result.get("returncode") != 0:
                    previous_failures = [
                        "plain_markdown_executor_returncode:"
                        + str(plain_result.get("returncode"))
                    ]
                    failure_code = plain_result.get("failure_code") or classify_executor_failure(
                        plain_result.get("stdout", ""), plain_result.get("stderr", ""),
                        int(plain_result.get("returncode", 1)),
                    )
                    build = {
                        **plain_result,
                        "returncode": 1,
                        "failure_code": failure_code,
                        "stderr": "plain_markdown_executor_failed:" + failure_code,
                    }
                    continue

                required_tokens = [node_id, executor, task["verifier"], "fail-closed", "main"]
                normalized_output = strip_known_cli_metadata(plain_result.get("stdout", ""))
                materialized = _materialize_bounded_markdown_output(
                    normalized_output, boundary, required_tokens
                )
                if not materialized:
                    previous_failures = [
                        "plain_markdown_output_not_materialized:requires_heading_and_contract_tokens"
                    ]
                    build = {
                        **plain_result,
                        "returncode": 1,
                        "stderr": previous_failures[0],
                    }
                    continue

                gate = deterministic_acceptance(task)
                plain_result["deterministic_acceptance"] = gate
                if gate.get("status") != "PASS":
                    previous_failures = list(gate.get("failures", []))
                    build = {
                        **plain_result,
                        "returncode": 1,
                        "stderr": "deterministic_acceptance_blocked:"
                            + ",".join(previous_failures),
                    }
                    continue

                build = plain_result
                build["materialized_plain_text_artifact"] = materialized
                break

            # This bounded path replaces the interactive multi-tool builder loop.
            # A failed artifact reaches the same fail-closed builder gate below.
            builder_attempts = 0

        for attempt in range(1, builder_attempts + 1):
            attempt_prompt = builder_prompt_text
            if attempt > 1:
                attempt_prompt += (
                    "\n\nRETRY REQUIREMENT: The previous builder attempt completed without a "
                    "usable diff. You MUST make the smallest concrete change required by the "
                    "acceptance criteria. For this task, modify the declared boundary directly; "
                    "do not merely explain what should be changed. Finish only after the file "
                    "contains the requested regression coverage."
                )
            if executor == "codex":
                build = exec_codex(attempt_prompt, True, cfg["model"], builder_timeout)
            else:
                build, server = exec_claude(
                    attempt_prompt,
                    cfg["model"],
                    builder_timeout,
                    Path(os.environ["ASTRA_FCC_ENV_FILE"]),
                    max_turns=6,
                )
            attempt_records.append({
                "attempt": attempt,
                "returncode": build.get("returncode"),
                "failure_code": build.get("failure_code", ""),
                "stdout": build.get("stdout", "")[-4000:],
                "stderr": build.get("stderr", "")[-3000:],
            })
            if build["returncode"] != 0:
                break
            changed_probe = changed_paths(target_sha)
            if changed_probe:
                gate = deterministic_acceptance(task)
                if gate["status"] == "PASS":
                    break
                attempt_records.append({
                    "attempt": attempt,
                    "mode": "deterministic_acceptance_retry",
                    "returncode": 1,
                    "stderr": json.dumps(gate.get("failures", []), sort_keys=True),
                })
                builder_prompt_text += (
                    "\n\nAUTOMATED ACCEPTANCE GATE BLOCKED the previous artifact. "
                    "Revise the declared deliverable to satisfy every deterministic requirement. "
                    "Do not claim success unless the file content itself satisfies these checks. "
                    "Exact failures: " + json.dumps(gate.get("failures", []), sort_keys=True)
                )
                if attempt < builder_attempts:
                    continue
                break
            if executor == "claude":
                boundaries = [str(x) for x in task.get("boundary", [])]
                if len(boundaries) == 1:
                    # Materialization is only a plausibility check; the independent A3 verifier must
                    # decide whether all acceptance criteria, including model/SHA binding, hold.
                    required_tokens = [node_id, executor, task["verifier"], "fail-closed", "main"]
                    materialized_builder = _materialize_bounded_markdown_output(
                        build.get("stdout", ""), boundaries[0], required_tokens
                    )
                    if materialized_builder:
                        changed_probe = changed_paths(target_sha)
                        if changed_probe:
                            gate = deterministic_acceptance(task)
                            if gate["status"] == "PASS":
                                build["materialized_builder_artifact"] = materialized_builder
                                break
                            attempt_records.append({
                                "attempt": attempt, "mode": "deterministic_acceptance_retry",
                                "returncode": 1,
                                "stderr": json.dumps(gate.get("failures", []), sort_keys=True),
                            })
                            builder_prompt_text += (
                                "\n\nAUTOMATED ACCEPTANCE GATE BLOCKED the artifact. "
                                "Correct these exact failures: "
                                + json.dumps(gate.get("failures", []), sort_keys=True)
                            )
                            if attempt < builder_attempts:
                                continue
            if executor == "claude" and attempt == builder_attempts:
                boundaries = [str(x) for x in task.get("boundary", [])]
                if len(boundaries) == 1 and boundaries[0].endswith(".md"):
                    document_facts = [
                        str(item) for item in task.get("acceptance", [])
                        if "document" in str(item).lower() or "states" in str(item).lower()
                    ]
                    artifact_prompt = (
                        "Generate one concise Markdown operations document. Do not discuss Python, charts, "
                        "regression examples, or hypothetical code. Do not emit tool calls. "
                        "Return only the document between ASTRA_ARTIFACT_BEGIN and ASTRA_ARTIFACT_END. "
                        f"Boundary: {boundaries[0]}. "
                        f"Required node: {node_id}. Executor: {executor}. Verifier: {task['verifier']}. "
                        f"Local model: {cfg['model']}. "
                        "The document must explicitly state the required facts below, using the exact identifiers "
                        "and security terms: "
                        + json.dumps(document_facts, sort_keys=True)
                        + ". Canonical task-specific instructions: " + str(task.get("builder_instructions", ""))
                        + ". Also state target-SHA binding, isolated branch execution, GitHub evidence transport, "
                        "fail-closed promotion, and no direct writes to main. No credentials or secrets."
                    )
                    artifact_schema = {
                        "type": "object",
                        "properties": {"markdown": {"type": "string"}},
                        "required": ["markdown"],
                        "additionalProperties": False,
                    }
                    artifact, server = exec_claude(
                        artifact_prompt
                        + "\nReturn a single JSON object matching the schema; put the complete Markdown document in the markdown field. "
                        + "Do not call tools and do not include any other fields.",
                        cfg["model"],
                        builder_timeout,
                        Path(os.environ["ASTRA_FCC_ENV_FILE"]),
                        max_turns=3,
                        structured_schema=artifact_schema,
                        tools_mode="",
                    )
                    attempt_records.append({
                        "attempt": attempt,
                        "mode": "artifact_fallback",
                        "returncode": artifact.get("returncode"),
                        "stdout": artifact.get("stdout", "")[-4000:],
                        "stderr": artifact.get("stderr", "")[-3000:],
                    })
                    output = artifact.get("stdout", "")
                    structured_markdown = (
                        _extract_structured_markdown(output)
                        if artifact.get("returncode") == 0
                        else None
                    )
                    if structured_markdown:
                        artifact_match = re.search(
                            r"__ASTRA_ARTIFACT_BEGIN__\\n(.*?)\\n__ASTRA_ARTIFACT_END__",
                            structured_markdown,
                            re.DOTALL,
                        )
                        if artifact_match:
                            structured_markdown = artifact_match.group(1).strip()
                    if structured_markdown and boundaries:
                        required_tokens = [node_id, executor, task["verifier"], "fail-closed", "main"]
                        if all(token.lower() in structured_markdown.lower() for token in required_tokens):
                            artifact_path = ROOT / boundaries[0]
                            artifact_path.parent.mkdir(parents=True, exist_ok=True)
                            artifact_path.write_text(structured_markdown + "\n", encoding="utf-8")
                            changed_probe = changed_paths(target_sha)
                            if changed_probe:
                                gate = deterministic_acceptance(task)
                                if gate["status"] == "PASS":
                                    build = artifact
                                    build["materialized_structured_artifact"] = boundaries[0]
                                    break
                                attempt_records.append({
                                    "attempt": attempt, "mode": "deterministic_acceptance_retry",
                                    "returncode": 1,
                                    "stderr": json.dumps(gate.get("failures", []), sort_keys=True),
                                })
                                builder_prompt_text += (
                                    "\n\nAUTOMATED ACCEPTANCE GATE BLOCKED the structured artifact. "
                                    "Correct these exact failures: "
                                    + json.dumps(gate.get("failures", []), sort_keys=True)
                                )
                                if attempt < builder_attempts:
                                    continue
                    materialized_tool = None
                    if artifact.get("returncode") == 0 and boundaries:
                        materialized_tool = _materialize_bounded_claude_tool_output(output, boundaries[0])
                        if materialized_tool:
                            changed_probe = changed_paths(target_sha)
                            if changed_probe:
                                gate = deterministic_acceptance(task)
                                if gate["status"] == "PASS":
                                    build = artifact
                                    build["materialized_tool_output"] = materialized_tool
                                    break
                                attempt_records.append({
                                    "attempt": attempt, "mode": "deterministic_acceptance_retry",
                                    "returncode": 1,
                                    "stderr": json.dumps(gate.get("failures", []), sort_keys=True),
                                })
                                builder_prompt_text += (
                                    "\n\nAUTOMATED ACCEPTANCE GATE BLOCKED the tool artifact. "
                                    "Correct these exact failures: "
                                    + json.dumps(gate.get("failures", []), sort_keys=True)
                                )
                                if attempt < builder_attempts:
                                    continue
                    match = re.search(
                        r"ASTRA_ARTIFACT_BEGIN\s*\n(.*?)\nASTRA_ARTIFACT_END",
                        output,
                        re.DOTALL,
                    )
                    if artifact.get("returncode") == 0 and match:
                        artifact_text = match.group(1).strip()
                        required_tokens = [node_id, executor, task["verifier"], "fail-closed", "main"]
                        if not all(token.lower() in artifact_text.lower() for token in required_tokens):
                            attempt_records.append({
                                "attempt": attempt,
                                "mode": "artifact_validation",
                                "returncode": 1,
                                "stderr": "artifact_missing_required_contract_terms",
                                "stdout": artifact_text[-4000:],
                            })
                        else:
                            artifact_path = ROOT / boundaries[0]
                            artifact_path.parent.mkdir(parents=True, exist_ok=True)
                            artifact_path.write_text(artifact_text + "\n", encoding="utf-8")
                            changed_probe = changed_paths(target_sha)
                            if changed_probe:
                                gate = deterministic_acceptance(task)
                                if gate["status"] == "PASS":
                                    build = artifact
                                    build["materialized_artifact"] = boundaries[0]
                                    break
                                attempt_records.append({
                                    "attempt": attempt, "mode": "deterministic_acceptance_retry",
                                    "returncode": 1,
                                    "stderr": json.dumps(gate.get("failures", []), sort_keys=True),
                                })
                                builder_prompt_text += (
                                    "\n\nAUTOMATED ACCEPTANCE GATE BLOCKED the fenced artifact. "
                                    "Correct these exact failures: "
                                    + json.dumps(gate.get("failures", []), sort_keys=True)
                                )
                                if attempt < builder_attempts:
                                    continue
        # StructuredOutput tool-call JSON is not supported consistently by local small
        # models. If all prior materialization routes failed, ask for plain Markdown once;
        # the same strict acceptance, scope, security, tests, and independent-verifier gates
        # still decide whether it can be published.
        if (
            task.get("builder_mode") != "plain_markdown"
            and executor == "claude"
            and isinstance(task.get("deterministic_checks"), dict)
            and len(task.get("boundary", [])) == 1
            and str(task.get("boundary", [""])[0]).endswith(".md")
            and deterministic_acceptance(task).get("status") != "PASS"
        ):
            boundary = str(task["boundary"][0])
            checks = task["deterministic_checks"]
            plain_prompt = (
                "Produce the actual requested Markdown deliverable now. Return only the document, "
                "not a plan, tutorial, example commands, or commentary. The first characters of "
                "your response must be a level-one Markdown heading naming the requested file. "
                "Copy every required literal text item exactly. Match every required positive "
                "requirement and avoid all forbidden requirements. Do not claim tests or external "
                "actions occurred unless there is evidence in the task context.\n"
                f"Required path: {boundary}\n"
                f"Required node: {node_id}\n"
                f"Executor: {executor}\nVerifier: {task['verifier']}\n"
                f"Local model: {cfg['model']}\n"
                f"Target SHA: {target_sha}\n"
                f"Task requirements: {json.dumps(task.get('acceptance', []), sort_keys=True)}\n"
                f"Exact task instructions: {task.get('builder_instructions', '')}\n"
                f"Required literal text: {json.dumps(checks.get('required_text', []), sort_keys=True)}\n"
                f"Required contract patterns: {json.dumps(checks.get('required_patterns', []), sort_keys=True)}\n"
                f"Forbidden contract patterns: {json.dumps(checks.get('forbidden_patterns', []), sort_keys=True)}\n"
                "The content must be factual, concise, and limited to the deliverable. Do not state "
                "that the work is complete without providing the document itself."
            )
            plain_artifact, server = exec_claude(
                plain_prompt,
                cfg["model"],
                min(builder_timeout, int(task.get("plain_artifact_timeout_seconds", 600))),
                Path(os.environ["ASTRA_FCC_ENV_FILE"]),
                max_turns=2,
                tools_mode="",
            )
            attempt_records.append({
                "attempt": builder_attempts + 1,
                "mode": "plain_text_artifact_fallback",
                "returncode": plain_artifact.get("returncode"),
                "stdout": plain_artifact.get("stdout", "")[-4000:],
                "stderr": plain_artifact.get("stderr", "")[-3000:],
            })
            if plain_artifact.get("returncode") == 0:
                required_tokens = [node_id, executor, task["verifier"], "fail-closed", "main"]
                materialized_plain = _materialize_bounded_markdown_output(
                    plain_artifact.get("stdout", ""), boundary, required_tokens
                )
                if materialized_plain:
                    plain_gate = deterministic_acceptance(task)
                    plain_artifact["materialized_plain_text_artifact"] = materialized_plain
                    plain_artifact["deterministic_acceptance"] = plain_gate
                    build = plain_artifact
                    if plain_gate.get("status") != "PASS":
                        attempt_records.append({
                            "attempt": builder_attempts + 1,
                            "mode": "plain_text_acceptance_retry_unavailable",
                            "returncode": 1,
                            "stderr": json.dumps(plain_gate.get("failures", []), sort_keys=True),
                        })
        record["builder"] = build
        record["builder_attempts"] = attempt_records
        if build["returncode"] != 0:
            raise RuntimeError(
                "builder_failed:{}".format(
                    (build.get("stderr") or build.get("stdout") or "no_builder_diagnostics")[-2000:]
                )
            )

        changed = changed_paths(target_sha)
        deterministic_result = deterministic_acceptance(task)
        record["deterministic_acceptance"] = deterministic_result
        if deterministic_result["status"] != "PASS":
            raise RuntimeError(
                "deterministic_acceptance_blocked:"
                + ",".join(deterministic_result.get("failures", []))
            )

        security_findings = security_gate(changed, task)
        record["security_gate"] = {"status": "PASS" if not security_findings else "BLOCKED", "findings": security_findings}
        if security_findings:
            raise RuntimeError("security_gate_blocked")
        outside = scope_paths(task, changed)
        record["scope"] = {"status": "PASS" if not outside else "BLOCKED", "outside_scope": outside}
        if outside:
            raise RuntimeError("task_boundary_violation")

        test_paths = [str(x) for x in task.get("test_paths", [])]
        test_env = os.environ.copy()
        test_env["PYTHONPATH"] = str(ROOT / "runtime") + os.pathsep + str(ROOT) + os.pathsep + test_env.get("PYTHONPATH", "")
        test_env = os.environ.copy()
        existing_pythonpath = test_env.get("PYTHONPATH", "")
        test_env["PYTHONPATH"] = os.pathsep.join(
            p for p in [str(ROOT / "runtime"), str(ROOT), existing_pythonpath] if p
        )
        if len(test_paths) == 1:
            test_path = Path(test_paths[0])
            test_script = (
                "import sys,unittest; "
                "sys.path.insert(0, 'runtime'); "
                f"sys.path.insert(0, '{test_path.parent}'); "
                f"s=unittest.defaultTestLoader.discover('{test_path.parent}', pattern='{test_path.name}'); "
                "r=unittest.TextTestRunner(verbosity=2).run(s); "
                "raise SystemExit(0 if r.wasSuccessful() else 1)"
            )
            test = run(["python3", "-c", test_script], 900, env=test_env)
        elif test_paths:
            test = run(["python3", "-m", "unittest", *test_paths], 900, env=test_env)
        else:
            test = run(["python3", "-c", "import sys,unittest; sys.path.insert(0,'runtime'); s=unittest.defaultTestLoader.discover('tests', pattern='test_*.py'); r=unittest.TextTestRunner(verbosity=2).run(s); raise SystemExit(0 if r.wasSuccessful() else 1)"], 900, env=test_env)
        record["tests"] = {
            "returncode": test.returncode,
            "stdout": test.stdout[-10000:],
            "stderr": test.stderr[-6000:],
        }
        if test.returncode != 0:
            raise RuntimeError("tests_failed")

        verifier_diff = diff_for_verifier(target_sha, changed)
        if not bool(task.get("allow_no_changes", False)) and not verifier_diff.strip():
            raise RuntimeError("no_changes_before_verifier")
        record["verifier_evidence"] = {
            "diff_characters": len(verifier_diff),
            "changed_paths": sorted(changed),
            "includes_untracked_files": any(
                run(["git", "ls-files", "--error-unmatch", "--", path], 15).returncode != 0
                for path in changed
            ),
        }
        verifier = verify_executor(
            task, verifier_diff, record["tests"]["stdout"] + record["tests"]["stderr"], cfg["model"]
        )
        record["verifier"] = verifier
        parsed_verdict = parse_verifier_verdict(verifier.get("stdout", ""))
        record["verifier"]["parsed_verdict"] = parsed_verdict
        if verifier["returncode"] != 0 or parsed_verdict != "PASS":
            raise RuntimeError("verifier_failed_or_noncanonical_verdict")

        if not run(["git", "status", "--porcelain"], 30).stdout.strip():
            if not bool(task.get("allow_no_changes", False)):
                raise RuntimeError("no_changes")
            record["change_status"] = "NO_CHANGES_REQUIRED"
            record["head_sha"] = target_sha
            record["push_verification"] = {"status": "NOT_REQUIRED", "branch": branch}
        else:
            if run(["git", "add", "-A"], 30).returncode != 0:
                raise RuntimeError("git_add_failed")
            commit = run(["git", "commit", "-m", f"astra distributed: complete {task_id}"], 120)
            if commit.returncode != 0:
                raise RuntimeError("git_commit_failed")
            push = run(["git", "push", "origin", f"HEAD:refs/heads/{branch}"], 180)
            record["push"] = {"returncode": push.returncode, "stdout": push.stdout[-5000:], "stderr": push.stderr[-5000:]}
            if push.returncode != 0:
                raise RuntimeError("git_push_failed")
            record["head_sha"] = run(["git", "rev-parse", "HEAD"], 30).stdout.strip()
            remote = run(["git", "ls-remote", "origin", f"refs/heads/{branch}"], 60)
            if remote.returncode != 0:
                raise RuntimeError("git_push_verification_failed")
            remote_sha = remote.stdout.split()[0] if remote.stdout.split() else ""
            if remote_sha != record["head_sha"]:
                raise RuntimeError("git_push_sha_mismatch")
            record["remote_head"] = remote_sha
            record["push_verification"] = {"status": "PASS", "branch": branch, "remote_sha": remote_sha}

        record["completed_at"] = int(time.time())
        record["status"] = "PASS"
    except Exception as exc:
        record["completed_at"] = int(time.time())
        if isinstance(locals().get("build"), dict) and locals()["build"].get("failure_code"):
            record["failure_code"] = locals()["build"]["failure_code"]
        record["error"] = type(exc).__name__ + ":" + str(exc)
    finally:
        if server is not None:
            try:
                server.terminate()
            except Exception:
                pass

    canonical = json.dumps(record, sort_keys=True, separators=(",", ":"))
    record["evidence_digest"] = "sha256:" + hashlib.sha256(canonical.encode()).hexdigest()
    out = Path(os.environ.get("ASTRA_WORKER_RESULT", "astra-distributed-worker-result.json"))
    out.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": record["status"],
        "task_id": task_id,
        "command_id": command_id,
        "target_sha": target_sha,
        "node_id": node_id,
        "executor": executor,
        "branch": record["branch"],
        "head_sha": record.get("head_sha"),
        "remote_head": record.get("remote_head"),
        "error": record.get("error"),
    }, sort_keys=True))
    return 0 if record["status"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
