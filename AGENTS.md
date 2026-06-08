# Agent Instructions — calaviaorg.setup

## Project Overview

Ansible collection for setting up local development environments (git, tmux, GPG, Neovim, OpenCode, mise). Published to Ansible Galaxy as `calaviaorg.setup`.

## Repository Layout

```
.
├── collections/ansible_collections/calaviaorg/setup/  # Collection root
│   ├── roles/          # tmux, git, gpg, nvim, opencode, mise
│   ├── playbooks/      # full_macos_setup, dev_machine
│   └── galaxy.yml      # Collection manifest (version source of truth)
├── tests/              # unit/ and integration/ tests
├── molecule/           # Molecule scenarios per role + darwin/
├── tox-ansible.ini     # Tox config for ansible-test
└── .github/workflows/  # PR checks and auto-bump
```

## Environment Setup

- **Python**: 3.12+ required
- **Virtualenv**: `python3 -m venv .venv && source .venv/bin/activate`
- **Dependencies**: `pip install -r requirements.txt`
- **Ansible**: 2.19+ required

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

# Available scenarios: darwin, git, gpg, mise, nvim, opencode, tmux
molecule test -s git
```

**Important**: Molecule tests build and install the collection from a git archive. The collection must be buildable before molecule tests work.

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
