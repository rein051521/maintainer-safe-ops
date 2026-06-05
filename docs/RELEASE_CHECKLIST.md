# Release Checklist

## Before publishing

- [ ] No internal, private, or strategy notes are included in the public tree
- [ ] `examples/**` fixtures contain only placeholder values (no real keys or tokens)
- [ ] `.env.example` uses placeholder values only
- [ ] LICENSE, README, SECURITY, CONTRIBUTING are present
- [ ] `maintainer-safe-ops .` reports no high-severity findings

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
git tag vX.Y.Z
git push origin vX.Y.Z
```

## Release notes

Summarize the changes for the tag from `CHANGELOG.md`, then publish with
`gh release create vX.Y.Z --title "vX.Y.Z" --notes "<summary>"`.
