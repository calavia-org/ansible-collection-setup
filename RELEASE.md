# Release Guide: Ansible Collection Setup

This document describes how to release new versions of the `ansible-collection-setup` repository.

## What This Repository Is

When a PR with a conventional commit title is merged to `main`:

1. The PR workflow auto-bumps the collection version in `galaxy.yml` (if not a `chore/` branch)
2. The release workflow triggers on push to `main` when `galaxy.yml` changes
3. Builds and publishes the collection tarball to Ansible Galaxy
4. Builds the execution environment (EE) image and pushes it to GHCR
5. Creates a GitHub Release with artifacts and release notes
6. Updates the floating major tag (`v1`, `v2`, …)

## Dependencies on Other Org Repos

| Dependency | Repository | Purpose | Release Method |
|------------|------------|---------|----------------|
| PR validation + test | [`calavia-org/workflows-lib`](https://github.com/calavia-org/workflows-lib) | Reusable workflows for branch check, version bump, lint, test | Manual tags (`v0`) |
| Version bump | [`calavia-org/bump-version-action`](https://github.com/calavia-org/bump-version-action) | Composite action used inside the reusable workflow | Automated on push to main via its own release workflow |

## Versioning

This repo follows **Semantic Versioning** derived from conventional commits:

| Commit / PR Title | Version Bump | Example |
|-------------------|--------------|---------|
| `fix:` | Patch (`1.1.2` → `1.1.3`) | Bug fix |
| `feat:` | Minor (`1.1.2` → `1.2.0`) | New feature or role |
| `feat!:` or `BREAKING CHANGE:` | Major (`1.1.2` → `2.0.0`) | Breaking change |
| `chore:` / `docs:` / `refactor:` | **None** | Non-functional change (checks still run) |
| `doc:` | None | Documentation only |

## Workflows

### PR Check and Auto-Bump

[`pr-check-and-bump.yml`](.github/workflows/pr-check-and-bump.yml) — calls `calavia-org/workflows-lib/.github/workflows/pr-check-and-bump.yml@v0`:

1. Validates branch name against `^(major|feat|fix|doc|chore)/.+`
2. Parses conventional commits for bump type
3. For `chore/` branches: skips the version bump
4. For other branches: auto-bumps `galaxy.yml` version

### PR Check and Test

[`pr-check-and-test.yml`](.github/workflows/pr-check-and-test.yml) — calls `calavia-org/workflows-lib/.github/workflows/pr-check-and-test.yml@v0`:

- Detects technology, runs lint, tests, and coverage
- Skips build/publish steps (those happen on merge)

### Release Artifacts

[`release-artifacts.yml`](.github/workflows/release-artifacts.yml) — calls `calavia-org/workflows-lib/.github/workflows/release-artifacts.yml@v0`:

1. Detects version from `galaxy.yml`
2. Builds collection tarball
3. Publishes to Ansible Galaxy
4. Builds EE image and pushes to GHCR
5. Creates GitHub Release

## Maintenance Releases

To release a patch for an older major version (e.g. `v1.x` while `main` is at `v2.x`):

1. Create a branch from the desired release tag:
   ```bash
   git checkout -b release/v1.x v1.2.0
   ```
2. Cherry-pick or apply the fix with a conventional commit (e.g. `fix:`)
3. Open a PR targeting `release/v1.x`
4. The reusable workflow will bump based on tags on `release/v1.x`, not `main`

Target branches allowed for PRs: `main`, `release/*`.

## Post-Release Checklist

- [ ] `galaxy.yml` version matches the GitHub Release tag
- [ ] Collection is available on Ansible Galaxy (`calaviaorg.setup`)
- [ ] EE image is updated on GHCR (`ghcr.io/calavia-org/ansible-ee-setup:<tag>`)
- [ ] GitHub Release contains the built collection artifact

## Troubleshooting

| Issue | Check |
|-------|-------|
| Release didn't trigger | Did `galaxy.yml` change in the push to `main`? |
| EE image push failed | Is `ansible-builder` configured with `--container-runtime docker`? |
| Galaxy publish failed | Is `ANSIBLE_GALAXY_API_KEY` secret configured? |
| Version bump didn't happen | Was the PR from a branch matching the allowed pattern? `chore/` branches intentionally skip the bump. |

## Manual Release (Emergency)

If the automated workflow fails:

```bash
git checkout main
git pull origin main
git tag -a vX.Y.Z -m "Manual release"
git push origin vX.Y.Z
```

Then follow the release workflow steps manually:

```bash
cd collections/ansible_collections/calaviaorg/setup
ansible-galaxy collection build
ansible-galaxy collection publish ./calaviaorg-setup-X.Y.Z.tar.gz
ansible-builder build --container-runtime docker
docker push ghcr.io/calavia-org/ansible-ee-setup:X.Y.Z
```

And create a GitHub Release from the tag with the tarball attached.

## References

- [Reusable PR Workflow](https://github.com/calavia-org/workflows-lib/blob/main/docs/pr-check-and-bump.md)
- [Bump Version Action](https://github.com/calavia-org/bump-version-action)
- [workflows-lib/RELEASE.md](https://github.com/calavia-org/workflows-lib/blob/main/RELEASE.md)
