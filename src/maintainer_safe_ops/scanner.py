from __future__ import annotations

import fnmatch
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from .rules import RULES

EXCLUDED_DIRS = {
    ".git",
    ".venv",
    "venv",
    "node_modules",
    "dist",
    "build",
    "__pycache__",
    ".pytest_cache",
    ".ruff_cache",
    ".mypy_cache",
}

TEXT_EXTENSIONS = {
    ".py",
    ".js",
    ".ts",
    ".tsx",
    ".jsx",
    ".json",
    ".yaml",
    ".yml",
    ".toml",
    ".md",
    ".txt",
    ".env",
    ".example",
    ".sh",
    ".ps1",
    ".bat",
    ".ini",
    ".cfg",
}


RECOMMENDED_FILES = {
    "README.md": "Project purpose and usage",
    "LICENSE": "Open-source license",
    ".gitignore": "Prevents accidental local file commits",
    "SECURITY.md": "Security reporting policy",
    "CONTRIBUTING.md": "Contribution workflow",
}


@dataclass(frozen=True)
class Finding:
    rule_id: str
    severity: str
    file: str
    line: int
    message: str
    message_ja: str
    snippet: str
    help_uri: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class MissingFile:
    file: str
    reason: str
    severity: str = "medium"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ScanResult:
    ok: bool
    findings: list[Finding]
    missing_files: list[MissingFile]
    checked_files: int
    skipped_files: int

    def to_dict(self) -> dict[str, Any]:
        return {
            "ok": self.ok,
            "checked_files": self.checked_files,
            "skipped_files": self.skipped_files,
            "findings": [finding.to_dict() for finding in self.findings],
            "missing_files": [missing.to_dict() for missing in self.missing_files],
        }


def scan_repository(
    root: str | Path, fail_on: str = "medium", config_path: str | Path | None = None
) -> ScanResult:
    root_path = Path(root).resolve()

    if not root_path.exists():
        raise FileNotFoundError(f"Target path does not exist: {root_path}")
    if not root_path.is_dir():
        raise NotADirectoryError(f"Target path is not a directory: {root_path}")

    config = _load_config(root_path, config_path)
    exclude_globs = set(config.get("exclude", []))

    findings: list[Finding] = []
    checked_files = 0
    skipped_files = 0

    for path in root_path.rglob("*"):
        if path.is_dir():
            continue
        if _is_excluded(path, root_path) or _matches_exclude_globs(path, root_path, exclude_globs):
            skipped_files += 1
            continue
        if not _looks_like_text_file(path):
            skipped_files += 1
            continue

        checked_files += 1
        findings.extend(_scan_file(path, root_path))

    missing_files = _missing_recommended_files(root_path)
    ok = not _has_blocking_issue(findings, missing_files, fail_on)

    return ScanResult(
        ok=ok,
        findings=findings,
        missing_files=missing_files,
        checked_files=checked_files,
        skipped_files=skipped_files,
    )


def _scan_file(path: Path, root: Path) -> list[Finding]:
    findings: list[Finding] = []

    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        try:
            text = path.read_text(encoding="cp932")
        except UnicodeDecodeError:
            return findings

    relative = str(path.relative_to(root)).replace("\\", "/")

    if path.name.startswith(".env") and not path.name.endswith(".example"):
        findings.append(
            Finding(
                rule_id="MSO000_ENV_FILE",
                severity="high",
                file=relative,
                line=1,
                message=".env file is included in the repository.",
                message_ja=".env ファイルが公開対象に含まれています。",
                snippet=path.name,
                help_uri="https://docs.github.com/code-security/secret-scanning",
            )
        )

    for rule in RULES:
        if path.suffix.lower() in {".yml", ".yaml"}:
            # Some workflow risks need multi-line context.
            for match in rule.pattern.finditer(text):
                line_no = text[: match.start()].count("\n") + 1
                findings.append(
                    Finding(
                        rule_id=rule.id,
                        severity=rule.severity,
                        file=relative,
                        line=line_no,
                        message=rule.message,
                        message_ja=rule.message_ja,
                        snippet=_mask_snippet(match.group(0).strip()),
                        help_uri=rule.help_uri,
                    )
                )

        for line_no, line in enumerate(text.splitlines(), start=1):
            if rule.pattern.search(line):
                findings.append(
                    Finding(
                        rule_id=rule.id,
                        severity=rule.severity,
                        file=relative,
                        line=line_no,
                        message=rule.message,
                        message_ja=rule.message_ja,
                        snippet=_mask_snippet(line.strip()),
                        help_uri=rule.help_uri,
                    )
                )

    return _dedupe_findings(findings)


def _is_excluded(path: Path, root: Path) -> bool:
    return any(part in EXCLUDED_DIRS for part in path.relative_to(root).parts)


def _looks_like_text_file(path: Path) -> bool:
    if path.name in {"Dockerfile", "Makefile"}:
        return True
    if path.name.startswith(".env"):
        return True
    return path.suffix.lower() in TEXT_EXTENSIONS


def _missing_recommended_files(root: Path) -> list[MissingFile]:
    return [
        MissingFile(file=name, reason=reason)
        for name, reason in RECOMMENDED_FILES.items()
        if not (root / name).exists()
    ]


def _severity_rank(severity: str) -> int:
    order = {"none": 99, "low": 1, "medium": 2, "high": 3}
    return order.get(severity, 2)


def _has_blocking_issue(
    findings: list[Finding],
    missing_files: list[MissingFile],
    fail_on: str,
) -> bool:
    if fail_on == "none":
        return False

    threshold = _severity_rank(fail_on)
    return any(_severity_rank(f.severity) >= threshold for f in findings) or any(
        _severity_rank(m.severity) >= threshold for m in missing_files
    )


def _mask_snippet(text: str) -> str:
    if len(text) <= 24:
        return text
    return text[:12] + "...[masked]..." + text[-6:]


def _dedupe_findings(findings: list[Finding]) -> list[Finding]:
    seen: set[tuple[str, str, int, str]] = set()
    deduped: list[Finding] = []

    for finding in findings:
        key = (finding.rule_id, finding.file, finding.line, finding.snippet)
        if key in seen:
            continue
        seen.add(key)
        deduped.append(finding)

    return deduped


def _load_config(root: Path, config_path: str | Path | None) -> dict[str, list[str]]:
    candidate = root / ".maintainer-safe-ops.json" if config_path is None else Path(config_path)

    if not candidate.exists():
        return {"exclude": []}

    try:
        payload = json.loads(candidate.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid config JSON: {candidate}") from exc

    exclude = payload.get("exclude", [])
    if not isinstance(exclude, list) or not all(isinstance(item, str) for item in exclude):
        raise ValueError("Config field 'exclude' must be a list of strings.")

    return {"exclude": exclude}


def _matches_exclude_globs(path: Path, root: Path, exclude_globs: set[str]) -> bool:
    relative = str(path.relative_to(root)).replace("\\", "/")
    return any(fnmatch.fnmatch(relative, pattern) for pattern in exclude_globs)
