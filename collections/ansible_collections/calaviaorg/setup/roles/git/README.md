# git

Install and configure git with LFS support.

## Requirements

- Ansible 2.19+
- `pkg` or `brew` package manager (platform-dependent)

## Role Variables

### Installation

| Variable | Default | Description |
|----------|---------|-------------|
| `git_installer` | `pkg` | Package manager to use: `pkg` or `brew` |
| `git_privilege_escalation` | `true` | Use `become` for package installation |
| `git_os_pkgs` | `[git]` | OS packages to install |

### Git LFS

| Variable | Default | Description |
|----------|---------|-------------|
| `git_lfs_enable` | `false` | Install git LFS extension |
| `git_lfs_os_pkgs` | `[git-lfs]` | LFS OS packages to install |

### Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `git_sys_config` | `/etc/gitconfig` | System-level gitconfig path |
| `git_usr_config` | `~/.gitconfig` | User-level gitconfig path |

## Dependencies

None.

## Example Playbook

```yaml
- hosts: all
  collections:
    - calaviaorg.setup
  roles:
    - role: git
      git_lfs_enable: true
```

## Platform Support

- Ubuntu (focal+)
- macOS (Darwin) — uses `brew` installer

## License

GPL-2.0-or-later

## Author

Jorge Calavia <jorge@calavia.org>
