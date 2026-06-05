from __future__ import annotations

import argparse
import sys

from .formatters import format_human, format_json
from .sarif import format_sarif
from .scanner import scan_repository


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="maintainer-safe-ops",
        description=(
            "Check repositories for maintainer-safety risks "
            "before publish, merge, or release."
        ),
    )
    parser.add_argument("path", nargs="?", default=".", help="Repository path to scan.")
    parser.add_argument(
        "--format",
        choices=["human", "json", "sarif"],
        default="human",
        help="Output format.",
    )
    parser.add_argument(
        "--config",
        default=None,
        help="Optional JSON config file. Defaults to .maintainer-safe-ops.json if present.",
    )
    parser.add_argument(
        "--fail-on",
        choices=["high", "medium", "low", "none"],
        default="medium",
        help="Minimum severity that causes exit code 1.",
    )

    args = parser.parse_args()

    try:
        result = scan_repository(args.path, fail_on=args.fail_on, config_path=args.config)
    except Exception as exc:
        print(f"[ERROR] {exc}", file=sys.stderr)
        return 2

    if args.format == "json":
        print(format_json(result))
    elif args.format == "sarif":
        print(format_sarif(result))
    else:
        print(format_human(result))

    return 0 if result.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
