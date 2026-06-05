from __future__ import annotations

from pathlib import Path

import pytest

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


def test_clean_repository_is_ok(tmp_path: Path) -> None:
    add_basic_files(tmp_path)
    write(tmp_path / "src" / "main.py", "print('hello')\n")

    result = scan_repository(tmp_path)

    assert result.ok is True
    assert result.findings == []
    assert result.missing_files == []


def test_detects_env_file(tmp_path: Path) -> None:
    add_basic_files(tmp_path)
    write(tmp_path / ".env", "OPENAI_API_KEY=sk-testtesttesttesttesttest\n")

    result = scan_repository(tmp_path)

    assert result.ok is False
    assert any(f.rule_id == "MSO000_ENV_FILE" for f in result.findings)


def test_detects_openai_key_like_string(tmp_path: Path) -> None:
    add_basic_files(tmp_path)
    write(tmp_path / "config.py", "KEY='sk-abcdefghijklmnopqrstuvwxyz123456'\n")

    result = scan_repository(tmp_path)

    assert result.ok is False
    assert any(f.rule_id == "MSO001_OPENAI_KEY" for f in result.findings)


def test_detects_secret_assignment(tmp_path: Path) -> None:
    add_basic_files(tmp_path)
    write(tmp_path / "config.toml", "github_token = 'abcdef1234567890'\n")

    result = scan_repository(tmp_path)

    assert result.ok is False
    assert any(f.rule_id == "MSO002_SECRET_ASSIGNMENT" for f in result.findings)


def test_detects_dangerous_rm_rf(tmp_path: Path) -> None:
    add_basic_files(tmp_path)
    write(tmp_path / "script.sh", "rm -rf /\n")

    result = scan_repository(tmp_path)

    assert result.ok is False
    assert any(f.rule_id == "MSO004_RM_RF_ROOT" for f in result.findings)


def test_detects_force_push(tmp_path: Path) -> None:
    add_basic_files(tmp_path)
    write(tmp_path / "memo.md", "git push --force origin main\n")

    result = scan_repository(tmp_path)

    assert result.ok is False
    assert any(f.rule_id == "MSO005_FORCE_PUSH" for f in result.findings)


def test_detects_pull_request_target_write(tmp_path: Path) -> None:
    add_basic_files(tmp_path)
    write(
        tmp_path / ".github" / "workflows" / "danger.yml",
        "on: pull_request_target\npermissions:\n  contents: write\n",
    )

    result = scan_repository(tmp_path)

    assert result.ok is False
    assert any(f.rule_id == "MSO007_PULL_REQUEST_TARGET_WRITE" for f in result.findings)


def test_missing_recommended_files(tmp_path: Path) -> None:
    write(tmp_path / "main.py", "print('hello')\n")

    result = scan_repository(tmp_path)

    missing = {m.file for m in result.missing_files}
    assert result.ok is False
    assert {"README.md", "LICENSE", ".gitignore", "SECURITY.md", "CONTRIBUTING.md"} <= missing


def test_ignores_node_modules(tmp_path: Path) -> None:
    add_basic_files(tmp_path)
    write(tmp_path / "node_modules" / "bad.js", "const key='sk-abcdefghijklmnopqrstuvwxyz123456'\n")

    result = scan_repository(tmp_path)

    assert result.ok is True
    assert result.findings == []


def test_fail_on_none_does_not_block(tmp_path: Path) -> None:
    write(tmp_path / ".env", "SECRET=abcdef123456\n")

    result = scan_repository(tmp_path, fail_on="none")

    assert result.ok is True
    assert result.findings


def test_invalid_path_raises() -> None:
    with pytest.raises(FileNotFoundError):
        scan_repository("/path/that/does/not/exist")


def test_config_excludes_fixture_files(tmp_path: Path) -> None:
    add_basic_files(tmp_path)
    write(tmp_path / ".maintainer-safe-ops.json", '{"exclude": ["tests/**"]}')
    write(tmp_path / "tests" / "fixture.py", "danger = 'sk-abcdefghijklmnopqrstuvwxyz123456'\n")

    result = scan_repository(tmp_path)

    assert result.ok is True
    assert result.findings == []
