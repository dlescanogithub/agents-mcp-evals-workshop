"""Token-shape scanner. Positives are built at runtime so the tree stays clean."""

from __future__ import annotations

import hashlib
import re
from pathlib import Path

from workshop.secretscan import PATTERNS, scan_path, scan_text

ROOT = Path(__file__).resolve().parents[1]
RULES = {name for name, _pattern in PATTERNS}


def _piece(*parts: str) -> str:
    return "".join(parts)


def test_pattern_ids_are_the_aligned_list() -> None:
    assert {
        "xai_prefix",
        "sk_prefix",
        "sk_ant_prefix",
        "sk_underscore_prefix",
        "github_token",
        "github_pat",
        "aws_access_key",
        "bearer_token",
        "private_key",
    } == RULES


def test_each_shape_is_flagged_and_short_forms_are_not() -> None:
    samples = (
        ("xai_prefix", _piece("xai-", "a" * 20), _piece("xai-", "a" * 19)),
        ("sk_prefix", _piece("sk-", "b" * 20), _piece("sk-", "b" * 19)),
        ("sk_prefix", _piece("sk-proj-", "c" * 20), _piece("sk-proj-", "c" * 19)),
        ("sk_ant_prefix", _piece("sk-ant-", "d" * 20), _piece("sk-ant-", "d" * 19)),
        ("sk_underscore_prefix", _piece("sk_", "e" * 20), _piece("sk_", "e" * 19)),
        ("github_token", _piece("ghp_", "f" * 20), _piece("ghp_", "f" * 19)),
        ("github_pat", _piece("github_pat_", "g" * 20), _piece("github_pat_", "g" * 19)),
        ("aws_access_key", _piece("AKIA", "H" * 16), _piece("AKIA", "H" * 15)),
        ("bearer_token", _piece("Bearer ", "i" * 20), _piece("Bearer ", "i" * 19)),
        ("private_key", _piece("-----BEGIN ", "PRIVATE KEY-----"), "-----BEGIN PUBLIC KEY-----"),
    )
    for rule, positive, negative in samples:
        found = {item.rule for item in scan_text(positive)}
        assert rule in found
        assert {item.rule for item in scan_text(negative)} == set()
    rsa_header = _piece("-----BEGIN ", "RSA ", "PRIVATE KEY-----")
    ec_header = _piece("-----BEGIN ", "EC ", "PRIVATE KEY-----")
    ssh_header = _piece("-----BEGIN ", "OPENSSH ", "PRIVATE KEY-----")
    assert "private_key" in {item.rule for item in scan_text(rsa_header)}
    assert "private_key" in {item.rule for item in scan_text(ec_header)}
    assert "private_key" in {item.rule for item in scan_text(ssh_header)}


def test_sk_ant_shape_does_not_use_the_plain_sk_rule() -> None:
    sample = _piece("sk-ant-", "d" * 20)
    rules = {item.rule for item in scan_text(sample)}
    assert rules == {"sk_ant_prefix"}


def test_url_safe_tail_and_allow_comment(tmp_path: Path) -> None:
    sample = _piece("xai-", "abc_", "def-ghij", "KLMNOPQR")
    assert "xai_prefix" in {item.rule for item in scan_text(sample)}
    allowed = scan_text(sample + "  # secretscan: allow")
    assert allowed == []
    marker = _piece("-----BEGIN ", "PRIVATE KEY-----") + "\n"
    path = tmp_path / "sample.txt"
    path.write_text(marker, encoding="utf-8")
    assert scan_path(path)[0].rule == "private_key"
    binary = tmp_path / "skip.png"
    binary.write_bytes(b"\xff\xd8not-text")
    assert scan_path(binary) == []
    huge = tmp_path / "huge.txt"
    huge.write_bytes(b"a" * 1_000_001)
    assert scan_path(huge) == []
    raw = tmp_path / "raw.bin"
    raw.write_bytes(b"\xff\xfe")
    assert scan_path(raw) == []
    nested = tmp_path / "__pycache__" / "hidden.py"
    nested.parent.mkdir()
    nested.write_text(_piece("ghp_", "z" * 20), encoding="utf-8")
    assert scan_path(tmp_path / "__pycache__") == []


def test_repo_tree_has_no_secret_findings() -> None:
    assert scan_path(ROOT) == []


def test_secretscan_sha256_matches_provenance() -> None:
    digest = hashlib.sha256((ROOT / "src/workshop/secretscan.py").read_bytes()).hexdigest()
    text = (ROOT / "docs/PROVENANCE.md").read_text(encoding="utf-8")
    match = re.search(r"sha256: ([0-9a-f]{64})", text)
    assert match is not None
    assert match.group(1) == digest
