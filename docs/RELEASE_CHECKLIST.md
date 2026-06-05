# Release Checklist

## Before tagging

- [ ] CI is green
- [ ] CodeQL has no blocking alerts
- [ ] Dependabot alerts reviewed
- [ ] OpenSSF Scorecard result reviewed
- [ ] `pytest` passes locally
- [ ] `ruff check .` passes locally
- [ ] `maintainer-safe-ops . --fail-on high` passes locally
- [ ] CHANGELOG updated
- [ ] README usage still accurate

## Tag

```bash
git tag v0.1.0
git push origin v0.1.0
```

## Release notes

Summarize the changes for the tag from `CHANGELOG.md`, then publish with
`gh release create v0.1.0 --title "v0.1.0" --notes "<summary>"`.
