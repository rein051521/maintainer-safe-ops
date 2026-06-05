from __future__ import annotations

import json
from pathlib import Path

from maintainer_safe_ops.formatters import format_human, format_json
from maintainer_safe_ops.scanner import scan_repository


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def add_basic_files(root: Path) -> None:
    write(root / "README.md", "# Test\n")
    write(root / "LICENSE", "MIT\n")
    write(root / ".gitignore", ".env\n")
    write(root / "SECURITY.md", "# Security\n")
    write(root / "CONTRIBUTING.md", "# Contributing\n")


def test_format_human_clean_repository(tmp_path: Path) -> None:
    add_basic_files(tmp_path)
    write(tmp_path / "main.py", "print('hello')\n")

    out = format_human(scan_repository(tmp_path))

    assert "status: OK" in out
    assert "No blocking maintainer-safety issues were detected." in out


def test_format_human_reports_findings(tmp_path: Path) -> None:
    add_basic_files(tmp_path)
    write(tmp_path / "memo.md", "git push --force origin main\n")

    out = format_human(scan_repository(tmp_path))

    assert "status: NG" in out
    assert "[Findings]" in out
    assert "MSO005_FORCE_PUSH" in out


def test_format_json_structure(tmp_path: Path) -> None:
    add_basic_files(tmp_path)

    payload = json.loads(format_json(scan_repository(tmp_path)))

    assert payload["ok"] is True
    assert payload["findings"] == []
    assert "missing_files" in payload
    assert "checked_files" in payload
    assert "skipped_files" in payload
