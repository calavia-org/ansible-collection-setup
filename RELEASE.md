# Release Guide: Ansible Collection Setup

This document describes how to release new versions of the `ansible-collection-setup` repository.

## What This Repository Is

When a PR with a conventional commit title is merged to `main`:

1. The release workflow triggers (`Release Collection`)
2. It bumps the collection version in `galaxy.yml` based on commit types
3. Builds and publishes the collection tarball to Ansible Galaxy
4. Builds the execution environment (EE) image and pushes it to GHCR
5. Creates a GitHub Release with artifacts and release notes
6. Updates the floating major tag (`v1`, `v2`, …)

## Dependencies on Other Org Repos

| Dependency | Repository | Purpose | Release Method |
|------------|------------|---------|----------------|
| PR validation | [`calavia-org/workflows-lib`](https://github.com/calavia-org/workflows-lib) | Reusable workflow for branch check and version bump | Manual tags (see its RELEASE.md) |
| Version bump | [`calavia-org/bump-version-action`](https://github.com/calavia-org/bump-version-action) | Composite action used inside the reusable workflow | Automated on push to main via its own release workflow |

## Versioning

This repo follows **Semantic Versioning** derived from conventional commits:

| Commit / PR Title | Version Bump | Example |
|-------------------|--------------|---------|
| `fix:` | Patch (`1.1.2` → `1.1.3`) | Bug fix |
| `feat:` | Minor (`1.1.2` → `1.2.0`) | New feature or role |
| `feat!:` or `BREAKING CHANGE:` | Major (`1.1.2` → `2.0.0`) | Breaking change |
| `chore:` / `docs:` / `refactor:` | Patch (minor) | Non-functional change |
| `doc:` | None | Documentation only

## Release Steps

### 1. Version Bump (Automatic via PR)

The reusable PR workflow handles this automatically:

1. Checks the branch name against the allowed pattern (`^(major|feat|fix|doc)/.+`)
2. Parses conventional commits in the PR to determine bump type
3. Bumps `galaxy.yml` version using `bump-version-action`
4. Commits the version bump back to the PR branch

### 2. Collection Build and Publish (Automatic on Merge)

The [`.github/workflows/release.yml`](.github/workflows/release.yml) workflow runs on push to `main` and:

1. Runs sanity, unit, and integration tests
2. Builds the collection tarball with `ansible-galaxy collection build`
3. Publishes to Ansible Galaxy via `ansible-galaxy collection publish`
4. Builds the execution environment image with `ansible-builder build`
5. Pushes the EE image to GHCR (`ghcr.io/calavia-org/ansible-ee-setup:<version>`)
6. Creates a GitHub Release with changelog and the built artifact

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

| Issue | Check |
|-------|-------|
| Release didn't trigger | Did `galaxy.yml` change in the push to `main`? |
| EE image push failed | Is `--container-runtime docker` set in `ansible-builder build`? |
| Galaxy publish failed | Is `ANSIBLE_GALAXY_API_KEY` secret configured? |
| Version bump didn't happen | Was the PR from a branch matching the allowed pattern? |

- [ ] `galaxy.yml` version matches the GitHub Release tag
- [ ] Collection is available on Ansible Galaxy (`calaviaorg.setup`)
- [ ] EE image is updated on GHCR (`ghcr.io/calavia-org/ansible-ee-setup:<tag>`)
- [ ] GitHub Release contains the built collection artifact

## Troubleshooting

| Issue | Check |
|-------|-------|
| Release didn't trigger | Did `galaxy.yml` change in the push to `main`? |
| EE image push failed | Is `--container-runtime docker` set in `ansible-builder build`? |
| Galaxy publish failed | Is `ANSIBLE_GALAXY_API_KEY` secret configured? |
| Version bump didn't happen | Was the PR from a branch matching the allowed pattern? |

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
