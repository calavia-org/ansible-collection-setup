# Playbooks — calaviaorg.setup

This collection provides two playbooks for setting up development environments.

## Available Playbooks

| Playbook | Description |
|----------|-------------|
| [`dev_machine`](./dev_machine.yaml) | Basic multi-host development machine setup |
| [`full_macos_setup`](./full_macos_setup.yml) | Complete macOS development environment with GPG keys and mise tools |

---

## dev_machine

Basic development machine setup targeting any host.

### Synopsis

Installs git, Neovim, tmux, and OpenCode on one or more remote hosts. Suitable for Ubuntu and macOS targets.

### Requirements

- Ansible 2.19+
- Target host(s) reachable via SSH
- Python 3.12+ on target hosts

### Usage

```bash
ansible-playbook -i inventory calaviaorg.setup.dev_machine
```

### Playbook Content

```yaml
- hosts: all
  roles:
    - calaviaorg.setup.git
    - calaviaorg.setup.nvim
    - calaviaorg.setup.tmux
    - calaviaorg.setup.opencode
```

### Variables

This playbook accepts all role variables from its included roles (see each role's README).

---

## full_macos_setup

Complete macOS development environment setup for localhost.

### Synopsis

Configures a local macOS machine with the full development toolchain: git identity, GPG key generation, tmux with TPM persistence, Neovim with IDE plugins, OpenCode with Engram memory plugin, and mise with Python, Java, Node.js, and Go.

### Requirements

- macOS (Sonoma+)
- Ansible 2.19+
- Python 3.12+
- Homebrew (used by most roles on Darwin)

### Usage

```bash
ansible-playbook calaviaorg.setup.full_macos_setup
```

### Playbook Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `git_user_name` | `{{ lookup("env", "USER") }}` | Git user name, also used for GPG key generation |
| `git_user_email` | `{{ lookup("env", "USER") }}@{{ ansible_hostname }}` | Git user email, also used for GPG key generation |
| `gpg_key_manage` | `true` | Enable GPG key generation |
| `gpg_key_real_name` | `{{ git_user_name }}` | Real name for the GPG key |
| `gpg_key_email` | `{{ git_user_email }}` | Email for the GPG key |
| `gpg_key_export_public` | `true` | Export public key after generation |
| `opencode_engram_enable` | `true` | Enable the Engram memory plugin |
| `opencode_opentmux_enable` | `true` | Enable the OpenTmux tmux integration |
| `mise_python_enable` | `true` | Install and set global Python (3.12) |
| `mise_java_enable` | `true` | Install and set global Java (temurin-21) |
| `mise_node_enable` | `true` | Install and set global Node.js (22) |
| `mise_go_enable` | `true` | Install and set global Go (latest) |

### Roles Applied

```yaml
roles:
  - role: git
    git_gpg_sign: true
  - role: gpg
  - role: tmux
    tmux_tpm_enable: true
  - role: nvim
  - role: opencode
  - role: mise
```

### Example with Overrides

```yaml
# playbook override example: custom GPG key and Java version
ansible-playbook calaviaorg.setup.full_macos_setup \
  -e gpg_key_real_name="Your Name" \
  -e gpg_key_email="you@example.com" \
  -e mise_java_version="openjdk-21"
```

---

## License

GPL-2.0-or-later

## Author

Jorge Calavia <jorge@calavia.org>
