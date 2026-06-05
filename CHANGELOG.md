# Changelog

## 0.1.1 - 2026-06-05

Fixed:

- Composite GitHub Action now installs its own package using `${{ github.action_path }}`,
  so `uses: rein051521/maintainer-safe-ops@v0.1.1` works from consumer repositories
  instead of trying to install the caller's checkout.

Changed:

- Self-scan configuration (`.maintainer-safe-ops.json`) excludes the rule
  definition file to avoid self-referential matches.

## 0.1.0 - 2026-06-05

Initial release.

Added:

- CLI scanner
- human, JSON, and SARIF output
- secret-looking pattern detection
- dangerous command detection
- GitHub Actions risk detection
- OSS readiness file checks
- GitHub Action wrapper
- test suite
