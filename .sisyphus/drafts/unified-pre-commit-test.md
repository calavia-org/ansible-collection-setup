# Unified Pre-Commit & Test Reusable Workflow

## Draft - Requirements Gathering

### Core Objective
Create a centralized, reusable GitHub Actions workflow in `calavia-org/workflows-lib` that standardizes pre-commit validation, static analysis, testing, and packaging across all repositories in the organization, regardless of technology stack.

### Key Requirements
1. **Reusable workflow**: New `pr-check-and-test.yml` in `workflows-lib` using `workflow_call`
2. **Technology support**: Python, Node.js, Go, Rust, Docker, Java, Ansible (python-based)
3. **Unified workflow**: Single workflow with input parameters to enable/disable specific phases
4. **Pre-commit integration**:
   - Run first as fail-fast gate
   - Configurable per-technology (pre-commit for Python, husky for Node.js, etc.)
   - Default to `.pre-commit-config.yaml` if present
   - Fail if no config found and `fail-on-missing: true`
5. **Configurable phases**: Pre-commit, lint, build, test (unit, integration, e2e), package, publish
6. **Technology auto-detection**: Scan repo for indicators (e.g., `package.json`, `go.mod`, `Cargo.toml`, etc.)
7. **Change detection**: Only run phases for changed files (like current `pr.yml`)
8. **Matrix support**: Support matrix builds across versions/platforms

### Current State Analysis
- `pre-commit.yml`: Simple, runs on all files, no change detection
- `pr.yml`: Complex Ansible-specific with tox matrix, change detection, molecule tests
- `release.yml`: Build, publish, create release
- `pr-check-and-bump.yml`: Already uses `workflows-lib` pattern

### Decisions to Make
- Where to store the unified workflow? `workflows-lib/.github/workflows/pr-check-and-test.yml`
- How to handle technology-specific defaults? Composite actions per technology
- What about monorepos? Support for multiple technologies in one repo
- How to handle test reporting? JUnit, coverage, SARIF
- What about security scanning? SAST, dependency scanning, container scanning
- How to handle caching? Per-technology cache keys
- What about parallel execution? Job dependencies and parallelization

### Constraints
- Must be backwards compatible with existing workflows
- Must work for both PR and push triggers
- Must support custom runner labels
- Must fail gracefully when tools are missing
- Must produce consistent artifacts

### Questions to Resolve
1. Should we support custom pre-commit hooks per repo?
2. Should we include security scanning (SAST, DAST, dependency check)?
3. Should we support container image scanning?
4. How to handle test result aggregation?
5. Should we support manual dispatch with custom parameters?
6. How to handle notifications (Slack, Teams, email)?
7. Should we include performance testing gates?
8. How to handle artifacts retention?

### Target Repositories
- `ansible-collection-setup` (Ansible/Python)
- `base-template` (generic)
- Other repos in `calavia-org`

### Success Criteria
- [ ] New workflow published in `workflows-lib`
- [ ] Consumer repos can call it with simple inputs
- [ ] Auto-detection works for all supported technologies
- [ ] Pre-commit runs first and fails fast
- [ ] All test phases are optional and configurable
- [ ] Reports are published and accessible
- [ ] Documentation is complete
