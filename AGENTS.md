# Agent Instructions — calaviaorg.setup

> **MANDATORY READ**: This repository is governed by [`~/Development/Github/AGENTS.md`](../AGENTS.md) (organization-wide rules). Per-repo rules below provide project-specific details but **cannot override** organization rules.

## Project Overview

Ansible collection for setting up local development environments (git, tmux, GPG, Neovim, OpenCode, mise, cli_tools). Published to Ansible Galaxy as `calaviaorg.setup`.

### What This Collection Installs

| Category | Tools | Managed By |
|----------|-------|------------|
| Version Control | git, gh (GitHub CLI) | ansible role |
| Terminal | tmux + TPM plugins | ansible role |
| Editor | neovim + plugins | ansible role |
| AI Agent | opencode + engram plugin | ansible role |
| GPG | gnupg, pinentry-mac | ansible role |
| CLI Tools | bat, btop, eza, fd, fzf, htop, jq, lazygit, tree, wget, zoxide | ansible role |
| Languages | python, node, go, java | **mise** (not ansible directly) |
| Containerization | docker, docker-compose, docker-desktop | **manual install** |
| Terminal Emulator | ghostty | **manual install** |

> **Important**: Go, Node.js, and Rust are intentionally managed by `mise`, not by ansible roles. Use `mise use -g go@latest` or edit `~/.config/mise/config.toml` to change versions.

## Repository Layout

```
.
├── collections/ansible_collections/calaviaorg/setup/  # Collection root
│   ├── roles/          # tmux, git, gpg, nvim, opencode, mise, cli_tools
│   ├── playbooks/      # full_macos_setup, dev_machine
│   └── galaxy.yml      # Collection manifest (version source of truth)
├── tests/              # unit/ and integration/ tests
├── molecule/           # Molecule scenarios per role + darwin/
├── tox-ansible.ini     # Tox config for ansible-test
└── .github/workflows/  # PR checks and auto-bump
```

## Environment Setup

### Required

- **Python**: 3.12+ required
- **Ansible**: 2.19+ required
- **Virtualenv**: Mandatory — always use a venv
  ```bash
  python3 -m venv .venv
  source .venv/bin/activate
  pip install -r requirements.txt
  ```
- **mise**: Used for managing language versions (Go, Node.js, Python, Java)
  ```bash
  # After ansible installs mise
  mise use -g python@3.12
  mise use -g node@22
  mise use -g go@latest
  ```

### Manual Installations (Not in Ansible)

These must be installed manually on macOS:

| Tool | Install Command | Why Manual |
|------|----------------|------------|
| Docker Desktop | `brew install --cask docker` | Requires GUI setup and license acceptance |
| Docker Compose | Included with Docker Desktop | Bundled |
| Ghostty | `brew install --cask ghostty` | Terminal emulator with GPU acceleration |

> **Note**: Docker Desktop must be launched once manually to complete setup. Ghostty requires font configuration via its GUI preferences.

## Linting & Formatting

Run in this order:

```bash
# 1. Ruff (format + lint)
ruff format .
ruff check . --fix

# 2. Pre-commit (all hooks)
pre-commit run --all-files

# 3. Ansible-lint
ansible-lint

# 4. YAML lint
yamllint -c .yamllint .
```

**Note**: `ansible-lint` runs in offline mode (`offline: true` in `.ansible-lint`). Playbooks directory is excluded from linting.

## Testing

> **⚠️ CRITICAL**: Run ALL tests locally before pushing. CI will reject failing tests.

### Pre-Push Checklist

Before creating a PR or pushing commits:

```bash
# 1. Ensure venv is active
source .venv/bin/activate

# 2. Run linting
ruff format . && ruff check . --fix
pre-commit run --all-files

# 3. Run unit tests
tox -e unit-py3.12-2.17 --ansible --conf tox-ansible.ini

# 4. Run sanity tests
tox -e sanity-py3.12-milestone --ansible --conf tox-ansible.ini

# 5. Test affected role(s) with molecule
molecule test -s <role_name>

# 6. Verify collection builds
ansible-galaxy collection build
```

### Unit Tests

```bash
tox -e unit-py3.12-2.17 --ansible --conf tox-ansible.ini
```

### Sanity Tests

```bash
tox -e sanity-py3.12-milestone --ansible --conf tox-ansible.ini
```

### Molecule (Integration Tests)

```bash
# Run molecule for a specific role
molecule test -s <role_name>

# Available scenarios: darwin, git, gpg, mise, nvim, opencode, tmux, cli_tools
molecule test -s git
```

**Important**: Molecule tests build and install the collection from a git archive. The collection must be buildable before molecule tests work.

## Mise Usage

This collection uses [mise](https://mise.jdx.dev) as the version manager for programming languages. Ansible installs mise and configures shell activation, but language versions are managed via mise commands.

### Common Commands

```bash
# List installed tools
mise list

# Install or update a tool globally
mise use -g go@latest
mise use -g node@lts
mise use -g python@3.12

# View global config
cat ~/.config/mise/config.toml
```

### What Mise Manages (vs Ansible)

| Tool | Managed By | Notes |
|------|------------|-------|
| Python | mise | `mise_python_version: '3.12'` in ansible, but versions updated via `mise use` |
| Node.js | mise | `mise_node_version: '22'` |
| Go | mise | `mise_go_version: 'latest'` |
| Java | mise | `mise_java_version: 'temurin-21'` |
| Rust | **not in ansible** | Install manually: `mise use -g rust@latest` |

> **Why not ansible for languages?** Mise allows quick version switching and per-project versions via `.mise.toml`. Ansible only sets the initial global defaults.

## Collection Build

```bash
cd collections/ansible_collections/calaviaorg/setup
ansible-galaxy collection build
ansible-galaxy collection install calaviaorg-setup-*.tar.gz --force
```

## Version Management

- **Source of truth**: `collections/ansible_collections/calaviaorg/setup/galaxy.yml`
- Root `galaxy.yml` is a symlink/copy — do not edit directly for version bumps
- **Auto-bump**: CI handles version bumps on PR merge (see `.github/workflows/pr-check-and-bump.yml`)
- **Branch naming**: Use `major/`, `feat/`, `fix/`, `doc/` prefixes for changes that require a version bump
- **No-bump commits**: Use `chore/` prefix for changes that do NOT need a new collection version (e.g., documentation, CI tweaks, AGENTS.md updates). These run checks but skip the auto-bump.
- **Conventional commits**: Required

## CI / PR Workflow

- PRs target `main` or `release/*` branches
- CI runs: lint checks, tests, and auto-bumps version
- **No-bump workflow**: PRs from `chore/` branches run checks and tests but skip the version bump (handled by the centralized `calavia-org/workflows-lib` reusable workflow)
- Fails if branch name doesn't match `^(major|feat|fix|doc|chore)/.+`

## Gotchas

- **Collection path**: Tox sets `ANSIBLE_COLLECTIONS_PATH` to include `{env_tmp_dir}/collections` plus the local `collections/` dir. If running tests manually, ensure the collection is in the expected path.
- **Offline mode**: `ansible-lint` is offline-only — no Galaxy queries during linting.
- **Playbook exclusions**: Playbooks in `collections/.../playbooks/` are excluded from ansible-lint checks.
- **Galaxy.yml duplication**: There are two `galaxy.yml` files — root and collection. Root version is for repo metadata; collection version is the build artifact source.
- **Requirements**: `requirements.txt` has `ansible-lint>=26.4.0` and `molecule>=26.4.0` — these are the primary test tools.
- **Pre-commit hooks**: Must be installed inside the venv. The `pre-commit` package is in `requirements.txt`.
- **Manual tools**: Docker Desktop and Ghostty are not automated by ansible — install them manually after running the playbook.
- **Mise languages**: After ansible installs mise, run `mise install` to fetch the global language versions. Rust is not pre-configured — add it manually if needed.

## Memory Protocol (Engram)

You have access to Engram persistent memory via MCP tools. You MUST use them.

### WHEN TO SAVE (Mandatory)
Call `mem_save` IMMEDIATELY after:
- Bug fixes (type: `bugfix`)
- Architecture or design decisions (type: `decision`)
- Important discoveries or gotchas (type: `discovery`)
- Configuration changes (type: `config`)
- Patterns or conventions established (type: `pattern`)
- User preferences or constraints (type: `preference`)

Format:
- **title**: Short, searchable (e.g., "Fixed N+1 query in UserList")
- **type**: `bugfix` | `decision` | `architecture` | `discovery` | `pattern` | `config` | `preference`
- **content**: Use this format:
  **What**: One sentence — what was done
  **Why**: What motivated it
  **Where**: Files or paths affected
  **Learned**: Gotchas, edge cases, decisions made

### WHEN TO SEARCH (Proactive + Reactive)
- **Reactive**: User says "remember", "recall", "what did we do", "how did we solve"
- **Proactive**: Starting work that might overlap past sessions, unfamiliar module, debugging recurring issues

Call `mem_search` or `mem_context` with relevant keywords.

### SESSION CLOSE (Mandatory)
Before ending ANY session, call `mem_session_summary` with:
- **Goal**: What we were building/working on
- **Discoveries**: Technical findings, gotchas
- **Accomplished**: Completed tasks with file paths
- **Next Steps**: What remains
- **Relevant Files**: `path/to/file` — what it does or what changed

This is NOT optional. If you skip this, the next session starts blind.

### AFTER COMPACTION (Mandatory)
After any context compaction or reset:
1. Call `mem_context` to recover previous session state
2. Call `mem_session_summary` with the compacted summary before continuing
3. Save any critical memories that were lost in compaction

### Anti-Patterns (NEVER)
- NEVER silently ignore memory tools
- NEVER say "I don't have memory" when you have Engram tools
- NEVER skip `mem_session_summary` before ending
- NEVER forget to recover context after compaction
