# tmux

Install and configure tmux with TPM plugin management.

## Requirements

- Ansible 2.19+
- `pkg` or `brew` package manager (platform-dependent)
- `git` (required for TPM plugin cloning)

## Role Variables

### Installation

| Variable | Default | Description |
|----------|---------|-------------|
| `tmux_installer` | `pkg` | Package manager to use: `pkg` or `brew` |
| `tmux_privilege_escalation` | `true` | Use `become` for package installation |
| `tmux_os_pkgs` | `[git, tmux]` | OS packages to install (git added for TPM) |

### TPM and Plugins

| Variable | Default | Description |
|----------|---------|-------------|
| `tmux_tpm_enable` | `true` | Enable TPM plugin management |
| `tmux_tpm_uri` | `https://github.com/tmux-plugins/tpm.git` | TPM repository URL |
| `tmux_tpm_path` | `~/.tmux/plugins/tpm` | TPM installation path |
| `tmux_plugins` | (see below) | List of plugins to manage |

### Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `tmux_config` | `~/.tmux.conf` | Path to tmux configuration file |

### Default plugins

```yaml
tmux_plugins:
  - repo: tmux-plugins/tmux-sensible
    tag: master
    enabled: true
  - repo: tmux-plugins/tmux-resurrect
    tag: master
    enabled: true
    config:
      resurrect-save-last-session: 'on'
      resurrect-save-bash-history: 'on'
  - repo: tmux-plugins/tmux-continuum
    tag: master
    enabled: true
    config:
      continuum-save-interval: '15'
      continuum-boot: 'on'
```

## Dependencies

None.

## Example Playbook

```yaml
- hosts: all
  collections:
    - calaviaorg.setup
  roles:
    - role: tmux
      tmux_tpm_enable: true
      tmux_plugins:
        - repo: tmux-plugins/tmux-sensible
          tag: master
          enabled: true
```

## Platform Support

- Ubuntu (focal+)
- macOS (Darwin) — uses `brew` installer

## License

GPL-2.0-or-later

## Author

Jorge Calavia <jorge@calavia.org>
