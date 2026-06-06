# Contributing

Thanks for considering a contribution.

## Feedback

Not ready to open a pull request? Feedback is just as valuable, especially in this
early stage:

- Quick thoughts and questions: [Feedback discussion (#19)](https://github.com/rein051521/maintainer-safe-ops/discussions/19)
- False positives, missed risks, or setup friction: [feedback tracking issue (#24)](https://github.com/rein051521/maintainer-safe-ops/issues/24)

Blunt, rough notes are welcome — no praise needed.

## Good first contributions

- Add a detection rule with tests
- Improve English or Japanese messages
- Improve SARIF output
- Add GitHub Actions workflow risk examples
- Improve documentation

## Development setup

```bash
python -m venv .venv
# Activate: source .venv/bin/activate (macOS/Linux)
#           .venv\Scripts\Activate.ps1 (Windows PowerShell)
pip install -e ".[dev]"
pytest
ruff check .
```

## Pull request checklist

Before opening a pull request:

- [ ] Add or update tests
- [ ] Run `pytest`
- [ ] Run `ruff check .`
- [ ] Update README or CHANGELOG if behavior changes
- [ ] Do not include real secrets in examples or tests

## Rule design principles

Rules should be:

- easy to understand
- low dependency
- tested with realistic examples
- careful about false positives
- useful for maintainers before publish, merge, or release
