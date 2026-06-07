# Implementation: Unified PR Check and Auto-Bump Workflow

## Overview

This document records all repositories touched during the implementation of the unified PR check and auto-bump workflow across the `calavia-org` organization.

### 4. `calavia-org/bump-version-action` (Custom Action)

**Branch:** `main`
**Changes:**
- Created repository with custom composite action
- Added `action.yml` — composite action that handles:
  - Auto-detection of technology from common version files
  - Reading current version from detected file
  - Semver bumping (major/minor/patch)
  - Writing new version back to file
- Added `README.md` — documentation for usage

**Supported Technologies:**
- Ansible: `galaxy.yml`
- Node.js: `package.json`
- Python: `pyproject.toml`, `setup.py`
- Rust: `Cargo.toml`
- Generic: `VERSION`, `version.txt`

**Usage:**
```yaml
- uses: calavia-org/bump-version-action@v1
  with:
    version-file: auto
    bump-type: patch
```

---

## Repositories Modified

### 1. `calavia-org/workflows-lib` (Reusable Workflow Source)

**Branch:** `feat/pr-check-and-bump`
**Changes:**
- Added `.github/workflows/pr-check-and-bump.yml` (274 lines)
  - Job 1: `check-branch-name` — validates branch name against regex and target branch
  - Job 2: `auto-bump-version` — fetches latest tag from base branch, bumps version using custom action

**Key Features:**
- `workflow_call` trigger for reuse across org
- Inputs: `allowed-branch-pattern`, `allowed-target-branches`, `version-file`, `fail-on-invalid-branch`
- Base branch detection via `github.base_ref` (supports `main`, `release/*`, etc.)
- Uses `calavia-org/bump-version-action@v1` for technology-agnostic version bumping
- Technology auto-detection: Ansible (`galaxy.yml`), Node.js (`package.json`), Python (`pyproject.toml`/`setup.py`), Rust (`Cargo.toml`), Generic (`VERSION`/`version.txt`)
- Secrets: `github-token` with write permissions

---

### 2. `calavia-org/.github` (Organization Workflow Templates)

**Branch:** `feat/pr-check-template`
**Changes:**
- Added `workflow-templates/pr-check-and-bump.yml` — caller template
- Added `workflow-templates/pr-check-and-bump.properties.json` — template metadata

**Purpose:**
Provides a starter workflow template visible in GitHub's "Actions" tab when creating new workflows.

---

### 3. `calavia-org/ansible-collection-setup` (Consumer / This Repo)

**Branch:** `feat/use-reusable-pr-workflow`
**Changes:**
- **Deleted:**
  - `.github/workflows/check_branch_name.yml` (14 lines)
  - `.github/workflows/auto-bump-version.yml` (112 lines)
- **Created:**
  - `.github/workflows/pr-check-and-bump.yml` (16 lines) — calls reusable workflow with explicit `version-file`

**Migration Note:**
Since this is an Ansible collection, the `version-file` input is explicitly set to `collections/ansible_collections/jcalavia_org/setup/galaxy.yml` to avoid auto-detection overhead.

---

## Migration Status by Repository

| Repository | Status | Action Required |
|------------|--------|-----------------|
| `bump-version-action` | ✅ Ready | Action published to marketplace |
| `workflows-lib` | ✅ Ready | Push branch `feat/pr-check-and-bump`, create PR, merge |
| `.github` | ✅ Ready | Push branch `feat/pr-check-template`, create PR, merge |
| `ansible-collection-setup` | ✅ Ready | Push branch `feat/use-reusable-pr-workflow`, create PR, merge |
| `base-template` | ⏳ Pending | Add `.github/workflows/pr-check-and-bump.yml` calling reusable workflow |
| `portainer-homelab-catalog` | ⏳ Pending | Evaluate if needed (may not use versioning) |
| `dev-containers` | ⏳ Pending | Evaluate if needed |
| Other repos | ⏳ Pending | Add caller workflow if they use PR-based versioning |

---

## Repository Settings (Required)

Before using the unified workflow, configure these GitHub repository settings:

### Branch Protection Rules (for `main` and `release/*`)

1. **Require linear history** → Enable (no merge commits)
2. **Allow squash merging** → Enable
3. **Allow merge commits** → Disable
4. **Allow rebase merging** → Disable

This ensures all PRs are squashed into a single conventional commit.

## How to Migrate a New Repository

1. Create `.github/workflows/pr-check-and-bump.yml`:
    ```yaml
    name: PR Check and Auto-Bump

    on:
      pull_request:
        types: [opened, edited, reopened, synchronize]

    jobs:
      pr-check-and-bump:
        uses: calavia-org/workflows-lib/.github/workflows/pr-check-and-bump.yml@main
        with:
          allowed-branch-pattern: ""                          # Optional: disable branch naming check
          allowed-target-branches: "main,release/*"
          version-file: "auto"
          fail-on-invalid-branch: false                      # Disabled when using conventional commits
          require-conventional-commits: true                   # Enforce conventional commit format
        secrets:
          github-token: ${{ secrets.GITHUB_TOKEN }}
    ```

2. Remove old `check_branch_name.yml` and `auto-bump-version.yml` if present.

3. Commit, push, and create PR with a conventional commit message:
    - `fix: description` → patch bump
    - `feat: description` → minor bump
    - `feat!: description` or `BREAKING CHANGE:` → major bump

---

## Validation Checklist

- [ ] Repository settings: Squash merge enabled, linear history required
- [ ] `workflows-lib` PR merged → reusable workflow available at `main`
- [ ] `.github` PR merged → template available in GitHub UI
- [ ] `ansible-collection-setup` PR merged → consumer using reusable workflow
- [ ] Test: Create PR with `feat: test feature` title → minor bump
- [ ] Test: Create PR with `fix: test bug` title → patch bump
- [ ] Test: Create PR with `feat!: breaking change` title → major bump
- [ ] Test: Create PR targeting `release/v1.x` → uses tags from that branch
- [ ] Test: Create PR with non-conventional title → workflow fails with clear message

---

## Rollback Plan

If the reusable workflow causes issues:
1. Revert the consumer repo to use the old standalone workflows.
2. Copy the old `check_branch_name.yml` and `auto-bump-version.yml` from git history.
3. The reusable workflow in `workflows-lib` can be updated independently without affecting consumers until they pin to a new version tag.

---

## Future Enhancements

- Add `v1` tag to `workflows-lib` for stable referencing (instead of `@main`)
- Add support for additional technologies (Go modules, Ruby gems, Java Maven/Gradle)
- Add optional Slack/Teams notification on version bump
- Support monorepo with multiple version files via matrix strategy

---

*Document generated during implementation on 2026-06-07*
