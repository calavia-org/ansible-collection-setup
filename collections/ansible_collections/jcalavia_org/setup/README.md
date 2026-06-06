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

## Usage

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

## License

GPL-2.0-or-later

## Author

Jorge Calavia <jorge@calavia.org>
