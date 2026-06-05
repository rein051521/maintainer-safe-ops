from __future__ import annotations

import json
from typing import Any

from .scanner import ScanResult


def format_sarif(result: ScanResult) -> str:
    rules: dict[str, dict[str, Any]] = {}

    sarif_results: list[dict[str, Any]] = []

    for finding in result.findings:
        rules[finding.rule_id] = {
            "id": finding.rule_id,
            "name": finding.rule_id,
            "shortDescription": {"text": finding.message},
            "fullDescription": {"text": finding.message_ja},
            "helpUri": finding.help_uri,
            "properties": {"severity": finding.severity},
        }

        sarif_results.append(
            {
                "ruleId": finding.rule_id,
                "level": _sarif_level(finding.severity),
                "message": {"text": f"{finding.message} / {finding.message_ja}"},
                "locations": [
                    {
                        "physicalLocation": {
                            "artifactLocation": {"uri": finding.file},
                            "region": {"startLine": finding.line},
                        }
                    }
                ],
                "properties": {"snippet": finding.snippet},
            }
        )

    for missing in result.missing_files:
        rule_id = f"MSO_READINESS_{missing.file.replace('.', '_').upper()}"
        rules[rule_id] = {
            "id": rule_id,
            "name": rule_id,
            "shortDescription": {"text": f"Missing {missing.file}"},
            "fullDescription": {"text": missing.reason},
            "properties": {"severity": missing.severity},
        }
        sarif_results.append(
            {
                "ruleId": rule_id,
                "level": _sarif_level(missing.severity),
                "message": {"text": f"Missing {missing.file}: {missing.reason}"},
                "locations": [
                    {
                        "physicalLocation": {
                            "artifactLocation": {"uri": missing.file},
                            "region": {"startLine": 1},
                        }
                    }
                ],
            }
        )

    sarif = {
        "$schema": "https://json.schemastore.org/sarif-2.1.0.json",
        "version": "2.1.0",
        "runs": [
            {
                "tool": {
                    "driver": {
                        "name": "maintainer-safe-ops",
                        "informationUri": "https://github.com/rein051521/maintainer-safe-ops",
                        "rules": list(rules.values()),
                    }
                },
                "results": sarif_results,
            }
        ],
    }

    return json.dumps(sarif, ensure_ascii=False, indent=2)


def _sarif_level(severity: str) -> str:
    if severity == "high":
        return "error"
    if severity == "medium":
        return "warning"
    return "note"
