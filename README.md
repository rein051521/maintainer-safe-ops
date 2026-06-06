# maintainer-safe-ops

[![CI](https://github.com/rein051521/maintainer-safe-ops/actions/workflows/ci.yml/badge.svg)](https://github.com/rein051521/maintainer-safe-ops/actions/workflows/ci.yml)
[![CodeQL](https://github.com/rein051521/maintainer-safe-ops/actions/workflows/codeql.yml/badge.svg)](https://github.com/rein051521/maintainer-safe-ops/actions/workflows/codeql.yml)
[![OpenSSF Scorecard](https://api.securityscorecards.dev/projects/github.com/rein051521/maintainer-safe-ops/badge)](https://securityscorecards.dev/viewer/?uri=github.com/rein051521/maintainer-safe-ops)
[![GitHub Marketplace](https://img.shields.io/badge/GitHub%20Marketplace-Maintainer%20Safe%20Ops-2ea44f?logo=github)](https://github.com/marketplace/actions/maintainer-safe-ops)

**maintainer-safe-ops** is a small CLI and GitHub Action for safer open-source maintainer workflows.

Available on the [GitHub Marketplace](https://github.com/marketplace/actions/maintainer-safe-ops).

It helps maintainers check a repository before publishing, merging, or releasing code by detecting:

- accidental `.env` exposure
- API-key-like strings and secret-looking assignments
- hardcoded private key blocks (PEM)
- risky commands such as `rm -rf /`
- force-push commands
- downloaded scripts piped into a shell (`curl ... | bash`)
- risky GitHub Actions patterns
- missing OSS readiness files such as `README.md`, `LICENSE`, `.gitignore`, `SECURITY.md`, and `CONTRIBUTING.md`
- optional SARIF output for security/code-scanning style workflows

The project is intentionally lightweight and dependency-free at runtime.

## 概要（日本語）

**maintainer-safe-ops** は、OSS のメンテナンス作業を少し安全にするための小さな CLI / GitHub Action です。

リポジトリを公開・マージ・リリースする前に、次のような項目を検出します。

- `.env` ファイルの誤公開
- API キーらしき文字列・秘密情報らしき代入
- `rm -rf /` などの危険なコマンド
- force push コマンド
- 危険な GitHub Actions のパターン
- `README.md` / `LICENSE` / `.gitignore` / `SECURITY.md` / `CONTRIBUTING.md` などの OSS 必須ファイルの欠如

ローカルでも CI でも実行でき、実行時の依存はありません。あくまで軽量な目安チェックであり、専用のシークレットスキャナや SAST の置き換えではありません。

## Why this exists

Open-source maintainers often handle repetitive safety checks:

- Is this repository safe to publish?
- Did a contributor accidentally include a token?
- Does a workflow grant write permissions in unsafe contexts?
- Are the basic OSS governance files present?
- Can release checks be automated without adding a large security platform?

This tool provides a practical baseline check that can run locally or in CI.

## Install from source

```bash
git clone https://github.com/rein051521/maintainer-safe-ops.git
cd maintainer-safe-ops
python -m venv .venv
```

Activate the virtual environment:

- **macOS / Linux:** `source .venv/bin/activate`
- **Windows (PowerShell):** `.venv\Scripts\Activate.ps1`
- **Windows (cmd):** `.venv\Scripts\activate.bat`

Then install:

```bash
pip install -e ".[dev]"
```

> PyPI distribution is planned. For now, install from source (above) or use the GitHub Action.

## CLI usage

```bash
maintainer-safe-ops .
```

JSON:

```bash
maintainer-safe-ops . --format json
```

SARIF:

```bash
maintainer-safe-ops . --format sarif > maintainer-safe-ops.sarif
```

Fail only on high severity findings:

```bash
maintainer-safe-ops . --fail-on high
```

## GitHub Action usage

```yaml
name: Maintainer Safe Ops

on:
  pull_request:
  push:
    branches: [main]

jobs:
  safe-ops:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v6
      - uses: rein051521/maintainer-safe-ops@v0.1.5
        with:
          path: "."
          format: "human"
          fail-on: "medium"
```

A ready-to-copy workflow is provided at
[examples/consumer-workflow.yml](examples/consumer-workflow.yml). The action runs
in a separate
[demo repository](https://github.com/rein051521/maintainer-safe-ops-demo) and is
self-tested in CI on every push and pull request — see
[docs/REAL_WORLD_USAGE.md](docs/REAL_WORLD_USAGE.md). Adopters are listed in
[ADOPTERS.md](ADOPTERS.md).

## Exit codes

| Code | Meaning |
|---:|---|
| 0 | No blocking issue detected |
| 1 | Blocking finding or missing required OSS file |
| 2 | Execution error |

## Severity model

| Severity | Meaning |
|---|---|
| high | Secret exposure or highly dangerous operation |
| medium | Risky maintainer operation that should be reviewed |
| low | OSS readiness or quality issue |

## Scope and limitations

This project is a safety baseline, not a complete security audit. It does not guarantee that a repository is free of secrets or vulnerabilities. Maintainers should still use dedicated scanners and manual review for high-risk projects.

### What it does not replace

maintainer-safe-ops complements, but does not replace, dedicated tools:

| Tool | Purpose | Relationship |
|---|---|---|
| gitleaks / TruffleHog | Deep secret scanning | Not a replacement — use them for thorough secret detection |
| CodeQL / Semgrep | Static analysis (SAST) | Not a replacement — use them for code vulnerability analysis |
| Dependabot / OSV | Dependency vulnerabilities | Not a replacement — use them for dependency alerts |

Instead, it provides a fast, dependency-free **pre-publish / pre-merge / pre-release** checklist that a maintainer can run locally or in CI to catch obvious mistakes (a committed `.env`, a `rm -rf /`, a risky `pull_request_target` workflow, or missing OSS readiness files) before they reach a release.

## Roadmap

- More GitHub Actions workflow rules
- Config file support
- allowlist support for false positives
- stronger SARIF compatibility
- PyPI distribution (planned for v0.2)
- npm package and pre-commit hook examples
- Japanese documentation expansion

## Development

```bash
pip install -e ".[dev]"
pytest
ruff check .
```

## Feedback

This is an early release and feedback is very welcome — especially false positives,
risky patterns it missed, rules you wish it had, and setup or adoption friction.

- Share quick feedback in the [Feedback discussion (#19)](https://github.com/rein051521/maintainer-safe-ops/discussions/19)
- Or comment on the [feedback tracking issue (#24)](https://github.com/rein051521/maintainer-safe-ops/issues/24)

Rough notes are fine; no praise needed.

### フィードバック（日本語）

初期版です。誤検知・拾えていない危険パターン・追加してほしいルール・導入時の詰まりなど、
辛口のフィードバックを歓迎します。

- 気軽な意見は [フィードバック用 Discussion (#19)](https://github.com/rein051521/maintainer-safe-ops/discussions/19) へ
- まとめての報告は [フィードバック用 Issue (#24)](https://github.com/rein051521/maintainer-safe-ops/issues/24) へ

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## Security

See [SECURITY.md](SECURITY.md).

## License

MIT


## Maintainer safety posture

This repository includes:

- CI for Python 3.10, 3.11, and 3.12
- CodeQL workflow
- OpenSSF Scorecard workflow
- Dependabot configuration
- release-check workflow
- issue template
- pull request template
- security policy
- contribution guide
- roadmap
- changelog

These files are included to make the project easier to review, maintain, and improve as an open-source maintainer tool.


Additional project-health files:

- `GOVERNANCE.md`
- `SUPPORT.md`
- `CITATION.cff`
- `.github/CODEOWNERS`
- `docs/HEALTH_METRICS.md`
- `docs/90_DAY_MAINTENANCE_PLAN.md`


## Configuration

By default, maintainer-safe-ops reads `.maintainer-safe-ops.json` if it exists.

Example:

```json
{
  "exclude": [
    "tests/**",
    "examples/risky-project/**"
  ]
}
```

This is useful when a repository intentionally contains risky strings in tests or documentation fixtures.
