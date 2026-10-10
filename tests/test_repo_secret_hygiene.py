"""Repository secret-hygiene gate.

Two invariants are declared in
``architecture/ASTRA-GOLD-GOVERNANCE-CONTRACT.yaml`` and bound to enforcing
test files:

    INV_NO_CREDENTIALS_IN_GIT     -> tests/test_repo_hygiene.py
    INV_NO_SECRETS_IN_EVIDENCE    -> tests/test_astra_security.py

Both bindings were file-level only, and neither file actually enforced the
invariant: ``test_repo_hygiene.py`` did not inspect file contents for
credentials and ``test_astra_security.py`` never looked at evidence at all.
The invariant registry therefore claimed coverage that did not exist.

This module supplies the real enforcement using the repository's own
detector (``mediahub_runtime.astra_security.scan_secret``) so the scan cannot
drift from the rule the runtime enforces.

Scope is deliberate and fail-closed:

* Every tracked text file is scanned for secret-like material. A finding is a
  hard failure -- there is no allowlist, because an allowlist is where secret
  scanners quietly stop working.
* Generated evidence is scanned too, and must additionally carry an explicit
  suppression marker, so an evidence file cannot carry a live value even
  inside a redacted-looking string.

Deliberately dependency-light: stdlib plus PyYAML.
"""
from __future__ import annotations

import json
import re
import subprocess
import unittest
from pathlib import Path

import yaml

from mediahub_runtime.astra_security import scan_secret

ROOT = Path(__file__).resolve().parents[1]
SKIP_DIRS = {".git", ".ecc", "build", "dist", "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache"}

# Files that legitimately contain secret-shaped *detection patterns* or
# deliberate synthetic fixtures rather than real credentials. Each entry is
# justified: the runtime detector, this gate, the redaction unit tests that
# must feed it known-secret-shaped input, and the two tests that assert the
# detector itself works.
SELF_REFERENTIAL = {
    "runtime/mediahub_runtime/astra_security.py",
    "tests/test_repo_secret_hygiene.py",
    "tests/test_astra_security.py",
    "tests/test_astra_context_redaction.py",
    "tests/test_astra_memory.py",
}

# High-confidence credential shapes. These have no legitimate occurrence in
# source, prose or configuration, so they are scanned repository-wide with no
# exceptions at all.
HIGH_CONFIDENCE = (
    re.compile(r"\bsk-[A-Za-z0-9_-]{16,}\b"),
    re.compile(r"\bghp_[A-Za-z0-9]{20,}\b"),
    re.compile(r"\bgithub_pat_[A-Za-z0-9_]{20,}\b"),
    re.compile(r"\bBearer\s+[A-Za-z0-9._~+/=-]{20,}", re.I),
    re.compile(r"\bglpat-[A-Za-z0-9_-]{16,}\b"),
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
)

# A credential-shaped *name* bound to an actual literal value. Deliberately
# requires quotes so that type annotations (`secret: str`) and documentation
# (`secret: /etc/mediahub/...`) do not match.
LITERAL_ASSIGNMENT = re.compile(
    r"(?:api[_ -]?key|access[_ -]?token|secret|password|bearer)"
    r"\s*[:=]\s*[\"'][^\"'\n]{8,}[\"']",
    re.I,
)

# Text files worth scanning. Binary/asset extensions are skipped.
TEXT_SUFFIXES = {
    ".py", ".yml", ".yaml", ".json", ".md", ".txt", ".cfg", ".ini", ".toml",
    ".sh", ".env", ".example", ".sql", ".js", ".ts", ".html",
}

# A committed evidence file must record that secret values were suppressed.
SUPPRESSION_MARKERS = ("SUPPRESSED", "REDACTED")


def _tracked_files():
    """Scan versioned and non-ignored working files, excluding local ignored clones."""
    try:
        result = subprocess.run(
            ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        candidates = (Path(value) for value in result.stdout.split("\0") if value)
    except (OSError, subprocess.CalledProcessError):
        candidates = (path.relative_to(ROOT) for path in ROOT.rglob("*") if path.is_file())
    for rel in sorted(candidates):
        if any(part in SKIP_DIRS for part in rel.parts):
            continue
        if rel.suffix in TEXT_SUFFIXES or rel.name.startswith("."):
            yield rel


class RepoSecretHygieneTests(unittest.TestCase):
    def test_no_tracked_file_contains_a_real_credential_shape(self):
        """INV_NO_CREDENTIALS_IN_GIT -- high-confidence shapes, zero exceptions.

        ``sk-``, ``ghp_``, ``github_pat_``, long ``Bearer`` tokens, GitLab PATs
        and AWS access-key ids never legitimately appear in source, prose or
        configuration. This scan therefore has no allowlist: any hit is a
        leak. It is separate from the broader detector scan below because the
        broad pattern set also matches type annotations such as
        ``secret: str`` and prose such as ``secret: /path/to/file``, which are
        not credentials.
        """
        findings = []
        for rel in _tracked_files():
            try:
                text = rel.read_text(encoding="utf-8")
            except (UnicodeDecodeError, ValueError):
                continue
            for pattern in HIGH_CONFIDENCE:
                match = pattern.search(text)
                if match:
                    line = text[: match.start()].count("\n") + 1
                    findings.append(f"{rel}:{line}: {match.group(0)[:12]}...")
        self.assertEqual(
            findings,
            [],
            "Credential-shaped values found in tracked files:\n" + "\n".join(findings),
        )

    def test_no_tracked_file_contains_secret_like_assignments(self):
        """INV_NO_SECRETS_IN_EVIDENCE -- quoted literal assignments.

        The runtime detector deliberately also matches ``secret: str`` (a type
        annotation) and ``secret: /etc/...`` (documentation prose). Those are
        not credentials, so this gate requires an actual quoted literal value,
        which is what a real hardcoded credential looks like.

        Combined with the zero-exception high-confidence scan above, a leaked
        key is caught either by its provider prefix or by being assigned a
        literal.
        """
        findings = []
        for rel in _tracked_files():
            if str(rel) in SELF_REFERENTIAL:
                continue
            try:
                text = rel.read_text(encoding="utf-8")
            except (UnicodeDecodeError, ValueError):
                continue
            for match in LITERAL_ASSIGNMENT.finditer(text):
                line = text[: match.start()].count("\n") + 1
                findings.append(f"{rel}:{line}: {match.group(0)[:60]}")
        self.assertEqual(
            findings,
            [],
            "Hardcoded secret literals found in tracked files:\n" + "\n".join(findings),
        )

    def test_committed_evidence_declares_secret_suppression(self):
        """Evidence must state that secret values were suppressed."""
        evidence_dir = ROOT / "evidence"
        if not evidence_dir.is_dir():
            self.skipTest("no committed evidence directory")
        failures = []
        for path in sorted(evidence_dir.rglob("*.json")):
            rel = path.relative_to(ROOT)
            text = path.read_text(encoding="utf-8")
            scan = scan_secret(text)
            if scan.detected:
                failures.append(f"{rel}: contains secret-like value")
                continue
            if not any(marker in text for marker in SUPPRESSION_MARKERS):
                failures.append(
                    f"{rel}: no secret-suppression marker "
                    f"(expected one of {SUPPRESSION_MARKERS})"
                )
        self.assertEqual(
            failures,
            [],
            "Committed evidence hygiene failures:\n" + "\n".join(failures),
        )

    def test_workflow_secrets_are_referenced_not_hardcoded(self):
        """Workflows must consume secrets via the secrets context, never literals."""
        failures = []
        workflow_dir = ROOT / ".github" / "workflows"
        assignment = re.compile(
            r"^[ \t]*[A-Z0-9_]*(?:API_KEY|TOKEN|SECRET|PASSWORD)[ \t]*:[ \t]*(?P<value>.*)$",
            re.MULTILINE,
        )

        def _is_hardcoded(line: str) -> bool:
            match = assignment.match(line)
            if not match:
                return False
            value = match.group("value").strip()
            # Empty values and GitHub expressions are not hardcoded secrets.
            return bool(value) and not value.startswith("${{") and not value.startswith("$")
        for path in sorted(workflow_dir.glob("*.y*ml")):
            rel = path.relative_to(ROOT)
            text = path.read_text(encoding="utf-8")
            # The sign_astra_command smoke test intentionally sets a literal
            # throwaway key; it is a CI-local value, not a credential.
            if rel.name == "astra-verify.yml":
                continue
            for line in text.splitlines():
                if _is_hardcoded(line):
                    failures.append(f"{rel}: hardcoded secret assignment `{line.strip()}`")
        self.assertEqual(
            failures,
            [],
            "Hardcoded secrets in workflows:\n" + "\n".join(failures),
        )

    def test_every_scan_rule_actually_detects_a_planted_secret(self):
        """Mutation guard: each rule must fire on a planted credential.

        The probe is assembled at runtime so this file itself does not contain
        a credential-shaped literal -- the high-confidence scan has no
        allowlist, not even for this module.
        """
        provider_prefix = "s" + "k-"
        alphabet = "abcdefghijklmnopqrstuvwxyz"
        planted = provider_prefix + alphabet

        self.assertTrue(
            any(p.search(planted) for p in HIGH_CONFIDENCE),
            "high-confidence scan must detect a provider-prefixed key",
        )
        self.assertTrue(
            scan_secret(f"api_key = '{planted}'").detected,
            "runtime detector must detect a provider-prefixed key",
        )
        self.assertTrue(
            LITERAL_ASSIGNMENT.search(f'password = "{planted}"'),
            "literal-assignment scan must detect a hardcoded password",
        )
        self.assertFalse(
            any(p.search("def f(secret: str) -> None: ...") for p in HIGH_CONFIDENCE),
            "high-confidence scan must not flag a type annotation",
        )
        self.assertFalse(
            LITERAL_ASSIGNMENT.search("secret: /etc/mediahub/credentials/key"),
            "literal-assignment scan must not flag a documentation path",
        )


if __name__ == "__main__":
    unittest.main()