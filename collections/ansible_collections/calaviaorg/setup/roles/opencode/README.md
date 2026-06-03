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
| `opencode_installer` | `pkg` | Package manager: `pkg` or `brew` |
| `opencode_privilege_escalation` | `true` | Use `become` for package installation |
| `opencode_os_pkgs` | `[opencode]` | OS packages to install |

### Plugins

| Variable | Default | Description |
|----------|---------|-------------|
| `opencode_plugins` | (see below) | List of plugin definitions |
| `opencode_plugin_roles` | `[]` | Role dependencies per plugin |
| `opencode_pkg_overrides` | `{}` | Platform-specific package name overrides |

### Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `opencode_config_dir` | `~/.config/opencode` | OpenCode config directory |
| `opencode_skip_configure` | `false` | Skip config file deployment |

### Default plugins

```yaml
opencode_plugins:
  - name: engram
    dependencies:
      - installer: package
        name: engram
      - installer: npm
        name: "@opencode-ai/plugin"
    files:
      - engram.ts
    mcp:
      command: ["engram", "mcp", "--tools=agent"]
      enabled: true
      type: local
```

### Installing plugins that need other roles

```yaml
opencode_plugins:
  - name: opentmux
    dependencies:
      - installer: npm
        name: opencode-plugin-tmux
    files:
      - opentmux.ts
    mcp:
      command: ["opentmux"]
      enabled: true
      type: local

opencode_plugin_roles:
  - plugin: opentmux
    role: tmux
    vars:
      tmux_tpm_enable: false
```

## Dependencies

- `git` role (soft dependency for npm install operations)

## Example Playbook

```yaml
- hosts: all
  collections:
    - calaviaorg.setup
  roles:
    - role: opencode
      opencode_plugins:
        - name: engram
          dependencies:
            - installer: package
              name: engram
            - installer: npm
              name: "@opencode-ai/plugin"
          files:
            - engram.ts
          mcp:
            command: ["engram", "mcp", "--tools=agent"]
            enabled: true
            type: local
```

## Platform Support

- macOS (Darwin) — uses `brew` installer
- Ubuntu (focal+)

## License

GPL-2.0-or-later

## Author

Jorge Calavia <jorge@calavia.org>
