# Ansible Collection — calaviaorg.setup

[![codecov](https://codecov.io/gh/calavia-org/ansible-collection-setup/branch/main/graph/badge.svg?token=T5NUI2U885)](https://codecov.io/gh/calavia-org/ansible-collection-setup)
[![PR Checks](https://github.com/calavia-org/ansible-collection-setup/actions/workflows/pr-check-and-bump.yml/badge.svg)](https://github.com/calavia-org/ansible-collection-setup/actions/workflows/pr-check-and-bump.yml)

An Ansible collection for setting up local development environments (git, tmux, GPG, Neovim, OpenCode, mise). Published to Ansible Galaxy as `calaviaorg.setup`.

## Docs

| Topic | Location |
|-------|----------|
| Collection (roles, installation, usage) | [`collections/.../setup/README.md`](collections/ansible_collections/calaviaorg/setup/README.md) |
| Playbooks (variables, examples) | [`collections/.../setup/playbooks/README.md`](collections/ansible_collections/calaviaorg/setup/playbooks/README.md) |
| Release process | [`RELEASE.md`](RELEASE.md) |
| Contributing | [`CONTRIBUTING.md`](CONTRIBUTING.md) |

## Quick Start

```bash
git clone https://github.com/calavia-org/ansible-collection-setup.git
cd ansible-collection-setup
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
tox -e unit-py3.12-milestone --ansible --conf tox-ansible.ini
```

## CI / Workflows

| Workflow | Purpose | Status |
|----------|---------|--------|
| [`pr-check-and-bump`](.github/workflows/pr-check-and-bump.yml) | Validate branch name, conventional commits, auto-bump version | Active |
| [`pr-check-and-test`](.github/workflows/pr-check-and-test.yml) | Lint, test, build (reusable from `calavia-org/workflows-lib`) | Active |
| [`release-artifacts`](.github/workflows/release-artifacts.yml) | Build and publish collection + EE image on merge | Active |

## Supported Platforms

- macOS (Sonoma+)
- Ubuntu (focal+)
