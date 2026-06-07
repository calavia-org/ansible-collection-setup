# Release Guide: Ansible Collection Setup

This document describes how to release new versions of the `ansible-collection-setup` repository.

## What This Repository Is

An Ansible collection (`jcalavia_org.setup`) that provides roles for setting up development environments (git, vim/tmux, gpg, nvim, opencode, mise). It is published to:
- **Ansible Galaxy** — collection tarball
- **GitHub Container Registry (GHCR)** — execution environment image
- **GitHub Releases** — release notes and artifacts

## Dependencies on Other Org Repos

| Dependency | Repository | Purpose | Release Method |
|------------|------------|---------|----------------|
| PR validation | [`calavia-org/workflows-lib`](https://github.com/calavia-org/workflows-lib) | Reusable workflow for branch check and version bump | Manual tags (see its RELEASE.md) |
| Version bump | [`calavia-org/bump-version-action`](https://github.com/calavia-org/bump-version-action) | Composite action used inside the reusable workflow | **Automated** on push to main via its own release workflow |

### Note on `bump-version-action` Release

The `bump-version-action` has its own automated release workflow (`.github/workflows/release.yml`) that creates semantic version tags from conventional commits. This means:
- When PRs with `feat:`, `fix:`, or `BREAKING CHANGE:` commits are merged to its `main`, it auto-releases
- It maintains a floating major tag (`v1`, `v2`, etc.) for consumer convenience
- No manual tagging needed for that repository

See the release guides in those repositories for their independent release cycles.

## Release Trigger

Releases are **automatic** on push to `main` when `galaxy.yml` changes, or on git tags `v*.*.*`.

## Release Steps

### 1. Version Bump (Automatic via PR)

When a PR is merged to `main`, the reusable workflow from `workflows-lib`:
1. Checks the branch name (`feat/`, `fix/`, `major/`)
2. Bumps `galaxy.yml` version using `bump-version-action`
3. Commits the version bump back to the branch

No manual version editing needed.

### 2. Collection Build and Publish (Automatic)

The [`.github/workflows/release.yml`](.github/workflows/release.yml) handles:
1. Running sanity, unit, and integration tests
2. Building the collection tarball (`ansible-galaxy collection build`)
3. Publishing to Ansible Galaxy (`ansible-galaxy collection publish`)
4. Building the execution environment image (`ansible-builder build`)
5. Pushing the EE image to GHCR (`docker push ghcr.io/...`)
6. Creating a GitHub Release with changelog and artifacts

### 3. Manual Verification

After the workflow completes:
- [ ] Collection available on Ansible Galaxy: `jcalavia_org.setup`
- [ ] EE image available on GHCR: `ghcr.io/calavia-org/ansible-ee-setup:<version>`
- [ ] GitHub Release created with correct tarball attached
- [ ] Changelog generated from commits since last tag

## Versioning

This repo follows **Semantic Versioning** as defined by the collection's `galaxy.yml`.

| Branch Prefix | Version Bump | Example |
|---------------|--------------|---------|
| `fix/` | Patch (`1.1.2 → 1.1.3`) | Bug fix |
| `feat/` | Minor (`1.1.2 → 1.2.0`) | New role |
| `major/` | Major (`1.1.2 → 2.0.0`) | Breaking change |
| `doc/` | None | Documentation only |

## Maintenance Releases

To release a patch for an old major version:
1. Create a branch from the old release tag: `git checkout -b release/v1.x v1.2.0`
2. Cherry-pick or apply the fix
3. Open a PR targeting `release/v1.x`
4. The reusable workflow will bump based on tags on `release/v1.x`, not `main`

## Troubleshooting

| Issue | Check |
|-------|-------|
| Release didn't trigger | Did `galaxy.yml` change in the push to `main`? |
| EE image push failed | Is `--container-runtime docker` set in `ansible-builder build`? |
| Galaxy publish failed | Is `ANSIBLE_GALAXY_API_KEY` secret configured? |
| Version bump didn't happen | Was the PR from a branch matching the allowed pattern? |

---

*For release processes of dependencies, see:*
- [`workflows-lib/RELEASE.md`](https://github.com/calavia-org/workflows-lib/blob/main/RELEASE.md)
- [`bump-version-action/RELEASE.md`](https://github.com/calavia-org/bump-version-action/blob/main/RELEASE.md)
