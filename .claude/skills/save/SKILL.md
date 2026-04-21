---
name: save
description: "Mid-session checkpoint (log, database, commit, push) without closing"
user-invocable: true
argument-hint: "[note]"
---

**Mid-Session Checkpoint** - Save progress without ending the session

Alias: `/checkpoint`

## What it does:

1. Create/update session log (append mode)
2. Apply Post-Action Protocol (update project + database entities)
3. Update diary if significant
4. Git commit + push
5. **Continue working** (session stays open)

## When to use:

- After completing a significant chunk of work
- After external actions (email sent, deploy, DNS change)
- Before switching project/topic mid-session
- Long sessions where losing context would hurt

## Instructions:

### Step 1: Session Log (Append Mode)

If a log for today + current project already exists, **append** to it. Otherwise create new.

```python
import os, glob

existing = glob.glob(f'diary/2026/2026-MM-DD-{project}-*.md')

if existing:
    # Append: ## Checkpoint HH:MM
    pass
else:
    from brain_writer import create_log
    create_log('YYYY-MM-DD', '{project}-checkpoint', """
## Work Done (checkpoint)
- [bullet points of work so far]

## Status
In progress - session continues
""", tags=['session', 'checkpoint', '{project}'], project='{project}')
```

**Status**: Always `open` (session is still active).

### Step 2: Post-Action Protocol

#### 2a. Update project file (ALWAYS)

| What | Where it goes | Where it does NOT go |
|------|---------------|----------------------|
| Current status | `index.md` — ONE line, REPLACE | Don't append timeline |
| Dated events | `diary/YYYY/` with project tag | NOT in index.md |
| Issue tracking | `{project}/issues.md` | NOT in index.md |

#### 2b. Update people/companies (if relevant)

#### 2c. Update diary (if there's concrete work)

#### 2d. When to ask vs. act
- **Act without asking**: updating existing files, appending to diary
- **Ask first**: creating new project files
- **Heuristic**: if 80%+ confident, just do it

### Step 3: Cleanup Backup Files

```bash
ls -t .claude.json.backup.* 2>/dev/null | tail -n +3 | xargs rm -f 2>/dev/null
```

### Step 4: Git Commit + Push

```bash
git add -A && git commit -m "Checkpoint: {project} - {brief summary}

Co-Authored-By: Claude <noreply@anthropic.com>"

git push origin $(git branch --show-current)
```

### Step 5: Update Tmux Pane Title

```bash
~/.tmux/set-pane-title.sh "EMOJI project / phase"
```

### Step 6: Pending Items Review

```
Still pending:
- [item 1] — [why it's open]
- [item 2] — [why it's open]
(or: nothing pending)
```

### Output

```
Checkpoint saved
diary/2026/2026-MM-DD-project-desc.md (updated)
Project: wiki/projects/{project}/index.md (updated)
Pushed to {branch}
```

## Args Provided:
```
$ARGUMENTS
```
