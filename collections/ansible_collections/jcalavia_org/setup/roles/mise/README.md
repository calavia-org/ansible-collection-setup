# mise

Install and configure [mise](https://mise.jdx.dev) (formerly rtx) version manager with global tool defaults.

## Requirements

- Ansible 2.19+
- `brew` package manager (macOS) or `curl` (Linux)
- Internet access for downloading tools

## Role Variables

### Installation

| Variable | Default | Description |
|----------|---------|-------------|
| `mise_installer` | `standalone` | Installation method: `standalone` (Linux) or `brew` (macOS) |
| `mise_privilege_escalation` | `true` | Use `become` for package installation |
| `mise_skip_configure` | `false` | Skip shell activation and tool installation |

### Shell Activation

| Variable | Default | Description |
|----------|---------|-------------|
| `mise_activate` | `true` | Add mise activation to shell rc |
| `mise_activate_shell` | `zsh` (Darwin), `bash` (Linux) | Shell to configure |

### Tool Versions

Each tool has an enable toggle and version string. When enabled, `mise use -g <tool>@<version>` is run.

| Variable | Default | Description |
|----------|---------|-------------|
| `mise_python_enable` | `true` | Install and set global Python |
| `mise_python_version` | `3.12` | Python version |
| `mise_java_enable` | `true` | Install and set global Java |
| `mise_java_version` | `temurin-21` | Java distribution and version |
| `mise_node_enable` | `true` | Install and set global Node.js |
| `mise_node_version` | `22` | Node.js version |
| `mise_go_enable` | `true` | Install and set global Go |
| `mise_go_version` | `latest` | Go version |

## Dependencies

None.

## Example Playbook

```yaml
- hosts: all
  collections:
    - jcalavia_org.setup
  roles:
    - role: mise
      mise_python_version: '3.11'
      mise_java_version: 'openjdk-21'
      mise_node_version: 'lts'
```

## Platform Support

- macOS (Darwin) — uses `brew` installer
- Ubuntu (focal+)

## License

GPL-2.0-or-later

## Author

Jorge Calavia <jorge@calavia.org>
