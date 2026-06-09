# Contributing to calaviaorg.setup

Thank you for your interest in contributing! This collection is managed with automated CI workflows and strict conventions.

## Prerequisites

- Python 3.12+
- Ansible 2.19+
- `tox-ansible` installed (`pip install tox-ansible`)

## Development Setup

```bash
git clone https://github.com/calavia-org/ansible-collection-setup.git
cd ansible-collection-setup
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

## Running Tests

```bash
# Unit tests
tox -e unit-py3.12-milestone --ansible --conf tox-ansible.ini

# Sanity tests
tox -e sanity-py3.12-milestone --ansible --conf tox-ansible.ini

# Integration tests (molecule)
tox -e integration-py3.12-milestone --ansible --conf tox-ansible.ini
```

## Linting

```bash
ruff format .
ruff check . --fix
pre-commit run --all-files
ansible-lint
yamllint -c .yamllint .
```

## Branch Naming

All branches **must** follow the pattern `^(major|feat|fix|doc|chore)/.+`:

| Prefix | Version Bump | Use Case |
|--------|--------------|----------|
| `fix/` | Patch | Bug fixes |
| `feat/` | Minor | New features or roles |
| `major/` | Major | Breaking changes |
| `doc/` | None | Documentation only |
| `chore/` | None | CI, tooling, non-functional changes |

## Commit Convention

- Squash merge is required
- PR title must follow conventional commits: `type(scope): description`
- Examples: `fix(ci): correct workflow version`, `feat(role): add tmux configuration`

## PR Workflow

1. Create a branch from `main` with the correct prefix
2. Make your changes
3. Run tests and linting locally
4. Open a PR targeting `main`
5. The reusable workflow will auto-bump `galaxy.yml` version before merge (unless `chore/` branch)

## Release Process

See [`RELEASE.md`](RELEASE.md) for the full release process.

## Questions?

Open an issue or reach out to the maintainers.
