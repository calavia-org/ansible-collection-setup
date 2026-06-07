# jcalavia_org.setup

Ansible collection for setting up local development environments.

## Included roles

| Role | Description |
|------|-------------|
| [tmux](./roles/tmux/README.md) | Install and configure tmux with TPM plugin management |
| [git](./roles/git/README.md) | Install and configure git with LFS support |
| [gpg](./roles/gpg/README.md) | Install and manage GPG keys, agent, and SSH integration |
| [nvim](./roles/nvim/README.md) | Install and configure Neovim with lazy.nvim plugin management |
| [opencode](./roles/opencode/README.md) | Install and configure OpenCode with plugin support |
| [mise](./roles/mise/README.md) | Install and configure mise version manager with global tool defaults |

## Requirements

- Ansible 2.19+
- Python 3.12+

## Installation

```bash
ansible-galaxy collection install jcalavia_org.setup
```

Or add to `requirements.yml`:

```yaml
collections:
  - name: jcalavia_org.setup
    version: 1.0.0
```

## Included Playbooks

| Playbook | Description |
|----------|-------------|
| [`full_macos_setup`](./playbooks/full_macos_setup.yml) | Full macOS development environment with GPG keys and mise tools |
| [`dev_machine`](./playbooks/dev_machine.yaml) | Basic multi-host development machine setup |

See the [playbooks documentation](./playbooks/README.md) for details.

## Usage

### Using Roles Directly

```yaml
- hosts: all
  collections:
    - jcalavia_org.setup
  roles:
    - role: tmux
    - role: git
    - role: nvim
    - role: opencode
    - role: mise
```

### Using a Playbook

```bash
# Full macOS setup (run locally)
ansible-playbook jcalavia_org.setup.full_macos_setup

# Basic setup on remote hosts
ansible-playbook -i inventory jcalavia_org.setup.dev_machine
```

## License

GPL-2.0-or-later

## Author

Jorge Calavia <jorge@calavia.org>
