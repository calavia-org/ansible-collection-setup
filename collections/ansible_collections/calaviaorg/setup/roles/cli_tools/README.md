# cli_tools

Install common CLI productivity tools for development.

## Requirements

- Ansible 2.19+
- `pkg` or `brew` package manager (platform-dependent)

## Role Variables

### Installation

| Variable | Default | Description |
|----------|---------|-------------|
| `cli_tools_installer` | `pkg` | Package manager to use: `pkg` or `brew` |
| `cli_tools_privilege_escalation` | `true` | Use `become` for package installation |
| `cli_tools_os_pkgs` | (see below) | OS packages to install |
| `cli_tools_skip_install` | `false` | Skip installation entirely |

Default packages:

```yaml
cli_tools_os_pkgs:
  - bat        # Cat clone with syntax highlighting
  - btop       # Resource monitor
  - coreutils  # GNU core utilities
  - eza        # Modern ls replacement
  - fd         # Fast find alternative
  - fzf        # Fuzzy finder
  - htop       # Process viewer
  - jq         # JSON processor
  - lazygit    # TUI for git
  - tree       # Directory tree viewer
  - wget       # File downloader
  - zoxide     # Smarter cd command
```

## Dependencies

None.

## Example Playbook

```yaml
- hosts: all
  collections:
    - calaviaorg.setup
  roles:
    - role: cli_tools
```

## Platform Support

- Ubuntu (focal+)
- macOS (Darwin) — uses `brew` installer, automatically sets `cli_tools_privilege_escalation: false`

## License

GPL-3.0-only

## Author

Jorge Calavia <jorge@calavia.org>
