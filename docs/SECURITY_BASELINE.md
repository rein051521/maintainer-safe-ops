# Security Baseline

This project follows a lightweight maintainer-focused security baseline.

## Repository controls

Recommended GitHub settings after publishing:

- Enable branch protection for `main`
- Require pull request before merging
- Require status checks before merging
- Require CodeQL to pass when available
- Enable Dependabot alerts
- Enable Dependabot security updates
- Enable secret scanning alerts when available
- Enable private vulnerability reporting if available

## GitHub Actions controls

Implemented in this repository:

- default workflow permissions are minimized with explicit `permissions`
- CI uses `contents: read`
- CodeQL uses only `contents: read` and `security-events: write`
- Scorecard uses `contents: read`, `security-events: write`, and `id-token: write`
- release check runs tests, lint, and self-scan

## Maintainer behavior

Before release:

- run `pytest`
- run `ruff check .`
- run `maintainer-safe-ops . --fail-on high`
- verify no real secrets exist in examples or tests
- check open issues for release blockers
