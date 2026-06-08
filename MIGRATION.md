# Migration Guide: Unified Pre-Commit & Test Workflow

## Overview

This guide explains how to migrate from per-repository CI/CD workflows to the centralized `pr-check-and-test.yml` reusable workflow in `calavia-org/workflows-lib`.

## What Changed

### Before
- `pre-commit.yml` - standalone pre-commit runner
- `pr.yml` - Ansible-specific test matrix with tox
- `release.yml` - build, publish, release
- Each repo maintained its own CI logic

### After
- `pr-check-and-test.yml` - unified caller workflow that delegates to `calavia-org/workflows-lib`
- Technology auto-detection (Python, Node.js, Go, Rust, Java, Docker, Ansible)
- Configurable phases (pre-commit, lint, build, test, package, publish)
- Centralized maintenance and updates

## Migration Steps

### 1. Create Caller Workflow

Create `.github/workflows/pr-check-and-test.yml` in your repository:

```yaml
name: PR Check and Test

on:
  pull_request:
    types: [opened, edited, reopened, synchronize]

jobs:
  pr-check-and-test:
    uses: calavia-org/workflows-lib/.github/workflows/pr-check-and-test.yml@v1
    with:
      technology: auto
      run-pre-commit: true
      run-lint: true
      run-build: true
      run-tests: true
      run-unit-tests: true
      run-integration-tests: true
      fail-on-missing: false
      python-version: '3.12'
      cache-enabled: true
      report-enabled: true
      comment-on-pr: true
    secrets:
      github-token: ${{ secrets.GITHUB_TOKEN }}
      codecov-token: ${{ secrets.CODECOV_TOKEN }}
```

### 2. Configure Inputs

#### Required Inputs
| Input | Description | Example |
|-------|-------------|---------|
| `technology` | Technology stack or `auto` for auto-detection | `auto`, `python`, `nodejs`, `go` |
| `run-pre-commit` | Enable pre-commit hooks | `true` or `false` |
| `run-tests` | Enable test execution | `true` or `false` |

#### Technology-Specific Inputs
| Input | For Technology | Description |
|-------|---------------|-------------|
| `python-version` | Python/Ansible | Python version (default: `3.12`) |
| `node-version` | Node.js | Node.js version (default: `20`) |
| `go-version` | Go | Go version (default: `1.22`) |
| `rust-toolchain` | Rust | Rust toolchain (default: `stable`) |
| `java-version` | Java | Java version (default: `21`) |
| `tox-ini` | Python/Ansible | Path to tox.ini (default: `tox.ini`) |
| `ansible-collection-path` | Ansible | Path to collection directory |

#### Optional Overrides
| Input | Description |
|-------|-------------|
| `test-command` | Override test command |
| `lint-command` | Override lint command |
| `build-command` | Override build command |
| `package-command` | Override package command |
| `publish-command` | Override publish command |

### 3. Deprecate Old Workflows

Add deprecation notices to old workflows:

```yaml
# ⚠️ DEPRECATED: This workflow is superseded by pr-check-and-test.yml
# which uses the unified calavia-org/workflows-lib reusable workflow.
# Remove this file after pr-check-and-test.yml is validated.
```

### 4. Technology-Specific Configuration

#### Python/Ansible
- Ensure `tox.ini` or `tox-ansible.ini` exists
- Ensure `.pre-commit-config.yaml` exists
- Set `python-version` to match your project
- Set `ansible-collection-path` if applicable

#### Node.js
- Ensure `package.json` has `test`, `lint`, and `build` scripts
- Ensure `.husky/pre-commit` or lint-staged is configured
- Set `node-version` to match your project

#### Go
- Ensure `go.mod` exists
- Ensure `.golangci.yml` exists for linting
- Set `go-version` to match your `go.mod`

#### Rust
- Ensure `Cargo.toml` exists
- Set `rust-toolchain` to match your project

#### Java
- Ensure `pom.xml` or `build.gradle` exists
- Set `java-version` and `java-distribution` to match your project

#### Docker
- Ensure `Dockerfile` exists
- Ensure `.hadolint.yaml` exists for linting

#### Generic
- Ensure `Makefile` exists with `test`, `lint`, `build`, `package` targets
- Or provide custom commands via inputs

### 5. Secrets Configuration

Add these secrets to your repository if needed:

| Secret | Required For | Description |
|--------|-------------|-------------|
| `GITHUB_TOKEN` | Always | Provided by GitHub Actions |
| `CODECOV_TOKEN` | Coverage reports | Codecov upload token |
| `SLACK_WEBHOOK_URL` | Notifications | Slack webhook URL |

### 6. Testing the Migration

1. Create a test PR
2. Verify the new workflow runs successfully
3. Check that all phases execute correctly
4. Verify test reports are published
5. Verify coverage reports are uploaded (if applicable)
6. Check PR comments are posted (if enabled)

### 7. Cleanup

After validating the new workflow:
1. Delete `pre-commit.yml`
2. Delete `pr.yml`
3. Update `release.yml` if needed
4. Update documentation

## Troubleshooting

### Common Issues

**1. Technology not detected**
- Set `technology` explicitly instead of `auto`
- Check that indicator files exist (e.g., `package.json`, `go.mod`, `Cargo.toml`)

**2. Pre-commit fails**
- Check `.pre-commit-config.yaml` exists
- Set `custom-pre-commit-config` if using non-standard location
- Set `fail-on-missing: false` to skip if not configured

**3. Tests not found**
- Check `test-command` override or use technology-specific defaults
- Ensure test files exist in standard locations
- Check `test-paths` if tests are in non-standard locations

**4. Coverage not uploaded**
- Check `CODECOV_TOKEN` is set
- Check `coverage-format` matches your tool output
- Verify coverage files are generated

**5. Workflow not triggered**
- Check `on:` triggers match your events
- Check `paths:` filters if using path filtering
- Ensure workflow file is in `.github/workflows/`

### Getting Help

- Check the [workflows-lib README](https://github.com/calavia-org/workflows-lib)
- Review the [plan document](.sisyphus/plans/unified-pre-commit-test.md)
- Open an issue in `calavia-org/workflows-lib`

## Example Configurations

### Python Project
```yaml
jobs:
  pr-check-and-test:
    uses: calavia-org/workflows-lib/.github/workflows/pr-check-and-test.yml@v1
    with:
      technology: python
      run-pre-commit: true
      run-tests: true
      python-version: '3.11'
      tox-ini: 'tox.ini'
      test-timeout: 20
    secrets:
      github-token: ${{ secrets.GITHUB_TOKEN }}
      codecov-token: ${{ secrets.CODECOV_TOKEN }}
```

### Node.js Project
```yaml
jobs:
  pr-check-and-test:
    uses: calavia-org/workflows-lib/.github/workflows/pr-check-and-test.yml@v1
    with:
      technology: nodejs
      run-pre-commit: true
      run-build: true
      run-tests: true
      node-version: '18'
      test-timeout: 15
    secrets:
      github-token: ${{ secrets.GITHUB_TOKEN }}
```

### Monorepo (Multiple Technologies)
```yaml
jobs:
  pr-check-and-test:
    uses: calavia-org/workflows-lib/.github/workflows/pr-check-and-test.yml@v1
    with:
      technology: auto
      run-pre-commit: true
      run-lint: true
      run-build: true
      run-tests: true
      fail-on-missing: false
    secrets:
      github-token: ${{ secrets.GITHUB_TOKEN }}
```

## Version History

| Version | Date | Changes |
|---------|------|---------|
| v1.0.0 | 2024-01-XX | Initial release |

## References

- [GitHub Actions: Reusing workflows](https://docs.github.com/en/actions/using-workflows/reusing-workflows)
- [Prometheus Plan](.sisyphus/plans/unified-pre-commit-test.md)
- [workflows-lib Repository](https://github.com/calavia-org/workflows-lib)
