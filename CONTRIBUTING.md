# Contributing

Thanks for considering a contribution.

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
