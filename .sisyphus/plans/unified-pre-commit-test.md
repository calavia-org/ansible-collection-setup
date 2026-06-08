# Unified Pre-Commit & Test Reusable Workflow

## Goal

Create a centralized, reusable GitHub Actions workflow in `calavia-org/workflows-lib` that standardizes pre-commit validation, static analysis, testing, and packaging across all repositories in the organization, regardless of technology stack.

## Background

Currently, each repository maintains its own CI/CD workflows:
- `pre-commit.yml` - simple pre-commit run
- `pr.yml` - complex Ansible-specific tox matrix
- `release.yml` - build, publish, release

This leads to duplicated logic, inconsistent standards, and maintenance overhead when CI best practices change. The `pr-check-and-bump.yml` already uses the `workflows-lib` pattern successfully, proving this approach works.

## Technical Decisions

### Architecture
- **Repository**: `calavia-org/workflows-lib`
- **Workflow**: `.github/workflows/pr-check-and-test.yml`
- **Pattern**: Reusable workflow with `workflow_call` trigger
- **Technology Detection**: Composite actions per technology stack

### Workflow Structure
```
pr-check-and-test.yml (reusable)
├── Phase 1: Detect Technology
├── Phase 2: Pre-Commit (fail-fast)
├── Phase 3: Static Analysis
├── Phase 4: Build
├── Phase 5: Test (unit, integration, e2e)
├── Phase 6: Package
├── Phase 7: Publish (optional)
└── Phase 8: Report
```

### Technology Detection Order
1. `galaxy.yml` → Ansible
2. `pyproject.toml` / `setup.py` / `setup.cfg` / `requirements.txt` → Python
3. `package.json` → Node.js
4. `go.mod` → Go
5. `Cargo.toml` → Rust
6. `pom.xml` / `build.gradle` → Java
7. `Dockerfile` / `docker-compose.yml` → Docker
8. `VERSION` / `version.txt` → Generic

### Input Parameters
| Parameter | Type | Default | Description |
|---|---|---|---|
| `technology` | string | `auto` | Technology stack or auto-detect |
| `run-pre-commit` | boolean | `true` | Run pre-commit hooks |
| `run-lint` | boolean | `true` | Run static analysis |
| `run-build` | boolean | `true` | Run build step |
| `run-tests` | boolean | `true` | Run all tests |
| `run-unit-tests` | boolean | `true` | Run unit tests |
| `run-integration-tests` | boolean | `true` | Run integration tests |
| `run-e2e-tests` | boolean | `false` | Run end-to-end tests |
| `run-package` | boolean | `false` | Run packaging step |
| `run-publish` | boolean | `false` | Run publish step |
| `fail-on-missing` | boolean | `false` | Fail if config file missing |
| `custom-pre-commit-config` | string | `` | Path to custom pre-commit config |
| `test-command` | string | `` | Override test command |
| `lint-command` | string | `` | Override lint command |
| `build-command` | string | `` | Override build command |
| `package-command` | string | `` | Override package command |
| `publish-command` | string | `` | Override publish command |
| `runner-label` | string | `ubuntu-latest` | Runner label |
| `timeout-minutes` | number | `30` | Global timeout |
| `artifact-retention-days` | number | `7` | Artifact retention |
| `cache-enabled` | boolean | `true` | Enable caching |
| `report-enabled` | boolean | `true` | Publish test reports |

### Per-Technology Defaults

**Python/Ansible**
- Pre-commit: `.pre-commit-config.yaml` (if exists)
- Lint: `ruff check .` or `flake8` or `pylint`
- Build: `python -m build` or `poetry build`
- Test: `pytest` or `tox` or `ansible-test`
- Package: `wheel`, `sdist`, `ansible-galaxy collection build`
- Publish: `twine upload` or `ansible-galaxy collection publish`

**Node.js**
- Pre-commit: `.husky/` (if exists) or `lint-staged`
- Lint: `eslint` or `prettier --check`
- Build: `npm run build` or `yarn build`
- Test: `npm test` or `jest`
- Package: `npm pack`
- Publish: `npm publish`

**Go**
- Pre-commit: `golangci-lint` (if configured)
- Lint: `golangci-lint run` or `go vet ./...`
- Build: `go build ./...`
- Test: `go test ./...`
- Package: `go build` with output
- Publish: `go get` or Docker image

**Rust**
- Pre-commit: `cargo clippy` or `rustfmt`
- Lint: `cargo clippy` or `cargo fmt --check`
- Build: `cargo build --release`
- Test: `cargo test`
- Package: `cargo package`
- Publish: `cargo publish`

**Java**
- Pre-commit: `spotless` or `checkstyle` (if configured)
- Lint: `mvn checkstyle:check` or `gradle check`
- Build: `mvn package` or `gradle build`
- Test: `mvn test` or `gradle test`
- Package: `mvn package` or `gradle jar`
- Publish: `mvn deploy` or `gradle publish`

**Docker**
- Pre-commit: `hadolint` or `dockerfilelint` (if configured)
- Lint: `hadolint Dockerfile` or `dockerfilelint`
- Build: `docker build`
- Test: `container-structure-test` or `dgoss`
- Package: `docker save` or `docker push`
- Publish: `docker push` or `skaffold run`

**Generic**
- Pre-commit: `pre-commit` if `.pre-commit-config.yaml` exists
- Lint: `shellcheck` for shell scripts
- Build: `make` if `Makefile` exists
- Test: `make test` if available
- Package: `tar` or `zip`
- Publish: Manual or custom script

## Plan

### Phase 1: Infrastructure Setup
1. Create `calavia-org/workflows-lib` repository structure
2. Create `.github/workflows/pr-check-and-test.yml`
3. Create `.github/actions/` directory for composite actions
4. Create composite actions for each technology:
   - `detect-technology`
   - `setup-pre-commit`
   - `setup-python`
   - `setup-nodejs`
   - `setup-go`
   - `setup-rust`
   - `setup-java`
   - `setup-docker`
   - `run-tests`
   - `publish-reports`

### Phase 2: Core Workflow Implementation
1. Implement `detect-technology` composite action
   - Scan for technology indicators
   - Output detected technology list
   - Support multiple technologies (monorepos)
2. Implement `setup-pre-commit` composite action
   - Check for `.pre-commit-config.yaml`
   - Install pre-commit
   - Run `pre-commit run --all-files` or `pre-commit run --from-ref`
   - Support custom config path
   - Support per-technology hooks
3. Implement `pr-check-and-test.yml` reusable workflow
   - Job 1: Detect technology
   - Job 2: Pre-commit (fail-fast)
   - Job 3: Lint (parallel per technology)
   - Job 4: Build (parallel per technology)
   - Job 5: Test (matrix per technology)
   - Job 6: Package (optional)
   - Job 7: Publish (optional)
   - Job 8: Report aggregation

### Phase 3: Test Matrix & Change Detection
1. Implement change detection logic
   - Compare PR head vs base
   - Filter changed files by technology
   - Determine which tests to run
2. Implement test matrix generation
   - Per-technology test commands
   - Version matrix support
   - Platform matrix support
3. Implement test result collection
   - JUnit XML parsing
   - Coverage report collection
   - SARIF report collection

### Phase 4: Reporting & Artifacts
1. Implement report aggregation
   - Test results summary
   - Coverage report
   - Lint results
   - Security scan results
2. Implement artifact publishing
   - Test reports
   - Coverage reports
   - Build artifacts
   - Package artifacts

### Phase 5: Consumer Migration
1. Update `ansible-collection-setup`
   - Create `.github/workflows/pr-check-and-test.yml` caller
   - Delete `pre-commit.yml`
   - Delete `pr.yml` (or keep for specific cases)
   - Update `release.yml` to use new workflow
2. Update documentation
   - Migration guide
   - Configuration reference
   - Troubleshooting

## TODOs

- [ ] Create `workflows-lib` repository structure
- [ ] Implement `detect-technology` composite action
- [ ] Implement `setup-pre-commit` composite action
- [ ] Implement `pr-check-and-test.yml` reusable workflow skeleton
- [ ] Add Python/Ansible support
- [ ] Add Node.js support
- [ ] Add Go support
- [ ] Add Rust support
- [ ] Add Java support
- [ ] Add Docker support
- [ ] Implement change detection
- [ ] Implement test matrix generation
- [ ] Implement test result collection
- [ ] Implement report aggregation
- [ ] Implement artifact publishing
- [ ] Write migration guide
- [ ] Update `ansible-collection-setup` workflows
- [ ] Test on `ansible-collection-setup`
- [ ] Test on `base-template`
- [ ] Publish documentation

## Acceptance Criteria

- [ ] The workflow can be called from any repository with `uses: calavia-org/workflows-lib/.github/workflows/pr-check-and-test.yml@v1`
- [ ] Auto-detection works for all supported technologies
- [ ] Pre-commit runs first and fails fast
- [ ] All test phases are optional and configurable
- [ ] Reports are published and accessible
- [ ] Consumer repos can override defaults per-technology
- [ ] Monorepo support works (multiple technologies in one repo)
- [ ] Migration from existing workflows is documented
- [ ] Performance is acceptable (caching works)
- [ ] Error messages are clear and actionable

## Execution Strategy

### Dependencies
1. Infrastructure setup must complete before composite actions
2. Composite actions must complete before core workflow
3. Core workflow must complete before testing
4. Testing must complete before consumer migration

### Parallelization
- Infrastructure + Composite actions (Phase 1-2): Can be done in parallel
- Technology support (Phase 2): Can be added incrementally
- Testing and reporting (Phase 3-4): Can be done in parallel with technology support
- Consumer migration (Phase 5): Depends on all previous phases

### Risk Mitigation
- **Risk**: Breaking existing workflows during migration
  - **Mitigation**: Gradual migration, keep old workflows until new ones are verified
- **Risk**: Technology auto-detection fails
  - **Mitigation**: Allow explicit technology override, fail gracefully
- **Risk**: Performance issues with large repos
  - **Mitigation**: Change detection, caching, configurable timeouts
- **Risk**: Monorepo complexity
  - **Mitigation**: Phase-by-phase execution, technology-specific filtering

## Verification Strategy

1. **Unit Testing**: Test composite actions in isolation
2. **Integration Testing**: Test full workflow on sample repos
3. **End-to-End Testing**: Test on `ansible-collection-setup` and `base-template`
4. **Performance Testing**: Measure execution time vs old workflows
5. **Security Testing**: Ensure secrets handling is correct
6. **Regression Testing**: Ensure existing workflows still work

## Commit Strategy

- Phase 1: `feat(ci): add infrastructure for unified test workflow`
- Phase 2: `feat(ci): implement core workflow and composite actions`
- Phase 3: `feat(ci): add test matrix and change detection`
- Phase 4: `feat(ci): add reporting and artifact publishing`
- Phase 5: `feat(ci): migrate ansible-collection-setup to new workflow`
- Phase 6: `docs(ci): add migration guide and configuration reference`

## Notes

- The workflow should be designed to be extensible for new technologies
- Consider using `actions/cache` for per-technology caching
- Consider using `actions/upload-artifact` for build artifacts
- Consider using `EnricoMi/publish-unit-test-result-action` for test results
- Consider using `codecov/codecov-action` for coverage reports
- The workflow should support both `pull_request` and `push` triggers
- The workflow should support `workflow_dispatch` for manual testing
