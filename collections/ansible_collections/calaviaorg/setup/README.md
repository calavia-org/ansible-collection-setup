# calaviaorg.setup

Ansible collection for setting up local development environments.

## Included roles

| Role | Description |
|------|-------------|
| [tmux](./roles/tmux/README.md) | Install and configure tmux with TPM plugin management |
| [git](./roles/git/README.md) | Install and configure git with LFS support |
| [gpg](./roles/gpg/README.md) | Install and manage GPG keys, agent, and SSH integration |
| [nvim](./roles/nvim/README.md) | Install and configure Neovim with lazy.nvim plugin management |

## Requirements

- Ansible 2.19+
- Python 3.12+

## Installation

```bash
ansible-galaxy collection install calaviaorg.setup
```

Or add to `requirements.yml`:

```yaml
collections:
  - name: calaviaorg.setup
    version: 1.0.0
```

## Usage

```yaml
- hosts: all
  collections:
    - calaviaorg.setup
  roles:
    - role: tmux
    - role: git
    - role: nvim
```

## License

GPL-2.0-or-later

## Author

Jorge Calavia <jorge@calavia.org>
