# Changelog

## 0.1.3 - 2026-06-06

Added:

- New rule `MSO009_CURL_PIPE_SHELL`: flags downloaded scripts piped directly into
  a shell (e.g. `curl ... | bash`), a common supply-chain risk. Includes positive
  and false-positive-guard tests.

## 0.1.2 - 2026-06-05

Added:

- `docs/REAL_WORLD_USAGE.md` documenting the CI self-test (dogfooding) of the action.
- README "What it does not replace" comparison (gitleaks / CodeQL / Dependabot).
- GitHub Action `branding` (icon and color) for Marketplace listing.

Fixed:

- README and CONTRIBUTING virtual-environment activation steps now render correctly
  across operating systems.

Changed:

- Pin the action's internal `setup-python` step by commit SHA.

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
