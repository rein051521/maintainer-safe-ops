from __future__ import annotations

import json

from .scanner import ScanResult


def format_human(result: ScanResult) -> str:
    lines: list[str] = []
    lines.append("Maintainer Safe Ops")
    lines.append("===================")
    lines.append(f"checked_files: {result.checked_files}")
    lines.append(f"skipped_files: {result.skipped_files}")
    lines.append(f"status: {'OK' if result.ok else 'NG'}")

    if result.missing_files:
        lines.append("")
        lines.append("[Missing OSS readiness files]")
        for missing in result.missing_files:
            lines.append(f"- [{missing.severity}] {missing.file}: {missing.reason}")

    if result.findings:
        lines.append("")
        lines.append("[Findings]")
        for finding in result.findings:
            lines.append(
                f"- [{finding.severity}] {finding.rule_id} "
                f"{finding.file}:{finding.line} - {finding.message}"
            )
            lines.append(f"  ja: {finding.message_ja}")
            lines.append(f"  snippet: {finding.snippet}")

    if not result.findings and not result.missing_files:
        lines.append("")
        lines.append("No blocking maintainer-safety issues were detected.")

    return "\n".join(lines)


def format_json(result: ScanResult) -> str:
    return json.dumps(result.to_dict(), ensure_ascii=False, indent=2)
