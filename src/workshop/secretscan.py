"""Lightweight secret scan for CI. It looks for common token shapes, not entropy."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

SKIP_DIRS = {
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    "dist",
    "build",
    "htmlcov",
    ".egg",
}

PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("aws_access_key", re.compile(r"AKIA[0-9A-Z]{16}")),
    ("private_key", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----")),
    ("github_token", re.compile(r"ghp_[A-Za-z0-9]{20,}")),
    ("github_pat", re.compile(r"github_pat_[A-Za-z0-9_]{20,}")),
    ("slack_token", re.compile(r"xox[baprs]-[A-Za-z0-9-]{10,}")),
    ("vendor_secret_key", re.compile(r"sk-(?:live|proj|ant)-[A-Za-z0-9]{10,}")),
    (
        "assigned_secret",
        re.compile(r"(?i)(?:api[_-]?key|secret|token)\s*[:=]\s*['\"][A-Za-z0-9_+\/=-]{20,}['\"]"),
    ),
)

MAX_BYTES = 1_000_000


@dataclass(frozen=True)
class Finding:
    path: str
    line: int
    rule: str


def _iter_files(root: Path) -> list[Path]:
    if root.is_file():
        return [root]
    found: list[Path] = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.suffix in {".png", ".jpg", ".jpeg", ".gif", ".webp", ".pyc"}:
            continue
        found.append(path)
    return found


def scan_text(text: str, *, path: str = "<memory>") -> list[Finding]:
    findings: list[Finding] = []
    for number, line in enumerate(text.splitlines(), start=1):
        if "secretscan: allow" in line:
            continue
        for name, pattern in PATTERNS:
            if pattern.search(line):
                findings.append(Finding(path=path, line=number, rule=name))
    return findings


def scan_path(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    for path in _iter_files(root):
        try:
            size = path.stat().st_size
        except OSError:
            continue
        if size > MAX_BYTES:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        findings.extend(scan_text(text, path=str(path)))
    return findings
