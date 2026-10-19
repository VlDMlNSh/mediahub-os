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
        f"Acceptance: {json.dumps(task.get('acceptance', []), sort_keys=True)}\n"        f"Builder instructions: {task.get('builder_instructions', 'Use shell/editor directly to complete the declared boundary.')}\n"
        f"Target SHA: {os.environ['ASTRA_TARGET_SHA']}\n"
        "Treat every acceptance criterion containing exact identifiers, node names, executor names, or security rules as literal requirements: copy them verbatim and never invent aliases, synonyms, or substitute names. "        "Work only inside the declared boundary. Do not touch production infrastructure, "
        "credentials, user data, or unrelated paths. Do not merge to main. "
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


def ollama_has_model(model: str) -> bool:
    binary = shutil.which("ollama") or "/usr/local/bin/ollama"
    p = run([binary, "list"], 20)
    return p.returncode == 0 and any(line.split() and line.split()[0] == model for line in p.stdout.splitlines())


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
    claude = shutil.which("claude")
    if not claude:
        raise RuntimeError("claude_cli_missing")
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
            command.extend([
                "--output-format", "text",
                "--permission-mode", "acceptEdits",
                "--tools", tools_mode,
                "--allowedTools", "Read", "Edit", "Bash(git *)", "Bash(python *)",
            ])
        p = run(command, timeout, ROOT, env)
    finally:
        shutil.rmtree(isolated_config, ignore_errors=True)
    return {"returncode": p.returncode, "stdout": p.stdout[-16000:], "stderr": p.stderr[-8000:]}, server

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
        return exec_claude(prompt, model, 240, env_file, 128, max_turns=2)[0]
    raise RuntimeError("unsupported_verifier")


def security_gate(changed: set[str], task: dict) -> list[str]:
    """Bounded pre-verifier security gate inspired by ECC security-review patterns."""
    forbidden = tuple(str(x) for x in task.get("forbidden", task.get("forbidden_surfaces", [])))
    findings: list[str] = []
    secret_patterns = [
        re.compile(r"""(?i)(api[_-]?key|access[_-]?token|secret|private[_-]?key|bearer)\s*[:=]\s*['"][^'"]{12,}"""),
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
                "stdout": build.get("stdout", "")[-4000:],
                "stderr": build.get("stderr", "")[-3000:],
            })
            if build["returncode"] != 0:
                break
            changed_probe = changed_paths(target_sha)
            if changed_probe:
                break
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
                    structured_markdown = None
                    if artifact.get("returncode") == 0:
                        try:
                            structured_payload = json.loads(output)
                            structured_markdown = str(
                                structured_payload.get("structured_output", {}).get("markdown", "")
                                if isinstance(structured_payload.get("structured_output"), dict)
                                else ""
                            ).strip()
                            if not structured_markdown and isinstance(structured_payload.get("result"), str):
                                inner = structured_payload["result"]
                                artifact_match = re.search(
                                    r"__ASTRA_ARTIFACT_BEGIN__\\n(.*?)\\n__ASTRA_ARTIFACT_END__",
                                    inner,
                                    re.DOTALL,
                                )
                                if artifact_match:
                                    structured_markdown = artifact_match.group(1).strip()
                        except (json.JSONDecodeError, AttributeError, TypeError):
                            structured_markdown = None
                    if structured_markdown and boundaries:
                        required_tokens = [
                            node_id,
                            executor,
                            task["verifier"],
                            cfg["model"],
                            "target-SHA",
                            "fail-closed",
                            "main",
                        ]
                        if all(token.lower() in structured_markdown.lower() for token in required_tokens):
                            artifact_path = ROOT / boundaries[0]
                            artifact_path.parent.mkdir(parents=True, exist_ok=True)
                            artifact_path.write_text(structured_markdown + "\n", encoding="utf-8")
                            changed_probe = changed_paths(target_sha)
                            if changed_probe:
                                build = artifact
                                build["materialized_structured_artifact"] = boundaries[0]
                                break
                    materialized_tool = None
                    if artifact.get("returncode") == 0 and boundaries:
                        materialized_tool = _materialize_bounded_claude_tool_output(output, boundaries[0])
                        if materialized_tool:
                            changed_probe = changed_paths(target_sha)
                            if changed_probe:
                                build = artifact
                                build["materialized_tool_output"] = materialized_tool
                                break
                    match = re.search(
                        r"ASTRA_ARTIFACT_BEGIN\s*\n(.*?)\nASTRA_ARTIFACT_END",
                        output,
                        re.DOTALL,
                    )
                    if artifact.get("returncode") == 0 and match:
                        artifact_text = match.group(1).strip()
                        required_tokens = [
                            node_id,
                            executor,
                            task["verifier"],
                            cfg["model"],
                            "target-SHA",
                            "fail-closed",
                            "main",
                        ]
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
                                build = artifact
                                build["materialized_artifact"] = boundaries[0]
                                break
        record["builder"] = build
        record["builder_attempts"] = attempt_records
        if build["returncode"] != 0:
            raise RuntimeError(
                "builder_failed:{}".format(
                    (build.get("stderr") or build.get("stdout") or "no_builder_diagnostics")[-2000:]
                )
            )

        changed = changed_paths(target_sha)
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

        diff = run(["git", "diff", "--no-ext-diff", target_sha, "HEAD"], 60)
        if diff.returncode != 0:
            raise RuntimeError("verifier_diff_failed")
        if not bool(task.get("allow_no_changes", False)) and not diff.stdout.strip():
            raise RuntimeError("no_changes_before_verifier")
        verifier = verify_executor(
            task, diff.stdout, record["tests"]["stdout"] + record["tests"]["stderr"], cfg["model"]
        )
        record["verifier"] = verifier
        if verifier["returncode"] != 0 or VERDICT_MARKER not in verifier["stdout"]:
            raise RuntimeError("verifier_failed")

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
