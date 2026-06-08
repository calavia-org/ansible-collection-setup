# Reusable Release Artifacts Workflow

## Goal

Create a centralized, reusable GitHub Actions workflow in `calavia-org/workflows-lib` that handles releasing artifacts after a PR is merged to `main`. The workflow is **test-agnostic** (assumes tests passed in PR), **auto-detects** the version, **builds sequentially** (respecting dependencies), and **publishes to multiple targets** (GitHub Release, GHCR, package manager, chart repository).

## Background

Currently, `release.yml` in `ansible-collection-setup` is tightly coupled to Ansible collections and runs tests redundantly. We need a generic, reusable release workflow that:
- Works for any technology (Java, Node.js, Go, Python, Rust, Ansible, Docker, Helm)
- Skips tests (already validated in PR)
- Auto-detects version from standard files
- Builds multiple artifacts sequentially (binary → Docker → Helm)
- Publishes to GitHub Release, GHCR, package managers, and chart repos
- Generates auto-release notes using **conventional commits format**
- Supports **optional artifact signing** (GPG, Cosign, Notary)
- Supports **rollback on failure** (atomic release)
- Supports **release branches** (`main`, `release/*`)

## Technical Decisions

### Architecture
- **Repository**: `calavia-org/workflows-lib`
- **Workflow**: `.github/workflows/release-artifacts.yml`
- **Pattern**: Reusable workflow with `workflow_call` trigger
- **Test Policy**: No tests — caller assumes PR already validated

### Workflow Structure
```
release-artifacts.yml (reusable)
├── Phase 1: Detect Technology & Version
├── Phase 2: Detect Artifacts to Release
├── Phase 3: Build Artifacts (sequential)
│   ├── Job: build-binary
│   ├── Job: build-docker (needs: build-binary)
│   └── Job: build-helm (needs: build-docker)
├── Phase 4: Sign Artifacts (optional, parallel)
│   ├── Job: sign-binary (GPG)
│   ├── Job: sign-docker (Cosign)
│   └── Job: sign-helm (Notary)
├── Phase 5: Publish Artifacts
│   ├── Job: publish-github-release
│   ├── Job: publish-ghcr
│   ├── Job: publish-package-manager
│   └── Job: publish-helm-chart
├── Phase 6: Generate Release Notes (conventional commits)
└── Phase 7: Rollback on Failure (if needed)
```

### Version Auto-Detection
Detects version from (in priority order):
1. `galaxy.yml` (Ansible) → `version: x.y.z`
2. `pom.xml` (Java) → `<version>x.y.z</version>`
3. `Chart.yml` (Helm) → `version: x.y.z`
4. `package.json` (Node.js) → `"version": "x.y.z"`
5. `Cargo.toml` (Rust) → `version = "x.y.z"`
6. `pyproject.toml` (Python) → `version = "x.y.z"`
7. `setup.py` (Python) → `version="x.y.z"`
8. `VERSION` or `version.txt` (Generic) → plain text

### Artifact Auto-Detection
| Indicator | Artifact Type | Build Tool |
|---|---|---|
| `Dockerfile` exists | `docker` | `docker build` |
| `helm/` or `Chart.yml` exists | `helm` | `helm package` |
| `pom.xml`, `build.gradle` | `binary` (Java) | `mvn package` / `gradle build` |
| `package.json` | `binary` (Node.js) | `npm run build` / `npm pack` |
| `Cargo.toml` | `binary` (Rust) | `cargo build --release` |
| `setup.py`, `pyproject.toml` | `binary` (Python) | `python -m build` |
| `galaxy.yml` | `binary` (Ansible) | `ansible-galaxy collection build` |
| `go.mod` | `binary` (Go) | `go build` / `goreleaser` |

### Sequential Build Dependencies
```
build-binary
  └── build-docker (needs build-binary)
        └── build-helm (needs build-docker)
```

**Rationale**: Docker images often need the binary artifact first. Helm charts reference the Docker image tag.

### Trigger Support
- **Primary**: `push` to `main` (post-merge auto-release)
- **Secondary**: `push` to `release/*` (maintenance releases)
- **Manual**: `workflow_dispatch` (on-demand release)

### Input Parameters
| Parameter | Type | Default | Description |
|---|---|---|---|
| `technology` | string | `auto` | Technology stack or auto-detect |
| `artifacts` | string | `auto` | Comma-separated: `binary,docker,helm` or `auto` |
| `version-source` | string | `auto` | Version file path override |
| `release-name` | string | `` | Override release name |
| `release-draft` | boolean | `false` | Create as draft (default: auto-publish) |
| `generate-notes` | boolean | `true` | Auto-generate release notes from conventional commits |
| `publish-github-release` | boolean | `true` | Create GitHub Release with artifacts |
| `publish-ghcr` | boolean | `false` | Publish Docker image to GHCR |
| `publish-package-manager` | boolean | `false` | Publish to package manager |
| `publish-helm-chart` | boolean | `false` | Publish Helm chart to chart repo |
| `ghcr-image-name` | string | `` | GHCR image name (default: repo name) |
| `ghcr-tags` | string | `latest` | Comma-separated tags for GHCR |
| `helm-chart-path` | string | `helm/` | Path to Helm chart directory |
| `helm-chart-repo` | string | `` | Helm chart repo URL |
| `package-manager` | string | `auto` | Package manager: `npm`, `pypi`, `maven` |
| `binary-artifacts` | string | `` | Comma-separated paths to binary artifacts |
| `release-notes-template` | string | `` | Path to custom release notes template |
| `changelog-since` | string | `` | Tag to generate changelog since |
| `sign-artifacts` | boolean | `false` | Enable artifact signing |
| `sign-binary` | boolean | `false` | Sign binary with GPG |
| `sign-docker` | boolean | `false` | Sign Docker image with Cosign |
| `sign-helm` | boolean | `false` | Sign Helm chart with Notary |
| `gpg-key` | string | `` | GPG private key for signing |
| `cosign-key` | string | `` | Cosign key for Docker signing |
| `rollback-on-failure` | boolean | `true` | Rollback all published artifacts on failure |
| `runner-label` | string | `ubuntu-latest` | Runner label |
| `timeout-minutes` | number | `60` | Global timeout |
| `artifact-retention-days` | number | `7` | Artifact retention |
| `notify-on-release` | boolean | `true` | Send notification on release |
| `slack-webhook` | string | `` | Slack webhook URL |

### Technology-Specific Build & Publish

**Java**
- Build: `mvn package -DskipTests` or `gradle build -x test`
- Binary: `.jar` file
- Docker: `docker build` using JAR
- Package manager: `mvn deploy` (Maven Central)
- Helm: `helm package` (if chart exists)

**Node.js**
- Build: `npm run build` or `npm pack`
- Binary: `dist/` or `.tgz`
- Docker: `docker build` using dist/
- Package manager: `npm publish`
- Helm: `helm package` (if chart exists)

**Go**
- Build: `go build` or `goreleaser`
- Binary: compiled binary
- Docker: `docker build` using binary
- Package manager: Not applicable (GitHub Release only)
- Helm: `helm package` (if chart exists)

**Python**
- Build: `python -m build` or `poetry build`
- Binary: `.whl` and `.tar.gz`
- Docker: `docker build` using wheel
- Package manager: `twine upload` or `poetry publish`
- Helm: `helm package` (if chart exists)

**Ansible**
- Build: `ansible-galaxy collection build`
- Binary: `.tar.gz`
- Docker: Not applicable (unless custom EE)
- Package manager: `ansible-galaxy collection publish`
- Helm: Not applicable

**Docker**
- Build: `docker build`
- Image: `ghcr.io/owner/repo:version`
- GHCR: `docker push ghcr.io/...`
- Package manager: Not applicable
- Helm: `helm package` (if chart references image)

**Helm**
- Build: `helm package`
- Chart: `.tgz`
- Chart repo: `helm repo index` + push to GitHub Pages
- Package manager: Not applicable

### Release Notes Strategy
- **Auto-generate**: From commits between last tag and HEAD
- **Format**: Markdown with sections
  - `# Release vX.Y.Z`
  - `## What's Changed`
  - List of commits (with authors)
  - `## Artifacts`
  - Links to artifacts
- **No CHANGELOG file**: Generated inline in GitHub Release body
- **No commits**: No files committed to protected `main`
- **Template**: Optional custom template via `release-notes-template`

### Composite Actions Needed
- `detect-version` — Auto-detect version from standard files
- `detect-artifacts` — Auto-detect artifacts to build
- `build-binary` — Build binary artifact per technology
- `build-docker` — Build Docker image
- `build-helm` — Build Helm chart
- `sign-binary` — Sign binary with GPG
- `sign-docker` — Sign Docker image with Cosign
- `sign-helm` — Sign Helm chart with Notary
- `publish-github-release` — Create GitHub Release
- `publish-ghcr` — Push to GHCR
- `publish-package` — Publish to package manager
- `publish-helm` — Publish to chart repo
- `generate-release-notes` — Generate release notes from conventional commits
- `rollback-release` — Rollback all published artifacts on failure

## Plan

### Phase 1: Infrastructure & Composite Actions
1. Create `calavia-org/workflows-lib` repository structure (if not exists)
2. Create `.github/workflows/release-artifacts.yml`
3. Create `.github/actions/` directory for composite actions
4. Create composite actions:
   - `detect-version`
   - `detect-artifacts`
   - `build-binary`
   - `build-docker`
   - `build-helm`
   - `publish-github-release`
   - `publish-ghcr`
   - `publish-package`
   - `publish-helm`
   - `generate-release-notes`

### Phase 2: Core Workflow Implementation
1. Implement `detect-version` composite action
   - Scan for version files in priority order
   - Parse version string
   - Output version for downstream jobs
2. Implement `detect-artifacts` composite action
   - Scan for Dockerfile, Chart.yml, pom.xml, etc.
   - Output list of artifacts to build
3. Implement `build-binary` composite action
   - Technology-specific build logic
   - Output binary artifact path
   - Upload artifact for downstream jobs
4. Implement `build-docker` composite action
   - Download binary artifact from upstream job
   - Build Docker image
   - Tag with version
   - Output image name and tag
5. Implement `build-helm` composite action
   - Download Docker image info from upstream job
   - Build Helm chart
   - Update chart version and appVersion
   - Output chart path

### Phase 3: Sign Actions (Optional)
1. Implement `sign-binary` composite action
   - Import GPG key (if provided)
   - Sign binary artifact
   - Output signature file
   - Skip if `sign-binary: false`
2. Implement `sign-docker` composite action
   - Install Cosign (if needed)
   - Sign Docker image with Cosign
   - Output signature and certificate
   - Skip if `sign-docker: false`
3. Implement `sign-helm` composite action
   - Install Notary (if needed)
   - Sign Helm chart with Notary
   - Output signature
   - Skip if `sign-helm: false`

### Phase 4: Publish Actions
1. Implement `publish-github-release` composite action
   - Download all artifacts (binary, Docker info, Helm chart)
   - Create GitHub Release with artifacts attached
   - Generate release notes using conventional commits
   - Handle draft vs published
   - Support custom release notes template
2. Implement `publish-ghcr` composite action
   - Log in to GHCR using `GITHUB_TOKEN`
   - Tag and push Docker image
   - Support multiple tags (version, latest, branch)
   - Push signed attestations (if Cosign enabled)
3. Implement `publish-package` composite action
   - Technology-specific publish logic
   - npm: `npm publish`
   - PyPI: `twine upload`
   - Maven: `mvn deploy`
   - Ansible Galaxy: `ansible-galaxy collection publish`
   - Skip if `publish-package-manager: false`
4. Implement `publish-helm` composite action
   - Package Helm chart
   - Push to chart repo (GitHub Pages or custom)
   - Update index.yaml
   - Skip if `publish-helm-chart: false`

### Phase 5: Rollback & Release Notes
1. Implement `rollback-release` composite action
   - Delete GitHub Release (if created)
   - Delete GHCR images (if pushed)
   - Revert package manager publish (if possible)
   - Revert Helm chart publish (if possible)
   - Delete signed artifacts (if uploaded)
   - Notify about rollback
2. Implement `generate-release-notes` composite action
   - Parse conventional commits from last tag to HEAD
   - Group by type: feat, fix, docs, chore, refactor, test, build, ci, security, BREAKING CHANGE
   - Generate Markdown with sections
   - Support custom template
   - Output release notes body

### Phase 6: Main Workflow Assembly
1. Implement `release-artifacts.yml` reusable workflow
   - Job 1: Detect version and artifacts
   - Job 2: Build binary (if detected)
   - Job 3: Build Docker (if detected, needs binary)
   - Job 4: Build Helm (if detected, needs Docker)
   - Job 5: Sign artifacts (if enabled, parallel)
   - Job 6: Publish GitHub Release (parallel with other publishes)
   - Job 7: Publish GHCR (if enabled)
   - Job 8: Publish package manager (if enabled)
   - Job 9: Publish Helm chart (if enabled)
   - Job 10: Rollback on failure (if any publish fails)
   - Job 11: Notify (Slack, etc.)
2. Add support for release branches (`main`, `release/*`)
3. Add support for `workflow_dispatch` (manual trigger)
4. Add support for `push` to `main` (auto-trigger)

### Phase 5: Consumer Migration
1. Update `ansible-collection-setup`
   - Create `.github/workflows/release-artifacts.yml` caller
   - Deprecate `release.yml` (add deprecation notice)
   - Configure inputs for Ansible collection + Docker EE + GitHub Release
2. Test on `ansible-collection-setup`
   - Trigger manual release
   - Verify artifacts published
   - Verify release notes generated
3. Document migration guide

## TODOs

- [ ] Create `workflows-lib` repository structure (if needed)
- [ ] Implement `detect-version` composite action
- [ ] Implement `detect-artifacts` composite action
- [ ] Implement `build-binary` composite action
- [ ] Implement `build-docker` composite action
- [ ] Implement `build-helm` composite action
- [ ] Implement `sign-binary` composite action
- [ ] Implement `sign-docker` composite action
- [ ] Implement `sign-helm` composite action
- [ ] Implement `publish-github-release` composite action
- [ ] Implement `publish-ghcr` composite action
- [ ] Implement `publish-package` composite action
- [ ] Implement `publish-helm` composite action
- [ ] Implement `generate-release-notes` composite action
- [ ] Implement `rollback-release` composite action
- [ ] Implement `release-artifacts.yml` reusable workflow
- [ ] Test version detection for all technologies
- [ ] Test artifact detection for all artifact types
- [ ] Test sequential build (binary → Docker → Helm)
- [ ] Test signing (GPG, Cosign, Notary)
- [ ] Test GitHub Release creation with conventional commits
- [ ] Test GHCR push
- [ ] Test package manager publish
- [ ] Test Helm chart publish
- [ ] Test rollback on failure
- [ ] Test release notes generation
- [ ] Test Slack notification
- [ ] Test release branch support (`main`, `release/*`)
- [ ] Test `workflow_dispatch` trigger
- [ ] Write migration guide
- [ ] Update `ansible-collection-setup` workflows
- [ ] Test on `ansible-collection-setup`

## Acceptance Criteria

- [ ] The workflow can be called from any repository with `uses: calavia-org/workflows-lib/.github/workflows/release-artifacts.yml@v1`
- [ ] Auto-detection works for version and artifacts
- [ ] No tests run (by design)
- [ ] Artifacts built sequentially (respecting dependencies)
- [ ] GitHub Release created with auto-generated notes (conventional commits format)
- [ ] GHCR push works (if enabled)
- [ ] Package manager publish works (if enabled)
- [ ] Helm chart publish works (if enabled)
- [ ] Signing works (if enabled)
- [ ] Rollback works on failure (if enabled)
- [ ] No CHANGELOG committed (by design)
- [ ] Works with protected `main` branch
- [ ] Supports release branches (`main`, `release/*`)
- [ ] Supports `workflow_dispatch` (manual trigger)
- [ ] Consumer repos can override defaults per-technology
- [ ] Migration from existing workflows is documented

## Execution Strategy

### Dependencies
1. Infrastructure setup must complete before composite actions
2. Composite actions must complete before main workflow
3. Main workflow must complete before testing
4. Testing must complete before consumer migration

### Parallelization
- Composite actions (Phase 1-3): Can be developed in parallel
- Main workflow assembly (Phase 4): Depends on all composite actions
- Consumer migration (Phase 5): Depends on all previous phases

### Risk Mitigation
- **Risk**: Breaking existing release workflow during migration
  - **Mitigation**: Gradual migration, keep old workflow until new one is validated
- **Risk**: Version auto-detection fails
  - **Mitigation**: Allow explicit version override via `version-source`
- **Risk**: Artifact build fails mid-sequence
  - **Mitigation**: Fail fast, trigger rollback if enabled
- **Risk**: Protected branch prevents commits
  - **Mitigation**: No commits in workflow — all actions are non-destructive
- **Risk**: Secrets missing for publish
  - **Mitigation**: Graceful skip — if secret missing, skip publish step with warning
- **Risk**: Rollback partially fails
  - **Mitigation**: Log rollback failures, alert for manual cleanup

## Verification Strategy

1. **Unit Testing**: Test composite actions in isolation
2. **Integration Testing**: Test full workflow on sample repos
3. **End-to-End Testing**: Test on `ansible-collection-setup`
4. **Regression Testing**: Ensure existing release workflow still works

## Commit Strategy

- Phase 1: `feat(ci): add release artifacts composite actions`
- Phase 2: `feat(ci): add release artifacts reusable workflow`
- Phase 3: `feat(ci): add sign and publish actions for release artifacts`
- Phase 4: `feat(ci): add release notes and rollback actions`
- Phase 5: `feat(ci): assemble release artifacts workflow`
- Phase 6: `feat(ci): migrate ansible-collection-setup to new release workflow`
- Phase 7: `docs(ci): add release artifacts migration guide`

## Notes

- The workflow is designed for **post-merge release** only
- Tests are intentionally skipped — use `pr-check-and-test.yml` for PR validation
- Version is assumed to be bumped by `pr-check-and-bump.yml` before merge
- The workflow should support both `workflow_dispatch` (manual) and `push` to `main` (auto)
- For release branches (`release/*`), the workflow should detect the branch and publish accordingly
- For monorepos, caller can specify multiple artifacts explicitly
- Consider using `docker/build-push-action` for GHCR push
- Consider using `helm/chart-releaser-action` for Helm chart publishing
- Consider using `goreleaser/goreleaser-action` for Go releases
- Consider using `softprops/action-gh-release` for GitHub Release creation
- Consider using `sigstore/cosign-installer` for Cosign signing
- Consider using `crazy-max/ghaction-import-gpg` for GPG signing
- Consider using `softprops/action-gh-release` for GitHub Release creation
