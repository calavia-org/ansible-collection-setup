# git

Install and configure git with LFS support, user identity, aliases, protocol mappings, and GPG signing.

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
| `git_sys_config` | `/etc/gitconfig` | System-level gitconfig path (requires escalation) |
| `git_usr_config` | `~/.gitconfig` | User-level gitconfig fallback path |
| `git_user_name` | `Jorge Calavia` | Git user name for commits |
| `git_user_email` | `1184336+jcalavia@users.noreply.github.com` | Git user email for commits |
| `git_core_editor` | `nvim` | Default editor for git |
| `git_pager` | `''` | Pager for git output (empty = git default) |
| `git_default_branch` | `main` | Default branch name for `git init` |
| `git_pull_rebase` | `false` | Set pull strategy to rebase |
| `git_merge_tool` | `nvimdiff` | Merge tool for conflict resolution |
| `git_merge_autosquash` | `true` | Enable `--autosquash` by default |
| `git_skip_configure` | `false` | Skip gitconfig deployment entirely |

### Aliases

| Variable | Default | Description |
|----------|---------|-------------|
| `git_aliases` | (see below) | Dict of git aliases (key = alias, value = command) |

Default aliases:

```yaml
git_aliases:
  st: status -sb
  ci: commit
  br: branch
  co: checkout
  df: diff
  dc: diff --cached
  lg: log --oneline --decorate --graph -20
  amend: commit --amend --no-edit
  undo: reset HEAD~1 --mixed
  last: log -1 HEAD
  unstage: reset HEAD --
  delete: branch -d
```

### Protocol Map

| Variable | Default | Description |
|----------|---------|-------------|
| `git_config_protocol_map` | (see below) | URL rewrite rules for git protocol |

Default protocol mappings:

```yaml
git_config_protocol_map:
  - url: 'ssh://git@github.com'
    insteadOf: 'git://github.com'
  - url: 'ssh://git@gist.github.com'
    insteadOf: 'git://gist.github.com'
```

### GPG Signing

| Variable | Default | Description |
|----------|---------|-------------|
| `git_gpg_sign` | `false` | Enable GPG signing of commits and tags |
| `git_gpg_key` | `''` | GPG key ID to use for signing |

### Include

| Variable | Default | Description |
|----------|---------|-------------|
| `git_include_config` | `''` | Path to an additional gitconfig to include |

## Dependencies

None.

## Example Playbook

```yaml
- hosts: all
  collections:
    - calaviaorg.setup
  roles:
    - role: git
      git_skip_configure: false
      git_user_name: 'Your Name'
      git_user_email: 'you@example.com'
      git_lfs_enable: true
      git_gpg_sign: true
      git_gpg_key: 'ABC123DEF456'
```

## Platform Support

- Ubuntu (focal+)
- macOS (Darwin) — uses `brew` installer, automatically sets `git_privilege_escalation: false`

## License

GPL-3.0-only

## Author

Jorge Calavia <jorge@calavia.org>
