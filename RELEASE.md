# Release Guide

Releases for this collection are automated via `.github/workflows/release.yml`.

## How It Works

When a PR is merged to `main` with a conventional commit title:

1. The release workflow runs (`Release Collection`)
2. It bumps the collection version in `galaxy.yml`
3. Builds and publishes the collection to Ansible Galaxy
4. Builds the execution environment image and pushes it to GHCR
5. Creates a GitHub Release with artifacts and release notes

## Conventional Commit → Release Type

| Commit type | Result |
|-------------|--------|
| `fix:` | Patch release (`v1.0.0` → `v1.0.1`) |
| `feat:` | Minor release (`v1.0.0` → `v1.1.0`) |
| `feat!:` or `BREAKING CHANGE:` | Major release (`v1.0.0` → `v2.0.0`) |

## Maintenance Releases

To release a patch for an older major version:

1. Create a branch from the desired tag: `git checkout -b release/v1.x v1.2.0`
2. Apply the fix with a conventional commit (e.g. `fix:`)
3. Open a PR targeting `release/v1.x`
4. The workflow bumps based on tags on that branch and publishes a patch release

## Post-Release Checklist

After the workflow completes, verify:

- [ ] `galaxy.yml` version matches the GitHub Release tag
- [ ] Collection is available on Ansible Galaxy (`jcalavia_org.setup`)
- [ ] Execution environment image is updated on GHCR (`ghcr.io/calavia-org/ansible-ee-setup:<tag>`) |
- [ ] GitHub Release contains the built collection artifact

## Manual Release (Emergency)

If the automated workflow fails:

```bash
git checkout main
git pull origin main
git tag -a vX.Y.Z -m "Manual release"
git push origin vX.Y.Z
```

Then follow the release workflow steps manually:
- `ansible-galaxy collection build`
- `ansible-galaxy collection publish`
- `ansible-builder build` / `docker push`
- Create GitHub Release with artifacts

## References

- [Reusable PR Workflow](https://github.com/calavia-org/workflows-lib/blob/main/docs/pr-check-and-bump.md)
- [Bump Version Action](https://github.com/calavia-org/bump-version-action)
