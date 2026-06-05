from __future__ import annotations

import json
from pathlib import Path

from maintainer_safe_ops.cli import main


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def add_basic_files(root: Path) -> None:
    write(root / "README.md", "# Test\n")
    write(root / "LICENSE", "MIT\n")
    write(root / ".gitignore", ".env\n")
    write(root / "SECURITY.md", "# Security\n")
    write(root / "CONTRIBUTING.md", "# Contributing\n")


def test_cli_json_output(tmp_path: Path, monkeypatch, capsys) -> None:
    add_basic_files(tmp_path)
    monkeypatch.setattr("sys.argv", ["maintainer-safe-ops", str(tmp_path), "--format", "json"])

    code = main()
    output = capsys.readouterr().out
    payload = json.loads(output)

    assert code == 0
    assert payload["ok"] is True


def test_cli_returns_one_on_blocking_finding(tmp_path: Path, monkeypatch) -> None:
    add_basic_files(tmp_path)
    write(tmp_path / ".env", "SECRET=abcdef123456\n")
    monkeypatch.setattr("sys.argv", ["maintainer-safe-ops", str(tmp_path)])

    code = main()

    assert code == 1


def test_cli_returns_two_on_bad_path(monkeypatch) -> None:
    monkeypatch.setattr("sys.argv", ["maintainer-safe-ops", "/does/not/exist"])

    code = main()

    assert code == 2
