# Ansible Collection - jcalavia_org.setup

[![codecov](https://codecov.io/gh/calavia-org/ansible-collection-setup/branch/main/graph/badge.svg?token=T5NUI2U885)](https://codecov.io/gh/calavia-org/ansible-collection-setup)
[![PR Checks](https://github.com/calavia-org/ansible-collection-setup/actions/workflows/pr-check-and-bump.yml/badge.svg)](https://github.com/calavia-org/ansible-collection-setup/actions/workflows/pr-check-and-bump.yml)

This Ansible collection sets up the local development environment:

* git
* vim
* tmux

## Supported platforms

* macOS
* Ubuntu / Debian

## Development

### Useful commands

* `tox -e unit-py3.12-2.17 --ansible --conf tox-ansible.ini -- junit-xml=tests/reports/unit.xml`
* `tox -e integration-py3.12-2.17 --ansible --conf tox-ansible.ini -- junit-xml=tests/reports/integration.xml`

## Pull Request Workflow

This repository uses the reusable [`pr-check-and-bump`](https://github.com/calavia-org/workflows-lib/blob/main/docs/pr-check-and-bump.md) workflow. When you open a PR:

1. Use **conventional commit** titles (e.g. `fix:`, `feat:`, `chore:`).
2. The workflow validates the title/commits and bumps `galaxy.yml` automatically.
3. Version changes are committed back to the PR branch.

Target branches allowed: `main`, `release/*` (for maintenance releases).

## Release Process

Releases are automated via `.github/workflows/release.yml`:

* Semantic version tags are created from conventional commits
* Floating major tag (`v1`, `v2`, …) is updated
* GitHub Releases are generated with release notes

See [RELEASE.md](RELEASE.md) for details.
