from __future__ import annotations

from pathlib import Path

import pytest

from maintainer_safe_ops.scanner import scan_repository


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def test_invalid_config_json_raises(tmp_path: Path) -> None:
    write(tmp_path / ".maintainer-safe-ops.json", "{ not valid json")

    with pytest.raises(ValueError):
        scan_repository(tmp_path)


def test_exclude_must_be_list_of_strings(tmp_path: Path) -> None:
    write(tmp_path / ".maintainer-safe-ops.json", '{"exclude": "tests/**"}')

    with pytest.raises(ValueError):
        scan_repository(tmp_path)


def test_explicit_config_path_is_used(tmp_path: Path) -> None:
    write(tmp_path / "README.md", "# Test\n")
    write(tmp_path / "LICENSE", "MIT\n")
    write(tmp_path / ".gitignore", ".env\n")
    write(tmp_path / "SECURITY.md", "# Security\n")
    write(tmp_path / "CONTRIBUTING.md", "# Contributing\n")
    write(tmp_path / "danger" / "memo.md", "git push --force origin main\n")
    write(tmp_path / "custom-config.json", '{"exclude": ["danger/**"]}')

    result = scan_repository(tmp_path, config_path=tmp_path / "custom-config.json")

    assert result.ok is True
    assert result.findings == []
