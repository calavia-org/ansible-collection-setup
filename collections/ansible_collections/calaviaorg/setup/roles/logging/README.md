# logging

Install and configure rsyslog, with optional TCP reception, remote TCP forwarding, and per-facility MySQL (`ommysql`) storage.

## Requirements

- Ansible 2.19+
- Debian or Ubuntu target (uses `apt`)
- Root privileges (`become`) for package installation and config placement

## Role Variables

### Packages and identity

| Variable | Default | Description |
|----------|---------|-------------|
| `logging_packages` | `[rsyslog, rsyslog-mysql, python3-pymysql]` | Packages to install |
| `logging_user` | `syslog` | Owner of the log directory |
| `logging_group` | `syslog` | Group of the log directory |
| `logging_service` | `rsyslog` | Service name to restart |

### Paths and permissions

| Variable | Default | Description |
|----------|---------|-------------|
| `logging_log_path` | `/var/log/rsyslog` | Directory where per-facility logs are written |
| `logging_log_path_mode` | `0640` | Mode for the log directory |
| `logging_global_config_file` | `/etc/rsyslog.conf` | Global rsyslog configuration file |
| `logging_facilities_config_file` | `/etc/rsyslog.d/50-default.conf` | Per-facility configuration file |
| `logging_config_files_mode` | `0640` | Mode for the configuration files |

### Receiver (this host as a syslog server)

| Variable | Default | Description |
|----------|---------|-------------|
| `logging_receiver_tcp` | `true` | Enable the TCP input (`imtcp` on port 514) |
| `logging_allowed_sender` | `*.example.net` | `$AllowedSender` pattern accepted over TCP |

### Remote forwarding

```yaml
logging_remote_tcp:
  enabled: true
  target: 'rsyslog.example.net'
  port: 514

logging_remote_mysql:
  enabled: true
  template: 'StdSQLFormat'
  server: 'mysql.example.net'
  db: 'rsyslog'
  uid: 'rsyslog'
  pwd: 'rsyslog'
```

| Variable | Description |
|----------|-------------|
| `logging_remote_tcp` | Forward matching facility messages to a remote syslog host over TCP (`omfwd`) |
| `logging_remote_mysql` | Store matching facility messages into a remote MySQL database (`ommysql`) |

### Facilities

`logging_facilities` lists every syslog facility with the severities to capture locally,
to the remote TCP target, and to MySQL. The per-facility severity maps are resolved from
`logging_facility_severities` in `vars/main.yml`, so a facility only emits a destination
block when it defines any severity for it.

```yaml
logging_facilities:
  - id: 4
    name: 'auth'
    description: 'authpriv/authorization messages'
    local_severities: "{{ logging_facility_severities['auth'].local_severities | default([]) }}"
    tcp_severities: "{{ logging_facility_severities['auth'].tcp_severities | default([]) }}"
    mysql_severities: "{{ logging_facility_severities['auth'].mysql_severities | default([]) }}"
```

## Dependencies

None.

## Example Playbook

```yaml
- hosts: servers
  become: true
  roles:
    - role: calaviaorg.setup.logging
```

## License

GPL-3.0-only

## Author

Jorge Calavia <jorge@calavia.org>
