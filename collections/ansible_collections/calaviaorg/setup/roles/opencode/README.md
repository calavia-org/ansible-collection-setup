# opencode

Install and configure [OpenCode](https://opencode.ai) with plugin support.

## Requirements

- Ansible 2.19+
- `brew` package manager (macOS) or `apt` (Linux)
- `git` (installed via dependency)

## Role Variables

### Installation

| Variable | Default | Description |
|----------|---------|-------------|
| `opencode_installer` | `binary` | Installation method: `binary`, `pkg`, or `brew` |
| `opencode_version` | `''` | Specific version to install (binary installer only) |
| `opencode_privilege_escalation` | `true` | Use `become` for package installation |
| `opencode_os_pkgs` | `[opencode]` | OS packages to install |

### Plugins

Each plugin has an explicit enable toggle. When enabled, the role runs a dedicated task file that follows the upstream install instructions.

| Variable | Default | Description |
|----------|---------|-------------|
| `opencode_engram_enable` | `true` | Enable the Engram memory plugin |
| `opencode_opentmux_enable` | `false` | Enable the OpenTmux tmux integration plugin |

### Engram Configuration

When `opencode_engram_enable` is `true`:

| Variable | Default | Description |
|----------|---------|-------------|
| `opencode_engram_mcp_command` | `["engram", "mcp", "--tools=agent"]` | MCP server command |
| `opencode_engram_mcp_enabled` | `true` | MCP server enabled flag |
| `opencode_engram_mcp_type` | `local` | MCP server type |

Engram installation per platform:
- **macOS**: `brew install gentleman-programming/tap/engram`
- **Linux**: `go install github.com/Gentleman-Programming/engram/cmd/engram@latest`

The role also copies the bundled `engram.ts` plugin file and installs the `@opencode-ai/plugin` npm package.

### OpenTmux Configuration

When `opencode_opentmux_enable` is `true`:

| Variable | Default | Description |
|----------|---------|-------------|
| `opencode_opentmux_package` | `opentmux` | npm package name |
| `opencode_opentmux_tmux_tpm_enable` | `false` | Enable TPM plugin management in the tmux role dependency |

OpenTmux is installed via `npm install -g opentmux`. The role also includes the `tmux` role to install and configure tmux as a dependency. By default, TPM is disabled since OpenTmux provides its own integration.

### Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `opencode_config_dir` | `~/.config/opencode` | OpenCode config directory |
| `opencode_skip_configure` | `false` | Skip all plugin and config deployment |

## Dependencies

- `git` role (soft dependency for npm install operations)

## Example Playbook

```yaml
- hosts: all
  collections:
    - calaviaorg.setup
  roles:
    - role: opencode
      opencode_engram_enable: true
      opencode_opentmux_enable: true
```

## Platform Support

- macOS (Darwin) — uses `brew` installer
- Ubuntu (focal+)

## License

GPL-2.0-or-later

## Author

Jorge Calavia <jorge@calavia.org>
