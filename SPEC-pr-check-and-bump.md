# SPEC: Unified Org-Level PR Workflow with Branch Name Check and Auto-Bump

## 1. Goal

Unify the `check_branch_name.yml` and `auto-bump-version.yml` workflows into a single, reusable, organization-level workflow that:

1. Validates PRs follow **conventional commit** format (squash merge required).
2. Automatically bumps the repository version based on **conventional commit type** (`fix:` → patch, `feat:` → minor, `BREAKING CHANGE:` → major) and technology.
3. Supports **any target branch**, not just `main`, to enable maintenance releases from old major versions.
4. Is reusable across all repositories in `calavia-org`.

### Required Repository Settings

| Setting | Value | Why |
|---------|-------|-----|
| Squash merge | Enabled | Ensures single conventional commit per PR |
| Merge commits | Disabled | Enforces linear history |
| Rebase merge | Disabled | Prevents non-squash merges |
| Linear history | Required | Clean commit graph |

## 2. Architecture

### 2.1 Repositories

| Repository | Role | Current State |
|---|---|---|
| `calavia-org/.github` | Org-level workflow **templates** and shared configuration | Has `check_branch_name.yml` (non-reusable template) |
| `calavia-org/workflows-lib` | Reusable workflow **library** using `workflow_call` | Has `build-container.yml` (reusable) |
| Consumer repos | Call reusable workflows from `workflows-lib` | `ansible-collection-setup`, `base-template`, etc. |

**Decision:** The unified reusable workflow lives in `calavia-org/workflows-lib`. The `calavia-org/.github` repository provides the **caller workflow template** that consumer repos can copy or reference.

**Rationale:**
- `workflows-lib` already hosts reusable workflows (`workflow_call` trigger).
- `.github` repo is the GitHub-recommended location for organization-level templates, but reusable workflows can live anywhere in the org.
- Keeping reusable logic in `workflows-lib` and templates in `.github` follows the existing convention.

### 2.2 Workflow Structure

```
calavia-org/bump-version-action
├── action.yml                          # Custom composite action
└── README.md

calavia-org/workflows-lib
└── .github/workflows/
    └── pr-check-and-bump.yml           # Reusable workflow (workflow_call)

calavia-org/.github
└── workflow-templates/
    └── pr-check-and-bump.properties.json   # Template metadata
    └── pr-check-and-bump.yml               # Caller template

Consumer repo (e.g., ansible-collection-setup)
└── .github/workflows/
    └── pr-check-and-bump.yml           # Calls calavia-org/workflows-lib/.github/workflows/pr-check-and-bump.yml@v0
```

## 3. Reusable Workflow Design (`workflows-lib`)

### 3.1 Inputs

```yaml
workflow_call:
  inputs:
    allowed-branch-pattern:
      description: "Regex for allowed branch names"
      type: string
      default: "^(major|feat|fix|doc|chore)/.+"
    version-file:
      description: "Path to the version file (auto-detected if not provided)"
      type: string
      default: "auto"
    commit-message-prefix:
      description: "Prefix for the auto-bump commit message"
      type: string
      default: "chore: bump version to"
```

### 3.2 Jobs

#### Job 1: `check-branch-name`
- **Purpose:** Validate the PR branch name against the configured regex.
- **Steps:**
  1. Extract branch name from `github.head_ref`.
  2. Run regex check using `actions-ecosystem/action-regex-match` or bash.
  3. Fail if branch name does not match allowed pattern.
- **Output:** `branch_type` (major/minor/fix/doc) extracted from branch prefix.

#### Job 2: `auto-bump-version`
- **Needs:** `check-pr` (to get `bump_type` from conventional commits).
- **Condition:** Only runs if conventional commits found and target branch is valid.
- **Steps:**
  1. Checkout PR branch with `fetch-depth: 0` and `token: secrets.GITHUB_TOKEN`.
  2. **Determine base branch:** Use `${{ github.base_ref }}` (the target branch of the PR).
  3. **Fetch tags on base branch:** `git fetch origin ${{ github.base_ref }} --tags`.
  4. **Get latest tag from base branch:** `git describe --tags --abbrev=0 origin/${{ github.base_ref }}`.
  5. **Bump version using custom action:**
     ```yaml
      - uses: calavia-org/bump-version-action@v0
        with:
          version-file: ${{ inputs.version-file }}
          bump-type: ${{ needs.check-pr.outputs.bump_type }}
          current-version: ${{ steps.current.outputs.version }}
     ```
  6. **Check for changes and last commit** (same logic as current).
  7. **Commit and push** version bump to PR branch.

## 4. Technology Detection and Bumping Strategies

### 4.1 Supported Technologies (v1)

| Technology | Version File | Parser | Notes |
|---|---|---|---|
| Ansible Collection | `galaxy.yml` | `yq` or `sed` | `version: x.y.z` |
| Python (PEP440) | `pyproject.toml` | `toml` CLI or Python | `[project] version = "x.y.z"` |
| Python (legacy) | `setup.py` | `sed` or Python | `version="x.y.z"` |
| Node.js/npm | `package.json` | `jq` | `"version": "x.y.z"` |
| Rust | `Cargo.toml` | `toml` CLI | `[package] version = "x.y.z"` |
| Generic | `VERSION` or `version.txt` | `sed` | Plain text `x.y.z` |

### 4.2 Detection Order

1. If `version-file: auto` (default), scan the repo root for known files in priority order.
2. If a specific `version-file` is provided, use that directly.
3. Fail with a clear message if no version file is found and `fail-if-missing: true`.

### 4.3 Bumping Action

A custom **composite action** stored in `calavia-org/bump-version-action` that:
- Takes inputs: `version-file`, `bump-type`, `current-version`
- Auto-detects technology if `version-file: auto`
- Reads the current version from the file
- Applies semver bump
- Writes the new version back
- Outputs: `new-version`, `version-file`, `technology`

**Why a custom action instead of a script?**
- Reusable across workflows without duplicating logic
- Easier to version and maintain independently
- Can be used outside the reusable workflow if needed
- Follows GitHub Actions best practices for composability

## 5. Base Branch Support (Key Requirement #2)

**Problem:** Current workflow hardcodes `main` for tag comparison.

**Solution:** Use `github.base_ref` which contains the target branch of the PR.

**Example:**
- PR targets `main` → compare tags on `origin/main` → bump from latest tag on main.
- PR targets `release/v1.x` → compare tags on `origin/release/v1.x` → bump from latest tag on that branch.
- PR targets `v2.0` (tag-based branch) → compare tags on that branch line.

**Implementation:**
```bash
BASE_BRANCH="${{ github.base_ref }}"
git fetch origin "$BASE_BRANCH" --tags
LATEST_TAG=$(git describe --tags --abbrev=0 "origin/$BASE_BRANCH" 2>/dev/null || echo "0.0.0")
```

## 6. Caller Workflow Template (`.github` repo)

The `calavia-org/.github` repository provides a starter workflow that consumer repos can use.

```yaml
# .github/workflows/pr-check-and-bump.yml (in consumer repo)
name: PR Check and Auto-Bump

on:
  pull_request:
    types: [opened, edited, reopened, synchronize]

jobs:
  pr-check-and-bump:
    uses: calavia-org/workflows-lib/.github/workflows/pr-check-and-bump.yml@v0
    with:
      allowed-branch-pattern: "^(major|feat|fix|doc|chore)/.+"
      no-bump-branch-pattern: "^chore/.+"
      # version-file: "auto"  # optional, auto-detected by default
    secrets:
      github-token: ${{ secrets.GITHUB_TOKEN }}
```

## 7. Migration Plan

### Phase 1: Create reusable workflow in `workflows-lib`
1. Create `calavia-org/workflows-lib/.github/workflows/pr-check-and-bump.yml`.
2. Create `calavia-org/workflows-lib/scripts/detect-version-file.sh` and `bump-version.sh`.
3. Test manually with `act` or a test repo.

### Phase 2: Update `.github` repo
1. Replace `check_branch_name.yml` with a caller template pointing to `workflows-lib`.
2. Add workflow template metadata for GitHub UI (`.properties.json`).

### Phase 3: Migrate consumer repos
1. **`ansible-collection-setup`:**
   - ✅ Create `.github/workflows/pr-check-and-bump.yml` calling the reusable workflow.
   - ✅ Create `.github/workflows/pr-check-and-test.yml` calling the reusable test workflow.
   - ✅ Create `.github/workflows/release-artifacts.yml` calling the reusable release workflow.
   - ✅ Deprecated old workflows (`pr.yml`, `release.yml`).
2. **`base-template`:**
   - Update `pull-request.yml` to include the reusable workflow call.
3. Other repos: Add the caller workflow as needed.

### Phase 4: Deprecate old workflows
1. ✅ After all repos are migrated, archive or delete old per-repo workflows.

## 8. Decisions Made

1. ✅ **Version bumping tool:** Custom composite action (`calavia-org/bump-version-action@v1`) instead of inline script or third-party action.
2. **Technology detection priority:** galaxy.yml → package.json → pyproject.toml → setup.py → Cargo.toml → VERSION → version.txt
3. ✅ **Branch pattern for base branches:** Yes, validate `github.base_ref` against allowed patterns (default: `main`, `release/*`).
4. ✅ **Bump type source:** Conventional commits, not branch names. Parse commit messages for `fix:`, `feat:`, `BREAKING CHANGE:`.
5. ✅ **Squash merge required:** All repositories must configure squash merge + linear history to ensure single conventional commit per PR.
6. **Matrix support:** Not for v1. Can be added later if monorepo needs arise.

## 9. Risks and Mitigations

| Risk | Mitigation |
|---|---|
| Reusable workflow changes break all repos | Pin to major version tags (`@v0`) instead of `@main` |
| Auto-detection picks wrong version file | Allow explicit `version-file` override in caller |
| Tag comparison on non-main branch fails gracefully | Default to `0.0.0` if no tags exist on base branch |
| Race condition: two PRs bump simultaneously | Commit check (`already_bumped`) prevents duplicate commits |

## 10. Success Criteria

- [x] `bump-version-action` custom action published to `calavia-org/bump-version-action@v0`.
- [x] `workflows-lib` has a reusable `pr-check-and-bump.yml` workflow using the action.
- [x] `workflows-lib` has a reusable `pr-check-and-test.yml` workflow.
- [x] `workflows-lib` has a reusable `release-artifacts.yml` workflow.
- [x] `.github` repo provides a caller template.
- [x] `ansible-collection-setup` uses the reusable workflows and deprecated old ones.
- [x] A PR to `main` correctly bumps version based on tags on `main`.
- [x] A PR to `release/v1.x` correctly bumps version based on tags on `release/v1.x`.
- [x] Branch names like `feat/new-feature` pass; `random-name` fails.
