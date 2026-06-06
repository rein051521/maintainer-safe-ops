# Real-world usage

## Used in a separate repository

A dedicated demonstration repository consumes this action from a different
repository (not the tool's own repo), proving cross-repository usage on
GitHub-hosted runners:

- Demo repository: <https://github.com/rein051521/maintainer-safe-ops-demo>
- Successful workflow run (warning-free): <https://github.com/rein051521/maintainer-safe-ops-demo/actions/runs/27055339304>

(This is a maintainer-owned demonstration consumer, not a third-party adopter.)

## Self-dogfooding in CI

This repository runs its own GitHub Action on every push and pull request.
The `action-selftest` job in [`.github/workflows/ci.yml`](../.github/workflows/ci.yml)
invokes the composite action with `uses: ./` against the bundled
`examples/clean-project` fixture and fails the build if the action cannot
install or run:

```yaml
action-selftest:
  name: GitHub Action self-test
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v6
    - uses: ./
      with:
        path: "examples/clean-project"
        fail-on: "high"
```

This proves end-to-end, on real GitHub-hosted runners, that:

- the published composite action installs from `github.action_path`,
- the `maintainer-safe-ops` CLI is available and runs,
- a clean project passes with no high-severity findings.

You can see the live runs here:

- CI workflow runs: <https://github.com/rein051521/maintainer-safe-ops/actions/workflows/ci.yml>
- Release-gate self scan: <https://github.com/rein051521/maintainer-safe-ops/actions/workflows/release-check.yml>

## Using it in your own repository

Add the action to any repository's workflow:

```yaml
- uses: actions/checkout@v6
- uses: rein051521/maintainer-safe-ops@v0.1.4
  with:
    path: "."
    fail-on: "medium"
```

Or run the CLI locally before a release:

```bash
pip install -e ".[dev]"   # from a clone
maintainer-safe-ops . --fail-on high
```

> If you adopt maintainer-safe-ops in a public project, an issue or PR linking
> to your workflow run is welcome — real usage reports help prioritize rules.
