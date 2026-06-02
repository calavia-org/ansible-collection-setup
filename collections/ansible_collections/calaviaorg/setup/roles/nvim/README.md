# nvim

Install and configure Neovim with lazy.nvim plugin management. Deploys the full
config as Jinja2 templates with toggleable plugins, configurable LSP servers,
and configurable treesitter languages.

## Requirements

- Ansible 2.19+
- `pkg` or `brew` package manager (platform-dependent)
- `git` role (dependency) — required for lazy.nvim bootstrap

## Role Variables

### Installation

| Variable | Default | Description |
|----------|---------|-------------|
| `nvim_installer` | `pkg` | Package manager to use: `pkg` or `brew` |
| `nvim_privilege_escalation` | `true` | Use `become` for package installation |
| `nvim_os_pkgs` | `[neovim]` | OS packages to install |
| `nvim_config_dir` | `~/.config/nvim` | Path to Neovim config directory |
| `nvim_skip_configure` | `false` | Skip config deployment entirely |

### Editor Options

| Variable | Default | Description |
|----------|---------|-------------|
| `nvim_leader` | ` ` (space) | Map leader key |
| `nvim_line_numbers` | `true` | Show line numbers |
| `nvim_relative_numbers` | `true` | Show relative line numbers |
| `nvim_cursorline` | `true` | Highlight current line |
| `nvim_wrap` | `false` | Disable line wrapping |
| `nvim_tab_width` | `2` | Tab width (spaces) |
| `nvim_shift_width` | `2` | Shift width for indentation |
| `nvim_clipboard` | `unnamedplus` | Clipboard option |

### Plugin Toggles

| Variable | Default | Description |
|----------|---------|-------------|
| `nvim_plugin_cmp` | `true` | blink.cmp completion plugin |
| `nvim_plugin_lsp` | `true` | mason.nvim + nvim-lspconfig |
| `nvim_plugin_tools` | `true` | tools plugin group (telescope, treesitter, gitsigns) |
| `nvim_plugin_ui` | `true` | UI plugin group (tokyonight, lualine, which-key, neo-tree) |
| `nvim_plugin_telescope` | `true` | telescope.nvim fuzzy finder |
| `nvim_plugin_treesitter` | `true` | nvim-treesitter parser |
| `nvim_plugin_gitsigns` | `true` | gitsigns.nvim git decorations |
| `nvim_plugin_tokyonight` | `true` | tokyonight.nvim colorscheme |
| `nvim_plugin_lualine` | `true` | lualine.nvim statusline |
| `nvim_plugin_which_key` | `true` | which-key.nvim key hints |
| `nvim_plugin_neotree` | `true` | neo-tree.nvim file explorer |

### LSP Servers

| Variable | Default | Description |
|----------|---------|-------------|
| `nvim_lsp_servers` | (see below) | List of LSP servers to enable |

Default LSP servers:

```yaml
nvim_lsp_servers:
  - lua_ls
  - ts_ls
  - pyright
  - gopls
  - rust_analyzer
  - bashls
```

### Treesitter Languages

| Variable | Default | Description |
|----------|---------|-------------|
| `nvim_treesitter_languages` | (see below) | List of treesitter parsers to install |

Default languages:

```yaml
nvim_treesitter_languages:
  - lua
  - vim
  - bash
  - javascript
  - typescript
  - json
  - yaml
  - python
  - go
  - rust
  - markdown
```

## Dependencies

- [git](../git/README.md) — required for lazy.nvim bootstrap

## Example Playbook

```yaml
- hosts: all
  collections:
    - calaviaorg.setup
  roles:
    - role: nvim
      nvim_skip_configure: false
      nvim_plugin_tokyonight: true
      nvim_plugin_neotree: true
      nvim_lsp_servers:
        - lua_ls
        - pyright
```

Minimal (no plugins):

```yaml
- hosts: all
  collections:
    - calaviaorg.setup
  roles:
    - role: nvim
      nvim_plugin_cmp: false
      nvim_plugin_lsp: false
      nvim_plugin_telescope: false
      nvim_plugin_treesitter: false
      nvim_plugin_gitsigns: false
      nvim_plugin_tokyonight: false
      nvim_plugin_lualine: false
      nvim_plugin_which_key: false
      nvim_plugin_neotree: false
```

## Platform Support

- Ubuntu (focal+)
- macOS (Darwin) — uses `brew` installer, automatically sets `nvim_privilege_escalation: false`

## License

GPL-3.0-only

## Author

Jorge Calavia <jorge@calavia.org>
