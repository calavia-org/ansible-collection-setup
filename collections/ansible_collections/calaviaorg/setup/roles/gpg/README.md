# gpg

Install and manage GPG keys and agent configuration.

## Requirements

- Ansible 2.19+
- `pkg` or `brew` package manager (platform-dependent)

## Role Variables

### Installation

| Variable | Default | Description |
|----------|---------|-------------|
| `gpg_installer` | `pkg` | Package manager to use: `pkg` or `brew` |
| `gpg_privilege_escalation` | `true` | Use `become` for package installation |
| `gpg_os_pkgs` | `[gnupg, pinentry-tty]` | OS packages to install |

### Agent config

| Variable | Default | Description |
|----------|---------|-------------|
| `gpg_agent_config` | `~/.gnupg/gpg-agent.conf` | Path to gpg-agent configuration file |
| `gpg_agent_ssh_support` | `true` | Enable SSH support in gpg-agent |
| `gpg_agent_cache_ttl` | `600` | Cache TTL for GPG passphrase (seconds) |
| `gpg_agent_pinentry` | `''` | Path to pinentry program (empty = default) |
| `gpg_skip_configure` | `false` | Skip gpg-agent configuration entirely |

### Key management

| Variable | Default | Description |
|----------|---------|-------------|
| `gpg_key_manage` | `false` | Enable key generation/import |
| `gpg_key_type` | `RSA` | Key type (e.g. RSA, ECC) |
| `gpg_key_length` | `4096` | Key length in bits |
| `gpg_key_real_name` | `{{ git_user_name }}` | Real name for key generation |
| `gpg_key_email` | `{{ git_user_email }}` | Email for key generation |
| `gpg_key_passphrase` | `''` | Passphrase for key (empty = no passphrase) |
| `gpg_key_import_file` | `''` | Path to existing key file to import |
| `gpg_key_export_public` | `false` | Export public key after generation |
| `gpg_key_export_path` | `~/.gnupg/public.key` | Path to export public key |

### SSH

| Variable | Default | Description |
|----------|---------|-------------|
| `gpg_ssh_control_keys` | `[]` | List of keygrips to add to sshcontrol |

## Dependencies

None.

## Example Playbook

```yaml
- hosts: all
  collections:
    - calaviaorg.setup
  roles:
    - role: gpg
      gpg_skip_configure: false
      gpg_key_manage: true
      gpg_key_real_name: 'Your Name'
      gpg_key_email: 'you@example.com'
      gpg_key_export_public: true
```

Example with git integration (GPG signing):

```yaml
- hosts: all
  collections:
    - calaviaorg.setup
  roles:
    - role: gpg
      gpg_key_manage: true
      gpg_key_real_name: 'Your Name'
      gpg_key_email: 'you@example.com'
    - role: git
      git_gpg_sign: true
      git_gpg_key: 'ABC123DEF456'
```

## Platform Support

- Ubuntu (focal+)
- macOS (Darwin) — uses `brew` installer, automatically sets `gpg_privilege_escalation: false` and `pinentry-mac`

## License

GPL-3.0-only

## Author

Jorge Calavia <jorge@calavia.org>
