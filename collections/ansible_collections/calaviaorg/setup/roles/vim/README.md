# vim

Install and configure vim.

## Requirements

- Ansible 2.19+
- `pkg` or `brew` package manager (platform-dependent)

## Role Variables

| Variable | Default | Description |
|----------|---------|-------------|

No configurable variables yet.

## Dependencies

None.

## Example Playbook

```yaml
- hosts: all
  collections:
    - calaviaorg.setup
  roles:
    - role: vim
```

## Platform Support

- Ubuntu (focal+)
- macOS (Darwin) — uses `brew` installer

## License

GPL-2.0-or-later

## Author

Jorge Calavia <jorge@calavia.org>
