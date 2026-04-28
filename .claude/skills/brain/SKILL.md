---
name: brain
description: "Brain package manager — install, update, list skills from registries"
user-invocable: true
argument-hint: "setup | install <skill> | update [skill] | list [--available] | uninstall <skill> | info <skill> | doctor [semantic] | diff"
---

# /brain — Package Manager

Manages skill installation from remote registries into the brain.

## Commands

```
/brain setup                    Fresh brain setup — fetch install prompt and run onboarding
/brain install <skill>          Install a skill from registered sources
/brain install <repo>/<skill>   Install from a specific GitHub repo
/brain update [skill]           Update one or all installed skills
/brain list                     List installed skills
/brain list --available         List skills available across all registries
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

1. Fetch the install prompt from the Brain Protocol website (use wget or python urllib)
2. Read the fetched content completely and follow all instructions.

This is equivalent to the user fetching `https://brainprotocol.ai/install` and pasting the result as a prompt — just automated.

---

## Architecture

```
boot/skills.yaml                <- Registered skill sources (GitHub repos, local paths, APIs)

.claude/skills/{name}/          <- Code (from registry, replaceable on update)
  SKILL.md                       Skill instructions
  *.py, *.sh                     Supporting scripts

wiki/skills/                    <- Brain-specific configuration (survives updates)
  index.yaml                    Registry of installed skills
  {name}.yaml                    Per-skill parameters and customization
```

**Key principle:** `boot/skills.yaml` = where to find skills. `.claude/skills/` = code (updatable). `wiki/skills/` = config (yours forever).

## Skill Registries

Skills can come from multiple sources. Each brain declares its registries in `boot/skills.yaml`:

```yaml
# boot/skills.yaml
registries:
  - name: official
    type: github
    repo: brainprotocol/skills
  - name: my-company
    type: github
    repo: acme/brain-skills
  - name: internal
    type: local
    path: /opt/brain-skills/
```

Supported registry types:

| Type | Source | Manifest location |
|------|--------|-------------------|
| `github` | GitHub repo | `manifest.yaml` at repo root |
| `local` | Local filesystem path | `manifest.yaml` at path root |
| `api` | HTTP endpoint | GET `{url}/manifest.yaml` |

Each registry MUST have a `manifest.yaml` at its root:

```yaml
# manifest.yaml — skill registry manifest
name: "Official Brain Protocol Skills"
version: "1.0.0"
url: "https://github.com/brainprotocol/skills"

skills:
  telegram:
    version: "1.0.0"
    description: "Telegram Bot — send messages, read inbox"
    min_brain: "5.0"
    engines: [claude-code, gemini-cli, cursor]
    requires:
      capabilities: [telegram]
      env: [TELEGRAM_BOT_TOKEN]
    path: skills/telegram/   # relative to registry root

  discord:
    version: "1.2.0"
    description: "Discord Bot — channels, DMs, reactions"
    min_brain: "5.0"
    engines: [claude-code]
    requires:
      capabilities: [discord]
      env: [DISCORD_BOT_TOKEN]
    path: skills/discord/
```

## GitHub API Helper

Registry operations that fetch from GitHub repos use `gh` if available, falling back to Python urllib (works without auth on public repos).

```python
import subprocess, urllib.request, json

def fetch_github(endpoint):
    """Fetch from GitHub API — gh first, urllib fallback."""
    try:
        result = subprocess.run(['gh', 'api', endpoint], capture_output=True, text=True)
        if result.returncode == 0:
            return json.loads(result.stdout)
    except FileNotFoundError:
        pass
    req = urllib.request.Request(
        f'https://api.github.com/{endpoint}',
        headers={'Accept': 'application/vnd.github.v3+json'}
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())
```

**IMPORTANT:** Always try `gh` first (handles auth for private repos), fall back to urllib (no external deps). Both return the same JSON from GitHub API.

## Install Flow

When user says `/brain install <skill>`:

### Step 1: Resolve registry

Read `boot/skills.yaml` for the list of registries. Search them in order until the skill is found.

If user specifies `<repo>/<skill>` (e.g. `acme/brain-skills/telegram`), use that repo directly — skip registry search.

### Step 2: Fetch manifest

For each registry (in order), fetch and parse `manifest.yaml`:

```python
import base64, yaml

# For github type:
resp = fetch_github(f"repos/{owner}/{repo}/contents/manifest.yaml")
manifest = yaml.safe_load(base64.b64decode(resp['content']))

# For local type:
with open(f"{path}/manifest.yaml") as f:
    manifest = yaml.safe_load(f)
```

Find the skill in the `skills` map. If not found in any registry, show available skills and abort.

### Step 3: Download skill files

```python
import tarfile, io, shutil

# For github type — download the repo tarball
resp = fetch_github(f"repos/{owner}/{repo}/tarball/main")
# ... extract and copy skill files from manifest path

# For local type — direct copy
shutil.copytree(f"{path}/{manifest_path}", f".claude/skills/{skill}/", dirs_exist_ok=True)
```

### Step 4: Check requires and dependencies

Read the skill's SKILL.md frontmatter.

**Gate: requires.capabilities** — If the skill has `requires.capabilities`, check `boot/local.yaml`:

```python
import yaml

with open('boot/local.yaml') as f:
    local = yaml.safe_load(f) or {}

capabilities = local.get('capabilities', [])
services = local.get('services', {})

for cap in skill_requires.get('capabilities', []):
    if cap not in capabilities and not services.get(cap):
        print(f"BLOCKED: skill requires '{cap}' but boot/local.yaml doesn't have it.")
        print(f"Add '{cap}' to the capabilities list in boot/local.yaml, then retry.")
        sys.exit(1)
```

If a required capability is missing -> **stop install**, tell the user what to add to `boot/local.yaml`. Do NOT install anyway.

**Config tiers** — after install, when a skill needs non-secret config:
- `wiki/skills/{name}.yaml` — non-secret config (bot name, channel, address, etc.)
- `.env` — secrets only (tokens, API keys, passwords)
- `boot/local.yaml` — machine/infra only (services installed, network, capabilities list)

**Gate: requires.env** — If the skill has `requires.env`, check `.env`:

```python
import os
for key in skill_requires.get('env', []):
    if not os.environ.get(key) and key not in open('.env').read():
        print(f"WARNING: {key} not found in .env — skill may not work")
```

Missing env keys are a **warning**, not a blocker (user may add them later).

**Dependencies** — If `depends:` field lists other skills, install them first (recursive).

### Step 5: Create parameter file

Create `wiki/skills/{skill}.yaml` via brain_writer:

```python
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
    source: {registry_name}/{owner}/{repo}
    version: {version}
    installed_at: {today}
```

### Step 8: Confirm

```
Installed: {skill_name} v{version}
   Source: {registry_name}
   Config: wiki/skills/{skill_name}.yaml
   Use: /{skill_name}
```

## Update Flow

When user says `/brain update [skill]`:

### Single skill
1. Read `wiki/skills/index.yaml` -> get source and current version
2. Fetch latest from the source registry
3. Compare versions — if same, skip
4. **Overwrite** `.claude/skills/{skill}/` with new code
5. **DO NOT touch** `wiki/skills/{skill}.yaml` (user parameters are sacred)
6. Update version in `index.yaml`
7. If POSTINSTALL.md changed, notify user of new config options

### All skills
Loop through all entries in `index.yaml` `installed:` section.

## Uninstall Flow

1. Delete `.claude/skills/{skill}/` directory
2. Ask user: "Keep config in wiki/skills/{skill}.yaml? (y/n)"
3. Remove entry from `index.yaml`

## List Flow

### `/brain list` (installed)
Read `index.yaml`, show table:
```
Skill         Version  Source              Installed
telegram      1.0.0    official            2026-03-20
discord       1.2.0    my-company          2026-03-20
custom-tool   0.1.0    internal            2026-04-01
```

### `/brain list --available`
Fetch manifest.yaml from ALL registered sources, show combined list. Mark installed ones with checkmark.

## What's New Flow

Triggered by: `/brain nuove`, `/brain aggiornamenti`, `/brain che skill nuove ci sono?` etc.

### Step 1: Fetch all manifests

For each registry in `boot/skills.yaml`, fetch `manifest.yaml`.

### Step 2: Read installed skills

```python
import yaml
with open('wiki/skills/index.yaml') as f:
    idx = yaml.safe_load(f) or {}
installed = idx.get('installed', {})
```

### Step 3: Compare

```python
new_skills = []         # in any registry, NOT installed
updates_available = []  # installed BUT registry version > local version

for registry in registries:
    for name, skill in registry['skills'].items():
        if name not in installed:
            new_skills.append({**skill, 'name': name, 'registry': registry['name']})
        else:
            if skill['version'] != installed[name].get('version'):
                updates_available.append({**skill, 'name': name, 'installed_version': installed[name]['version']})
```

### Step 4: Output

```
/brain nuove

New skills available (5):
  telegram     Telegram Bot — send messages, read inbox              [official]
  discord      Discord Bot — channels, DMs, reactions                [official]
  custom-crm   Internal CRM integration                             [my-company]

Updates available (2):
  brainstorm   v1.0.0 -> v1.1.0                                     [official]
  save         v1.0.0 -> v1.1.0                                     [official]

To install: /brain install <name>
To update all: /brain update
```

If there's nothing new:
```
All up to date — {N} skills installed, nothing new in registries.
```

## Info Flow

`/brain info telegram`:
1. Read `index.yaml` for install info
2. Read `.claude/skills/telegram/SKILL.md` for description
3. Read `wiki/skills/telegram.yaml` for current parameters
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

During install, if `parameters:` exist with `required: true`, the post-install prompts the user. Parameters are stored in `wiki/skills/{name}.yaml`.

At runtime, the SKILL.md instructions say: "Read your parameters from `wiki/skills/{name}.yaml`".

## Doctor Flow

`/brain doctor` — health check of the entire brain:

### Checks (run all, report at end):

1. **boot/ files exist**: brain.md, soul.md, user.md — MUST exist. local.yaml, skills.yaml, domain.md — optional.
2. **Frontmatter valid**: Scan all `.md` in wiki/ and diary/ — each MUST have valid YAML frontmatter with at least `date` and `type`. **Also flag any file named `README.md` or `LICENSE.md` as a naming violation** — these are anti-patterns in the brain. Files must have semantic names (e.g. `deploy-guide.md`, `concept.md`, `tech-stack.md`). `index.md` is the only reserved generic name (directory index).
3. **index.md/index.yaml present**: Every directory in wiki/ SHOULD have an index.md or index.yaml.
4. **Diary has project**: Every diary entry SHOULD have `project:` in frontmatter. Skip `index.md` files (directory indexes, not entries).
5. **Skill requires satisfied**: For each installed skill, read its SKILL.md `requires:` and check against `boot/local.yaml`. Report unmet capabilities.
6. **Env keys present**: For skills with `requires.env`, check `.env` for the keys.
7. **Orphan skills**: Skills in `.claude/skills/` not listed in `wiki/skills/index.yaml`. Skills bundled with the brain protocol template (brain, devil) are always known.
8. **Dotted files**: Check for any remaining `.index.yaml` or `.index.md` (should be `index.yaml`/`index.md`).
9. **Registries reachable**: For each registry in `boot/skills.yaml`, verify the manifest is fetchable. WARN if unreachable.

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
PASS  All registries reachable

Score: 9/9 checks, 3 warnings
```

Severity: FAIL = broken, needs fix. WARN = suboptimal, should fix. PASS = good.

## Doctor Semantic Flow

`/brain doctor semantic` — deep content analysis, interactive cleanup.

Unlike the structural doctor (which checks format and structure), the semantic doctor **reads the actual content** of every file, understands what it says, and finds issues that only a human (or a very attentive AI) would notice.

### What it detects

Scan the entire brain and classify findings into these categories:

| Category | What it means |
|----------|---------------|
| **ROGUE** | Folders/files outside the standard brain structure (not in boot/, wiki/, diary/, todo/, inbox/, public/, storage/, .env) |
| **STUB** | Files with frontmatter but empty or near-empty body (<20 words of actual content) |
| **MISPLACED** | Content in the wrong location (e.g., project docs in storage/, notes in root, README.md instead of index.md) |
| **DUPLICATE** | Same topic/entity described in multiple files |
| **MERGE** | Files that logically belong together (e.g., a project with only 1 file that could be folded into the project index) |
| **STALE** | TODOs referencing completed work, projects with outdated status, entries with old dates and no updates |
| **BLOAT** | Files that are too large and should be split, or contain multiple unrelated topics |
| **ORPHAN** | Files not linked from anywhere, not tagged properly, not findable via normal navigation |
| **NAMING** | Files violating naming conventions (uppercase, underscores, spaces, README.md, non-semantic names) |

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
- **Whether it's in the right place** (a person described in projects/ should be in people/)
- **Whether it's complete** (stub check: frontmatter-only or near-empty body)
- **Whether it's current** (stale check: old TODOs, outdated status)

Cross-reference:
- wiki/people/ entries vs. names mentioned in projects and diary
- wiki/projects/ entries vs. project tags in diary and todo
- TODOs vs. diary entries (was the TODO completed but not closed?)

#### Step 3: Interactive presentation

Present findings ONE CATEGORY AT A TIME, starting from the most impactful. For each finding, provide 2-4 concrete action options plus "skip".

**Interaction rules:**
- Present ONE category at a time
- Wait for the user to respond to ALL items before moving to the next
- If the user says "fix all" for a category, apply the recommended action to all items
- After the user decides, execute the action immediately
- Show a summary at the end of what was changed

#### Step 4: Execute actions

For each user decision:
- **Move**: Relocate the file, update frontmatter if needed, fix wiki-links pointing to the old path.
- **Delete**: Remove the file, update any index that referenced it.
- **Merge**: Combine content intelligently, write merged file, delete the duplicate.
- **Enrich**: For stubs, prompt: "This file needs content. Would you like to describe [entity] now?"
- **Rename**: Fix naming violations (lowercase, hyphens, semantic name).

#### Step 5: Summary

```
Doctor Semantic — Summary

Executed: 8 actions
  - 2 files moved
  - 3 stubs enriched
  - 1 file renamed
  - 2 skipped

Suggested next step: /brain doctor (structural check).
```

### Notes

- The semantic doctor is conversational — it's a dialogue, not a report
- Always explain WHY something is a finding, not just WHAT
- Respect user decisions — if they skip something, don't nag
- After execution, if the brain has git, suggest a commit with the changes

## Diff Flow

`/brain diff [skill]` — show differences between installed skill and upstream:

### Single skill

1. Read installed version from `wiki/skills/index.yaml`
2. Fetch upstream SKILL.md from the source registry
3. Compare the two SKILL.md files — show a readable diff
4. If other files exist in the skill dir, note which ones differ

### All skills

Loop through installed skills, show summary:

```
/brain diff

telegram      UP TO DATE  (v1.0.0)
discord       CHANGED     3 lines differ in SKILL.md
custom-tool   UP TO DATE  (v0.1.0)
my-skill      NOT IN REGISTRY  (native skill)
```

## Notes

- Skills are flat in `.claude/skills/` — no nesting, no prefixes
- Anyone can create a registry — publish a repo with a `manifest.yaml` and skills in subdirectories
- `wiki/skills/` follows brain conventions for frontmatter and naming
- Works with `gh` (private repos) or Python urllib (public repos) — no hard dependency on either
- `brain_writer` is the core writing tool — it handles frontmatter, naming, and indexes
