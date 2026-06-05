from __future__ import annotations

import json
from pathlib import Path

from maintainer_safe_ops import __version__
from maintainer_safe_ops.sarif import format_sarif
from maintainer_safe_ops.scanner import scan_repository


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def test_sarif_output_is_valid_json(tmp_path: Path) -> None:
    write(tmp_path / ".env", "SECRET=abcdef123456\n")

    result = scan_repository(tmp_path)
    sarif = json.loads(format_sarif(result))

    assert sarif["version"] == "2.1.0"
    driver = sarif["runs"][0]["tool"]["driver"]
    assert driver["name"] == "maintainer-safe-ops"
    assert driver["version"] == __version__
    assert sarif["runs"][0]["results"]
