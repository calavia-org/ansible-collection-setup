# Reusable Release Workflow — Requirements

## Core Objective
Create a centralized, reusable GitHub Actions workflow in `calavia-org/workflows-lib` that handles releasing artifacts after a PR is merged to `main`. The workflow should be **test-agnostic** (assumes tests passed in PR), **auto-detect** the version, **build sequentially** (dependencies), and **publish to multiple targets** (GitHub Release, GHCR, package manager, chart repo).

## Key Requirements (from Q&A)

### Q1: Trigger & Scope
- **Triggers**: `push` to `main` (post-merge), `workflow_dispatch` (manual)
- **Technology support**: All (Java, Node.js, Go, Python, Rust, Ansible, Docker, Helm, Generic)
- **Extensibility**: Room for per-repo specification/override

### Q2: Multiple Artifacts
- **Artifact types**: Binary (jar, npm, binary go), Docker image, Helm chart
- **Build order**: Sequential (due to dependencies, e.g., Docker image needs the binary first)
- **Dependency chain**: Binary → Docker image → Helm chart (if applicable)

### Q3: Release Targets
- **GitHub Release**: Auto-create release with artifacts attached
- **GHCR**: GitHub Container Registry (only, no DockerHub for now)
- **Package Manager**: npm, PyPI, Maven Central, etc. (auto-detect or specify)
- **Chart Repository**: Helm chart repository (e.g., GitHub Pages or custom)

### Q4: Test Strategy
- **Option B**: Skip tests entirely — assume caller already validated in PR
- **If tests skipped in PR**: Must also be skipped in release (no re-run)
- **Rationale**: Release should be fast, tests are gatekeepers at PR time

### Q5: Version Management
- **Source of truth**: `pr-check-branch-and-bump` workflow (already bumps version in PR)
- **Auto-detection**: Read version from `galaxy.yml`, `pom.xml`, `Chart.yml`, `package.json`, `Cargo.toml`, `VERSION`, etc.
- **No manual version input**: Version is already committed in `main` after merge

### Q6: Release Drafts & Notes
- **Auto-publish**: No manual approval — main is protected, PR already reviewed
- **Auto-release notes**: Generate from commits (like current `release.yml`)
- **CHANGELOG policy**: Do NOT commit CHANGELOG in release workflow — either generate inline or skip
- **Rationale**: Main is protected, commits in release workflow require special tokens/branch rules

### Q7: Secrets & Registries
- **Secrets needed**: GitHub token (for Release + GHCR), registry-specific tokens (npm, PyPI, Maven)
- **No DockerHub**: Only GHCR for containers
- **Multiple registries**: Not in one run, but GitHub Release + GHCR + chart repo should be possible simultaneously
- **GHCR**: Uses `GITHUB_TOKEN` (no extra secret needed for GHCR)

## Current State Analysis

### `release.yml` (current)
- Trigger: `workflow_dispatch` + `push` to `main` (on `galaxy.yml` changes) + `tags`
- Jobs: sanity → unit test → integration test → build → build-ee → create-release
- Publishes: Ansible Galaxy (tar.gz), GHCR (Docker image), GitHub Release
- Auto-generates release notes from commits

### Problems with current `release.yml`
- Tightly coupled to Ansible collection
- Runs tests again (redundant if PR already tested)
- Hardcoded to specific technologies
- No support for multi-artifact releases
- No Helm chart support
- No package manager support

## Design Decisions

### Architecture
- **Repository**: `calavia-org/workflows-lib`
- **Workflow**: `.github/workflows/release-artifacts.yml`
- **Pattern**: Reusable workflow with `workflow_call` trigger
- **No test jobs**: Only build, package, and publish

### Workflow Structure
```
release-artifacts.yml (reusable)
├── Phase 1: Detect Technology & Version
├── Phase 2: Detect Artifacts to Release
├── Phase 3: Build Artifacts (sequential)
│   ├── Build binary
│   ├── Build Docker image
│   └── Build Helm chart
├── Phase 4: Publish Artifacts
│   ├── GitHub Release
│   ├── GHCR
│   ├── Package Manager
│   └── Chart Repository
└── Phase 5: Generate Release Notes
```

### Input Parameters
| Parameter | Type | Default | Description |
|---|---|---|---|
| `technology` | string | `auto` | Technology stack or auto-detect |
| `artifacts` | string | `auto` | Comma-separated: `binary,docker,helm` or `auto` |
| `version-source` | string | `auto` | Version file: `galaxy.yml`, `pom.xml`, `Chart.yml`, `package.json` |
| `release-name` | string | `` | Override release name (default: auto from version) |
| `release-draft` | boolean | `false` | Create as draft (default: auto-publish) |
| `generate-notes` | boolean | `true` | Auto-generate release notes from commits |
| `publish-github-release` | boolean | `true` | Create GitHub Release |
| `publish-ghcr` | boolean | `false` | Publish Docker image to GHCR |
| `publish-package-manager` | boolean | `false` | Publish to package manager (npm, PyPI, Maven) |
| `publish-helm-chart` | boolean | `false` | Publish Helm chart to chart repo |
| `ghcr-image-name` | string | `` | GHCR image name (default: repo name) |
| `ghcr-tags` | string | `latest` | Comma-separated tags for GHCR |
| `helm-chart-path` | string | `helm/` | Path to Helm chart directory |
| `helm-chart-repo` | string | `` | Helm chart repo URL (GitHub Pages or custom) |
| `package-manager` | string | `auto` | Package manager: `npm`, `pypi`, `maven` |
| `binary-artifacts` | string | `` | Comma-separated paths to binary artifacts to attach |
| `release-notes-template` | string | `` | Path to custom release notes template |
| `changelog-since` | string | `` | Tag to generate changelog since |
| `runner-label` | string | `ubuntu-latest` | Runner label |
| `timeout-minutes` | number | `60` | Global timeout |
| `artifact-retention-days` | number | `7` | Artifact retention |
| `notify-on-release` | boolean | `true` | Send notification on release |
| `slack-webhook` | string | `` | Slack webhook URL |

### Artifact Detection (Auto)
| Indicator | Artifact Type |
|---|---|
| `Dockerfile` exists | `docker` |
| `helm/` or `Chart.yml` exists | `helm` |
| `pom.xml`, `build.gradle`, `package.json`, `Cargo.toml` | `binary` |
| `setup.py`, `pyproject.toml` | `binary` |
| `galaxy.yml` | `binary` (Ansible collection) |

### Technology-Specific Build

**Java**
- Build: `mvn package` or `gradle build`
- Docker: `docker build` using JAR
- Helm: `helm package` (if chart exists)

**Node.js**
- Build: `npm run build` or `npm pack`
- Docker: `docker build` using dist/
- Package manager: `npm publish`

**Go**
- Build: `go build` or `goreleaser`
- Docker: `docker build` using binary
- Package manager: Not applicable (GitHub Release)

**Python**
- Build: `python -m build` or `poetry build`
- Docker: `docker build` using wheel
- Package manager: `twine upload` or `poetry publish`

**Ansible**
- Build: `ansible-galaxy collection build`
- Package manager: `ansible-galaxy collection publish`

**Docker**
- Build: `docker build`
- GHCR: `docker push ghcr.io/...`

**Helm**
- Build: `helm package`
- Chart repo: `helm repo index` + push to GitHub Pages

### Release Notes Strategy
- Generate from commits between last tag and HEAD
- Format: Markdown with changelog sections
- Include: Version, date, commit list, artifact links
- No CHANGELOG file committed — generated inline in release

### Sequential Build Strategy
```yaml
jobs:
  build-binary:
    # Build binary artifact
  build-docker:
    needs: build-binary
    # Build Docker image using binary artifact
  build-helm:
    needs: build-docker
    # Build Helm chart referencing Docker image
  publish:
    needs: [build-binary, build-docker, build-helm]
    # Publish all artifacts
  release:
    needs: publish
    # Create GitHub Release with notes
```

## Constraints
- Must not run tests (already done in PR)
- Must auto-detect version from existing files
- Must handle multiple artifacts in one release
- Must support sequential builds with dependencies
- Must generate release notes without committing files
- Must be extensible for new technologies

## Success Criteria
- [ ] New workflow published in `workflows-lib`
- [ ] Consumer repos can call it with simple inputs
- [ ] Auto-detection works for all supported technologies
- [ ] Version auto-detected from standard files
- [ ] Artifacts built sequentially (respecting dependencies)
- [ ] GitHub Release created with auto-generated notes
- [ ] GHCR push works (if enabled)
- [ ] Package manager publish works (if enabled)
- [ ] Helm chart publish works (if enabled)
- [ ] No tests run (by design)
- [ ] No CHANGELOG committed (by design)
- [ ] Works with protected `main` branch

## Notes
- This workflow is designed for **post-merge release** only
- Tests are intentionally skipped — use `pr-check-and-test.yml` for PR validation
- Version is assumed to be bumped by `pr-check-and-bump.yml` before merge
- The workflow should support both `workflow_dispatch` (manual) and `push` to `main` (auto)
- For monorepos, caller can specify multiple artifacts explicitly
- Consider using `actions/download-artifact` to get artifacts from previous workflows
- Consider using `docker/build-push-action` for GHCR push
- Consider using `helm/chart-releaser-action` for Helm chart publishing
