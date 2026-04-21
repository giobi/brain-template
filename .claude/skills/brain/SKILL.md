---
name: brain
description: "Brain package manager — install, update, list skills from registries"
user-invocable: true
argument-hint: "setup | install <skill> | update [skill] | nuove | list [--available] | uninstall <skill> | info <skill> | doctor [semantic] | diff"
---

# /brain — Package Manager

Manages skill installation from remote registries into the brain.

## Commands

```
/brain setup                    Fresh brain setup — fetch install promptone and run onboarding
/brain install <skill>          Install a skill from registry
/brain install <repo>/<skill>   Install from a specific repo
/brain update [skill]           Update one or all installed skills
/brain list                     List installed skills
/brain list --available         List skills available in registry
/brain uninstall <skill>        Remove an installed skill
/brain info <skill>             Show skill details and parameters
/brain doctor                   Health check: frontmatter, index.md, requires, .env
/brain doctor semantic          Deep content analysis: duplicates, misplaced files, stubs, merge candidates
/brain diff [skill]             Show differences between installed and upstream
```

## NLP Intent Detection

Parse `$ARGUMENTS` with natural language before dispatching to the right flow:

```python
args = "$ARGUMENTS".strip().lower()

if not args:
    intent = "list_installed"
elif any(w in args for w in ["setup", "start", "init", "inizia", "onboarding", "installa brain", "nuovo brain"]):
    intent = "setup"
elif any(w in args for w in ["nuove", "novità", "new", "aggiornam", "updates", "cosa c'è", "cosa ci sono", "cosa è uscito", "mancanti", "missing"]):
    intent = "whats_new"
elif any(w in args for w in ["install", "installa", "aggiungi", "add"]):
    intent = "install"
    skill_name = args.split()[-1]
elif any(w in args for w in ["update", "aggiorna"]) and "--available" not in args:
    intent = "update"
    skill_name = args.replace("update","").replace("aggiorna","").strip() or None
elif any(w in args for w in ["list", "lista", "elenca", "--available", "disponibili", "tutte"]):
    intent = "list_available" if "--available" in args or any(w in args for w in ["disponibili","tutte","registry"]) else "list_installed"
elif any(w in args for w in ["uninstall", "rimuovi", "disinstalla", "remove"]):
    intent = "uninstall"
elif any(w in args for w in ["info", "dettaglio", "cos'è", "cose"]):
    intent = "info"
elif any(w in args for w in ["doctor", "check", "salute", "stato"]):
    if any(w in args for w in ["semantic", "semantico", "deep", "pulisci", "cleanup", "merge", "mergia", "riordina", "contenuto", "contenuti"]):
        intent = "doctor_semantic"
    else:
        intent = "doctor"
elif any(w in args for w in ["diff", "differenze", "cambiamenti"]):
    intent = "diff"
else:
    intent = "install"  # default: try to install whatever was named
    skill_name = args.split()[0]
```

## Flow: setup

When `intent == "setup"`:

1. Fetch the install promptone:

```bash
curl -sL https://brainprotocol.it/install
```

2. Read the fetched content completely and follow all instructions.

This is equivalent to the user running `curl -sL https://brainprotocol.it/install` and pasting the result as a prompt — just automated.

---

## Architecture

```
.claude/skills/{name}/          <- Code (from registry, replaceable on update)
  SKILL.md                       Skill instructions
  *.py, *.sh                     Supporting scripts

wiki/skills/                    <- Brain-specific configuration (survives updates)
  index.yaml                    Registry of installed skills
  {name}.md                      Per-skill parameters and customization
```

**Key principle:** `.claude/skills/` = code (updatable). `wiki/skills/` = config (yours forever).

## GitHub API Helper

All registry operations need to fetch from GitHub. Use `gh` if available, fall back to `curl` (works without auth on public repos).

```bash
# Helper function — use this pattern everywhere
fetch_github() {
  local endpoint="$1"
  if command -v gh &>/dev/null; then
    gh api "$endpoint"
  else
    curl -sf "https://api.github.com/$endpoint"
  fi
}

# Examples:
# fetch_github "repos/giobi/claude-skills/contents/.claude-plugin/marketplace.json"
# fetch_github "repos/giobi/claude-skills/tarball/main" > /tmp/repo.tar.gz
```

**IMPORTANT:** Always try `gh` first (handles auth for private repos), fall back to `curl -sf` (silent, fail on error). Both return the same JSON from GitHub API.

## Install Flow

When user says `/brain install <skill>`:

### Step 1: Resolve registry

Read `wiki/skills/index.yaml` for the default registry. Default: `giobi/claude-skills`.

If user specifies `<repo>/<skill>` (e.g. `someone/their-skills/brainstorm`), use that repo instead.

### Step 2: Fetch marketplace

```bash
# Fetch marketplace.json — gh with curl fallback
MARKETPLACE_B64=$(fetch_github "repos/{owner}/{repo}/contents/.claude-plugin/marketplace.json" | python3 -c "import sys,json; print(json.load(sys.stdin)['content'])")
echo "$MARKETPLACE_B64" | base64 -d > /tmp/marketplace.json
```

Find the skill in the `plugins` array. If not found, show available skills and abort.

### Step 3: Download skill files

```bash
# Download the plugin directory — gh with curl fallback
cd /tmp
if command -v gh &>/dev/null; then
  gh api "repos/{owner}/{repo}/tarball/main" > repo.tar.gz
else
  curl -sfL "https://api.github.com/repos/{owner}/{repo}/tarball/main" -o repo.tar.gz
fi
tar xzf repo.tar.gz
# Find and copy the skill
mkdir -p .claude/skills/{skill}/
cp -r */plugins/{skill}/skills/{skill}/* .claude/skills/{skill}/
# Also copy scripts if they exist
cp -r */plugins/{skill}/skills/{skill}/scripts/* .claude/skills/{skill}/ 2>/dev/null
# Cleanup
rm -rf /tmp/repo.tar.gz /tmp/*-claude-skills-*
```

### Step 4: Check requires and dependencies

Read the skill's SKILL.md frontmatter.

**Gate: requires.capabilities** — If the skill has `requires.capabilities`, check `boot/local.yaml`:

```python
import yaml

with open('boot/local.yaml') as f:
    local = yaml.safe_load(f) or {}

# capabilities is a flat list: ['discord', 'telegram', ...]
capabilities = local.get('capabilities', [])
services = local.get('services', {})

# Check each required capability
for cap in skill_requires.get('capabilities', []):
    if cap not in capabilities and not services.get(cap):
        print(f"BLOCKED: skill requires '{cap}' but boot/local.yaml doesn't have it.")
        print(f"Add '{cap}' to the capabilities list in boot/local.yaml, then retry.")
        sys.exit(1)
```

If a required capability is missing → **stop install**, tell the user what to add to `boot/local.yaml`. Do NOT install anyway.

**Config tiers** — after install, when a skill needs non-secret config:
- `wiki/skills/{name}.yaml` — non-secret config (bot name, channel, address, etc.)
- `.env` — secrets only (tokens, API keys, passwords)
- `boot/local.yaml` — machine/infra only (services installed, network, capabilities list)

**Gate: requires.env** — If the skill has `requires.env`, check `.env`:

```bash
for key in ${required_env[@]}; do
  grep -q "^${key}=" .env 2>/dev/null || echo "WARNING: $key not found in .env — skill may not work"
done
```

Missing env keys are a **warning**, not a blocker (user may add them later).

**Dependencies** — If `depends:` field lists other skills, install them first (recursive).

### Step 5: Create parameter file

Create `wiki/skills/{skill}.md` via brain_writer:

```python
import sys; sys.path.insert(0, '.claude/skills/brain-writer')
from brain_writer import create_entity

create_entity('skills', skill_name, f'''
Parameters for skill **{skill_name}**.

## Configuration

_No configuration needed._
''', entity_type='tech', tags=['skill', 'installed', skill_name])
```

### Step 6: Post-install

If the skill directory contains `POSTINSTALL.md`, read it and execute the instructions. This typically asks the user for configuration (e.g., style samples for ghostwriter, API keys for external services).

### Step 7: Update registry

Update `wiki/skills/index.yaml`:

```yaml
installed:
  {skill_name}:
    source: {owner}/{repo}
    version: {version from plugin.json}
    installed_at: {today}
```

### Step 8: Confirm

```
Installed: {skill_name} v{version}
   Source: {registry}
   Config: wiki/skills/{skill_name}.md
   Use: /{skill_name}
```

## Update Flow

When user says `/brain update [skill]`:

### Single skill
1. Read `wiki/skills/index.yaml` -> get source and current version
2. Fetch latest from registry
3. Compare versions — if same, skip
4. **Overwrite** `.claude/skills/{skill}/` with new code
5. **DO NOT touch** `wiki/skills/{skill}.md` (user parameters are sacred)
6. Update version in `index.yaml`
7. If POSTINSTALL.md changed, notify user of new config options

### All skills
Loop through all entries in `index.yaml` `installed:` section.

## Uninstall Flow

1. Delete `.claude/skills/{skill}/` directory
2. Ask user: "Keep config in wiki/skills/{skill}.md? (y/n)"
3. Remove entry from `index.yaml`

## List Flow

### `/brain list` (installed)
Read `index.yaml`, show table:
```
Skill         Version  Source              Installed
brainstorm    1.0.0    giobi/claude-skills 2026-03-20
stalker       1.0.0    giobi/claude-skills 2026-03-20
```

### `/brain list --available`
Fetch marketplace.json, show all plugins with descriptions. Mark installed ones with checkmark.

## What's New Flow

Triggered by: `/brain nuove`, `/brain aggiornamenti`, `/brain che skill nuove ci sono?` etc.

### Step 1: Fetch marketplace

```bash
MARKETPLACE_B64=$(fetch_github "repos/giobi/claude-skills/contents/.claude-plugin/marketplace.json" | python3 -c "import sys,json; print(json.load(sys.stdin)['content'])")
marketplace=$(echo "$MARKETPLACE_B64" | base64 -d)
```

### Step 2: Read installed skills

```python
import yaml
with open('wiki/skills/index.yaml') as f:
    idx = yaml.safe_load(f) or {}
installed = idx.get('installed', {})  # {name: {version, installed_at, source}}
```

### Step 3: Compare

```python
import json

registry_plugins = {p['name']: p for p in marketplace_data['plugins']}

new_skills = []       # in registry, NOT installed
updates_available = []  # installed BUT registry version > local version

for name, plugin in registry_plugins.items():
    if name not in installed:
        new_skills.append(plugin)
    else:
        reg_ver = plugin.get('version', '0.0.0')
        loc_ver = installed[name].get('version', '0.0.0')
        if reg_ver != loc_ver:
            updates_available.append({**plugin, 'installed_version': loc_ver})
```

### Step 4: Output

```
/brain nuove

🆕 Skills not yet installed (5):
  telegram     Telegram Bot — send messages, read inbox, manage bot interactions
  discord      Discord Bot — send messages to channels, DMs, and project channels
  gmail        Gmail orchestrator — read, triage, draft in-thread replies
  imagen       AI image generation — Gemini Imagen, fal.ai, Replicate Flux
  schedule     Schedule manager — list, add, edit brain scheduled tasks

🔄 Updates available (2):
  brainstorm   v1.0.0 → v1.1.0
  save         v1.0.0 → v1.1.0

To install: /brain install <nome>
To update all: /brain update
```

If there's nothing new:
```
All up to date ✓ — 28 skills installed, nothing new in registry.
```

## Info Flow

`/brain info stalker`:
1. Read `index.yaml` for install info
2. Read `.claude/skills/stalker/SKILL.md` for description
3. Read `wiki/skills/stalker.md` for current parameters
4. Show combined info

## Parameter Pattern

Skills that need user configuration include a `parameters:` section in their SKILL.md frontmatter:

```yaml
---
name: ghostwriter
parameters:
  - name: style_samples
    description: "Writing samples in the user's voice"
    required: true
  - name: tone
    description: "Default tone (formal/informal/technical)"
    default: informal
---
```

During install, if `parameters:` exist with `required: true`, the post-install prompts the user. Parameters are stored in `wiki/skills/{name}.md` frontmatter.

At runtime, the SKILL.md instructions say: "Read your parameters from `wiki/skills/{name}.md`".

## Doctor Flow

`/brain doctor` — health check of the entire brain:

### Checks (run all, report at end):

1. **boot/ files exist**: brain.md, soul.md, user.md — MUST exist. local.yaml, domain.md — optional.
2. **Frontmatter valid**: Scan all `.md` in wiki/ and diary/ — each MUST have valid YAML frontmatter with at least `date` and `type`. **Also flag any file named `README.md` or `LICENSE.md` as a naming violation** — these are anti-patterns in the brain. Files must have semantic names (e.g. `deploy-guide.md`, `concept.md`, `tech-stack.md`). `index.md` is the only reserved generic name (directory index).
3. **index.md/index.yaml present**: Every directory in wiki/ SHOULD have an index.md or index.yaml.
4. **Diary has project**: Every diary entry SHOULD have `project:` in frontmatter. Skip `index.md` files (directory indexes, not entries).
5. **Skill requires satisfied**: For each installed skill, read its SKILL.md `requires:` and check against `boot/local.yaml`. Report unmet capabilities.
6. **Env keys present**: For skills with `requires.env`, check `.env` for the keys.
7. **Orphan skills**: Skills in `.claude/skills/` not listed in `wiki/skills/index.yaml` (neither `installed:` nor anywhere in the `native:` section). Read the full `native:` subtree from index.yaml and flatten all skill names from all sub-lists (zero_deps, needs_services.*, needs_capabilities.*, depends.*). Also treat bundled brain skills as always-known: brain, brain-writer, save, bye, project, sessions, todo, engine.
8. **Dotted files**: Check for any remaining `.index.yaml` or `.index.md` (should be `index.yaml`/`index.md`).
9. **Memory guardian hook**: The brain MUST block Claude's built-in memory system (`~/.claude/projects/*/memory/`). The brain IS the memory — Claude's `memory/` directory is redundant and pollutes the system. Check:
   - `.claude/hooks/memory-guardian.sh` exists and is executable
   - `.claude/settings.json` has the hook registered on BOTH `Write` and `Edit` matchers in `PreToolUse`
   - If either is missing → **FAIL** (not WARN) and **auto-fix**: create the hook script and register it in settings.json.

   **Auto-fix: create hook** (if missing):
   ```bash
   cat > .claude/hooks/memory-guardian.sh << 'HOOK'
   #!/bin/bash
   # Memory Guardian — blocks writes to Claude's memory/ directory
   # The brain IS the memory. Claude's built-in memory/ is not used.
   set -euo pipefail
   input=$(cat)
   file_path=$(echo "$input" | jq -r '.tool_input.file_path // empty')
   if [[ -z "$file_path" ]]; then
     jq -n '{decision:"approve",reasoning:"No file_path"}'
     exit 0
   fi
   if [[ "$file_path" =~ memory/ ]]; then
     jq -n '{decision:"block",reasoning:"memory/ blocked by brain",message:"BLOCKED: memory/ is not used. The brain (wiki/, diary/, boot/) is your memory."}'
     exit 2
   fi
   jq -n '{decision:"approve",reasoning:"Not a memory path"}'
   exit 0
   HOOK
   chmod +x .claude/hooks/memory-guardian.sh
   ```

   **Auto-fix: register in settings.json** (if hook exists but not registered):
   Read `.claude/settings.json`, ensure `hooks.PreToolUse` has the memory-guardian on both Write and Edit matchers. Use `jq` or Python to merge without clobbering existing hooks. The command path must use `$CLAUDE_PROJECT_DIR/.claude/hooks/memory-guardian.sh`.

### Output format:

```
/brain doctor

PASS  boot/ files complete
PASS  Frontmatter valid (342/342 files)
WARN  Missing index.md in 3 directories
      - wiki/sessions/
      - wiki/skills/
      - storage/awareness/
WARN  12 diary entries without project in frontmatter
PASS  All skill requires satisfied
WARN  FIGMA_ACCESS_TOKEN not in .env (needed by figma)
PASS  No orphan skills
PASS  No dotted index files

Score: 8/8 checks, 3 warnings
```

Severity: FAIL = broken, needs fix. WARN = suboptimal, should fix. PASS = good.

## Doctor Semantic Flow

`/brain doctor semantic` — deep content analysis, interactive cleanup.

Unlike the structural doctor (which checks format and structure), the semantic doctor **reads the actual content** of every file, understands what it says, and finds issues that only a human (or a very attentive AI) would notice.

### What it detects

Scan the entire brain and classify findings into these categoriess:

| Category | Icon | What it means |
|----------|------|---------------|
| **ROGUE** | 📁 | Folders/files outside the standard brain structure (not in boot/, wiki/, diary/, todo/, inbox/, public/, storage/, .env) |
| **STUB** | 📄 | Files with frontmatter but empty or near-empty body (<20 words of actual content) |
| **MISPLACED** | 📍 | Content in the wrong location (e.g., project docs in storage/, notes in root, README.md instead of index.md) |
| **DUPLICATE** | 🔄 | Same topic/entity described in multiple files (e.g., same person in wiki/people/ AND referenced inline in a project) |
| **MERGE** | 🔀 | Files that logically belong together (e.g., a project with only 1 file that could be folded into the project index) |
| **STALE** | ⏰ | TODOs referencing completed work, projects with outdated status, entries with old dates and no updates |
| **BLOAT** | 🫧 | Files that are too large and should be split, or contain multiple unrelated topics |
| **ORPHAN** | 👻 | Files not linked from anywhere, not tagged properly, not findable via normal navigation |
| **NAMING** | 🏷️ | Files violating naming conventions (uppercase, underscores, spaces, README.md, non-semantic names) |

### How it works

#### Step 1: Full scan

Read every `.md` and `.yaml` file in the brain. For each file, note:
- Path and name
- Frontmatter (type, tags, date, project)
- Body content (first 500 chars minimum, full text for small files)
- Size (lines, words)
- Last modified date

Also scan for:
- Non-standard root folders (anything not in the allowed list)
- Files without frontmatter in wiki/ and diary/
- Non-.md files in unexpected places

#### Step 2: Content analysis

For each file, determine:
- **What entity/topic it's about** (person, project, concept, how-to, log)
- **Whether it overlaps** with other files (same person, same project, same topic)
- **Whether it's in the right place** (a person described in projects/ → should be in people/)
- **Whether it's complete** (stub check: frontmatter-only or near-empty body)
- **Whether it's current** (stale check: old TODOs, outdated status)

Cross-reference:
- wiki/people/ entries vs. names mentioned in projects and diary
- wiki/projects/ entries vs. project tags in diary and todo
- TODOs vs. diary entries (was the TODO completed but not closed?)

#### Step 3: Interactive presentation

Present findings ONE CATEGORY AT A TIME, starting from the most impactful:

```
🧠 Brain Doctor Semantic — Analisi completa

Found 12 issues in 5 categories.

---

📁 ROGUE — Folders/files outside standard structure (2 found)

  1. `progetti/DHL/` — non-standard folder in root.
     Contains: README.md (boilerplate React+Vite), no brain .md files.

     What do you want to do?
     [a] Move to storage/dhl/
     [b] Move to wiki/projects/dhl/
     [c] Delete (no brain data)
     [d] Leave as is (skip)

  2. `progetti/EsercizioLoginEcommerce_SpringBoot.zip` — .zip file in root

     What do you want to do?
     [a] Move to storage/
     [b] Delete
     [c] Skip
```

**IMPORTANT interaction rules:**
- Present ONE category at a time
- Wait for the user to respond to ALL items in the category before moving to the next
- For each finding, provide 2-4 concrete action options plus "skip"
- If the user says "fix all" or "sistema tutto" for a category, apply the recommended action (first option) to all items
- After the user decides, **execute the action immediately** (move, delete, merge files)
- Show a summary at the end of what was changed

#### Step 4: Execute actions

For each user decision:

- **Move**: Use filesystem commands to relocate the file. Update frontmatter if needed (e.g., change `type:` if moving between domains). Fix any wiki-links pointing to the old path.
- **Delete**: Remove the file. If it was in an index, update the index.
- **Merge**: Read both files, combine content intelligently (keep the richer version, append unique info from the other), write the merged file, delete the duplicate.
- **Enrich**: For stubs, add a TODO prompt: "This file needs content. Would you like to describe [entity] now?"
- **Rename**: Fix naming violations (lowercase, hyphens, semantic name).

#### Step 5: Summary

```
🧠 Doctor Semantic — Riepilogo

Executed: 8 actions
  - 2 files moved (progetti/ → storage/)
  - 3 stubs enriched
  - 1 file renamed
  - 2 skipped

The brain is cleaner. Suggested next step: /brain doctor (structural check).
```

### Notes

- The semantic doctor is conversational — it's a dialogue, not a report
- Always explain WHY something is a finding, not just WHAT
- Respect user decisions — if they skip something, don't nag
- After execution, if the brain has git, suggest a commit with the changes
- Can be triggered with NLP: "clean up the brain", "reorganize", "what needs fixing", "merge duplicates"

## Diff Flow

`/brain diff [skill]` — show differences between installed skill and upstream:

### Single skill

1. Read installed version from `wiki/skills/index.yaml`
2. Fetch upstream SKILL.md from registry (same fetch_github helper)
3. Compare the two SKILL.md files — show a readable diff
4. If other files exist in the skill dir, note which ones differ

### All skills

Loop through installed skills, show summary:

```
/brain diff

brainstorm    UP TO DATE  (v1.0.0)
stalker       CHANGED     3 lines differ in SKILL.md
public        UP TO DATE  (v1.0.0)
learn         NOT IN REGISTRY  (native skill)
```

## Notes

- Skills are flat in `.claude/skills/` — no nesting, no prefixes
- The registry is just a GitHub repo with a `marketplace.json`
- Anyone can create a registry — just follow the plugin structure
- `wiki/skills/` is managed by brain_writer, follows brain conventions
- Works with `gh` (private repos) or `curl` (public repos) — no hard dependency on either
